"""Trợ lý không tự khởi động lại TISA BOT giữa lượt trả lời (V2.75, sự cố 10/11/2026).

Chuyện đã xảy ra: chủ nhờ cộng sự Hằng sửa lỗi chào "buổi tối" lúc 9 giờ sáng. Hằng sửa xong rồi tự chạy
`launchctl kickstart -k gui/.../com.tisa.os` để phần mới chạy ngay. Lệnh đó tắt luôn máy chủ đang chạy CHÍNH lượt trả
lời của Hằng, nên câu trả lời không bao giờ tới: chủ nhắn "Hằng ơi, bạn đâu", "bạn ơi" mà chỉ thấy vòng xoay. Hai lần
trong 20 phút, và cả các khung chat khác đang chạy lúc đó cũng mất lượt.

Cách sửa: móc vào hook PreToolUse sẵn có của mọi lượt Claude (claude_secret_hook.py). Lệnh shell nào khởi động lại hoặc
tắt máy chủ TISA BOT thì bị từ chối, đồng thời hệ thống HẸN khởi động lại: chờ mọi lượt chat đang chạy xong (kể cả lượt
vừa xin), rồi mới đổi ca bằng đúng đường của bộ cập nhật (updater.py: launchd / Windows / systemd / nohup). Trợ lý nhận
lời từ chối kèm hướng dẫn trả lời người dùng ngay, nên người dùng luôn nhận được câu trả lời.

Hỏng ở đây không bao giờ được chặn một lượt: mọi lỗi đều trả {} (cho lệnh chạy như cũ).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

_SERVER = Path(__file__).resolve().parent

# Chờ hết lượt chat bao lâu thì thôi chờ và khởi động lại luôn (lượt kẹt không ai gạch).
CHO_TOI_DA = 2 * 3600
# Phải yên (không lượt nào chạy) liên tục chừng này giây mới đổi ca, để lượt vừa xong kịp ghi câu trả lời.
YEN_DU = 6

_khoa = threading.Lock()
_hen = {"luc": 0.0, "ly_do": "", "luong": None}

_NHAN = r"com\.tisa\.os(?!\.open)(?![\w-])"
_MAU = [
    # macOS: launchd giữ máy chủ.
    re.compile(r"\blaunchctl\s+(?:kickstart|stop|kill|unload|bootout|remove)\b[^\n;&|]*" + _NHAN, re.I),
    # Linux: systemd.
    re.compile(r"\bsystemctl\s+(?:--user\s+)?(?:restart|stop|kill|reload-or-restart|try-restart)\b[^\n;&|]*\btisa", re.I),
    # Diệt tiến trình uvicorn của máy chủ.
    re.compile(r"\b(?:pkill|killall)\b[^\n;&|]*(?:uvicorn|main:app)", re.I),
    re.compile(r"\bkill\b[^\n;&|]*\$\([^)]*(?:lsof|pgrep|fuser)[^)]*(?:7777|uvicorn|main:app)", re.I),
    re.compile(r"\b(?:lsof|pgrep|fuser)\b[^\n;&]*(?:7777|uvicorn|main:app)[^\n;&]*\|\s*xargs\s+(?:-\S+\s+)*kill\b", re.I),
    # Windows: bộ tắt / bật lại của bản cài (start-*.vbs tự tắt bản cũ trước khi chạy).
    re.compile(r"\b(?:stop|start|restart)-tisa\.(?:bat|cmd|vbs|ps1)\b", re.I),
    re.compile(r"\bStop-Process\b[^\n;|]*\b(?:uvicorn|main:app)", re.I),
]
_KILL_SO = re.compile(r"\b(?:kill|taskkill)\b[^\n;&|]*?(?:/pid\s+|\s)(\d{2,7})\b", re.I)


def la_lenh_khoi_dong_lai(lenh: str, pid_may_chu: int = 0) -> bool:
    """Lệnh shell này khởi động lại hoặc tắt máy chủ TISA BOT đang chạy không."""
    s = str(lenh or "")
    if not s.strip():
        return False
    if any(m.search(s) for m in _MAU):
        return True
    pid = int(pid_may_chu or os.getpid())
    return any(int(x) == pid for x in _KILL_SO.findall(s))


def _so_luot_dang_chay() -> int:
    try:
        import luot_dang_chay
        return len(getattr(luot_dang_chay, "_SONG", {}) or {})
    except Exception:  # noqa: BLE001
        return 0


_TRO_GIUP = r'''
import sys, time
sys.path.insert(0, ".")
import updater
pid, port = int(sys.argv[1]), sys.argv[2]
m = updater.service_mode()
if m == "systemd":
    m = "systemd-signal"
updater.log("Khởi động lại theo hẹn của trợ lý, sau khi các lượt chat đã xong (chế độ %s)." % m)
if m == "nohup":
    # Chỉ dừng đúng tiến trình máy chủ: stop_server còn dừng mọi tiến trình có kết nối tới cổng (cả trình duyệt).
    updater._kill_pid(pid)
else:
    updater.stop_server(m, pid, port)
time.sleep(2)
updater.start_server(m, port)
'''


def _doi_ca() -> None:
    """Đổi ca máy chủ bằng một tiến trình tách rời (sống lâu hơn máy chủ), y đường của bộ cập nhật."""
    port = os.getenv("TISA_PORT") or "7777"
    args = [sys.executable, "-c", _TRO_GIUP, str(os.getpid()), str(port)]
    if os.name == "nt":
        subprocess.Popen(args, cwd=str(_SERVER), creationflags=0x00000008 | 0x00000200)  # DETACHED | NEW_GROUP
    else:
        subprocess.Popen(args, cwd=str(_SERVER), start_new_session=True,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _cho_roi_doi_ca() -> None:
    bat_dau = time.time()
    yen_tu = 0.0
    while True:
        time.sleep(2)
        if _so_luot_dang_chay() == 0:
            yen_tu = yen_tu or time.time()
            if time.time() - yen_tu >= YEN_DU:
                break
        else:
            yen_tu = 0.0
        if time.time() - bat_dau > CHO_TOI_DA:
            print("[tisa_khoi_dong_lai] chờ quá lâu, khởi động lại dù còn lượt chạy", file=sys.stderr)
            break
    print(f"[tisa_khoi_dong_lai] khởi động lại theo hẹn: {_hen['ly_do'][:120]}", file=sys.stderr)
    try:
        _doi_ca()
    except Exception as e:  # noqa: BLE001
        print(f"[tisa_khoi_dong_lai] không khởi động lại được: {type(e).__name__}: {e}", file=sys.stderr)
        with _khoa:
            _hen.update(luc=0.0, luong=None)


def hen_khoi_dong_lai(ly_do: str = "") -> bool:
    """Hẹn khởi động lại sau khi hết lượt chat. Gọi nhiều lần chỉ hẹn một lần. True = đã có hẹn."""
    with _khoa:
        if _hen["luong"] is not None and _hen["luong"].is_alive():
            return True
        _hen.update(luc=time.time(), ly_do=str(ly_do or ""))
        t = threading.Thread(target=_cho_roi_doi_ca, name="tisa-khoi-dong-lai", daemon=True)
        _hen["luong"] = t
        t.start()
    print(f"[tisa_khoi_dong_lai] đã hẹn khởi động lại sau khi hết lượt chat: {str(ly_do)[:120]}", file=sys.stderr)
    return True


LOI_TU_CHOI = (
    "Lệnh này bị chặn: nó khởi động lại / tắt máy chủ TISA BOT, mà chính lượt trả lời bạn đang chạy nằm trong máy chủ đó, "
    "nên chạy ngay thì người dùng sẽ KHÔNG nhận được câu trả lời. Hệ thống đã HẸN tự khởi động lại ngay sau khi lượt này "
    "và các lượt đang chạy khác xong (vài giây). Đừng thử lại bằng lệnh khác. Hãy trả lời người dùng ngay bây giờ: "
    "việc đã làm xong, thay đổi có hiệu lực sau khi TISA BOT tự khởi động lại trong ít giây; muốn kiểm tra kết quả thì "
    "nhắn lại sau khoảng 30 giây."
)


def chan_lenh(input_data) -> dict:
    """Dùng trong hook PreToolUse. Lệnh khởi động lại máy chủ: hẹn khởi động lại + trả lời từ chối. Còn lại {}."""
    try:
        if os.getenv("TISA_CHO_TU_KHOI_DONG_LAI") == "1":
            return {}
        d = input_data or {}
        vao = d.get("tool_input") or {}
        lenh = vao.get("command") if isinstance(vao, dict) else ""
        if not lenh or not la_lenh_khoi_dong_lai(str(lenh)):
            return {}
        hen_khoi_dong_lai(str(lenh))
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                       "permissionDecisionReason": LOI_TU_CHOI}}
    except Exception:  # noqa: BLE001 - hỏng ở đây không được chặn lượt
        return {}
