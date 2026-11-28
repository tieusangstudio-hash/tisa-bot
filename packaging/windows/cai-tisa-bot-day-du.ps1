# ============================================================
# TISA BOT + 53 skill TISA cho Claude Code - cai tron goi tren Windows, mot lenh (28/11/2026)
#
#   powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/windows/cai-tisa-bot-day-du.ps1 | iex"
#
# 1. Cai TISA BOT ban chinh thuc, khong can bam (get-tisa-bot.ps1 voi TISA_SILENT=1).
# 2. Chep 53 skill tu kho tieusangstudio-hash/tisa-skills vao %USERPROFILE%\.claude\skills.
# 3. Cho TISA BOT len, in link dang nhap va tai khoan, nhac khoi dong lai may.
# ASCII only: Windows PowerShell 5.1 reads text without BOM in the ANSI codepage.
# ============================================================
& {
  $ErrorActionPreference = "Stop"
  $ProgressPreference = "SilentlyContinue"
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  $port = if ($env:TISA_PORT) { $env:TISA_PORT } else { "7777" }
  $goc = "https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/windows"

  Write-Host ""
  Write-Host "  [1/3] Cai TISA BOT (ban chinh thuc)" -ForegroundColor Cyan
  $env:TISA_SILENT = "1"
  try {
    Invoke-Expression (Invoke-RestMethod "$goc/get-tisa-bot.ps1" -UseBasicParsing)
  } catch {
    Write-Host "  [LOI] Cai TISA BOT chua xong: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Sua xong chay lai dung lenh nay." -ForegroundColor Red
    return
  }

  Write-Host ""
  Write-Host "  [2/3] Cai 53 skill TISA cho Claude Code" -ForegroundColor Cyan
  $tmp = Join-Path $env:TEMP ("tisa-skills-" + [guid]::NewGuid().ToString("N"))
  try {
    New-Item -ItemType Directory -Force $tmp | Out-Null
    $zip = Join-Path $tmp "skills.zip"
    Invoke-WebRequest -Uri "https://codeload.github.com/tieusangstudio-hash/tisa-skills/zip/refs/heads/main" -OutFile $zip -UseBasicParsing
    Expand-Archive -Path $zip -DestinationPath $tmp -Force
    $src = Get-ChildItem -Path $tmp -Directory -Filter "tisa-skills-*" | Select-Object -First 1
    $src = if ($src) { Join-Path $src.FullName ".claude\skills" } else { "" }
    if ($src -and (Test-Path $src)) {
      $dst = Join-Path $env:USERPROFILE ".claude\skills"
      New-Item -ItemType Directory -Force $dst | Out-Null
      Copy-Item -Path (Join-Path $src "*") -Destination $dst -Recurse -Force
      $so = (Get-ChildItem -Path $src -Directory).Count
      Write-Host "    OK  Da chep $so skill vao $dst" -ForegroundColor Green
    } else {
      Write-Host "    [!] Goi skill khong dung cau truc, bo qua buoc nay." -ForegroundColor Yellow
    }
  } catch {
    Write-Host "    [!] Khong tai duoc bo skill: $($_.Exception.Message). TISA BOT van dung binh thuong." -ForegroundColor Yellow
  } finally {
    Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
  }

  Write-Host ""
  Write-Host "  [3/3] Cho TISA BOT san sang" -ForegroundColor Cyan
  $len = $false
  for ($i = 0; $i -lt 60; $i++) {
    try { Invoke-WebRequest -Uri "http://127.0.0.1:$port/" -UseBasicParsing -TimeoutSec 3 | Out-Null; $len = $true; break } catch { Start-Sleep -Seconds 3 }
  }

  $userTk = "admin"; $mk = ""
  $envf = Join-Path $env:USERPROFILE "TISABot\.env"
  if (Test-Path $envf) {
    foreach ($ln in Get-Content $envf) {
      if ($ln -match '^TISA_ADMIN_USER=(.*)$') { $u = $Matches[1].Trim('"', "'"); if ($u) { $userTk = $u } }
      # Only the DEFAULT password is printed. An owner's own password never is.
      if ($ln -match '^TISA_ADMIN_PASSWORD=(.*)$') { if ($Matches[1].Trim('"', "'") -eq "123456") { $mk = "123456" } }
    }
  }

  Write-Host ""
  Write-Host "==================================================================" -ForegroundColor Green
  if ($len) { Write-Host "  TISA BOT DA CHAY. Mo trinh duyet vao:" -ForegroundColor Green }
  else { Write-Host "  TISA BOT dang khoi dong (lan dau co the mat them 1-2 phut). Mo trinh duyet vao:" -ForegroundColor Yellow }
  Write-Host "      http://127.0.0.1:$port      (hoac http://localhost:$port)"
  Write-Host ""
  Write-Host "  Dang nhap:"
  Write-Host "      Ten dang nhap:  $userTk"
  if ($mk) { Write-Host "      Mat khau:       $mk   (doi ngay o trang Tai khoan truoc khi mo truy cap tu xa)" }
  else { Write-Host "      Mat khau:       mat khau da dat luc cai lan truoc (giu nguyen)" }
  Write-Host ""
  Write-Host "  Sau khi dang nhap:"
  Write-Host "    - Trang Models: Ket noi Claude, roi bam ""Chuyen sang token dai han"""
  Write-Host "      (dung 1 nam, tat mo may khong bi vang ket noi)."
  Write-Host "    - Claude Code: go /ts- de thay 53 skill (mo lai Claude Code neu chua thay)."
  Write-Host ""
  Write-Host "  NEN KHOI DONG LAI MAY MOT LAN de TISA BOT tu chay cung may va" -ForegroundColor Cyan
  Write-Host "  Claude Code nap du skill moi. Bat lai may, TISA BOT tu mo." -ForegroundColor Cyan
  Write-Host "==================================================================" -ForegroundColor Green
}
