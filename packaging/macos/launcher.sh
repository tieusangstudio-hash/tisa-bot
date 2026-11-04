#!/bin/bash
# ============================================================
# TISA BOT.app (the one inside TISA-BOT-macOS.dmg) - what a double-click runs.
#
# First run (no TISA BOT in ~/TISABot yet): opens Terminal on bootstrap.sh, which checks the Mac,
# installs what is missing and starts TISA BOT. Terminal on purpose: the first install takes
# minutes and may ask for the Mac password once, so the person must SEE what happens.
# Every run after that: bin/tisa-start.sh, which only opens the window when TISA BOT is already
# up and starts it first when it is not. It never restarts a running server.
#
# Unlike the in-repo "TISA BOT.app" (which must stay inside the repo folder), this bundle can
# live in /Applications: it finds TISA BOT through TISA_HOME, default ~/TISABot.
# ============================================================
TISA_HOME="${TISA_HOME:-$HOME/TISABot}"
RES="$(cd "$(dirname "$0")/../Resources" && pwd)"

if [ -d "${TISA_HOME}/.git" ] && [ -x "${TISA_HOME}/.venv/bin/python" ] && [ -x "${TISA_HOME}/bin/tisa-start.sh" ]; then
  exec "${TISA_HOME}/bin/tisa-start.sh"
fi

# macOS asks once whether "TISA BOT" may control Terminal. If the person clicks Don't Allow
# (or the prompt never shows), osascript fails and nothing would happen at all: fall back to
# putting the command on the clipboard, opening Terminal, and saying "paste it".
# Not `open -a Terminal bootstrap.sh`: a script copied off the downloaded .dmg carries the
# quarantine flag, and Gatekeeper blocks it when it is opened through LaunchServices.
if ! osascript - "${RES}/bootstrap.sh" "${TISA_HOME}" <<'AS' >/dev/null 2>&1
on run argv
  tell application "Terminal"
    activate
    do script "TISA_HOME=" & quoted form of (item 2 of argv) & " bash " & quoted form of (item 1 of argv)
  end tell
end run
AS
then
  # %q escapes spaces and quotes in a form both bash and zsh (the Terminal default) accept.
  printf 'TISA_HOME=%q bash %q\n' "${TISA_HOME}" "${RES}/bootstrap.sh" | pbcopy
  open -a Terminal
  osascript -e 'display alert "TISA BOT" message "Terminal is open. Paste (Cmd+V) and press Enter to install TISA BOT.\n\nTerminal da mo. Dan (Cmd+V) roi bam Enter de cai TISA BOT."' >/dev/null 2>&1 || true
fi
