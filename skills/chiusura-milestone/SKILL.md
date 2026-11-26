---
name: chiusura-milestone
description: Chiude una milestone col suo rilascio — versione nuova, build da main, prova, caricamento, tag, devlog e aggiornamento di docs/agents/milestone.md — oppure fa un rilascio di sole correzioni. Vale per ogni progetto che segue il metodo di lavoro; i comandi di build e caricamento li dà il progetto.
disable-model-invocation: true
argument-hint: "M<n> | patch"
---

# Chiusura di una milestone

Le regole sono nella skill `metodo-di-lavoro` («Versioni e rilasci»); i comandi di build, prova e caricamento del progetto in `docs/agents/rilasci.md`, la numerazione e dove si rilascia in `docs/agents/milestone.md`. Leggili prima di partire. Con `patch` è un rilascio di sole correzioni da `main`, senza chiudere una milestone: salta i passi che parlano della milestone.

Una milestone che non rilascia si chiude coi soli passi 1 e 7.

Richiesta: $ARGUMENTS

## 1. Si può chiudere?

- Issue aperte della milestone: `gh issue list --milestone "M<n> <nome>" --state open`. L'unica che può restare aperta è `M<n> · Rilascio <versione>`; se ce n'è un'altra, fermati e mostrala.
- PR aperte che chiudono issue della milestone: `gh pr list --state open`.
- La versione nuova: l'ultimo tag (`git tag --sort=-v:refname | head -1`) con la regola di `docs/agents/milestone.md`; di solito MINOR +1 e PATCH a 0 per una milestone, PATCH +1 per un rilascio di correzioni.

Fatto quando: resta aperta al più l'issue del rilascio, nessuna PR aperta della milestone, e la versione nuova è detta all'utente.

## 2. Commit della versione

Su un branch `claude/versione-<x.y.z>` da `origin/main`:

1. la versione nel progetto (in Unity `bundleVersion` di `ProjectSettings/ProjectSettings.asset`, l'unico cambio di `ProjectSettings` che non si chiede; altrove il `package.json` o il file che il progetto indica);
2. la nota del rilascio, dove la tiene il progetto (per esempio `docs/rilasci/<x.y.z>.md`): cosa cambia per chi gioca o usa il prodotto, in parole sue, senza numeri di issue;
3. un commit «Versione X.Y.Z (M<n>)» e la PR, che chiude l'issue del rilascio.

Fatto quando: l'utente ha fatto il merge e il commit della versione è su `origin/main`.

## 3. Build

Da `main` aggiornato, in un worktree nuovo e pulito, coi comandi di `docs/agents/rilasci.md`. In Unity la build passa da `tools/pesante.sh` e gira in background; finita la build, ripristina con `git checkout` i file che lo strumento lascia modificati.

Fatto quando: la build c'è e il suo log finisce senza errori.

## 4. Prova

La prova che dice `docs/agents/rilasci.md`: per una build web, servita in locale e aperta nel browser integrato, con `read_console_messages` (`onlyErrors`) vuoto; per desktop o mobile, avviata e giocata nei punti che il documento elenca. Se il prodotto ha più lingue, in ognuna.

Se qualcosa non va, apri un'issue nella milestone con la skill `nuova-issue`, che blocca il rilascio, e fermati: non si carica e la milestone resta aperta. Se una parte non si riesce a provare da qui, chiedi all'utente se la prova lui o la si salta, e scrivilo nella nota del rilascio.

Fatto quando: ogni punto è provato, o saltato con la decisione dell'utente scritta.

## 5. Caricamento e tag

Chiedi l'ok all'utente: caricare cambia quello che vede chi gioca. Poi carica coi comandi di `docs/agents/rilasci.md` (per itch.io, `butler push ... --userversion X.Y.Z` e il controllo con `butler status`); se il caricamento vuole l'account dell'utente, lo lancia lui e tu gli dai il comando. Poi:

```bash
git tag vX.Y.Z <commit della versione>
git push origin vX.Y.Z
```

Fatto quando: il servizio mostra la versione nuova e il tag è su `origin`.

## 6. Devlog (facoltativo)

Se il progetto pubblica un devlog (`docs/agents/rilasci.md` lo dice), scrivine la bozza dalla nota del rilascio e mostrala all'utente: lo pubblica lui, o tu dopo il suo ok.

## 7. Chiudere la milestone

```bash
gh api 'repos/<owner>/<repo>/milestones?state=open' --jq '.[] | [.number, .title] | @tsv'
gh api -X PATCH repos/<owner>/<repo>/milestones/<numero> -f state=closed
```

In `docs/agents/milestone.md` togli la sua riga e toglila dal «Dipende da» delle altre, in una PR (anche quella del passo 2, se la milestone non rilascia).

Fatto quando: `gh api repos/<owner>/<repo>/milestones/<numero> --jq .state` dà `closed` e il resoconto all'utente dice versione, stato della milestone, cosa è stato provato e cosa no.
