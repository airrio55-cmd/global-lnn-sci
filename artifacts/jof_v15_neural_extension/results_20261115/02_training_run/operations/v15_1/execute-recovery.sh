#!/usr/bin/env bash
set -euo pipefail
here=$(cd -- "$(dirname -- "$0")" && pwd)
run=${1:-$(cat "$HOME/v15-runs/latest_recovery.txt")}
repo="$HOME/global-lnn-sci"
[[ -f "$run/preparation_complete.json" && ! -f "$run/process.json" ]] || { echo 'STOP: readiness missing or attempt already launched'; exit 1; }
sudo -v
sudo service docker start
sudo docker image inspect global-lnn-sci-v15-runtime:locked-d866841 | python3 "$here/../verify-runtime-image.py"
[[ -z $(sudo docker ps -q --filter 'label=org.global-lnn-sci.v15=true') ]] || { echo 'STOP: active V15 container exists'; exit 1; }
python3 - "$run" <<'PY'
import pathlib,json,sys,os
run=pathlib.Path(sys.argv[1]);r=json.loads((run/'preparation_complete.json').read_text());assert r['status']=='READY_FOR_SEPARATE_RECOVERY_EXECUTION'
mem={line.split(':')[0]:int(line.split()[1])*1024 for line in pathlib.Path('/proc/meminfo').read_text().splitlines() if line.split(':')[0] in ['MemAvailable','SwapTotal']};assert mem['MemAvailable']>=10*1024**3 and mem['SwapTotal']>=3*1024**3,'Insufficient WSL RAM/swap'
assert os.statvfs(run).f_bavail*os.statvfs(run).f_frsize>=10*1024**3,'Insufficient disk space'
PY
# Separate minimized Windows WSL client keeps the distro active if the main terminal closes.
# It cannot prevent a Windows restart,power loss or company-policy shutdown.
keepalive_pid=$(powershell.exe -NoProfile -NonInteractive -Command '$p=Start-Process wsl.exe -ArgumentList "-d Ubuntu-24.04 --exec sleep infinity" -WindowStyle Minimized -PassThru; [Console]::Write($p.Id)' | tr -d '\r\n')
[[ "$keepalive_pid" =~ ^[0-9]+$ ]] || { echo 'STOP: independent WSL keepalive was not confirmed'; exit 1; }
printf '%s\n' "$keepalive_pid" > "$run/windows_wsl_keepalive_pid.txt"
container="v15-${run##*/}"
sudo docker run -d --name "$container" --label org.global-lnn-sci.v15=true \
 --restart=no --network none --read-only --cpus 2 --memory 12g --memory-swap 16g \
 --tmpfs /tmp:rw,nosuid,nodev,size=2g -e XDG_CACHE_HOME=/tmp/cache -e TORCH_HOME=/tmp/torch \
 --mount "type=bind,source=$repo,target=/repo,readonly" \
 --mount "type=bind,source=$run/authorization.json,target=/authorization/record.json,readonly" \
 --mount "type=bind,source=$run/operations/v15_1,target=/operations,readonly" \
 --mount "type=bind,source=$run,target=/runs" \
 --entrypoint /workspace/.venvs/global-lnn-sci/bin/python global-lnn-sci-v15-runtime:locked-d866841 -u /operations/controller.py --execute
printf '%s\n' "$container" > "$run/container_name.txt"
printf '%s\n' "$run" > "$HOME/v15-runs/latest_run.txt"
echo "RECOVERY_CONTAINER_CREATED: $container"
echo "RESULTS_DIRECTORY: $run"
echo 'Run status-v15.sh to confirm actual new epoch/loss;container creation alone is not training confirmation.'
