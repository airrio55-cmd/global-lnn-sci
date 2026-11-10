#!/usr/bin/env bash
set -euo pipefail
here=$(cd -- "$(dirname -- "$0")" && pwd)
repo="$HOME/global-lnn-sci"
source_run=${1:-"$HOME/v15-runs/v15_0_20261110T001623Z"}
backup=${2:-"$HOME/v15-backup-20261110T042742Z.tar.gz"}
backup_sha=${3:-'62f383a7d5642a0cc25d89a8ae4302b85f68ee4f58b9ce7d1b7d9b217a6a8997'}
image='global-lnn-sci-v15-runtime:locked-d866841'
[[ -d "$source_run/results/fits" && -f "$backup" ]] || { echo 'STOP: source run or backup missing'; exit 1; }
sudo -v
sudo service docker start
sudo docker image inspect "$image" | python3 "$here/../verify-runtime-image.py"
[[ -z $(sudo docker ps -q --filter 'label=org.global-lnn-sci.v15=true') ]] || { echo 'STOP: a V15 process is still running'; exit 1; }
run="$HOME/v15-runs/v15_1_recovery_$(date -u +%Y%m%dT%H%M%SZ)"
mkdir "$run"
mkdir -p "$run/operations/v15_1"
cp "$here/"*.py "$here/"*.sh "$here/version_manifest.json" "$here/"*.md "$run/operations/v15_1/"
python3 - "$repo" "$run" "$source_run" "$backup_sha" <<'PY'
from pathlib import Path
import json,sys,datetime,hashlib
repo,run,source=map(Path,sys.argv[1:4]);sha=sys.argv[4]
r=json.loads((repo/'artifacts/jof_v15_neural_extension/V15_LOCK_RECORD.json').read_text());assert r['locked_commit']=='d866841eeb87c63f42bd10240c7acc06ee7dbe49'
r.update({'run_id':run.name,'recovery_version':'V15.1','source_run_id':source.name,'source_backup_sha256':sha,'execution_authorized':True,'analysis_authorized':True,'approval_source':'User approved versioned recovery preparation;training requires separate execute-recovery operator invocation after readiness PASS','authorization_recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'resume_mode':'Reuse fully revalidated jobs;restart incomplete jobs from epoch1'})
(run/'operations_sha256.json').write_text(json.dumps({str(p.relative_to(run/'operations')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (run/'operations').rglob('*') if p.is_file()},indent=2)+'\n')
(run/'authorization.json').write_text(json.dumps(r,indent=2)+'\n');(run/'source_paths.json').write_text(json.dumps({'source_run':str(source),'backup':None,'source_backup_sha256':sha},indent=2)+'\n')
PY
python3 - "$run/source_paths.json" "$backup" <<'PY'
import json,sys,pathlib
p=pathlib.Path(sys.argv[1]);x=json.loads(p.read_text());x['backup']=sys.argv[2];p.write_text(json.dumps(x,indent=2)+'\n')
PY
# Preparation never invokes a fitting worker or AUC analysis. Original run and backup are read-only.
sudo docker run --rm --network none --read-only --cpus 2 --memory 12g --memory-swap 16g \
 --tmpfs /tmp:rw,nosuid,nodev,size=2g \
 --mount "type=bind,source=$repo,target=/repo,readonly" \
 --mount "type=bind,source=$source_run,target=/source,readonly" \
 --mount "type=bind,source=$backup,target=/backup/source.tar.gz,readonly" \
 --mount "type=bind,source=$run/authorization.json,target=/authorization/record.json,readonly" \
 --mount "type=bind,source=$run/operations/v15_1,target=/operations,readonly" \
 --mount "type=bind,source=$run,target=/runs" \
 --entrypoint /workspace/.venvs/global-lnn-sci/bin/python "$image" -u /operations/prepare.py 2>&1 | tee "$run/preparation.log"
printf '%s\n' "$run" > "$HOME/v15-runs/latest_recovery.txt"
echo "RECOVERY_PREPARED_DIRECTORY: $run"
echo 'Preparation only. No training or statistics were started. Keep original run,container and backup.'
