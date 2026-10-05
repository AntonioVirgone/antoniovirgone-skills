---
name: deploy-online
description: Mette online database, API e web app di un monorepo API + web + mobile — PostgreSQL su Supabase, API NestJS su Render, web Next.js su Vercel — con le configurazioni nel repo, le migrazioni, le variabili e un wizard per i passi da console.
disable-model-invocation: true
---

# Deploy online: Supabase, Render, Vercel

Porta online i tre pezzi lato server e li collega: la stringa del database va a Render, l'indirizzo dell'API va a Vercel (e alle build dell'app), l'indirizzo della web app torna a Render come origine ammessa e a Firebase come dominio autorizzato.

Prima di cominciare leggi [le regole comuni](../servizi-esterni.md): chi fa cosa, dove stanno i valori, come si chiude.

Richiesta dell'utente: $ARGUMENTS

## Passi

### 1. Stato di partenza

Leggi dal repo i valori della tabella delle regole comuni, più:

- lo script di migrazione dell'API (`db:deploy` o simile, che lancia `prisma migrate deploy`) e il percorso dell'endpoint di salute;
- se ci sono già `render.yaml`, `apps/<progetto>-web/vercel.json`, `.npmrc` con `include=dev`, `docs/deploy.md`, un `scripts/configura-deploy.sh`, `~/.config/<progetto>/deploy.env`;
- uno script che crea il primo amministratore (per esempio `operator:add`), se l'app ne ha uno;
- `vercel whoami` e `gh auth status`.

Poi presenta in un messaggio la tabella dei valori che useresti e chiedi solo quello che manca. Le domande tipiche:

- **database**: un progetto Supabase nuovo, oppure un database a sé (`create database <progetto>`) su un progetto esistente, per non pagarne un secondo;
- variabili d'ambiente dell'API con un valore fisso in produzione (limiti, flag) che il `.env.example` non dice.

Fatto quando: l'utente ha confermato la tabella.

### 2. File nel repo

Su un branch, scrivi o aggiorna:

- `render.yaml` da [templates/render.yaml](templates/render.yaml): sostituisci i segnaposto, aggiungi le variabili d'ambiente dell'API con un commento che dice perché hanno quel valore, e marca `sync: false` i segreti;
- `apps/<progetto>-web/vercel.json` da [templates/vercel.json](templates/vercel.json);
- `.npmrc` alla radice con `include=dev`, se manca;
- `docs/deploy.md`: una tabella pezzo → dove → file, poi una sezione per pezzo con le scelte non ovvie (le trovi nei commenti dei template e in [Trappole](#trappole)) e cosa comporta il piano gratuito;
- il wizard `scripts/configura-deploy.sh` con la skill `wizard`, con gli stadi del passo 3 che toccano all'utente. Valori in `~/.config/<progetto>/deploy.env`.

Verifica in locale quello che si può: `npm ci --include=dev --workspace=@<progetto>/api --include-workspace-root` e il `buildCommand` di Render in un worktree pulito; `npx turbo run build --filter=@<progetto>/web`; `bash -n` sul wizard.

Apri la PR e fermati: Render legge il Blueprint da `main`. Riprendi quando l'utente dice che è mergiata.

Fatto quando: la PR è mergiata e `render.yaml` è su `main`.

### 3. Il giro sui servizi

L'utente lancia il wizard; tu fai, tra uno stadio e l'altro, le parti con la CLI. L'ordine:

1. **Supabase** (utente): progetto o `create database`, poi la stringa del **Session pooler**. Tu controlli la forma — host `*.pooler.supabase.com`, porta `5432`, nome del database giusto in fondo — e, con conferma, lanci la migrazione contro di essa (`DATABASE_URL=… npm run db:deploy -w @<progetto>/api`) e lo script del primo amministratore, se c'è.
2. **Render** (utente): New Blueprint Instance sul repo, `DATABASE_URL` dal passo prima, `CORS_ORIGINS` vuoto per ora. Tu aspetti l'endpoint di salute con `curl --max-time 90` ripetuto: il primo deploy dura minuti.
3. **Vercel**: l'utente importa il repo dalla dashboard con Root Directory `apps/<progetto>-web` (così Vercel collega Git e fa i deploy a ogni push). Poi tu, dalla cartella della web app, `vercel link --yes --project <nome>` e una `vercel env add <NOME> production` per variabile del suo `.env.example` (il valore da `printf '%s' … |`, senza a capo), con l'URL dell'API di Render; infine `vercel redeploy` dell'ultimo deploy di produzione, perché le variabili valgono dal deploy successivo. Senza login a Vercel, le variabili le incolla l'utente nel wizard prima del primo deploy.
4. **Collegamenti**: `CORS_ORIGINS` su Render con l'URL di Vercel senza `/` finale, poi «Save, rebuild and deploy» (utente, o tu con l'API di Render se c'è `RENDER_API_KEY`); il dominio di Vercel tra gli **Authorized domains** di Firebase Authentication (utente).

Fatto quando: l'endpoint di salute risponde, la web app si apre, e l'utente entra con il suo account e vede dati che arrivano dall'API.

### 4. Chiusura

Segui la chiusura delle regole comuni. Nel resoconto: gli indirizzi di API e web app, dove stanno i valori, e che il passo successivo per le build dell'app è `/antoniovirgone-skills:app-di-test`, che usa l'indirizzo dell'API.

Fatto quando: l'utente ha il resoconto e la memoria ha gli ID dei servizi.

## Trappole

- **Stringa di Supabase**: la «Direct connection» è solo IPv6 e Render non la raggiunge; con il «Transaction pooler» (porta 6543) `prisma migrate deploy` non va. Il Session pooler (5432) serve sia all'API sia alle migrazioni. Con un database a sé su un progetto esistente, in fondo alla stringa `/<progetto>` al posto di `/postgres`: una stringa che finisce ancora con `/postgres` userebbe il database dell'altro progetto, e il wizard la rifiuta.
- **Render free**: niente pre-deploy command (le migrazioni stanno nello `startCommand`); il servizio si addormenta dopo 15 minuti senza richieste e la prima richiesta dopo aspetta circa un minuto; mentre dorme non girano i job pianificati, che ripartono al risveglio.
- **Build su Render**: con `NODE_ENV=production` npm salta le devDependencies, dove stanno `nest`, `typescript`, `turbo` e `prisma`: da qui `--include=dev` nel `buildCommand` e `include=dev` in `.npmrc`. Installare tutti i workspace (Expo, Next.js) sfora i limiti del piano: si installa solo quello dell'API.
- **Vercel in un monorepo**: `vercel.json` sta nella cartella della web app e risale alla radice per installare e compilare con Turborepo, che costruisce prima i pacchetti condivisi; `turbo-ignore` salta i deploy che non toccano la web app né i suoi pacchetti.
- **Login sulla web app**: senza il dominio di Vercel tra gli Authorized domains di Firebase il login fallisce con un errore di dominio, e sembra un problema di CORS.
