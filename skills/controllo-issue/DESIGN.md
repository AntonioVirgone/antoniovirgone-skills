# Controllo del design

Il ramo del passo 5 di [SKILL.md](SKILL.md): il repo tiene un design versionato, e va deciso se l'ultima versione chiede modifiche — al repo, alle issue o al design stesso — o se per ora va bene.

## 1. Ultima versione e cosa è cambiato

- Trova l'ultima versione: tag `design-v*` (`git tag -l 'design-*' --sort=-v:refname`), il changelog del README del design, o l'ultimo commit che tocca la cartella.
- Guarda anche i commit **dopo** l'ultimo tag che toccano la cartella (`git log <tag>..origin/main -- <cartella>`): rinomini e ritocchi non taggati sono spesso quelli che lasciano riferimenti rotti.
- Leggi il diff rispetto alla versione precedente (`git diff <tag-precedente> <tag> --stat -- <cartella>`) e il changelog.

Fatto quando: sai quali tavole sono nuove, cambiate, rinominate o spostate.

## 2. Coerenza del repo con il design

- **Riferimenti**: cerca nel repo (`docs/`, README del design, prompt, `CONTEXT.md`) e nei corpi delle issue i percorsi e i nomi delle tavole; ogni percorso deve esistere su `main`.
- **Vocabolario**: i nomi degli elementi nuovi del design devono avere una voce nel glossario del dominio se il repo ne ha uno; un elemento chiamato in due modi diversi è da segnalare.
- **Perimetro**: se il repo divide il lavoro in tappe o versioni (ADR, README del design), controlla che ogni elemento nuovo sia assegnato a una tappa.

## 3. Copertura delle issue

Per ogni issue di interfaccia aperta, confronta i criteri di accettazione con le tavole:

- criterio con la sua tavola o il suo stato → coperto;
- criterio senza tavola (uno stato d'errore, offline, vuoto, una voce di impostazioni) → **lacuna**: di' se blocca l'issue adesso o si può colmare con una versione successiva prima di iniziarla;
- tavola senza issue → elemento che nessun ticket costruisce.

Segnala le issue di interfaccia che non citano le tavole: chi le implementa non sa che il mockup esiste.

Fatto quando: ogni issue di interfaccia aperta ha il suo elenco di tavole e di lacune.

## 4. Nel resoconto

Un verdetto in una riga — «va bene così», «va bene con correzioni piccole», «serve una nuova versione prima di #N» — seguito da: correzioni da fare nel repo, lacune per issue, rimandi alle tavole da aggiungere alle issue. Tra le scritture proposte del passo 7 includi, se servono, una sezione `## Design` nelle issue di interfaccia:

```markdown
## Design

Tavole del mockup (`docs/design/mobile/project/`, v10): `Main`, `Partita8x8`, `StatoSacchetto*`.
Mancano: stato offline della mappa.
```
