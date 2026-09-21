# antoniovirgone-skills

Plugin di Claude Code con le mie skill. Si invocano con il prefisso del plugin:

| Skill | Cosa fa |
| --- | --- |
| `/antoniovirgone-skills:monorepo-api-web-mobile-setup` | Imposta un monorepo API + web + mobile con il metodo di lavoro per agenti. |
| `/antoniovirgone-skills:monorepo-api-web-mobile-grill-iniziale` | Primo grill di dominio: `CONTEXT.md`, ADR, elenco di issue. |
| `/antoniovirgone-skills:controllo-issue` | Quali issue si possono implementare adesso, quali sono bloccate, e se il design chiede modifiche. |

## Installazione

Da GitHub, su qualunque macchina:

```bash
claude plugin marketplace add AntonioVirgone/antoniovirgone-skills
claude plugin install antoniovirgone-skills@antoniovirgone
```

Per lavorare sulle skill, dal clone locale (le modifiche si vedono senza passare da GitHub):

```bash
claude plugin marketplace add ~/workspaces/antoniovirgone-skills
claude plugin install antoniovirgone-skills@antoniovirgone
```

Dopo una modifica alle skill alza `version` in `.claude-plugin/plugin.json`, poi `claude plugin marketplace update antoniovirgone` e `claude plugin update antoniovirgone-skills@antoniovirgone`: senza il cambio di versione resta installata quella vecchia.
