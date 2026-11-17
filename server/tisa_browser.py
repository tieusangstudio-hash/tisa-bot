"""tisa_browser.py - Trình duyệt TISA (V2.98): một cửa sổ Chrome (hoặc Edge) riêng của TISA BOT mà AI Agent điều khiển như người thật.

Người dùng mở cửa sổ này, TỰ đăng nhập các trang cần dùng (mật khẩu, mã xác thực do người dùng gõ, TISA BOT không nhận), rồi giao việc cho agent:
agent nhìn trang, tự tìm nút, di chuột, bấm, gõ, cuộn, chờ, kiểm tra kết quả. Dùng cho việc không có MCP hay API (tạo Fanpage, đăng bài, lấy mã...).

Cách làm: Chrome chạy với hồ sơ riêng (thư mục dữ liệu bền, không chung Chrome cá nhân) và cổng điều khiển chỉ nghe 127.0.0.1. TISA BOT nói chuyện
với nó bằng giao thức DevTools (websockets, không cần cài thêm gì, không tải trình duyệt). Agent gọi hai công cụ của hub:
  - tisa_browser_look (chỉ xem): open, look, screenshot, tabs, status
  - tisa_browser_do   (thao tác): click, type, press, scroll, select, upload, wait, wait_user, back, forward, reload, new_tab, switch_tab, close_tab

Rào chắn (nằm TRONG công cụ, agent không tự gỡ được):
  - Ô mật khẩu, mã xác thực, số thẻ, CAPTCHA: agent KHÔNG gõ, chỉ chờ người dùng làm (op wait_user).
  - Thanh toán, nạp tiền, mua: agent không bấm; người dùng tự bấm bước cuối. Trang ngân hàng, ví, sàn coin: mọi thao tác bị chặn.
  - Đăng công khai, gửi, xóa, đổi bảo mật, đăng ký tài khoản: tool trả "CAN_DUYET", người dùng bấm Duyệt trong TISA BOT (đường /trinh-duyet/duyet,
    sau đăng nhập), agent gọi lại với duyet_id. Mã duyệt dùng một lần, 10 phút, khớp đúng việc.
  - Nút Dừng ngay: mọi thao tác ngừng cho tới khi người dùng cho tiếp tục. Nhật ký từng bước.
  - Cổng điều khiển không bật --remote-allow-origins nên trang web trong trình duyệt không nối được vào cổng này.
"""
from __future__ import annotations

import asyncio
import base64
import contextvars
import json
import os
import random
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

try:   # đứng ở đầu tệp: FastAPI đọc chú thích kiểu theo tên toàn cục
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

try:
    import config as _cfg
    STATE_DIR = Path(_cfg.STATE_DIR)
except Exception:  # noqa: BLE001
    STATE_DIR = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)

DIR = STATE_DIR / "trinh-duyet"
HOSO = DIR / "ho-so"
ANH = DIR / "anh"
TEP_NK = DIR / "nhat-ky.jsonl"
CONG = int(os.getenv("TISA_BROWSER_PORT") or 9335)
HEADLESS = os.getenv("TISA_BROWSER_HEADLESS") == "1"
HIEU_LUC_DUYET = 10 * 60
TOI_DA_MOT_PHUT = 45

_khoa = threading.RLock()
_tt = {"dung": False, "cho_nguoi": None, "tab": "", "hoso": "chinh", "muc": "quan_trong", "muc_den": 0.0}
_HS = contextvars.ContextVar("tisa_hoso", default="")      # trình duyệt đang được thao tác trong lượt gọi này
TEP_HS = DIR / "ho-so.json"
CONG_DAU, CONG_CUOI = CONG, CONG + 64
MUC = ("hoi_het", "quan_trong", "toan_quyen")
TEP_MUC = DIR / "muc.json"
_mien_toi: set = set()
_duyet: dict = {}
_nhip: list = []

# ---------------------------------------------------------------- phân loại hành động
_DANG_NHAP = re.compile(r"đăng nhập|dang nhap|log ?in|sign ?in|đăng nhập bằng", re.I)
_BI_MAT = re.compile(r"mật khẩu|mat khau|password|passcode|\botp\b|mã xác (thực|minh|nhận)|ma xac (thuc|minh|nhan)|verification code|security code|"
                     r"\bcvv\b|\bcvc\b|số thẻ|so the|card number|authenticator|mã 2fa|two[- ]factor", re.I)
_TIEN = re.compile(r"thanh toán|thanh toan|\bpay\b|pay now|place order|mua ngay|đặt hàng|dat hang|buy now|checkout|nạp tiền|nap tien|top ?up|"
                   r"nâng cấp gói|nang cap goi|upgrade plan|confirm payment|xác nhận thanh toán|purchase|subscribe|đăng ký gói|add payment|thêm thẻ|them the", re.I)
_XOA = re.compile(r"\bxóa\b|\bxoá\b|\bxoa\b|\bdelete\b|\bremove\b|hủy gói|huy goi|cancel subscription|deactivate|vô hiệu hóa|gỡ bỏ|close account|đóng tài khoản|dong tai khoan|"
                  r"unpublish|permanently", re.I)
_BAO_MAT = re.compile(r"đổi mật khẩu|doi mat khau|change password|đổi email|add admin|thêm quản trị|them quan tri|cấp quyền|cap quyen|grant access|authorize|"
                      r"cho phép truy cập|disconnect|revoke|thu hồi|tắt xác thực|two-step|transfer ownership|chuyển quyền", re.I)
_RA_NGOAI = re.compile(r"\bđăng\b|\bdang bai\b|publish|\bpost\b|\bgửi\b|\bgui\b|\bsend\b|submit|\bshare\b|chia sẻ|chia se|tweet|\breply\b|trả lời|bình luận|"
                       r"\bcomment\b|gửi yêu cầu|xác nhận|\bconfirm\b|tạo trang|create page|\binvite\b|\bmời\b|đăng ký|dang ky|sign ?up|register|"
                       r"create account|tạo tài khoản|tạo quảng cáo|create ad|boost|đẩy bài|schedule|lên lịch|\bapply\b|áp dụng", re.I)
_MIEN_CHAN = re.compile(r"(^|\.)(vietcombank|vcbdigibank|techcombank|bidv|vietinbank|agribank|mbbank|tpb|tpbank|vpbank|sacombank|hdbank|ocb|msb|eximbank|shb|"
                        r"vib|seabank|acb|lienvietpostbank|ncb|scb|abbank|bacabank|baovietbank|momo|zalopay|vnpay|shopeepay|viettelmoney|paypal|payoneer|wise|"
                        r"binance|coinbase|kraken|bybit|okx|kucoin|metamask|trustwallet|stripe)\.", re.I)
_MIEN_CHAN_PATH = re.compile(r"(ebank|internet-?banking|ibanking|\.bank\.|/checkout|/payment|/thanh-toan|/pay/)", re.I)
_CAPTCHA_JS = ("!!document.querySelector('iframe[src*=\"recaptcha\"],iframe[src*=\"hcaptcha\"],iframe[src*=\"turnstile\"],iframe[src*=\"captcha\"],"
               ".g-recaptcha,.h-captcha,.cf-turnstile,#captcha,[class*=\"captcha\" i]')")


def phan_loai(ngu_canh: dict) -> tuple[str, str]:
    """(loại, mô tả). Loại: vo_hai, bi_mat, tien, chan, can_duyet. Văn bản ngữ cảnh gồm tên nút, nhãn, nút gửi của biểu mẫu."""
    host = str(ngu_canh.get("host") or "")
    url = str(ngu_canh.get("url") or "")
    if _MIEN_CHAN.search(host) or _MIEN_CHAN_PATH.search(url):
        return "chan", "Trang ngân hàng, ví, cổng thanh toán hoặc sàn coin: agent không thao tác ở đây, anh tự làm."
    ten = " ".join(str(ngu_canh.get(k) or "") for k in ("ten", "nhan", "gui"))
    tag, kieu, ac = str(ngu_canh.get("tag") or ""), str(ngu_canh.get("kieu") or "").lower(), str(ngu_canh.get("ac") or "").lower()
    if tag in ("input", "textarea") and (kieu == "password" or ac in ("one-time-code", "cc-number", "cc-csc", "cc-exp", "current-password", "new-password")
                                         or _BI_MAT.search(ten)):
        return "bi_mat", "Ô mật khẩu, mã xác thực hoặc số thẻ: người dùng tự nhập."
    if ngu_canh.get("captcha"):
        return "bi_mat", "Trang có CAPTCHA: người dùng tự giải."
    if _DANG_NHAP.search(ten) and not _RA_NGOAI.search(re.sub(_DANG_NHAP, "", ten)):
        return "vo_hai", "Đăng nhập"
    if _TIEN.search(ten):
        return "tien", "Bước tiền bạc (thanh toán, mua, nạp, nâng gói): người dùng tự bấm."
    if _XOA.search(ten):
        return "can_duyet", "Xóa hoặc gỡ bỏ"
    if _BAO_MAT.search(ten):
        return "can_duyet", "Đổi bảo mật hoặc cấp quyền"
    if _RA_NGOAI.search(ten):
        return "can_duyet", "Việc ra ngoài (đăng, gửi, nộp, tạo, đăng ký)"
    return "vo_hai", ""


# ---------------------------------------------------------------- nhiều trình duyệt (mỗi trình duyệt một hồ sơ riêng, đăng nhập tài khoản riêng)
def _doc_hs() -> dict:
    try:
        d = json.loads(TEP_HS.read_text(encoding="utf-8"))
        if isinstance(d.get("ds"), list) and d["ds"]:
            return d
    except (OSError, ValueError):
        pass
    return {"ds": [{"id": "chinh", "ten": "Trình duyệt 1", "cong": CONG}], "dang_dung": "chinh"}


def _luu_hs(d: dict) -> None:
    try:
        DIR.mkdir(parents=True, exist_ok=True)
        TEP_HS.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


def ds_ho_so() -> list:
    return list(_doc_hs()["ds"])


def hs_dang_dung() -> str:
    d = _doc_hs()
    return d.get("dang_dung") if any(x["id"] == d.get("dang_dung") for x in d["ds"]) else d["ds"][0]["id"]


def _hs() -> str:
    h = _HS.get() or hs_dang_dung()
    return h if any(x["id"] == h for x in _doc_hs()["ds"]) else hs_dang_dung()


def tim_ho_so(ten_hoac_id: str):
    """Tìm trình duyệt theo mã, tên đầy đủ hoặc số thứ tự ('2', 'trình duyệt 2')."""
    t = str(ten_hoac_id or "").strip().lower()
    if not t:
        return None
    ds = ds_ho_so()
    for x in ds:
        if t in (x["id"].lower(), x["ten"].lower()):
            return x
    m = re.search(r"(\d+)\s*$", t)
    if m and 1 <= int(m.group(1)) <= len(ds):
        return ds[int(m.group(1)) - 1]
    for x in ds:
        if t in x["ten"].lower():
            return x
    return None


def _cong(hs: str = "") -> int:
    h = hs or _hs()
    return next((int(x["cong"]) for x in _doc_hs()["ds"] if x["id"] == h), CONG)


def _ten_hs(hs: str = "") -> str:
    h = hs or _hs()
    return next((x["ten"] for x in _doc_hs()["ds"] if x["id"] == h), "Trình duyệt")


def tao_ho_so(ten: str = "", extra: dict | None = None) -> dict:
    d = _doc_hs()
    if len(d["ds"]) >= 10:
        return {"ok": False, "loi": "Tối đa 10 trình duyệt."}
    dung = {int(x["cong"]) for x in d["ds"]}
    cong = next((c for c in range(CONG_DAU, CONG_CUOI) if c not in dung and not _cong_mo(c)), 0)
    if not cong:
        return {"ok": False, "loi": "Hết cổng trống."}
    n = len(d["ds"]) + 1
    ma = "tk%d" % int(time.time() * 1000 % 10 ** 8)
    ten = re.sub(r"\s+", " ", str(ten or "").strip())[:40] or "Trình duyệt %d" % n
    if any(x["ten"].lower() == ten.lower() for x in d["ds"]):
        ten = "%s (%d)" % (ten, n)
    muc = {"id": ma, "ten": ten, "cong": cong}
    if extra:
        muc.update(extra)
    d["ds"].append(muc)
    _luu_hs(d)
    _ghi_nk({"op": "ho_so", "ket_qua": "đã tạo", "mo_ta": "Tạo trình duyệt mới: %s" % ten})
    return {"ok": True, "id": ma, "ten": ten}


def doi_ten_ho_so(ma: str, ten: str) -> dict:
    d = _doc_hs()
    ten = re.sub(r"\s+", " ", str(ten or "").strip())[:40]
    x = next((x for x in d["ds"] if x["id"] == ma), None)
    if not x or not ten:
        return {"ok": False, "loi": "Không đổi được tên."}
    if any(y["ten"].lower() == ten.lower() and y["id"] != ma for y in d["ds"]):
        return {"ok": False, "loi": "Đã có trình duyệt tên này."}
    x["ten"] = ten
    _luu_hs(d)
    return {"ok": True}


def chon_ho_so(ma: str) -> dict:
    d = _doc_hs()
    if not any(x["id"] == ma for x in d["ds"]):
        return {"ok": False, "loi": "Không có trình duyệt này."}
    d["dang_dung"] = ma
    _luu_hs(d)
    with _khoa:
        _tt["hoso"], _tt["tab"] = ma, ""
    return {"ok": True}


async def xoa_ho_so(ma: str) -> dict:
    d = _doc_hs()
    if len(d["ds"]) <= 1:
        return {"ok": False, "loi": "Phải còn ít nhất một trình duyệt."}
    x = next((x for x in d["ds"] if x["id"] == ma), None)
    if not x:
        return {"ok": False, "loi": "Không có trình duyệt này."}
    tok = _HS.set(ma)
    try:
        await dong_trinh_duyet()
    finally:
        _HS.reset(tok)
    await asyncio.sleep(0.8)
    d["ds"] = [y for y in d["ds"] if y["id"] != ma]
    if d.get("dang_dung") == ma:
        d["dang_dung"] = d["ds"][0]["id"]
        with _khoa:
            _tt["hoso"] = d["dang_dung"]
    _luu_hs(d)
    shutil.rmtree(HOSO / ma, ignore_errors=True)       # xóa hồ sơ đăng nhập của trình duyệt này (chỉ dữ liệu của chính trình duyệt TISA)
    _ghi_nk({"op": "ho_so", "ket_qua": "đã xóa", "mo_ta": "Xóa trình duyệt %s và các đăng nhập của nó" % x["ten"]})
    return {"ok": True}


# ---------------------------------------------------------------- dùng hồ sơ Chrome (Edge, Brave) anh đã có: không phải đăng nhập lại
def _nguon_trinh_duyet() -> list:
    """Các trình duyệt Chrome có trên máy: (mã, tên, thư mục dữ liệu, tệp chạy)."""
    h = Path.home()
    if sys.platform == "darwin":
        a = h / "Library" / "Application Support"
        c = [("chrome", "Google Chrome", a / "Google" / "Chrome", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
             ("edge", "Microsoft Edge", a / "Microsoft Edge", "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
             ("brave", "Brave", a / "BraveSoftware" / "Brave-Browser", "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"),
             ("chromium", "Chromium", a / "Chromium", "/Applications/Chromium.app/Contents/MacOS/Chromium")]
    elif os.name == "nt":
        la = Path(os.environ.get("LOCALAPPDATA") or (h / "AppData" / "Local"))
        pf = [os.environ.get("PROGRAMFILES", ""), os.environ.get("PROGRAMFILES(X86)", ""), str(la)]
        def exe(*rel):
            return next((str(Path(x) / Path(*rel)) for x in pf if x and (Path(x) / Path(*rel)).exists()), "")
        c = [("chrome", "Google Chrome", la / "Google" / "Chrome" / "User Data", exe("Google", "Chrome", "Application", "chrome.exe")),
             ("edge", "Microsoft Edge", la / "Microsoft" / "Edge" / "User Data", exe("Microsoft", "Edge", "Application", "msedge.exe")),
             ("brave", "Brave", la / "BraveSoftware" / "Brave-Browser" / "User Data", exe("BraveSoftware", "Brave-Browser", "Application", "brave.exe"))]
    else:
        a = h / ".config"
        c = [("chrome", "Google Chrome", a / "google-chrome", shutil.which("google-chrome") or ""), ("chromium", "Chromium", a / "chromium", shutil.which("chromium") or ""),
             ("edge", "Microsoft Edge", a / "microsoft-edge", shutil.which("microsoft-edge") or ""), ("brave", "Brave", a / "BraveSoftware" / "Brave-Browser", shutil.which("brave-browser") or "")]
    return [x for x in c if x[2].is_dir() and (x[2] / "Local State").is_file() and x[3] and Path(x[3]).exists()]


def _dang_mo(goc: Path) -> bool:
    for ten in ("SingletonLock", "lockfile", "SingletonSocket"):
        if os.path.lexists(goc / ten):
            return True
    return False


def nguon_chrome() -> list:
    """Danh sách hồ sơ có sẵn để anh chọn (tên, email, thư mục). Không đọc mật khẩu hay cookie."""
    out = []
    for ma, ten, goc, exe in _nguon_trinh_duyet():
        try:
            ls = json.loads((goc / "Local State").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        hs = []
        for thu_muc, v in sorted((ls.get("profile", {}).get("info_cache") or {}).items()):
            if not (goc / thu_muc).is_dir():
                continue
            hs.append({"thu_muc": thu_muc, "ten": str(v.get("name") or v.get("gaia_name") or thu_muc)[:60], "email": str(v.get("user_name") or "")[:80],
                       "co_cookie": any((goc / thu_muc / r).is_file() for r in ("Network/Cookies", "Cookies"))})
        if hs:
            out.append({"ma": ma, "ten": ten, "dang_mo": _dang_mo(goc), "ho_so": hs})
    return out


_SAO_CHEP = ("Network/Cookies", "Network/Cookies-journal", "Cookies", "Cookies-journal", "Local Storage", "Session Storage")


def _sao_chep_dang_nhap(goc: Path, thu_muc: str, dich: Path) -> dict:
    """Chép phần ĐĂNG NHẬP của một hồ sơ (cookie, Local Storage, Session Storage) sang hồ sơ của trình duyệt TISA.
    Không chép mật khẩu đã lưu, thẻ, lịch sử, tiện ích. Hồ sơ gốc chỉ được đọc, không sửa."""
    nguon = goc / thu_muc
    d = dich / "Default"
    if dich.exists():
        shutil.rmtree(dich, ignore_errors=True)
    d.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy2(goc / "Local State", dich / "Local State")     # khóa giải mã cookie (Windows) nằm ở đây
    except OSError:
        pass
    so_tep = 0
    for rel in _SAO_CHEP:
        src = nguon / rel
        if not src.exists():
            continue
        dst = d / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True, ignore_dangling_symlinks=True)
            else:
                shutil.copy2(src, dst)
            so_tep += 1
        except OSError:
            continue
    so_cookie, mien = 0, []
    for rel in ("Network/Cookies", "Cookies"):
        f = d / rel
        if f.is_file():
            try:
                import sqlite3
                con = sqlite3.connect("file:%s?mode=ro" % f, uri=True, timeout=3)
                so_cookie = con.execute("SELECT COUNT(*) FROM cookies").fetchone()[0]
                mien = [r[0].lstrip(".") for r in con.execute("SELECT DISTINCT host_key FROM cookies WHERE name IN (%s)" % ",".join("?" * len(_DAU_PHIEN)), tuple(_DAU_PHIEN)).fetchall()]
                con.close()
            except Exception:  # noqa: BLE001
                pass
            break
    goc_mien = sorted({".".join(m.split(".")[-2:]) for m in mien})[:30]
    try:
        os.chmod(dich, 0o700)
    except OSError:
        pass
    return {"so_tep": so_tep, "so_cookie": so_cookie, "dang_nhap": goc_mien}


async def nhap_chrome(ma_nguon: str, thu_muc: str, ten: str = "") -> dict:
    nguon = next((x for x in _nguon_trinh_duyet() if x[0] == ma_nguon), None)
    if not nguon:
        return {"ok": False, "loi": "Không thấy trình duyệt này trên máy."}
    _, ten_nguon, goc, exe = nguon
    ds = nguon_chrome()
    hs = next((h for n in ds if n["ma"] == ma_nguon for h in n["ho_so"] if h["thu_muc"] == thu_muc), None)
    if not hs:
        return {"ok": False, "loi": "Không thấy hồ sơ này."}
    tao = tao_ho_so(ten or hs["ten"], {"exe": exe, "nhap_tu": {"nguon": ma_nguon, "thu_muc": thu_muc, "ten_nguon": ten_nguon, "ten_ho_so": hs["ten"], "luc": int(time.time())}})
    if not tao.get("ok"):
        return tao
    kq = await asyncio.to_thread(_sao_chep_dang_nhap, goc, thu_muc, HOSO / tao["id"])
    _ghi_nk({"op": "ho_so", "ket_qua": "đã nhập", "mo_ta": "Nhập đăng nhập từ hồ sơ %s của %s (%d cookie)" % (hs["ten"], ten_nguon, kq["so_cookie"])})
    canh_bao = []
    if _dang_mo(goc):
        canh_bao.append("%s đang mở nên có thể thiếu những đăng nhập mới nhất. Đóng %s rồi bấm Cập nhật đăng nhập để lấy đủ." % (ten_nguon, ten_nguon))
    if kq["so_cookie"] == 0:
        canh_bao.append("Không đọc được cookie nào từ hồ sơ này. Có thể hồ sơ chưa đăng nhập trang nào; anh đăng nhập thẳng trong trình duyệt vừa tạo.")
    return dict(kq, ok=True, id=tao["id"], ten=tao["ten"], canh_bao=canh_bao)


async def lam_moi_chrome(ma: str) -> dict:
    """Lấy lại đăng nhập mới nhất từ hồ sơ Chrome gốc (khi anh vừa đăng nhập thêm trang ở Chrome)."""
    x = next((y for y in ds_ho_so() if y["id"] == ma), None)
    if not x or not x.get("nhap_tu"):
        return {"ok": False, "loi": "Trình duyệt này không được nhập từ Chrome."}
    nt = x["nhap_tu"]
    nguon = next((y for y in _nguon_trinh_duyet() if y[0] == nt["nguon"]), None)
    if not nguon:
        return {"ok": False, "loi": "Không thấy %s trên máy." % nt.get("ten_nguon")}
    tok = _HS.set(ma)
    try:
        await dong_trinh_duyet()
    finally:
        _HS.reset(tok)
    await asyncio.sleep(1.2)
    kq = await asyncio.to_thread(_sao_chep_dang_nhap, nguon[2], nt["thu_muc"], HOSO / ma)
    d = _doc_hs()
    for y in d["ds"]:
        if y["id"] == ma:
            y["nhap_tu"]["luc"] = int(time.time())
    _luu_hs(d)
    _ghi_nk({"op": "ho_so", "ket_qua": "đã làm mới", "mo_ta": "Làm mới đăng nhập cho %s từ %s (%d cookie)" % (x["ten"], nt.get("ten_nguon"), kq["so_cookie"])})
    return dict(kq, ok=True, canh_bao=(["%s đang mở nên có thể thiếu đăng nhập mới nhất." % nt.get("ten_nguon")] if _dang_mo(nguon[2]) else []))


# ---------------------------------------------------------------- mức tự động của AI
def _nap_muc() -> None:
    try:
        d = json.loads(TEP_MUC.read_text(encoding="utf-8"))
        if d.get("muc") in MUC:
            _tt["muc"] = d["muc"]
            _tt["muc_den"] = float(d.get("muc_den") or 0)
        for h in d.get("mien_toi") or []:
            _mien_toi.add(str(h).lower())
    except (OSError, ValueError):
        pass


def _luu_muc() -> None:
    try:
        DIR.mkdir(parents=True, exist_ok=True)
        TEP_MUC.write_text(json.dumps({"muc": _tt["muc"], "muc_den": _tt["muc_den"], "mien_toi": sorted(_mien_toi)[:20]}, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


def muc_hien_tai() -> str:
    """Mức đang có hiệu lực. Toàn quyền hết hạn thì tự về 'hỏi bước quan trọng'."""
    with _khoa:
        if _tt["muc"] == "toan_quyen" and _tt["muc_den"] and time.time() > _tt["muc_den"]:
            _tt["muc"], _tt["muc_den"] = "quan_trong", 0.0
            _luu_muc()
            _ghi_nk({"op": "muc", "ket_qua": "hết hạn", "mo_ta": "Toàn quyền hết hạn, về mức Hỏi bước quan trọng"})
        return _tt["muc"]


def dat_muc(muc: str, phut: int = 0) -> dict:
    if muc not in MUC:
        return {"ok": False, "loi": "Mức không hợp lệ."}
    with _khoa:
        _tt["muc"] = muc
        _tt["muc_den"] = (time.time() + max(1, int(phut)) * 60) if (muc == "toan_quyen" and phut) else 0.0
        _luu_muc()
    ten = {"hoi_het": "Hỏi mọi bước", "quan_trong": "Hỏi bước quan trọng", "toan_quyen": "Toàn quyền"}[muc]
    _ghi_nk({"op": "muc", "ket_qua": "đã đổi", "mo_ta": "Mức tự động: %s%s" % (ten, (" trong %d phút" % phut) if (muc == "toan_quyen" and phut) else "")})
    return {"ok": True}


def hoc_mien_toi(host: str) -> None:
    """Ghi nhớ tên miền anh đang dùng để mở bảng TISA BOT (chỉ gọi từ đường đã đăng nhập): trang này là chính TISA BOT, được nhận mã dán vào."""
    h = str(host or "").split(",")[0].strip().lower()
    if h and h not in _mien_toi:
        _mien_toi.add(h)
        _luu_muc()


def la_trang_cua_toi(host: str) -> bool:
    h = str(host or "").lower()
    return h.split(":")[0] in ("127.0.0.1", "localhost", "[::1]", "::1") or h in _mien_toi or h.split(":")[0] in {x.split(":")[0] for x in _mien_toi}


# ---------------------------------------------------------------- nhật ký, nhịp, duyệt
def _ghi_nk(d: dict) -> None:
    try:
        DIR.mkdir(parents=True, exist_ok=True)
        d = dict(d, t=time.strftime("%Y-%m-%d %H:%M:%S"))
        with open(TEP_NK, "a", encoding="utf-8") as f:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
        if TEP_NK.stat().st_size > 2_000_000:
            dong = TEP_NK.read_text(encoding="utf-8").splitlines()[-800:]
            TEP_NK.write_text("\n".join(dong) + "\n", encoding="utf-8")
    except OSError:
        pass


def doc_nk(n: int = 30) -> list:
    try:
        return [json.loads(x) for x in TEP_NK.read_text(encoding="utf-8").splitlines()[-n:] if x.strip()]
    except (OSError, ValueError):
        return []


def _qua_nhanh() -> bool:
    now = time.time()
    with _khoa:
        _nhip[:] = [x for x in _nhip if now - x < 60]
        if len(_nhip) >= TOI_DA_MOT_PHUT:
            return True
        _nhip.append(now)
    return False


def _dau_van_tay(op: str, ngu_canh: dict) -> str:
    return "%s|%s|%s" % (op, str(ngu_canh.get("host") or ""), re.sub(r"\s+", " ", str(ngu_canh.get("ten") or ngu_canh.get("gui") or ""))[:80].lower())


def xin_duyet(op: str, ngu_canh: dict, mo_ta: str) -> str:
    with _khoa:
        for k in [k for k, v in _duyet.items() if time.time() - v["luc"] > HIEU_LUC_DUYET]:
            _duyet.pop(k, None)
        for k, v in _duyet.items():          # cùng một việc đang chờ thì dùng lại mã cũ
            if v["van_tay"] == _dau_van_tay(op, ngu_canh) and v["trang_thai"] == "cho":
                return k
        k = uuid.uuid4().hex[:8]
        _duyet[k] = {"luc": time.time(), "van_tay": _dau_van_tay(op, ngu_canh), "trang_thai": "cho", "op": op, "mo_ta": mo_ta,
                     "ten": str(ngu_canh.get("ten") or ngu_canh.get("gui") or "")[:120], "host": str(ngu_canh.get("host") or ""),
                     "trang": str(ngu_canh.get("tieu_de") or "")[:100], "anh": ngu_canh.get("anh") or ""}
        return k


def dung_duyet(duyet_id: str, op: str, ngu_canh: dict) -> bool:
    with _khoa:
        v = _duyet.get(str(duyet_id or ""))
        if not v or v["trang_thai"] != "dong_y" or time.time() - v["luc"] > HIEU_LUC_DUYET:
            return False
        if v["van_tay"] != _dau_van_tay(op, ngu_canh):
            return False
        v["trang_thai"] = "da_dung"
        return True


def quyet_dinh(duyet_id: str, dong_y: bool) -> dict:
    with _khoa:
        v = _duyet.get(str(duyet_id or ""))
        if not v or v["trang_thai"] != "cho":
            return {"ok": False, "loi": "Không còn việc chờ duyệt này."}
        v["trang_thai"] = "dong_y" if dong_y else "tu_choi"
        v["luc"] = time.time()
    _ghi_nk({"op": "duyet", "ket_qua": "đồng ý" if dong_y else "từ chối", "mo_ta": v["mo_ta"], "ten": v["ten"], "host": v["host"]})
    return {"ok": True}


# ---------------------------------------------------------------- trình duyệt
def tim_chrome() -> str:
    env = os.getenv("TISA_BROWSER_EXE")
    if env and Path(env).exists():
        return env
    ds: list = []
    if sys.platform == "darwin":
        ds = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
              "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser", "/Applications/Chromium.app/Contents/MacOS/Chromium"]
    elif os.name == "nt":
        goc = [os.environ.get(k, "") for k in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")]
        for g in goc:
            if g:
                ds += [g + r"\Google\Chrome\Application\chrome.exe", g + r"\Microsoft\Edge\Application\msedge.exe", g + r"\BraveSoftware\Brave-Browser\Application\brave.exe"]
    else:
        ds = [shutil.which(x) or "" for x in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "brave-browser")]
    return next((d for d in ds if d and Path(d).exists()), "")


def _cong_mo(cong: int = 0) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", int(cong) or _cong()), timeout=0.6):
            return True
    except OSError:
        return False


def _http_json(path: str, timeout: float = 4.0, method: str = "GET", cong: int = 0):
    req = urllib.request.Request("http://127.0.0.1:%d%s" % (int(cong) or _cong(), path), method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


async def mo_trinh_duyet(url: str = "", hoso: str = "") -> dict:
    """Mở cửa sổ của MỘT trình duyệt (mỗi trình duyệt một hồ sơ và một cổng riêng). Đã mở thì đưa lên trước, có url thì mở thêm tab."""
    x = tim_ho_so(hoso) if hoso else next((y for y in ds_ho_so() if y["id"] == _hs()), None)
    if not x:
        return {"ok": False, "loi": "Không có trình duyệt tên %s." % hoso}
    hoso = x["id"]
    _HS.set(hoso)
    if _cong_mo():
        if url:
            await _tab_moi(url)
        await len_truoc()
        return {"ok": True, "da_mo": True}
    exe = x.get("exe") if x.get("exe") and Path(x["exe"]).exists() else tim_chrome()
    if not exe:
        return {"ok": False, "loi": "Máy chưa có Chrome hoặc Edge. Cài Google Chrome rồi bấm Mở trình duyệt lại."}
    pf = HOSO / hoso
    pf.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(HOSO, 0o700)
        os.chmod(pf, 0o700)
    except OSError:
        pass
    args = [exe, "--remote-debugging-port=%d" % _cong(hoso), "--remote-debugging-address=127.0.0.1", "--user-data-dir=%s" % pf, "--profile-directory=Default", "--no-first-run", "--restore-last-session",
            "--no-default-browser-check", "--restore-last-session", "--disable-features=Translate,MediaRouter", "--window-size=1280,880", "--lang=vi"]
    if HEADLESS:
        args.append("--headless=new")
    args.append(url or "about:blank")
    try:
        subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, start_new_session=True)
    except OSError as e:
        return {"ok": False, "loi": "Không mở được trình duyệt: %s" % e}
    for _ in range(50):
        await asyncio.sleep(0.3)
        if _cong_mo():
            _ghi_nk({"op": "mo", "ket_qua": "đã mở", "mo_ta": "Mở %s" % _ten_hs(hoso)})
            return {"ok": True, "da_mo": False}
    return {"ok": False, "loi": "Trình duyệt chưa sẵn sàng. Máy có màn hình không? Thử bấm Mở trình duyệt lại."}


async def len_truoc() -> None:
    """Đưa cửa sổ trình duyệt TISA lên trước (chỉ có MỘT trình duyệt dùng chung, anh đăng nhập mọi tài khoản vào đây)."""
    try:
        ds = await asyncio.to_thread(_trang_dang_co)
        if ds:
            async with _Phien(ds[0]["webSocketDebuggerUrl"]) as p:
                await p.gui("Page.bringToFront", timeout=5)
    except Exception:  # noqa: BLE001
        pass
    if sys.platform == "darwin" and not HEADLESS:
        exe = tim_chrome()
        m = re.search(r"/Applications/(.+?)\.app/", exe or "")
        if m:
            try:
                subprocess.Popen(["osascript", "-e", 'tell application "%s" to activate' % m.group(1)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except OSError:
                pass


def _trang_dang_co(hs: str = "") -> list:
    try:
        return [t for t in _http_json("/json/list", cong=_cong(hs)) if t.get("type") == "page" and not str(t.get("url", "")).startswith(("devtools://", "chrome-extension://"))]
    except Exception:  # noqa: BLE001
        return []


async def _ws_url_trinh_duyet() -> str:
    return (await asyncio.to_thread(_http_json, "/json/version")).get("webSocketDebuggerUrl", "")


class _Phien:
    """Một kết nối DevTools tới MỘT trang (hoặc tới trình duyệt khi ws là cấp trình duyệt)."""

    def __init__(self, ws_url: str):
        self.url = ws_url
        self.ws = None
        self.id = 0
        self.cho: dict = {}
        self.tac_vu = None

    async def __aenter__(self):
        import websockets
        self.ws = await websockets.connect(self.url, max_size=60 * 2 ** 20, ping_interval=None, open_timeout=8)
        self.tac_vu = asyncio.create_task(self._nghe())
        return self

    async def __aexit__(self, *a):
        try:
            if self.tac_vu:
                self.tac_vu.cancel()
            if self.ws:
                await self.ws.close()
        except Exception:  # noqa: BLE001
            pass

    async def _nghe(self):
        try:
            async for m in self.ws:
                d = json.loads(m)
                f = self.cho.pop(d.get("id"), None) if "id" in d else None
                if f and not f.done():
                    f.set_result(d)
        except Exception:  # noqa: BLE001
            for f in self.cho.values():
                if not f.done():
                    f.set_exception(RuntimeError("mất kết nối trình duyệt"))

    async def gui(self, method: str, params: dict | None = None, timeout: float = 20.0):
        self.id += 1
        i = self.id
        f = asyncio.get_running_loop().create_future()
        self.cho[i] = f
        await self.ws.send(json.dumps({"id": i, "method": method, "params": params or {}}))
        try:
            d = await asyncio.wait_for(f, timeout)
        except asyncio.TimeoutError:
            self.cho.pop(i, None)
            if method.startswith("Runtime."):      # hộp thoại alert chặn trang: đóng rồi báo
                try:
                    await asyncio.wait_for(self._gui_nhanh("Page.handleJavaScriptDialog", {"accept": True}), 2)
                except Exception:  # noqa: BLE001
                    pass
            raise RuntimeError("trình duyệt không trả lời (%s)" % method)
        if "error" in d:
            raise RuntimeError(str(d["error"].get("message") or d["error"])[:200])
        return d.get("result") or {}

    async def _gui_nhanh(self, method, params):
        self.id += 1
        await self.ws.send(json.dumps({"id": self.id, "method": method, "params": params}))

    async def js(self, bieu_thuc: str, tham_chieu: bool = False, timeout: float = 20.0):
        r = await self.gui("Runtime.evaluate", {"expression": bieu_thuc, "returnByValue": not tham_chieu, "awaitPromise": True, "userGesture": True}, timeout)
        if r.get("exceptionDetails"):
            raise RuntimeError("lỗi trang: " + str((r["exceptionDetails"].get("exception") or {}).get("description") or r["exceptionDetails"].get("text"))[:200])
        return r["result"] if tham_chieu else (r.get("result") or {}).get("value")


async def _trang_hien_tai() -> dict:
    ds = await asyncio.to_thread(_trang_dang_co)
    if not ds:
        raise RuntimeError("Trình duyệt chưa có trang nào. Gọi tisa_browser_look op=open với url.")
    with _khoa:
        tab = _tt.get("tab") or ""
    for t in ds:
        if t.get("id") == tab:
            return t
    return ds[0]


async def _tab_moi(url: str) -> str:
    async with _Phien(await _ws_url_trinh_duyet()) as b:
        r = await b.gui("Target.createTarget", {"url": url})
    with _khoa:
        _tt["tab"] = r.get("targetId", "")
    return r.get("targetId", "")


# ---------------------------------------------------------------- mắt: nhìn trang
_JS_NHIN = r"""(() => {
  const q = 'a[href],button,input,select,textarea,summary,[role=button],[role=link],[role=tab],[role=menuitem],[role=checkbox],[role=radio],[role=switch],[role=option],[role=combobox],[contenteditable=""],[contenteditable=true],[onclick],[tabindex]:not([tabindex="-1"]),code,pre,kbd,samp,input[readonly],textarea[readonly]';
  const hien = e => { const r = e.getBoundingClientRect(); if (r.width < 3 || r.height < 3) return false; const s = getComputedStyle(e);
    if (s.visibility === 'hidden' || s.display === 'none' || +s.opacity === 0) return false; return r.bottom > 0 && r.right > 0 && r.top < innerHeight && r.left < innerWidth; };
  const ten = e => (e.getAttribute('aria-label') || e.innerText || e.value || e.placeholder || e.title || e.alt || e.getAttribute('name') || '').trim().replace(/\s+/g, ' ').slice(0, 90);
  const marks = [], out = [];
  for (const e of document.querySelectorAll(q)) {
    if (!hien(e)) continue; const r = e.getBoundingClientRect(); marks.push(e);
    let host = '', path = ''; if (e.href) { try { const u = new URL(e.href, location.href); host = u.host; path = u.pathname.slice(0, 40); } catch (x) {} }
    out.push({i: marks.length, tag: e.tagName.toLowerCase(), role: e.getAttribute('role') || '', type: e.type || '', name: ten(e), host, path,
      value: e.type === 'password' ? '' : String(e.value || '').slice(0, 40), x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2),
      off: !!e.disabled, on: e.checked === true});
    if (out.length >= 110) break;
  }
  window.__tisa = {marks};
  const rac = CAPTCHA_JS || /xác minh bạn là người|verify you are human|i'm not a robot|tôi không phải người máy/i.test(document.body ? document.body.innerText.slice(0, 4000) : '');
  return {url: location.href, title: document.title, captcha: !!rac,
    text: (document.body ? document.body.innerText : '').replace(/\n{3,}/g, '\n\n').slice(0, 3200),
    scroll: {y: Math.round(scrollY), h: document.documentElement.scrollHeight, vh: innerHeight}, els: out};
})()""".replace("CAPTCHA_JS", _CAPTCHA_JS)

_JS_CON_TRO = r"""((x, y, nhan) => { let c = document.getElementById('__tisa_cur');
  if (!c) { c = document.createElement('div'); c.id = '__tisa_cur';
    c.style.cssText = 'position:fixed;z-index:2147483647;width:24px;height:24px;border-radius:50%;background:rgba(255,107,53,.35);border:3px solid #ff6b35;pointer-events:none;transition:left .3s,top .3s;transform:translate(-50%,-50%);left:' + x + 'px;top:' + y + 'px';
    document.documentElement.appendChild(c);
    const b = document.createElement('div'); b.id = '__tisa_bar';
    b.style.cssText = 'position:fixed;z-index:2147483647;left:50%;top:8px;transform:translateX(-50%);background:#172f72;color:#fff;font:600 13px system-ui,sans-serif;padding:6px 16px;border-radius:999px;pointer-events:none;box-shadow:0 6px 20px rgba(0,0,0,.3)';
    document.documentElement.appendChild(b); }
  requestAnimationFrame(() => { c.style.left = x + 'px'; c.style.top = y + 'px'; });
  document.getElementById('__tisa_bar').textContent = 'TISA BOT đang thao tác: ' + nhan;
  clearTimeout(window.__tisaT); window.__tisaT = setTimeout(() => { for (const id of ['__tisa_bar', '__tisa_cur']) { const e = document.getElementById(id); if (e) e.remove(); } }, 5000); })"""


_MA_DAI = re.compile(r"[A-Za-z0-9_\-\.\~\+/=]{24,}")


def _che(txt: str) -> str:
    """Che chuỗi giống mã bí mật (token, khóa API, đường dẫn MCP kèm khóa) trước khi đưa cho mô hình. Muốn chuyển mã thì dùng op=dan_ma, giá trị không qua mô hình."""
    def f(m):
        x = m.group(0)
        return "⟦mã ẩn %d ký tự⟧" % len(x) if ((re.search(r"[0-9]", x) and re.search(r"[A-Za-z]", x)) or len(x) >= 60) else x
    return _MA_DAI.sub(f, str(txt or ""))


def _dong_phan_tu(e: dict) -> str:
    loai = {"a": "liên kết", "button": "nút", "input": "ô nhập", "textarea": "ô nhập dài", "select": "danh sách chọn", "summary": "mục gập"}.get(e["tag"], e.get("role") or e["tag"])
    if e["tag"] == "input" and e.get("type") in ("checkbox", "radio", "submit", "button", "file", "password", "search", "email", "tel", "number", "date"):
        loai += " " + e["type"]
    s = '[%d] %s "%s"' % (e["i"], loai, _che(e["name"]))
    if e.get("value") and e["tag"] in ("input", "textarea", "select"):
        s += ' (đang có: "%s")' % _che(e["value"])
    if e.get("on"):
        s += " (đã chọn)"
    if e.get("off"):
        s += " (tắt)"
    if e.get("host"):
        s += " -> %s%s" % (e["host"], e.get("path") or "")
    return s + "  @%d,%d" % (e["x"], e["y"])


async def nhin() -> str:
    t = await _trang_hien_tai()
    async with _Phien(t["webSocketDebuggerUrl"]) as p:
        d = await p.js(_JS_NHIN)
    host = urllib.parse.urlparse(d["url"]).netloc
    phan_loai_trang = phan_loai({"host": host, "url": d["url"]})[0]
    dong = ["TRANG: %s | %s" % (d["title"][:100], d["url"][:200]),
            "Cuộn: %d/%d (cao màn hình %d)" % (d["scroll"]["y"], d["scroll"]["h"], d["scroll"]["vh"])]
    if phan_loai_trang == "chan":
        dong.append("TRANG BỊ CHẶN: ngân hàng, ví, cổng thanh toán hoặc sàn coin. Agent chỉ đọc, mọi thao tác do anh tự làm.")
    if d.get("captcha"):
        dong.append("CÓ CAPTCHA hoặc kiểm tra người máy: dừng lại, gọi tisa_browser_do op=wait_user ly_do=\"giải CAPTCHA\" cho anh giải.")
    dong.append("CHỮ TRÊN TRANG (rút gọn; chuỗi giống mã bí mật được che, muốn chuyển mã thì dùng op=dan_ma):\n" + _che(d["text"]))
    dong.append("PHẦN TỬ TƯƠNG TÁC (gọi theo số trong ngoặc vuông; số chỉ đúng cho lần look này):")
    dong += [_dong_phan_tu(e) for e in d["els"]] or ["(không thấy nút hay ô nhập nào trong màn hình này, thử cuộn)"]
    return "\n".join(dong)


# ---------------------------------------------------------------- tay: thao tác
_PHIM = {"Enter": (13, "\r"), "Tab": (9, ""), "Escape": (27, ""), "Backspace": (8, ""), "Delete": (46, ""), "ArrowDown": (40, ""), "ArrowUp": (38, ""),
         "ArrowLeft": (37, ""), "ArrowRight": (39, ""), "PageDown": (34, ""), "PageUp": (33, ""), "Home": (36, ""), "End": (35, ""), "Space": (32, " ")}


async def _ngu_canh_phan_tu(p: _Phien, i: int) -> dict:
    return await p.js("""(() => { const m = (window.__tisa && window.__tisa.marks) || []; const e = m[%d - 1];
      if (!e) return {loi: 'Số %d không còn trên trang. Gọi tisa_browser_look op=look lại để lấy số mới.'};
      e.scrollIntoView({block: 'center', inline: 'center'}); const r = e.getBoundingClientRect(); const f = e.closest('form,[role=dialog],dialog');
      const nut = f ? [...f.querySelectorAll('button,input[type=submit],[role=button]')].map(b => (b.innerText || b.value || '').trim()).filter(Boolean).slice(0, 6).join(' | ') : '';
      return {x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2), tag: e.tagName.toLowerCase(), kieu: e.type || '', ac: e.autocomplete || '',
        ten: (e.getAttribute('aria-label') || e.innerText || e.value || e.placeholder || e.title || e.name || '').trim().replace(/\\s+/g, ' ').slice(0, 100),
        nhan: (e.labels && e.labels[0] ? e.labels[0].innerText : '') + ' ' + (e.placeholder || '') + ' ' + (e.name || '') + ' ' + (e.id || ''),
        gui: nut, host: location.host, url: location.href, tieu_de: document.title, captcha: %s}; })()""" % (int(i), int(i), _CAPTCHA_JS))


async def _chuot(p: _Phien, x: int, y: int, nhan: str) -> None:
    try:
        await p.js("(%s)(%d,%d,%s)" % (_JS_CON_TRO, x, y, json.dumps(("[%s] %s" % (_ten_hs(), nhan))[:70], ensure_ascii=False)), timeout=5)
    except RuntimeError:
        pass
    await p.gui("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
    await asyncio.sleep(random.uniform(0.25, 0.55))
    await p.gui("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    await asyncio.sleep(random.uniform(0.05, 0.14))
    await p.gui("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})


async def _chup(p: _Phien, ten: str = "") -> str:
    r = await p.gui("Page.captureScreenshot", {"format": "jpeg", "quality": 62})
    ANH.mkdir(parents=True, exist_ok=True)
    f = ANH / ((ten or time.strftime("%Y%m%d-%H%M%S")) + ".jpg")
    f.write_bytes(base64.b64decode(r["data"]))
    for x in sorted(ANH.glob("*.jpg"))[:-60]:      # giữ 60 ảnh mới nhất
        try:
            x.unlink()
        except OSError:
            pass
    return str(f)


def _chan_neu_can(op: str, nc: dict, duyet_id: str):
    """None nếu được làm; ngược lại chuỗi trả cho agent."""
    loai, mo_ta = phan_loai(nc)
    muc = muc_hien_tai()
    if loai == "vo_hai":
        if muc == "hoi_het" and op in ("click", "type", "select", "upload", "press_enter", "press"):
            loai, mo_ta = "can_duyet", "Bước thao tác (mức Hỏi mọi bước)"
        else:
            return None
    if loai == "can_duyet" and muc == "toan_quyen":
        _ghi_nk({"op": op, "ket_qua": "tự duyệt (toàn quyền)", "mo_ta": mo_ta, "ten": nc.get("ten", ""), "host": nc.get("host", "")})
        return None
    if loai == "chan":
        _ghi_nk({"op": op, "ket_qua": "chặn", "mo_ta": mo_ta, "ten": nc.get("ten", ""), "host": nc.get("host", "")})
        return "BI_CHAN: " + mo_ta
    if loai in ("bi_mat", "tien"):
        _ghi_nk({"op": op, "ket_qua": "chờ người dùng", "mo_ta": mo_ta, "ten": nc.get("ten", ""), "host": nc.get("host", "")})
        return ("CAN_NGUOI_DUNG: %s Dừng ở đây, nói với anh việc cần làm rồi gọi tisa_browser_do op=wait_user ly_do=\"...\" để chờ anh làm xong. "
                "Không tự nhập, không tìm cách vòng." % mo_ta)
    if dung_duyet(duyet_id, op, nc):
        return None
    k = xin_duyet(op, nc, mo_ta)
    _ghi_nk({"op": op, "ket_qua": "chờ duyệt", "mo_ta": mo_ta, "ten": nc.get("ten", ""), "host": nc.get("host", "")})
    return ("CAN_DUYET: %s: \"%s\" trên %s (mức tự động hiện tại: %s). Anh phải bấm Duyệt trong TISA BOT (có thẻ nổi, anh cũng có thể chọn Duyệt và cho AI tự làm tiếp). "
            "Nói rõ với anh sẽ làm gì rồi gọi lại đúng lệnh này với duyet_id=\"%s\" sau khi anh duyệt. Chưa duyệt thì KHÔNG làm." %
            (mo_ta, nc.get("ten") or nc.get("gui") or "", nc.get("host", ""), {"hoi_het": "hỏi mọi bước", "quan_trong": "hỏi bước quan trọng"}.get(muc, muc), k))


async def thuc_hien(op: str, a: dict) -> str:
    op = str(op or "").strip().lower()
    a = a or {}
    chon = a.get("trinh_duyet") or a.get("browser") or ""
    if chon:
        x = tim_ho_so(str(chon))
        if not x:
            return "LOI: không có trình duyệt \"%s\". Các trình duyệt hiện có: %s." % (chon, ", ".join("%s" % y["ten"] for y in ds_ho_so()))
        _HS.set(x["id"])
    else:
        _HS.set(hs_dang_dung())
    if op == "profiles":
        cur = hs_dang_dung()
        return "Các trình duyệt (mỗi cái đăng nhập tài khoản riêng):\n" + "\n".join("- %s%s: %s" % (y["ten"], " (đang dùng mặc định)" if y["id"] == cur else "", "đang mở" if _cong_mo(y["cong"]) else "chưa mở") for y in ds_ho_so()) + \
            "\nChọn trình duyệt khác bằng tham số trinh_duyet=<tên hoặc số>. Không chọn thì dùng trình duyệt mặc định."
    with _khoa:
        dung = _tt["dung"]
    if dung and op not in ("status", "tabs"):
        return "DA_DUNG: Anh đã bấm Dừng ngay. Không thao tác tiếp, hỏi anh khi nào cho làm tiếp."
    if op == "status":
        return json.dumps(trang_thai(), ensure_ascii=False)
    if op not in ("open", "tabs") and not _cong_mo():
        return "CHUA_MO: %s chưa mở. Gọi tisa_browser_look op=open url=... (cửa sổ sẽ hiện trên máy anh), hoặc nhờ anh bấm Mở trình duyệt." % _ten_hs()
    if op in ("click", "type", "press", "scroll", "select", "upload", "dan_ma", "back", "forward", "reload", "new_tab", "open") and _qua_nhanh():
        return "CHAM_LAI: Thao tác quá nhanh (tối đa %d lần mỗi phút để giống người thật và không bị nền tảng khóa). Chờ vài giây rồi làm tiếp." % TOI_DA_MOT_PHUT
    try:
        if op == "open":
            url = str(a.get("url") or "").strip()
            if not re.match(r"^https?://", url):
                url = "https://" + url if url and "." in url else ""
            if not url:
                return "LOI: thiếu url (ví dụ https://www.facebook.com)."
            r = await mo_trinh_duyet(url if not _cong_mo() else "")
            if not r.get("ok"):
                return "LOI: " + r["loi"]
            if r.get("da_mo") or _cong_mo():
                t = await _trang_hien_tai() if _trang_dang_co() else None
                if t is None:
                    await _tab_moi(url)
                else:
                    async with _Phien(t["webSocketDebuggerUrl"]) as p:
                        await p.gui("Page.navigate", {"url": url})
                        await _doi_tai(p)
            else:
                await asyncio.sleep(1.5)
            _ghi_nk({"op": "open", "ket_qua": "ok", "mo_ta": url[:140], "host": urllib.parse.urlparse(url).netloc})
            return await nhin()
        if op == "look":
            return await nhin()
        if op == "tabs":
            ds = await asyncio.to_thread(_trang_dang_co)
            with _khoa:
                tab = _tt.get("tab") or (ds[0]["id"] if ds else "")
            return "\n".join("%s %s | %s | %s" % ("*" if t["id"] == tab else " ", t["id"][:8], t.get("title", "")[:60], t.get("url", "")[:100]) for t in ds) or "(chưa có tab nào)"
        if op == "screenshot":
            t = await _trang_hien_tai()
            async with _Phien(t["webSocketDebuggerUrl"]) as p:
                f = await _chup(p)
            return "Ảnh chụp màn hình đã lưu: %s (đọc ảnh bằng công cụ đọc file nếu cần nhìn bố cục)." % f
        t = await _trang_hien_tai()
        async with _Phien(t["webSocketDebuggerUrl"]) as p:
            return await _thao_tac(op, a, p, t)
    except RuntimeError as e:
        _ghi_nk({"op": op, "ket_qua": "lỗi", "mo_ta": str(e)[:160]})
        return "LOI: %s" % e
    except Exception as e:  # noqa: BLE001
        _ghi_nk({"op": op, "ket_qua": "lỗi", "mo_ta": "%s: %s" % (type(e).__name__, str(e)[:140])})
        return "LOI: %s: %s" % (type(e).__name__, str(e)[:200])


async def _doi_tai(p: _Phien, toi_da: float = 15.0) -> None:
    t0 = time.time()
    await asyncio.sleep(0.6)
    while time.time() - t0 < toi_da:
        try:
            if await p.js("document.readyState", timeout=4) == "complete":
                break
        except RuntimeError:
            pass
        await asyncio.sleep(0.4)
    await asyncio.sleep(0.5)


async def _dan_ma(a: dict, p_dich: _Phien, t_dich: dict) -> str:
    """Chép một giá trị (mã API, token, đường dẫn MCP...) từ một ô hoặc khối chữ ở tab NGUỒN rồi dán vào ô của TISA BOT ở tab hiện tại.
    Giá trị đi thẳng từ trang này sang trang kia, KHÔNG BAO GIỜ trả về cho mô hình và không ghi vào nhật ký. Chỉ dán được vào trang của chính TISA BOT."""
    host_dich = urllib.parse.urlparse(t_dich.get("url", "")).netloc
    if not la_trang_cua_toi(host_dich):
        return ("BI_CHAN: dan_ma chỉ dán vào trang của chính TISA BOT (127.0.0.1, localhost hoặc tên miền anh đang dùng để mở TISA BOT). Tab hiện tại là %s. "
                "Chuyển sang tab TISA BOT (switch_tab), look để lấy số ô, rồi gọi lại." % (host_dich or "trống"))
    tu_tab = str(a.get("tu_tab") or "")
    try:
        tu_id, den_id = int(a.get("tu_id") or 0), int(a.get("id") or 0)
    except (TypeError, ValueError):
        tu_id = den_id = 0
    if not tu_tab or tu_id <= 0 or den_id <= 0:
        return "LOI: dan_ma cần tu_tab (mã tab nguồn, xem op=tabs), tu_id (số [n] ở tab nguồn, từ look) và id (số [n] của ô đích ở tab hiện tại)."
    hs_nguon = ""
    if a.get("tu_trinh_duyet"):
        xn = tim_ho_so(str(a.get("tu_trinh_duyet")))
        if not xn:
            return "LOI: không có trình duyệt nguồn \"%s\"." % a.get("tu_trinh_duyet")
        hs_nguon = xn["id"]
    ds = await asyncio.to_thread(_trang_dang_co, hs_nguon)
    nguon = next((x for x in ds if x["id"].startswith(tu_tab)), None)
    if not nguon:
        return "LOI: không thấy tab nguồn %s (xem op=tabs)." % tu_tab
    if nguon["id"] == t_dich["id"] and not hs_nguon:
        return "LOI: tab nguồn và tab đích trùng nhau."
    async with _Phien(nguon["webSocketDebuggerUrl"]) as ps:
        gia_tri = await ps.js("""(() => { const e = (window.__tisa && window.__tisa.marks || [])[%d - 1]; if (!e) return null;
          const v = (e.value !== undefined && String(e.value) !== '') ? e.value : (e.innerText || e.textContent || ''); return String(v).trim(); })()""" % tu_id)
    if not gia_tri:
        return "LOI: không đọc được giá trị ở ô [%d] của tab nguồn (số có thể đã cũ: look lại tab nguồn)." % tu_id
    if len(gia_tri) > 6000:
        return "LOI: giá trị dài bất thường (%d ký tự), không dán." % len(gia_tri)
    nc = await _ngu_canh_phan_tu(p_dich, den_id)
    if nc.get("loi"):
        return "LOI: " + nc["loi"]
    if nc.get("tag") not in ("input", "textarea"):
        return "LOI: ô đích [%d] không phải ô nhập." % den_id
    if re.search(r"login|dang-nhap|signin|auth", t_dich.get("url", ""), re.I) or nc.get("ac") in ("current-password", "new-password"):
        return "BI_CHAN: đây là trang đăng nhập TISA BOT, không dán mã vào đây. Anh tự đăng nhập, rồi mở đúng trang kết nối."
    await _chuot(p_dich, nc["x"], nc["y"], "dán mã (ẩn)")
    await p_dich.js("""(() => { const e = document.activeElement; if (e) { if (e.select) e.select(); document.execCommand('selectAll'); document.execCommand('delete'); } })()""", timeout=5)
    await p_dich.gui("Input.insertText", {"text": gia_tri})
    _ghi_nk({"op": "dan_ma", "ket_qua": "ok", "mo_ta": "Dán mã (%d ký tự, ẩn) từ %s vào TISA BOT" % (len(gia_tri), urllib.parse.urlparse(nguon.get("url", "")).netloc),
             "ten": nc.get("ten", ""), "host": host_dich})
    return "Đã chuyển %d ký tự (giá trị được giấu, em không nhìn thấy) vào ô [%d] \"%s\". Bấm nút Lưu hoặc Kiểm tra của TISA BOT để hoàn tất." % (len(gia_tri), den_id, nc.get("ten", ""))


async def _thao_tac(op: str, a: dict, p: _Phien, t: dict) -> str:
    duyet_id = str(a.get("duyet_id") or "")
    if op in ("click", "type", "select", "upload"):
        i = int(a.get("id") or 0)
        if i <= 0 and op == "click" and a.get("x") is not None and a.get("y") is not None:
            nc = {"host": urllib.parse.urlparse(t.get("url", "")).netloc, "url": t.get("url", ""), "tag": "", "ten": str(a.get("ly_do") or "bấm theo tọa độ"), "tieu_de": t.get("title", "")}
            nc["captcha"] = bool(await p.js(_CAPTCHA_JS))
            x, y = int(a["x"]), int(a["y"])
        else:
            if i <= 0:
                return "LOI: thiếu id (số trong ngoặc vuông của tisa_browser_look)."
            nc = await _ngu_canh_phan_tu(p, i)
            if nc.get("loi"):
                return "LOI: " + nc["loi"]
            x, y = nc["x"], nc["y"]
        if op == "type" and nc.get("tag") not in ("input", "textarea", "") and not str(a.get("text") or ""):
            return "LOI: thiếu text."
        loai_op = "type" if op == "type" else op
        if op == "type" and nc.get("tag") in ("input", "textarea"):
            nc2 = dict(nc, gui="")            # gõ chữ không bị coi là gửi; chỉ chặn ô bí mật
            kq = _chan_neu_can("type", nc2, duyet_id) if (phan_loai(nc2)[0] in ("bi_mat", "chan") or muc_hien_tai() == "hoi_het") else None
        else:
            kq = _chan_neu_can(loai_op, nc, duyet_id)
        if kq:
            return kq
        if op == "click":
            await _chuot(p, x, y, str(nc.get("ten") or "bấm")[:50])
            await _doi_tai(p, 5)
            _ghi_nk({"op": "click", "ket_qua": "ok", "ten": nc.get("ten", ""), "host": nc.get("host", "")})
            return "Đã bấm [%s] \"%s\". Gọi look để xem trang sau khi bấm." % (i or "%d,%d" % (x, y), nc.get("ten", ""))
        if op == "type":
            await _chuot(p, x, y, "gõ: " + str(a.get("text") or "")[:30])
            if a.get("xoa", True):
                await p.js("""(() => { const e = document.activeElement; if (e) { if (e.select) e.select(); document.execCommand('selectAll'); document.execCommand('delete'); } })()""", timeout=5)
            text = str(a.get("text") or "")
            for khuc in [text[k:k + 40] for k in range(0, len(text), 40)] or [""]:
                if khuc:
                    await p.gui("Input.insertText", {"text": khuc})
                await asyncio.sleep(random.uniform(0.04, 0.16))
            _ghi_nk({"op": "type", "ket_qua": "ok", "ten": nc.get("ten", ""), "host": nc.get("host", ""), "mo_ta": "gõ %d ký tự" % len(text)})
            if a.get("enter"):
                return "Đã gõ %d ký tự vào [%s]. Muốn gửi thì gọi op=press key=Enter (có thể cần duyệt)." % (len(text), i)
            return "Đã gõ %d ký tự vào [%s] \"%s\"." % (len(text), i, nc.get("ten", ""))
        if op == "select":
            ok = await p.js("""(() => { const e = (window.__tisa.marks || [])[%d - 1]; if (!e || e.tagName !== 'SELECT') return false; const v = %s.toLowerCase();
              const o = [...e.options].find(o => o.value.toLowerCase() === v || o.text.trim().toLowerCase() === v || o.text.toLowerCase().includes(v)); if (!o) return false;
              e.value = o.value; e.dispatchEvent(new Event('input', {bubbles: true})); e.dispatchEvent(new Event('change', {bubbles: true})); return true; })()""" % (i, json.dumps(str(a.get("value") or ""))))
            _ghi_nk({"op": "select", "ket_qua": "ok" if ok else "không thấy", "ten": nc.get("ten", ""), "host": nc.get("host", "")})
            return "Đã chọn." if ok else "LOI: không có lựa chọn khớp (op=select chỉ dùng cho danh sách chọn <select>; menu tự vẽ thì bấm từng mục)."
        if op == "upload":
            f = Path(str(a.get("path") or "")).expanduser()
            if not f.is_file():
                return "LOI: không thấy tệp %s" % f
            obj = await p.js("(window.__tisa.marks || [])[%d - 1]" % i, tham_chieu=True)
            await p.gui("DOM.setFileInputFiles", {"files": [str(f)], "objectId": obj["objectId"]})
            _ghi_nk({"op": "upload", "ket_qua": "ok", "ten": f.name, "host": nc.get("host", "")})
            return "Đã chọn tệp %s vào ô tải lên [%d]." % (f.name, i)
    if op == "dan_ma":
        return await _dan_ma(a, p, t)
    if op == "press":
        key = str(a.get("key") or "Enter")
        ctx = await p.js("""(() => { const e = document.activeElement || document.body; const f = e.closest && e.closest('form,[role=dialog],dialog');
          const nut = f ? [...f.querySelectorAll('button[type=submit],input[type=submit],button:not([type]),[role=button]')].map(b => (b.innerText || b.value || '').trim()).filter(Boolean).slice(0, 4).join(' | ') : '';
          return {tag: (e.tagName || '').toLowerCase(), kieu: e.type || '', ac: e.autocomplete || '', ten: (e.getAttribute && e.getAttribute('aria-label')) || e.name || '', gui: nut,
            host: location.host, url: location.href, tieu_de: document.title, captcha: %s}; })()""" % _CAPTCHA_JS)
        if key == "Enter":
            kq = _chan_neu_can("press_enter", dict(ctx, ten=ctx.get("gui") or ctx.get("ten")), duyet_id)
            if kq:
                return kq
        ma, ky_tu = _PHIM.get(key, (0, key if len(key) == 1 else ""))
        for kieu in ("keyDown", "keyUp"):
            await p.gui("Input.dispatchKeyEvent", {"type": kieu, "key": key, "code": key, "windowsVirtualKeyCode": ma, "text": ky_tu if kieu == "keyDown" else ""})
        await _doi_tai(p, 5)
        _ghi_nk({"op": "press", "ket_qua": "ok", "ten": key, "host": ctx.get("host", "")})
        return "Đã nhấn %s. Gọi look để xem trang." % key
    if op == "scroll":
        huong = str(a.get("huong") or a.get("direction") or "down").lower()
        px = int(a.get("px") or 600)
        await p.gui("Input.dispatchMouseEvent", {"type": "mouseWheel", "x": 400, "y": 300, "deltaX": 0, "deltaY": px if huong in ("down", "xuong") else -px})
        await asyncio.sleep(0.5)
        _ghi_nk({"op": "scroll", "ket_qua": "ok", "ten": huong})
        return "Đã cuộn %s %dpx. Gọi look để thấy phần mới." % (huong, px)
    if op in ("back", "forward", "reload"):
        h = await p.gui("Page.getNavigationHistory")
        if op == "reload":
            await p.gui("Page.reload")
        else:
            i = h["currentIndex"] + (-1 if op == "back" else 1)
            if i < 0 or i >= len(h["entries"]):
                return "LOI: không còn trang để %s." % op
            await p.gui("Page.navigateToHistoryEntry", {"entryId": h["entries"][i]["id"]})
        await _doi_tai(p)
        return "Đã %s. Gọi look để xem trang." % op
    if op == "wait":
        ms = min(max(int(a.get("ms") or 1500), 200), 15000)
        cho = str(a.get("text") or "")
        t0 = time.time()
        while True:
            await asyncio.sleep(0.5)
            if cho and cho.lower() in str(await p.js("document.body ? document.body.innerText : ''", timeout=5)).lower():
                return "Thấy chữ \"%s\" trên trang." % cho
            if time.time() - t0 >= ms / 1000:
                return "Đã chờ %.1f giây%s." % (ms / 1000, (" nhưng chưa thấy chữ \"%s\"" % cho) if cho else "")
    if op == "wait_user":
        ly_do = str(a.get("ly_do") or "làm bước cần anh")[:200]
        toi_da = min(max(int(a.get("giay") or 180), 10), 600)
        cho = str(a.get("text") or "")
        url0 = t.get("url", "")
        with _khoa:
            _tt["cho_nguoi"] = {"ly_do": ly_do, "luc": time.time()}
        _ghi_nk({"op": "wait_user", "ket_qua": "đang chờ anh", "mo_ta": ly_do, "host": urllib.parse.urlparse(url0).netloc})
        try:
            t0 = time.time()
            while time.time() - t0 < toi_da:
                await asyncio.sleep(1.5)
                with _khoa:
                    if _tt["dung"]:
                        return "DA_DUNG: Anh đã bấm Dừng ngay."
                try:
                    now = await p.js("({u: location.href, t: document.body ? document.body.innerText.slice(0, 6000) : ''})", timeout=5)
                except RuntimeError:
                    continue
                if cho and cho.lower() in now["t"].lower():
                    return "Anh đã làm xong (thấy chữ \"%s\"). Gọi look để xem trang." % cho
                if not cho and now["u"] != url0 and time.time() - t0 > 4:
                    return "Trang đã đổi sang %s, có vẻ anh đã làm xong. Gọi look để kiểm tra." % now["u"][:120]
            return "HET_GIO: Chờ %d giây mà chưa thấy anh làm xong. Hỏi anh lại trong khung chat." % toi_da
        finally:
            with _khoa:
                _tt["cho_nguoi"] = None
    if op == "new_tab":
        url = str(a.get("url") or "about:blank")
        await _tab_moi(url)
        _ghi_nk({"op": "new_tab", "ket_qua": "ok", "mo_ta": url[:120]})
        return "Đã mở tab mới. Gọi look để xem."
    if op == "switch_tab":
        k = str(a.get("tab") or "")
        ds = await asyncio.to_thread(_trang_dang_co)
        m = next((x for x in ds if x["id"].startswith(k)), None)
        if not m:
            return "LOI: không thấy tab %s (xem op=tabs)." % k
        with _khoa:
            _tt["tab"] = m["id"]
        async with _Phien(await _ws_url_trinh_duyet()) as b:
            await b.gui("Target.activateTarget", {"targetId": m["id"]})
        return "Đã chuyển sang tab %s." % m.get("title", "")[:50]
    if op == "close_tab":
        async with _Phien(await _ws_url_trinh_duyet()) as b:
            await b.gui("Target.closeTarget", {"targetId": t["id"]})
        with _khoa:
            _tt["tab"] = ""
        return "Đã đóng tab."
    return "LOI: op không hợp lệ: %s" % op


# ---------------------------------------------------------------- trạng thái cho bảng điều khiển
_DAU_PHIEN = {"c_user", "xs", "sessionid", "sid", "ssid", "auth_token", "li_at", "oauth_token", "session", "token", "access_token", "zpsid", "zpw_sek", "sapisid", "__secure-1psid", "login"}


def trang_thai(hs: str = "") -> dict:
    if hs:
        _HS.set(hs)
    mo = _cong_mo()
    out = {"dang_chay": mo, "chrome": Path(tim_chrome()).name if tim_chrome() else "", "dung": _tt["dung"], "hoso": _hs(), "muc": muc_hien_tai(), "muc_den": _tt["muc_den"],
           "cho_nguoi": _tt["cho_nguoi"], "trang": [], "cho_duyet": [], "nhat_ky": doc_nk(14),
           "ho_so_ds": [{"id": x["id"], "ten": x["ten"], "dang_chay": _cong_mo(x["cong"]), "nhap_tu": (x.get("nhap_tu") or {}).get("ten_nguon", "")} for x in ds_ho_so()], "hoso_dang_dung": hs_dang_dung(), "hoso_xem": _hs(), "ten_xem": _ten_hs()}
    if mo:
        out["trang"] = [{"id": t["id"][:8], "tieu_de": t.get("title", "")[:70], "host": urllib.parse.urlparse(t.get("url", "")).netloc} for t in _trang_dang_co()][:8]
    with _khoa:
        for k, v in _duyet.items():
            if v["trang_thai"] == "cho" and time.time() - v["luc"] < HIEU_LUC_DUYET:
                out["cho_duyet"].append({"id": k, "op": v["op"], "mo_ta": v["mo_ta"], "ten": v["ten"], "host": v["host"], "trang": v["trang"]})
    return out


async def trang_da_dang_nhap(hs: str = "") -> list:
    """Tên miền có phiên đăng nhập (chỉ tên miền và số cookie, không bao giờ giá trị)."""
    if hs:
        _HS.set(hs)
    if not _cong_mo():
        return []
    try:
        async with _Phien(await _ws_url_trinh_duyet()) as b:
            r = await b.gui("Storage.getCookies", timeout=8)
    except Exception:  # noqa: BLE001
        return []
    ds: dict = {}
    for c in r.get("cookies", []):
        d = str(c.get("domain", "")).lstrip(".")
        goc = ".".join(d.split(".")[-2:]) if d.count(".") >= 1 else d
        e = ds.setdefault(goc, {"mien": goc, "so": 0, "phien": False})
        e["so"] += 1
        if str(c.get("name", "")).lower() in _DAU_PHIEN:
            e["phien"] = True
    return sorted(ds.values(), key=lambda x: (not x["phien"], -x["so"]))[:40]


async def dong_trinh_duyet(hs: str = "") -> dict:
    if hs:
        _HS.set(hs)
    if not _cong_mo():
        return {"ok": True}
    try:
        async with _Phien(await _ws_url_trinh_duyet()) as b:
            await b.gui("Browser.close", timeout=5)
    except Exception:  # noqa: BLE001
        pass
    _ghi_nk({"op": "dong", "ket_qua": "đã đóng", "mo_ta": "Đóng %s" % _ten_hs()})
    return {"ok": True}


# ---------------------------------------------------------------- đăng ký vào hub và máy chủ
_MO_TA_NHIN = ("Trình duyệt riêng của TISA BOT trên máy anh (anh đăng nhập sẵn các trang). op=open url=... mở trang (tự bật cửa sổ nếu chưa mở); op=look xem trang hiện tại: "
               "chữ và danh sách nút, ô nhập đánh số [n]; op=screenshot chụp màn hình; op=tabs liệt kê tab; op=status; op=profiles liệt kê các trình duyệt (mỗi cái đăng nhập tài khoản riêng, ví dụ Facebook 1, Facebook 2); chọn cái cần dùng bằng trinh_duyet=<tên hoặc số>. Dùng khi việc không có MCP hay API và phải thao tác trên "
               "web. Làm theo kỹ năng dq-trinh-duyet. Agent không nhập mật khẩu, mã xác thực, CAPTCHA, không thanh toán.")
_MO_TA_LAM = ("Điều khiển trình duyệt TISA như người thật. op=click id=n (hoặc x,y); op=type id=n text=... (xoa=false để không xóa chữ cũ); op=press key=Enter|Tab|Escape...; "
              "op=scroll huong=down|up px=600; op=select id=n value=...; op=upload id=n path=...; op=wait ms=... text=...; op=wait_user ly_do=... (chờ anh đăng nhập, nhập mã, giải CAPTCHA); "
              "op=dan_ma tu_tab=<mã tab nguồn> tu_id=<số ô nguồn> id=<số ô đích> (chép mã API, token từ trang nền tảng sang ô của TISA BOT mà em không nhìn thấy giá trị; chỉ dán vào trang TISA BOT); op=back|forward|reload|new_tab url|switch_tab tab|close_tab. Mọi lần bấm phải sau một lần look (số n chỉ đúng cho lần look gần nhất). Việc đăng, gửi, xóa, đổi bảo mật trả CAN_DUYET: "
              "xin anh duyệt rồi gọi lại với duyet_id. Làm theo kỹ năng dq-trinh-duyet.")


def dang_ky_hub(add, vault_root=None) -> None:
    async def _nhin(args):
        a = args or {}
        op = str(a.get("op") or "look").lower()
        if op not in ("open", "look", "screenshot", "tabs", "status", "profiles"):
            return "LOI: op của tisa_browser_look chỉ là open, look, screenshot, tabs, status, profiles. Thao tác bấm, gõ dùng tisa_browser_do."
        return await thuc_hien(op, a)

    async def _lam(args):
        a = args or {}
        op = str(a.get("op") or "").lower()
        if op in ("open", "look", "screenshot", "tabs", "status", "profiles", ""):
            return "LOI: op của tisa_browser_do: click, type, press, scroll, select, upload, dan_ma, wait, wait_user, back, forward, reload, new_tab, switch_tab, close_tab."
        return await thuc_hien(op, a)

    add("tisa_browser_look", _MO_TA_NHIN,
        {"op": {"type": "string", "description": "open | look | screenshot | tabs | status | profiles (mặc định look)"}, "url": {"type": "string"},
         "trinh_duyet": {"type": "string", "description": "tên hoặc số của trình duyệt cần dùng (xem op=profiles); bỏ trống = trình duyệt mặc định"}},
        [], _nhin, effect="write")
    add("tisa_browser_do", _MO_TA_LAM,
        {"op": {"type": "string"}, "id": {"type": "integer", "description": "số [n] từ look"}, "x": {"type": "integer"}, "y": {"type": "integer"},
         "text": {"type": "string"}, "key": {"type": "string"}, "value": {"type": "string"}, "path": {"type": "string"}, "url": {"type": "string"},
         "huong": {"type": "string"}, "px": {"type": "integer"}, "ms": {"type": "integer"}, "giay": {"type": "integer"}, "tab": {"type": "string"},
         "ly_do": {"type": "string"}, "duyet_id": {"type": "string"}, "xoa": {"type": "boolean"}, "tu_tab": {"type": "string"}, "tu_id": {"type": "integer"},
         "trinh_duyet": {"type": "string", "description": "tên hoặc số của trình duyệt cần dùng; bỏ trống = trình duyệt mặc định"}, "tu_trinh_duyet": {"type": "string", "description": "dan_ma: trình duyệt chứa trang nguồn"}},
        ["op"], _lam, effect="write")


def gan(app) -> None:
    @app.get("/trinh-duyet/trang-thai")
    async def tb_trang_thai(request: Request, nhe: int = 0, hoso: str = ""):
        from fastapi.responses import JSONResponse
        hoc_mien_toi(request.headers.get("x-forwarded-host") or request.headers.get("host") or "")
        x = tim_ho_so(hoso) if hoso else None
        hs = x["id"] if x else ""
        d = trang_thai(hs)
        d["da_dang_nhap"] = await trang_da_dang_nhap(hs) if (d["dang_chay"] and not nhe) else []
        return JSONResponse(d)

    @app.post("/trinh-duyet/mo")
    async def tb_mo(request: Request):
        from fastapi.responses import JSONResponse
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        url = str((d or {}).get("url") or "")
        if url and not re.match(r"^https?://", url):
            url = ""
        return JSONResponse(await mo_trinh_duyet(url, str((d or {}).get("hoso") or "")))

    @app.post("/trinh-duyet/dong")
    async def tb_dong(request: Request):
        from fastapi.responses import JSONResponse
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        x = tim_ho_so(str((d or {}).get("hoso") or "")) if (d or {}).get("hoso") else None
        return JSONResponse(await dong_trinh_duyet(x["id"] if x else ""))

    @app.get("/trinh-duyet/nguon-chrome")
    async def tb_nguon():
        from fastapi.responses import JSONResponse
        return JSONResponse({"nguon": await asyncio.to_thread(nguon_chrome)})

    @app.post("/trinh-duyet/nhap-chrome")
    async def tb_nhap(request: Request):
        from fastapi.responses import JSONResponse
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        return JSONResponse(await nhap_chrome(str((d or {}).get("nguon") or ""), str((d or {}).get("thu_muc") or ""), str((d or {}).get("ten") or "")))

    @app.post("/trinh-duyet/lam-moi-chrome")
    async def tb_lam_moi(request: Request):
        from fastapi.responses import JSONResponse
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        return JSONResponse(await lam_moi_chrome(str((d or {}).get("id") or "")))

    @app.post("/trinh-duyet/ho-so")
    async def tb_ho_so(request: Request):
        from fastapi.responses import JSONResponse
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        h = str((d or {}).get("hanh") or "tao")
        if h == "tao":
            return JSONResponse(tao_ho_so(str((d or {}).get("ten") or "")))
        if h == "doi_ten":
            return JSONResponse(doi_ten_ho_so(str((d or {}).get("id") or ""), str((d or {}).get("ten") or "")))
        if h == "chon":
            return JSONResponse(chon_ho_so(str((d or {}).get("id") or "")))
        if h == "xoa":
            return JSONResponse(await xoa_ho_so(str((d or {}).get("id") or "")))
        return JSONResponse({"ok": False, "loi": "Hành động không hợp lệ."})

    @app.post("/trinh-duyet/muc")
    async def tb_muc(request: Request):
        from fastapi.responses import JSONResponse
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        try:
            phut = int((d or {}).get("phut") or 0)
        except (TypeError, ValueError):
            phut = 0
        return JSONResponse(dat_muc(str((d or {}).get("muc") or ""), max(0, min(phut, 24 * 60))))

    @app.post("/trinh-duyet/dung")
    async def tb_dung():
        from fastapi.responses import JSONResponse
        with _khoa:
            _tt["dung"] = True
        _ghi_nk({"op": "dung", "ket_qua": "đã dừng", "mo_ta": "Anh bấm Dừng ngay"})
        return JSONResponse({"ok": True})

    @app.post("/trinh-duyet/tiep-tuc")
    async def tb_tiep_tuc():
        from fastapi.responses import JSONResponse
        with _khoa:
            _tt["dung"] = False
        _ghi_nk({"op": "tiep", "ket_qua": "cho làm tiếp", "mo_ta": "Anh cho agent làm tiếp"})
        return JSONResponse({"ok": True})

    @app.post("/trinh-duyet/duyet")
    async def tb_duyet(request: Request):
        from fastapi.responses import JSONResponse
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        return JSONResponse(quyet_dinh(str((d or {}).get("id") or ""), bool((d or {}).get("ok"))))

    @app.get("/trinh-duyet/nhat-ky")
    async def tb_nk(n: int = 60):
        from fastapi.responses import JSONResponse
        return JSONResponse({"nhat_ky": doc_nk(max(1, min(int(n), 300)))})


_nap_muc()
