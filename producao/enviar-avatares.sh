#!/usr/bin/env bash
set -euo pipefail
export DISPLAY=:99
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:/usr/local/bin:/usr/bin:/bin"
ROOT=/home/nmaldaner/projetos/output/solar-noaa-serie
EV=/home/nmaldaner/projetos/explicavideos
cd "$EV"
for slug in solar-equipamentos solar-noaa-painel solar-historia-protecao; do
  cfg="$ROOT/$slug/v1.json"
  printf '%s Envio: %s\n' "$(date -Is)" "$slug"
  EXPLICAVIDEOS_CONFIG="$cfg" timeout 14400 python3 engine/submit.py > "$ROOT/$slug/envio.log" 2>&1
done
printf '%s Todos os avatares submetidos.\n' "$(date -Is)"
