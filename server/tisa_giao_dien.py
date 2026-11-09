"""tisa_giao_dien.py - Đội Quân AI thành trang con của TISA BOT, và phần tự đổi tên, màu của giao diện.

1. /doiquanagent/...: TISA BOT chuyển tiếp sang Bảng giao việc (Node, 127.0.0.1:TISA_BOARD_PORT). Đi qua cổng đăng nhập
   của TISA BOT nên một tài khoản dùng cho cả hai, một tên miền là đủ. Bảng nhận yêu cầu như thể mở từ chính máy này
   (Host 127.0.0.1, bỏ các header của đường hầm) nên tự vào, không hỏi mật khẩu lần hai.
   Mã bảng gọi máy chủ bằng đường dẫn tuyệt đối ('/api/...'), nên trang và tệp JS của bảng được thêm tiền tố khi đi qua.
2. /tisa-giao-dien.json, /tisa-giao-dien.css: tên hiển thị và hai màu (màu nhấn, màu chính) người dùng chọn.
   Công khai như /brand-logo vì màn đăng nhập cũng dùng; không chứa gì bí mật.

Lỗi ở đây không được làm hỏng TISA BOT: bảng chưa chạy thì báo 502, cài đặt hỏng thì về màu mặc định.
"""
import json
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


_NGOAI = {"khoa": None, "v": ("", "")}


def _bang_ngoai():
    """(gốc https của bảng đặt ngoài, khoá Bearer) khi bảng chạy ở nơi khác (TISA_BANG_NGOAI, ví dụ Cloudflare Worker); ("", "") nếu
    bảng chạy trên máy. Đọc TISA_BANG_URL, thiếu thì BOARD_URL trong tệp DOI_QUAN_ENV; khoá là BOARD_TOKEN cùng tệp.
    Chủ yêu cầu 10/11/2026: mọi thứ chung một tên miền, bấm Giao dự án không mở tên miền riêng của bảng nữa."""
    if not os.getenv("TISA_BANG_NGOAI") and not os.getenv("TISA_BANG_URL"):
        return "", ""
    f = Path(os.getenv("DOI_QUAN_ENV") or (Path.home() / ".config" / "doi-quan-ai" / ".env"))
    try:
        st = f.stat()
        khoa = (str(f), st.st_mtime_ns)
    except OSError:
        khoa = (str(f), 0)
    if _NGOAI["khoa"] != khoa:
        kv = {}
        try:
            for dong in f.read_text(encoding="utf-8").splitlines():
                if "=" in dong and not dong.lstrip().startswith("#"):
                    k, v = dong.split("=", 1)
                    kv[k.strip()] = v.strip().strip('"').strip("'")
        except OSError:
            pass
        goc = (os.getenv("TISA_BANG_URL") or kv.get("BOARD_URL") or "").strip().rstrip("/")
        m = re.match(r"^(?:https://[A-Za-z0-9.-]+(?::\d+)?|http://127\.0\.0\.1:\d+)", goc)
        _NGOAI.update(khoa=khoa, v=((m.group(0) if m else ""), kv.get("BOARD_TOKEN", "")))
    return _NGOAI["v"]


def doc():
    """Tên và màu đang dùng. Giá trị hỏng thì về mặc định, không bao giờ ném lỗi."""
    try:
        g = cfgmod.read_settings().get("tisa_giao_dien") or {}
    except Exception:  # noqa: BLE001
        g = {}
    out = dict(MAC_DINH)
    ten = str(g.get("ten") or "").strip()
    if ten:
        out["ten"] = ten[:60]
    for k in ("mau_nhan", "mau_chinh"):
        v = str(g.get(k) or "")
        if _HEX.match(v):
            out[k] = v.lower()
    return out


def ghi(data: dict):
    cfg = cfgmod.read_settings()
    g = dict(cfg.get("tisa_giao_dien") or {})
    if "ten" in data:
        # Tên dài được xuống hàng: người dùng bấm Shift + Enter lúc gõ. Tối đa 3 dòng, 60 ký tự.
        ten = str(data.get("ten") or "").replace("\r\n", "\n").replace("\r", "\n")
        ten = re.sub(r"[\x00-\x09\x0b-\x1f<>]", "", ten)
        dong = [re.sub(r"\s+", " ", x).strip() for x in ten.split("\n")]
        g["ten"] = "\n".join([x for x in dong if x][:3])[:60]
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
    ngoai, khoa_ngoai = _bang_ngoai()
    if ngoai:
        # Bảng đặt ngoài: TISA BOT đứng giữa, gắn khoá Bearer của máy chủ (chỉ người đã đăng nhập TISA BOT tới được đây),
        # nên chủ không phải đăng nhập bảng lần nữa. Origin đặt bằng gốc của bảng để bảng nhận lệnh ghi.
        url = "%s/%s" % (ngoai, rest)
        headers = {k: v for k, v in request.headers.items() if k.lower() not in _BO_HEADER and k.lower() not in ("origin", "referer")}
        headers["host"] = ngoai.split("://", 1)[1]
        if request.method not in ("GET", "HEAD"):
            headers["origin"] = ngoai
        if khoa_ngoai:
            headers["authorization"] = "Bearer " + khoa_ngoai
    else:
        cong = _cong_bang()
        url = "http://127.0.0.1:%d/%s" % (cong, rest)
        headers = {k: v for k, v in request.headers.items() if k.lower() not in _BO_HEADER}
        headers["host"] = "127.0.0.1:%d" % cong
    q = [(k, v) for k, v in request.query_params.multi_items() if k != "nhung"]
    if q:
        url += "?" + urlencode(q)
    ck = _cookie(request.headers.get("cookie", ""))
    if ck and not ngoai:
        headers["cookie"] = ck
    body = None
    if request.method not in ("GET", "HEAD"):
        # Bảng đặt ngoài: gửi cả thân một lần (có độ dài), máy chủ nào cũng nhận; bảng trên máy vẫn gửi dạng luồng.
        body = (await request.body()) if ngoai else request.stream()
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


_BANG_MANG = {"luc": 0.0, "bang": {}}


async def _bang_tren_mang():
    """Bảng số nội bộ -> tên V trên nhánh main của repo học viên, đệm 10 phút. Lỗi mạng thì trả bảng cũ."""
    import time
    if time.time() - _BANG_MANG["luc"] < 600:
        return _BANG_MANG["bang"]
    _BANG_MANG["luc"] = time.time()
    try:
        repo = getattr(__import__("sys").modules.get("main"), "GITHUB_REPO", "") or "tieusangstudio-hash/tisa-bot"
        async with httpx.AsyncClient(timeout=8) as cli:
            r = await cli.get("https://raw.githubusercontent.com/%s/main/TISA_BAN.json" % repo)
        if r.status_code == 200:
            _BANG_MANG["bang"] = dict((r.json() or {}).get("ban") or {})
    except Exception:  # noqa: BLE001
        pass
    return _BANG_MANG["bang"]


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

    @app.get("/tisa-ban")
    async def _tisa_ban(moi: str = ""):
        """Tên phiên bản hiện cho người dùng (TiSaBot - V2.69). Số nội bộ trong VERSION giữ nguyên cho bộ cập nhật.
        moi=<số nội bộ bản mới nhất> (lấy từ /version): tra tên V của bản đó trong TISA_BAN.json trên nhánh main."""
        goc = Path(__file__).resolve().parent.parent
        try:
            d = json.loads((goc / "TISA_BAN.json").read_text(encoding="utf-8"))
            noi_bo = (goc / "VERSION").read_text(encoding="utf-8").strip()
        except (OSError, ValueError):
            return JSONResponse({"ok": False}, status_code=404)
        ban = (d.get("ban") or {}).get(noi_bo) or d.get("hien_tai") or ""
        ban_moi = ""
        moi = re.sub(r"[^\d.]", "", moi)[:20]
        if moi and moi != noi_bo:
            ban_moi = (await _bang_tren_mang()).get(moi, "")
        return {"ok": bool(ban), "ban": ban, "noi_bo": noi_bo, "ban_moi": ban_moi, "bang": d.get("ban") or {}}

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
