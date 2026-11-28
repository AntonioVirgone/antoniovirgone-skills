# antoniovirgone-skills

Plugin di Claude Code con le mie skill. Si invocano con il prefisso del plugin:

| Skill | Cosa fa |
| --- | --- |
| `/antoniovirgone-skills:monorepo-api-web-mobile-setup` | Imposta un monorepo API + web + mobile con il metodo di lavoro per agenti. |
| `/antoniovirgone-skills:monorepo-api-web-mobile-grill-iniziale` | Primo grill di dominio: `CONTEXT.md`, ADR, elenco di issue. |
| `/antoniovirgone-skills:metodo-di-lavoro` | Il metodo comune a tutti i progetti: milestone, issue, etichette, grill, sessioni e worktree, commit, PR, Definition of Done, versioni e rilasci, con la parte Unity e i suoi script. |
| `/antoniovirgone-skills:nuova-issue` | Apre un'issue col formato del metodo: milestone, prefisso `M<n> ·`, etichette, corpo e blocchi. |
| `/antoniovirgone-skills:controllo-issue` | Quali issue si possono implementare adesso, quali sono bloccate (anche da una milestone che aspetta un'altra), e se il design chiede modifiche. |
| `/antoniovirgone-skills:chiusura-milestone` | Chiude una milestone col suo rilascio: versione, build, prova, caricamento, tag, devlog. |
| `/antoniovirgone-skills:pubblicazione-itch-io` | Pubblica su itch.io quando l'utente lo chiede: butler, prova dalla pagina, tag e release GitHub, devlog e descrizione da Claude in Chrome. |
| `/antoniovirgone-skills:firebase-progetto` | Il progetto Firebase: app, provider di accesso, Sign in with Apple, client OAuth, account di servizio. |
| `/antoniovirgone-skills:deploy-online` | Database su Supabase, API su Render, web app su Vercel, collegati tra loro. |
| `/antoniovirgone-skills:app-di-test` | EAS, push, TestFlight e test interno di Google Play. |
| `/antoniovirgone-skills:app-in-locale` | L'app su simulatore, emulatore o telefono collegato, con Metro e l'API locale. |
| `/antoniovirgone-skills:unity-setup-claude-blender` | Un progetto Unity collegato a Claude Code (Unity MCP) e a Blender (Blender MCP), con Git LFS e un CLAUDE.md con le regole per l'Editor. |

Ogni progetto segue [`metodo-di-lavoro`](skills/metodo-di-lavoro/SKILL.md) e nel suo `CLAUDE.md` e in `docs/agents/` tiene solo quello che è suo: repo, aree, ordine delle milestone, comandi del rilascio.

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
