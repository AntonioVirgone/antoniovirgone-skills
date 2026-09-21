---
name: monorepo-api-web-mobile-grill-iniziale
description: Primo grill di dominio di un monorepo appena impostato con /antonio-skills:monorepo-api-web-mobile-setup. A differenza di /grilling, che è generico, segue una scaletta fissa, tratta le specifiche di vecchi progetti come guida e produce CONTEXT.md, i primi ADR, un elenco di issue e una PR.
disable-model-invocation: true
---

# Grill iniziale di un monorepo API + web + mobile

Definisci il dominio del progetto con l'utente, prima che esista una sola issue. Il grill si fa una volta, all'avvio, e lascia tre cose: il primo `CONTEXT.md`, i primi ADR, un elenco di issue da cui partire.

Sotto usa due skill del plugin `mattpocock-skills`: **`grilling`** per il modo di interrogare, **`domain-modeling`** per scrivere glossario e ADR. Questa skill aggiunge la scaletta, il trattamento delle vecchie specifiche e la chiusura.

Richiesta dell'utente: $ARGUMENTS

## Passi

### 1. Prerequisiti

- `docs/agents/domain.md` esiste: è il segno che il setup è stato fatto, e contiene il formato di `CONTEXT.md` e degli ADR. Se manca, di' all'utente di lanciare prima `/antonio-skills:monorepo-api-web-mobile-setup` e fermati.
- Le skill `grilling` e `domain-modeling` sono disponibili. Se mancano, di' all'utente come installare il plugin (`/plugin install mattpocock-skills@claude-plugins-official`) e fermati.
- Crea il branch `docs/dominio-iniziale` da `main` aggiornato.

Fatto quando: i due file e le due skill ci sono, e sei sul branch.

### 2. Leggi

Carica `grilling` e `domain-modeling`. Poi leggi `CLAUDE.md`, `docs/agents/`, i subagenti in `.claude/agents/`, il README e la richiesta dell'utente. Se esistono specifiche di progetti precedenti (i subagenti o le note in cima ai README le indicano), leggile per intero: seguono le regole di [Vecchie specifiche](#vecchie-specifiche).

Apri il grill con un riepilogo di cinque righe: cosa hai capito del progetto, e quali specifiche hai trovato.

Fatto quando: l'utente ha confermato o corretto il riepilogo.

### 3. Il grill

Percorri la [scaletta](#scaletta), nell'ordine che le risposte rendono più naturale.

- **Una domanda alla volta**, con la tua raccomandazione e il perché; aspetta la risposta prima della successiva.
- Le raccomandazioni partono da ciò che serve a questo progetto. Quando coincidono con una scelta delle vecchie specifiche, dillo e cita il documento.
- I fatti li cerchi tu, nel repo e nei documenti; all'utente chiedi le decisioni.
- **Scrivi mentre procedi**: un termine fissato va subito in `CONTEXT.md`, una decisione con un'alternativa scartata che vale la pena ricordare va subito in un ADR, nel formato di `docs/agents/domain.md`. Le decisioni ovvie restano nel glossario o nella conversazione.
- Nel glossario ogni concetto dice anche il suo nome in codice, nella lingua degli identificatori scelta al setup.

Fatto quando: ogni voce della scaletta ha una decisione o compare tra le domande aperte, e l'utente dice che basta.

### 4. Chiusura

Presenta all'utente:

1. se c'erano vecchie specifiche: cosa è stato **tenuto**, cosa **cambiato**, cosa **scartato**;
2. i termini fissati, gli ADR scritti, le domande rimaste aperte;
3. un primo elenco di issue, titolo e una riga ciascuna, in un ordine che si possa costruire (prima le fondamenta: scaffolding delle app, tipi condivisi, autenticazione).

Le issue restano una proposta: le crei su GitHub quando l'utente te lo chiede, seguendo `docs/agents/issue-tracker.md`. Ogni issue che dipende da un'altra chiude il corpo con una sezione `## Bloccata da` (una riga `- #N — motivo` per blocco): è quella che `/antonio-skills:controllo-issue` rilegge.

Poi commit (`docs: glossario e primi ADR`), push, `gh pr create` verso `main`. La PR resta aperta: la mergia l'utente.

Fatto quando: l'utente ha il riepilogo e il link alla PR.

## Scaletta

1. **Il nucleo del prodotto** — cosa lo rende quello che è, e cosa serve alla prima versione usabile. Il resto si valuta dopo, e può restare fuori.
2. **Il vocabolario di base** — i concetti principali: cosa sono per noi, quali sinonimi unificare, quali parole evitare.
3. **Dove vive la logica condivisa** — regole che più app devono applicare allo stesso modo (per esempio un engine e il suo validatore): pacchetto comune o altro. Di solito diventa un ADR.
4. **Chi ha l'ultima parola** — client o server, sui dati che contano (progressi, crediti, acquisti…): cosa si fa offline, e come si riconcilia.
5. **I cicli di vita** delle entità principali: stati, passaggi, cosa succede a ciò che dipende da un'entità quando cambia.
6. **Utenti e ruoli** — chi fa cosa, come si autentica, cosa vede ciascuno in quale app.

Aggiungi le zone specifiche che emergono dalla lettura o dalla richiesta dell'utente.

## Vecchie specifiche

Documentazione estratta da progetti precedenti è una **guida**: esperienza da cui attingere, con `CONTEXT.md` e gli ADR come unica verità del progetto nuovo.

- Un concetto, una regola o una meccanica entra solo dopo una decisione dell'utente. La proponi citando il documento da cui viene e cosa cambieresti.
- Il vocabolario si sceglie da capo: un nome vecchio confuso lascia il posto a uno migliore, e il vecchio finisce sotto _Avoid_.
- Una scelta che sembra dettata dai limiti del vecchio progetto (stack diverso, scorciatoia, pezzo aggiunto dopo) va messa in discussione con l'utente.
- Una cosa importante che i vecchi progetti avevano e che viene scartata va in un ADR, così chi legge le specifiche sa che è stata esclusa di proposito.
- Se un subagente o un README tratta quelle specifiche come comportamento da riprodurre, riscrivi la riga: sono un riferimento storico, e dove divergono da `CONTEXT.md` o da un ADR prevalgono questi ultimi.
