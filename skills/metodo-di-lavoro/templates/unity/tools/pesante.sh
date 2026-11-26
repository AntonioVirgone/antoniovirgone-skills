#!/bin/bash
# L'unica strada per lanciare un processo pesante: Unity in batchmode (test, compilazione, build).
# Il Mac è uno solo e lo usano più sessioni e più progetti (anche age-of-dinos, da cui viene questo
# script), quindi i posti sono contati per tutto il Mac, non per sessione: al massimo PESANTI_MAX processi
# pesanti insieme (6), contando anche quelli lanciati fuori da qui, compresi i player e il Blender headless
# di age-of-dinos. Un processo aspetta il suo posto, e se il carico è già alto aspetta che scenda. Gira con
# nice -n 10 e viene ucciso dopo PESANTE_TIMEOUT secondi (2 ore).
#
# Uso:  tools/pesante.sh <comando> [argomenti...]
# Tanti in parallelo: xargs -P 6 ... tools/pesante.sh ... (anche con -P più alto il tetto resta 6).
# L'hook tools/hooks/blocca_pesanti.py rifiuta i lanci che non passano di qui.

set -u

MAX=${PESANTI_MAX:-6}
(( MAX > 6 )) && MAX=6
TIMEOUT=${PESANTE_TIMEOUT:-7200}
WAIT_LIMIT=${PESANTE_ATTESA:-3600}
CPUS=$(sysctl -n hw.ncpu 2>/dev/null || echo 8)
LOAD_LIMIT=$(( CPUS * 2 ))
# Lo stesso lucchetto del pesante.sh di age-of-dinos: due lanci insieme, uno per progetto, non prendono
# lo stesso posto.
DIR=${TMPDIR:-/tmp}/age-of-dinos-pesanti
LOCK=$DIR/lock

if (( $# == 0 )); then
  echo "uso: tools/pesante.sh <comando> [argomenti...]" >&2
  exit 64
fi
mkdir -p "$DIR"

# I processi pesanti che girano ora, di tutte le sessioni: Unity in batchmode (non l'Editor
# dell'utente né i suoi AssetImportWorker), i player di age-of-dinos e Blender headless.
# Si guarda l'eseguibile (comm, in ultima colonna perché non sia troncato), non gli argomenti: una shell
# o questo script, che hanno Unity negli argomenti, non contano.
running() {
  local n=0 pid comm args
  while read -r pid comm; do
    case $comm in
      */MacOS/Unity)
        args=$(/bin/ps -o args= -p "$pid" 2>/dev/null)
        [[ $args == *" -batchmode"* && $args != *AssetImportWorker* ]] && n=$((n + 1)) ;;
      *.app/Contents/MacOS/age-of-dinos)
        n=$((n + 1)) ;;
      */MacOS/Blender|*/blender)
        # Solo headless: il Blender aperto dall'utente non conta.
        args=$(/bin/ps -o args= -p "$pid" 2>/dev/null)
        [[ " $args " == *" -b "* || " $args " == *" --background "* ]] && n=$((n + 1)) ;;
    esac
  done < <(/bin/ps -Axo pid=,comm=)
  echo $n
}

load() {
  sysctl -n vm.loadavg | awk '{ printf "%d", $2 }'
}

# Il lucchetto: un mkdir, atomico. Uno lasciato da un processo morto si toglie.
lock() {
  until mkdir "$LOCK" 2>/dev/null; do
    if [[ -f $LOCK/pid ]] && ! kill -0 "$(cat "$LOCK/pid" 2>/dev/null)" 2>/dev/null; then
      rm -rf "$LOCK"
      continue
    fi
    sleep 0.5
  done
  echo $$ > "$LOCK/pid"
}
unlock() { rm -rf "$LOCK"; }

started=$(date +%s)
said=0
while :; do
  lock
  count=$(running)
  current=$(load)
  if (( count < MAX && current < LOAD_LIMIT )); then
    break
  fi
  unlock
  now=$(date +%s)
  if (( now - started > WAIT_LIMIT )); then
    echo "[pesante] rinuncio dopo ${WAIT_LIMIT} s di attesa: $count processi pesanti, carico $current" >&2
    exit 75
  fi
  if (( now - said >= 30 )); then
    echo "[pesante] aspetto: $count processi pesanti su $MAX, carico $current (limite $LOAD_LIMIT)" >&2
    said=$now
  fi
  sleep 2
done

nice -n 10 "$@" &
child=$!
# Il lucchetto resta finché il processo nuovo non si vede tra quelli pesanti (o 10 s), così due
# lanci insieme non prendono lo stesso posto.
for _ in $(seq 1 20); do
  (( $(running) > count )) && break
  kill -0 $child 2>/dev/null || break
  sleep 0.5
done
unlock

# Il watchdog del timeout. Non eredita stdin, stdout e stderr: un suo processo ancora vivo terrebbe
# aperta la pipe di chi legge l'output, e `tools/pesante.sh ... | tail` resterebbe appeso fino al timeout.
( sleep "$TIMEOUT"; kill -TERM $child 2>/dev/null; sleep 10; kill -KILL $child 2>/dev/null ) \
  </dev/null >/dev/null 2>&1 &
watchdog=$!
# Ferma il watchdog e anche il suo sleep: un kill al solo subshell lascia lo sleep orfano (ppid 1)
# per tutta la durata del timeout.
stop_watchdog() {
  local sleeps
  sleeps=$(pgrep -P $watchdog 2>/dev/null)
  kill $watchdog 2>/dev/null
  [[ -n $sleeps ]] && kill $sleeps 2>/dev/null
}
trap 'kill -TERM $child 2>/dev/null; stop_watchdog' INT TERM
wait $child
status=$?
stop_watchdog
exit $status
