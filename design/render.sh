#!/bin/sh
# Render design/page.html to entry.png (1024x1024) with a local headless Chromium.
# Usage: CHROME=/path/to/chrome-headless-shell sh design/render.sh
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
CHROME=${CHROME:-chrome-headless-shell}
"$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1024,1024 \
  --default-background-color=00000000 \
  --screenshot="$HERE/../entry.png" "file://$HERE/page.html" 2>/dev/null
ls -l "$HERE/../entry.png"
