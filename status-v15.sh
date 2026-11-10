#!/usr/bin/env bash
set -euo pipefail
run=$(cat "$HOME/v15-runs/latest_run.txt")
container=$(cat "$run/container_name.txt")
sudo docker inspect --format 'Container={{.Name}} Running={{.State.Running}} ExitCode={{.State.ExitCode}} OOMKilled={{.State.OOMKilled}}' "$container"
if [[ -f "$run/progress.json" ]]; then cat "$run/progress.json"; else echo 'No progress record yet; training is not confirmed.'; fi
sudo docker logs --tail 15 "$container" 2>&1
if [[ $(sudo docker inspect --format '{{.State.Running}}' "$container") != true ]]; then
  echo 'Container stopped. A stale RUNNING progress value is not proof of live training. No automatic resume exists; preserve all completed jobs.'
fi
