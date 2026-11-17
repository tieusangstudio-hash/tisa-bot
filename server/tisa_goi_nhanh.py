"""Cuộc gọi nhanh hơn và đo được (chủ báo 17/11/2026: bấm gọi, đồng hồ chạy tới 25 giây AI mới nghe).

Hai việc:
  1. LÀM NÓNG: lần gọi đầu của ChatGPT Live phải khởi động Codex app-server rồi mở một thread (đo trên Mac: 0,45 giây khởi động,
     2,3 giây cho thread đầu, 0,26 giây từ thread thứ hai; Windows chậm hơn nhiều). Trình duyệt gọi /voice/prewarm lúc mở trang
     và mỗi vài phút để việc đó xong TRƯỚC khi anh bấm gọi.
  2. GHI THỜI GIAN từng chặng của mỗi cuộc gọi (máy chủ và trình duyệt) vào live_timing.jsonl: lần sau chậm thì đọc file này
     là biết chậm ở chặng nào, không phải đoán. Không ghi nội dung cuộc nói, chỉ số mili giây và kết quả.

  ghi(dict)          thêm một dòng vào file thời gian (máy chủ gọi).
  gan(app)           POST /voice/prewarm, POST /voice/timing (trình duyệt gửi), GET /voice/timing (xem 30 dòng cuối).
"""
from __future__ import annotations

import asyncio
import json
import tempfile
import threading
import time
from pathlib import Path

try:
    from fastapi import Request   # phải ở mức module: FastAPI đọc chú thích 'Request' từ đây
except Exception:  # noqa: BLE001
    Request = None

_FILE_NAME = "live_timing.jsonl"
_MAX_LINES = 300
_lock = threading.Lock()
_state = {"warm_at": 0.0, "busy": False, "last_error": ""}


def _path() -> Path:
    try:
        import config as _cfg
        return Path(_cfg.STATE_DIR) / _FILE_NAME
    except Exception:  # noqa: BLE001
        return Path(__file__).resolve().parent / _FILE_NAME


def ghi(row: dict) -> None:
    """Thêm một dòng. Không bao giờ làm hỏng cuộc gọi: lỗi ghi file thì bỏ qua."""
    try:
        clean = {}
        for k, v in (row or {}).items():
            if isinstance(v, (int, float, bool)) or v is None:
                clean[str(k)[:40]] = v
            else:
                clean[str(k)[:40]] = str(v)[:80]
        clean["luc"] = time.strftime("%Y-%m-%d %H:%M:%S")
        line = json.dumps(clean, ensure_ascii=False)
        p = _path()
        with _lock:
            old = []
            if p.exists():
                try:
                    old = p.read_text(encoding="utf-8").splitlines()
                except OSError:
                    old = []
            old.append(line)
            p.write_text("\n".join(old[-_MAX_LINES:]) + "\n", encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass


def doc(n: int = 30) -> list:
    out = []
    try:
        for line in _path().read_text(encoding="utf-8").splitlines()[-n:]:
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
    except OSError:
        pass
    return out


async def lam_nong() -> dict:
    """Dựng sẵn Codex app-server và một thread thử, một lần cho mỗi tiến trình máy chủ. Không gọi mạng, không tốn lượt."""
    import codex_realtime
    t0 = time.monotonic()
    srv = await codex_realtime.get_app_server()
    xong_may = int((time.monotonic() - t0) * 1000)
    if getattr(srv, "_tisa_da_nong", False):
        return {"ok": True, "da_nong": True, "app_server_ms": xong_may}
    t1 = time.monotonic()
    cwd = tempfile.mkdtemp(prefix="tisa-live-warm-")
    try:
        await srv.request("thread/start", {
            "ephemeral": True, "cwd": cwd, "sandbox": "read-only", "approvalPolicy": "never",
            "developerInstructions": "Reply only: [FINAL]",
        }, timeout=40)
    finally:
        try:
            import shutil
            shutil.rmtree(cwd, ignore_errors=True)
        except Exception:  # noqa: BLE001
            pass
    srv._tisa_da_nong = True
    thread_ms = int((time.monotonic() - t1) * 1000)
    ghi({"nguon": "lam_nong", "app_server_ms": xong_may, "thread_ms": thread_ms})
    return {"ok": True, "da_nong": False, "app_server_ms": xong_may, "thread_ms": thread_ms}


def gan(app) -> None:
    from fastapi.responses import JSONResponse

    @app.post("/voice/prewarm")
    async def _prewarm():
        if _state["busy"]:
            return JSONResponse({"ok": True, "busy": True})
        _state["busy"] = True
        try:
            res = await asyncio.wait_for(lam_nong(), 60)
            _state["warm_at"] = time.time()
            _state["last_error"] = ""
            return JSONResponse(res)
        except Exception as e:  # noqa: BLE001  (chưa cài Codex, chưa đăng nhập ChatGPT...: không phải lỗi, chỉ là không có gì để làm nóng)
            _state["last_error"] = f"{type(e).__name__}: {str(e)[:120]}"
            return JSONResponse({"ok": False, "ly_do": _state["last_error"]})
        finally:
            _state["busy"] = False

    @app.post("/voice/timing")
    async def _timing_gui(request: Request):
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            return JSONResponse({"ok": False})
        if isinstance(d, dict):
            d["nguon"] = "trinh_duyet"
            ghi(d)
        return JSONResponse({"ok": True})

    @app.get("/voice/timing")
    async def _timing_xem():
        return JSONResponse({"dong": doc(30), "lam_nong": dict(_state)})
