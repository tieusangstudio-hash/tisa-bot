"""tisa_kenh_an.py - ẨN BỚT FANPAGE, NICK KHÔNG DÙNG ở Chatbot (V2.91).

Nối Facebook có thể kéo về hàng chục Fanpage (chủ có 47) trong khi chatbot chỉ trả lời vài trang. Danh sách ẩn lưu trên máy
(STATE_DIR/kenh-an.json) để dùng chung mọi thiết bị. Ẩn chỉ là KHÔNG HIỂN THỊ trong danh sách kênh, bộ chọn kênh và danh sách hội thoại
"Tất cả kênh"; không xoá kênh, không tắt bot, không đổi gì ở nền tảng. Hiện lại bất cứ lúc nào.

GET  /tisa-kenh/an  -> {ok, an: [account_key]}
POST /tisa-kenh/an  {an: [account_key]}  (thay cả danh sách)
"""
from __future__ import annotations

import json
import os
import threading
from pathlib import Path

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

_khoa = threading.RLock()


def _file() -> Path:
    try:
        import config as _cfg
        base = Path(_cfg.STATE_DIR)
    except Exception:  # noqa: BLE001
        base = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)
    base.mkdir(parents=True, exist_ok=True)
    return base / "kenh-an.json"


def doc() -> list:
    try:
        d = json.loads(_file().read_text(encoding="utf-8"))
        return [str(x) for x in d.get("an", [])] if isinstance(d, dict) else []
    except (OSError, ValueError):
        return []


def ghi(ds) -> list:
    ds = sorted({str(x)[:200] for x in (ds or []) if str(x).strip()})[:3000]
    f = _file()
    tmp = f.with_suffix(".tmp")
    with _khoa:
        tmp.write_text(json.dumps({"an": ds}, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, f)
    return ds


def gan(app) -> None:
    from fastapi.responses import JSONResponse

    @app.get("/tisa-kenh/an")
    async def _lay():
        return JSONResponse({"ok": True, "an": doc()}, headers={"cache-control": "no-store"})

    @app.post("/tisa-kenh/an")
    async def _dat(request: Request):
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            return JSONResponse({"ok": False, "error": "Dữ liệu không đúng."}, status_code=400)
        ds = d.get("an") if isinstance(d, dict) else None
        if not isinstance(ds, list):
            return JSONResponse({"ok": False, "error": "Thiếu danh sách."}, status_code=400)
        return {"ok": True, "an": ghi(ds)}
