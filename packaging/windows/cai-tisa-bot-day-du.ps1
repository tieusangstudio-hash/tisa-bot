# ============================================================
# TISA BOT + 53 skill TISA cho Claude Code - cai tron goi tren Windows, mot lenh (28/11/2026)
#
#   powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/windows/cai-tisa-bot-day-du.ps1 | iex"
#
# 1. Cai TISA BOT ban chinh thuc, khong can bam (get-tisa-bot.ps1 voi TISA_SILENT=1).
# 2. Chep 53 skill tu kho tieusangstudio-hash/tisa-skills vao %USERPROFILE%\.claude\skills.
# 3. Ket noi Claude: may da dang nhap Claude Code thi dung chung, chua thi tu mo trang dang nhap.
# 4. Cho TISA BOT len (chua len thi tu chay lai va in nhat ky), in link, tai khoan, nhac khoi dong lai.
# ASCII only: Windows PowerShell 5.1 reads text without BOM in the ANSI codepage.
# ============================================================
& {
  $ErrorActionPreference = "Stop"
  $ProgressPreference = "SilentlyContinue"
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  $port = if ($env:TISA_PORT) { $env:TISA_PORT } else { "7777" }
  $goc = "https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/windows"

  Write-Host ""
  Write-Host "  [1/4] Cai TISA BOT (ban chinh thuc)" -ForegroundColor Cyan
  $env:TISA_SILENT = "1"
  try {
    Invoke-Expression (Invoke-RestMethod "$goc/get-tisa-bot.ps1" -UseBasicParsing)
  } catch {
    Write-Host "  [LOI] Cai TISA BOT chua xong: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Sua xong chay lai dung lenh nay." -ForegroundColor Red
    return
  }

  Write-Host ""
  Write-Host "  [2/4] Cai 53 skill TISA cho Claude Code" -ForegroundColor Cyan
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
  Write-Host "  [3/4] Ket noi Claude cho TISA BOT" -ForegroundColor Cyan
  # A fresh install put npm's folder on the user PATH, which this session has not read yet.
  $env:Path = [Environment]::GetEnvironmentVariable("Path", "User") + ";" + [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + $env:Path
  $claudeOk = $false
  $cl = Get-Command claude -ErrorAction SilentlyContinue
  function DaDangNhap { try { $j = (& cmd /d /c "claude auth status --json" 2>$null | Out-String); return ($j -match '"loggedIn":\s*true') } catch { return $false } }
  if (-not $cl) {
    Write-Host "    [!] Chua thay lenh claude, TISA BOT se nhac ket noi o trang Models." -ForegroundColor Yellow
  } elseif (DaDangNhap) {
    $claudeOk = $true
    Write-Host "    OK  May da dang nhap Claude, TISA BOT dung chung, khong phai dang nhap lai" -ForegroundColor Green
  } else {
    Write-Host "    Trinh duyet se mo trang dang nhap Claude: dang nhap roi bam Authorize (Cho phep)."
    Start-Process -FilePath $env:ComSpec -ArgumentList "/d /c claude auth login --claudeai" -WindowStyle Hidden
    for ($i = 0; $i -lt 100; $i++) { Start-Sleep -Seconds 3; if (DaDangNhap) { $claudeOk = $true; break } }
    if ($claudeOk) { Write-Host "    OK  Da ket noi Claude" -ForegroundColor Green }
    else { Write-Host "    [!] Chua dang nhap Claude. Vao trang Models cua TISA BOT bam Ket noi Claude." -ForegroundColor Yellow }
  }

  Write-Host ""
  Write-Host "  [4/4] Cho TISA BOT san sang" -ForegroundColor Cyan
  $dir = Join-Path $env:USERPROFILE "TISABot"
  function DangChay { try { Invoke-WebRequest -Uri "http://127.0.0.1:$port/" -UseBasicParsing -TimeoutSec 3 | Out-Null; return $true } catch { return $false } }
  $len = $false
  for ($i = 0; $i -lt 40; $i++) { if (DangChay) { $len = $true; break }; Start-Sleep -Seconds 3 }
  if (-not $len -and (Test-Path "$dir\start-tisa.vbs")) {
    Write-Host "    TISA BOT chua len, dang chay lai..."
    Start-Process wscript.exe -ArgumentList "//nologo `"$dir\start-tisa.vbs`"" -WorkingDirectory $dir
    for ($i = 0; $i -lt 40; $i++) { if (DangChay) { $len = $true; break }; Start-Sleep -Seconds 3 }
  }
  $log = Join-Path $dir "server\tisa.log"
  if (-not $len -and (Test-Path $log)) {
    Write-Host "    [!] TISA BOT van chua len. 25 dong cuoi nhat ky ($log):" -ForegroundColor Yellow
    Get-Content $log -Tail 25 | ForEach-Object { Write-Host "      $_" }
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
  if ($claudeOk) { Write-Host "  Claude: da ket noi" } else { Write-Host "  Claude: chua ket noi, vao trang Models bam Ket noi Claude" }
  Write-Host ""
  Write-Host "  Sau khi dang nhap:"
  Write-Host "    - Trang Models: bam ""Chuyen sang token dai han""" 
  Write-Host "      (dung 1 nam, tat mo may khong bi vang ket noi)."
  Write-Host "    - Claude Code: go /ts- de thay 53 skill (mo lai Claude Code neu chua thay)."
  Write-Host ""
  Write-Host "  NEN KHOI DONG LAI MAY MOT LAN de TISA BOT tu chay cung may va" -ForegroundColor Cyan
  Write-Host "  Claude Code nap du skill moi. Bat lai may, TISA BOT tu mo." -ForegroundColor Cyan
  Write-Host "==================================================================" -ForegroundColor Green
}
