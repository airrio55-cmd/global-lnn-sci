#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
sha256sum -c parts.sha256
archive=v15-runtime-locked-d866841.tar.gz
if [[ -e "$archive" ]]; then
  sha256sum -c image.sha256
  echo 'Existing archive is valid; nothing overwritten.'
  exit 0
fi
tmp=$(mktemp ./runtime-reassembly.XXXXXX)
trap 'rm -f -- "$tmp"' EXIT
cat runtime.part-01 runtime.part-02 runtime.part-03 runtime.part-04 runtime.part-05 > "$tmp"
printf '%s  %s\n' '9b6d1e17f519c99aa0b42055439f564430b9374e84fd07143e3541b68870dbe6' "$tmp" | sha256sum -c -
mv -- "$tmp" "$archive"
trap - EXIT
sha256sum -c image.sha256
echo 'IMAGE_RESTORED_AND_SHA256_VERIFIED. No training was started.'
