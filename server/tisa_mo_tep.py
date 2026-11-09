"""Mở tệp kết quả bằng ứng dụng trên chính máy chủ TISA BOT (bộ TISA).

Bấm link slide/Word/Excel trong chat trên máy tính đang chạy TISA BOT thì mở thẳng bằng PowerPoint,
Word, Excel..., hoặc mở thư mục chứa tệp, không phải tải về. Máy khác vào qua tên miền vẫn tải về như cũ.

Hàng rào:
- Chỉ nhận yêu cầu làm ngay trên máy này: địa chỉ 127.0.0.1, không có header chuyển tiếp của đường hầm,
  Host là localhost, và trình duyệt báo cùng nguồn (chặn trang lạ đổi DNS về 127.0.0.1).
- Vẫn đòi phiên đăng nhập của chủ như mọi đường khác.
- Đường dẫn khoá trong bộ não (_safe_serve_path). Chỉ mở bằng ứng dụng các đuôi tài liệu, ảnh, âm thanh,
  video; tệp chạy được (.app, .command, .sh, .exe...) chỉ được "mở thư mục", không bao giờ chạy.
"""
import os
import subprocess
import sys
from pathlib import Path

from fastapi import Request
from fastapi.responses import JSONResponse

DUOI_MO = {
    "pptx", "ppt", "key", "docx", "doc", "pages", "rtf", "xlsx", "xls", "csv", "numbers", "pdf", "txt", "md",
    "png", "jpg", "jpeg", "gif", "webp", "bmp", "heic", "svg",
    "mp4", "mov", "m4v", "webm", "mkv", "avi", "mp3", "wav", "m4a", "ogg", "flac",
}
_LOOP = ("127.0.0.1", "localhost", "::1")
_CHUYEN_TIEP = ("x-forwarded-for", "x-real-ip", "forwarded", "cf-connecting-ip")


def _host(h):
    h = (h or "").strip().lower()
    if h.startswith("["):
        return h[1:h.find("]")] if "]" in h else h
    return h.rsplit(":", 1)[0] if h.count(":") == 1 else h


def tren_may_chu(request: Request) -> bool:
    ip = request.client.host if request.client else ""
    if ip not in ("127.0.0.1", "::1"):
        return False
    if any(request.headers.get(h) for h in _CHUYEN_TIEP):
        return False
    if _host(request.headers.get("host")) not in _LOOP:
        return False
    site = request.headers.get("sec-fetch-site")
    return site in (None, "", "same-origin")


def _mo(duong, cach):
    duong = str(duong)
    if sys.platform == "darwin":
        lenh = ["open", "-R", duong] if cach == "thu-muc" else ["open", duong]
        subprocess.Popen(lenh, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif os.name == "nt":
        if cach == "thu-muc":
            subprocess.Popen(["explorer", "/select,", duong])
        else:
            os.startfile(duong)  # noqa: S606 - đuôi đã lọc theo DUOI_MO
    else:
        dich = os.path.dirname(duong) if cach == "thu-muc" else duong
        subprocess.Popen(["xdg-open", dich], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def gan(app, safe_path, brain_root):

    @app.get("/tisa-mo-tep/may-chu")
    async def _may_chu(request: Request):
        return JSONResponse({"may_chu": tren_may_chu(request)}, headers={"cache-control": "no-store"})

    @app.post("/tisa-mo-tep")
    async def _mo_tep(request: Request):
        if not tren_may_chu(request):
            return JSONResponse({"ok": False, "error": "Chỉ mở được trên máy đang chạy TISA BOT"}, status_code=403)
        try:
            body = await request.json()
        except Exception:  # noqa: BLE001
            body = {}
        cach = "thu-muc" if body.get("cach") == "thu-muc" else "mo"
        try:
            f = safe_path(str(body.get("brain") or "brain"), str(body.get("path") or ""))
        except ValueError as e:
            return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
        try:
            goc = Path(brain_root(str(body.get("brain") or "brain"))).resolve()
            that = f.resolve()
        except Exception:  # noqa: BLE001
            return JSONResponse({"ok": False, "error": "Đường dẫn không hợp lệ"}, status_code=400)
        if that != goc and goc not in that.parents:
            return JSONResponse({"ok": False, "error": "Chỉ mở tệp trong bộ não"}, status_code=403)
        f = that
        if not f.exists():
            return JSONResponse({"ok": False, "error": "Không tìm thấy tệp"}, status_code=404)
        if cach == "mo" and (not f.is_file() or f.suffix.lower().lstrip(".") not in DUOI_MO):
            return JSONResponse({"ok": False, "error": "Loại tệp này chỉ mở thư mục"}, status_code=400)
        try:
            _mo(f, cach)
        except Exception as e:  # noqa: BLE001
            return JSONResponse({"ok": False, "error": "Không mở được: %s" % type(e).__name__}, status_code=500)
        return {"ok": True}
