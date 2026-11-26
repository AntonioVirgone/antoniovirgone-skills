#!/bin/bash
# Compila il progetto e fa girare i test EditMode con Unity in batchmode, sul checkout o sul worktree in cui
# sta questo script, senza l'Editor. L'Editor può restare aperto su un altro checkout: Unity rifiuta
# solo un secondo processo sullo stesso progetto. Passa da tools/pesante.sh.
#
# Uso:  tools/unity-check.sh [--compile-only] [--filter <espressione>] [--category <categoria>]
#   --compile-only  solo compilazione (ogni assembly del progetto), niente test
#   --filter        il -testFilter di Unity: nomi di test, classi o namespace separati da |, o una regex
#   --category      il -testCategory di Unity
#
# Log e risultati in Logs/unity-check/ (fuori da git). Esce con 0 se compila e i test passano, 1 se ci sono
# errori di compilazione, 2 se un test fallisce, 3 per ogni altro problema (Editor aperto qui, Unity che
# non parte o non finisce).

set -u

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
MAIN=$(git -C "$ROOT" worktree list --porcelain | sed -n '1s/^worktree //p')
VERSION=$(sed -n 's/^m_EditorVersion: //p' "$ROOT/ProjectSettings/ProjectVersion.txt")
UNITY="/Applications/Unity/Hub/Editor/$VERSION/Unity.app/Contents/MacOS/Unity"
OUT="$ROOT/Logs/unity-check"
LOG="$OUT/unity.log"
XML="$OUT/test-results.xml"

compile_only=0
filter=""
category=""
while (( $# > 0 )); do
  case $1 in
    --compile-only) compile_only=1 ;;
    --filter) filter=${2:?--filter vuole un valore}; shift ;;
    --category) category=${2:?--category vuole un valore}; shift ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) echo "[unity-check] argomento sconosciuto: $1" >&2; exit 64 ;;
  esac
  shift
done

if [[ ! -x $UNITY ]]; then
  echo "[unity-check] manca Unity $VERSION in $UNITY" >&2
  exit 3
fi

# Un Editor aperto su questo stesso progetto tiene il lucchetto di Temp/: in batchmode Unity uscirebbe
# subito. L'Editor aperto su un altro checkout non conta: lo spazio dopo il percorso tiene fuori i worktree,
# il cui percorso comincia con quello del checkout principale.
if /bin/ps -Axo args= | grep -F "MacOS/Unity" | grep -v -- -batchmode | grep -v AssetImportWorker \
    | sed 's/$/ /' | grep -i -q -F -- "-projectPath $ROOT "; then
  echo "[unity-check] l'Editor è aperto su $ROOT: ricompila e lancia i test da lì via MCP," \
       "oppure chiudilo (metodo-di-lavoro, UNITY.md, «Worktree e Editor»)" >&2
  exit 3
fi

# Un worktree nuovo non ha la Library: la si clona dal checkout principale (copia APFS, pochi secondi e
# niente spazio in più), così Unity reimporta solo quello che cambia invece di importare tutto.
if [[ ! -d $ROOT/Library && -n $MAIN && $MAIN != "$ROOT" && -d $MAIN/Library ]]; then
  echo "[unity-check] clono la Library da $MAIN" >&2
  cp -cR "$MAIN/Library" "$ROOT/Library" || { echo "[unity-check] clonazione della Library fallita" >&2; exit 3; }
fi

mkdir -p "$OUT"
rm -f "$LOG" "$XML"

args=(-batchmode -nographics -projectPath "$ROOT" -logFile "$LOG")
if (( compile_only )); then
  args=("${args[@]}" -quit)
else
  args=("${args[@]}" -runTests -testPlatform EditMode -testResults "$XML")
  [[ -n $filter ]] && args=("${args[@]}" -testFilter "$filter")
  [[ -n $category ]] && args=("${args[@]}" -testCategory "$category")
fi

echo "[unity-check] Unity $VERSION in batchmode su $ROOT (log: $LOG)" >&2
started=$(date +%s)
"$ROOT/tools/pesante.sh" "$UNITY" "${args[@]}"
status=$?
echo "[unity-check] Unity è uscito con $status dopo $(( $(date +%s) - started )) s" >&2

errors=$(grep -E "error CS[0-9]+" "$LOG" 2>/dev/null | sed -E 's/^[[:space:]]+//' | sort -u)
if [[ -n $errors ]]; then
  echo "[unity-check] errori di compilazione:"
  echo "$errors" | head -30
  exit 1
fi

if (( compile_only )); then
  if (( status == 0 )); then
    echo "[unity-check] compila senza errori"
    exit 0
  fi
  echo "[unity-check] Unity non ha finito bene: guarda $LOG" >&2
  exit 3
fi

if [[ ! -f $XML ]]; then
  echo "[unity-check] nessun risultato dei test: guarda $LOG" >&2
  exit 3
fi

python3 -I - "$XML" <<'PY'
import sys
import xml.etree.ElementTree as ET

run = ET.parse(sys.argv[1]).getroot()
print(f"[unity-check] test: {run.get('total')} in tutto, {run.get('passed')} passati, "
      f"{run.get('failed')} falliti, {run.get('skipped')} saltati ({run.get('result')})")
for case in run.iter("test-case"):
    if case.get("result") == "Failed":
        message = (case.findtext("failure/message") or "").strip().splitlines()
        print(f"  - {case.get('fullname')}: {message[0] if message else ''}")
PY

case $status in
  0) exit 0 ;;
  2) exit 2 ;;
  *) echo "[unity-check] Unity non ha finito bene: guarda $LOG" >&2; exit 3 ;;
esac
