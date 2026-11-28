---
name: pubblicazione-itch-io
description: Pubblica un gioco su itch.io quando l'utente lo chiede — caricamento della build con butler, prova dalla pagina, tag e release GitHub, devlog e descrizione della pagina dalla dashboard in Claude in Chrome. Usala ogni volta che carichi o aggiorni un gioco su itch.io: una build nuova, un devlog, la descrizione della pagina.
---

# Pubblicazione su itch.io

La pubblicazione parte quando l'utente la chiede, di solito dal passo 5 della skill `chiusura-milestone`: cambia quello che vede chi gioca. Da lì la fa l'agente, dal caricamento al devlog.

Richiesta: $ARGUMENTS

## I dati del progetto

Li dà il progetto, in `docs/agents/rilasci.md` o nel suo README di itch.io:

- l'utente itch.io e il gioco, cioè il progetto butler `<utente>/<gioco>`, e il canale (per una build web di solito `html5`);
- lo script di caricamento, se il progetto ne ha uno, e la cartella della build;
- l'URL della pagina (`https://<utente>.itch.io/<gioco>`) e l'id del gioco nella dashboard;
- dove stanno la nota del rilascio, la nota del devlog e il testo della descrizione.

Prendi i valori da lì, così come sono scritti. Un dato che manca lo chiedi all'utente, e proponi di aggiungerlo al documento del progetto.

## Chi fa cosa

- **L'agente**: caricamento, `butler status`, prova dalla pagina, tag e release GitHub, devlog, descrizione.
- **L'utente**: quello che chiede il suo giudizio, il suo account o il suo dispositivo. Il via alla pubblicazione; `butler login`, una volta sola per Mac (butler poi tiene le credenziali sul Mac, e se le richiede il login resta a lui); la prova dal suo telefono e quella dei suoi progressi.

## I due browser

- **La dashboard** di itch.io (devlog, *Edit game*) si usa da **Claude in Chrome**, strumenti `mcp__claude-in-chrome__*`: è il Chrome dell'utente, dove è già collegato a itch.io. Il browser dell'app (`mcp__Claude_Browser__*`) per la dashboard non serve: lì itch.io mostra la verifica di Cloudflare e chiede un accesso che l'utente da lì non può fare. Se Claude in Chrome non risponde, fermati e chiedi all'utente di collegarlo.
- **La pagina pubblica** del gioco si prova dall'uno o dall'altro.

## 1. Caricamento

Dal worktree pulito della build (`chiusura-milestone`, passi 3 e 4), con lo script del progetto: prima la sua prova a vuoto, se ce l'ha (`--dry-run`), poi il caricamento vero. Senza script:

```bash
butler push <cartella della build> <utente>/<gioco>:<canale> --userversion X.Y.Z
```

Poi `butler status <utente>/<gioco>:<canale>`: quando mostra `X.Y.Z`, itch.io ha finito di elaborare la build. Se butler chiede l'accesso, dai all'utente `butler login`, aspetta che ti dica che è fatto e riparti dal caricamento.

Fatto quando: `butler status` mostra `X.Y.Z` sul canale.

## 2. Prova dalla pagina

Apri la pagina del gioco, avvia il gioco e controlla che sia la versione nuova e che quello che il rilascio cambia funzioni, con `read_console_messages` (`onlyErrors`) vuoto. Poi chiedi all'utente la prova dal suo telefono e quella dei suoi progressi, e aspetta la sua risposta.

Se la prova trova un difetto, il tag resta fuori da GitHub: toglilo in locale se c'è (`git tag -d vX.Y.Z`), apri il difetto come issue della milestone con la skill `nuova-issue` e riparti dalla PR della correzione.

Fatto quando: la tua prova è passata e l'utente ha risposto sulle sue.

## 3. Tag e release GitHub

Con la build che si gioca dalla pagina, il tag `vX.Y.Z` sul commit della versione va su GitHub, e dal tag la release con la nota del rilascio:

```bash
git tag vX.Y.Z <commit della versione>   # se non c'è già in locale
git push origin vX.Y.Z
gh release create vX.Y.Z --title "<Gioco> X.Y.Z" --notes-file <nota del rilascio>
```

Fatto quando: `gh release view vX.Y.Z` mostra la release.

## 4. Devlog

Se il progetto pubblica un devlog, da Claude in Chrome apri «Write new post»: `https://itch.io/dashboard/game/<id>/new-devlog`.

- *Title*: il titolo della nota del devlog, senza il `#`;
- il testo: il resto della nota, senza i commenti `<!-- -->`;
- *Type*: *Major Update or Launch* per una milestone, *General Update* per un correttivo;
- l'allegato: la build della versione, che itch.io propone già fra i file del gioco;
- *Published*, poi *Save*.

Fatto quando: il post, col suo titolo, compare nella pagina *Devlog* del gioco.

## 5. Descrizione

Solo se il rilascio ha cambiato il testo della descrizione del progetto: da Claude in Chrome, *Edit game* (`https://itch.io/game/edit/<id>`), il campo *Description* col testo del progetto, poi *Save*.

Fatto quando: la pagina del gioco mostra il testo nuovo.

## 6. Resoconto

Di' all'utente cosa è pubblicato, con i link (pagina, release, devlog), e cosa ha provato chi: tu dalla pagina, lui dal telefono e coi suoi progressi. Poi si torna a `chiusura-milestone` per chiudere issue del rilascio e milestone.

Fatto quando: l'utente ha i tre link e sa cosa è stato provato e cosa no.
