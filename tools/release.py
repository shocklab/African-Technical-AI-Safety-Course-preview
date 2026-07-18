#!/usr/bin/env python3
"""Release revised weeks from the dev branch to the public site.

Workflow: Ben and Jonathan edit on the `dev` branch of the private repo
(dev-origin = African-Technical-AI-Safety-Course-dev). The public repo
(origin) serves GitHub Pages from `main`. This script pulls chosen
sessions' files from dev into main, so unreleased revisions stay private
until their week.

Usage, from the repo root with main checked out and clean:

    python3 tools/release.py 3 4      # release sessions 3 and 4

Steps it performs:
  1. git fetch dev-origin dev
  2. git checkout dev-origin/dev -- <that session's files>, plus
     docs/index.html and docs/assets (so titles/styles never desync)
  3. re-run add_page_nav.py (nav derives from index.html)
  4. commit
It does NOT push. Review the diff, then:
    git push origin main && git push dev-origin main
"""
import subprocess
import sys


def run(*cmd, capture=False):
    return subprocess.run(cmd, check=True, capture_output=capture, text=True)


def main():
    sessions = sys.argv[1:]
    if not sessions:
        sys.exit("give session numbers, e.g.: python3 tools/release.py 3 4")

    branch = run("git", "rev-parse", "--abbrev-ref", "HEAD", capture=True).stdout.strip()
    if branch != "main":
        sys.exit(f"on branch {branch!r}; releases run from main")
    dirty = run("git", "status", "--porcelain", capture=True).stdout.strip()
    if any(not l.startswith("??") for l in dirty.splitlines()):
        sys.exit("working tree has uncommitted changes; commit or stash first")

    run("git", "fetch", "dev-origin", "dev")
    tree = run("git", "ls-tree", "-r", "--name-only", "dev-origin/dev",
               "docs/sessions/", capture=True).stdout.split()

    paths = ["docs/index.html", "docs/assets"]
    for s in sessions:
        nn = f"{int(s):02d}"
        match = [p for p in tree if p.startswith(f"docs/sessions/session-{nn}")]
        if not match:
            sys.exit(f"no session-{nn} content on dev-origin/dev")
        paths += match

    run("git", "checkout", "dev-origin/dev", "--", *paths)
    run("python3", "add_page_nav.py")
    run("git", "add", "docs")
    run("git", "commit", "-m",
        f"Release session(s) {', '.join(sessions)} from dev")
    print("Committed. Review the diff, then:")
    print("  git push origin main && git push dev-origin main")


if __name__ == "__main__":
    main()
