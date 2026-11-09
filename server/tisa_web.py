"""Quản lý web (bộ TISA): các trang web làm từ ô chat TISA BOT và đã đưa lên mạng.

Chủ yêu cầu 09/11/2026: một trang để kiểm soát mọi web tạo từ TISA BOT (Vercel, Netlify, tên miền riêng...),
kiểm tra kết nối, chỉnh sửa, và để TISA BOT vào web lấy dữ liệu hỗ trợ tư vấn.

- Danh sách web lưu ở STATE_DIR/tisa_web/web.json. Web mới tự hiện khi bot ghi kết quả đưa web lên mạng vào
  04-ket-qua (nút "Tìm web đã tạo" quét các ghi chép đó), hoặc chủ thêm tay.
- Kiểm tra kết nối: mã trả về, thời gian phản hồi, tiêu đề, ảnh chia sẻ, số ngày còn lại của chứng chỉ https.
- Lấy dữ liệu về bộ não: nội dung chữ của trang và bảng Google Sheet (link CSV công khai) ghi vào
  02-kien-thuc/web/<tên>/ để Hỏi nhanh, chuyên gia, Chatbot đọc khi tư vấn.
- Form khách để lại thông tin: mỗi web có một địa chỉ nhận riêng /tisa-web/thu/<khoá> (công khai, chỉ nhận ghi,
  có giới hạn tần suất và kích thước). Khách lưu vào STATE_DIR và vào bộ não.

Mọi đường /tisa-web/ khác đòi phiên đăng nhập của chủ (lớp chặn chung của TISA BOT).
Máy chủ chỉ tải địa chỉ công khai trên Internet, không với vào mạng nội bộ (chặn SSRF).
"""
import asyncio
import csv
import hashlib
import io
import ipaddress
import json
import os
import re
import secrets
import socket
import ssl
import threading
import time
import unicodedata
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

import config as cfgmod

ROOT = Path(__file__).resolve().parent.parent
KHO = Path(cfgmod.STATE_DIR) / "tisa_web"
TRANG = ROOT / "dashboard" / "tisa-web.html"
_KHOA = threading.Lock()
UA = "TISA-BOT-kiem-tra-web/1.0"
NEN_TANG = {
    "vercel.app": "Vercel", "netlify.app": "Netlify", "pages.dev": "Cloudflare", "workers.dev": "Cloudflare",
    "github.io": "GitHub Pages", "web.app": "Firebase", "firebaseapp.com": "Firebase", "onrender.com": "Render",
    "surge.sh": "Surge", "ladipage.me": "LadiPage", "wixsite.com": "Wix", "trycloudflare.com": "Cloudflare",
}
_LINK_RE = re.compile(r"https?://[A-Za-z0-9.-]+\.(?:vercel\.app|netlify\.app|pages\.dev|workers\.dev|github\.io|web\.app|"
                      r"firebaseapp\.com|onrender\.com|surge\.sh|ladipage\.me|wixsite\.com)(?:/[^\s)\]>\"'`]*)?", re.I)


# ---------------------------------------------------------------- lưu trữ

def _brain():
    return Path(os.getenv("BRAINS_DIR") or (ROOT / "brains")) / "Brain Default"


def _doc(p, mac_dinh):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return mac_dinh


def _ghi(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    tam = p.with_suffix(".tmp")
    tam.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tam, p)


def _ds():
    return _doc(KHO / "web.json", [])


def _luu_ds(ds):
    _ghi(KHO / "web.json", ds)


def _bay_gio():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _khong_dau(s):
    s = unicodedata.normalize("NFD", str(s or "")).replace("đ", "d").replace("Đ", "D")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60] or "web"


def _chuan_link(u):
    u = (u or "").strip()
    if not u:
        return ""
    if not re.match(r"^https?://", u, re.I):
        u = "https://" + u
    p = urlparse(u)
    if p.scheme not in ("http", "https") or not p.hostname or len(u) > 500:
        raise ValueError("Link không hợp lệ")
    return u.rstrip("/") if p.path in ("", "/") else u


def _nen_tang(*links):
    for l in links:
        h = (urlparse(l).hostname or "") if l else ""
        for duoi, ten in NEN_TANG.items():
            if h.endswith(duoi):
                return ten
    return ""


def _tim(ds, wid):
    return next((w for w in ds if w.get("id") == wid), None)


def _thu_muc_du_lieu(w):
    return _brain() / "02-kien-thuc" / "web" / (w.get("slug") or _khong_dau(w.get("ten")))


# ---------------------------------------------------------------- tải web an toàn

def _ip_cong_khai(host):
    try:
        infos = socket.getaddrinfo(host, None)
    except OSError:
        raise ValueError("Không phân giải được tên miền %s" % host)
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast or ip.is_unspecified:
            raise ValueError("Địa chỉ nội bộ, không kiểm tra")
    return True


async def _chan_noi_bo(request):
    await asyncio.to_thread(_ip_cong_khai, request.url.host)


async def _tai(url, toi_da=600_000):
    import httpx
    bd = time.monotonic()
    async with httpx.AsyncClient(follow_redirects=True, timeout=httpx.Timeout(15.0), max_redirects=6,
                                 headers={"user-agent": UA, "accept": "text/html,*/*;q=0.8"},
                                 event_hooks={"request": [_chan_noi_bo]}) as c:
        async with c.stream("GET", url) as r:
            buf = b""
            async for phan in r.aiter_bytes():
                buf += phan
                if len(buf) >= toi_da:
                    break
            return r.status_code, str(r.url), buf[:toi_da], r.headers.get("content-type", ""), int((time.monotonic() - bd) * 1000)


def _ssl_con_ngay(host):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=8) as s:
            with ctx.wrap_socket(s, server_hostname=host) as t:
                het = ssl.cert_time_to_seconds(t.getpeercert()["notAfter"])
        return int((het - time.time()) // 86400)
    except Exception:  # noqa: BLE001
        return None


class _Doc(HTMLParser):
    """Lấy tiêu đề, mô tả, ảnh chia sẻ và chữ hiển thị của trang (bỏ script, style)."""
    BO = {"script", "style", "noscript", "svg", "template", "iframe"}
    KHOI = {"p", "div", "section", "li", "h1", "h2", "h3", "h4", "h5", "h6", "br", "tr", "article", "header", "footer", "td", "th", "button", "a"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tieu_de, self.mo_ta, self.anh, self.icon = "", "", "", ""
        self._sau, self._trong_title, self.chu = 0, False, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.BO:
            self._sau += 1
        elif tag == "title":
            self._trong_title = True
        elif tag == "meta":
            ten = (a.get("property") or a.get("name") or "").lower()
            if ten in ("og:image", "twitter:image") and not self.anh:
                self.anh = a.get("content") or ""
            elif ten in ("description", "og:description") and not self.mo_ta:
                self.mo_ta = a.get("content") or ""
        elif tag == "link" and "icon" in (a.get("rel") or "").lower() and not self.icon:
            self.icon = a.get("href") or ""
        if tag in self.KHOI:
            self.chu.append("\n")
        if tag in ("h1", "h2", "h3"):
            self.chu.append("\n## " if tag != "h3" else "\n### ")

    def handle_endtag(self, tag):
        if tag in self.BO and self._sau:
            self._sau -= 1
        elif tag == "title":
            self._trong_title = False
        if tag in self.KHOI:
            self.chu.append("\n")

    def handle_data(self, data):
        if self._trong_title:
            self.tieu_de += data
        elif not self._sau:
            self.chu.append(data)

    def van_ban(self):
        t = "".join(self.chu)
        t = re.sub(r"[ \t\r\f\v]+", " ", t)
        t = re.sub(r" *\n *", "\n", t)
        return re.sub(r"\n{3,}", "\n\n", t).strip()


def _doc_html(raw, ct):
    m = re.search(r"charset=([\w-]+)", ct or "")
    try:
        html = raw.decode(m.group(1) if m else "utf-8", errors="replace")
    except LookupError:
        html = raw.decode("utf-8", errors="replace")
    d = _Doc()
    try:
        d.feed(html)
    except Exception:  # noqa: BLE001
        pass
    return d


def _tuyet_doi(goc, u):
    if not u:
        return ""
    from urllib.parse import urljoin
    u = urljoin(goc, u)
    return u if u.startswith(("http://", "https://")) else ""


async def _kiem_tra(w):
    """Kiểm tra link chính và tên miền riêng. Trả kết quả gọn để lưu."""
    kq = {"luc": _bay_gio(), "muc": []}
    for nhan, link in (("link", w.get("link")), ("ten_mien", w.get("ten_mien"))):
        if not link:
            continue
        m = {"loai": nhan, "url": link}
        try:
            ma, cuoi, raw, ct, ms = await _tai(link)
            m.update(ma=ma, ms=ms, url_cuoi=cuoi, ok=200 <= ma < 400)
            if "html" in (ct or "") or raw[:200].lstrip().lower().startswith((b"<!doctype", b"<html")):
                d = _doc_html(raw, ct)
                m.update(tieu_de=d.tieu_de.strip()[:160], mo_ta=d.mo_ta.strip()[:300],
                         anh=_tuyet_doi(cuoi, d.anh), icon=_tuyet_doi(cuoi, d.icon))
            h = urlparse(cuoi).hostname or ""
            if cuoi.startswith("https://") and h:
                m["ssl_ngay"] = await asyncio.to_thread(_ssl_con_ngay, h)
        except ValueError as e:
            m.update(ok=False, loi=str(e))
        except Exception as e:  # noqa: BLE001
            ten = type(e).__name__
            m.update(ok=False, loi={"ConnectTimeout": "Hết thời gian chờ kết nối", "ReadTimeout": "Trang phản hồi quá chậm",
                                    "ConnectError": "Không kết nối được (tên miền chưa trỏ đúng hoặc web đã tắt)",
                                    "TooManyRedirects": "Chuyển hướng vòng lặp"}.get(ten, "Lỗi kết nối: " + ten))
        kq["muc"].append(m)
    kq["ok"] = bool(kq["muc"]) and all(x.get("ok") for x in kq["muc"])
    return kq


# ---------------------------------------------------------------- tìm web đã tạo trong bộ não

def _tim_trong_bo_nao(da_co):
    goc = _brain() / "04-ket-qua"
    if not goc.is_dir():
        return []
    ung_vien = {}
    dem = 0
    for f in sorted(goc.rglob("*.md")):
        dem += 1
        if dem > 3000:
            break
        try:
            if f.stat().st_size > 400_000:
                continue
            t = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        links = []
        fm = re.match(r"^---\n(.*?)\n---", t, re.S)
        loai_web = False
        ten = ""
        ten_mien = ""
        if fm:
            for dong in fm.group(1).splitlines():
                k, _, v = dong.partition(":")
                k, v = k.strip().lower(), v.strip().strip("'\"")
                if k == "loai" and v.lower() in ("web", "website", "trang-web"):
                    loai_web = True
                elif k in ("link", "url") and v.startswith("http"):
                    links.append(v)
                elif k in ("ten-mien", "ten_mien", "domain") and v:
                    ten_mien = v
                elif k in ("title", "ten", "chu-de") and v and not ten:
                    ten = v
        links += _LINK_RE.findall(t)
        if not links and not loai_web:
            continue
        thu_muc = f.parent.relative_to(_brain()).as_posix()
        link = next((l for l in links if l), "").rstrip(".,;")
        try:
            link = _chuan_link(link) if link else ""
        except ValueError:
            link = ""
        if ten_mien:
            try:
                ten_mien = _chuan_link(ten_mien)
            except ValueError:
                ten_mien = ""
        khoa = (link or ten_mien or thu_muc).lower()
        if khoa in da_co or (ten_mien and ten_mien.lower() in da_co) or khoa in ung_vien:
            continue
        if not ten:
            ten = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", f.parent.name).replace("-", " ").strip().capitalize()
        ung_vien[khoa] = {"ten": ten[:80], "link": link, "ten_mien": ten_mien, "thu_muc": thu_muc,
                          "nen_tang": _nen_tang(link, ten_mien), "tu": f.relative_to(_brain()).as_posix()}
    return list(ung_vien.values())[:60]


# ---------------------------------------------------------------- khách để lại thông tin (công khai)

_TAN_SUAT = {}


def _qua_tai(khoa, gioi_han, giay):
    now = time.time()
    with _KHOA:
        q = [t for t in _TAN_SUAT.get(khoa, []) if now - t < giay]
        if len(q) >= gioi_han:
            _TAN_SUAT[khoa] = q
            return True
        q.append(now)
        _TAN_SUAT[khoa] = q
        if len(_TAN_SUAT) > 5000:
            _TAN_SUAT.clear()
        return False


_KHONG_LUU = re.compile(r"pass|mat[-_ ]?khau|card|the[-_ ]?tin[-_ ]?dung|cvv|otp|token|secret", re.I)
CORS = {"access-control-allow-origin": "*", "access-control-allow-methods": "POST, OPTIONS",
        "access-control-allow-headers": "content-type", "access-control-max-age": "86400"}


def _ghi_khach_vao_bo_nao(w, ban_ghi):
    d = _thu_muc_du_lieu(w)
    f = d / "khach-de-lai-thong-tin.md"
    try:
        d.mkdir(parents=True, exist_ok=True)
        if not f.exists():
            f.write_text("---\ntype: du-lieu-web\ntitle: \"Khách để lại thông tin trên %s\"\nnguon: %s\n---\n\n"
                         "# Khách để lại thông tin trên %s\n\nMỗi dòng là một lần khách gửi form trên web (mới nhất ở cuối).\n\n"
                         % (w.get("ten"), w.get("ten_mien") or w.get("link"), w.get("ten")), encoding="utf-8")
        o = "; ".join("%s: %s" % (k, str(v).replace("\n", " ")) for k, v in ban_ghi["du_lieu"].items())
        with open(f, "a", encoding="utf-8") as fh:
            fh.write("- %s · %s\n" % (ban_ghi["luc"][:16].replace("T", " "), o))
    except OSError:
        pass


# ---------------------------------------------------------------- gắn vào app

def gan(app):

    @app.middleware("http")
    async def _tisa_web_mw(request: Request, call_next):
        if request.url.path == "/tisa-web":
            return RedirectResponse("/tisa-web/", status_code=302)
        return await call_next(request)

    @app.get("/tisa-web/")
    async def _trang():
        try:
            return HTMLResponse(TRANG.read_text(encoding="utf-8"), headers={"cache-control": "no-cache"})
        except OSError:
            return HTMLResponse("Thiếu trang quản lý web", status_code=500)

    def _cong_khai(request):
        try:
            import remote_tunnel
            st = remote_tunnel.MANAGER.status()
            if st.get("enabled") and st.get("url"):
                return st["url"].rstrip("/")
        except Exception:  # noqa: BLE001
            pass
        host = (request.headers.get("host") or "").split(":")[0]
        if host and host not in ("127.0.0.1", "localhost", "::1"):
            return "https://" + host
        return ""

    @app.get("/tisa-web/api/ds")
    async def _api_ds(request: Request):
        ds = _ds()
        ra = []
        for w in ds:
            x = dict(w)
            f = KHO / ("khach-%s.jsonl" % w["id"])
            x["so_khach"] = sum(1 for _ in open(f, encoding="utf-8")) if f.exists() else 0
            ra.append(x)
        return {"ds": ra, "cong_khai": _cong_khai(request)}

    @app.post("/tisa-web/api/luu")
    async def _api_luu(request: Request):
        b = await request.json()
        try:
            link = _chuan_link(b.get("link"))
            ten_mien = _chuan_link(b.get("ten_mien"))
            sheet = _chuan_link(b.get("sheet_csv")) if b.get("sheet_csv") else ""
        except ValueError as e:
            return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
        ten = str(b.get("ten") or "").strip()[:80]
        if not ten or not (link or ten_mien or b.get("thu_muc")):
            return JSONResponse({"ok": False, "error": "Cần tên web và ít nhất một link hoặc thư mục mã nguồn"}, status_code=400)
        thu_muc = str(b.get("thu_muc") or "").strip().strip("/")[:300]
        if ".." in thu_muc.split("/"):
            return JSONResponse({"ok": False, "error": "Thư mục không hợp lệ"}, status_code=400)
        with _KHOA:
            ds = _ds()
            w = _tim(ds, b.get("id")) if b.get("id") else None
            if w is None:
                w = {"id": "web_" + secrets.token_hex(5), "tao": _bay_gio(), "khoa": secrets.token_urlsafe(18),
                     "slug": _khong_dau(ten), "lich_su": []}
                ds.append(w)
            w.update(ten=ten, link=link, ten_mien=ten_mien, thu_muc=thu_muc, sheet_csv=sheet,
                     ghi_chu=str(b.get("ghi_chu") or "")[:1000], cap_nhat=_bay_gio(),
                     nen_tang=str(b.get("nen_tang") or "").strip()[:40] or _nen_tang(link, ten_mien) or "Khác")
            _luu_ds(ds)
        return {"ok": True, "web": w}

    @app.post("/tisa-web/api/xoa")
    async def _api_xoa(request: Request):
        b = await request.json()
        with _KHOA:
            ds = [w for w in _ds() if w.get("id") != b.get("id")]
            _luu_ds(ds)
        return {"ok": True}

    @app.post("/tisa-web/api/doi-khoa")
    async def _api_doi_khoa(request: Request):
        b = await request.json()
        with _KHOA:
            ds = _ds()
            w = _tim(ds, b.get("id"))
            if not w:
                return JSONResponse({"ok": False, "error": "Không thấy web"}, status_code=404)
            w["khoa"] = secrets.token_urlsafe(18)
            _luu_ds(ds)
        return {"ok": True, "khoa": w["khoa"]}

    @app.post("/tisa-web/api/kiem-tra")
    async def _api_kiem_tra(request: Request):
        b = await request.json()
        ds = _ds()
        chon = ds if b.get("tat_ca") else [w for w in ds if w.get("id") == b.get("id")]
        kqs = await asyncio.gather(*[_kiem_tra(w) for w in chon])
        with _KHOA:
            ds = _ds()
            for w0, kq in zip(chon, kqs):
                w = _tim(ds, w0["id"])
                if not w:
                    continue
                w["kiem_tra"] = kq
                ls = w.get("lich_su") or []
                ms = [m.get("ms") for m in kq["muc"] if m.get("ms")]
                ls.append({"luc": kq["luc"], "ok": kq["ok"], "ms": min(ms) if ms else None})
                w["lich_su"] = ls[-24:]
            _luu_ds(ds)
        return {"ok": True, "ket_qua": {w["id"]: k for w, k in zip(chon, kqs)}}

    @app.get("/tisa-web/api/tim")
    async def _api_tim():
        ds = _ds()
        da_co = set()
        for w in ds:
            for k in ("link", "ten_mien", "thu_muc"):
                if w.get(k):
                    da_co.add(str(w[k]).lower())
        return {"ung_vien": await asyncio.to_thread(_tim_trong_bo_nao, da_co)}

    @app.post("/tisa-web/api/lay-trang")
    async def _api_lay_trang(request: Request):
        b = await request.json()
        w = _tim(_ds(), b.get("id"))
        if not w:
            return JSONResponse({"ok": False, "error": "Không thấy web"}, status_code=404)
        url = w.get("ten_mien") or w.get("link")
        if not url:
            return JSONResponse({"ok": False, "error": "Web chưa có link"}, status_code=400)
        try:
            ma, cuoi, raw, ct, _ms = await _tai(url, 2_000_000)
        except ValueError as e:
            return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
        except Exception as e:  # noqa: BLE001
            return JSONResponse({"ok": False, "error": "Không tải được trang: " + type(e).__name__}, status_code=502)
        if not 200 <= ma < 400:
            return JSONResponse({"ok": False, "error": "Trang trả về mã %s" % ma}, status_code=502)
        d = _doc_html(raw, ct)
        chu = d.van_ban()[:60000]
        thu = _thu_muc_du_lieu(w)
        thu.mkdir(parents=True, exist_ok=True)
        f = thu / "noi-dung-trang.md"
        f.write_text("---\ntype: du-lieu-web\ntitle: \"Nội dung trang %s\"\nnguon: %s\nlay-luc: %s\n---\n\n"
                     "# %s\n\nNguồn: %s · lấy lúc %s. Đây là chữ hiển thị trên trang, dùng khi tư vấn khách về web này.\n\n"
                     "%s%s\n" % (w["ten"].replace('"', "'"), cuoi, _bay_gio(), d.tieu_de.strip() or w["ten"], cuoi, _bay_gio()[:16],
                                 ("> " + d.mo_ta.strip() + "\n\n") if d.mo_ta.strip() else "", chu), encoding="utf-8")
        it_chu = len(chu) < 300
        with _KHOA:
            ds = _ds()
            x = _tim(ds, w["id"])
            if x:
                x.setdefault("du_lieu", {})["trang"] = {"luc": _bay_gio(), "ky_tu": len(chu),
                                                        "tep": f.relative_to(_brain()).as_posix()}
                _luu_ds(ds)
        return {"ok": True, "tep": f.relative_to(_brain()).as_posix(), "ky_tu": len(chu),
                "canh_bao": "Trang ít chữ (có thể dựng bằng JavaScript), nên lấy thêm từ thư mục mã nguồn." if it_chu else ""}

    @app.post("/tisa-web/api/lay-sheet")
    async def _api_lay_sheet(request: Request):
        b = await request.json()
        w = _tim(_ds(), b.get("id"))
        if not w or not w.get("sheet_csv"):
            return JSONResponse({"ok": False, "error": "Chưa nhập link Google Sheet (CSV công khai)"}, status_code=400)
        try:
            ma, _cuoi, raw, _ct, _ms = await _tai(w["sheet_csv"], 3_000_000)
        except ValueError as e:
            return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
        except Exception as e:  # noqa: BLE001
            return JSONResponse({"ok": False, "error": "Không tải được bảng: " + type(e).__name__}, status_code=502)
        if not 200 <= ma < 400:
            return JSONResponse({"ok": False, "error": "Bảng trả về mã %s (đã bật Xuất bản lên web dạng CSV chưa?)" % ma}, status_code=502)
        txt = raw.decode("utf-8-sig", errors="replace")
        if txt.lstrip().lower().startswith(("<!doctype", "<html")):
            return JSONResponse({"ok": False, "error": "Link chưa phải CSV. Trong Google Sheet: Tệp → Chia sẻ → Xuất bản lên web → chọn CSV."}, status_code=400)
        dong = list(csv.reader(io.StringIO(txt)))
        dong = [d for d in dong if any(c.strip() for c in d)]
        if not dong:
            return JSONResponse({"ok": False, "error": "Bảng trống"}, status_code=400)
        dau, than = dong[0], dong[1:501]
        o = lambda c: str(c).replace("|", "/").replace("\n", " ").strip()[:200]
        bang = "| " + " | ".join(o(c) for c in dau) + " |\n|" + "---|" * len(dau) + "\n" + \
               "\n".join("| " + " | ".join(o(c) for c in (d + [""] * (len(dau) - len(d)))[:len(dau)]) + " |" for d in than)
        thu = _thu_muc_du_lieu(w)
        thu.mkdir(parents=True, exist_ok=True)
        f = thu / "du-lieu-google-sheet.md"
        f.write_text("---\ntype: du-lieu-web\ntitle: \"Dữ liệu Google Sheet của %s\"\nlay-luc: %s\n---\n\n# Dữ liệu Google Sheet của %s\n\n"
                     "%s dòng (tối đa 500 dòng đầu), lấy lúc %s.\n\n%s\n" % (w["ten"].replace('"', "'"), _bay_gio(), w["ten"],
                                                                              len(than), _bay_gio()[:16], bang), encoding="utf-8")
        with _KHOA:
            ds = _ds()
            x = _tim(ds, w["id"])
            if x:
                x.setdefault("du_lieu", {})["sheet"] = {"luc": _bay_gio(), "dong": len(than), "tep": f.relative_to(_brain()).as_posix()}
                _luu_ds(ds)
        return {"ok": True, "dong": len(than), "tep": f.relative_to(_brain()).as_posix()}

    @app.get("/tisa-web/api/khach")
    async def _api_khach(id: str):
        f = KHO / ("khach-%s.jsonl" % re.sub(r"[^\w]", "", id))
        ra = []
        if f.exists():
            for dong in f.read_text(encoding="utf-8").splitlines()[-300:]:
                try:
                    ra.append(json.loads(dong))
                except ValueError:
                    pass
        return {"khach": list(reversed(ra))}

    # ---------- công khai: web gửi form khách về TISA BOT ----------
    @app.options("/tisa-web/thu/{khoa}")
    async def _thu_options(khoa: str):
        return Response(status_code=204, headers=CORS)

    @app.post("/tisa-web/thu/{khoa}")
    async def _thu(khoa: str, request: Request):
        ip = request.headers.get("cf-connecting-ip") or (request.client.host if request.client else "?")
        if _qua_tai("ip:" + ip, 8, 60) or _qua_tai("web:" + khoa[:40], 300, 3600):
            return JSONResponse({"ok": False, "error": "Gửi quá nhiều, thử lại sau"}, status_code=429, headers=CORS)
        w = next((x for x in _ds() if secrets.compare_digest(str(x.get("khoa") or ""), khoa)), None)
        if not w:
            return JSONResponse({"ok": False, "error": "Địa chỉ nhận không đúng"}, status_code=404, headers=CORS)
        raw = await request.body()
        if len(raw) > 16_000:
            return JSONResponse({"ok": False, "error": "Dữ liệu quá lớn"}, status_code=413, headers=CORS)
        ct = request.headers.get("content-type", "")
        try:
            if "json" in ct:
                data = json.loads(raw.decode("utf-8") or "{}")
            else:
                from urllib.parse import parse_qsl
                data = dict(parse_qsl(raw.decode("utf-8", errors="replace"), keep_blank_values=True))
        except ValueError:
            return JSONResponse({"ok": False, "error": "Dữ liệu không đọc được"}, status_code=400, headers=CORS)
        if not isinstance(data, dict):
            return JSONResponse({"ok": False, "error": "Dữ liệu phải là các ô tên: giá trị"}, status_code=400, headers=CORS)
        if any(str(data.get(k) or "").strip() for k in ("_gotcha", "_hp", "website_url")):
            return JSONResponse({"ok": True}, headers=CORS)          # bẫy máy spam: trả ok nhưng không lưu
        sach = {}
        for k, v in list(data.items())[:40]:
            k = str(k).strip()[:60]
            if not k or k.startswith("_") or _KHONG_LUU.search(k):
                continue
            sach[k] = (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)).strip()[:1000]
        if not sach:
            return JSONResponse({"ok": False, "error": "Form trống"}, status_code=400, headers=CORS)
        ban_ghi = {"luc": _bay_gio(), "trang": (request.headers.get("referer") or "")[:300], "du_lieu": sach}
        with _KHOA:
            KHO.mkdir(parents=True, exist_ok=True)
            with open(KHO / ("khach-%s.jsonl" % w["id"]), "a", encoding="utf-8") as fh:
                fh.write(json.dumps(ban_ghi, ensure_ascii=False) + "\n")
        await asyncio.to_thread(_ghi_khach_vao_bo_nao, w, ban_ghi)
        if "json" not in (request.headers.get("accept") or "") and "json" not in ct and "text/html" in (request.headers.get("accept") or ""):
            sau = str(data.get("_next") or "")
            hop = sau.startswith(("https://", "http://")) and urlparse(sau).hostname in (
                urlparse(w.get("link") or "").hostname, urlparse(w.get("ten_mien") or "").hostname)
            if hop:
                return RedirectResponse(sau, status_code=303)
            return HTMLResponse("<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
                                "<body style='font-family:system-ui;display:grid;place-items:center;height:90vh;text-align:center'>"
                                "<div><h2>Đã gửi thông tin</h2><p>Cảm ơn bạn, chúng tôi sẽ liên hệ sớm.</p></div>", headers=CORS)
        return JSONResponse({"ok": True}, headers=CORS)
