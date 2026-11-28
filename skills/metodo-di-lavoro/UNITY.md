# Metodo di lavoro: la parte Unity

Vale per i progetti Unity collegati a Claude con `unity-setup-claude-blender` (Unity MCP a livello utente). Si aggiunge a [SKILL.md](SKILL.md).

## Worktree e Editor

Ogni sessione lavora nel suo worktree; l'Editor resta aperto sul **checkout principale**. Per compilare e testare l'Editor non serve.

- **Compilazione e test**: `tools/unity-check.sh` lancia Unity in batchmode sul worktree in cui sta, anche con l'Editor aperto sul checkout principale. Senza argomenti compila e fa girare tutti i test EditMode; `--filter "<classi o namespace separati da |>"` ne fa girare una parte; `--compile-only` controlla solo la compilazione. Esce con 0 se va tutto bene, 1 per errori di compilazione, 2 per test falliti, 3 per il resto; log e risultati in `Logs/unity-check/`. La prima volta in un worktree clona la `Library/` dal checkout principale (copia APFS: pochi secondi, niente spazio in più). Se l'Editor è aperto proprio su quel worktree lo script si rifiuta: lì si ricompila e si testa via MCP.
- **Processi pesanti**: Unity in batchmode (test, compilazione, build) si lancia solo con `tools/pesante.sh <comando>`, come fa `unity-check.sh`. Lo script tiene al massimo 6 processi pesanti su tutto il Mac, contando quelli di tutte le sessioni e di tutti i progetti (il lucchetto è comune), aspetta che il carico scenda e li fa girare con `nice -n 10` e un timeout. Per tanti in parallelo `xargs -P 6 ... tools/pesante.sh ...`, mai un ciclo con `&`. L'hook `tools/hooks/blocca_pesanti.py` rifiuta ogni comando che lancia Unity in batchmode senza `pesante.sh`: non si aggira.
- **Sessioni in parallelo**: sullo stesso Mac possono lavorare insieme più sessioni, anche di progetti Unity diversi. Compilazione, test, build e tutto il lavoro senza Editor vanno in parallelo, entro il tetto comune di `pesante.sh`. L'Editor via MCP invece lo usa **una sessione alla volta, su tutti i progetti Unity del Mac**: `unity-mcp` è uno solo, a livello utente.
- **Quale Editor risponde**: il relay del MCP si collega al primo Editor che trova fra i `bridge-*.json` di `~/.unity/mcp/connections/`, anche se è di un altro progetto. Lì restano anche i file di Editor già chiusi, e il relay risponde «Named pipe socket file not found»: controlla `editor_pid` con `ps -p` e togli solo i file dei pid morti.
- **Di chi è l'Editor**: prima di **ogni** comando MCP, anche uno che legge soltanto, leggi `Application.dataPath`.
  - È tuo se è la `Assets` del tuo worktree, oppure del checkout principale del tuo progetto, che non è di nessuna sessione: lì puoi lavorare.
  - È di un'altra sessione se è la `Assets` di un altro worktree dello stesso progetto, o di un altro progetto. Allora non gli mandi comandi e non lo chiudi: dillo all'utente e aspetta che si liberi. L'utente preferisce aspettare piuttosto che chiudere l'Editor di un'altra sessione.
- **L'Editor nel worktree**: solo per il lavoro che vuole l'Editor — scene e prefab via MCP, Play mode, catture. Allora lo sposti tu, senza chiedere:
  1. l'Editor collegato si chiude solo se è **tuo** («Di chi è l'Editor»): del checkout principale del tuo progetto o del tuo worktree. Se è di un altro progetto o di un altro worktree, fermati e aspetta. Se è tuo, controlla che non sia in Play mode e che nessuna scena sia `isDirty`; se lo è, chiedi all'utente. Poi chiudilo via MCP con `EditorApplication.delayCall += () => EditorApplication.Exit(0)` e aspetta che il processo esca (in background ci mette circa 40 s);
  2. se il worktree non ha `Library/`, clonala a Editor chiuso: `cp -cR <checkout principale>/Library <worktree>/Library`;
  3. apri il worktree con `open -na /Applications/Unity/Hub/Editor/<versione>/Unity.app --args -projectPath <worktree>`. L'Editor è pronto quando in `~/.unity/mcp/connections/` compare un `bridge-*.json` col `project_path` del worktree (circa un minuto).

  A lavoro finito riporta l'Editor sul checkout principale, con gli stessi passi.
- **Dopo il merge** il worktree si cancella, perché ogni `Library/` pesa qualche GB: chiudi l'Editor se è aperto lì, `git worktree remove <worktree>` e `git branch -d <branch>`.
- In un worktree Unity riscrive `.vscode/settings.json` col nome della soluzione del worktree: quella modifica resta fuori dai commit.

## Regole dell'Editor

- Scene e prefab si modificano **solo via MCP**, mai editando lo YAML.
- Dopo ogni modifica C# si ricompila (`tools/unity-check.sh --compile-only`, o via MCP leggendo la console se l'Editor è sul tuo worktree): zero errori prima di finire.
- Niente modifiche agli script durante il Play mode: la ricompilazione interrompe la sessione MCP.
- `Library/`, `Temp/`, `ProjectSettings/` non si toccano senza chiedere. Eccezioni: clonare la `Library/` in un worktree nuovo e `bundleVersion` nel commit della versione. Impostare `Application.runInBackground` da un comando MCP in Editor modifica `PlayerSettings.runInBackground` in `ProjectSettings.asset`: va rimesso com'era.

## Definition of Done in Unity

In più a quella generale:

- `tools/unity-check.sh` esce con 0 sul worktree (compilazione e tutti i test EditMode);
- la logica di gioco (regole, generatori, combattimento, salvataggi) sta in assembly di C# puro, senza `UnityEngine` dove si può, e ha i suoi test EditMode;
- se la modifica si vede, una prova in Play mode via MCP con le catture nella PR. Con l'Editor in background il player loop è lento e `ScreenCapture` non arriva: si renderizza la camera su una `RenderTexture` e si salva il PNG; per avere la UI nella cattura il Canvas passa per un momento a `ScreenSpaceCamera`. `Application.runInBackground = true` serve perché il gioco avanzi, e a fine prova torna `false`;
- i salvataggi del gioco possono contenere progressi veri dell'utente: durante le prove non si cancellano.

## Applicare la parte Unity

1. Copia nel progetto i template di [templates/unity/](templates/unity/): `tools/unity-check.sh`, `tools/pesante.sh`, `tools/hooks/blocca_pesanti.py` e `tools/hooks/test_blocca_pesanti.py`, con `chmod +x` sui due script.
2. Aggiungi l'hook a `.claude/settings.json` del progetto (quello versionato, non `settings.local.json`), unendolo a quello che c'è: il blocco è in [templates/unity/claude-settings.json](templates/unity/claude-settings.json).
3. Servono un assembly di test EditMode (`<Namespace>.Tests`, con `UNITY_INCLUDE_TESTS`) e almeno un test, altrimenti `unity-check.sh` non ha niente da far girare.
4. Nel `CLAUDE.md`, sezione «Struttura», le righe di `tools/unity-check.sh` e `tools/pesante.sh`.

Fatto quando: `python3 -m unittest test_blocca_pesanti` passa dalla cartella `tools/hooks`, e `tools/unity-check.sh` esce con 0 da un worktree del progetto.
