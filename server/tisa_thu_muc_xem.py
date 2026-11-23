"""tisa_thu_muc_xem.py - Cho khung chat XEM video, ảnh, âm thanh, PDF nằm ở một vài THƯ MỤC CHỈ ĐỊNH ngoài bộ não (chủ chọn 23/11/2026).

Lỗi gốc: video dựng xong để ở Desktop/MKT AI AGENT K01/..., ngoài bộ não. /files/raw bắt đăng nhập nên khoá vùng đọc tệp trong bộ não (đúng chủ ý: mở cả ổ đĩa là
lộ khoá và mật khẩu cho mọi phiên đăng nhập), nên ô video trong chat trả 404 và hiện ô xám.

Cách sửa hẹp: chủ tự thêm từng thư mục cụ thể vào danh sách (trang "Thư mục xem trong chat"). /files/raw hỏi tim(path) trước luật cũ. CHỈ phục vụ tệp:
  - nằm đúng trong một thư mục trong danh sách (đã resolve nên không đi qua ../ và không theo liên kết ra ngoài),
  - có đuôi video, ảnh, âm thanh hoặc PDF (không bao giờ .json, .py, .env, tệp khoá...).
Thư mục thêm vào phải: nằm trong thư mục người dùng, sâu ít nhất 2 cấp (không cho cả Desktop, Documents, cả thư mục người dùng), không có thành phần ẩn (bắt đầu bằng .),
không nằm trong Library và không nằm trong thư mục cài TISA BOT. Vẫn đòi đăng nhập như mọi đường /files/*.
Không ghi khoá hay dữ liệu cá nhân ở đây; danh sách nằm ở server/thu-muc-xem.json (không lên git).
"""
from __future__ import annotations

import json
import os
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEP = ROOT / "server" / "thu-muc-xem.json"
DUOI = {
    ".mp4", ".mov", ".m4v", ".webm", ".mkv",            # video
    ".mp3", ".wav", ".m4a", ".aac", ".ogg",             # âm thanh
    ".jpg", ".jpeg", ".png", ".gif", ".webp",           # ảnh
    ".pdf",
}
_khoa = threading.RLock()


def _nha() -> Path:
    return Path.home().resolve()


def _doc() -> list:
    try:
        d = json.loads(TEP.read_text(encoding="utf-8"))
        return [str(x) for x in (d.get("ds") or []) if isinstance(x, str)]
    except (OSError, ValueError, AttributeError):
        return []


def _ghi(ds: list) -> None:
    with _khoa:
        TEP.parent.mkdir(parents=True, exist_ok=True)
        tmp = TEP.with_suffix(".tmp")
        tmp.write_text(json.dumps({"ds": ds}, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(tmp, TEP)


def kiem_tra(p) -> tuple:
    """(Path đã resolve | None, lý do nếu không hợp lệ)."""
    s = str(p or "").strip()
    if not s or "\x00" in s or len(s) > 500:
        return None, "Chưa nhập đường dẫn thư mục."
    try:
        r = Path(s).expanduser().resolve(strict=True)
    except (OSError, RuntimeError):
        return None, "Không thấy thư mục này trên máy."
    if not r.is_dir():
        return None, "Đây không phải thư mục."
    nha = _nha()
    try:
        con = r.relative_to(nha).parts
    except ValueError:
        return None, "Chỉ cho thêm thư mục nằm trong thư mục người dùng của máy này."
    if len(con) < 2:
        return None, "Thư mục này quá rộng (cả Desktop, Documents hay cả thư mục người dùng). Chọn một thư mục dự án cụ thể, ví dụ Desktop/MKT AI AGENT K01."
    if any(x.startswith(".") for x in con):
        return None, "Không cho thêm thư mục ẩn."
    if con[0].lower() == "library":
        return None, "Không cho thêm thư mục hệ thống (Library)."
    try:
        r.relative_to(ROOT.resolve())
        return None, "Không cho thêm thư mục nằm trong nơi cài TISA BOT."
    except ValueError:
        pass
    try:
        ROOT.resolve().relative_to(r)
        return None, "Thư mục này chứa cả nơi cài TISA BOT, quá rộng."
    except ValueError:
        pass
    return r, ""


def danh_sach() -> list:
    """[{path, co}] co=False khi thư mục không còn trên máy."""
    out = []
    for s in _doc():
        try:
            co = Path(s).is_dir()
        except OSError:
            co = False
        out.append({"path": s, "co": co})
    return out


def them(p) -> dict:
    r, ly_do = kiem_tra(p)
    if r is None:
        return {"ok": False, "loi": ly_do}
    ds = _doc()
    if str(r) not in ds:
        ds.append(str(r))
        _ghi(ds)
    return {"ok": True, "ds": danh_sach()}


def xoa(p) -> dict:
    s = str(p or "").strip()
    ds = [x for x in _doc() if x != s]
    _ghi(ds)
    return {"ok": True, "ds": danh_sach()}


def _cac_thu_muc() -> list:
    out = []
    for s in _doc():
        r, _ = kiem_tra(s)            # kiểm lại mỗi lần: thư mục bị xoá hoặc thành liên kết ra ngoài thì thôi
        if r is not None:
            out.append(r)
    return out


def tim(path):
    """Trả Path tệp media nếu `path` trỏ đúng vào một thư mục trong danh sách, ngược lại None (để luật cũ chạy như trước).
    `path` có thể là đường dẫn đầy đủ (có hoặc mất dấu / đầu, khung chat hay bỏ) hoặc tương đối so với thư mục người dùng ("Desktop/...")."""
    p = str(path or "").replace("\\", "/").strip()
    if not p or "\x00" in p or len(p) > 800:
        return None
    if Path(p.lstrip("/")).suffix.lower() not in DUOI:
        return None
    dirs = _cac_thu_muc()
    if not dirs:
        return None
    ung = [Path("/" + p.lstrip("/")), _nha() / p.lstrip("/")]
    for c in ung:
        try:
            r = c.resolve()
        except (OSError, RuntimeError):
            continue
        if r.suffix.lower() in DUOI and any(d == r.parent or d in r.parents for d in dirs):
            try:
                if r.is_file():
                    return r
            except OSError:
                continue
    return None


def gan(app) -> None:
    from fastapi import Request
    from fastapi.responses import HTMLResponse, JSONResponse

    trang = ROOT / "dashboard" / "tisa-thu-muc-xem.html"

    @app.get("/tisa-thu-muc-xem/")
    async def _trang():
        try:
            return HTMLResponse(trang.read_text(encoding="utf-8"), headers={"cache-control": "no-cache"})
        except OSError:
            return HTMLResponse("Thiếu trang Thư mục xem trong chat", status_code=500)

    @app.get("/tisa-thu-muc-xem/api/ds")
    async def _ds():
        return JSONResponse({"ok": True, "ds": danh_sach(), "duoi": sorted(DUOI)})

    @app.post("/tisa-thu-muc-xem/api/them")
    async def _them(request: Request):
        try:
            b = await request.json()
        except Exception:  # noqa: BLE001
            b = {}
        r = them((b or {}).get("path"))
        return JSONResponse(r, status_code=200 if r.get("ok") else 400)

    @app.post("/tisa-thu-muc-xem/api/xoa")
    async def _xoa(request: Request):
        try:
            b = await request.json()
        except Exception:  # noqa: BLE001
            b = {}
        return JSONResponse(xoa((b or {}).get("path")))
