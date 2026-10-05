# Wiki

Come gli agenti usano [<wiki>](https://github.com/<owner>/<wiki>), la wiki sui progetti precedenti mantenuta da un agente.

La wiki è una **mappa**: dice dove guardare e come le cose si collegano, non che cosa è vero. La verità di questo progetto resta in `CONTEXT.md`, in `docs/adr/` e nel codice; quella dei progetti precedenti nei loro repo. Le conclusioni vengono dalla lettura delle fonti, mai dalla wiki da sola.

## Trovarla

È un repo a sé, accanto a questo, di solito in `../<cartella-wiki>`; il nome della cartella può cambiare da una macchina all'altra. Riconoscila da `wiki/index.md` e dal remote `<wiki>`; da un worktree, cercala anche accanto alla checkout principale:

```bash
for p in "$(git rev-parse --show-toplevel)/.." \
         "$(dirname "$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")")"; do
  for d in "$p"/*wiki*/; do
    [ -f "$d/wiki/index.md" ] &&
      git -C "$d" remote get-url origin 2>/dev/null | grep -qE '/<wiki>(\.git)?$' &&
      echo "${d%/}" && break 2
  done
done
```

Nessun risultato: la wiki non c'è. **Vai avanti senza dirlo**, con la lettura di sempre; non clonarla e non proporre di farlo.

## Quando usarla

Parti sempre da `wiki/index.md`, che ha una riga per pagina.

- **Come l'ha fatto un progetto precedente**: le pagine di confronto mettono i progetti a fianco sullo stesso tema. Prima di progettare qualcosa che esiste già altrove, leggi il confronto: spesso la stessa domanda ha già una risposta con le sue ragioni.
- **La storia di una decisione**: le mappe degli ADR li raggruppano per tema e dicono quale ne supera un altro.
- **Un flusso tra le app**: le pagine dei flussi seguono un'operazione dal client all'API e ritorno.
- **Che cosa è già noto che non torna**: la pagina delle incongruenze, se c'è.

Per un file, un simbolo o un ADR che conosci già, leggilo direttamente: la wiki non aggiunge niente.

## Quanto è vecchia

Ogni pagina ha nel frontmatter `commit:`, lo sha del repo da cui è stata scritta, e `fonti:`; `wiki/log.md` dice fin dove è arrivato l'ultimo ingest. Le modifiche del tuo branch non le conosce.

Per sapere se le fonti di una pagina sono cambiate da allora, nel repo a cui si riferisce:

```bash
git log --oneline <commit>..origin/main -- <percorsi in fonti:>
```

## Che cosa non farci

- **Non modificarla da qui.** La scrive solo il suo agente, con l'ingest: se una pagina è sbagliata, ha ragione la fonte. Se la differenza è grossa, dillo al maintainer.
- **Non citarla come fonte** in un ADR, in `CONTEXT.md`, in un test o in un commento: cita l'ADR, la voce del glossario o il file che la wiki ti ha indicato. In una issue o in una PR un link a una pagina della wiki come contesto va bene.
