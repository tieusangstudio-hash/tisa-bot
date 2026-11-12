# ============================================================
# TISA BOT - one-line install for Windows, no red SmartScreen screen
#
#   irm https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/windows/get-tisa-bot.ps1 | iex
#
# Downloads the same TISA-BOT-Setup.exe the website links to and opens its wizard.
# Why this avoids "Windows protected your PC": SmartScreen checks files the BROWSER saved
# (they carry a "downloaded from the Internet" mark) and the .exe is not code-signed yet.
# A file PowerShell downloads itself carries no such mark. Claude Code, Antigravity and Grok
# install the same way. Once the .exe is signed (desktop-installers.yml, WINDOWS_CERT_*), the
# normal download stops warning too and this script stays as a shortcut.
#
# Everything runs inside & { } so nothing leaks into the person's PowerShell session.
# ASCII only: Windows PowerShell 5.1 reads text without BOM in the ANSI codepage.
# ============================================================
& {
  $ErrorActionPreference = "Stop"
  $ProgressPreference = "SilentlyContinue"   # the PS 5.1 progress bar makes downloads 10x slower
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  $url = "https://github.com/tieusangstudio-hash/tisa-bot/releases/download/desktop/TISA-BOT-Setup.exe"
  $out = Join-Path $env:TEMP "TISA-BOT-Setup.exe"
  Write-Host ""
  Write-Host "  TISA BOT: dang tai bo cai... (downloading the installer)" -ForegroundColor Cyan
  try {
    Invoke-WebRequest -Uri $url -OutFile $out -UseBasicParsing
  } catch {
    Write-Host "  Khong tai duoc bo cai: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Kiem tra mang Internet roi chay lai lenh." -ForegroundColor Red
    return
  }
  Write-Host "  Da tai xong, dang mo trinh cai dat TISA BOT... (opening the setup wizard)" -ForegroundColor Green
  if ($env:TISA_SILENT -eq "1") {
    # Claude Code or a script runs this: no wizard clicks, wait until done, then start TISA BOT.
    $p = Start-Process -FilePath $out -ArgumentList "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-" -Wait -PassThru
    if ($p.ExitCode -ne 0) { throw "TISA BOT setup failed with code $($p.ExitCode)" }
    $dir = Join-Path $env:USERPROFILE "TISABot"
    Start-Process wscript.exe -ArgumentList "//nologo `"$dir\start-tisa.vbs`"" -WorkingDirectory $dir
    Write-Host "  Xong. Mo http://127.0.0.1:7777 (admin / 123456)" -ForegroundColor Green
    return
  }
  Start-Process -FilePath $out
  # The rest happens inside the TISA BOT Setup window, progress included. Say so, or people keep
  # watching this console and think the install is stuck.
  Write-Host "  Moi thu tiep theo hien trong cua so TISA BOT Setup. Co the dong cua so nay." -ForegroundColor Cyan
  Write-Host "  (Everything else shows in the TISA BOT Setup window. You can close this one.)" -ForegroundColor Cyan
}
