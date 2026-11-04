#!/usr/bin/env python3
"""smoke_test.py - kiểm tra bộ TISA sau khi cài, chạy được trên cả Windows và Mac (chỉ dùng thư viện chuẩn).

    python suite/smoke_test.py

GitHub Actions chạy tệp này trên máy sạch sau khi cài. Trên máy đã cài cũng chạy được khi cần soát.
Không cần đăng nhập Claude: kiểm tra đủ hai chiều giữa bảng và TISA BOT, trừ phần Claude tự làm việc.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
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
ENV = HOME / ".config" / "doi-quan-ai" / ".env"
BRAIN = Path(os.environ.get("BRAINS_DIR") or (ROOT / "brains")) / "Brain Default"
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


st = wait(status_file, 300)
check("Bộ cài đã chạy xong", bool(st))
if not st:
    show_log()
    sys.exit(1)
for step, v in st["buoc"].items():
    check(step, v.get("ok"), v.get("chi_tiet", ""))

check("52 kỹ năng trong bộ não", len(list((BRAIN / "skills").glob("ts-*"))) == 52)
check("15 nhân sự", len(list((BRAIN / "agents").glob("dq-*.md"))) == 15)
check("Lệnh /ts- cho Claude", len(list((HOME / ".claude" / "skills").glob("ts-*"))) == 52)

cfg = {}
for line in ENV.read_text(encoding="utf-8").splitlines():
    if "=" in line:
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip()
for k in ("BOARD_URL", "BOARD_TOKEN", "JAVIS_URL", "JAVIS_HOOK_ID", "JAVIS_HOOK_TOKEN"):
    check("Có " + k, bool(cfg.get(k)))


def board(path):
    req = urllib.request.Request(cfg["BOARD_URL"] + path, headers={"Authorization": "Bearer " + cfg["BOARD_TOKEN"]})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


with urllib.request.urlopen(cfg["BOARD_URL"] + "/voice/tam-hello.mp3", timeout=15) as r:
    check("Giọng đọc của bảng", r.status == 200)

# Giao việc đúng đường Claude dùng: công cụ MCP, có chữ tiếng Việt để bắt lỗi mã hóa trên Windows.
TASK = "Việc thử sau khi cài: viết một câu chào tiếng Việt có dấu"
p = subprocess.run([sys.executable, str(SUITE / "mcp_doi_quan.py")], capture_output=True, timeout=60, input="\n".join(json.dumps(m, ensure_ascii=False) for m in [
    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "thu", "version": "1"}}},
    {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
    {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "giao_viec", "arguments": {"yeu_cau": TASK, "tieu_de": "Việc thử sau khi cài"}}},
]).encode("utf-8") + b"\n")
replies = [json.loads(x) for x in p.stdout.decode("utf-8").splitlines() if x.strip()]
check("Công cụ MCP cho Claude", len(replies) == 3 and len(replies[1]["result"]["tools"]) == 4, p.stderr.decode("utf-8", "replace")[-300:])
job = json.loads(replies[2]["result"]["content"][0]["text"])["job_id"]
doc = board("/api/db/results/" + job)
check("Việc lên bảng đúng chữ tiếng Việt", doc.get("task") == TASK)


def received():
    d = board("/api/db/results/" + job)
    return d if d.get("status") != "hang-doi" else None


got = wait(received, 90)
check("TISA BOT nhận việc qua cầu nối", bool(got), (got or {}).get("summary", ""))

r = subprocess.run([sys.executable, str(SUITE / "bridge" / "bang.py"), "kiem-tra"], capture_output=True, timeout=60)
check("Cầu nối kiểm tra kết nối", r.returncode == 0 and "TISA BOT: đang chạy".encode("utf-8") in r.stdout, r.stdout.decode("utf-8", "replace")[-300:])

# Chiều ngược lại: nhân sự trên TISA BOT báo về bảng, đúng các lệnh ghi trong skill dq-bao-cao-bang.
def bang(*args):
    r = subprocess.run([sys.executable, str(SUITE / "bridge" / "bang.py"), *args], capture_output=True, timeout=120)
    if r.returncode:
        print("   ", r.stderr.decode("utf-8", "replace")[-300:])
    return r.returncode == 0


def api(method, path, body):
    req = urllib.request.Request(cfg["BOARD_URL"] + path, data=json.dumps(body, ensure_ascii=False).encode("utf-8"), method=method,
                                 headers={"Authorization": "Bearer " + cfg["BOARD_TOKEN"], "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    (tmp / "ke-hoach.json").write_text(json.dumps({"summary": "Kế hoạch thử", "plan": [
        {"agent": "linh", "viec": "Viết một bài", "dau_ra": "Một bài", "deps": [], "state": "wait"},
        {"agent": "hoa", "viec": "Làm một ảnh", "dau_ra": "Một ảnh", "deps": [1], "state": "wait"}]}, ensure_ascii=False), encoding="utf-8")
    OUT = "Bài viết thử có dấu tiếng Việt"
    (tmp / "ket-qua.md").write_text(OUT, encoding="utf-8")
    (tmp / "anh.png").write_bytes((ROOT / "dashboard" / "favicon.png").read_bytes())
    check("Đăng kế hoạch lên bảng", bang("ke-hoach", job, str(tmp / "ke-hoach.json")))
    check("Báo tiến độ lên bảng", bang("phan", job, "1", "--state", "run", "--pct", "40"))
    check("Gửi kết quả lên bảng", bang("phan", job, "1", "--state", "done", "--out-file", str(tmp / "ket-qua.md")))
    check("Gửi ảnh lên bảng", bang("anh", job, str(tmp / "anh.png"), "--title", "Ảnh thử"))
    check("Gửi link lên bảng", bang("link", job, "--title", "Báo cáo", "--url", "https://example.com/bao-cao", "--kind", "doc"))
    check("Báo chờ duyệt", bang("xong", job, "--status", "cho-duyet", "--summary", "Đã xong phần thử"))
doc = board("/api/db/results/" + job)
check("Bảng hiện đúng trạng thái", doc.get("status") == "cho-duyet", doc.get("status"))
check("Bảng hiện đúng kết quả tiếng Việt", doc["plan"][0].get("state") == "done" and str(doc["plan"][0].get("out", "")).strip() == OUT)
links = doc.get("links") or []
check("Bảng có ảnh và link", len(links) == 2, [x.get("title") for x in links])
req = urllib.request.Request(cfg["BOARD_URL"] + links[0]["url"], headers={"Authorization": "Bearer " + cfg["BOARD_TOKEN"]})
with urllib.request.urlopen(req, timeout=15) as r:
    check("Mở lại được ảnh đã gửi", r.read() == (ROOT / "dashboard" / "favicon.png").read_bytes())

# Tin chủ nhắn trên bảng phải tới TISA BOT.
mid = api("POST", "/api/db/messages", {"from": "chu", "status": "moi", "to": "linh", "text": "Hỏi thử có dấu", "jobId": job, "part": 1, "kind": "hoi",
                                       "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})["id"]
sent = wait(lambda: (lambda d: d if d.get("status") != "moi" else None)(board("/api/db/messages/" + mid)), 60)
check("Tin nhắn từ bảng tới TISA BOT", bool(sent), (sent or {}).get("status", ""))

# TISA BOT báo tình trạng và kết nối lên bảng (mục Kết nối, chấm xanh ở chân bảng).
check("Đồng bộ kết nối lên bảng", bang("dong-bo"))
check("Bảng thấy thông tin TISA BOT", bool(board("/api/db/settings/tisabot").get("checked")))
check("Bảng báo TISA BOT đang nối", (board("/api/status").get("javis") or {}).get("online") is True)

# Chỉ đúng trên máy vừa cài, chưa đổi mật khẩu.
if "--mac-dinh" in sys.argv:
    import urllib.parse
    form = urllib.parse.urlencode({"username": "admin", "password": "123456"}).encode()
    with urllib.request.urlopen(urllib.request.Request(cfg["JAVIS_URL"] + "/auth/login", data=form), timeout=20) as r:
        check("Đăng nhập admin / 123456", json.loads(r.read().decode("utf-8")).get("ok") is True)
    with urllib.request.urlopen(cfg["JAVIS_URL"] + "/auth/status", timeout=20) as r:
        check("TISA BOT yêu cầu đăng nhập", json.loads(r.read().decode("utf-8")).get("auth_required") is True)

if failed:
    print("\nCÓ %s LỖI: %s" % (len(failed), ", ".join(failed)))
    show_log()
    sys.exit(1)
print("\nBộ TISA chạy tốt.")
