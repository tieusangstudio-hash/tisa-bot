#!/bin/bash
# ============================================================
# TISA BOT + 53 skill TISA cho Claude Code - cai tron goi tren macOS, mot lenh (28/11/2026)
#
#   curl -fsSL https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/macos/cai-tisa-bot-day-du.sh | bash
#
# 1. Cai TISA BOT ban chinh thuc (get-tisa-bot.sh: app vao Applications, ma nguon vao ~/TISABot,
#    tu chay cung may). May da cai roi thi giu nguyen, chi mo lai.
# 2. Chep 53 skill tu kho tieusangstudio-hash/tisa-skills vao ~/.claude/skills (de len ban cu cung ten).
# 3. Cho TISA BOT len, in link dang nhap va tai khoan, nhac khoi dong lai may.
# Chay lai bao nhieu lan cung duoc.
# ============================================================
set -uo pipefail

PORT="${TISA_PORT:-7777}"
TISA_HOME="${TISA_HOME:-$HOME/TISABot}"
GOC="https://raw.githubusercontent.com/tieusangstudio-hash/tisa-bot/main/packaging/macos"
SKILL_ZIP="https://codeload.github.com/tieusangstudio-hash/tisa-skills/zip/refs/heads/main"

echo ""
echo " =========================================="
echo "  [1/3] Cai TISA BOT (ban chinh thuc)"
echo " =========================================="
if ! curl -fsSL "${GOC}/get-tisa-bot.sh" | bash; then
  echo ""
  echo "  [LOI] Cai TISA BOT chua xong, doc cac dong phia tren. Sua xong chay lai dung lenh nay."
  exit 1
fi

echo ""
echo " =========================================="
echo "  [2/3] Cai 53 skill TISA cho Claude Code"
echo " =========================================="
TMP="$(mktemp -d)"
trap 'rm -rf "${TMP}"' EXIT
if curl -fsSL -o "${TMP}/skills.zip" "${SKILL_ZIP}" && unzip -q "${TMP}/skills.zip" -d "${TMP}"; then
  SRC="$(ls -d "${TMP}"/tisa-skills-*/.claude/skills 2>/dev/null | head -1)"
  if [ -n "${SRC}" ] && [ -d "${SRC}" ]; then
    mkdir -p "${HOME}/.claude/skills"
    cp -R "${SRC}/." "${HOME}/.claude/skills/"
    SO="$(ls -d "${SRC}"/*/ 2>/dev/null | wc -l | tr -d ' ')"
    echo "    OK  Da chep ${SO} skill vao ~/.claude/skills"
  else
    echo "    [!] Goi skill khong dung cau truc, bo qua buoc nay."
  fi
else
  echo "    [!] Khong tai duoc bo skill (kiem tra mang), TISA BOT van dung binh thuong. Chay lai lenh de cai skill."
fi

echo ""
echo " =========================================="
echo "  [3/3] Cho TISA BOT san sang"
echo " =========================================="
LEN=0
for _ in $(seq 1 60); do
  if curl -fsS -o /dev/null "http://127.0.0.1:${PORT}/" 2>/dev/null; then LEN=1; break; fi
  sleep 3
done

USER_TK="admin"; MK=""
if [ -f "${TISA_HOME}/.env" ]; then
  U="$(sed -n 's/^TISA_ADMIN_USER=//p' "${TISA_HOME}/.env" | tail -1 | tr -d "\"'")"
  [ -n "${U}" ] && USER_TK="${U}"
  P="$(sed -n 's/^TISA_ADMIN_PASSWORD=//p' "${TISA_HOME}/.env" | tail -1 | tr -d "\"'")"
  # Chi in mat khau MAC DINH. Mat khau rieng cua chu may khong bao gio in ra man hinh.
  [ "${P}" = "123456" ] && MK="123456"
fi

echo ""
echo "=================================================================="
if [ "${LEN}" = "1" ]; then
  echo "  TISA BOT DA CHAY. Mo trinh duyet vao:"
else
  echo "  TISA BOT dang khoi dong (lan dau co the mat them 1-2 phut). Mo trinh duyet vao:"
fi
echo "      http://127.0.0.1:${PORT}      (hoac http://localhost:${PORT})"
echo ""
echo "  Dang nhap:"
echo "      Ten dang nhap:  ${USER_TK}"
if [ -n "${MK}" ]; then
  echo "      Mat khau:       ${MK}   (doi ngay o trang Tai khoan truoc khi mo truy cap tu xa)"
else
  echo "      Mat khau:       mat khau da dat luc cai lan truoc (giu nguyen)"
fi
echo ""
echo "  Sau khi dang nhap:"
echo "    - Trang Models: Ket noi Claude, roi bam \"Chuyen sang token dai han\""
echo "      (dung 1 nam, tat mo may khong bi vang ket noi)."
echo "    - Claude Code: go /ts- de thay 53 skill (mo lai Claude Code neu chua thay)."
echo ""
echo "  NEN KHOI DONG LAI MAY MOT LAN de TISA BOT tu chay cung may va"
echo "  Claude Code nap du skill moi. Bat lai may, TISA BOT tu mo."
echo "=================================================================="
