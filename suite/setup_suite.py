#!/usr/bin/env python3
"""setup_suite.py - nối ba phần thành một: TISA BOT, Bảng giao việc, 52 skill + 15 nhân sự, Claude.

TISA BOT tự chạy tệp này mỗi lần khởi động, nên chạy lại bao nhiêu lần cũng an toàn:
- Skill và hồ sơ nhân sự: bản mới của TISA đè lên bản cũ của TISA. Tệp học viên đã tự sửa thì GIỮ NGUYÊN.
- Webhook, nhóm, cấu hình bảng: chỉ tạo khi chưa có. Kết nối Claude: chỉ thêm, không xoá, không ghi đè.
Không bao giờ in mã bí mật ra màn hình hay nhật ký.
"""
import hashlib
import http.cookiejar
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

SUITE = Path(__file__).resolve().parent
ROOT = SUITE.parent
HOME = Path.home()
DATA = Path(os.environ.get("DOI_QUAN_HOME") or (HOME / ".doi-quan-ai"))
ENV = Path(os.environ.get("DOI_QUAN_ENV") or (HOME / ".config" / "doi-quan-ai" / ".env"))
MANIFEST = DATA / "manifest.json"
STATUS = DATA / "setup-status.json"
BOT = (os.environ.get("TISA_BOT_URL") or "http://127.0.0.1:7777").rstrip("/")
BOARD_PORT = os.environ.get("TISA_BOARD_PORT") or "7788"
BOARD = "http://127.0.0.1:" + BOARD_PORT
BRAIN = Path(os.environ.get("BRAINS_DIR") or (ROOT / "brains")) / "Brain Default"
OFFICE = "05 - Van Phong AI"
TEAM_NAME = "Đội Quân AI"
HOOK_NAME = "Đội Quân AI nhận việc"
HOOK_TEXT = ("Đây là việc chủ doanh nghiệp giao trên Bảng giao việc sau khi đăng nhập. Trường yeu_cau trong sự kiện là yêu cầu của chủ, "
             "làm như chủ giao trực tiếp. Tâm Tổng Quản làm theo skill dq-nhan-viec-tu-bang với mã việc job_id trong sự kiện: đọc bộ não, "
             "chia việc cho đúng nhân sự, cả đội làm thật, báo tiến độ, gắn ảnh và kết quả lên bảng bằng bang.py. "
             "Sự kiện có lan là sua thì chỉ sửa đúng các phần trong gop_y.")
BRAIN_NOTE_MARK = "<!-- tisa-suite -->"
BRAIN_NOTE = BRAIN_NOTE_MARK + """
## Bộ Não Thứ 2 và Đội Quân AI

Thư mục này chính là **Bộ Não Thứ 2** mà các lệnh `/ts-` tìm ở Bước 0: đọc `00-DOC-TRUOC.md`, `muc-luc.md`, `01-ho-so/`; lưu kết quả vào `04-ket-qua/`.
Không chạy `/ts-cai-dat-bo-nao` để tạo bộ não mới. Việc giao trên Bảng giao việc lưu ở `05 - Van Phong AI/03 - Ket qua/`.
Đội hình 15 nhân sự nằm ở `agents/dq-*.md`, kỹ năng nằm ở `skills/`.
"""

status = {"luc": time.strftime("%Y-%m-%d %H:%M:%S"), "buoc": {}}


def note(step, ok, detail=""):
    status["buoc"][step] = {"ok": bool(ok), "chi_tiet": str(detail)[:300]}
    print(("OK  " if ok else "!!  ") + step + (": " + str(detail) if detail else ""))


def posix(p):
    return Path(p).as_posix()


# ---------------------------------------------------------------- .env của bộ
def env_read():
    out = {}
    try:
        for line in ENV.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip()
    except OSError:
        pass
    return out


def env_set(**kw):
    cur = env_read()
    cur.update({k: str(v) for k, v in kw.items()})
    ENV.parent.mkdir(parents=True, exist_ok=True)
    ENV.write_text("".join("%s=%s\n" % kv for kv in cur.items()), encoding="utf-8")
    try:
        os.chmod(ENV, 0o600)
    except OSError:
        pass


# ---------------------------------------------------------------- chép tệp, giữ bản học viên đã sửa
def _hash(b):
    return hashlib.sha256(b).hexdigest()


def _render(data, path):
    """Tệp .md trong skill có chỗ điền đường dẫn thật của máy này."""
    if path.suffix != ".md":
        return data
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return (text.replace("{{BANG}}", posix(SUITE / "bridge" / "bang.py")).replace("{{PY}}", posix(sys.executable))
            .replace("{{BRAIN}}", posix(BRAIN))).encode("utf-8")


def _noi_bo_nao(data, f):
    """Lệnh /ts- mở trong Claude hay Codex ở ngoài thư mục não vẫn dùng đúng bộ não chung, không tạo não mới."""
    if f.name != "SKILL.md":
        return data
    t = data.decode("utf-8")
    cuoi = t.find("\n---", 3)
    if not t.startswith("---") or cuoi < 0:
        return data
    cuoi += 4
    return (t[:cuoi] + "\n\n> **Máy này đã cài TISA BOT:** Bộ Não Thứ 2 là thư mục `%s`, dùng chung cho TISA BOT và Đội Quân AI. "
            "Ở Bước 0, đọc và lưu tại đây; không tạo bộ não mới.\n" % posix(BRAIN) + t[cuoi:]).encode("utf-8")


def sync_tree(src, dst, man, scope, them=None):
    """Chép src vào dst. man nhớ băm bản đã chép lần trước: tệp đích khác băm đó là học viên đã sửa, không đè."""
    copied = kept = 0
    for f in sorted(p for p in src.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.name != ".DS_Store"):
        rel = f.relative_to(src)
        key = scope + "/" + rel.as_posix()
        target = dst / rel
        data = _render(f.read_bytes(), f)
        if them:
            data = them(data, f)
        new = _hash(data)
        if target.exists():
            cur = _hash(target.read_bytes())
            if cur == new:
                man[key] = new
                continue
            if man.get(key) != cur:
                kept += 1
                continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        man[key] = new
        copied += 1
    return copied, kept


def install_files():
    man = {}
    try:
        man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass
    BRAIN.mkdir(parents=True, exist_ok=True)
    c, k = sync_tree(SUITE / "skills", BRAIN / "skills", man, "skills")
    note("Skill vào bộ não", True, "%s tệp mới, giữ %s tệp đã sửa" % (c, k))
    c, k = sync_tree(SUITE / "agents", BRAIN / "agents", man, "agents")
    note("Hồ sơ 15 nhân sự", True, "%s tệp mới, giữ %s tệp đã sửa" % (c, k))

    # Khung bộ não: chỉ thêm tệp còn thiếu, không đụng tệp đã có của brain.
    tpl = SUITE / "brain-template"
    added = 0
    for f in sorted(p for p in tpl.rglob("*") if p.is_file() and p.name != ".DS_Store"):
        t = BRAIN / f.relative_to(tpl)
        if not t.exists():
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, t)
            added += 1
    for sub in ("01 - Ho so", "03 - Ket qua", "05 - Tai nguyen"):
        (BRAIN / OFFICE / sub).mkdir(parents=True, exist_ok=True)
    note("Khung Bộ Não Thứ 2", True, "thêm %s tệp" % added)

    guide = BRAIN / "CLAUDE.md"
    try:
        cur = guide.read_text(encoding="utf-8") if guide.exists() else ""
        if BRAIN_NOTE_MARK not in cur:
            guide.write_text(cur.rstrip() + "\n\n" + BRAIN_NOTE, encoding="utf-8")
    except OSError as e:
        note("Sổ tay bộ não", False, e)

    # 52 lệnh /ts- dùng được cả trong Claude Code, Claude Desktop (tab Code) và Codex.
    ts = SUITE / "skills"
    for name, base in (("Claude", HOME / ".claude" / "skills"), ("Codex", HOME / ".codex" / "skills")):
        if name == "Codex" and not (HOME / ".codex").exists():
            continue
        n = 0
        for d in sorted(ts.glob("ts-*")):
            c, _ = sync_tree(d, base / d.name, man, name.lower() + "/" + d.name, _noi_bo_nao)
            n += 1 if c else 0
        note("Lệnh /ts- cho " + name, True, "%s skill có thay đổi" % n)
    DATA.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=0), encoding="utf-8")


# ---------------------------------------------------------------- gọi TISA BOT và bảng
def bot_call(method, path, body=None):
    headers = {"Content-Type": "application/json", "User-Agent": "tisa-suite/1", "Origin": BOT}
    session = os.environ.get("TISA_SUITE_SESSION")
    if session:
        headers["Cookie"] = "tisa_session=" + session
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(BOT + path, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8") or "{}")


def board_call(method, path, body=None):
    token = env_read().get("BOARD_TOKEN", "")
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(BOARD + path, data=data, method=method, headers={
        "Authorization": "Bearer " + token, "Content-Type": "application/json", "User-Agent": "tisa-suite/1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8") or "{}")


def link_env():
    env_set(BOARD_URL=BOARD, TISA_URL=BOT, TISA_DIR=posix(ROOT / "server"), CHAT_BRAIN=posix(BRAIN))


def ensure_webhook():
    c = env_read()
    try:
        hooks = bot_call("GET", "/webhooks?brain=brain").get("hooks") or []
    except urllib.error.URLError as e:
        if c.get("TISA_HOOK_ID") and c.get("TISA_HOOK_TOKEN"):
            return note("Webhook nhận việc", True, "đã có")
        return note("Webhook nhận việc", False, "chưa gọi được TISA BOT: %s" % e)
    if c.get("TISA_HOOK_ID") and c.get("TISA_HOOK_TOKEN") and any(h.get("id") == c["TISA_HOOK_ID"] for h in hooks):
        return note("Webhook nhận việc", True, "đã có")
    try:
        same = [h for h in hooks if h.get("name") == HOOK_NAME]
        if same:
            # Có webhook mà mất mã trong .env: cấp lại mã mới cho đúng webhook đó.
            got = bot_call("POST", "/webhooks/rotate", {"brain": "brain", "id": same[0]["id"]})
            hook_id = same[0]["id"]
        else:
            got = bot_call("POST", "/webhooks", {"brain": "brain", "name": HOOK_NAME, "target": "task", "level": "full", "text": HOOK_TEXT})
            hook_id = (got.get("hook") or {}).get("id")
        if not (hook_id and got.get("token")):
            return note("Webhook nhận việc", False, "TISA BOT chưa trả mã webhook")
        env_set(TISA_HOOK_ID=hook_id, TISA_HOOK_TOKEN=got["token"])
        note("Webhook nhận việc", True, "đã tạo")
    except urllib.error.HTTPError as e:
        note("Webhook nhận việc", False, "TISA BOT trả %s" % e.code)


def ensure_team():
    if not os.environ.get("TISA_SUITE_SESSION") and env_read().get("TISA_HOOK_ID"):
        return note("Nhóm Đội Quân AI", True, "bỏ qua khi chạy tay")
    try:
        teams = bot_call("GET", "/teams?brain=brain").get("teams") or []
        if any(t.get("name") == TEAM_NAME for t in teams):
            return note("Nhóm Đội Quân AI", True, "đã có")
        members = sorted(p.stem for p in (BRAIN / "agents").glob("dq-*.md"))
        got = bot_call("POST", "/teams?brain=brain", {"name": TEAM_NAME, "members": members, "leader_slug": "dq-tam-tong-quan",
                                                       "description": "Đội 15 nhân sự, Tâm Tổng Quản chia việc.", "client_req_id": "tisa-suite-doi-quan"})
        note("Nhóm Đội Quân AI", bool(got.get("ok")), "%s thành viên" % len(members))
    except urllib.error.HTTPError as e:
        note("Nhóm Đội Quân AI", False, "TISA BOT trả %s: %s" % (e.code, e.read()[:200].decode("utf-8", "replace")))
    except urllib.error.URLError as e:
        note("Nhóm Đội Quân AI", False, e)


def ensure_board_kit():
    try:
        try:
            board_call("GET", "/api/db/settings/kit")
            return note("Cấu hình bảng", True, "giữ nguyên cấu hình đã có")
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
        kit = json.loads((SUITE / "board" / "kit-default.json").read_text(encoding="utf-8"))
        kit["brain"] = {"path": posix(BRAIN), "abs": posix(BRAIN), "office": OFFICE}
        kit["engine"] = "tisa"
        board_call("PUT", "/api/db/settings/kit", kit)
        note("Cấu hình bảng", True, "đã nối bộ não và TISA BOT")
    except (urllib.error.URLError, OSError, ValueError) as e:
        note("Cấu hình bảng", False, e)


def ensure_connectors():
    """Cài sẵn mọi kết nối của TISA Store để trang Kết nối sẵn có đầy đủ. Gói học viên đã gỡ thì không cài lại."""
    done_path = DATA / "ket-noi-da-cai.json"
    try:
        done = set(json.loads(done_path.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        done = set()
    try:
        packs = bot_call("GET", "/packs/store?refresh=1").get("packs") or []
    except (urllib.error.URLError, OSError, ValueError) as e:
        return note("Kết nối sẵn có", False, "chưa đọc được TISA Store: %s" % e)
    moi = loi = 0
    for a in packs:
        if a.get("kind") != "connector" or not (a.get("download") or {}).get("url") or a.get("installed") or a["id"] in done:
            continue
        try:
            got = bot_call("POST", "/packs/install-url", {"url": a["download"]["url"], "expect_sha256": a["download"].get("sha256", "")})
            res = bot_call("POST", "/packs/install", {"staging_id": got.get("staging_id"), "consent_sha256": got.get("sha256"), "enable": True,
                                                       "source": got.get("source") or {"kind": "zip"}, "brain": "brain"}) if got.get("ok") else got
            if res.get("ok"):
                moi += 1
                done.add(a["id"])
            else:
                loi += 1
                print("    chưa cài được %s: %s" % (a["id"], str(res.get("error"))[:160]))
        except (urllib.error.URLError, OSError, ValueError) as e:
            loi += 1
            print("    chưa cài được %s: %s" % (a["id"], e))
    done_path.write_text(json.dumps(sorted(done)), encoding="utf-8")
    note("Kết nối sẵn có", loi == 0, "cài thêm %s kết nối, lỗi %s" % (moi, loi))


# ---------------------------------------------------------------- kết nối Claude
def find_claude():
    try:
        p = json.loads((ROOT / "server" / "bin_paths.json").read_text(encoding="utf-8")).get("claude")
        if p and Path(p).exists():
            return p
    except (OSError, ValueError):
        pass
    return shutil.which("claude")


def desktop_config():
    if sys.platform == "darwin":
        return HOME / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    if os.name == "nt":
        return Path(os.environ.get("APPDATA") or (HOME / "AppData" / "Roaming")) / "Claude" / "claude_desktop_config.json"
    return HOME / ".config" / "Claude" / "claude_desktop_config.json"


def claude_user_servers():
    try:
        return json.loads((HOME / ".claude.json").read_text(encoding="utf-8")).get("mcpServers") or {}
    except (OSError, ValueError):
        return {}


def claude_add(claude, name, spec):
    try:
        r = subprocess.run([claude, "mcp", "add-json", "-s", "user", name, json.dumps(spec, ensure_ascii=False)],
                           capture_output=True, text=True, timeout=60,
                           creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        if r.returncode == 0:
            return True
    except (OSError, subprocess.SubprocessError):
        pass
    # Lệnh claude lỗi (hay gặp trên Windows do dấu ngoặc kép): tự thêm vào tệp cấu hình của Claude Code, giữ nguyên phần còn lại.
    p = HOME / ".claude.json"
    try:
        data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        data.setdefault("mcpServers", {}).setdefault(name, spec)
        tmp = p.with_name(p.name + ".tisa-tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, p)
        return True
    except (OSError, ValueError):
        return False


def connect_claude():
    spec = {"type": "stdio", "command": sys.executable, "args": [str(SUITE / "mcp_doi_quan.py")]}
    claude = find_claude()
    if not claude:
        return note("Nối Claude", False, "chưa thấy lệnh claude, lần mở sau làm tiếp")
    have = claude_user_servers()
    added = []
    if "doi-quan-ai" not in have and claude_add(claude, "doi-quan-ai", spec):
        added.append("doi-quan-ai")
    # Claude Desktop: thêm máy chủ giao việc, và đưa MCP đang có trên Desktop sang Claude Code.
    # TISA BOT chạy bằng Claude Code nên thấy ngay các MCP này (và connector trên tài khoản claude.ai).
    cfg = desktop_config()
    desk = {}
    if cfg.parent.exists():
        try:
            data = json.loads(cfg.read_text(encoding="utf-8")) if cfg.exists() else {}
            desk = data.get("mcpServers") or {}
            if "doi-quan-ai" not in desk:
                if cfg.exists():
                    bak = cfg.with_name(cfg.name + ".truoc-tisa")
                    if not bak.exists():
                        shutil.copy2(cfg, bak)
                data.setdefault("mcpServers", {})["doi-quan-ai"] = {"command": sys.executable, "args": [str(SUITE / "mcp_doi_quan.py")]}
                cfg.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                added.append("Claude Desktop")
        except (OSError, ValueError) as e:
            note("Cấu hình Claude Desktop", False, e)
    copied = []
    for name, s in desk.items():
        if name == "doi-quan-ai" or name in have or not isinstance(s, dict) or not (s.get("command") or s.get("url")):
            continue
        item = dict(s)
        item.setdefault("type", "stdio" if s.get("command") else "http")
        if claude_add(claude, name, item):
            copied.append(name)
    note("Nối Claude", True, "thêm: %s; MCP từ Desktop sang Claude Code: %s" % (", ".join(added) or "không", ", ".join(copied) or "không"))


def main():
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    DATA.mkdir(parents=True, exist_ok=True)
    install_files()
    link_env()
    ensure_board_kit()
    ensure_webhook()
    ensure_team()
    ensure_connectors()
    connect_claude()
    STATUS.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
