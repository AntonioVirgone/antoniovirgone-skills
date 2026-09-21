## Agent skills

### Issue tracker

Issues live in GitHub Issues (`<owner>/<repo>`), via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Branching and PRs

One branch per ticket, never commit ticket work to `main`; at the end of the ticket push the branch and open a PR for the maintainer to review. See `docs/agents/branching.md`.

### Domain docs

Single-context — `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
