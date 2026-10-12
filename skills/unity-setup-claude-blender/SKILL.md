---
name: unity-setup-claude-blender
description: Collega un progetto Unity a Claude Code e a Blender — Unity MCP (ponte dell'Editor e relay a livello utente), Blender MCP nel `.mcp.json`, Git LFS per modelli e audio, `.gitignore` Unity, solo nuovo Input System e un CLAUDE.md con le regole per lavorare sull'Editor via MCP. Usala quando si apre o si crea un progetto Unity e bisogna prepararlo per lavorarci con Claude, anche se l'utente dice solo "configura questo progetto Unity come vibecode-test" o "collega Claude a Unity e Blender".
---

# Setup di un progetto Unity per Claude Code e Blender

Prepara il progetto Unity corrente perché Claude lo controlli via MCP e ci porti modelli fatti in Blender:

- **Unity MCP**: il pacchetto `com.unity.ai.assistant` avvia nell'Editor un ponte, e Claude ci arriva attraverso un relay in `~/.unity/relay/`. Il server si registra **a livello utente** (`~/.claude.json`): il percorso del relay dipende dalla macchina, quindi non va nel repo;
- **Blender MCP**: `uvx blender-mcp` nel `.mcp.json` del progetto, più l'addon dentro Blender;
- **Git** con LFS per `.fbx`, `.blend`, audio e immagini, e il `.gitignore` di Unity;
- un **CLAUDE.md** con le regole imparate sul campo: scene e prefab solo via MCP, console dopo ogni compilazione, niente script in Play mode, screenshot su `RenderTexture`, convenzioni di export da Blender.

Questa skill non crea il progetto: quello si fa dall'Unity Hub (o con `unity:new-unity-project`). Parte da un progetto che esiste già, nuovo o vecchio.

Richiesta dell'utente: $ARGUMENTS

Quello che la richiesta dice già (nome del gioco, namespace, "come al solito") precompila le scelte del passo 2.

I file da copiare stanno in `templates/`, accanto a questo file.

## Chi fa cosa

Alcuni passi vivono solo dentro un'app: aprire il progetto nell'Editor, approvare la connessione MCP, installare l'addon in Blender. Li fa l'utente, e l'agente glieli dà come checklist numerata con i menu esatti, poi **verifica** con i tool MCP che siano andati a buon fine. Non dichiarare fatto un passo che non hai verificato.

I tool MCP si caricano all'avvio della sessione di Claude Code: un server registrato o abilitato a metà sessione si vede solo dopo `/mcp` (riconnetti) o in una sessione nuova. Quando serve, dillo all'utente e riprendi lì.

## Passi

### 1. Prerequisiti

Verifica, e riporta l'esito di ciascuno:

- la cartella è un progetto Unity: ci sono `Assets/`, `Packages/manifest.json` e `ProjectSettings/ProjectVersion.txt` (da lì leggi la versione dell'Editor). Se non lo è, fermati e suggerisci di crearlo dall'Hub;
- `git` e `git lfs version` funzionano (manca LFS: `brew install git-lfs`);
- `uvx --version` funziona (manca: `brew install uv`): è quello che lancia `blender-mcp`;
- Blender è installato (`/Applications/Blender.app` su macOS, o `blender --version`);
- l'Editor Unity della versione giusta è installato (`~/Applications/Unity/Hub/Editor/<versione>/` o `/Applications/Unity/Hub/Editor/<versione>/`).

Se manca qualcosa, di' cosa e come si installa, e riprendi alla conferma: installare è una scelta dell'utente.

Fatto quando: i controlli sono verdi, o l'utente ha deciso di procedere senza Blender (allora salta i passi su Blender).

### 2. Raccogli le scelte, in una volta sola

Leggi `Packages/manifest.json`, `ProjectSettings/ProjectSettings.asset` (`activeInputHandler`), le cartelle in `Assets/` e un eventuale CLAUDE.md. Poi presenta **in un unico messaggio** la tabella con il valore che useresti e da dove viene:

- nome del gioco e cartella in `Assets/` (default: il nome del gioco in PascalCase, o quello del progetto se il gioco non ne ha uno);
- namespace radice C# (default: quello già usato negli script; altrimenti chiedi se riusare il prefisso degli altri progetti dell'utente, per esempio `VibecodeTest.<Gioco>`);
- pipeline di render e versione dell'Input System (dal manifest);
- se impostare **solo nuovo Input System** (`activeInputHandler: 1`): tocca `ProjectSettings`, quindi chiedi;
- se esistono già `.gitattributes`, `.gitignore`, `.mcp.json` o CLAUDE.md: li integri, non li sovrascrivi.

Aspetta la conferma o le correzioni prima di scrivere.

### 3. I file del repo

- **Git**: se non c'è un repo, `git init`. Poi `git lfs install --local`: attiva i filtri LFS solo in questo repo, senza toccare `~/.gitconfig`.
- **`.gitattributes`** da `templates/gitattributes` (il template di Unity: oltre a modelli e audio mette in LFS anche immagini, video, archivi e librerie), **`.gitignore`** da `templates/gitignore` (include `.claude/settings.local.json`). Se esistono già, aggiungi solo le regole che mancano. Se ci sono già `.fbx`, `.blend` o audio committati senza LFS, dillo all'utente: spostarli in LFS riscrive la storia (`git lfs migrate`) ed è una scelta sua.
- **`.mcp.json`** da `templates/mcp.json`. Se esiste, aggiungi solo il server `blender`.
- **`.claude/settings.local.json`** con `"enabledMcpjsonServers": ["blender"]`, unito a quello che c'è: evita la domanda di approvazione al primo avvio.
- **CLAUDE.md** da `templates/CLAUDE.md`, con i segnaposto riempiti dalle scelte del passo 2 (versioni come nel manifest e in `ProjectVersion.txt`, per esempio `Unity 6 (6000.5.3f1), URP 17.5`). La sezione Struttura descrive il progetto com'è: togli le righe di cartelle che non esistono e non verranno create. Se l'utente non vuole solo il nuovo Input System, togli quella parte dalla riga dello Stack. Le regole in fondo valgono per ogni progetto: tienile. Se un CLAUDE.md esiste, aggiungi le sezioni che mancano senza toccare il resto.

Fatto quando: `git check-attr filter -- Art/x.blend Assets/x.fbx` risponde `lfs` per entrambi e i file sono scritti.

### 4. Il pacchetto Unity AI Assistant

Se `com.unity.ai.assistant` non è nel manifest, va aggiunto con una versione compatibile con l'Editor. Non inventare il numero: è un pacchetto in rapida evoluzione, spesso in pre-release.

L'Editor ha il progetto aperto se esiste `Temp/UnityLockfile` e c'è un processo Unity (`pgrep -fl Unity.app`). Con l'Editor aperto non modificare il manifest a mano: lo ricarica al volo, ma conviene passare dal Package Manager.

- Con l'Editor chiuso: trova la versione con la skill `unity:unity-package-management` e aggiungila al manifest.
- Con l'Editor aperto: l'utente lo aggiunge da **Window → Package Manager → + → Add package by name** → `com.unity.ai.assistant`.

Poi l'utente apre il progetto nell'Editor (se non è già aperto) e controlla **Edit → Project Settings → AI → Unity MCP Server**: **Unity Bridge** deve dire **Running**. All'avvio l'Editor installa anche il relay in `~/.unity/relay/`.

Unity ha dichiarato il server MCP deprecato a favore della Unity CLI. Se in quella pagina il server MCP non c'è più, fermati e proponi la strada della CLI (skill `unity:unity-cli`): le regole del CLAUDE.md restano valide, cambia solo il canale.

Fatto quando: il pacchetto è nel manifest, il relay esiste in `~/.unity/relay/` e l'utente conferma che il bridge è Running. Il relay da solo non prova niente: lo installa qualunque progetto con il pacchetto.

### 5. Unity MCP a livello utente

Controlla con `claude mcp get unity-mcp` se è già registrato. Se c'è e punta a un relay che esiste, non toccarlo: serve tutti i progetti Unity della macchina.

Se manca, registralo per l'utente, con il binario giusto per l'architettura (`uname -m`: `arm64` → `relay_mac_arm64`, altrimenti `relay_mac_x64`) e il percorso assoluto, perché il client non espande `~`:

```bash
claude mcp add --scope user unity-mcp -- "$HOME/.unity/relay/relay_mac_arm64.app/Contents/MacOS/relay_mac_arm64" --mcp
```

Con più Editor aperti insieme il relay si collega al primo che trova: se l'utente lavora spesso così, proponi una voce in più solo per questo progetto e solo su questa macchina, con `claude mcp add --scope local unity-mcp -- <relay> --mcp --project-path <percorso del progetto>`, invece di cambiare quella utente.

Poi l'utente riconnette (`/mcp`) e, al primo collegamento, approva il client in **Project Settings → AI → Unity MCP Server → Pending Connections → Allow**.

Fatto quando: `Unity_GetConsoleLogs` risponde.

### 6. Blender MCP

Il server è nel `.mcp.json`; manca l'addon dentro Blender. Checklist per l'utente:

1. Scaricare `addon.py` dal repository `ahujasid/blender-mcp` su GitHub.
2. In Blender: **Edit → Preferences → Add-ons → Install from Disk**, scegliere il file e attivare **Interface: Blender MCP**.
3. Nella vista 3D, pannello laterale (**N**) → scheda **BlenderMCP** → **Connect to MCP server**.
4. In Claude Code: `/mcp` per riconnettere `blender`.

Fatto quando: `get_addon_status` e `get_scene_info` del server `blender` rispondono.

Per i sorgenti crea `Art/Blender/` alla radice (fuori da `Assets/`: Unity importerebbe i `.blend` da solo). I modelli si esportano in FBX in `Assets/<Gioco>/Models/` con le convenzioni del CLAUDE.md.

### 7. Impostazioni via MCP

Solo quelle confermate al passo 2, sempre dall'Editor via MCP e mai editando lo YAML di `ProjectSettings`.

- **Solo nuovo Input System**: se `activeInputHandler` non è `1`, con `Unity_RunCommand`:

  ```csharp
  var ps = Unsupported.GetSerializedAssetInterfaceSingleton("PlayerSettings");
  var so = new SerializedObject(ps);
  so.FindProperty("activeInputHandler").intValue = 1;
  so.ApplyModifiedProperties();
  AssetDatabase.SaveAssets();
  ```

  Il cambio vale dopo il riavvio dell'Editor: dillo all'utente. Serve il pacchetto `com.unity.inputsystem` nel manifest.
- Se l'utente lo chiede, le cartelle del gioco in `Assets/<Gioco>/` (`Scenes`, `Scripts`, `Models`, `Materials`, `Prefabs`) con `AssetDatabase.CreateFolder`, così nascono anche i `.meta`.

Fatto quando: la console dell'Editor ha zero errori.

### 8. Verifica e riepilogo

Chiudi con una tabella: per ogni pezzo (Git e LFS, `.gitignore`, `.mcp.json`, pacchetto, bridge, unity-mcp utente, connessione approvata, addon Blender, Input System, CLAUDE.md) lo stato e come l'hai verificato. Elenca a parte quello che resta da fare all'utente.

Proponi un commit: i file nuovi (`.gitattributes`, `.gitignore`, `.mcp.json`, CLAUDE.md) e il manifest; se il repo l'hai appena creato, il primo commit comprende tutto il progetto (`Assets/`, `Packages/`, `ProjectSettings/`), che il `.gitignore` già filtra. Committa solo se l'utente dice di sì, e non fare push senza che lo chieda.
