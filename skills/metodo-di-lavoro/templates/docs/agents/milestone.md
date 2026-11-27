# Ordine delle milestone

Le milestone sono le milestone GitHub di `<owner>/<repo>`, col nome `M<n> <nome>`. Il numero non dice l'ordine in cui si lavorano: lo dicono le **dipendenze** qui sotto. Le regole generali (dipendenze, percorsi paralleli, issue di rilascio, versioni) sono nel metodo di lavoro, skill `antoniovirgone-skills:metodo-di-lavoro`.

- Una milestone è **di turno** quando le sue dipendenze sono chiuse. Un'issue di una milestone non di turno è bloccata dalla dipendenza ancora aperta, salvo che il suo corpo dica che si può anticipare.
- Una milestone nuova entra nella tabella quando si apre, con dipendenze e rilascio; una milestone chiusa esce dalla tabella e dal «Dipende da» delle altre.

## Rilasci

<Dove si rilascia (itch.io, store…), se pubblico o privato, la numerazione dei primi rilasci; i comandi stanno in `docs/agents/rilasci.md`.>

## Milestone aperte

| Milestone | Dipende da | Rilascio | Perché |
| --- | --- | --- | --- |
| M0 Organizzazione | — | no | Il metodo di lavoro e le prime decisioni vengono prima del codice |

## Percorsi paralleli

| Milestone | Rilascio | Perché |
| --- | --- | --- |
| M<n> Ritocchi | no: non si chiude; i ritocchi escono col rilascio successivo | Bug e piccoli difetti che non appartengono a un'altra milestone aperta |
