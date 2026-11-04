"""tisa_chat_sync.py - khung chat với nhân sự trên Đội Quân AI và trên TISA BOT là MỘT cuộc trò chuyện.

Bảng -> TISA BOT: tin chủ nhắn riêng một nhân sự chạy thẳng vào phiên chat `agent:<slug>` của cộng sự đó, đúng đường trang
Cộng sự dùng (WebSocket /ws), cùng model, cùng bộ nhớ. Chữ trả lời chảy dần về bảng trong lúc đang viết.
TISA BOT -> bảng: tin nhắn trong trang Cộng sự được chép sang khung chat của nhân sự đó trên bảng.
Chạy trong tiến trình TISA BOT. Lỗi một tin chỉ báo vào đúng tin đó, không dừng cả đồng bộ.
"""
import json
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from tisa_team_sync import board_roster

POLL_IN = 0.3       # giây, hỏi bảng có tin mới
POLL_BACK = 2.0     # giây, hỏi TISA BOT có tin mới
STREAM_EVERY = 0.4  # giây, nhịp đẩy chữ đang viết lên bảng
TURN_TIMEOUT = 900


def _iso(ts=None):
    return datetime.fromtimestamp(ts or time.time(), timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


class ChatSync:
    def __init__(self, brain, data_dir, env_path, bot_url, session, bang_path, py, stop, log=print):
        self.brain, self.env_path, self.bot, self.session = Path(brain), Path(env_path), bot_url.rstrip("/"), session
        self.bang, self.py, self.stop, self.log = str(bang_path), str(py), stop, log
        self.state_path = Path(data_dir) / "chat-sync.json"
        self.locks, self.busy, self.guard = {}, set(), threading.Lock()
        self.chat_at = {}
        self.seen = self._load()

    # ------------------------------------------------------------ gọi hai bên
    def _load(self):
        try:
            return json.loads(self.state_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}

    def _save(self):
        with self.guard:
            self.state_path.write_text(json.dumps(self.seen), encoding="utf-8")

    def cfg(self):
        out = {}
        try:
            for line in self.env_path.read_text(encoding="utf-8").splitlines():
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    out[k.strip()] = v.strip()
        except OSError:
            pass
        return out

    def board(self, method, path, body=None):
        c = self.cfg()
        data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
        req = urllib.request.Request(c["BOARD_URL"].rstrip("/") + path, data=data, method=method, headers={
            "Authorization": "Bearer " + c["BOARD_TOKEN"], "Content-Type": "application/json", "User-Agent": "tisa-chat-sync/1"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8") or "{}")

    def bot_call(self, path, form=None):
        data = urllib.parse.urlencode(form).encode() if form is not None else None
        req = urllib.request.Request(self.bot + path, data=data, headers={
            "Cookie": "tisa_session=" + self.session(), "Origin": self.bot, "User-Agent": "tisa-chat-sync/1"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8") or "{}")

    def roster(self):
        kit = self.board("GET", "/api/db/settings/kit")
        return board_roster(kit)

    def session_of(self, slug, create=False):
        ch = urllib.parse.quote("agent:" + slug)
        rows = self.bot_call("/sessions?brain=brain&limit=1&channel=" + ch).get("sessions") or []
        if rows:
            return rows[0].get("id") or rows[0].get("session_id")
        if not create:
            return ""
        got = self.bot_call("/sessions/new", {"brain": "brain", "channel": "agent:" + slug})
        return got.get("id") or got.get("session_id") or (got.get("session") or {}).get("id") or ""

    def messages(self, sid, limit=50):
        return self.bot_call("/sessions/%s/messages?limit=%d" % (urllib.parse.quote(sid), limit)).get("messages") or []

    # ------------------------------------------------------------ bảng -> TISA BOT
    def _text(self, m):
        text = str(m.get("text") or "").strip()
        imgs, files = m.get("images") or [], m.get("files") or []
        cmds = ['"%s" "%s" tai %s "<đường dẫn>/%s"' % (self.py, self.bang, x.get("id"), x.get("name") or x.get("id")) for x in (imgs + files)[:12]]
        return text + ("\n\nChủ gửi kèm %d ảnh, %d tệp. Tải về bằng:\n%s" % (len(imgs), len(files), "\n".join(cmds)) if cmds else "")

    def handle(self, m, slug):
        ma = m.get("to") or "tam"
        with self.guard:
            lock = self.locks.setdefault(slug, threading.Lock())
        with lock:
            self.busy.add(slug)
            reply_id, text = "", ""
            try:
                from websockets.sync.client import connect
                sid = self.session_of(slug, create=True)
                if not sid:
                    raise RuntimeError("không mở được phiên chat của cộng sự")
                url = self.bot.replace("http", "ws", 1) + "/ws"
                started, last_push = time.time(), 0.0
                with connect(url, additional_headers={"Cookie": "tisa_session=" + self.session(), "Origin": self.bot},
                             open_timeout=15, max_size=None) as ws:
                    ws.send(json.dumps({"message": self._text(m), "brain": "brain", "session_id": sid, "voice": False}, ensure_ascii=False))
                    final, err = None, ""
                    while time.time() - started < TURN_TIMEOUT:
                        o = json.loads(ws.recv(timeout=TURN_TIMEOUT))
                        if o.get("session_id") not in (None, sid):
                            continue
                        t = o.get("type")
                        if t == "stream":
                            text += str(o.get("content") or "")
                            if text.strip() and time.time() - last_push >= STREAM_EVERY:
                                last_push = time.time()
                                if reply_id:
                                    self.board("PATCH", "/api/db/messages/" + reply_id, {"text": text[:8000]})
                                else:
                                    reply_id = self.board("POST", "/api/v1/tin/tra-loi", {"replyTo": m["id"], "from": ma, "text": text[:8000], "done": False})["id"]
                        elif t == "response":
                            final = str(o.get("content") or "") or final
                        elif t == "error":
                            err = str(o.get("content") or o.get("message") or "lỗi")
                        elif t in ("turn_done", "stopped"):
                            break
                answer = (final or text).strip() or ("Em chưa trả lời được: " + err[:400] if err else "Em chưa trả lời được, anh nhắn lại giúp em nhé.")
                self.log("Chat bảng -> %s: %.1f giây, %d chữ" % (slug, time.time() - started, len(answer)))
            except Exception as e:      # noqa: BLE001 - báo vào đúng tin đó để chủ không chờ mãi
                answer = "Em chưa trả lời được: %s: %s" % (type(e).__name__, str(e)[:300])
                self.log("Chat lỗi %s: %s" % (slug, answer))
            try:
                if reply_id:
                    self.board("PATCH", "/api/db/messages/" + reply_id, {"text": answer[:8000]})
                    self.board("PATCH", "/api/db/messages/" + m["id"], {"status": "da-tra-loi", "answeredAt": _iso()})
                else:
                    self.board("POST", "/api/v1/tin/tra-loi", {"replyTo": m["id"], "from": ma, "text": answer[:8000]})
                # Tin vừa đi qua đường này đã có trên bảng: đánh dấu đã thấy để không chép lại.
                sid = self.session_of(slug)
                ids = [x.get("id") for x in self.messages(sid, 10) if isinstance(x.get("id"), int)] if sid else []
                if ids:
                    self.seen[sid] = max(ids + [self.seen.get(sid, 0)])
                    self._save()
            finally:
                self.busy.discard(slug)

    def loop_in(self):
        ver = None
        while not self.stop.is_set():
            try:
                q = "/api/v1/tin/hang-doi?tisa=0" + ("&since=%s" % ver if ver is not None else "")
                got = self.board("GET", q)
                tin = [m for m in got.get("tin") or [] if m.get("dm")]
                if tin:
                    r = self.roster()
                    for m in tin:
                        self.board("POST", "/api/v1/tin/%s/ack" % m["id"], {})
                        a = r.get(m.get("to")) or r.get("tam") or {}
                        threading.Thread(target=self.handle, args=(m, a.get("slug") or "dq-tam-tong-quan"), daemon=True).start()
                ver = got.get("ver") if not tin else None
            except Exception as e:      # noqa: BLE001
                ver = None
                self.log("Chat: chưa đọc được bảng: %s" % e)
                self.stop.wait(3)
            self.stop.wait(POLL_IN)

    # ------------------------------------------------------------ TISA BOT -> bảng
    def _copy(self, ma, sid):
        last = self.seen.get(sid, 0)
        rows = [x for x in self.messages(sid) if isinstance(x.get("id"), int) and x["id"] > last and x.get("role") in ("user", "assistant")]
        for x in sorted(rows, key=lambda y: y["id"]):
            text = x.get("content")
            text = text if isinstance(text, str) else json.dumps(text, ensure_ascii=False)
            if not text.strip():
                continue
            ts = x.get("ts") or x.get("created_at") or x.get("time")
            when = _iso(float(ts)) if isinstance(ts, (int, float)) else _iso()
            doc = {"dm": ma, "jobId": "", "part": 0, "text": text[:8000], "created": when, "nguon": "tisa-bot"}
            if x["role"] == "user":
                doc.update(kind="chat", to=ma, **{"from": "chu"}, status="da-tra-loi")
            else:
                doc.update(kind="tra-loi", to="chu", **{"from": ma}, status="tra-loi")
            self.board("POST", "/api/db/messages", doc)
        if rows:
            self.seen[sid] = max(y["id"] for y in rows)
            self._save()

    def loop_back(self):
        while not self.stop.is_set():
            try:
                rows = self.bot_call("/agents?brain=brain").get("agents") or []
                changed = {a["slug"]: a.get("last_chat_at") for a in rows if a.get("last_chat_at") and a.get("last_chat_at") != self.chat_at.get(a["slug"])}
                if changed:
                    by_slug = {a["slug"]: ma for ma, a in self.roster().items()}
                    for slug, at in changed.items():
                        if slug in self.busy:
                            continue    # đang trả lời tin từ bảng, vòng sau mới xét
                        ma = by_slug.get(slug)
                        sid = self.session_of(slug) if ma else ""
                        if sid:
                            self._copy(ma, sid)
                        self.chat_at[slug] = at
            except urllib.error.HTTPError as e:
                self.log("Chat: TISA BOT trả %s" % e.code)
                self.stop.wait(5)
            except Exception as e:      # noqa: BLE001
                self.log("Chat: chưa chép được tin: %s" % e)
                self.stop.wait(5)
            self.stop.wait(POLL_BACK)

    def start(self):
        for fn in (self.loop_in, self.loop_back):
            threading.Thread(target=fn, name="tisa-" + fn.__name__, daemon=True).start()
