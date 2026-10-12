# Idempotency and checks log (PR #42)

1. 2026-10-12, commit da8c863 (note only): Auto build finished with no regenerate commit, so
   re-running all update_*.py scripts changed nothing. The legacy "checks" workflow failed.
2. Commit fff690d: checks.py variant detection fixed (only -<number>w.webp counts as a variant);
   update_035 slims recipe cards. Auto build regenerated the site (f6467af).
   recipes/index.html went from about 101 KB to 78,484 bytes (76.6 KB, budget 80 KB).
3. This commit (note only) re-triggers both workflows on the regenerated site:
   expected result is no regenerate commit and a passing "checks" run.

This note lives in _src/, which the site comparison excludes, so it does not affect the site.
