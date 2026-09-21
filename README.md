# antonio-skills

Plugin di Claude Code con le mie skill. Si invocano con il prefisso del plugin:

| Skill | Cosa fa |
| --- | --- |
| `/antonio-skills:monorepo-api-web-mobile-setup` | Imposta un monorepo API + web + mobile con il metodo di lavoro per agenti. |
| `/antonio-skills:monorepo-api-web-mobile-grill-iniziale` | Primo grill di dominio: `CONTEXT.md`, ADR, elenco di issue. |
| `/antonio-skills:controllo-issue` | Quali issue si possono implementare adesso, quali sono bloccate, e se il design chiede modifiche. |

## Installazione

```bash
claude plugin marketplace add ~/workspaces/antonio-skills
claude plugin install antonio-skills@antonio
```

Dopo una modifica alle skill: `claude plugin marketplace update antonio`, e aggiorna il plugin.
Quando il repo sarà su GitHub, `claude plugin marketplace add <owner>/antonio-skills` lo installa su qualunque macchina.
