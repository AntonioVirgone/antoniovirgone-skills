# Le milestone del repo

Se il repo dichiara in che ordine si lavorano le milestone, la mappa di prontezza segue quell'ordine: una milestone che aspetta un'altra blocca le sue issue. Senza dichiarazione le milestone servono solo a raggruppare le issue nel resoconto.

## Trovare la dichiarazione

Cerca `docs/agents/milestone.md` su `origin/main` (o una sezione «Milestone» in `CLAUDE.md` che ci rimanda). Il numero di una milestone non dice l'ordine: lo dice solo il documento.

Nessun documento: raggruppa per milestone, senza blocchi di milestone, e dillo nel resoconto in una riga.

## Lo stato di ogni milestone aperta

Le milestone aperte vengono da GitHub, non dal documento: `gh api 'repos/{owner}/{repo}/milestones?state=open&per_page=100' --jq '.[] | [.number, .title, .open_issues, .closed_issues] | @tsv'`. Per ognuna, con le dipendenze del documento:

- **di turno**: tutte le sue dipendenze sono chiuse su GitHub;
- **in attesa di** `<milestone>`: almeno una dipendenza è ancora aperta;
- **parallela**: il documento la dichiara un percorso parallelo, che non aspetta e non blocca;
- **da chiudere**: zero issue aperte. Se il repo dichiara una procedura di chiusura (in `CLAUDE.md` o in una skill del progetto), nominala.

Il documento può essere indietro rispetto a GitHub: una dipendenza chiusa su GitHub conta come chiusa anche se il documento la elenca ancora, e una milestone aperta che il documento non nomina va segnalata. Segnala anche le issue aperte senza milestone e quelle il cui titolo non segue la convenzione del repo sulle milestone (per esempio un prefisso `M<n> ·` con un numero diverso dalla milestone).

Fatto quando: ogni milestone aperta ha uno stato, e hai l'elenco delle incongruenze tra documento, GitHub e titoli.

## Come pesa sulle issue

Segui le regole del documento. Dove non dice altro:

- un'issue di una milestone **in attesa** ha come blocco duro la milestone che aspetta («milestone M15 aperta»), salvo che il suo corpo dica che si può anticipare;
- le issue di una milestone **parallela** si valutano solo coi blocchi fra issue;
- il blocco di milestone si ricava dal documento a ogni giro: non va scritto nelle sezioni `## Bloccata da` delle issue.
