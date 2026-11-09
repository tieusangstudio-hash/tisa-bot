"""tisa_nhan_vien.py - tài khoản nhân viên: hỏi đáp với bộ não, không đụng được gì khác của chủ.

Chủ tạo tài khoản và chọn quyền (Hệ thống > Tài khoản nhân viên). Nhân viên đăng nhập ở /nv/ và chỉ thấy:
  - Hỏi nhanh (nếu được bật),
  - các chuyên gia (cộng sự) chủ tích chọn,
  - nhật ký các Chatbot chủ tích chọn (chỉ xem).

An toàn:
  - Phiên nhân viên là cookie riêng (`tisa_nv`), KHÔNG phải phiên TISA BOT: mọi đường khác của TISA BOT vẫn đòi phiên
    chủ nên nhân viên không gọi được. Chỉ /nv/ được mở cho cookie này (đăng ký là đường công khai, tự kiểm phiên).
  - Câu trả lời chạy qua đúng bộ trả lời của Chatbot ở mức "Đọc tài liệu": tra được bộ não, không ghi, không chạy
    lệnh máy, không gửi gì ra ngoài. Không ghi vào kho hội thoại của chủ nên Tự học không học từ câu của nhân viên.
  - Mỗi người một hạn mức câu hỏi mỗi ngày (giờ Việt Nam), hết thì dừng: câu hỏi tiêu vào gói AI của chủ.
  - Mật khẩu băm PBKDF2, phiên lưu dạng băm. Sai mật khẩu nhiều lần thì khoá IP 15 phút.
Mọi câu hỏi và câu trả lời ghi lại để chủ xem (trang quản lý); màn đăng nhập của nhân viên báo trước điều này.
"""
import hashlib
import hmac
import json
import os
import re
import secrets
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

import config as cfgmod

KHO = Path(cfgmod.STATE_DIR) / "tisa_nhan_vien"
TEP_DS = KHO / "tai-khoan.json"
TEP_PHIEN = KHO / "phien.json"
TEP_DEM = KHO / "dem.json"
COOKIE = "tisa_nv"
PHIEN_NGAY = 30
VN = timezone(timedelta(hours=7))
HOI_TOI_DA = 4000          # ký tự một câu hỏi
GIOI_HAN_MAC_DINH = 30
SAI_TOI_DA, SAI_KHOA_GIAY = 8, 900
HOI_NHANH = "tisa-core"    # cộng sự hệ thống trả lời "Hỏi nhanh"; không có thì để lõi tự chọn
_khoa = threading.Lock()
_dang_hoi = set()          # nhân viên đang chờ trả lời: mỗi người một câu một lúc
_sai = {}                  # ip -> [mốc sai]
_da_nap = set()            # cuộc hỏi đã có phiên trong bộ nhớ tiến trình này
ROOT = Path(__file__).resolve().parent.parent
TRANG_NV = ROOT / "dashboard" / "tisa-nhan-vien.html"
TRANG_QL = ROOT / "dashboard" / "tisa-nhan-vien-ql.html"


# ---------------------------------------------------------------- lưu trữ

def _brain_dir():
    return Path(os.getenv("BRAINS_DIR") or (ROOT / "brains")) / "Brain Default"


def _doc(p, mac_dinh):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return mac_dinh


def _ghi(p, data):
    KHO.mkdir(parents=True, exist_ok=True)
    tam = p.with_suffix(".tmp")
    tam.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tam, p)
    try:
        os.chmod(p, 0o600)
    except OSError:
        pass


def _bam(mk, salt):
    return hashlib.pbkdf2_hmac("sha256", mk.encode("utf-8"), bytes.fromhex(salt), 200_000).hex()


def _hom_nay():
    return datetime.now(VN).strftime("%Y-%m-%d")


def _ds():
    return _doc(TEP_DS, {"ds": []}).get("ds") or []


def _tim(nv_id):
    return next((x for x in _ds() if x.get("id") == nv_id), None)


def _da_dung(nv_id):
    d = _doc(TEP_DEM, {})
    x = d.get(nv_id) or {}
    return int(x.get("so") or 0) if x.get("ngay") == _hom_nay() else 0


def _cong_dem(nv_id, buoc):
    with _khoa:
        d = _doc(TEP_DEM, {})
        x = d.get(nv_id) or {}
        so = int(x.get("so") or 0) if x.get("ngay") == _hom_nay() else 0
        d[nv_id] = {"ngay": _hom_nay(), "so": max(0, so + buoc)}
        _ghi(TEP_DEM, d)


def _tep_lich_su(nv_id):
    return KHO / ("lich-su-%s.jsonl" % re.sub(r"[^\w-]", "", nv_id))


def _ghi_lich_su(nv_id, dong):
    KHO.mkdir(parents=True, exist_ok=True)
    with _khoa, open(_tep_lich_su(nv_id), "a", encoding="utf-8") as f:
        f.write(json.dumps(dong, ensure_ascii=False) + "\n")


def _doc_lich_su(nv_id, cuoc="", gioi_han=200):
    p = _tep_lich_su(nv_id)
    if not p.exists():
        return []
    out = []
    for dong in p.read_text(encoding="utf-8").splitlines():
        try:
            x = json.loads(dong)
        except ValueError:
            continue
        if not cuoc or x.get("cuoc") == cuoc:
            out.append(x)
    return out[-gioi_han:]


def _tep_cuoc(nv_id):
    return KHO / ("cuoc-%s.json" % re.sub(r"[^\w-]", "", nv_id))


def _ds_cuoc(nv_id):
    return _doc(_tep_cuoc(nv_id), {})


def _cham_cuoc(nv_id, cuoc, slug, hoi):
    """Ghi nhận một cuộc hỏi: tạo mới thì lấy câu hỏi đầu làm tên (nhân viên đổi được)."""
    with _khoa:
        d = _ds_cuoc(nv_id)
        x = d.get(cuoc)
        now = time.time()
        if not x:
            ten = re.sub(r"\s+", " ", hoi).strip()
            x = d[cuoc] = {"ten": (ten[:48] + "…") if len(ten) > 48 else ten, "chuyen_gia": slug, "tao": now}
        x["sua"] = now
        x["so"] = int(x.get("so") or 0) + 1
        _ghi(_tep_cuoc(nv_id), d)


# ---------------------------------------------------------------- danh mục để chọn quyền

def chuyen_gia_co():
    """Cộng sự trong bộ não chính: [{slug, ten, vai}]. Đọc thẳng hồ sơ agents/*.md."""
    out = []
    d = _brain_dir() / "agents"
    for f in sorted(d.glob("*.md")) if d.is_dir() else []:
        try:
            dau = f.read_text(encoding="utf-8")[:1500]
        except OSError:
            continue
        ten = re.search(r'^name:\s*"?([^"\n]+)"?', dau, re.M)
        vai = re.search(r'^role:\s*"?([^"\n]+)"?', dau, re.M)
        out.append({"slug": f.stem, "ten": (ten.group(1).strip() if ten else f.stem),
                    "vai": (vai.group(1).strip()[:90] if vai else "")})
    return out


def chatbot_co():
    try:
        import chatbot_store
        return [{"id": b.get("id"), "ten": b.get("name") or b.get("id")} for b in chatbot_store.list_bots()]
    except Exception:  # noqa: BLE001
        return []


def _cong_khai(nv):
    return {k: nv.get(k) for k in ("id", "ten", "user", "khoa", "hoi_nhanh", "chuyen_gia", "chatbot", "gioi_han", "tao_luc", "mo_hinh")} | \
        {"da_dung": _da_dung(nv.get("id"))}


# ---------------------------------------------------------------- phiên nhân viên

def _ip(request):
    return request.headers.get("cf-connecting-ip") or (request.client.host if request.client else "?")


def _bi_khoa(ip):
    now = time.time()
    ds = [t for t in _sai.get(ip, []) if now - t < SAI_KHOA_GIAY]
    _sai[ip] = ds
    return len(ds) >= SAI_TOI_DA


def _tao_phien(nv_id):
    tok = secrets.token_urlsafe(32)
    with _khoa:
        d = _doc(TEP_PHIEN, {})
        now = time.time()
        d = {k: v for k, v in d.items() if v.get("het", 0) > now}
        d[hashlib.sha256(tok.encode()).hexdigest()] = {"nv": nv_id, "het": now + PHIEN_NGAY * 86400}
        _ghi(TEP_PHIEN, d)
    return tok


def _nv_cua(request):
    """Nhân viên của phiên này, hoặc None. Tài khoản bị khoá hay đã xoá thì phiên hết hiệu lực ngay."""
    tok = request.cookies.get(COOKIE, "")
    if not tok:
        return None
    x = _doc(TEP_PHIEN, {}).get(hashlib.sha256(tok.encode()).hexdigest())
    if not x or x.get("het", 0) < time.time():
        return None
    nv = _tim(x.get("nv"))
    if not nv or nv.get("khoa"):
        return None
    return nv


def _bo_phien_cua(nv_id):
    with _khoa:
        d = _doc(TEP_PHIEN, {})
        _ghi(TEP_PHIEN, {k: v for k, v in d.items() if v.get("nv") != nv_id})


# ---------------------------------------------------------------- trả lời

async def _tra_loi(nv, slug, cuoc, text):
    """Một lượt hỏi đáp qua bộ trả lời của Chatbot, mức Đọc tài liệu, không ghi kho hội thoại của chủ."""
    import chatbot_doc_tools
    import chatbot_runtime as cr
    ten_cg = next((c["ten"] for c in chuyen_gia_co() if c["slug"] == slug), "") if slug else ""
    agent_slug = slug or (HOI_NHANH if (_brain_dir() / "agents" / (HOI_NHANH + ".md")).exists() else "")
    bot_id = "nv_%s_%s" % (nv["id"], slug or "nhanh")
    cfg = {
        "id": bot_id, "slug": bot_id, "name": "Trợ lý nhân viên",
        "agent": {"brain": "brain", "slug": agent_slug} if agent_slug else None,
        "brain": "brain", "channel": "web", "accounts": [], "groups": [], "people": [],
        "reply_when": "always", "audience": "all", "nguon_tra_loi": "agent",
        "muc_quyen": chatbot_doc_tools.MODE, "enabled": True,
    }
    meta = {"chat_id": "nv:%s:%s" % (nv["id"], cuoc), "chat_type": "private", "chat_title": "",
            "user_id": nv["id"], "user_name": nv.get("ten") or nv.get("user"), "username": nv.get("user"),
            "message_id": "", "account_id": "", "platform": "web", "_kenh": "web", "mentioned": True, "ts": time.time()}
    try:
        tl = await cr._tra_tai_lieu(bot_id, cfg, text)
    except Exception:  # noqa: BLE001 - không tra được tài liệu thì vẫn trả lời bằng hiểu biết của cộng sự
        tl = {}
    cfg["_tai_lieu"], cfg["_kenh_luot"], cfg["_tu_dong"] = tl, "web", False
    mh = str(nv.get("mo_hinh") or "")
    if mh:
        # "nhà|mô hình" do chủ chọn: nhân viên không đổi được, tránh tốn token vì mô hình đắt.
        nha, _, ten_mh = mh.rpartition("|")
        cfg["_ep_mo_hinh"] = {"provider": nha, "model": ten_mh}
    loi_dan = ("Bạn đang trả lời %s, một nhân viên của doanh nghiệp, qua tài khoản nhân viên%s. "
               "Chỉ trả lời và tư vấn; không hứa thay chủ, không tiết lộ mật khẩu, khoá, số liệu tài chính riêng nếu không có "
               "trong tài liệu được phép.\n\n" % (nv.get("ten") or nv.get("user"), (" (chuyên gia: %s)" % ten_cg) if ten_cg else ""))
    # Phiên hội thoại nằm trong bộ nhớ máy chủ: sau khi khởi động lại, lượt đầu của một cuộc cũ kèm vài lượt
    # gần nhất để AI nối tiếp đúng mạch.
    khoa_cuoc = nv["id"] + ":" + cuoc
    if khoa_cuoc not in _da_nap:
        _da_nap.add(khoa_cuoc)
        cu = [x for x in _doc_lich_su(nv["id"], cuoc, 6) if x.get("dap")]
        if cu:
            loi_dan += "Các lượt trước của cuộc hỏi này:\n" + "\n".join(
                "- Hỏi: %s\n  Đáp: %s" % (x["hoi"][:600], x["dap"][:1200]) for x in cu) + "\n\nCâu hỏi mới:\n"
    res = await cr._deps["answer"](loi_dan + text, meta, None, channel="web", bot=cfg, phien_kho="", ghi_kho=False)
    if isinstance(res, str):
        raise RuntimeError(res.strip()[:300] or "Không soạn được câu trả lời")
    return str((res or {}).get("text") or "").strip(), list(tl.get("nguon") or [])[:6] if isinstance(tl, dict) else []


# ---------------------------------------------------------------- gắn vào app

def gan(app):

    @app.middleware("http")
    async def _tisa_nv_mw(request: Request, call_next):
        if request.url.path == "/nv":
            return RedirectResponse("/nv/", status_code=302)
        return await call_next(request)

    # ---------- trang và API của nhân viên (/nv/ là đường công khai, tự kiểm phiên) ----------
    @app.get("/nv/")
    async def _nv_trang():
        try:
            return HTMLResponse(TRANG_NV.read_text(encoding="utf-8"), headers={"cache-control": "no-cache"})
        except OSError:
            return HTMLResponse("Thiếu trang nhân viên", status_code=500)

    @app.post("/nv/api/dang-nhap")
    async def _nv_dang_nhap(request: Request):
        ip = _ip(request)
        if _bi_khoa(ip):
            return JSONResponse({"ok": False, "error": "Sai quá nhiều lần, thử lại sau 15 phút."}, status_code=429)
        try:
            d = await request.json()
        except ValueError:
            d = {}
        user = str(d.get("user") or "").strip().lower()
        mk = str(d.get("mat_khau") or "")
        nv = next((x for x in _ds() if x.get("user") == user), None)
        if not nv or not hmac.compare_digest(_bam(mk, nv.get("salt") or "00"), nv.get("hash") or ""):
            _sai.setdefault(ip, []).append(time.time())
            return JSONResponse({"ok": False, "error": "Sai tên đăng nhập hoặc mật khẩu."}, status_code=401)
        if nv.get("khoa"):
            return JSONResponse({"ok": False, "error": "Tài khoản đang bị khoá. Hỏi quản lý của bạn."}, status_code=403)
        tok = _tao_phien(nv["id"])
        r = JSONResponse({"ok": True})
        r.set_cookie(COOKIE, tok, max_age=PHIEN_NGAY * 86400, httponly=True, samesite="lax", path="/nv",
                     secure=request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https")
        return r

    @app.post("/nv/api/dang-xuat")
    async def _nv_dang_xuat(request: Request):
        tok = request.cookies.get(COOKIE, "")
        if tok:
            with _khoa:
                d = _doc(TEP_PHIEN, {})
                d.pop(hashlib.sha256(tok.encode()).hexdigest(), None)
                _ghi(TEP_PHIEN, d)
        r = JSONResponse({"ok": True})
        r.delete_cookie(COOKIE, path="/nv")
        return r

    def _can_nv(request):
        nv = _nv_cua(request)
        return nv, (None if nv else JSONResponse({"ok": False, "error": "Hết phiên, đăng nhập lại.", "dang_nhap": True}, status_code=401))

    @app.get("/nv/api/toi")
    async def _nv_toi(request: Request):
        nv, loi = _can_nv(request)
        if loi:
            return loi
        cg = {c["slug"]: c for c in chuyen_gia_co()}
        cb = {c["id"]: c for c in chatbot_co()}
        gioi = int(nv.get("gioi_han") or 0)
        return {"ok": True, "ten": nv.get("ten"), "user": nv.get("user"), "hoi_nhanh": bool(nv.get("hoi_nhanh")),
                "chuyen_gia": [cg[s] for s in (nv.get("chuyen_gia") or []) if s in cg],
                "chatbot": [cb[i] for i in (nv.get("chatbot") or []) if i in cb],
                "gioi_han": gioi, "da_dung": _da_dung(nv["id"]), "ten_app": _ten_app(),
                "mo_hinh": str(nv.get("mo_hinh") or "").rpartition("|")[2]}

    @app.post("/nv/api/hoi")
    async def _nv_hoi(request: Request):
        nv, loi = _can_nv(request)
        if loi:
            return loi
        try:
            d = await request.json()
        except ValueError:
            d = {}
        text = str(d.get("text") or "").strip()[:HOI_TOI_DA]
        slug = str(d.get("chuyen_gia") or "").strip()
        cuoc = re.sub(r"[^\w-]", "", str(d.get("cuoc") or ""))[:40] or secrets.token_hex(6)
        if not text:
            return JSONResponse({"ok": False, "error": "Gõ câu hỏi trước đã."}, status_code=400)
        if slug and slug not in (nv.get("chuyen_gia") or []):
            return JSONResponse({"ok": False, "error": "Bạn chưa được cấp quyền hỏi chuyên gia này."}, status_code=403)
        if not slug and not nv.get("hoi_nhanh"):
            return JSONResponse({"ok": False, "error": "Bạn chưa được cấp quyền Hỏi nhanh."}, status_code=403)
        gioi = int(nv.get("gioi_han") or 0)
        if gioi and _da_dung(nv["id"]) >= gioi:
            return JSONResponse({"ok": False, "het_luot": True,
                                 "error": "Hôm nay bạn đã dùng hết %d câu hỏi. Mai quay lại nhé." % gioi}, status_code=429)
        if nv["id"] in _dang_hoi:
            return JSONResponse({"ok": False, "error": "Đang trả lời câu trước, chờ chút."}, status_code=409)
        _dang_hoi.add(nv["id"])
        _cong_dem(nv["id"], 1)
        t0 = time.time()
        try:
            dap, nguon = await _tra_loi(nv, slug, cuoc, text)
        except Exception as e:  # noqa: BLE001
            _cong_dem(nv["id"], -1)      # lượt hỏng không tính vào hạn mức
            _ghi_lich_su(nv["id"], {"ts": t0, "cuoc": cuoc, "chuyen_gia": slug, "hoi": text, "dap": "", "loi": str(e)[:300]})
            return JSONResponse({"ok": False, "error": "Chưa trả lời được: %s" % str(e)[:200]}, status_code=502)
        finally:
            _dang_hoi.discard(nv["id"])
        _ghi_lich_su(nv["id"], {"ts": t0, "cuoc": cuoc, "chuyen_gia": slug, "hoi": text, "dap": dap, "giay": round(time.time() - t0, 1)})
        _cham_cuoc(nv["id"], cuoc, slug, text)
        return {"ok": True, "dap": dap, "nguon": nguon, "cuoc": cuoc, "da_dung": _da_dung(nv["id"]), "gioi_han": gioi}

    @app.get("/nv/api/lich-su")
    async def _nv_lich_su(request: Request, cuoc: str = ""):
        nv, loi = _can_nv(request)
        if loi:
            return loi
        return {"ok": True, "luot": _doc_lich_su(nv["id"], cuoc, 300)}

    @app.get("/nv/api/cuoc")
    async def _nv_cuoc(request: Request, chuyen_gia: str = "", tat_ca: int = 0):
        nv, loi = _can_nv(request)
        if loi:
            return loi
        d = _ds_cuoc(nv["id"])
        # tat_ca=1: mọi cuộc của người này (danh sách bên trái trang nhân viên), chỉ những chuyên gia còn được cấp.
        duoc = set(nv.get("chuyen_gia") or []) | ({""} if nv.get("hoi_nhanh") else set())
        ds = [dict(v, id=k) for k, v in d.items() if not v.get("an") and (
            ((v.get("chuyen_gia") or "") in duoc) if tat_ca else ((v.get("chuyen_gia") or "") == chuyen_gia))]
        ds.sort(key=lambda x: -(x.get("sua") or 0))
        return {"ok": True, "cuoc": ds[:200]}

    @app.post("/nv/api/cuoc/doi-ten")
    async def _nv_cuoc_ten(request: Request):
        nv, loi = _can_nv(request)
        if loi:
            return loi
        try:
            d = await request.json()
        except ValueError:
            d = {}
        cuoc = str(d.get("cuoc") or "")
        ten = re.sub(r"[\x00-\x1f<>]", "", str(d.get("ten") or "")).strip()[:80]
        if not ten:
            return JSONResponse({"ok": False, "error": "Tên không được trống."}, status_code=400)
        with _khoa:
            ds = _ds_cuoc(nv["id"])
            if cuoc not in ds:
                return JSONResponse({"ok": False, "error": "Không có cuộc hỏi này."}, status_code=404)
            ds[cuoc]["ten"] = ten
            _ghi(_tep_cuoc(nv["id"]), ds)
        return {"ok": True}

    @app.post("/nv/api/cuoc/xoa")
    async def _nv_cuoc_xoa(request: Request):
        """Nhân viên ẩn một cuộc khỏi danh sách của họ. Lịch sử vẫn giữ để chủ xem."""
        nv, loi = _can_nv(request)
        if loi:
            return loi
        try:
            d = await request.json()
        except ValueError:
            d = {}
        cuoc = str(d.get("cuoc") or "")
        with _khoa:
            ds = _ds_cuoc(nv["id"])
            if cuoc in ds:
                ds[cuoc]["an"] = True
                _ghi(_tep_cuoc(nv["id"]), ds)
        return {"ok": True}

    @app.get("/nv/api/chatbot/{bot_id}")
    async def _nv_chatbot(request: Request, bot_id: str):
        nv, loi = _can_nv(request)
        if loi:
            return loi
        if bot_id not in (nv.get("chatbot") or []):
            return JSONResponse({"ok": False, "error": "Bạn chưa được cấp quyền xem Chatbot này."}, status_code=403)
        import chatbot_log
        return {"ok": True, "luot": chatbot_log.doc(bot_id, 80)}

    # ---------- quản lý của chủ (đòi phiên TISA BOT như mọi đường khác) ----------
    @app.get("/tisa-nv/")
    async def _ql_trang():
        try:
            return HTMLResponse(TRANG_QL.read_text(encoding="utf-8"), headers={"cache-control": "no-cache"})
        except OSError:
            return HTMLResponse("Thiếu trang quản lý", status_code=500)

    @app.get("/tisa-nv/api/ds")
    async def _ql_ds():
        try:
            chinh = (cfgmod.read_settings().get("model") or {}).get("main") or {}
        except Exception:  # noqa: BLE001
            chinh = {}
        return {"ok": True, "ds": [_cong_khai(x) for x in _ds()], "chuyen_gia": chuyen_gia_co(), "chatbot": chatbot_co(),
                "nha_chinh": chinh.get("provider") or "", "mo_hinh_chinh": chinh.get("model") or "",
                "gioi_han_mac_dinh": GIOI_HAN_MAC_DINH}

    @app.post("/tisa-nv/api/luu")
    async def _ql_luu(request: Request):
        try:
            d = await request.json()
        except ValueError:
            d = {}
        ten = re.sub(r"[\x00-\x1f<>]", "", str(d.get("ten") or "")).strip()[:60]
        user = str(d.get("user") or "").strip().lower()
        mk = str(d.get("mat_khau") or "")
        if not re.match(r"^[a-z0-9._-]{3,32}$", user):
            return JSONResponse({"ok": False, "error": "Tên đăng nhập 3-32 ký tự: chữ thường không dấu, số, dấu chấm, gạch."}, status_code=400)
        with _khoa:
            ds = _ds()
            nv = next((x for x in ds if x.get("id") == d.get("id")), None) if d.get("id") else None
            if any(x.get("user") == user and x is not nv for x in ds):
                return JSONResponse({"ok": False, "error": "Tên đăng nhập này đã có người dùng."}, status_code=400)
            if nv is None:
                if len(mk) < 8:
                    return JSONResponse({"ok": False, "error": "Mật khẩu ít nhất 8 ký tự."}, status_code=400)
                nv = {"id": "nv_" + secrets.token_hex(5), "tao_luc": time.time()}
                ds.append(nv)
            elif mk and len(mk) < 8:
                return JSONResponse({"ok": False, "error": "Mật khẩu mới ít nhất 8 ký tự."}, status_code=400)
            if mk:
                nv["salt"] = secrets.token_hex(16)
                nv["hash"] = _bam(mk, nv["salt"])
            cg = {c["slug"] for c in chuyen_gia_co()}
            cb = {c["id"] for c in chatbot_co()}
            try:
                gioi = max(0, min(10000, int(d.get("gioi_han") if d.get("gioi_han") is not None else GIOI_HAN_MAC_DINH)))
            except (TypeError, ValueError):
                gioi = GIOI_HAN_MAC_DINH
            mh = str(d.get("mo_hinh") or "").strip()
            if mh and not re.match(r"^[\w.-]*\|[\w.:/-]{1,80}$", mh):
                return JSONResponse({"ok": False, "error": "Mô hình không hợp lệ."}, status_code=400)
            nv["mo_hinh"] = mh
            nv.update(ten=ten or user, user=user, khoa=bool(d.get("khoa")), hoi_nhanh=bool(d.get("hoi_nhanh")),
                      chuyen_gia=[s for s in (d.get("chuyen_gia") or []) if s in cg],
                      chatbot=[i for i in (d.get("chatbot") or []) if i in cb], gioi_han=gioi)
            _ghi(TEP_DS, {"ds": ds})
        if nv.get("khoa") or mk:
            _bo_phien_cua(nv["id"])      # khoá hoặc đổi mật khẩu: đăng xuất mọi máy của người đó
        return {"ok": True, "nv": _cong_khai(nv)}

    @app.post("/tisa-nv/api/xoa")
    async def _ql_xoa(request: Request):
        try:
            d = await request.json()
        except ValueError:
            d = {}
        with _khoa:
            ds = [x for x in _ds() if x.get("id") != d.get("id")]
            _ghi(TEP_DS, {"ds": ds})
        _bo_phien_cua(str(d.get("id") or ""))
        return {"ok": True}

    @app.get("/tisa-nv/api/lich-su")
    async def _ql_lich_su(id: str, gioi_han: int = 300):
        return {"ok": True, "luot": _doc_lich_su(id, "", max(1, min(2000, gioi_han)))}


def _ten_app():
    try:
        import tisa_giao_dien
        return tisa_giao_dien.doc().get("ten") or "TISA BOT"
    except Exception:  # noqa: BLE001
        return "TISA BOT"
