# antoniovirgone-skills

Plugin di Claude Code con le mie skill. Si invocano con il prefisso del plugin:

| Skill | Cosa fa |
| --- | --- |
| `/antoniovirgone-skills:monorepo-api-web-mobile-setup` | Imposta un monorepo API + web + mobile con il metodo di lavoro per agenti. |
| `/antoniovirgone-skills:monorepo-api-web-mobile-grill-iniziale` | Primo grill di dominio: `CONTEXT.md`, ADR, elenco di issue. |
| `/antoniovirgone-skills:controllo-issue` | Quali issue si possono implementare adesso, quali sono bloccate, e se il design chiede modifiche. |
| `/antoniovirgone-skills:firebase-progetto` | Il progetto Firebase: app, provider di accesso, Sign in with Apple, client OAuth, account di servizio. |
| `/antoniovirgone-skills:deploy-online` | Database su Supabase, API su Render, web app su Vercel, collegati tra loro. |
| `/antoniovirgone-skills:app-di-test` | EAS, push, TestFlight e test interno di Google Play. |
| `/antoniovirgone-skills:app-in-locale` | L'app su simulatore, emulatore o telefono collegato, con Metro e l'API locale. |

Le quattro skill sui servizi esterni seguono le regole comuni di [`skills/servizi-esterni.md`](skills/servizi-esterni.md): l'agente usa le CLI dove ci sono, e per i passi da console (login, termini, chiavi da scaricare) scrive un wizard che lanci tu. L'ordine è `firebase-progetto`, `deploy-online`, `app-di-test`; `app-in-locale` serve da subito.

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

## Licenza

MIT — vedi [LICENSE](LICENSE).
