#!/bin/bash
# Double-click in Finder to stop TISA BOT.
cd "$(dirname "$0")" || exit 1
bash "bin/tisa-stop.sh"
echo ""
echo "You can close this window."
