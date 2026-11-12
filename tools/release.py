#!/usr/bin/env python3
"""Weekly-release mechanism for the public site.

The private dev repo (remote `dev-origin`, branch `dev`) always holds the
FULL course; the public site (this repo's `main`, served by GitHub Pages)
shows only released sessions. The contents page lists the whole syllabus,
with unreleased sessions as plain text instead of links; unreleased page
files are absent from the deployed tree (docs/404.html catches deep links).

State: RELEASED-SESSIONS at the repo root, one session number per line.
Anything in dev's index between <!-- DEV-ONLY-START --> and
<!-- DEV-ONLY-END --> is dropped from the public index; a
<span id="release-note"> in dev's index replaces the default note.
The public docs/index.html is GENERATED (from dev's index + the RELEASED
list) — never hand-edit it on main; edit dev's index instead.

Usage, from the repo root on a clean main:

    python3 tools/release.py init 1 2 3 4   # first gating: set the list,
                                            # trim the tree, rebuild index
    python3 tools/release.py 5              # release session 5 (also
                                            # re-syncs already-released
                                            # files from dev)
    python3 tools/release.py sync           # no new sessions; pull dev's
                                            # revisions to released weeks

Add --prune to any of these to remove files from main that dev has deleted
within the synced paths; without it, a run that finds such files lists them
and stops before changing anything.

Each run: fetch dev-origin/dev -> update RELEASED-SESSIONS -> checkout
released sessions' files + about/disclaimer/assets from dev -> regenerate
the gated index -> delete unreleased session files -> add_page_nav.py ->
commit. It does NOT push; review the diff, then:
    git push origin main && git push dev-origin main
(Never force dev to main: the dev branch keeps the full course.)
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RELEASED_FILE = ROOT / "RELEASED-SESSIONS"
SYNC_PATHS = ["docs/assets", "docs/labs", "docs/about.html", "docs/ai-disclaimer.html",
              # the 2026 taught-route pages, which sit outside session-NN
              "docs/short-course-2026.html",
              "docs/sessions/project-kickoff-short-course.html"]
RELEASE_NOTE = (
    '<span id="release-note">Sessions are released week by week as the '
    "course runs; syllabus entries without links are still to come.</span> "
)


def run(*cmd, capture=False):
    if cmd[0] == "git":
        cmd = ("git", "-C", str(ROOT), *cmd[1:])
    return subprocess.run(cmd, check=True, capture_output=capture, text=True,
                          cwd=ROOT)


def read_released():
    if not RELEASED_FILE.exists():
        return set()
    return {int(x) for x in RELEASED_FILE.read_text().split()}


def sync_files(released, prune):
    """Replace tracked files within the selected shared and released paths."""
    source = set(run("git", "ls-tree", "-r", "-z", "--name-only",
                     "dev-origin/dev", "--", "docs", capture=True).stdout.split("\0")) - {""}
    tracked = set(run("git", "ls-files", "-z", "--", "docs",
                      capture=True).stdout.split("\0")) - {""}

    def selected(path):
        # Never prune the generated contents page or any path outside docs/.
        if path == "docs/index.html" or not path.startswith("docs/"):
            return False
        if any(path == scope or path.startswith(scope + "/") for scope in SYNC_PATHS):
            return True
        m = re.match(r"docs/sessions/session-(\d{2})(?:/|[-.])", path)
        return bool(m and int(m.group(1)) in released)

    incoming = sorted(p for p in source if selected(p))
    for s in sorted(released):
        if not any(re.match(rf"docs/sessions/session-{s:02d}(?:/|[-.])", p)
                   for p in incoming):
            sys.exit(f"no session-{s:02d} content on dev-origin/dev")
    stale = sorted(p for p in tracked - source if selected(p))
    if stale and not prune:
        print("These files are on main but deleted on dev:")
        for path in stale:
            print(f"  {path}")
        sys.exit("rerun with --prune to remove them, or restore them on dev")
    # Remove first so file-to-directory and directory-to-file changes can sync.
    for path in stale:
        print(f"Removing deleted dev file: {path}")
        run("git", "rm", "--", path)
    if incoming:
        run("git", "checkout", "dev-origin/dev", "--", *incoming)


def gate_index(full_index: str, released: set) -> str:
    """De-link every syllabus entry whose session is not released, and drop
    the dev index's DEV-ONLY block (reference material outside the taught
    route) entirely."""
    full_index = re.sub(r"[ \t]*<!-- DEV-ONLY-START -->.*?<!-- DEV-ONLY-END -->"
                        r"[ \t]*\n?", "", full_index, flags=re.S)

    def session_of(href):
        m = re.search(r"sessions/session-(\d+)", href)
        return int(m.group(1)) if m else None

    def sub_li(m):
        href, text = m.group(1), m.group(2)
        s = session_of(href)
        if s is None or s in released:  # unnumbered pages (project launch) stay
            return m.group(0)
        text = re.sub(r'<span class="badge-built">.*?</span>', "", text,
                      flags=re.S).strip()
        return f'<li><span class="soon">{text}</span></li>'

    out = re.sub(r'<li><a href="(sessions/[^"]+)">(.*?)</a></li>',
                 sub_li, full_index, flags=re.S)

    def group_div(m):
        title = m.group(1)
        s = re.search(r"Session (\d+)", title)
        if s and int(s.group(1)) in released:
            return m.group(0)
        clean = re.sub(r'\s*<span class="badge-built">.*?</span>', "", title,
                       flags=re.S)
        return f'<div class="session-group">{clean}</div>'

    out = re.sub(r'<div class="session-group">(.*?)</div>', group_div, out,
                 flags=re.S)

    # the dev index's own status line and badges are dev-facing; drop them
    out = out.replace(
        '<p style="margin-top:12px;"><em>Built lessons are linked below; '
        "the rest are in preparation.</em></p>", "")
    out = re.sub(r'\s*<span class="badge-built">.*?</span>', "", out,
                 flags=re.S)

    # release note in the caveat banner: dev's own note wins; otherwise the
    # default, inserted once
    if '<span id="release-note">' not in out:
        out = out.replace('<div class="caveat-banner">\n            <p>',
                          '<div class="caveat-banner">\n            <p>'
                          + RELEASE_NOTE, 1)
    return out


def main():
    args = sys.argv[1:]
    prune = "--prune" in args
    args = [a for a in args if a != "--prune"]
    if not args:
        sys.exit(__doc__)

    branch = run("git", "rev-parse", "--abbrev-ref", "HEAD",
                 capture=True).stdout.strip()
    if branch != "main":
        sys.exit(f"on branch {branch!r}; releases run from main")
    dirty = run("git", "status", "--porcelain", "-z", "--untracked-files=all", capture=True).stdout
    entries = dirty.split("\0")
    if any(l.startswith("?? docs/") for l in entries):
        sys.exit("untracked files under docs/; move or review them before releasing")
    if any(l and not l.startswith("??") for l in entries):
        sys.exit("uncommitted changes on main; commit or stash first")

    init = args and args[0] == "init"
    if init:
        args = args[1:]
    new = [] if (args and args[0] == "sync") else [int(a) for a in args]

    released = (set() if init else read_released()) | set(new)
    if not released:
        sys.exit("no sessions to release")

    run("git", "fetch", "dev-origin", "dev")
    full_index = run("git", "show", "dev-origin/dev:docs/index.html",
                     capture=True).stdout

    sync_files(released, prune)

    # remove unreleased session files from the deployed tree
    for p in sorted((ROOT / "docs" / "sessions").glob("session-*")):
        m = re.match(r"session-(\d+)", p.name)
        if m and int(m.group(1)) not in released:
            run("git", "rm", "-r", "-q", "--ignore-unmatch",
                str(p.relative_to(ROOT)))

    (ROOT / "docs" / "index.html").write_text(gate_index(full_index, released),
                                              encoding="utf-8")
    RELEASED_FILE.write_text("\n".join(str(s) for s in sorted(released)) + "\n")

    run("python3", "add_page_nav.py")
    run("git", "add", "docs", "RELEASED-SESSIONS")
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
        print("Nothing to release: main already matches dev for these sessions.")
        return
    label = ("Gate site to" if init else
             "Release" if new else "Sync released sessions:")
    what = " ".join(str(s) for s in (sorted(released) if init else
                                     new if new else sorted(released)))
    run("git", "commit", "-m", f"{label} session(s) {what} [release.py]")
    print("Committed. Review the diff, then:")
    print("  git push origin main && git push dev-origin main")


if __name__ == "__main__":
    main()
