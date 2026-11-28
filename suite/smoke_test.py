#!/usr/bin/env python3
"""smoke_test.py - kiểm tra TISA BOT sau khi cài, chạy được trên cả Windows và Mac (chỉ dùng thư viện chuẩn).

    python suite/smoke_test.py [--mac-dinh]

GitHub Actions chạy tệp này trên máy sạch sau khi cài. Trên máy đã cài cũng chạy được khi cần soát.
V3.81 (chủ 28/11/2026): bỏ Đội Quân AI. Bài thử kiểm tra phần tự cài của TISA BOT (lệnh /ts-, khung Bộ Não, kết nối
sẵn có) và kiểm tra KHÔNG còn bảng Đội Quân (cổng 7788), MCP doi-quan-ai, 15 nhân sự.
--mac-dinh: chỉ trên máy vừa cài, đăng nhập bằng mật khẩu mặc định để soát thêm phần cần đăng nhập.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

SUITE = Path(__file__).resolve().parent
ROOT = SUITE.parent
HOME = Path.home()
DATA = Path(os.environ.get("DOI_QUAN_HOME") or (HOME / ".doi-quan-ai"))
BRAIN = Path(os.environ.get("BRAINS_DIR") or (ROOT / "brains")) / "Brain Default"
TISA_URL = "http://127.0.0.1:%s" % (os.environ.get("TISA_PORT") or "7777")
SO_TS = len([p for p in (SUITE / "skills").glob("ts-*") if p.is_dir()])
failed = []


def check(name, ok, detail=""):
    print(("OK    " if ok else "LOI   ") + name + (": " + str(detail) if detail else ""))
    if not ok:
        failed.append(name)


def wait(fn, seconds, every=3):
    end = time.time() + seconds
    while time.time() < end:
        got = fn()
        if got:
            return got
        time.sleep(every)
    return None


def status_file():
    try:
        return json.loads((DATA / "setup-status.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def show_log():
    try:
        print((DATA / "logs" / "suite.log").read_text(encoding="utf-8", errors="replace")[-3000:])
    except OSError:
        pass


def tra_loi(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.status == 200
    except OSError:
        return False


check("TISA BOT trả lời /health", bool(wait(lambda: tra_loi(TISA_URL + "/health"), 180)))
st = wait(status_file, 300)
check("Phần tự cài đã chạy xong", bool(st))
if not st:
    show_log()
    sys.exit(1)
for step, v in st["buoc"].items():
    check(step, v.get("ok"), v.get("chi_tiet", ""))

check("%s lệnh /ts- trong bộ não" % SO_TS, len(list((BRAIN / "skills").glob("ts-*"))) >= SO_TS)
check("Lệnh /ts- cho Claude Code", len(list((HOME / ".claude" / "skills").glob("ts-*"))) >= SO_TS)
check("Bộ não không còn chữ mẫu", not [p.name for p in list(BRAIN.glob("*.md")) + list((BRAIN / "01-ho-so").glob("*.md")) + list((BRAIN / "06-mau").glob("*.md")) if "{{TEN}}" in p.read_text(encoding="utf-8") or "{{NGAY}}" in p.read_text(encoding="utf-8")])
huong_dan = (BRAIN / "CLAUDE.md").read_text(encoding="utf-8") if (BRAIN / "CLAUDE.md").exists() else ""
check("Sổ tay bộ não không còn nhắc Đội Quân AI", "<!-- tisa-suite -->" in huong_dan and "Đội Quân" not in huong_dan)

# Không còn Đội Quân AI.
check("Không bật bảng Đội Quân (cổng 7788)", not tra_loi("http://127.0.0.1:%s/health" % (os.environ.get("TISA_BOARD_PORT") or "7788")))
try:
    mcp = json.loads((HOME / ".claude.json").read_text(encoding="utf-8")).get("mcpServers") or {}
except (OSError, ValueError):
    mcp = {}
check("Claude Code không có MCP doi-quan-ai", "doi-quan-ai" not in mcp)
if "--mac-dinh" in sys.argv:
    check("Máy mới không có 15 nhân sự Đội Quân", not list((BRAIN / "agents").glob("dq-*.md")))
    sys.path.insert(0, str(SUITE))
    import setup_suite
    du = sorted(p.name for p in (BRAIN / "skills").glob("dq-*") if p.name not in setup_suite.KY_NANG_TISA)
    check("Máy mới chỉ có skill dq- của TISA BOT", not du, du[:5])
    thieu = [n for n in setup_suite.KY_NANG_TISA if not (BRAIN / "skills" / n / "SKILL.md").exists()]
    check("Đủ skill công cụ của TISA BOT", not thieu, thieu)
    check("Có cộng sự Đạt Đấu Nối và Quản Trị WEB", all((BRAIN / "agents" / n).exists() for n in ("tisa-dau-noi.md", "tisa-quan-tri-web.md")))

# Chỉ chạy trên máy vừa cài: dùng mật khẩu mặc định.
if "--mac-dinh" in sys.argv:
    login = urllib.request.urlopen(urllib.request.Request(TISA_URL + "/auth/login", data=urllib.parse.urlencode({"username": "admin", "password": "123456"}).encode()), timeout=20)
    check("Đăng nhập admin / 123456", json.loads(login.read().decode("utf-8")).get("ok") is True)
    cookie = login.headers.get("Set-Cookie", "").split(";")[0]
    with urllib.request.urlopen(TISA_URL + "/auth/status", timeout=20) as r:
        check("TISA BOT yêu cầu đăng nhập", json.loads(r.read().decode("utf-8")).get("auth_required") is True)

    def bot(path):
        req = urllib.request.Request(TISA_URL + path, headers={"Cookie": cookie, "Origin": TISA_URL})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8") or "{}")

    check("Không có báo bản mới", bot("/version").get("update_available") is False)
    packs = bot("/packs/store").get("packs") or []
    check("TISA Store có danh mục", bool(packs), len(packs))
    conn = [a for a in packs if a.get("kind") == "connector"]
    check("TISA Store đủ kết nối", len(conn) >= 44, len(conn))
    check("Kết nối được cài sẵn", all(a.get("installed") or not (a.get("download") or {}).get("url") for a in conn), [a["id"] for a in conn if not a.get("installed") and (a.get("download") or {}).get("url")][:5])

if failed:
    print("\nCÓ %s LỖI: %s" % (len(failed), ", ".join(failed)))
    show_log()
    sys.exit(1)
print("\nTISA BOT chạy tốt.")
