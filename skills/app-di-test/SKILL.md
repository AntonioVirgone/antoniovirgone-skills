---
name: app-di-test
description: Prepara l'app Expo di un monorepo API + web + mobile per i test sugli store — progetto EAS, variabili delle build, credenziali delle push (FCM V1 e APNs), build su TestFlight e sul test interno di Google Play, build interne da installare a mano, impronte di release in Firebase.
disable-model-invocation: true
---

# App di test su Apple e Google

Porta l'app sui telefoni dei tester senza una scheda pubblica: TestFlight con i tester interni (Apple non fa la revisione) e il track «Test interno» di Play. Le build le fa EAS nel cloud.

Prima di cominciare leggi [le regole comuni](../servizi-esterni.md). Servono l'indirizzo dell'API di produzione (da `deploy-online`) e il progetto Firebase (da `firebase-progetto`); se mancano, dillo e chiedi se procedere con la sola parte che non ne dipende.

Richiesta dell'utente: $ARGUMENTS

La CLI è `npx -y eas-cli@latest` (qui sotto `eas`), lanciata dalla cartella dell'app mobile. `eas whoami` dice se c'è il login.

## Passi

### 1. Stato di partenza

Controlla nell'app mobile e riporta all'utente una riga per voce:

- **progetto EAS**: `extra.eas.projectId` in `app.json`. Se manca, con conferma, `eas init --non-interactive --force`;
- **identità**: bundle ID iOS e pacchetto Android, nome, icona e splash veri (senza icona non si va sugli store), `version` almeno `0.1.0` (App Store Connect rifiuta `0.0.0`);
- **`eas.json`**: `cli.appVersionSource: "remote"`; profilo `preview` con `distribution: internal` e APK su Android; profilo `production` con `autoIncrement: true`; `submit.production.android` con `track: internal` e `releaseStatus: draft`; ogni profilo con il suo `environment`;
- **pacchetti del workspace**: su EAS arriva il repo senza i `dist/` dei pacchetti condivisi, e senza i `.env`. Serve uno script `eas-build-post-install` nel `package.json` dell'app che li compila (`cd ../.. && npx turbo run build --filter=@<progetto>/mobile^...`);
- **SDK e iOS**: con l'SDK di iOS 27 un'app che non adotta il ciclo di vita a scene si ferma all'avvio. Se il template nativo della versione di Expo in uso crea ancora la finestra nell'AppDelegate, serve un config plugin che colleghi lo scene delegate (o il passaggio a un SDK che lo fa da sé): chiedi all'utente quale strada, è una decisione da ADR;
- **push**: se l'app usa `expo-notifications`, `app.config.ts` legge `google-services.json` da `GOOGLE_SERVICES_JSON`.

Le correzioni ai file vanno su un branch e in una PR, prima delle build.

Fatto quando: ogni voce è a posto o ha una PR aperta, e l'utente l'ha vista.

### 2. Variabili delle build

Il `.env` non arriva su EAS. Per ogni `EXPO_PUBLIC_…` del `.env.example` dell'app:

```bash
eas env:set --name <NOME> --value <valore> --visibility plaintext \
  --environment preview --environment production --scope project --non-interactive
```

`EXPO_PUBLIC_API_URL` è l'indirizzo dell'API di produzione; gli altri valori vengono dal `.env` locale. Una variabile vuota la salti e la elenchi nel resoconto. Con le push, anche `google-services.json` come variabile di tipo file:

```bash
eas env:set --name GOOGLE_SERVICES_JSON --type file --value ~/.config/<progetto>/google-services.json \
  --visibility sensitive --environment development --environment preview --environment production \
  --scope project --non-interactive
```

Fatto quando: `eas env:list --environment production` mostra tutte le variabili attese.

### 3. Il wizard

Scrivi `scripts/configura-store.sh` con la skill `wizard`. Gli stadi, nell'ordine, saltando quelli che non servono:

1. **google-services.json** — Firebase → l'app Android → scarica il file. Il wizard controlla che `package_name` e `project_id` siano quelli giusti e lo copia in `~/.config/<progetto>/`.
2. **API FCM** — console.cloud.google.com, «Firebase Cloud Messaging API» del progetto: abilitata.
3. **Chiave FCM V1 su EAS** — `eas credentials -p android` → Google Service Account → la chiave per le push FCM V1, con il JSON dell'account di servizio di `firebase-progetto`.
4. **Chiave APNs su EAS** — `eas credentials -p ios` → Push Notifications. Vedi [APNs](#apns).
5. **iOS su TestFlight** — `eas build -p ios --profile production --auto-submit`: chiede l'accesso Apple, crea certificati, profili e, al primo invio, l'app su App Store Connect. Poi TestFlight → tester interni → installazione dal telefono.
6. **Play Console** — crea l'app (nome, gioco o app, gratuita), poi `eas build -p android --profile production` e il **primo AAB caricato a mano**: Test → Test interno → nuova release, accetta la firma di Google Play, carica, pubblica. Scheda Tester: un elenco con le email e il link di adesione da aprire sul telefono.
7. **Impronte di release** — SHA-1 e SHA-256 del keystore di caricamento (`eas credentials -p android`) e del certificato di firma di Play (Play Console → Integrità dell'app → Firma dell'app). Il wizard le chiede e le registra lui con `npx -y firebase-tools@latest apps:android:sha:create`.
8. **La prova** — sui telefoni dei tester: installazione, login, una push vera.

Fatto quando: `bash -n` e `shellcheck` (se c'è) passano, e l'utente l'ha lanciato.

### 4. Dopo il primo giro

- Dal secondo AAB basta `eas submit -p android --latest`, dopo aver dato a EAS un account di servizio con accesso alla Play Console (`eas credentials`); va in bozza sul track interno.
- Per installare senza store: profilo `preview`. Android installa l'APK dal link della build; iOS installa solo sui dispositivi registrati con `eas device:create` **prima** della build.
- A ogni rilascio sugli store si alza `version`; il numero di build lo alza EAS.

Segui la chiusura delle regole comuni; nel resoconto anche lo stato delle push per piattaforma.

Fatto quando: l'app è installata su almeno un telefono per piattaforma, oppure il resoconto dice dove si è fermata e perché.

## APNs

- Una chiave APNs vale per **tutte le app del team**, e Apple ne concede solo due per team. Se EAS propone di riusare una chiave che esiste già (di un'altra app dello stesso team), si risponde sì.
- Revocare una chiave ferma le push di tutte le app che la usano: non si revoca per «rifare pulito».
- La chiave APNs non è il `.p8` di Sign in with Apple, anche se sono dello stesso team.
- Se Expo accetta la push ma la ricevuta dice `InvalidCredentials` o APNs risponde `InvalidProviderToken` (403), la chiave caricata su EAS non vale: Key ID, Team ID o chiave revocata. Le ricevute si leggono con `POST https://exp.host/--/api/v2/push/getReceipts` e gli ID dei biglietti salvati dall'API.
- Le push su iOS non arrivano al simulatore: si provano su un telefono, con una build che contiene `expo-notifications`.

## Trappole

- **Google non accetta il primo caricamento via API** per un'app che non ne ha mai ricevuto uno: il primo AAB è sempre a mano.
- Il pacchetto Android si fissa al primo caricamento su Play, il bundle ID alla registrazione su Apple: controllali prima.
- Il login con Google sull'app di Play fallisce finché in Firebase non ci sono le impronte della firma di Play: quella che arriva da Play non è firmata dalla chiave di EAS.
