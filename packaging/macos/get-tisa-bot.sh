#!/bin/bash
# ============================================================
# TISA BOT - one-line install for macOS, no "cannot be opened" block
#
#   curl -fsSL https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/macos/get-tisa-bot.sh | bash
#
# Downloads the same TISA-BOT-macOS.dmg the website links to, copies TISA BOT.app into
# Applications, then runs its first-time install right here in this Terminal window.
# Why no Gatekeeper prompt: macOS only checks files a browser saved (they carry a quarantine
# flag), and the app is not signed with an Apple Developer ID yet. A file curl downloads
# carries no such flag.
# ============================================================
set -euo pipefail

URL="https://github.com/tieusangstudio-hash/tisa-bot/releases/download/desktop/TISA-BOT-macOS.dmg"
[ "$(uname -s)" = "Darwin" ] || { echo "This installer is for macOS. On Linux run ./install.sh from the repo."; exit 1; }

TMP="$(mktemp -d)"
MNT=""
cleanup() { [ -n "${MNT}" ] && hdiutil detach -quiet "${MNT}" 2>/dev/null; rm -rf "${TMP}"; }
trap cleanup EXIT

echo ""
echo "  TISA BOT: dang tai bo cai... (downloading)"
curl -fL --progress-bar -o "${TMP}/TISA-BOT-macOS.dmg" "${URL}"
MNT="$(hdiutil attach -nobrowse -readonly "${TMP}/TISA-BOT-macOS.dmg" | awk -F'\t' '/\/Volumes\//{print $NF}')"
[ -d "${MNT}/TISA BOT.app" ] || { echo "The disk image has no TISA BOT.app"; exit 1; }

# /Applications when it is writable (an admin account), else ~/Applications.
DEST="/Applications"
[ -w "${DEST}" ] || { DEST="${HOME}/Applications"; mkdir -p "${DEST}"; }
# Replace only the app bundle; the brain lives in ~/TISABot and is never touched here.
rm -rf "${DEST}/TISA BOT.app"
cp -R "${MNT}/TISA BOT.app" "${DEST}/"
xattr -dr com.apple.quarantine "${DEST}/TISA BOT.app" 2>/dev/null || true
echo "  Da chep TISA BOT vao ${DEST} (copied to ${DEST})"

APP="${DEST}/TISA BOT.app"
if [ -d "${HOME}/TISABot/.git" ] && [ -x "${HOME}/TISABot/.venv/bin/python" ]; then
  echo "  TISA BOT da cai san, dang mo... (already installed, opening)"
  open "${APP}"
  exit 0
fi
# First install in THIS window. stdin is the curl pipe, so give the installer the keyboard
# back: install.sh asks for the TISA BOT admin account and may ask for the Mac password.
if (exec < /dev/tty) 2>/dev/null; then
  bash "${APP}/Contents/Resources/bootstrap.sh" < /dev/tty
else
  bash "${APP}/Contents/Resources/bootstrap.sh" < /dev/null
fi
