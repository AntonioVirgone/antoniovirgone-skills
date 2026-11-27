---
name: nuova-issue
description: Apre un'issue su GitHub col formato del metodo di lavoro — milestone, prefisso `M<n> ·`, etichette di triage, area e tipo, corpo con Obiettivo, Cosa, Fatto quando e blocchi. Usala per ogni issue nuova di qualunque progetto, anche di design, documentazione o grafica, per un problema trovato provando una build, e quando un grill o un piano approvato va diviso in issue.
---

# Aprire un'issue

Il formato è quello della skill `metodo-di-lavoro` («Issue»). Il repo, le aree e l'ordine delle milestone li dice il progetto in `docs/agents/triage-labels.md` e `docs/agents/milestone.md`: leggili prima.

Richiesta dell'utente: $ARGUMENTS

## 1. Milestone

Leggi le milestone aperte con la loro descrizione:

```bash
gh api 'repos/<owner>/<repo>/milestones?state=open&per_page=100' --jq '.[] | "\(.title): \(.description)"'
```

Scegli quella a cui appartiene il lavoro: la descrizione dice cosa ci sta dentro, `docs/agents/milestone.md` l'ordine. Un problema trovato provando la build di un rilascio va nella milestone che si sta chiudendo e blocca la sua issue `M<n> · Rilascio <versione>`. Un bug o un ritocco che non appartiene a nessuna va nella milestone dei ritocchi.

Se nessuna milestone aperta va bene, chiedi all'utente prima di aprire l'issue: un'issue senza milestone non si apre.

Fatto quando: hai la milestone, col motivo in una riga.

## 2. Etichette

Una di triage (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`), tutte quelle d'area che il lavoro tocca (da `docs/agents/triage-labels.md`) e una di tipo (`enhancement`, `bug`, `documentation`).

## 3. Corpo

In italiano, coi termini di `CONTEXT.md`, sul modello delle issue già aperte del repo:

- `## Obiettivo`: una o due frasi su cosa cambia per chi usa il prodotto o per chi ci lavora;
- `## Cosa` (o `## Cosa c'è già` e `## Cosa fare`): i pezzi del lavoro, coi nomi dei tipi e dei file;
- `## Fatto quando`: criteri controllabili, ognuno con la sua verifica (test, cattura, prova nel browser); se serve un giudizio dell'utente, dillo;
- `## Bloccata da` (`- #N — <motivo>`, solo blocchi duri) o `## Ordine consigliato` (`Meglio dopo #N: <motivo>`), se dipende da altre issue;
- in fondo la riga `Riferimenti:` con ADR, sezioni del GDD e file da cui parte.

Fatto quando: un agente che legge solo l'issue sa cosa fare e quando ha finito.

## 4. Creare e controllare

Scrivi il corpo in un file nella cartella temporanea della sessione, poi:

```bash
gh issue create -R <owner>/<repo> --title "M<n> · <titolo>" --milestone "M<n> <nome>" --label "<triage>,<area>,<tipo>" --body-file <file>
```

Rileggi con `gh issue view <numero> -R <owner>/<repo> --json title,milestone,labels`. Se apri più issue che dipendono l'una dall'altra, aprile nell'ordine in cui si lavorano, così i «Bloccata da» hanno già i numeri, o aggiungili dopo averle create tutte.

Una milestone nuova si apre solo dopo averla chiesta all'utente, ed entra nella tabella di `docs/agents/milestone.md` con le sue dipendenze e col suo rilascio. Se rilascia, con lei si apre la sua issue `M<n> · Rilascio <versione>`, che resta l'ultima: ogni issue aperta dopo nella stessa milestone entra fra i suoi «Bloccata da».

Fatto quando: per ogni issue aperta il numero del prefisso è quello della milestone, la milestone è assegnata e ci sono le etichette di triage, d'area e di tipo; all'utente dai numero e titolo di ognuna.
