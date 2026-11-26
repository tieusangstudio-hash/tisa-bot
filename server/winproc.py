"""Chạy lệnh con trên Windows mà KHÔNG bật cửa sổ console đen.

Vì sao cần một module riêng cho đúng một cái cờ
-----------------------------------------------
TISA BOT trên Windows khởi động qua `start-tisa.vbs`, tức tiến trình server chạy **không có
console**. Trong Windows, một tiến trình không console mà sinh ra chương trình dạng console
(git, curl, node, python...) thì hệ điều hành TỰ CẤP cho đứa con một cửa sổ console mới. Người
dùng thấy đúng một cái nháy đen giữa màn hình rồi tắt - chủ repo báo 2026-08-13: "thi thoảng
chuyển tab nó lại nháy đen màn hình terminal xong tắt luôn".

Nó không làm hỏng gì, nhưng nó cướp tiêu điểm bàn phím và trông như phần mềm bị lỗi. Chữa bằng
đúng một cờ: `CREATE_NO_WINDOW`.

Cờ này CHỈ có trên Windows, nên mọi nơi đều phải viết `getattr(subprocess, ...)` hoặc `if
os.name == "nt"`. Trước khi có file này, mỗi module tự viết lại một kiểu và đã sai theo hai
cách khác nhau:

- quên hẳn (curl của Substack, git của luồng cập nhật, script của nhắc hẹn);
- viết đúng hình thức nhưng lấy nhầm chỗ: `getattr(asyncio.subprocess, "CREATE_NO_WINDOW", 0)`
  trong plugin `zalo-image`. Module `asyncio.subprocess` KHÔNG hề export cờ đó, nên biểu thức
  luôn trả 0 và lời gọi trông như đã được bảo vệ trong khi không có gì cả. Đây đúng kiểu lỗi
  chỉ lộ ra trên máy người dùng.

Nên gom về một chỗ, và có canary (`tests/python/test_windows_no_console.py`) canh rằng KHÔNG
lời gọi subprocess nào trong repo quên cờ này.
"""
from __future__ import annotations

import os
import subprocess

# 0 trên mọi hệ khác Windows, nên truyền vô điều kiện là an toàn.
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

# Cửa sổ console MỚI, tách hẳn khỏi tiến trình cha. Dùng cho việc CỐ Ý mở terminal cho người
# dùng nhìn (đăng nhập MCP) hoặc cho tiến trình sống lâu hơn server (trình cập nhật).
DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200


CREATE_NEW_CONSOLE = 0x00000010


def co_moi(cf: int, co_console: bool) -> int:
    """Cờ tạo tiến trình sau khi chỉnh (26/11/2026). Hàm thuần để kiểm thử trên mọi máy.

    Vì sao: `CREATE_NO_WINDOW` chỉ che được ĐỨA CON. Đứa con chạy không console, nên mọi chương trình dạng console mà NÓ sinh ra
    (Codex chạy lệnh bằng PowerShell, Claude Code chạy bash/cmd, npx của nguồn MCP chạy cmd rồi node...) lại được Windows cấp một
    cửa sổ đen MỚI: học viên thấy nháy đen khoảng 1 giây, lặp lại mỗi lần AI dùng công cụ. Server khởi động qua start-tisa.vbs đã có
    sẵn một console ẨN (cmd chạy với cửa sổ ẩn, python.exe dùng chung console đó). Cho con dùng CHUNG console ẩn ấy thì cả con lẫn
    cháu đều không có cửa sổ nào hiện ra.
    Chỉ bỏ cờ khi server có console. Không đụng tiến trình CỐ Ý mở cửa sổ (CREATE_NEW_CONSOLE) hay tách hẳn (DETACHED_PROCESS)."""
    cf = int(cf or 0)
    if co_console and (cf & CREATE_NO_WINDOW) and not (cf & (DETACHED_PROCESS | CREATE_NEW_CONSOLE)):
        return cf & ~CREATE_NO_WINDOW
    return cf


_DA_CAI = {"v": False}


def co_console() -> bool:
    """Tiến trình server có console (kể cả console ẩn) không. Chỉ Windows."""
    if os.name != "nt":
        return False
    try:
        import ctypes
        return bool(ctypes.windll.kernel32.GetConsoleWindow())
    except Exception:  # noqa: BLE001
        return False


def cai_dung_chung_console(co=None) -> bool:
    """Gắn một lần lúc khởi động (main.py): mọi subprocess.Popen (kể cả asyncio và claude-agent-sdk, vì chúng đi qua Popen) bỏ
    `CREATE_NO_WINDOW` khi server có console ẩn. True nếu đã gắn. Tắt bằng TISA_AN_CUA_SO_CU=1 (quay về cách cũ)."""
    if _DA_CAI["v"] or os.environ.get("TISA_AN_CUA_SO_CU") == "1":
        return False
    co = co_console() if co is None else bool(co)
    if not co:
        return False                          # server không có console (chạy kiểu khác): giữ CREATE_NO_WINDOW như cũ
    goc = subprocess.Popen.__init__

    def _init(self, *args, **kwargs):
        if "creationflags" in kwargs:
            kwargs["creationflags"] = co_moi(kwargs.get("creationflags") or 0, True)
        goc(self, *args, **kwargs)
    subprocess.Popen.__init__ = _init
    _DA_CAI["v"] = True
    return True


def no_window() -> int:
    """Cờ `creationflags` để lệnh con chạy câm trên Windows, 0 ở nơi khác."""
    return CREATE_NO_WINDOW if os.name == "nt" else 0


def kwargs_no_window() -> dict:
    """Dạng `**kwargs` cho `asyncio.create_subprocess_exec` (nó chuyển tiếp xuống subprocess).

    Trả dict RỖNG ngoài Windows: truyền `creationflags=0` vào asyncio trên POSIX là hợp lệ,
    nhưng để rỗng thì đọc log lỗi đỡ phải hỏi "cờ này ở đâu ra".
    """
    return {"creationflags": CREATE_NO_WINDOW} if os.name == "nt" else {}


def kill_tree(pid: int) -> bool:
    """Giết CẢ CÂY tiến trình mang gốc `pid`, không riêng cái launcher.

    Vì sao là hàm dùng chung chứ không phải method: có ít nhất hai chỗ spawn tiến trình con
    sống lâu và cả hai đều phải quét cây, nhưng chúng cầm hai LOẠI đối tượng khác nhau -
    `mcp_client.McpStdioSession` giữ một asyncio subprocess, còn `zalo_login` giữ một
    `subprocess.Popen`. Điểm chung duy nhất là con số pid, nên hàm nhận đúng con số đó.

    Vụ đã cắn (2026-08-15): npx trên Windows chạy qua `cmd.exe /c`, giết launcher thì tiến
    trình node cháu vẫn sống và vẫn giữ khoá trên thư mục home cô lập. Trên POSIX cũng vậy
    khi launcher chết trước mà nhóm vẫn còn thành viên.

    Trả True khi đã quét được cả nhóm; False thì người gọi tự `kill()` cái launcher như cũ.
    Hai chốt an toàn: không bao giờ đụng nhóm của chính server, và pid không phải leader
    (bản cũ chưa đặt session riêng) thì nhóm mang số đó không tồn tại nên rơi về False.
    """
    if os.name == "nt":
        try:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)],
                           capture_output=True, timeout=10, creationflags=no_window())
            return True
        except Exception:
            return False
    try:
        import signal
        if pid != os.getpgid(0):
            os.killpg(pid, signal.SIGKILL)
            return True
    except ProcessLookupError:
        pass   # cả nhóm đã chết sạch, hoặc child không phải leader
    except Exception:
        pass
    return False
