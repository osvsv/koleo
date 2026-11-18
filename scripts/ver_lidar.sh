#!/usr/bin/env bash
# Muestra lo que detecta el código (localizar_tarima / localizar_poste) con el RPLIDAR de la Pi, por SSH (alias koleo-pi).
# Uso: bash scripts/ver_lidar.sh          # EN VIVO: ventana que se actualiza cada vuelta (cierra la ventana o Ctrl+C)
#      bash scripts/ver_lidar.sh 5        # captura 5 vueltas y dibuja la primera y la última en una imagen
# Requiere: hotspot activo, Pi encendida, `ssh koleo-pi` funcionando y matplotlib en el Python de la laptop.
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
PY="${KOLEO_PYTHON:-C:/Users/osval/AppData/Local/Programs/Python/Python313/python.exe}"
SALIDA="${TMPDIR:-${TEMP:-/tmp}}/koleo_lidar"
mkdir -p "$SALIDA"

ssh koleo-pi 'mkdir -p /tmp/koleo_cap'
scp -q "$RAIZ"/scripts/lidar_captura_pi.py "$RAIZ"/scripts/lidar_stream_pi.py koleo-pi:/tmp/koleo_cap/

if [ $# -eq 0 ]; then
  ssh koleo-pi 'cd /tmp/koleo_cap && exec ~/koleo_env/bin/python -u lidar_stream_pi.py' | "$PY" -u "$RAIZ/scripts/lidar_vivo.py"
else
  ssh koleo-pi "cd /tmp/koleo_cap && ~/koleo_env/bin/python lidar_captura_pi.py $1"
  scp -q koleo-pi:/tmp/koleo_cap/vueltas.json "$SALIDA/"
  "$PY" "$RAIZ/scripts/lidar_ver.py" "$SALIDA/vueltas.json" "$SALIDA/escaneo.png"
  echo "Imagen: $SALIDA/escaneo.png"
  start "" "$SALIDA/escaneo.png" 2>/dev/null || true
fi
