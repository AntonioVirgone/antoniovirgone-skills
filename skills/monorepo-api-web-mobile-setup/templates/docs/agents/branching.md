# Branching and pull requests

Ticket work never lands on `main` directly.

## Rules

- **One branch per ticket**, created from an up-to-date `main`, named `<type>/<issue-number>-<slug>` — e.g. `feat/4-emissione-invito`, `fix/12-timeout-sessione`. Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`.
- All commits for that ticket go on that branch, and only that branch.
- **At the end of the ticket**: push the branch and open a PR with `gh pr create`, referencing the issue (`Closes #<n>`).
- The maintainer reviews and merges. Agents never merge a PR and never push to `main`.
- If ticket work has already been committed to local `main` by mistake, move it before pushing: create the branch at the current commit, then `git reset --hard origin/main`.
- A ticket that depends on an unmerged branch is stacked on it: branch from it, and open the PR against it as base.

## PR body

- What changed and why, framed against the ticket's acceptance criteria.
- Any decision taken that the ticket did not specify, and any known gap deliberately left open.
- How it was verified — which suites were run, against what.
