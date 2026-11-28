"""tisa_suite.py - phần tự cài của TISA BOT chạy mỗi lần server khởi động.

V3.81 (chủ 28/11/2026): bỏ Đội Quân AI, học viên chỉ cài và dùng đúng một TISA BOT. Không còn bật Bảng giao việc
(Node, cổng 7788), cầu nối, đồng bộ đội hình, đồng bộ chat. Lần đầu và sau mỗi bản cập nhật, suite/setup_suite.py chỉ làm
phần của TISA BOT: lệnh /ts- cho Claude Code và Codex, khung Bộ Não Thứ 2, kết nối sẵn có, lối tắt "TISA BOT - Kết quả";
và trên máy đã cài bản có Đội Quân thì gỡ máy chủ MCP doi-quan-ai mà TISA từng gắn vào Claude.

Bảng và cầu nối của lần chạy trước (máy cập nhật từ bản cũ) được dừng, chỉ khi đúng là tiến trình của Đội Quân.
Dữ liệu cũ trong ~/.doi-quan-ai giữ nguyên. Phần này hỏng không được làm hỏng TISA BOT: lỗi chỉ ghi vào ~/.doi-quan-ai/logs/.
TISA_SUITE_OFF=1 tắt hẳn phần tự cài.
"""
import os
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUITE = ROOT / "suite"
DATA = Path(os.getenv("DOI_QUAN_HOME") or (Path.home() / ".doi-quan-ai"))
LOGS = DATA / "logs"

_stop = threading.Event()
# Tiến trình cũ của Đội Quân: tên tệp pid -> chữ phải có trong dòng lệnh thì mới dừng (pid cũ có thể đã thuộc chương trình khác).
_CU = {"board": "board-server.mjs", "bridge": "bang.py"}


def _log(msg):
    try:
        LOGS.mkdir(parents=True, exist_ok=True)
        with open(LOGS / "suite.log", "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + str(msg) + "\n")
    except OSError:
        pass


def _flags():
    return subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def _dong_lenh(pid):
    try:
        if os.name == "nt":
            r = subprocess.run(["powershell", "-NoProfile", "-Command",
                                "(Get-CimInstance Win32_Process -Filter 'ProcessId=%d').CommandLine" % pid],
                               capture_output=True, text=True, timeout=20, creationflags=_flags())
        else:
            r = subprocess.run(["ps", "-p", str(pid), "-o", "command="], capture_output=True, text=True, timeout=10)
        return r.stdout or ""
    except (OSError, subprocess.SubprocessError):
        return ""


def _dung_doi_quan_cu():
    """Máy cập nhật từ bản có Đội Quân: bảng và cầu nối cũ có thể còn chạy. Dừng đúng chúng, rồi bỏ tệp pid."""
    for ten, dau_hieu in _CU.items():
        pf = DATA / (ten + ".pid")
        try:
            pid = int(pf.read_text().strip())
        except (OSError, ValueError):
            continue
        if pid > 1 and dau_hieu in _dong_lenh(pid):
            try:
                if os.name == "nt":
                    subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, creationflags=_flags())
                else:
                    os.kill(pid, 15)
                _log("Đã dừng %s cũ của Đội Quân AI (pid %s)" % (ten, pid))
            except OSError:
                pass
        try:
            pf.unlink()
        except OSError:
            pass


def _wait_http(url, seconds):
    end = time.time() + seconds
    while time.time() < end and not _stop.is_set():
        try:
            with urllib.request.urlopen(url, timeout=3) as r:
                if r.status == 200:
                    return True
        except OSError:
            pass
        _stop.wait(2)
    return False


def _run():
    DATA.mkdir(parents=True, exist_ok=True)
    _dung_doi_quan_cu()
    port = os.getenv("TISA_PORT") or os.getenv("PORT") or "7777"
    env = dict(os.environ, DOI_QUAN_HOME=str(DATA), TISA_BOT_ROOT=str(ROOT), TISA_BOT_URL="http://127.0.0.1:%s" % port,
               PYTHONIOENCODING="utf-8")
    # Chờ TISA BOT mở cổng: bước cài kết nối sẵn có gọi chính TISA BOT.
    _wait_http(env["TISA_BOT_URL"] + "/health", 120)
    token = ""
    cfgmod = None
    try:
        import config as cfgmod
        token = cfgmod.new_session()
    except Exception as e:      # noqa: BLE001
        _log("Không tạo được phiên nội bộ: %s" % e)
    try:
        r = subprocess.run([sys.executable, str(SUITE / "setup_suite.py")], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=600, cwd=str(SUITE),
                           env=dict(env, TISA_SUITE_SESSION=token), creationflags=_flags())
        _log("setup_suite xong (mã %s)\n%s%s" % (r.returncode, r.stdout[-3000:], r.stderr[-3000:]))
    except (OSError, subprocess.SubprocessError) as e:
        _log("setup_suite lỗi: %s" % e)
    finally:
        if token and cfgmod is not None:
            try:
                cfgmod.drop_session(token)
            except Exception:   # noqa: BLE001
                pass


def stop():
    _stop.set()


def start():
    if os.getenv("TISA_SUITE_OFF"):
        return
    threading.Thread(target=_run, name="tisa-suite", daemon=True).start()
