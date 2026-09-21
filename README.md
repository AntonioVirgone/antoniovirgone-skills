# antoniovirgone-skills

Plugin di Claude Code con le mie skill. Si invocano con il prefisso del plugin:

| Skill | Cosa fa |
| --- | --- |
| `/antoniovirgone-skills:monorepo-api-web-mobile-setup` | Imposta un monorepo API + web + mobile con il metodo di lavoro per agenti. |
| `/antoniovirgone-skills:monorepo-api-web-mobile-grill-iniziale` | Primo grill di dominio: `CONTEXT.md`, ADR, elenco di issue. |
| `/antoniovirgone-skills:controllo-issue` | Quali issue si possono implementare adesso, quali sono bloccate, e se il design chiede modifiche. |

## Installazione

```bash
claude plugin marketplace add ~/workspaces/antoniovirgone-skills
claude plugin install antoniovirgone-skills@antoniovirgone
```

Dopo una modifica alle skill alza `version` in `.claude-plugin/plugin.json`, poi `claude plugin marketplace update antoniovirgone` e `claude plugin update antoniovirgone-skills@antoniovirgone`: senza il cambio di versione resta installata quella vecchia.
Quando il repo sarà su GitHub, `claude plugin marketplace add <owner>/antoniovirgone-skills` lo installa su qualunque macchina.
