"""Giao việc cho MÁY KHÁC trong Nhiều máy (bản thử, chủ yêu cầu 21/11/2026).

Chủ muốn: gõ xong yêu cầu trong ô chat (Hỏi nhanh hoặc một cộng sự như Dũng Edit) thì chọn được "máy nào làm việc này".
Cách làm:
  - Máy A (máy anh đang mở trang) gửi việc sang máy B qua ĐỊA CHỈ RIÊNG của B (đường hầm B báo lên Trạm mỗi nhịp).
  - Lời gọi giữa hai máy ký bằng khóa suy ra từ KHÓA BỘ NÃO: chỉ máy đã ghép (biết mật khẩu bộ não) mới ký được.
    Có giờ ký (lệch tối đa 5 phút), số dùng một lần, và máy gửi phải có trong sổ máy của Trạm. Mọi việc nhận đều ghi nhật ký.
  - B chạy việc ở nền bằng đúng đường của /chat (cùng cộng sự, cùng bộ não), trong một cuộc trò chuyện riêng mang tên phiên của A,
    nên hỏi tiếp trong cùng khung chat thì B vẫn nhớ ngữ cảnh. A hỏi tiến độ mỗi vài giây, trang vẽ kết quả vào khung chat.
Đường của B (/tisa-nhieu-may/nhan/...) không cần cookie đăng nhập (máy A không có), nên tự kiểm chữ ký ở đây.
"""
from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import re
import secrets
import time
import urllib.error
import urllib.request

import tisa_nhieu_may as NM

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

GIAO = NM.NM / "giao-di.json"        # việc máy này đã giao cho máy khác (để vẽ lại sau khi tải lại trang)
NHAN = NM.NM / "nhan-ve.json"        # việc máy này nhận từ máy khác (kết quả giữ lại để máy kia hỏi)
LECH_GIO = 300
GIU_TOI_DA = 200
TIEN_DO_TOI_DA = 40

_dung_roi = {}                       # số dùng một lần đã gặp -> lúc gặp
_nhan = {}                           # id -> việc đang/đã làm cho máy khác
_khoa_viec = None


def _khoa():
    global _khoa_viec
    if _khoa_viec is None:
        import threading
        _khoa_viec = threading.RLock()
    return _khoa_viec


# ================================================================ chữ ký giữa các máy
def _khoa_ky() -> bytes:
    return hmac.new(NM._khoa_nao(), b"tisa-giao-may-v1", hashlib.sha256).digest()


def _chuoi_ky(method: str, duong: str, luc: str, so: str, than: bytes) -> bytes:
    return "\n".join([method.upper(), duong, luc, so, hashlib.sha256(than or b"").hexdigest()]).encode()


def ky(method: str, duong: str, than: bytes = b"") -> str:
    c = NM.cau_hinh()
    luc, so = str(int(time.time())), secrets.token_hex(12)
    chu_ky = hmac.new(_khoa_ky(), _chuoi_ky(method, duong, luc, so, than), hashlib.sha256).hexdigest()
    return "%s.%s.%s.%s" % (c.get("may_id") or "", luc, so, chu_ky)


def _may_trong_so(may_id: str) -> dict:
    for m in ((NM._tt.get("nhip") or {}).get("may") or []):
        if m.get("id") == may_id:
            return m
    return {}


def kiem_ky(method: str, duong: str, than: bytes, dau: str) -> str:
    """Trả mã máy gửi nếu chữ ký đúng; sai thì ném ValueError (kèm lý do để ghi nhật ký, không trả chi tiết ra ngoài)."""
    if not NM.dang_bat():
        raise ValueError("máy này chưa nối Trạm")
    p = (dau or "").split(".")
    if len(p) != 4 or not re.fullmatch(r"[A-Za-z0-9]{6,40}", p[0]) or not p[1].isdigit() or not re.fullmatch(r"[0-9a-f]{24}", p[2]):
        raise ValueError("chữ ký sai dạng")
    may_id, luc, so, chu_ky = p
    if abs(time.time() - int(luc)) > LECH_GIO:
        raise ValueError("chữ ký quá hạn (giờ hai máy lệch nhau quá 5 phút?)")
    if may_id == NM.cau_hinh().get("may_id"):
        raise ValueError("máy tự gửi cho chính nó")
    if not _may_trong_so(may_id):
        raise ValueError("máy gửi không có trong sổ máy của Trạm")
    dung = hmac.new(_khoa_ky(), _chuoi_ky(method, duong, luc, so, than), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(dung, chu_ky):
        raise ValueError("chữ ký không khớp (khác bộ não?)")
    now = time.time()
    for k in [k for k, v in _dung_roi.items() if now - v > LECH_GIO * 2]:
        _dung_roi.pop(k, None)
    if so in _dung_roi:
        raise ValueError("chữ ký đã dùng rồi")
    _dung_roi[so] = now
    return may_id


def _goi_may(may: dict, method: str, duong: str, body=None, cho=30) -> dict:
    dia_chi = (may.get("dia_chi") or "").rstrip("/")
    if not dia_chi:
        raise ValueError("Máy %s chưa có địa chỉ (đường hầm chưa bật). Chờ 1 phút rồi thử lại." % (may.get("ten") or ""))
    than = json.dumps(body, ensure_ascii=False).encode() if body is not None else b""
    h = {"User-Agent": "tisa-bot-may", "Accept": "application/json", "X-Tisa-May": ky(method, duong, than)}
    if body is not None:
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(dia_chi + duong, data=than if body is not None else None, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=cho) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            d = json.loads(e.read().decode() or "{}")
        except ValueError:
            d = {}
        if not d.get("loi") and e.code in (401, 404, 405):   # máy kia còn bản cũ: chưa có đường nhận việc
            raise ValueError("Máy %s chưa có bản TISA BOT mới nên chưa nhận việc từ máy khác được. Cập nhật TISA BOT trên máy đó rồi thử lại."
                             % (may.get("ten") or ""))
        raise ValueError(d.get("loi") or "Máy %s trả lỗi %s" % (may.get("ten") or "", e.code))
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise ValueError("Không gọi được máy %s: %s" % (may.get("ten") or "", getattr(e, "reason", e)))


# ================================================================ danh sách máy cho nút "Máy làm"
def may_lam() -> dict:
    c = NM.cau_hinh()
    if not NM.dang_bat():
        return {"ok": True, "bat": False, "may_nay": {"ten": NM.ten_may(), "may_that": NM._ten_may_he()}, "may": []}
    toi = c.get("may_id")
    n = NM._tt.get("nhip") or {}
    vai = n.get("vai") or {}
    chu = (vai.get("cong") or {}).get("may_id")
    ds = []
    for m in n.get("may") or []:
        giu = [k for k, v in vai.items() if (v or {}).get("may_id") == m.get("id")]
        ds.append({"id": m.get("id"), "ten": m.get("ten") or m.get("id"), "he": m.get("he") or "", "dang_bat": bool(m.get("dang_bat")),
                   "la_may_nay": m.get("id") == toi, "la_chu": m.get("id") == chu, "co_dia_chi": bool(m.get("dia_chi")),
                   "viec_nang": "viec_nang" in giu})
    ds.sort(key=lambda x: (not x["la_may_nay"], not x["la_chu"], x["ten"].lower()))
    la_chu = chu == toi if chu else ("cong" in (NM._doc(NM.VAI_TT, {}) or {}).get("giu", []))
    return {"ok": True, "bat": True, "may_nay": {"id": toi, "ten": NM.ten_may(), "la_chu": bool(la_chu), "may_that": NM._ten_may_he()},
            "may": ds, "luc_nhip": NM._tt.get("luc_nhip")}


# ================================================================ máy A: giao đi, hỏi tiến độ
def _doc_giao() -> list:
    d = NM._doc(GIAO, []) or []
    return d if isinstance(d, list) else []


def _luu_giao(ds: list) -> None:
    NM._ghi(GIAO, ds[-GIU_TOI_DA:])


def _brain_tuong_doi(brain: str) -> str:
    """Đường dẫn bộ não của máy này -> tên tương đối trong brains/ (mỗi máy để brains ở chỗ khác nhau)."""
    b = (brain or "").strip()
    if not b or b == "brain":
        return ""
    try:
        from pathlib import Path
        return Path(b).resolve().relative_to(NM.BRAINS_DIR.resolve()).as_posix()
    except (ValueError, OSError):
        return ""


def giao(may_id: str, loi_nhan: str, agent: str = "", brain: str = "", phien: str = "", ten_cong_su: str = "") -> dict:
    loi_nhan = (loi_nhan or "").strip()
    if not loi_nhan:
        raise ValueError("Chưa có nội dung việc.")
    if len(loi_nhan) > 60000:
        raise ValueError("Nội dung quá dài để gửi sang máy khác.")
    if not NM.dang_bat():
        raise ValueError("Máy này chưa nối Nhiều máy.")
    if may_id == NM.cau_hinh().get("may_id"):
        raise ValueError("Đây là máy này, gửi như bình thường.")
    may = _may_trong_so(may_id)
    if not may:
        raise ValueError("Không thấy máy này trong sổ máy. Mở trang Nhiều máy kiểm tra lại.")
    if not may.get("dang_bat"):
        raise ValueError("Máy %s đang tắt. Bật máy đó lên hoặc chọn máy khác." % (may.get("ten") or ""))
    vid = secrets.token_hex(8)
    phien = re.sub(r"[^A-Za-z0-9_-]", "", phien or "")[:40] or ("moi-" + vid)
    agent = re.sub(r"[^A-Za-z0-9_.-]", "", agent or "")[:80]
    body = {"id": vid, "loi_nhan": loi_nhan, "agent": agent, "brain": _brain_tuong_doi(brain), "phien": "may-" + phien,
            "tu_may": NM.ten_may()}
    _goi_may(may, "POST", "/tisa-nhieu-may/nhan/viec", body, cho=40)
    r = {"id": vid, "may_id": may_id, "ten_may": may.get("ten") or may_id, "agent": agent, "ten_cong_su": (ten_cong_su or "")[:80],
         "loi_nhan": loi_nhan[:4000], "phien": phien, "luc": time.time(), "trang_thai": "dang_lam", "tien_do": "Đã gửi, máy kia đang nhận việc"}
    with _khoa():
        ds = _doc_giao()
        ds.append(r)
        _luu_giao(ds)
    NM.nhat_ky("giao_viec", may=may.get("ten"), agent=agent, id=vid)
    return r


def xem_giao(vid: str) -> dict:
    with _khoa():
        ds = _doc_giao()
        r = next((x for x in ds if x.get("id") == vid), None)
    if not r:
        raise KeyError(vid)
    if r.get("trang_thai") != "dang_lam":
        return r
    may = _may_trong_so(r["may_id"])
    if not may:
        r["tien_do"] = "Không thấy máy %s trong sổ máy" % r.get("ten_may")
        return r
    try:
        d = _goi_may(may, "GET", "/tisa-nhieu-may/nhan/viec/" + vid, cho=20)
    except ValueError as e:
        if "không có việc đó" in str(e):          # máy kia khởi động lại giữa chừng: việc đã mất, báo thẳng để anh gửi lại
            doi = {"trang_thai": "loi", "loi": "Máy %s khởi động lại giữa chừng nên việc bị dừng. Gửi lại việc này." % r.get("ten_may"),
                   "xong_luc": time.time()}
            with _khoa():
                ds = _doc_giao()
                for x in ds:
                    if x.get("id") == vid:
                        x.update(doi)
                        r = x
                _luu_giao(ds)
            return r
        r["tien_do"] = "Chưa hỏi được máy %s (%s). Việc vẫn chạy trên máy đó nếu máy còn bật." % (r.get("ten_may"), str(e)[:120])
        return r
    doi = {"tien_do": d.get("tien_do") or r.get("tien_do")}
    if d.get("trang_thai") in ("xong", "loi"):
        doi.update({"trang_thai": d["trang_thai"], "tra_loi": d.get("tra_loi") or "", "tep": d.get("tep") or [], "loi": d.get("loi") or "",
                    "xong_luc": d.get("xong_luc") or time.time()})
    with _khoa():
        ds = _doc_giao()
        for x in ds:
            if x.get("id") == vid:
                x.update(doi)
                r = x
        _luu_giao(ds)
    return r


def danh_sach_giao(phien: str = "", so: int = 20) -> list:
    ds = _doc_giao()
    if phien:
        ds = [x for x in ds if x.get("phien") == phien]
    return ds[-so:]


# ================================================================ máy B: nhận việc, chạy, trả kết quả
def _ghi_nhan(v: dict) -> None:
    ds = [x for x in (NM._doc(NHAN, []) or []) if isinstance(x, dict) and x.get("id") != v.get("id")]
    ds.append({k: v.get(k) for k in ("id", "tu_may", "tu_may_id", "agent", "phien", "luc", "trang_thai", "tien_do", "tra_loi", "tep", "loi", "xong_luc")})
    NM._ghi(NHAN, ds[-GIU_TOI_DA:])


def _xem_nhan(vid: str):
    v = _nhan.get(vid)
    if v:
        return v
    return next((x for x in (NM._doc(NHAN, []) or []) if isinstance(x, dict) and x.get("id") == vid), None)


async def _chay(v: dict, brain: str, ag) -> None:
    import main as M        # lõi TISA BOT (uvicorn chạy main:app): dùng đúng đường của /chat

    async def tien_do(s):
        s = str(s or "").strip()
        if s:
            v["tien_do"] = s[:300]

    try:
        out, _key = await M._cli_turn(v["loi_nhan"], brain, v["phien"], "may:" + (v.get("tu_may") or "")[:40], progress=tien_do, agent=ag)
        p = M._cli_payload(out, _key)
        v.update({"trang_thai": "xong" if p.get("ok") else "loi", "tra_loi": p.get("text") or "", "tep": p.get("files") or [],
                  "loi": "" if p.get("ok") else (p.get("text") or "Lỗi không rõ")[:500], "tien_do": "Xong"})
    except Exception as e:  # noqa: BLE001 - lỗi phải về tới máy giao việc
        v.update({"trang_thai": "loi", "loi": "%s: %s" % (type(e).__name__, str(e)[:400]), "tien_do": "Lỗi"})
    v["xong_luc"] = time.time()
    v.pop("loi_nhan", None)
    _ghi_nhan(v)
    NM.nhat_ky("nhan_viec_xong", tu=v.get("tu_may"), id=v.get("id"), trang_thai=v.get("trang_thai"))


def nhan(d: dict, tu_may_id: str) -> dict:
    import main as M
    vid = str(d.get("id") or "")
    if not re.fullmatch(r"[0-9a-f]{16}", vid):
        raise ValueError("Mã việc sai dạng.")
    if _xem_nhan(vid):
        return {"ok": True, "id": vid, "da_co": True}
    phien = re.sub(r"[^A-Za-z0-9_-]", "", str(d.get("phien") or ""))[:48] or "may-" + vid
    for x in _nhan.values():
        if x.get("phien") == phien and x.get("agent") == (d.get("agent") or "") and x.get("trang_thai") == "dang_lam":
            raise ValueError("Máy này đang làm việc trước của cuộc trò chuyện này. Chờ xong rồi gửi tiếp.")
    rel = str(d.get("brain") or "")
    brain = ""
    if rel and ".." not in rel.split("/"):
        p = NM.BRAINS_DIR / rel
        if p.is_dir():
            brain = str(p)
    agent = str(d.get("agent") or "")
    ag, loi = M._cli_agent(brain, phien, agent)
    if loi:
        raise ValueError("Máy này không có cộng sự đó (%s). Chờ đồng bộ bộ não vài phút rồi thử lại." % agent)
    v = {"id": vid, "tu_may": str(d.get("tu_may") or "")[:60], "tu_may_id": tu_may_id, "agent": agent, "phien": phien,
         "loi_nhan": str(d.get("loi_nhan") or ""), "luc": time.time(), "trang_thai": "dang_lam", "tien_do": "Đang bắt đầu"}
    _nhan[vid] = v
    for k in [k for k, x in _nhan.items() if x.get("trang_thai") != "dang_lam" and time.time() - (x.get("xong_luc") or 0) > 3600]:
        _nhan.pop(k, None)
    asyncio.get_running_loop().create_task(_chay(v, brain, ag))
    NM.nhat_ky("nhan_viec", tu=v["tu_may"], tu_may_id=tu_may_id, agent=agent, id=vid)
    return {"ok": True, "id": vid}


def tinh_trang_nhan(vid: str) -> dict:
    v = _xem_nhan(vid)
    if not v:
        raise KeyError(vid)
    return {"ok": True, **{k: v.get(k) for k in ("id", "trang_thai", "tien_do", "tra_loi", "tep", "loi", "xong_luc")}}


# ================================================================ gắn vào máy chủ web
def gan(app) -> None:
    from fastapi.responses import JSONResponse

    def _loi(e, ma=400):
        return JSONResponse({"ok": False, "loi": str(e)}, status_code=ma)

    async def _xac_thuc(req) -> tuple:
        than = await req.body()
        duong = req.scope.get("path") or ""
        try:
            return kiem_ky(req.method, duong, than, req.headers.get("x-tisa-may", "")), than
        except ValueError as e:
            if time.time() - _dung_roi.get("_luc_ghi_tu_choi", 0) > 30:     # bị gọi bậy liên tục: ghi tối đa 1 dòng / 30 giây
                _dung_roi["_luc_ghi_tu_choi"] = time.time()
                NM.nhat_ky("tu_choi_viec_may_khac", ly_do=str(e)[:200], duong=duong[:80])
            return None, than

    @app.get("/tisa-nhieu-may/api/may-lam")
    async def _may_lam():
        return may_lam()

    @app.post("/tisa-nhieu-may/api/giao")
    async def _giao(req: Request):
        try:
            b = await req.json()
        except Exception:  # noqa: BLE001
            b = {}
        try:
            r = await asyncio.to_thread(giao, str(b.get("may_id") or ""), str(b.get("loi_nhan") or ""), str(b.get("agent") or ""),
                                        str(b.get("brain") or ""), str(b.get("phien") or ""), str(b.get("ten_cong_su") or ""))
            return {"ok": True, "viec": r}
        except ValueError as e:
            return _loi(e)

    @app.get("/tisa-nhieu-may/api/giao")
    async def _ds_giao(phien: str = ""):
        return {"ok": True, "viec": danh_sach_giao(phien)}

    @app.get("/tisa-nhieu-may/api/giao/{vid}")
    async def _xem_giao(vid: str):
        try:
            return {"ok": True, "viec": await asyncio.to_thread(xem_giao, vid)}
        except KeyError:
            return _loi("Không có việc này.", 404)

    @app.post("/tisa-nhieu-may/nhan/viec")
    async def _nhan_viec(req: Request):
        tu, than = await _xac_thuc(req)
        if not tu:
            return _loi("Không xác thực được máy gửi.", 401)
        try:
            return nhan(json.loads(than.decode() or "{}"), tu)
        except ValueError as e:
            return _loi(e, 409)

    @app.get("/tisa-nhieu-may/nhan/viec/{vid}")
    async def _nhan_xem(vid: str, req: Request):
        tu, _ = await _xac_thuc(req)
        if not tu:
            return _loi("Không xác thực được máy gửi.", 401)
        try:
            return tinh_trang_nhan(vid)
        except KeyError:
            return _loi("Máy này không có việc đó (có thể máy vừa khởi động lại).", 404)
