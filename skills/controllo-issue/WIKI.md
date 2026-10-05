# La wiki del progetto

Se il repo ha una wiki mantenuta da un agente — un repo a sé che sintetizza glossario, ADR e codice —, usala come **mappa** per il passo 3: dice quali app tocca un criterio, quali ADR si superano a vicenda e che cosa è già noto che non torna, non che cosa c'è su `main`. Senza wiki il passo 3 si fa come sempre.

## Trovarla

Il plugin non sa dove sta: lo dice il repo. Cerca `docs/agents/wiki.md` su `origin/main` (o una sezione «Wiki» in `CLAUDE.md` che ci rimanda) e segui le sue istruzioni per trovare il clone locale, anche da un worktree.

Nessun documento, o il documento c'è ma la wiki non si trova: niente wiki, salta il resto di questo file senza dirlo. Non clonarla e non proporre di farlo.

## Quanto è vecchia

Se `docs/agents/wiki.md` spiega come capirlo, segui quello. Altrimenti, nelle wiki con il frontmatter per pagina:

- `commit:` è lo sha di questo repo da cui la pagina è stata scritta, `fonti:` i file letti per scriverla;
- per sapere se una pagina è indietro: `git log --oneline <commit>..origin/main -- <percorsi in fonti>`;
- il log della wiki (`wiki/log.md`) dice fin dove è arrivato l'ultimo ingest.

Una pagina con le fonti cambiate da allora vale come indicazione di dove guardare, non di che cosa c'è. Se è indietro buona parte di quello che ti serve, usala poco e dillo nel resoconto, proponendo l'ingest nella sessione della wiki: da qui la wiki non si scrive.

## Usarla

Parti dall'indice (`wiki/index.md`), che ha una riga per pagina, e apri solo le pagine che servono alle issue che stai controllando.

- **Flussi tra le app**: per un criterio che attraversa più app (un'azione del client che arriva all'API e torna come evento), la pagina del flusso elenca file e funzioni da verificare su `main`. Ti dice anche se l'issue tocca un pezzo che un'altra issue aperta sta cambiando.
- **Mappa degli ADR**: se un criterio si appoggia a un ADR, controlla che non sia superato o modificato da uno più recente, anche quando l'ADR vecchio non lo dice. Un criterio che contraddice l'ADR in vigore **non cambia la categoria** dell'issue, che dipende solo da etichette, blocchi e PR: segnalalo con una nota accanto all'issue e nel resoconto. Se va rimessa in triage, lo decide l'utente (passo 7).
- **Incongruenze aperte**: le contraddizioni già note tra ADR, glossario e codice, ciascuna con la sua issue. Un'issue aperta che compare lì, o che si appoggia a una parte contraddittoria, merita una nota nel resoconto; anche qui la categoria non cambia.

Il nome di una pagina e le sue parole sono quelle del dominio, non quelle del codice: qui si cerca nell'indice con le parole delle issue, al contrario del grafo.

Poi apri su `origin/main` i file che la wiki indica e verifica lì, come chiede il passo 3. Non citare la wiki come prova nel resoconto né nelle sezioni `## Bloccata da`: cita l'ADR, la voce del glossario o il file che ti ha indicato.

Fatto quando: per le issue che hai controllato con la wiki sai quali verifiche ha guidato, e nessuna conclusione poggia solo sulla wiki.
