"""tisa_bieu_tuong.py - biểu tượng ứng dụng luôn khớp logo người dùng tải lên (V2.78, chủ báo 12/11/2026).

Trước đây tab trình duyệt đã theo logo (/brand-logo), nhưng khi cài TISA BOT thành ứng dụng (icon dưới Dock, Launchpad,
màn hình chính điện thoại) thì icon lấy từ manifest tĩnh với logo TISA mặc định, nên đổi logo xong icon ứng dụng vẫn cũ.

Ở đây:
  /manifest.json          manifest tạo theo logo hiện tại, địa chỉ icon có mã ?v= đổi theo logo.
  /brand-icon/<cỡ>.png    icon vuông <cỡ>x<cỡ> từ logo hiện tại (logo mặc định thì dùng icon TISA có sẵn).
Cả hai công khai (trình duyệt tải manifest không kèm đăng nhập). Có Pillow thì ảnh được đưa về hình vuông trong suốt
đúng cỡ, không có thì trả nguyên logo (vẫn hiện đúng hình, chỉ không ép vuông).
"""
from __future__ import annotations

import hashlib
import io
import json
import re
from pathlib import Path

_DASH = Path(__file__).resolve().parent.parent / "dashboard"
_MEDIA = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif"}
_CO = (192, 512)


def _logo_tuy_chinh():
    try:
        import config
        ext = ((config.read_settings().get("branding") or {}).get("logo_ext") or "")
        if ext:
            p = Path(config.BRANDING_DIR) / ("logo" + ext)
            if p.is_file():
                return p
    except Exception:  # noqa: BLE001
        pass
    return None


def _ma(p) -> str:
    """Mã ngắn đổi mỗi khi logo đổi (nội dung), để trình duyệt tải lại manifest và icon."""
    if p is None:
        return "mac-dinh"
    try:
        return hashlib.sha1(p.read_bytes()).hexdigest()[:10]
    except OSError:
        return "x"


def _bo_dem(co: int, ma: str):
    try:
        import config
        return Path(config.BRANDING_DIR) / ("_bieu-tuong-%s-%d.png" % (ma, co))
    except Exception:  # noqa: BLE001
        return None


def icon(co: int):
    """(bytes hoặc đường dẫn, kiểu media) của icon vuông cỡ co."""
    p = _logo_tuy_chinh()
    if p is None:
        mac_dinh = _DASH / ("icon-%d.png" % co)
        if mac_dinh.is_file():
            return mac_dinh, "image/png"
        return _DASH / "logo.png", "image/png"
    ma = _ma(p)
    cache = _bo_dem(co, ma)
    if cache is not None and cache.is_file():
        return cache, "image/png"
    try:
        from PIL import Image
        im = Image.open(p)
        im.load()
        im = im.convert("RGBA")
        im.thumbnail((co, co))
        nen = Image.new("RGBA", (co, co), (0, 0, 0, 0))
        nen.paste(im, ((co - im.width) // 2, (co - im.height) // 2), im)
        buf = io.BytesIO()
        nen.save(buf, "PNG", optimize=True)
        data = buf.getvalue()
        if cache is not None:
            try:
                cache.parent.mkdir(parents=True, exist_ok=True)
                cache.write_bytes(data)
            except OSError:
                pass
        return data, "image/png"
    except Exception:  # noqa: BLE001 - không có Pillow hoặc ảnh lạ: trả nguyên logo
        return p, _MEDIA.get(p.suffix.lower(), "image/png")


def manifest() -> dict:
    try:
        doc = json.loads((_DASH / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        doc = {"name": "TISA BOT", "short_name": "TISA", "id": "/", "start_url": "/", "scope": "/", "display": "standalone"}
    p = _logo_tuy_chinh()
    ma = _ma(p)
    kieu = _MEDIA.get(p.suffix.lower(), "image/png") if p is not None else "image/png"
    doc["icons"] = [{"src": "/brand-icon/%d.png?v=%s" % (co, ma), "sizes": "%dx%d" % (co, co), "type": kieu, "purpose": "any"}
                    for co in _CO]
    return doc


def gan(app) -> None:
    from starlette.responses import FileResponse, JSONResponse, Response

    @app.middleware("http")
    async def _tisa_bieu_tuong_mw(request, call_next):
        d = request.url.path
        if request.method in ("GET", "HEAD"):
            if d == "/manifest.json":
                return Response(json.dumps(manifest(), ensure_ascii=False), media_type="application/manifest+json",
                                headers={"cache-control": "no-cache"})
            m = re.fullmatch(r"/brand-icon/(\d{2,4})\.png", d)
            if m:
                co = max(16, min(1024, int(m.group(1))))
                nguon, media = icon(co)
                cache = {"cache-control": "public, max-age=3600", "x-content-type-options": "nosniff"}
                if isinstance(nguon, Path):
                    if not nguon.is_file():
                        return JSONResponse({"error": "no icon"}, status_code=404)
                    return FileResponse(str(nguon), media_type=media, headers=cache)
                return Response(nguon, media_type=media, headers=cache)
        return await call_next(request)
