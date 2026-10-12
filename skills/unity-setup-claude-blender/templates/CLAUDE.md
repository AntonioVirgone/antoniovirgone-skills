# <Progetto> — istruzioni per Claude

## Stack
- Unity <versione Editor>, <pipeline di render>, C#, Input System <versione> (solo nuovo Input System: `activeInputHandler: 1`)
- Editor controllato via MCP `unity-mcp`, configurato a livello utente in `~/.claude.json` (non in `.mcp.json`: il percorso del relay è specifico della macchina)
- Modelli 3D via MCP `blender`, configurato nel `.mcp.json` del progetto
- `.fbx` e `.blend` sono tracciati con Git LFS

## Struttura
La radice del repo coincide con la radice del progetto Unity.
- `Assets/<Gioco>/` → <il gioco, in una riga>
  - `Scenes/`, `Scripts/`, `Models` (FBX da Blender), `Materials` (nomi uguali ai materiali Blender: l'importer li rimappa per nome), `Prefabs` (un prefab per modello: root con lo script + figlio `Model`)
- `Art/Blender/` → sorgenti `.blend`
- `Assets/Settings` → asset della pipeline di render
- Nuovo codice C# nel namespace `<Namespace>` o in suoi sotto-namespace; nuove cartelle solo quando servono

## Regole
- Scene e prefab: modificali SOLO tramite tool MCP, mai editando lo YAML
- Dopo ogni modifica C#: ricompila via MCP e leggi la console; zero errori prima di finire. Non modificare script durante il Play mode: il domain reload interrompe la sessione MCP e azzera gli static
- Export da Blender: FBX, scala 1 unità = 1 metro, -Z forward, Y up, Apply Transform. Modella con il fronte verso **-Y** in Blender, così in Unity guarda verso +Z
- Nomi asset in PascalCase; un prefab per asset importato
- Non toccare `Library/`, `Temp/`, `ProjectSettings/` senza chiedere. Attenzione: impostare `Application.runInBackground` da un comando MCP in Editor modifica `PlayerSettings.runInBackground` in `ProjectSettings.asset`

## Test in Play mode via MCP
- Con l'Editor in background il player loop gira lento e gli screenshot asincroni (`ScreenCapture`) non arrivano: renderizza la camera su una `RenderTexture` e salva il PNG
- Per includere la UI nel render, passa temporaneamente il Canvas a `ScreenSpaceCamera` e poi riportalo a `ScreenSpaceOverlay`
- `Application.runInBackground = true` serve perché il player loop avanzi con l'Editor in background: rimettilo a `false` a fine test
- Il salvataggio del gioco può contenere progressi reali dell'utente: non cancellarlo durante i test
