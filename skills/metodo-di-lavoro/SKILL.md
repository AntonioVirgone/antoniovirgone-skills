---
name: metodo-di-lavoro
description: Il metodo di lavoro comune a tutti i progetti di Antonio — milestone, issue, etichette, grill, sessioni e worktree, branch, commit, PR, Definition of Done, versioni e rilasci — con una parte in più per i progetti Unity. Usala prima di aprire o lavorare un'issue, fare un commit o una PR, chiudere una milestone, e quando un progetto nuovo o vecchio va portato su questo metodo, anche se l'utente dice solo «organizziamo il progetto come gli altri».
---

# Metodo di lavoro

Vale per ogni progetto. Il progetto aggiunge solo quello che è suo, in `docs/agents/` e nel suo `CLAUDE.md`: il repo GitHub, le aree, l'ordine delle milestone, i comandi del rilascio. Se il progetto dice una cosa diversa da qui, vale il progetto.

I progetti Unity seguono anche [UNITY.md](UNITY.md). Per portare un progetto su questo metodo segui [Applicare il metodo](#applicare-il-metodo-a-un-progetto).

Richiesta dell'utente: $ARGUMENTS

## Lingua

Issue, PR, commit, documentazione e commenti nel codice in **italiano**. Identificatori del codice (tipi, metodi, variabili, nomi di file del codice) in inglese.

## I documenti del progetto

- **`CONTEXT.md`** alla radice: il glossario del dominio, un termine per voce, con il significato che ha *in questo progetto*. È il file che leggono le skill `domain-modeling` e `grilling`. Un termine nuovo nato in un grill ci entra subito.
- **`docs/GDD.md`** nei giochi (o il documento di design del prodotto): le decisioni vive, quello che il prodotto *è* oggi. Ogni grill che decide qualcosa lo aggiorna. Le alternative scartate non stanno qui: stanno negli ADR.
- **`docs/adr/NNNN-<titolo>.md`**: una decisione difficile da cambiare dopo (stack, architettura, formato dei dati, modello commerciale), con contesto, decisione, alternative e conseguenze. Numeri a 4 cifre, mai riusati; un ADR superato resta, con una riga in cima che dice chi lo supera.
- **`docs/agents/`**: le convenzioni del progetto per gli agenti, dai template in [templates/docs/agents/](templates/docs/agents/):
  - `triage-labels.md`: il repo GitHub e le etichette, con le aree del progetto;
  - `milestone.md`: l'ordine delle milestone, le dipendenze, i percorsi paralleli e i rilasci;
  - `rilasci.md`, quando il progetto rilascia: i comandi di build, prova e caricamento.

Niente piano separato per milestone: il grill di una milestone produce le sue issue, e l'ordine sta nelle loro sezioni `## Bloccata da` e `## Ordine consigliato`.

## Milestone

- Nome `M<n> <nome>` (`M3 Combattimento`). Il numero identifica, non ordina: l'ordine lo dice `docs/agents/milestone.md`.
- Ogni milestone è un **incremento che si prova**: alla sua chiusura qualcosa in più funziona davvero, non un mucchio di pezzi che serviranno dopo.
- Tutte le milestone del progetto si aprono subito su GitHub, con una descrizione di una o due frasi. Le issue invece si scrivono in dettaglio solo fino alla prima versione completa del prodotto; le milestone dopo restano con la sola descrizione finché non tocca a loro.
- **Dipendenza**: una milestone ne aspetta un'altra solo se le serve qualcosa che arriva da lì. **Percorso parallelo**: una milestone che non aspetta e non blocca nessuna.
- Ogni progetto ha una milestone perpetua di **ritocchi** (bug e piccoli difetti che non appartengono a nessun'altra), che non si chiude mai.
- Niente board di GitHub Projects: bastano milestone, etichette e i blocchi nelle issue.

## Issue

Ogni lavoro parte da un'issue, anche di design, documentazione o grafica. Si aprono con la skill `nuova-issue` di questo plugin, e la skill `controllo-issue` dice quali si possono lavorare adesso.

- **Titolo** `M<n> · <titolo>`, con lo stesso numero della milestone GitHub assegnata. Nessuna issue senza milestone: se nessuna va bene, si chiede all'utente. Se l'issue cambia milestone, cambia anche il prefisso.
- **Corpo**, senza template in `.github/`:
  - `## Obiettivo`: una o due frasi su cosa cambia per chi usa il prodotto o per chi ci lavora;
  - `## Cosa` (o `## Cosa c'è già` e `## Cosa fare`): i pezzi del lavoro, coi nomi dei tipi e dei file;
  - `## Fatto quando`: criteri controllabili, ognuno con la sua verifica (test, cattura, prova nel browser); se serve un giudizio dell'utente, lo dice;
  - `## Bloccata da` con `- #N — <motivo>` per i blocchi duri, oppure `## Ordine consigliato` con `Meglio dopo #N: <motivo>`;
  - in fondo la riga `Riferimenti:` con ADR, sezioni del GDD e file da cui parte.
- **Etichette**: una di triage, almeno una d'area, una di tipo.

| Triage | Significato |
| --- | --- |
| `needs-triage` | Da valutare: scelta aperta o perimetro da fissare |
| `needs-info` | In attesa di informazioni da chi l'ha aperta |
| `ready-for-agent` | Specificata del tutto: un agente ci lavora da solo |
| `ready-for-human` | Serve una persona: un account, un giudizio, una misura che l'agente non può fare |
| `wontfix` | Non verrà fatta |

Tipi: `enhancement` (lavoro nuovo), `bug` (difetto), `documentation` (decisioni, regole, documenti). Le aree sono del progetto e stanno in `docs/agents/triage-labels.md`.

Un disegno che l'agente fa da solo resta `ready-for-agent`, con l'approvazione dell'utente fra i criteri di «Fatto quando».

## Dal piano alle issue

Un'idea nuova o una milestone che tocca passa da un **grill** (skill `grilling`): domande a round, ognuna con la raccomandazione, finché non resta niente di deciso in silenzio. Il grill produce decisioni (nel GDD, in `CONTEXT.md`, negli ADR) e issue, **non codice**. Si scrive solo dopo che l'utente conferma l'intesa.

## Sessioni, branch e PR

- **Una sessione per issue**, nel suo worktree (`.claude/worktrees/<nome>`), su un branch `claude/<slug>` da `origin/main` aggiornato.
- Il codice arriva su `main` solo con una PR che chiude l'issue (`Closes #N`). Più issue nella stessa PR solo se sono piccole e della stessa milestone.
- Il **merge lo fa sempre l'utente**, con un merge commit. Il branch si cancella al merge, e il worktree subito dopo.
- Le correzioni dopo una revisione sono **commit nuovi** sullo stesso branch: niente `--amend` né force push su una PR aperta.
- **Sessioni in cloud** (`CLAUDE_CODE_REMOTE=true`): non hanno gli strumenti locali del progetto (Editor, MCP, file LFS). Lì si fa solo quello che non è sviluppo: grill, analisi, issue, revisione, documentazione. Davanti a una richiesta di implementazione ci si ferma prima di toccare file e si avverte che serve una sessione sul Mac.

## Commit

Una frase in italiano che dice cosa cambia, col numero dell'issue in fondo:

```
Minimappa con la nebbia di guerra (#14)
```

Niente conventional commits (`feat:`, `fix(scope):`), neanche nei monorepo. Un corpo, se serve, spiega il perché, non il come.

## Definition of Done

Un'issue è fatta quando:

1. ogni criterio di «Fatto quando» è soddisfatto e verificato come dice il criterio;
2. il progetto compila senza errori e i test passano (quelli nuovi compresi: la logica nuova ha i suoi test);
3. se la modifica si vede, la PR ha le catture (screenshot o GIF) che la mostrano;
4. `CLAUDE.md`, `CONTEXT.md`, il GDD o `docs/agents/` sono aggiornati se il lavoro ha cambiato quello che dicono.

La PR dice cosa è stato verificato e come, e cosa no.

## Versioni e rilasci

- Versioni `0.MINOR.PATCH` finché l'utente non decide la 1.0.0. Il progetto può fissare una numerazione sua per i primi rilasci (per esempio rilasci privati `0.0.x` prima della prima demo pubblica): la scrive in `docs/agents/milestone.md`.
- Una milestone che rilascia fa salire la MINOR e azzera la PATCH; un rilascio di sole correzioni fa salire la PATCH. Le milestone senza rilascio escono col rilascio successivo.
- Una milestone che rilascia ha un'issue `M<n> · Rilascio <versione>`, bloccata da tutte le altre issue della milestone: è l'ultima a chiudersi. Un problema trovato provando la build del rilascio diventa un'issue della stessa milestone e blocca il rilascio.
- Il rilascio si fa con la skill `chiusura-milestone`: commit «Versione X.Y.Z (M<n>)», build da `main` aggiornato, prova senza errori, caricamento (con l'ok dell'utente), tag `vX.Y.Z` sul commit della versione, chiusura della milestone e aggiornamento di `docs/agents/milestone.md`.

## Applicare il metodo a un progetto

1. **Etichette** su GitHub: triage e tipi come sopra, più le aree del progetto. Le etichette di default che non servono (`duplicate`, `good first issue`, `help wanted`, `invalid`, `question`) si tolgono solo con l'ok dell'utente.

   ```bash
   gh label create needs-triage --color fbca04 --description "Da valutare: scelta aperta o perimetro da fissare" --force
   gh label create needs-info --color d876e3 --description "In attesa di informazioni" --force
   gh label create ready-for-agent --color 0e8a16 --description "Specificata del tutto: un agente ci lavora da solo" --force
   gh label create ready-for-human --color 1d76db --description "Serve una persona" --force
   gh label create wontfix --color ffffff --description "Non verrà fatta" --force
   gh label create enhancement --color a2eeef --description "Lavoro nuovo" --force
   gh label create bug --color d73a4a --description "Un difetto" --force
   gh label create documentation --color 0075ca --description "Decisioni, regole e documenti" --force
   gh label create <area> --color c5def5 --description "<dove si svolge il lavoro>" --force
   ```

2. **`docs/agents/`** dai template, con repo, aree e tabella delle milestone del progetto.
3. **Milestone** su GitHub, tutte, con la descrizione: `gh api repos/<owner>/<repo>/milestones -f title="M<n> <nome>" -f description="<descrizione>"`.
4. Nel **`CLAUDE.md`** una sezione breve:

   ```markdown
   ## Metodo di lavoro
   Segui la skill `antoniovirgone-skills:metodo-di-lavoro` (e la sua parte Unity): milestone, issue, branch, commit, PR, Definition of Done e rilasci. Qui e in `docs/agents/` solo quello che è di questo progetto: etichette e aree in `docs/agents/triage-labels.md`, ordine delle milestone e rilasci in `docs/agents/milestone.md`. Le issue si aprono con la skill `antoniovirgone-skills:nuova-issue`.
   ```

5. Per un progetto Unity, i passi di [UNITY.md](UNITY.md#applicare-la-parte-unity).
6. Skill del progetto che rifanno quelle di qui (`<progetto>-nuova-issue`, `<progetto>-chiusura-milestone`) si tolgono, portando in `docs/agents/` quello che avevano di specifico.

Fatto quando: le etichette e le milestone sono su GitHub, `docs/agents/` e il rimando nel `CLAUDE.md` sono nella PR del progetto.
