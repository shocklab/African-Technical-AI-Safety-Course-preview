# Probes for the Session 7.6 lab rewrite

Throwaway scripts, kept because their *results* cost real CPU time to re-derive and they
decide the shape of the lab. Run any of them with `python3 -u probeN.py`.

| script | question it answers |
|---|---|
| `probe1.py` | can (A)/(B) log-probs be read cleanly at 0.5B? |
| `probe2.py` | position bias and principle sensitivity, two model sizes |
| `probe3.py` | does critique-and-revise work with the *instruct* model? |
| `probe4.py` | does it work with base-as-generator, instruct-as-critic? |
| `probe5.py` | the same two questions at 1.5B (never completed: download stalled) |

Results are recorded in `SESSION-07-HANDOFF-2026-08-26.md` at the repo root. Read that
before re-running anything.
