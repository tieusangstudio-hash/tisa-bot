"""tisa_web_thong_tin.py - Thông tin THẬT của các web mẫu trong trang Quản lý web (V3.34, chủ yêu cầu 19/11/2026).

1. TÊN MIỀN, TÊN WEB, SEO: thẻ Web CRM và Lead/Sale Page hiện đúng tên miền đang chạy thật, tên web, tiêu đề + mô tả + ảnh chia sẻ (SEO) lấy từ chính web đó.
   Nguồn thông tin: (a) hồ sơ cộng sự Quản Trị WEB ghi vào bộ não (`04-ket-qua/web/<ngày-tên>/ghi-chep.md`, khóa `thu-muc-ma`, `link`, `ten-mien`, `ten-web`),
   (b) chủ đặt tay ("Đặt tên miền"), (c) địa chỉ công khai CRM đã đặt sẵn. Khi tên miền đổi, ghi chép mới hơn thắng, thẻ tự đổi.
   SEO đọc từ web thật (tải công khai, chặn mạng nội bộ), nhớ 10 phút, làm mới ở luồng nền, không làm chậm trang.
2. ĐỔI THÔNG TIN ĐĂNG NHẬP admin của Web CRM trên máy (tên đăng nhập là email, tên hiển thị, mật khẩu): dành cho người quên mật khẩu.
   Ghi thẳng vào cơ sở dữ liệu CRM (.local/app.sqlite), băm pbkdf2 đúng định dạng CRM dùng, thu hồi mọi phiên đăng nhập cũ (CRM gắn phiên với bản băm mật khẩu).
   Mật khẩu không bao giờ được lưu hay ghi nhật ký, chỉ bản băm nằm trong cơ sở dữ liệu CRM.
Mô-đun này không import tisa_web_mau (tránh vòng lặp): tisa_web_mau.gan() truyền chính nó vào gan_them().
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import os
import re
import secrets
import sqlite3
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

CHU_OPENID = "local:owner"
VONG_BAM = 100000
MAT_KHAU_YEU = {"123456", "12345678", "123456789", "password", "matkhau", "admin123", "11111111", "00000000", "qwertyui", "iloveyou"}
TTL_SEO = 600          # giây
TTL_SEO_LOI = 300
_NEN = {}              # khóa -> đang làm mới
_KHOA_NEN = threading.Lock()
_RE_EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


# ================================================================ 2. đăng nhập admin của Web CRM
def _bam(mat_khau: str) -> str:
    muoi = secrets.token_bytes(16)
    h = hashlib.pbkdf2_hmac("sha256", mat_khau.encode("utf-8"), muoi, VONG_BAM, 32)
    return "pbkdf2$%d$%s$%s" % (VONG_BAM, base64.b64encode(muoi).decode(), base64.b64encode(h).decode())


def kiem_mat_khau(mat_khau: str, ma_bam: str) -> bool:
    try:
        a, n, muoi, muon = (ma_bam or "").split("$")
        if a != "pbkdf2":
            return False
        h = hashlib.pbkdf2_hmac("sha256", mat_khau.encode("utf-8"), base64.b64decode(muoi), int(n), 32)
        return secrets.compare_digest(h, base64.b64decode(muon))
    except Exception:  # noqa: BLE001
        return False


def _db(goc_crm: Path) -> sqlite3.Connection:
    p = Path(goc_crm) / ".local" / "app.sqlite"
    if not p.is_file():
        raise ValueError("CRM chưa có dữ liệu trên máy này. Bấm Chạy cho Web CRM một lần rồi quay lại đổi đăng nhập.")
    c = sqlite3.connect(str(p), timeout=20)
    c.row_factory = sqlite3.Row
    return c


def doc_dang_nhap(goc_crm: Path) -> dict:
    """Thông tin đăng nhập hiện tại của admin (KHÔNG có mật khẩu): email, tên hiển thị, còn mật khẩu xem thử 123456 hay không."""
    c = _db(goc_crm)
    try:
        u = c.execute("SELECT email,name,passwordHash FROM users WHERE openId=?", (CHU_OPENID,)).fetchone()
    finally:
        c.close()
    if not u:
        raise ValueError("Không thấy tài khoản quản trị trong CRM này.")
    return {"email": u["email"] or "", "ten": u["name"] or "", "mac_dinh": kiem_mat_khau("123456", u["passwordHash"])}


def _kiem_dau_vao(email: str, ten: str, mat_khau: str, mat_khau2: str | None):
    email, ten = str(email or "").strip().lower(), str(ten or "").strip()
    if not _RE_EMAIL.match(email) or len(email) > 120:
        raise ValueError("Email đăng nhập chưa đúng. Dạng đúng: ten@gmail.com (CRM đăng nhập bằng email).")
    if not 1 <= len(ten) <= 60:
        raise ValueError("Tên hiển thị từ 1 đến 60 ký tự.")
    mk = str(mat_khau or "")
    if len(mk) < 8 or len(mk) > 100:
        raise ValueError("Mật khẩu mới từ 8 đến 100 ký tự.")
    if mat_khau2 is not None and mk != str(mat_khau2):
        raise ValueError("Hai lần nhập mật khẩu chưa giống nhau.")
    if mk.lower() in MAT_KHAU_YEU or mk.lower() == email or mk.lower() == email.split("@")[0]:
        raise ValueError("Mật khẩu này quá dễ đoán. Chọn mật khẩu khác, nên có cả chữ và số.")
    return email, ten, mk


def doi_dang_nhap(goc_crm: Path, email: str, ten: str, mat_khau: str, mat_khau2: str | None = None) -> dict:
    """Đặt email đăng nhập, tên hiển thị và mật khẩu mới cho admin của CRM. Trả {email, ten}; ném ValueError kèm lời giải thích."""
    email, ten, mk = _kiem_dau_vao(email, ten, mat_khau, mat_khau2)
    goc_crm = Path(goc_crm)
    c = _db(goc_crm)
    bay_gio = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    try:
        u = c.execute("SELECT id FROM users WHERE openId=?", (CHU_OPENID,)).fetchone()
        if not u:
            raise ValueError("Không thấy tài khoản quản trị trong CRM này.")
        khac = c.execute("SELECT id FROM users WHERE id<>? AND (lower(email)=? OR canonicalEmail=?)", (u["id"], email, email)).fetchone()
        if khac:
            raise ValueError("Email này đang được tài khoản khác trong CRM dùng. Chọn email khác.")
        try:
            c.execute("UPDATE users SET name=?, email=?, canonicalEmail=?, passwordHash=?, loginMethod='nova-password', updatedAt=? WHERE id=?",
                      (ten, email, email, _bam(mk), bay_gio, u["id"]))
        except sqlite3.IntegrityError:
            raise ValueError("Email này đang được tài khoản khác trong CRM dùng. Chọn email khác.")
        # Thu hồi các thiết bị đang đăng nhập: người dùng đặt lại vì quên/lộ mật khẩu thì phiên cũ không được sống tiếp.
        try:
            c.execute("DELETE FROM loginDevices WHERE userId=?", (u["id"],))
        except sqlite3.Error:
            pass
        c.commit()
    finally:
        c.close()
    # ownerEmail phải khớp: CRM so email tài khoản với ownerEmail (đọc lúc khởi động) để biết ai là chủ hệ thống.
    bj = goc_crm / "template" / "business.json"
    try:
        d = json.loads(bj.read_text(encoding="utf-8"))
        d["ownerEmail"] = email
        tam = bj.with_suffix(".tmp")
        tam.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(tam, bj)
    except (OSError, ValueError):
        pass
    return {"email": email, "ten": ten}


# ================================================================ 1. tên miền, tên web, SEO
def _bay_gio() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _khoa_dau(s: str) -> str:
    return re.sub(r"\s+", " ", str(s or "")).strip()


def quet_ghi_chep(brain: Path, toi_da: int = 3000) -> list[dict]:
    """Các hồ sơ web trong bộ não (khóa `thu-muc-ma` để biết thuộc web mẫu nào). Mỗi hồ sơ: link, ten_mien, ten_web, thu_muc_ma, luc (mtime)."""
    goc = Path(brain) / "04-ket-qua"
    kq = []
    if not goc.is_dir():
        return kq
    n = 0
    for f in goc.rglob("*.md"):
        n += 1
        if n > toi_da:
            break
        try:
            if f.stat().st_size > 200_000:
                continue
            t = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        m = re.match(r"^---\r?\n(.*?)\r?\n---", t, re.S)
        if not m:
            continue
        kv = {}
        for dong in m.group(1).splitlines():
            k, _, v = dong.partition(":")
            kv[k.strip().lower()] = v.strip().strip("'\"")
        if kv.get("loai", "").lower() not in ("web", "website", "trang-web"):
            continue
        tm = kv.get("thu-muc-ma") or ""
        if not tm:
            mm = re.search(r"^- Mã nguồn:\s*(.+)$", t, re.M)
            tm = mm.group(1).strip() if mm else ""
        if not tm:
            continue
        kq.append({"thu_muc_ma": tm, "link": kv.get("link") or kv.get("url") or "", "ten_mien": kv.get("ten-mien") or kv.get("domain") or "",
                   "ten_web": kv.get("ten-web") or "", "nen_tang": kv.get("nen-tang") or "", "luc": f.stat().st_mtime, "tep": str(f)})
    kq.sort(key=lambda x: x["luc"])
    return kq


def _trong(p: Path, thu_muc: Path) -> bool:
    try:
        Path(os.path.realpath(os.path.expanduser(str(p)))).relative_to(Path(os.path.realpath(str(thu_muc))))
        return True
    except (ValueError, OSError):
        return False


def khop_ghi_chep(ds_ghi_chep: list[dict], bo: dict, trang: list[dict], goc: Path) -> dict:
    """{id mục: hồ sơ mới nhất} cho bộ và các trang. Trang (thư mục sâu hơn) được xét trước bộ."""
    kq = {}
    thu_trang = [(t, goc / t.get("thu_muc_con", "lead")) for t in trang]
    for r in ds_ghi_chep:                       # đã sắp cũ -> mới, mục sau đè mục trước
        p = Path(r["thu_muc_ma"])
        da = False
        for t, d in thu_trang:
            if _trong(p, d):
                kq[t["id"]] = r
                da = True
                break
        if not da and (_trong(p, goc / "crm") or os.path.realpath(os.path.expanduser(str(p))) == os.path.realpath(str(goc))):
            kq[bo["id"]] = r
    return kq


def _chuan_link(u: str) -> str:
    u = _khoa_dau(u)
    if not u:
        return ""
    if not re.match(r"^https?://", u, re.I):
        u = "https://" + u
    p = urlparse(u)
    if p.scheme not in ("http", "https") or not p.hostname or len(u) > 500 or " " in u:
        raise ValueError("Địa chỉ không hợp lệ. Dạng đúng: https://ten-mien-cua-ban.com")
    return u.rstrip("/") if p.path in ("", "/") else u


MIEN_TAM = (".workers.dev", ".pages.dev", ".trycloudflare.com", ".vercel.app", ".netlify.app", ".ngrok-free.app", ".ngrok.io", ".github.io")


def la_mien_rieng(link: str) -> bool:
    h = (urlparse(link or "").hostname or "").lower()
    return bool(h) and h not in ("localhost", "127.0.0.1", "::1") and not h.endswith(MIEN_TAM) and "." in h


async def _lay_seo_async(url: str) -> dict:
    import tisa_web as W
    ma, cuoi, buf, loai, ms = await W._tai(url, 400_000)
    kq = {"luc": time.time(), "ma": ma, "ms": ms, "url_cuoi": cuoi}
    if ma >= 400:
        kq["loi"] = "Web trả mã %s" % ma
        return kq
    if "html" not in (loai or "").lower() and buf[:1] != b"<":
        kq["loi"] = "Không phải trang web (HTML)"
        return kq
    p = W._Doc()
    try:
        p.feed(buf.decode("utf-8", "replace"))
    except Exception:  # noqa: BLE001
        pass
    og = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']*)', buf.decode("utf-8", "replace"), re.I)
    kq["tieu_de"] = _khoa_dau(p.tieu_de)[:160]
    kq["tieu_de_chia_se"] = _khoa_dau(og.group(1))[:160] if og else ""
    kq["mo_ta"] = _khoa_dau(p.mo_ta)[:300]
    kq["anh"] = urljoin(cuoi, p.anh)[:500] if p.anh else ""
    kq["icon"] = urljoin(cuoi, p.icon)[:500] if p.icon else ""
    return kq


def lay_seo(url: str) -> dict:
    """Đọc SEO của web thật (đồng bộ, tối đa ~15 giây). Luôn trả dict, lỗi nằm ở khóa `loi`."""
    try:
        return asyncio.run(_lay_seo_async(url))
    except ValueError as e:
        return {"luc": time.time(), "loi": str(e)[:120]}
    except Exception as e:  # noqa: BLE001
        ten = type(e).__name__
        return {"luc": time.time(), "loi": {"ConnectTimeout": "Hết thời gian chờ kết nối", "ReadTimeout": "Web phản hồi quá chậm", "ConnectError": "Không kết nối được (tên miền chưa trỏ đúng hoặc web đã tắt)"}.get(ten, "Lỗi kết nối: " + ten)}


def link_that(item: dict, loai: str, cong_khai: str, bo: dict | None) -> str:
    """Địa chỉ web đang chạy thật của một thẻ, theo thứ tự ưu tiên: tên miền riêng đã đặt > link đã đặt > link công khai mặc định."""
    w = item.get("web") or {}
    if w.get("ten_mien"):
        return w["ten_mien"]
    if w.get("link"):
        return w["link"]
    if loai == "bo":
        return (item.get("crm_public") or "").rstrip("/")
    if cong_khai:
        return "%s/tisa-web/trang/%s/" % (cong_khai, item.get("slug"))
    return ""


def _nen_seo(M, loai: str, ma: str, url: str, cong_khai: str = "") -> None:
    """Luồng nền: đọc SEO rồi ghi vào mau.json. Mỗi mục một luồng một lúc."""
    khoa = loai + ":" + ma
    with _KHOA_NEN:
        if _NEN.get(khoa):
            return
        _NEN[khoa] = True

    def lam():
        try:
            kq = lay_seo(url)
            with M._KHOA:
                d = M._mac_dinh(M._doc())
                x = M._tim(d["bo"] if loai == "bo" else d["trang"], ma)
                # Trong lúc đọc, chủ hay cộng sự có thể đã đổi tên miền: kết quả của địa chỉ cũ không được đè lên thẻ.
                if x is not None and link_that(x, loai, cong_khai, None) == url:
                    w = x.setdefault("web", {})
                    kq["url"] = url
                    w["seo"] = kq
                    M._ghi(d)
        except Exception:  # noqa: BLE001
            pass
        finally:
            with _KHOA_NEN:
                _NEN.pop(khoa, None)
    threading.Thread(target=lam, daemon=True, name="tisa-web-seo").start()


def lam_giau(M, d: dict, cong_khai: str, brain: Path) -> bool:
    """Gộp hồ sơ web trong bộ não vào d (tại chỗ). Trả True nếu d đổi (cần ghi). Rồi xếp việc đọc SEO nền cho thẻ nào cũ quá 10 phút."""
    doi = False
    try:
        ds = quet_ghi_chep(brain)
    except Exception:  # noqa: BLE001
        ds = []
    for b in d["bo"]:
        goc = M._goc(b)
        trang = [t for t in d["trang"] if t.get("bo") == b["id"]]
        khop = khop_ghi_chep(ds, b, trang, goc) if ds else {}
        for loai, it in [("bo", b)] + [("trang", t) for t in trang]:
            r = khop.get(it["id"])
            if r:
                w = it.setdefault("web", {})
                if float(w.get("ghi_chep_luc") or 0) < r["luc"]:
                    try:
                        link = _chuan_link(r["link"])
                        mien = _chuan_link(r["ten_mien"])
                    except ValueError:
                        link = mien = ""
                    thay = (w.get("link") or "", w.get("ten_mien") or "") != (link, mien)
                    w.update(link=link, ten_mien=mien, nen_tang=r.get("nen_tang") or w.get("nen_tang") or "", tu="ghi-chep", ghi_chep_luc=r["luc"], luc=_bay_gio())
                    if r.get("ten_web") and r["ten_web"] != w.get("ten_web"):
                        w["ten_web"] = r["ten_web"][:80]
                        it["ten"] = r["ten_web"][:80]
                    if thay:
                        w.pop("seo", None)          # đổi tên miền thì thông tin SEO cũ hết đúng
                    doi = True
            u = link_that(it, loai, cong_khai, b if loai == "trang" else None)
            seo = (it.get("web") or {}).get("seo") or {}
            if u and u.startswith("http") and la_web_ngoai(u):
                tuoi = time.time() - float(seo.get("luc") or 0)
                if tuoi > (TTL_SEO_LOI if seo.get("loi") else TTL_SEO) or seo.get("url") != u:
                    _nen_seo(M, loai, it["id"], u, cong_khai)
    return doi


def la_web_ngoai(u: str) -> bool:
    h = (urlparse(u).hostname or "").lower()
    return bool(h) and h not in ("localhost", "127.0.0.1", "::1") and not re.match(r"^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)", h)


def hien_thi(it: dict, loai: str, cong_khai: str) -> dict:
    """Phần JSON cho giao diện: địa chỉ đang chạy, có phải tên miền riêng, tên web, SEO."""
    w = it.get("web") or {}
    u = link_that(it, loai, cong_khai, None)
    seo = w.get("seo") or {}
    return {"link": u, "host": (urlparse(u).hostname or "") if u else "", "mien_rieng": la_mien_rieng(u), "ten_web": w.get("ten_web") or "",
            "nen_tang": w.get("nen_tang") or "", "tu": w.get("tu") or "", "luc": w.get("luc") or "",
            "seo": {k: seo.get(k) for k in ("tieu_de", "tieu_de_chia_se", "mo_ta", "anh", "icon", "luc", "ma", "ms", "loi") if seo.get(k) not in (None, "")}}


# ================================================================ đường API
def gan_them(app, M) -> None:
    """Thêm các đường vào trang Quản lý web. M = mô-đun tisa_web_mau (dùng _doc, _ghi, _KHOA, _tim, _mac_dinh, _goc, _cong_mo)."""
    from fastapi import Request
    from fastapi.responses import JSONResponse
    globals()["Request"] = Request

    def loi(m, ma=400):
        return JSONResponse({"ok": False, "error": str(m)[:300]}, status_code=ma)

    async def than(request) -> dict:
        try:
            b = await request.json()
            return b if isinstance(b, dict) else {}
        except Exception:  # noqa: BLE001
            return {}

    def tim_bo(i):
        return M._tim(M._mac_dinh(M._doc())["bo"], i)

    @app.get("/tisa-web/api/mau/dang-nhap")
    async def _dn(bo: str = ""):
        x = tim_bo(bo)
        if not x:
            return loi("Không thấy bộ web", 404)
        try:
            return {"ok": True, **(await asyncio.to_thread(doc_dang_nhap, M._goc(x) / "crm")), "dang_chay": bool(M._cua_minh(x) and M._cong_mo(x["cong_crm"]))}
        except ValueError as e:
            return loi(e)

    @app.post("/tisa-web/api/mau/doi-dang-nhap")
    async def _doi_dn(request: Request):
        b = await than(request)
        x = tim_bo(b.get("bo"))
        if not x:
            return loi("Không thấy bộ web", 404)
        try:
            kq = await asyncio.to_thread(doi_dang_nhap, M._goc(x) / "crm", b.get("email"), b.get("ten"), b.get("mat_khau"), b.get("mat_khau2"))
        except ValueError as e:
            return loi(e)
        except sqlite3.Error as e:
            return loi("Chưa ghi được vào dữ liệu CRM (%s). Tắt CRM rồi thử lại." % type(e).__name__)
        with M._KHOA:
            d = M._mac_dinh(M._doc())
            y = M._tim(d["bo"], x["id"])
            if y is not None:
                y["admin"] = {"email": kq["email"], "ten": kq["ten"], "doi_luc": _bay_gio()}
                M._ghi(d)
        dang_chay = bool(M._cua_minh(x) and M._cong_mo(x["cong_crm"]))
        return {"ok": True, **kq, "dang_chay": dang_chay, "can_khoi_dong_lai": dang_chay}

    @app.post("/tisa-web/api/mau/dat-web")
    async def _dat_web(request: Request):
        """Chủ (hay giao diện) đặt tên miền / link / tên web cho một thẻ. Link trống = bỏ, quay về link mặc định."""
        b = await than(request)
        loai = "trang" if b.get("loai") == "trang" else "bo"
        try:
            link, mien = _chuan_link(b.get("link")), _chuan_link(b.get("ten_mien"))
        except ValueError as e:
            return loi(e)
        ten = _khoa_dau(b.get("ten_web"))[:80]
        with M._KHOA:
            d = M._mac_dinh(M._doc())
            x = M._tim(d["bo"] if loai == "bo" else d["trang"], b.get("id"))
            if not x:
                return loi("Không thấy web này", 404)
            w = x.setdefault("web", {})
            w.update(link=link, ten_mien=mien, tu="tay", luc=_bay_gio(), ghi_chep_luc=time.time())   # tay đặt = mới nhất, hồ sơ cũ hơn không đè
            w.pop("seo", None)
            if ten:
                w["ten_web"] = ten
                x["ten"] = ten
            if loai == "bo" and (mien or link):
                x["crm_public"] = (mien or link).rstrip("/")
            elif loai == "bo":
                x.pop("crm_public", None)
            M._ghi(d)
        return {"ok": True}

    @app.post("/tisa-web/api/mau/lam-moi")
    async def _lam_moi(request: Request):
        """Đọc lại tên web, SEO (tiêu đề, mô tả, ảnh chia sẻ) từ web thật ngay."""
        b = await than(request)
        loai = "trang" if b.get("loai") == "trang" else "bo"
        d = M._mac_dinh(M._doc())
        x = M._tim(d["bo"] if loai == "bo" else d["trang"], b.get("id"))
        if not x:
            return loi("Không thấy web này", 404)
        u = link_that(x, loai, str(b.get("cong_khai") or ""), None)
        if not u or not u.startswith("http") or not la_web_ngoai(u):
            return loi("Web này chưa có địa chỉ công khai để kiểm tra. Đặt tên miền hoặc bật Truy cập từ xa trước.")
        seo = await asyncio.to_thread(lay_seo, u)
        seo["url"] = u
        with M._KHOA:
            d = M._mac_dinh(M._doc())
            y = M._tim(d["bo"] if loai == "bo" else d["trang"], x["id"])
            if y is not None and link_that(y, loai, str(b.get("cong_khai") or ""), None) == u:
                y.setdefault("web", {})["seo"] = seo
                M._ghi(d)
        return {"ok": not seo.get("loi"), "seo": seo, "error": seo.get("loi") or ""}
