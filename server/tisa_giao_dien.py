"""tisa_giao_dien.py - Đội Quân AI thành trang con của TISA BOT, và phần tự đổi tên, màu của giao diện.

1. /doiquanagent/...: TISA BOT chuyển tiếp sang Bảng giao việc (Node, 127.0.0.1:TISA_BOARD_PORT). Đi qua cổng đăng nhập
   của TISA BOT nên một tài khoản dùng cho cả hai, một tên miền là đủ. Bảng nhận yêu cầu như thể mở từ chính máy này
   (Host 127.0.0.1, bỏ các header của đường hầm) nên tự vào, không hỏi mật khẩu lần hai.
   Mã bảng gọi máy chủ bằng đường dẫn tuyệt đối ('/api/...'), nên trang và tệp JS của bảng được thêm tiền tố khi đi qua.
2. /tisa-giao-dien.json, /tisa-giao-dien.css: tên hiển thị và hai màu (màu nhấn, màu chính) người dùng chọn.
   Công khai như /brand-logo vì màn đăng nhập cũng dùng; không chứa gì bí mật.

Lỗi ở đây không được làm hỏng TISA BOT: bảng chưa chạy thì báo 502, cài đặt hỏng thì về màu mặc định.
"""
import os
import re
import zlib
from pathlib import Path
from urllib.parse import urlencode

import httpx
from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse, Response, StreamingResponse
from starlette.background import BackgroundTask

import config as cfgmod

TIEN_TO = "/doiquanagent"
MAC_DINH = {"ten": "TISA BOT", "mau_nhan": "#ff6b35", "mau_chinh": "#172f72"}
_HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
# Header của đường hầm, proxy: bỏ đi để bảng coi là yêu cầu từ chính máy này.
_BO_HEADER = {"host", "content-length", "connection", "accept-encoding", "cookie", "x-forwarded-for", "x-forwarded-host",
              "x-forwarded-proto", "x-real-ip", "cf-connecting-ip", "cf-ray", "cf-visitor", "cf-ipcountry", "forwarded",
              "cdn-loop", "true-client-ip"}
_BO_TRA = {"content-length", "content-encoding", "transfer-encoding", "connection", "x-frame-options", "set-cookie"}
# Đường dẫn tuyệt đối trong mã bảng (đếm ngày 09/11/2026: /api, /_blob, /kit.js, /tisa-model.js).
_DUONG = ("/api/", "/_blob/", "/kit.js", "/tisa-model.js")
_client = None
_SHIM = Path(__file__).resolve().parent.parent / "dashboard" / "tisa-doi-quan-nhung.js"
_shim_ban = {"khoa": None, "v": "1"}


def _ban_shim():
    """Số phiên bản theo nội dung tệp: /static được nhớ một năm, đổi tệp mà giữ số cũ là trình duyệt dùng bản cũ."""
    try:
        st = _SHIM.stat()
        khoa = (st.st_mtime_ns, st.st_size)
        if _shim_ban["khoa"] != khoa:
            _shim_ban.update(khoa=khoa, v="%08x" % zlib.crc32(_SHIM.read_bytes()))
    except OSError:
        pass
    return _shim_ban["v"]


def _cong_bang():
    return int(os.getenv("TISA_BOARD_PORT") or 7788)


def doc():
    """Tên và màu đang dùng. Giá trị hỏng thì về mặc định, không bao giờ ném lỗi."""
    try:
        g = cfgmod.read_settings().get("tisa_giao_dien") or {}
    except Exception:  # noqa: BLE001
        g = {}
    out = dict(MAC_DINH)
    ten = str(g.get("ten") or "").strip()
    if ten:
        out["ten"] = ten[:40]
    for k in ("mau_nhan", "mau_chinh"):
        v = str(g.get(k) or "")
        if _HEX.match(v):
            out[k] = v.lower()
    return out


def ghi(data: dict):
    cfg = cfgmod.read_settings()
    g = dict(cfg.get("tisa_giao_dien") or {})
    if "ten" in data:
        ten = re.sub(r"[\x00-\x1f<>]", "", str(data.get("ten") or "")).strip()[:40]
        g["ten"] = ten
    for k in ("mau_nhan", "mau_chinh"):
        if k in data:
            v = str(data.get(k) or "").strip()
            if v and not _HEX.match(v):
                raise ValueError("Mã màu phải có dạng #RRGGBB")
            g[k] = v.lower()
    cfg["tisa_giao_dien"] = g
    cfgmod.write_settings(cfg)
    return doc()


def css():
    """Biến màu cho TISA BOT (tisa-tong-mau.css, tisa-giao-dien.css đọc --tisa-*) và cho bảng (--b1, --b2)."""
    g = doc()
    n, c = g["mau_nhan"], g["mau_chinh"]
    sang = "color-mix(in srgb, %s 78%%, #ffffff)" % n
    out = ("html:root, html:root[data-theme], html:root[data-theme=\"light\"], html:root[data-theme=\"dark\"] {\n"
           "  --tisa-nhan: %s;\n  --tisa-nhan-sang: %s;\n  --tisa-nhan-dam: color-mix(in srgb, %s 86%%, #000000);\n"
           "  --tisa-chinh: %s;\n  --tisa-chinh-dam: color-mix(in srgb, %s 80%%, #000000);\n"
           "  --b1: %s;\n  --b1l: %s;\n  --b2: %s;\n  --b2l: color-mix(in srgb, %s 82%%, #ffffff);\n}\n") % (n, sang, n, c, c, n, sang, c, c)
    if n != MAC_DINH["mau_nhan"]:
        # Chữ màu nhấn (tab đang chọn, liên kết nhấn): đậm hơn ở tông sáng, nhạt hơn ở tông tối cho dễ đọc.
        # Màu mặc định giữ nguyên chữ cam đất của tisa-tong-mau.css.
        out += ("html:root[data-theme=\"light\"] { --accent-ink: color-mix(in srgb, %s 72%%, #000000); --brain-ink-hot: color-mix(in srgb, %s 72%%, #000000); }\n"
                "html:root[data-theme=\"dark\"] { --accent-ink: color-mix(in srgb, %s 70%%, #ffffff); --brain-ink-hot: color-mix(in srgb, %s 70%%, #ffffff); }\n"
                # Nền và chữ nhấn của bảng, cùng công thức brand() trong board.html.
                "html:root { --gold-ink: color-mix(in srgb, %s 72%%, #000); --gold-wash: color-mix(in srgb, %s 9%%, #fff); --gold-line: color-mix(in srgb, %s 32%%, #fff); }\n"
                "html:root[data-theme=\"dark\"] { --gold-ink: color-mix(in srgb, %s 70%%, #fff); --gold-wash: color-mix(in srgb, %s 22%%, #0B1026); --gold-line: color-mix(in srgb, %s 45%%, #0B1026); }\n"
                ) % ((n,) * 10)
    return out


async def _http():
    global _client
    if _client is None:
        _client = httpx.AsyncClient(timeout=httpx.Timeout(60.0, read=None), follow_redirects=False)
    return _client


def _them_tien_to(text: str) -> str:
    for q in ("'", '"', "`"):
        for p in _DUONG:
            text = text.replace(q + p, q + TIEN_TO + p)
    return text


def _cookie(header: str) -> str:
    """Chỉ chuyển cookie của bảng, không đưa phiên TISA BOT sang tiến trình khác."""
    giu = [c for c in re.split(r";\s*", header or "") if c.startswith("dq_s=")]
    return "; ".join(giu)


async def chuyen_tiep(request: Request, rest: str = ""):
    rest = rest.lstrip("/")
    nhung = request.query_params.get("nhung") or request.headers.get("sec-fetch-dest") == "iframe"
    # Mở thẳng /doiquanagent trên thanh địa chỉ: đưa vào khung TISA BOT để có menu, tài khoản, màu chung.
    if not rest and request.method == "GET" and not nhung:
        return RedirectResponse("/#doiquan", status_code=302)
    cong = _cong_bang()
    url = "http://127.0.0.1:%d/%s" % (cong, rest)
    q = [(k, v) for k, v in request.query_params.multi_items() if k != "nhung"]
    if q:
        url += "?" + urlencode(q)
    headers = {k: v for k, v in request.headers.items() if k.lower() not in _BO_HEADER}
    headers["host"] = "127.0.0.1:%d" % cong
    ck = _cookie(request.headers.get("cookie", ""))
    if ck:
        headers["cookie"] = ck
    body = None
    if request.method not in ("GET", "HEAD"):
        body = request.stream()
    cli = await _http()
    try:
        r = await cli.send(cli.build_request(request.method, url, headers=headers, content=body), stream=True)
    except httpx.HTTPError:
        return JSONResponse({"error": "Đội Quân AI chưa chạy. Mở lại TISA BOT rồi thử lại sau một phút."}, status_code=502)
    tra = {k: v for k, v in r.headers.items() if k.lower() not in _BO_TRA}
    if "location" in tra and tra["location"].startswith("/"):
        tra["location"] = TIEN_TO + tra["location"]
    cookies = [re.sub(r"(?i);\s*path=/(?=;|$)", "; Path=" + TIEN_TO, c) for c in r.headers.get_list("set-cookie")]
    loai = r.headers.get("content-type", "")
    if "text/html" in loai or "javascript" in loai:
        raw = await r.aread()
        await r.aclose()
        text = _them_tien_to(raw.decode("utf-8", "replace"))
        if "text/html" in loai:
            text = text.replace("<head>", '<head><script>window.__DQ_BASE="%s"</script>'
                                '<script src="/static/tisa-doi-quan-nhung.js?v=%s"></script>' % (TIEN_TO, _ban_shim()), 1)
            text = text.replace("</head>", '<link rel="stylesheet" href="/tisa-giao-dien.css">\n</head>', 1)
        resp = Response(text, status_code=r.status_code, headers=tra)
    else:
        resp = StreamingResponse(r.aiter_bytes(), status_code=r.status_code, headers=tra, background=BackgroundTask(r.aclose))
    for c in cookies:
        resp.headers.append("set-cookie", c)
    resp.headers["x-frame-options"] = "SAMEORIGIN"
    return resp


def gan(app):
    """Gắn route và lớp chặn vào app của TISA BOT. Gọi một lần lúc nạp main.py."""

    @app.middleware("http")
    async def _tisa_giao_dien_mw(request: Request, call_next):
        path = request.url.path
        # Công khai: màn đăng nhập cũng hiện tên và màu riêng.
        if path == "/tisa-giao-dien.css" and request.method == "GET":
            return Response(css(), media_type="text/css", headers={"cache-control": "no-cache"})
        if path == "/tisa-giao-dien.json" and request.method == "GET":
            return JSONResponse(doc(), headers={"cache-control": "no-cache"})
        # Chưa đăng nhập mà mở trang bảng: đưa về màn đăng nhập thay vì trả JSON 401.
        if (path == TIEN_TO or path == TIEN_TO + "/") and request.method == "GET" and cfgmod.gate_active() \
                and not cfgmod.valid_session(request.cookies.get("tisa_session", "")):
            return RedirectResponse("/#doiquan", status_code=302)
        return await call_next(request)

    @app.post("/tisa-giao-dien")
    async def _tisa_giao_dien_luu(request: Request):
        try:
            data = await request.json()
            return {"ok": True, **ghi(data if isinstance(data, dict) else {})}
        except ValueError as e:
            return JSONResponse({"ok": False, "error": str(e)}, status_code=400)

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
    app.add_api_route(TIEN_TO, chuyen_tiep, methods=methods, include_in_schema=False)
    app.add_api_route(TIEN_TO + "/{rest:path}", chuyen_tiep, methods=methods, include_in_schema=False)
