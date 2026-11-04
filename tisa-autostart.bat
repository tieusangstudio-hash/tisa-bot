@echo off
chcp 65001 >nul
title Tu khoi dong TISA BOT
REM Tu khoi dong TISA BOT cung Windows. Dung: tisa-autostart.bat install | uninstall | status
REM Logic nam trong tisa-autostart.ps1 (ghi/xoa muc TISABot trong HKCU Run, khong can quyen
REM admin). Bat roi thi dang nhap may la server tu chay nen va tu mo dashboard (0.306.0).
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tisa-autostart.ps1" %1
