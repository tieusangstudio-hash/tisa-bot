@echo off
chcp 65001 >nul
title Khoi dong TISA BOT
cd /d "%~dp0"

echo Bat TISA BOT chay NEN - khong con cua so den (port 7777)...
REM Viec tat instance cu + chay server AN giao het cho start-tisa.vbs (cua so an hoan toan).
REM Log ghi vao server\tisa.log (mo file do neu can xem loi). Tat server: stop-tisa.bat.
wscript //nologo start-tisa.vbs

echo.
echo Da bat. Cho ~10 giay roi mo http://localhost:7777 va bam Ctrl+Shift+R.
echo (Tat server: chay stop-tisa.bat. Xem loi: mo file server\tisa.log)
timeout /t 4 >nul
