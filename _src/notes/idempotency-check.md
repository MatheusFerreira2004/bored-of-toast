# Idempotency check (PR #42)

On 2026-10-12 a commit that changed only this note triggered the Auto build. The run finished
successfully and created no "Regenerate site (auto build)" commit, i.e. re-running all
update_*.py scripts produced no changes to the site.

The same run's legacy "checks" workflow failed. Likely causes, fixed in the next commit:
- checks.py crashed on tomato-white-bean-stew.webp in the orphan-variant loop (the old glob
  'images/*-*w.webp' matched it and re.search(...).group(1) returned None);
- recipes/index.html was about 101 KB, over the 80 KB HTML budget (update_035 slims the cards).

This note lives in _src/, which the site comparison excludes, so it does not affect the site.
