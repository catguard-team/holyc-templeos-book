#!/bin/sh
set -eu
cd -- "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if command -v python3 >/dev/null 2>&1; then
  exec python3 tools/launch.py "$@"
fi
printf '%s\n' 'Python 3.10+ is required. See docs/PLATFORMS.md.'
exit 1
