---
name: controllo-issue
description: Controlla le issue aperte di un repo GitHub contro il codice su main e dice quali si possono implementare adesso, quali sono bloccate e da cosa, quali aspettano una decisione. Se il repo ha un design versionato, verifica anche se l'ultima versione chiede modifiche.
disable-model-invocation: true
---

# Controllo delle issue

Dai all'utente una **mappa di prontezza**: ogni issue aperta in una sola categoria, con il motivo e le issue che la bloccano. La mappa si basa sul codice su `main` e sulle issue come sono adesso, non su quello che ricordi di sessioni precedenti.

Richiesta dell'utente: $ARGUMENTS

## Passi

### 1. Convenzioni del repo

Leggi `CLAUDE.md` / `AGENTS.md` e, se ci sono, i documenti a cui rimandano su issue tracker, etichette di triage e branching (per esempio `docs/agents/`). Da lì prendi il vocabolario delle etichette (`needs-triage`, `ready-for-agent`…) e le aree. Se il repo non le dichiara, usa le etichette che trovi sulle issue.

Fatto quando: sai quali etichette vogliono dire «da smistare», «per un agente», «per una persona».

### 2. Stato di partenza

- `git fetch origin` e lavora su `origin/main` (o il branch principale): leggi i file con `git show origin/main:<percorso>` o in un checkout staccato, mai sul branch locale, che può essere indietro.
- Issue aperte con corpo ed etichette: `gh issue list --state open --limit 200 --json number,title,labels,body`.
- Issue chiuse, solo numero e titolo: sono i mattoni già posati.
- PR aperte con le issue che chiudono: `gh pr list --state open --json number,title,headRefName,body`. Un'issue con una PR aperta è **in corso**.

Fatto quando: hai i tre elenchi e sai su quale commit di `main` stai ragionando.

### 3. Dipendenze di ogni issue

Per ogni issue aperta:

1. Se il corpo ha una sezione `## Bloccata da` o `## Ordine consigliato` (formato in [Scrivere i blocchi](#scrivere-i-blocchi)), parti da quella e verifica che ogni riga sia ancora vera.
2. Altrimenti ricavale dai criteri di accettazione: per ciascun criterio chiediti che cosa deve già esistere perché si possa soddisfare (un endpoint, una regola del motore, un ruolo, uno schema, una schermata) e quale issue — aperta o chiusa — lo fornisce.
3. Controlla nel codice su `main` che quello che dai per fatto ci sia davvero: tipi senza logica, stub e TODO con il numero dell'issue contano come **non fatto**. Cerca anche il caso opposto: un'issue aperta il cui lavoro è già su `main`, da segnalare come «forse da chiudere».

Distingui un blocco **duro** (senza l'altra issue un criterio non si può soddisfare) da un **ordine consigliato** (si può fare, ma dopo costa meno o evita un buco temporaneo, per esempio endpoint pubblici prima dell'autenticazione).

Fatto quando: ogni issue aperta ha l'elenco dei suoi blocchi duri, ciascuno con una riga di motivo, e i blocchi che dai per risolti sono verificati nel codice.

### 4. Classifica

Ogni issue va in una sola categoria:

- **Pronta** — etichetta «per un agente», nessun blocco duro aperto, nessuna PR aperta.
- **Pronta con condizione** — nessun blocco duro, ma un ordine consigliato da rispettare o una parte che si può anticipare: scrivi la condizione.
- **Per una persona** — pronta, ma etichettata per un umano (decisioni di gusto, contenuti, UI da valutare a occhio).
- **Da smistare** — `needs-triage` / `needs-info`: di' quale decisione manca e a chi spetta.
- **In corso** — c'è una PR aperta.
- **Bloccata** — almeno un blocco duro aperto: elenca i numeri.

Poi ricava le **catene**: l'ordine in cui le bloccate si sbloccano (`#10 → #14 → #15`), per area. Segnala l'issue che sblocca più lavoro.

Fatto quando: ogni issue aperta compare in esattamente una categoria.

### 5. Design

Se il repo ha un design versionato — una cartella di mockup (`docs/design/`, `design/`…), tag `design-v*`, un README con changelog — segui [DESIGN.md](DESIGN.md). Altrimenti salta il passo e dillo nel resoconto in una riga.

### 6. Resoconto

In chat, in quest'ordine:

1. il commit di `main` su cui hai ragionato;
2. tabella delle **pronte** (numero, titolo, perché è libera, cosa sblocca), poi le pronte con condizione, per una persona, da smistare, in corso;
3. le **bloccate** come catene per area, non come tabella lunga;
4. le issue forse da chiudere e i blocchi dichiarati che non tornano più;
5. l'esito del design, se c'è.

Chiudi proponendo le scritture del passo 7 che servono, e chiedi quali fare. Non scrivere niente su GitHub prima della risposta.

### 7. Scritture, solo su richiesta

#### Scrivere i blocchi

Per ogni issue con blocchi duri, aggiungi o aggiorna in fondo al corpo, prima di eventuali righe finali di contesto, questa sezione — è quella che il passo 3 rilegge al giro successivo:

```markdown
## Bloccata da

- #17 — il ruolo amministratore arriva con l'autenticazione
- #22 — la scrittura deve finire nel registro delle attività
```

Solo blocchi duri; l'ordine consigliato, se serve, va in una riga `Meglio dopo #N: <motivo>` sotto la lista. Un'issue senza blocchi duri ma con un ordine consigliato ha invece una sezione `## Ordine consigliato` con quella riga. Quando un blocco si chiude, la riga si toglie; se la lista resta vuota, si toglie la sezione.

Le sezioni vanno prima della riga finale di contesto (`---` + rimandi), se c'è. Modifica il corpo con `gh issue edit <n> --body-file <file>`, partendo dal corpo appena riletto con `gh issue view`, così non sovrascrivi modifiche fatte nel frattempo. Scrivi nella lingua delle issue.

Fatto quando: rileggendo ogni issue toccata, la sezione c'è e il resto del corpo è identico a prima.
