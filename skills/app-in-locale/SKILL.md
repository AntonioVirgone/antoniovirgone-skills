---
name: app-in-locale
description: Installa e avvia l'app Expo di un monorepo API + web + mobile in locale — simulatore iOS, emulatore Android, iPhone o telefono Android collegato — con la build giusta, Metro, e l'app che raggiunge l'API locale. Usala quando bisogna vedere o provare l'app su un dispositivo.
---

# L'app in locale

Mette l'app mobile su un dispositivo di questa macchina e la fa parlare con Metro e con l'API. Quale ramo seguire dipende dal dispositivo: chiedilo solo se non si capisce dalla richiesta.

Leggi [le regole comuni](../servizi-esterni.md) per i login e i valori.

Richiesta dell'utente: $ARGUMENTS

## Passi

### 1. Preparazione

- `npm install` alla radice e i pacchetti del workspace compilati (`npx turbo run build --filter=@<progetto>/mobile^...`): senza, Metro non risolve `@<progetto>/…`.
- Il `.env` dell'app mobile, dal suo `.env.example` se manca. `EXPO_PUBLIC_API_URL` punta all'API che vuoi usare: quella locale (vedi [L'API locale](#lapi-locale)) o quella di produzione.
- Se serve l'API locale: database avviato (Docker o Postgres locale), `.env` dell'API, `npx prisma generate`, API in esecuzione in background.

Fatto quando: `npx tsc --noEmit` nell'app passa e l'API scelta risponde all'endpoint di salute.

### 2. La build

L'app usa moduli nativi (login Apple e Google, notifiche, aptica…), quindi serve una **development build**, non Expo Go: Expo Go ha un bundle ID suo, Firebase rifiuta i suoi token, e i moduli che non contiene si rompono.

- Se c'è già una build di debug e i moduli nativi non sono cambiati da allora (stesse dipendenze `expo-*` e native in `package.json`, stessi config plugin), si **reinstalla quella**: su iOS si trova in `~/Library/Developer/Xcode/DerivedData/<Nome>-*/Build/Products/Debug-iphonesimulator/<Nome>.app`.
- Altrimenti si costruisce: `npx expo run:ios --device <udid>` o `npx expo run:android --device <nome>`. La prima volta fa il prebuild e dura minuti: lanciala in background.

Fatto quando: la build è installata sul dispositivo.

### 3. Il dispositivo

**Simulatore iOS**

- Con più simulatori accesi usa l'UDID (`xcrun simctl list devices booted`), mai `booted`.
- Con il ciclo di vita a scene non adottato (vedi `app-di-test`), sui runtime iOS 27 la build si chiude all'avvio: usa un simulatore con il runtime precedente.
- Installazione e avvio: `xcrun simctl install <udid> <app>`, `xcrun simctl launch <udid> <bundle>`. Foto dello schermo: `xcrun simctl io <udid> screenshot <file>.png`.

**Emulatore Android**

- `adb` e `emulator` stanno in `~/Library/Android/sdk/platform-tools/` e `~/Library/Android/sdk/emulator/`, spesso fuori dal `PATH`. Gli AVD: `emulator -list-avds`; avvio: `emulator -avd <nome>` in background, poi `adb wait-for-device`.
- `adb reverse tcp:8081 tcp:8081` per Metro, e lo stesso per la porta dell'API locale.
- `adb install -r <apk>`, `adb shell monkey -p <pacchetto> 1` per aprirla, `adb exec-out screencap -p > <file>.png` per la foto.

**iPhone collegato**

- Con un account Apple gratuito o del team: `npx expo run:ios --device` firma con il team scelto in Xcode. La prima volta l'utente deve fidarsi del certificato sviluppatore sul telefono (Impostazioni → Generali → VPN e gestione dispositivi) e attivare la Modalità sviluppatore.
- Senza Xcode sul telefono: una build `preview` di EAS, dopo aver registrato il dispositivo con `eas device:create` (vedi `app-di-test`).

**Telefono Android collegato**

- Debug USB attivo, il telefono che compare in `adb devices`. Poi come l'emulatore: `adb reverse` e `npx expo run:android --device`, oppure l'APK di una build `preview`.

Fatto quando: l'app è aperta sul dispositivo.

### 4. Metro

- Da dentro l'app mobile: `npx expo start --port 8081`, in background, **senza** `CI=1`: con `CI=1` Metro non guarda i file, e un file nuovo non lo trova.
- Aspetta che `curl -s localhost:8081/status` risponda `packager-status:running` prima di aprire l'app: aperta prima, resta sulla schermata iniziale o sull'errore di connessione.
- Se la 8081 è occupata da un'altra sessione: su Android Metro va su un'altra porta, `adb reverse tcp:8081 tcp:<porta>` e l'host di debug impostato a `localhost:8081` nelle preferenze dell'app (`run-as <pacchetto>`, `shared_prefs/<pacchetto>_preferences.xml`, `debug_http_host`); senza, l'app va su `10.0.2.2:8081`, cioè sul Metro dell'altra sessione. Su iOS cambiare porta non funziona: serve la 8081 libera.
- I `console.warn` dell'app non sempre arrivano nel log di Metro: per leggere un valore, mostralo a schermo.

Fatto quando: l'app carica il bundle da Metro (si vede nel log) e una modifica a un file arriva con Fast Refresh.

### 5. Resoconto

Dispositivo, build usata (riusata o nuova), porta di Metro, API a cui punta l'app, una foto dello schermo. Le trappole nuove vanno nella memoria del progetto.

## L'API locale

`localhost` sul dispositivo è il dispositivo stesso:

- **simulatore iOS**: `localhost` arriva al Mac, va bene;
- **emulatore Android**: `adb reverse tcp:<porta-api> tcp:<porta-api>` e `localhost`, oppure `10.0.2.2`;
- **telefono vero**: l'IP del Mac sulla rete locale (`ipconfig getifaddr en0`), con l'API in ascolto su `0.0.0.0`; con un telefono Android via USB basta `adb reverse`.

Le `EXPO_PUBLIC_…` si leggono all'avvio di Metro: dopo averle cambiate, riavvialo con `--clear`.
