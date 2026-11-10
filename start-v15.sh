#!/usr/bin/env bash
set -euo pipefail
here=$(cd -- "$(dirname -- "$0")" && pwd)
repo="$HOME/global-lnn-sci"
image='global-lnn-sci-v15-runtime:locked-d866841'
command -v python3 >/dev/null
[[ -d "$repo/.git" ]] || { echo 'STOP: frozen experiment repository missing'; exit 1; }
sudo -v
sudo service docker start
sudo docker image inspect "$image" | python3 "$here/verify-runtime-image.py"
[[ -z $(sudo docker ps -aq --filter 'label=org.global-lnn-sci.v15=true') ]] || { echo 'STOP: previous V15 container exists. No duplicate execution or automatic resume.'; exit 1; }
python3 - "$HOME" "$repo" <<'PY'
import pathlib,sys,json,subprocess,os
home=pathlib.Path(sys.argv[1]);repo=pathlib.Path(sys.argv[2])
if subprocess.check_output(['git','-C',str(repo),'status','--porcelain'],text=True).strip():raise SystemExit('STOP: experiment checkout is not clean')
for p in (home/'v15-runs').glob('*/results/fits/*'):
 if p.is_dir():raise SystemExit('STOP: prior fit artifacts exist; frozen V15 has no resume. Preserve and review them.')
mem={line.split(':')[0]:int(line.split()[1])*1024 for line in pathlib.Path('/proc/meminfo').read_text().splitlines() if line.split(':')[0] in ['MemAvailable','SwapTotal']}
if mem['MemAvailable']<10*1024**3:raise SystemExit('STOP: less than10GiB available WSL RAM')
if mem['SwapTotal']<3*1024**3:raise SystemExit('STOP: less than3GiB WSL swap')
free=os.statvfs(home).f_bavail*os.statvfs(home).f_frsize
if free<10*1024**3:raise SystemExit('STOP: insufficient Linux filesystem space')
# WSL virtual capacity does not prove actual Windows C: free space.
try:
 output=subprocess.check_output(['powershell.exe','-NoProfile','-NonInteractive','-Command','[Console]::Write((Get-PSDrive C).Free)'],text=True,stderr=subprocess.PIPE).strip()
 windows_free=int(output.lstrip('\ufeff'))
except Exception as e:raise SystemExit('STOP: cannot verify actual Windows C: free space: '+str(e))
if windows_free<15*1024**3:raise SystemExit('STOP: actual Windows C: free space below15GiB')
print('HOST_RESOURCE_PASS;Windows C: free GiB=',round(windows_free/1024**3,1))
PY
run_id="v15_0_$(date -u +%Y%m%dT%H%M%SZ)"
run="$HOME/v15-runs/$run_id"
mkdir -p "$run/operations"
cp "$here/run-v15-container.py" "$here/start-v15.sh" "$here/status-v15.sh" "$here/verify-runtime-image.py" "$run/operations/"
python3 - "$repo" "$run" "$run_id" <<'PY'
import json,pathlib,sys,datetime,hashlib
repo=pathlib.Path(sys.argv[1]);run=pathlib.Path(sys.argv[2]);rid=sys.argv[3]
record=json.loads((repo/'artifacts/jof_v15_neural_extension/V15_LOCK_RECORD.json').read_text());assert record['locked_commit']=='d866841eeb87c63f42bd10240c7acc06ee7dbe49'
record.update({'execution_authorized':True,'analysis_authorized':True,'approval_source':'User explicitly authorized full1080training and subsequent frozen statistical analysis in this conversation','run_id':rid,'authorization_recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'analysis_condition':'Only after all1080jobs and combined/per-job integrity checks pass','resume_supported':False})
(run/'authorization.json').write_text(json.dumps(record,indent=2)+'\n');(run/'operations_sha256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (run/'operations').glob('*.py')},indent=2)+'\n')
PY
chmod 600 "$run/authorization.json"
# Explicit read-only check before launching any training. External record is outside /repo.
sudo docker run --rm --network none --cpus 2 --memory 12g \
  --mount "type=bind,source=$repo,target=/repo,readonly" \
  --mount "type=bind,source=$run/authorization.json,target=/authorization/record.json,readonly" \
  "$image" verify
container="v15-$run_id"
sudo docker run -d --name "$container" --label org.global-lnn-sci.v15=true \
  --restart=no --network none --read-only --cpus 2 --memory 12g --memory-swap 16g \
  --tmpfs /tmp:rw,nosuid,nodev,size=2g -e XDG_CACHE_HOME=/tmp/cache -e TORCH_HOME=/tmp/torch \
  --mount "type=bind,source=$repo,target=/repo,readonly" \
  --mount "type=bind,source=$run/authorization.json,target=/authorization/record.json,readonly" \
  --mount "type=bind,source=$run/operations,target=/operations,readonly" \
  --mount "type=bind,source=$run,target=/runs" \
  --entrypoint /workspace/.venvs/global-lnn-sci/bin/python \
  "$image" -u /operations/run-v15-container.py --execute
printf '%s\n' "$container" > "$run/container_name.txt"
printf '%s\n' "$run" > "$HOME/v15-runs/latest_run.txt"
echo "CONTAINER_CREATED: $container"
echo "OUTPUT_DIRECTORY: $run"
echo 'Waiting for actual epoch/loss; container creation alone is not training confirmation.'
for attempt in $(seq 1 90); do
  logs=$(sudo docker logs --tail 40 "$container" 2>&1)
  if grep -q 'TRAINING_CONFIRMED' <<< "$logs"; then
    printf '%s\n' "$logs"
    echo 'Training is confirmed by saved epoch/loss. Keep Windows powered on and the Ubuntu window open.'
    echo "Progress: bash $here/status-v15.sh"
    exit 0
  fi
  if [[ $(sudo docker inspect --format '{{.State.Running}}' "$container") != true ]]; then
    printf '%s\n' "$logs"; echo 'STOPPED before training confirmation. Do not restart or rerun; preserve artifacts.'; exit 1
  fi
  if (( attempt % 10 == 0 )); then echo 'WAITING_FOR_FIRST_EPOCH_LOSS...'; fi
  sleep 2
done
echo 'Container exists but first epoch/loss not confirmed yet. Run status-v15.sh and send its output; do not launch a duplicate.'
