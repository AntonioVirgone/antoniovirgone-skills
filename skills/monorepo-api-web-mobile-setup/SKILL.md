---
name: monorepo-api-web-mobile-setup
description: Imposta un repo nuovo come monorepo API + web + mobile (NestJS/Prisma, Next.js, Expo, tipi condivisi, Turborepo) con un metodo di lavoro per agenti — ticket su GitHub, un branch e una PR per ticket, glossario e ADR, subagenti per app.
disable-model-invocation: true
---

# Setup di un monorepo API + web + mobile

Imposta il repository corrente perché gli agenti ci lavorino con un metodo preciso:

- ogni lavoro parte da un'**issue** GitHub con criteri di accettazione;
- **un branch e una PR per ticket**: la PR la rivede e la mergia una persona;
- il vocabolario di dominio vive in `CONTEXT.md`, le decisioni in ADR numerati in `docs/adr/`;
- un **subagente per app**, che conosce il suo stack e le regole condivise.

Questa skill scrive le istruzioni, le convenzioni e i subagenti; il codice delle app e il dominio arrivano dopo. Il passo successivo, a PR mergiata, è `/antoniovirgone-skills:monorepo-api-web-mobile-grill-iniziale`.

Richiesta dell'utente: $ARGUMENTS

I file da copiare stanno in `templates/`, accanto a questo file.

## Passi

### 1. Prerequisiti

Verifica, e riporta all'utente l'esito di ciascuno:

- `gh auth status` riesce;
- `git remote -v` punta a un repo GitHub (da lì ricavi `<owner>/<repo>`);
- tra le skill disponibili ci sono `grilling` e `domain-modeling` del plugin `mattpocock-skills` (il grill iniziale e le skill di triage le usano).

Se ne manca uno, fermati: di' all'utente cosa manca e come si installa (per il plugin: `/plugin install mattpocock-skills@claude-plugins-official`), e riprendi quando ti conferma. Installare è una sua scelta.

Fatto quando: i tre controlli sono verdi.

### 2. Raccogli le scelte, in una volta sola

Leggi il repo (README, `package.json`, cartelle presenti, eventuale `docs/`) e la richiesta dell'utente. Poi presenta **in un unico messaggio** la tabella delle scelte con il valore che useresti, marcando quali vengono dai default (sezione [Default](#default)) e quali dal repo o dall'utente:

- nome del progetto e prefisso delle app (`<progetto>`);
- descrizione in due righe: cosa fa, chi lo usa;
- app e percorsi (default: `apps/<progetto>-api`, `apps/<progetto>-web`, `apps/<progetto>-mobile`, `packages/shared-types` come `@<progetto>/types`). Se la web app è pensata per un ruolo preciso, proponi di chiamarla col nome del ruolo;
- stack;
- cartelle con specifiche di progetti precedenti, se ce ne sono;
- lingue (chat, prosa, identificatori, commit);
- se creare le label su GitHub.

Chiedi solo quello che non hai ricavato, e aspetta la conferma.

Fatto quando: l'utente ha confermato ogni riga della tabella.

### 3. File di istruzioni

Copia da `templates/`, sostituendo `<owner>/<repo>`:

- `templates/CLAUDE.md` → `CLAUDE.md` alla radice (se esiste già, aggiungi la sezione in fondo);
- `templates/docs/agents/*.md` → `docs/agents/`.

Il template di `CLAUDE.md` dichiara un solo contesto di dominio: è la scelta giusta anche con tre app, perché il contesto riguarda il dominio, non le app. Proponi la variante multi-contesto (`CONTEXT-MAP.md`) solo se nel materiale vedi la stessa parola usata con significati diversi in parti diverse del sistema.

`CONTEXT.md` e `docs/adr/` restano da creare: nascono nel grill iniziale.

Se ci sono specifiche di progetti precedenti, aggiungi in cima al README di ciascuna cartella una nota: sono un riferimento storico, e dove divergono da `CONTEXT.md` o da un ADR prevalgono questi ultimi.

Fatto quando: `CLAUDE.md` e i quattro file di `docs/agents/` sono scritti e contengono il repo giusto.

### 4. Subagenti

Per ogni app, una bozza di `.claude/agents/<progetto>-<app>.md` dal template `templates/subagent.md`. La cartella dell'app può essere ancora vuota: bastano percorso e stack. La `description` è quello che l'agente principale legge per decidere a chi delegare: nomina in concreto cosa contiene l'app.

Aggiungi queste regole, adattate:

- **agente API**: possiede anche `packages/shared-types`. Ogni DTO o forma di risposta usata dai client sta lì, una volta sola. Una modifica ai tipi condivisi adatta nello stesso ticket anche web e mobile, e si verifica col typecheck di tutto il monorepo: è ciò che tiene in piedi la build dei frontend;
- **agenti web e mobile**: usano i tipi di `@<progetto>/types` così come sono. Quando serve un tipo nuovo o diverso, si fermano e lo segnalano all'agente principale come modifica lato API: un subagente non può delegare a un altro subagente, quindi la decisione torna a chi coordina;
- **logica condivisa**: se due app implementano le stesse regole (per esempio un engine di gioco e il suo validatore), in entrambi gli agenti scrivi che quelle regole vivono in un posto solo e che, finché un ADR non dice dove, ogni duplicazione va segnalata.

Nei file, la prima riga è `---` e il frontmatter è YAML puro.

Mostra tutte le bozze all'utente e aspetta il suo ok prima di scriverle.

Fatto quando: l'utente ha approvato le bozze e i file sono scritti.

### 5. Scaffolding minimo della radice

Se il repo non ha ancora un `package.json` di radice, crealo per lo stack scelto: workspaces `apps/*` e `packages/*`, `turbo` tra le devDependencies, `packageManager` fissato alla versione di `npm --version`. Con lo stack di default aggiungi anche `.npmrc` con `include=dev` e un commento che dice perché: i build server che installano solo le dipendenze di produzione (Render lo fa) non trovano `turbo`, `typescript` e `@nestjs/cli`, e la build si ferma.

Le app vere e proprie si creano con i loro ticket.

Fatto quando: la radice ha `package.json` (e `.npmrc`, con lo stack di default), oppure li aveva già.

### 6. Label

Se l'utente ha detto sì al passo 2, crea con `gh label create` le label di `templates/docs/agents/triage-labels.md` che mancano (`gh label list` per vederle). `wontfix` GitHub la crea già in ogni repo nuovo: resta com'è.

Fatto quando: `gh label list` mostra tutte e cinque le label.

### 7. Memoria

Salva nella memoria di questo progetto le [abitudini](#abitudini-da-salvare-in-memoria), una per file, ognuna con **Why:** e **How to apply:**, più le preferenze di lingua confermate al passo 2.

Fatto quando: ogni abitudine ha il suo file e la sua riga nell'indice della memoria.

### 8. Verifica e PR

- Ogni percorso citato nei file scritti (specifiche, cartelle, file) esiste. Se un rimando punta a qualcosa che non c'è, toglilo.
- Branch `chore/setup-agenti`, un commit `chore: imposta CLAUDE.md, docs/agents e le convenzioni di lavoro`, push, `gh pr create` verso `main`.
- La PR resta aperta: la mergia l'utente.

Chiudi con il link alla PR e ricorda il passo successivo: `/antoniovirgone-skills:monorepo-api-web-mobile-grill-iniziale`, in una sessione nuova dopo il merge.

Fatto quando: la PR esiste e l'utente ha il link.

## Default

Valgono salvo diversa indicazione dell'utente al passo 2.

**Stack**

- monorepo **npm workspaces + Turborepo**. npm e non pnpm: con pnpm il bundler di Expo (Metro) a volte non trova i pacchetti, e il rimedio (`node-linker=hoisted`) toglie gran parte del vantaggio;
- API: NestJS + Prisma su PostgreSQL, TypeScript;
- web: Next.js 16 (App Router), React 19, Tailwind v4, TypeScript;
- mobile: Expo (React Native), TypeScript;
- tipi condivisi: `packages/shared-types`, pubblicato nel workspace come `@<progetto>/types`.

**Lingue**

- chat con l'utente in italiano;
- identificatori di codice in inglese; commenti, messaggi d'errore, documentazione, commit e PR in italiano; i test possono usare l'italiano anche negli identificatori.

**Commit e PR**

- conventional commits, descrizione nella lingua della prosa e numero dell'issue in fondo: `feat(mobile): la mappa mostra i livelli sbloccati (#12)`. Lo scope è l'app toccata. Un ADR va in un commit `docs:` a sé;
- nel corpo della PR la parola chiave di chiusura è in inglese, `Closes #N`: GitHub riconosce solo quella, e una traduzione lascia l'issue aperta;
- le correzioni dopo la revisione arrivano come commit nuovi sullo stesso branch (`fix(<scope>): la revisione di #N — …`), così la cronologia della revisione resta leggibile.

## Abitudini da salvare in memoria

- Prima di implementare un ticket, confrontare i criteri di accettazione con il codice reale: se un criterio presuppone qualcosa che non esiste o contraddice una decisione già mergiata, chiedere, oppure tenere la scelta già in produzione e dichiararlo nella PR.
- Prima di cominciare un ticket, verificare su `main` che quello che descrive ci sia davvero; se dipende da un branch non mergiato, partire da quel branch e aprire la PR verso di esso.
- Prima di aggiungere commit a un branch, controllare che la sua PR sia ancora aperta.
- Un ADR che descrive male una decisione ancora valida si corregge nella stessa PR; se la decisione cambia, si chiede all'utente.
- Un worktree nuovo si prepara prima dei test: `npm install` in radice e `npx prisma generate` nell'API. Senza, i test falliscono con errori di moduli mancanti che sembrano colpa del proprio lavoro.
- Formatter e linter si lanciano sui file del ticket.
- Una PR di API che cambia i tipi condivisi adatta anche web e mobile nella stessa PR.
