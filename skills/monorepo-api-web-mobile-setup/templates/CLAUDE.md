## Agent skills

### Issue tracker

Issues live in GitHub Issues (`<owner>/<repo>`), via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Branching and PRs

One branch per ticket, never commit ticket work to `main`; at the end of the ticket push the branch and open a PR for the maintainer to review. See `docs/agents/branching.md`.

### Domain docs

Single-context — `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.

<!-- Solo con una wiki: togli il commento. Senza, cancella anche questo blocco.
### Wiki

Accanto al repo può esserci [<wiki>](https://github.com/<owner>/<wiki>), la wiki sui progetti precedenti mantenuta da un agente. Se c'è, usala come mappa per la storia di una decisione e per il confronto con i progetti precedenti, partendo da `wiki/index.md`, poi verifica nelle fonti; se non c'è, vai avanti senza. Non si modifica da qui. Vedi `docs/agents/wiki.md`.
-->
