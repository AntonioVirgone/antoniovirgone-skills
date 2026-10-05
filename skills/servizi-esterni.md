# Regole comuni per i servizi esterni

Le seguono `deploy-online`, `firebase-progetto`, `app-di-test` e `app-in-locale`. Valgono per un monorepo impostato con `monorepo-api-web-mobile-setup`: API NestJS + Prisma, web Next.js, mobile Expo, tipi condivisi, Turborepo.

## Chi fa cosa

- **L'agente** fa quello che ha una CLI o un'API: `gh`, `vercel`, `firebase-tools`, `eas-cli`, `prisma`, `curl`, `xcrun`, `adb`. Le CLI che non sono installate si usano con `npx -y <pacchetto>@latest`, dalla cartella in cui leggono la configurazione (`eas` da quella dell'app mobile).
- **L'utente** fa i login, la creazione degli account, l'accettazione dei termini, i pagamenti e tutto quello che vive solo in una console web. Per questi passi l'agente scrive un **wizard** con la skill `wizard` di `mattpocock-skills`, in `scripts/configura-<area>.sh`, e l'utente lo lancia dal suo terminale. Un comando interattivo che chiede password o 2FA (`eas build` al primo giro su iOS, `eas credentials`, `firebase login`) va nel wizard, oppure l'utente lo lancia in chat col prefisso `!`.
- Quando una CLI dice che manca il login, l'agente si ferma, dice all'utente quale comando lanciare (`! npx -y firebase-tools@latest login`, `! vercel login`, `! npx -y eas-cli@latest login`) e riprende alla sua conferma.

Un wizard che esiste già nel repo si aggiorna, non si riscrive: i suoi stadi raccontano decisioni già prese.

## I valori

Prima di chiedere, l'agente ricava dal repo:

| Valore | Dove |
| --- | --- |
| `<progetto>` | lo scope dei pacchetti (`@<progetto>/api`), il nome delle cartelle in `apps/` |
| repo GitHub | `git remote -v` |
| bundle ID e pacchetto Android | `ios.bundleIdentifier` e `android.package` in `app.json` / `app.config.ts` |
| progetto EAS | `extra.eas.projectId` e `owner` in `app.json` |
| progetto Firebase | `FIREBASE_PROJECT_ID` nel `.env` dell'API |
| variabili attese | i `.env.example` delle tre app, `render.yaml`, `vercel.json`, `eas.json` |

Dove finiscono:

- i `.env` delle app (ignorati da git): valori per il locale. Un `.env` che manca parte dal suo `.env.example`;
- `~/.config/<progetto>/` (`chmod 600` sui file): chiavi e valori di produzione — `deploy.env`, il JSON dell'account di servizio, i `.p8`, `google-services.json`. Mai dentro il repo: un percorso che sta sotto la radice del repo si rifiuta;
- nei servizi (Render, Vercel, EAS): con le loro CLI quando ci sono, altrimenti nel wizard come valori da incollare.

Una chiave pubblica per natura (la `apiKey` di Firebase, le `NEXT_PUBLIC_…`, le `EXPO_PUBLIC_…`) si può mostrare in chat; un segreto no: lo legge e lo scrive il wizard con `ask_secret`, o l'agente lo passa da un file a una CLI senza stamparlo.

## Le scelte fisse

Database PostgreSQL su Supabase, API su Render (piano free, Francoforte), web su Vercel (Hobby), autenticazione con Firebase Auth, build e push con EAS, test su TestFlight e sul «Test interno» di Play. Un ID che non si cambia più (ID del progetto Firebase, bundle ID su Apple, nome del pacchetto su Play) l'utente lo conferma prima che l'agente lo crei.

## Ordine tra le skill

1. `firebase-progetto` — serve all'API (verifica dei token) e alle app (login).
2. `deploy-online` — database, API e web, che si passano indirizzi e origini.
3. `app-di-test` — le build per gli store, che hanno bisogno dell'indirizzo dell'API e di Firebase.

`app-in-locale` è indipendente: serve dal primo giorno.

## Chiusura di ogni skill

- I file del repo (configurazioni, wizard, `docs/deploy.md`) arrivano su un branch e in una PR, come un ticket: un servizio che legge la configurazione da `main` (il Blueprint di Render) aspetta il merge.
- Un resoconto in chat: cosa è fatto, cosa è stato saltato e perché, quale wizard lanciare e quando.
- Nella memoria del progetto: gli ID creati (progetto Firebase, progetto EAS, servizio Render, progetto Vercel), dove stanno le chiavi, e le trappole incontrate che il repo non dice.
