---
name: firebase-progetto
description: Crea e configura il progetto Firebase di un monorepo API + web + mobile — app web, iOS e Android, impronte SHA, provider di accesso (anonimo, email, Google, Apple), App ID e chiave di Sign in with Apple, client OAuth, account di servizio — e scrive i valori nei .env delle tre app.
disable-model-invocation: true
---

# Il progetto Firebase

Firebase Auth serve all'API (verifica dei token, cancellazione degli utenti), alla web app e all'app mobile, che usano Firebase JS. Questa skill crea il progetto con la CLI dove si può, guida l'utente nelle console di Firebase, Apple e Google Cloud per il resto, e lascia i valori nei `.env` e le chiavi in `~/.config/<progetto>/`.

Prima di cominciare leggi [le regole comuni](../servizi-esterni.md).

Richiesta dell'utente: $ARGUMENTS

La CLI è `npx -y firebase-tools@latest` (qui sotto `firebase`). Il login lo fa l'utente: `! npx -y firebase-tools@latest login`.

## Passi

### 1. Scelte

Leggi i valori dal repo e dai `.env.example` delle tre app (le variabili `FIREBASE_…`, `NEXT_PUBLIC_FIREBASE_…`, `EXPO_PUBLIC_FIREBASE_…`, `EXPO_PUBLIC_GOOGLE_…`, `APPLE_…`, `GOOGLE_APPLICATION_CREDENTIALS`). Poi presenta in un messaggio:

- l'**ID del progetto** (per esempio `<progetto>-dev`): non si cambia più, ed è quello che compare nei token;
- il **bundle ID**, lo stesso su iOS e Android: su Apple, una volta registrato, non si riusa più;
- i **provider**: anonimo (primo avvio senza account), email/password (operatori della web app), Google, Apple. Proponi quelli che il codice usa già;
- il Team ID di Apple, se c'è un'altra app dello stesso team da cui ricavarlo.

Se il progetto deve essere separato da quello di un'altra app dello stesso autore, dillo: chi cancella l'account in un'app non deve perderlo nell'altra.

Fatto quando: l'utente ha confermato ID, bundle ID e provider.

### 2. Con la CLI

Con `firebase login:list` che mostra un account:

1. `firebase projects:create <id> --display-name "<Nome>"`. Se fallisce perché l'account non ha mai accettato i termini, l'utente crea il progetto dalla console con lo stesso ID e tu riprendi da qui.
2. `firebase apps:create WEB "<Nome>" --project <id>`, poi `apps:create IOS "<Nome> iOS" --bundle-id <bundle>` e `apps:create ANDROID "<Nome> Android" --package-name <bundle>`.
3. `firebase apps:sdkconfig WEB <appId> --project <id>`: `apiKey` e `authDomain` vanno nel `.env` della web app (`NEXT_PUBLIC_…`) e in quello dell'app mobile (`EXPO_PUBLIC_…`); l'ID del progetto anche in quello dell'API. Sono valori pubblici: finiscono comunque nel bundle.
4. Le impronte di **debug** dell'app Android (vedi [Impronte](#impronte)): `firebase apps:android:sha:create <appIdAndroid> <sha> --project <id>`, per SHA-1 e SHA-256.

`GoogleService-Info.plist` e `google-services.json` non servono per l'accesso, perché l'app usa Firebase JS e non l'SDK nativo; `google-services.json` serve alle push Android, e lo prende `app-di-test`.

Fatto quando: `firebase apps:list --project <id>` mostra le tre app e i `.env` hanno i valori.

### 3. Il wizard

Scrivi `scripts/configura-firebase.sh` con la skill `wizard`, solo con gli stadi che restano all'utente. Ognuno scrive i valori nel `.env` giusto (`.env` dell'API per `APPLE_…` e `GOOGLE_APPLICATION_CREDENTIALS`, dell'app mobile per i client OAuth):

1. **Provider** — Authentication → Metodo di accesso: quelli scelti al passo 1. Google chiede nome pubblico ed email di assistenza; Apple basta attivarlo (Services ID e chiave servono solo al web e ad Android). Poi Impostazioni → Azioni utente: protezione contro l'enumerazione delle email.
2. **Apple, App ID** — developer.apple.com → Identifiers → App IDs, bundle ID esplicito, capability «Sign in with Apple» come primary App ID. Solo con il provider Apple.
3. **Apple, chiave per la revoca** — Keys → nuova chiave con Sign in with Apple → il `.p8` (si scarica una volta sola), Key ID e Team ID. Il wizard legge il `.p8` da un percorso fuori dal repo, controlla che contenga `BEGIN PRIVATE KEY` e lo scrive su una riga con `\n` al posto degli a capo. Serve alla cancellazione dell'account.
4. **Google Cloud, client OAuth** — Google Auth Platform → Branding (schermata di consenso, pubblico Esterno), poi Clients: si usano quelli «auto created by Google Service» che Firebase crea attivando Google, uno per app registrata; un secondo client Android con stesso pacchetto e stesso SHA-1 Google lo rifiuta. Copia gli ID dei client iOS e Android. Sul client Android, Impostazioni avanzate → abilita lo **schema URI personalizzato**, altrimenti il ritorno all'app dopo il login non arriva.
5. **Account di servizio** — Impostazioni progetto → Account di servizio → Genera nuova chiave privata. Il wizard accetta il JSON solo fuori dal repo e solo se `project_id` è quello del progetto; il percorso va in `GOOGLE_APPLICATION_CREDENTIALS`. Serve a cancellare utenti Firebase dall'API, e alle push Android (FCM V1).
6. **Controllo** — un utente email/password in Authentication → Users, poi l'accesso alla web app in locale.

Fatto quando: `bash -n` e `shellcheck` (se c'è) passano, e ogni variabile Firebase dei `.env.example` è scritta da te o da uno stadio.

### 4. Giro e chiusura

L'utente lancia il wizard. Dopo, controlla che i `.env` abbiano tutti i valori (senza stamparne i segreti) e che i percorsi delle chiavi esistano. Segui la chiusura delle regole comuni; nella memoria anche quali impronte sono registrate e quali mancano.

Fatto quando: l'utente entra nella web app in locale con l'utente di prova, oppure il resoconto dice quale stadio è rimasto e perché.

## Impronte

L'app Android ha bisogno di SHA-1 e SHA-256 di tre chiavi: **debug** (il keystore di questa macchina, `~/.android/debug.keystore`, alias `androiddebugkey`, password `android`), **caricamento** (il keystore con cui EAS firma le build) e **firma di Play** (il certificato con cui Google firma l'app distribuita). Le ultime due esistono solo dopo la prima build di EAS e il primo caricamento su Play: le aggiunge `app-di-test`.

- Il keystore di debug nasce alla prima build Android su questa macchina: se manca, registra le altre più tardi e dillo.
- `keytool` va lanciato con `-J-Duser.language=en`: in italiano alcune versioni del JDK si fermano con un errore prima delle impronte, e le etichette da cercare (`SHA1:`, `SHA256:`) sono quelle inglesi.
- Su macOS `/usr/bin/keytool` senza un Java installato chiede solo di installarlo: prova prima `$JAVA_HOME/bin/keytool`, poi quello di Android Studio (`/Applications/Android Studio.app/Contents/jbr/Contents/Home/bin/keytool`).
- Senza impronta giusta il login con Google su Android fallisce con `DEVELOPER_ERROR`.

## Trappole

- **Expo Go** ha un bundle ID suo: i token di Apple e Google intestati a lui Firebase li rifiuta. Il login si prova con una development build (vedi `app-in-locale`).
- Il `.p8` di Sign in with Apple e la chiave APNs delle push sono chiavi diverse dello stesso team: non vanno scambiate.
