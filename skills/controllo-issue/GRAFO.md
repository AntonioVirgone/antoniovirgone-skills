# Il grafo del codice (graphify)

Se il repo ha un grafo costruito con graphify, usalo come **mappa** per il passo 3: dice dove guardare, non che cosa c'è. Senza grafo il passo 3 si fa come sempre, cercando nel codice.

## Trovarlo

`graphify-out/` di solito è ignorata da git, quindi in un worktree non c'è: cercala prima nella radice del checkout corrente, poi in quella della checkout principale.

```bash
for d in "$(git rev-parse --show-toplevel)" \
         "$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"; do
  [ -f "$d/graphify-out/graph.json" ] && echo "$d/graphify-out" && break
done
```

Nessun risultato, o `graphify` non è nel `PATH`: niente grafo, salta il resto di questo file.

## Quanto è vecchio

Il grafo fotografa i file della checkout com'erano quando è stato costruito, non `origin/main`. Elenca i file cambiati su `origin/main` da allora:

```bash
G=<cartella trovata sopra>
C=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("built_at_commit",""))' "$G/graph.json")
if [ -n "$C" ] && git cat-file -e "$C^{commit}" 2>/dev/null; then
  git diff --name-only "$C" origin/main
else
  git log origin/main --since="$(date -r "$G/graph.json" '+%Y-%m-%dT%H:%M:%S%z')" --name-only --format= | sort -u
fi
```

graphify scrive in `graph.json` il commit da cui l'ha costruito (`built_at_commit`, riportato anche in `GRAPH_REPORT.md`): il confronto con quel commit dà esattamente i file cambiati. I grafi costruiti con versioni più vecchie di graphify non lo scrivono, e allora si ripiega sulla data del file, che è meno precisa.

Per quei file il grafo non sa niente: cercali direttamente nel codice. Se l'elenco tocca buona parte del codice, il grafo vale poco: usalo appena o per niente, e proponi nel resoconto di aggiornarlo nella checkout principale: `graphify update .` per il codice (senza token), `/graphify . --update` se sono cambiati anche i documenti.

## Usarlo

Per ogni cosa che un criterio di accettazione dà per esistente (un endpoint, una regola, uno schema, una schermata):

```bash
graphify query "<termini>" --graph "$G/graph.json" --budget 1500   # dove se ne parla
graphify path "<A>" "<B>" --graph "$G/graph.json"                  # come si collegano due pezzi
graphify explain "<nodo>" --graph "$G/graph.json"                  # un nodo e i suoi vicini
```

Cerca con i nomi del codice (in genere inglesi), non con quelli delle issue: il grafo confronta le parole alla lettera, senza sinonimi né traduzioni. Zero risultati non vuol dire «non esiste»: prova altri termini o cerca nel codice.

Poi apri su `origin/main` i file che il grafo indica e verifica lì, come chiede il passo 3: un nodo nel grafo non prova che la logica ci sia, e può venire da un file cambiato o sparito da allora.

Fatto quando: per le issue che hai controllato col grafo sai quali verifiche ha guidato, e nessuna conclusione poggia solo sul grafo.
