"""tisa_suite.py - bật Bảng giao việc Đội Quân AI và cầu nối cùng lúc với TISA BOT.

Học viên chỉ cài và mở một app: server khởi động thì bảng (Node, cổng 7788, chỉ nghe trên máy này)
và cầu nối (bang.py cau-noi) tự chạy, hỏng thì tự bật lại, tắt server thì tắt theo. Lần đầu và sau
mỗi bản cập nhật, suite/setup_suite.py cài skill, đội hình, webhook, nhóm và kết nối Claude.

Phần bổ sung hỏng không được làm hỏng TISA BOT: mọi lỗi chỉ ghi vào ~/.doi-quan-ai/logs/.
"""
import atexit
import os
import re
import shutil
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
BOARD_PORT = int(os.getenv("TISA_BOARD_PORT") or 7788)
NODE_MIN = (22, 13)

_procs = {}
_stop = threading.Event()


def _log(msg):
    try:
        LOGS.mkdir(parents=True, exist_ok=True)
        with open(LOGS / "suite.log", "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + str(msg) + "\n")
    except OSError:
        pass


def _flags():
    return subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def _node_ok(path):
    try:
        out = subprocess.run([path, "-v"], capture_output=True, text=True, timeout=15,
                             creationflags=_flags()).stdout
    except (OSError, subprocess.SubprocessError):
        return False
    m = re.match(r"v(\d+)\.(\d+)", out.strip())
    return bool(m) and (int(m.group(1)), int(m.group(2))) >= NODE_MIN


def find_node():
    """Node >= 22.13 (có sẵn node:sqlite). Bộ cài TISA BOT cài Node 22 trở lên."""
    tries = [shutil.which("node")]
    home = Path.home()
    tries += [str(home / ".tisa" / "node" / "bin" / "node"), "/opt/homebrew/bin/node", "/usr/local/bin/node",
              str(Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "nodejs" / "node.exe")]
    for t in tries:
        if t and Path(t).exists() and _node_ok(t):
            return t
    return None


def _kill_old(name):
    """Tiến trình của lần chạy trước còn sống (server bị tắt đột ngột, vừa cập nhật) thì dừng để chạy mã mới."""
    pf = DATA / (name + ".pid")
    try:
        pid = int(pf.read_text().strip())
    except (OSError, ValueError):
        return
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, creationflags=_flags())
        else:
            os.kill(pid, 15)
            time.sleep(0.5)
    except OSError:
        pass
    try:
        pf.unlink()
    except OSError:
        pass


def _supervise(name, cmd, env):
    """Chạy cmd, chết thì bật lại (chờ tăng dần, tối đa 60 giây)."""
    wait = 2
    _kill_old(name)
    while not _stop.is_set():
        started = time.time()
        try:
            LOGS.mkdir(parents=True, exist_ok=True)
            with open(LOGS / (name + ".log"), "ab") as out:
                p = subprocess.Popen(cmd, stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                     cwd=str(SUITE), env=env, creationflags=_flags())
            _procs[name] = p
            (DATA / (name + ".pid")).write_text(str(p.pid))
            _log("Đã bật %s (pid %s)" % (name, p.pid))
            p.wait()
        except OSError as e:
            _log("Không bật được %s: %s" % (name, e))
        if _stop.is_set():
            return
        wait = 2 if time.time() - started > 120 else min(wait * 2, 60)
        _log("%s dừng, bật lại sau %ss" % (name, wait))
        _stop.wait(wait)


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
    env = dict(os.environ, DOI_QUAN_HOME=str(DATA), TISA_BOARD_PORT=str(BOARD_PORT), TISA_BOT_ROOT=str(ROOT),
               PYTHONIOENCODING="utf-8")
    port = os.getenv("TISA_PORT") or os.getenv("PORT") or "7777"
    env["TISA_BOT_URL"] = "http://127.0.0.1:%s" % port

    node = find_node()
    if not node:
        _log("Thiếu Node 22.13 trở lên: Bảng giao việc chưa bật. Mở Cập nhật hoặc cài Node LTS tại nodejs.org.")
    else:
        threading.Thread(target=_supervise, args=("board", [node, str(SUITE / "board" / "board-server.mjs")], env),
                         daemon=True).start()
        if not _wait_http("http://127.0.0.1:%s/health" % BOARD_PORT, 60):
            _log("Bảng chưa trả lời /health sau 60 giây, xem logs/board.log")

    # Chờ TISA BOT mở cổng rồi mới cài webhook và nhóm: các bước đó gọi chính TISA BOT.
    _wait_http(env["TISA_BOT_URL"] + "/health", 120)
    token = ""
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
        if token:
            try:
                cfgmod.drop_session(token)
            except Exception:   # noqa: BLE001
                pass

    if node:
        threading.Thread(target=_supervise, args=("bridge", [sys.executable, str(SUITE / "bridge" / "bang.py"), "cau-noi"], env),
                         daemon=True).start()
        threading.Thread(target=_team_sync_loop, args=(env["TISA_BOT_URL"],), name="tisa-team-sync", daemon=True).start()
        _start_chat_sync(env["TISA_BOT_URL"])


def _start_chat_sync(bot_url):
    """Khung chat với nhân sự trên bảng và trên TISA BOT là một cuộc trò chuyện."""
    try:
        import config as cfgmod
        import tisa_chat_sync
        tok = {"v": cfgmod.new_session()}

        def session():
            # Đổi mật khẩu thì mọi phiên cũ hết hiệu lực: tự lấy phiên mới.
            if not cfgmod.valid_session(tok["v"]):
                tok["v"] = cfgmod.new_session()
            return tok["v"]

        brain = Path(os.getenv("BRAINS_DIR") or (ROOT / "brains")) / "Brain Default"
        env_path = Path(os.getenv("DOI_QUAN_ENV") or (Path.home() / ".config" / "doi-quan-ai" / ".env"))
        tisa_chat_sync.ChatSync(brain, DATA, env_path, bot_url, session, SUITE / "bridge" / "bang.py", sys.executable, _stop, log=_log).start()
    except Exception as e:      # noqa: BLE001
        _log("Không bật được đồng bộ chat: %s: %s" % (type(e).__name__, e))


def _chat_bang_ngoai():
    port = os.getenv("TISA_PORT") or os.getenv("PORT") or "7777"
    bot_url = "http://127.0.0.1:%s" % port
    _wait_http(bot_url + "/health", 120)
    DATA.mkdir(parents=True, exist_ok=True)
    _start_chat_sync(bot_url)
    # Cộng sự tạo ở ô Cộng sự phải hiện ở Văn phòng, Đội ngũ, Cài đặt đội của bảng đặt ngoài (V2.78).
    threading.Thread(target=_team_sync_loop, args=(bot_url, True), name="tisa-team-sync", daemon=True).start()


def _team_sync_loop(bot_url, ngoai=False):
    """Đội Quân AI chỉ là giao diện: nhân sự, phòng ban, skill luôn khớp với cộng sự trong TISA BOT.
    ngoai=True: bảng đặt ở nơi khác (Cloudflare), chỉ đồng bộ đội hình và chỉ cộng sự tạo từ lúc bật."""
    import config as cfgmod
    import tisa_team_sync

    tokens = []

    def session():
        if not tokens:
            tokens.append(cfgmod.new_session())
        return tokens[0]

    brain = Path(os.getenv("BRAINS_DIR") or (ROOT / "brains")) / "Brain Default"
    env_path = Path(os.getenv("DOI_QUAN_ENV") or (Path.home() / ".config" / "doi-quan-ai" / ".env"))
    sync = tisa_team_sync.Sync(brain, DATA, env_path, bot_url, session=session, log=_log, chi_tu_nay=ngoai, ket_noi=not ngoai)
    while not _stop.is_set():
        try:
            sync.run_once()
        except Exception as e:      # noqa: BLE001 - lỗi một vòng không được dừng cả đồng bộ
            _log("Đồng bộ đội hình lỗi: %s: %s" % (type(e).__name__, e))
        while tokens:
            try:
                cfgmod.drop_session(tokens.pop())
            except Exception:       # noqa: BLE001
                pass
        _stop.wait(10)


def stop():
    _stop.set()
    for p in list(_procs.values()):
        try:
            p.terminate()
        except OSError:
            pass


def start():
    # Bảng đặt ở nơi khác (Cloudflare): không bật bảng và không cài lại gì trên máy, chỉ nối khung chat.
    if os.getenv("TISA_BANG_NGOAI"):
        atexit.register(stop)
        threading.Thread(target=_chat_bang_ngoai, name="tisa-chat-ngoai", daemon=True).start()
        return
    if os.getenv("TISA_SUITE_OFF"):
        return
    atexit.register(stop)
    threading.Thread(target=_run, name="tisa-suite", daemon=True).start()
