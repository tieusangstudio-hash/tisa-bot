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
# (V3.43) Mỗi ô chat có tab riêng: AI ở ô chat nào chỉ làm trên tab của ô đó; khung Trình duyệt cạnh ô chat chỉ hiện tab của ô đó.
_CHAT = contextvars.ContextVar("tisa_chat_tab", default=None)      # khung Trình duyệt đặt; None = đọc từ lượt chat (turn_context)
_tab_chat: dict = {}           # mã phiên chat -> {"tab": tab đang làm, "tabs": [các tab của ô chat]}
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
def chat_hien_tai() -> str:
    """Mã phiên của ô chat đang gọi ("" ngoài ô chat: kênh khác, lịch, việc nền: dùng tab chung như cũ)."""
    v = _CHAT.get()
    if v is not None:
        return str(v)
    try:
        import turn_context
        return str((turn_context.current() or {}).get("session_id") or "")
    except Exception:  # noqa: BLE001
        return ""


def _luu_tab_chat() -> None:
    try:
        DIR.mkdir(parents=True, exist_ok=True)
        (DIR / "tab-theo-chat.json").write_text(json.dumps(_tab_chat, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


def _nap_tab_chat() -> None:
    try:
        d = json.loads((DIR / "tab-theo-chat.json").read_text(encoding="utf-8"))
        if isinstance(d, dict):
            _tab_chat.update({str(k): {"tab": str(v.get("tab") or ""), "tabs": [str(x) for x in v.get("tabs") or []][-20:]} for k, v in d.items() if isinstance(v, dict)})
    except (OSError, ValueError):
        pass


def _lay_tab(c=None) -> str:
    c = chat_hien_tai() if c is None else c
    with _khoa:
        return (_tab_chat.get(c) or {}).get("tab", "") if c else (_tt.get("tab") or "")


def _dat_tab(tid: str, c=None) -> None:
    c = chat_hien_tai() if c is None else c
    with _khoa:
        if not c:
            _tt["tab"] = tid
            return
        e = _tab_chat.setdefault(c, {"tab": "", "tabs": []})
        e["tab"] = tid
        if tid and tid not in e["tabs"]:
            e["tabs"] = (e["tabs"] + [tid])[-20:]
        if len(_tab_chat) > 300:          # giữ gọn: bỏ các ô chat cũ nhất
            for k in list(_tab_chat)[:len(_tab_chat) - 300]:
                _tab_chat.pop(k, None)
    _luu_tab_chat()


def hs_cua_chat(c=None) -> str:
    """Trình duyệt riêng của ô chat (gắn khi anh mở khung Trình duyệt ở ô chat đó); rỗng = dùng trình duyệt anh đã chọn như cũ."""
    c = chat_hien_tai() if c is None else c
    if not c:
        return ""
    with _khoa:
        h = (_tab_chat.get(c) or {}).get("hs", "")
    return h if h and any(x["id"] == h for x in _doc_hs()["ds"]) else ""


def chat_vua_dung(c: str, giay: float = 120) -> bool:
    """AI của ô chat này vừa dùng trình duyệt (trong 2 phút)."""
    with _khoa:
        return bool(c) and time.time() - float((_tab_chat.get(c) or {}).get("luc") or 0) < giay


def gan_hs_chat(c: str, hs: str) -> None:
    if not c:
        return
    with _khoa:
        e = _tab_chat.setdefault(c, {"tab": "", "tabs": []})
        if e.get("hs") != hs:
            e["hs"], e["tab"], e["tabs"] = hs, "", []
    _luu_tab_chat()


def ho_so_khung() -> str:
    """(V3.43) Trình duyệt chạy ngầm dành cho khung Trình duyệt cạnh ô chat: không hiện cửa sổ, không lẫn với tab Chrome anh đang mở.
    Anh đăng nhập tài khoản ngay trong khung; đăng nhập được giữ lại trong trình duyệt này."""
    x = next((y for y in _doc_hs()["ds"] if y.get("khung")), None)
    if x:
        return x["id"]
    kq = tao_ho_so("Trình duyệt ô chat", {"khung": True})
    return kq.get("id", "") if kq.get("ok") else ""


def _ua_thuong(exe: str) -> str:
    """Chrome chạy ngầm tự xưng HeadlessChrome nên nhiều trang (Google, Facebook) chặn đăng nhập: xưng như Chrome thường cùng số bản."""
    ban = ""
    try:
        if os.name == "nt":
            goc = Path(exe).parent
            ban = next((p.name for p in goc.iterdir() if p.is_dir() and re.match(r"^\d+\.\d+\.\d+\.\d+$", p.name)), "")
        else:
            r = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=8)
            m = re.search(r"(\d+)\.\d+\.\d+\.\d+", r.stdout or "")
            ban = m.group(0) if m else ""
    except Exception:  # noqa: BLE001
        pass
    chinh = (ban.split(".")[0] if ban else "") or "142"
    he = "Windows NT 10.0; Win64; x64" if os.name == "nt" else "Macintosh; Intel Mac OS X 10_15_7"
    return "Mozilla/5.0 (%s) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s.0.0.0 Safari/537.36" % (he, chinh)


def chu_cua_tab(tid: str) -> str:
    with _khoa:
        return next((k for k, v in _tab_chat.items() if tid in (v.get("tabs") or [])), "")


def tab_cua_chat(ds: list, c=None) -> list:
    """Trong ô chat: chỉ các tab của ô chat đó (còn mở). Ngoài ô chat: mọi tab."""
    c = chat_hien_tai() if c is None else c
    if not c:
        return ds
    with _khoa:
        cua = set((_tab_chat.get(c) or {}).get("tabs") or [])
    return [t for t in ds if t["id"] in cua]


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


CONG_NGOAI = 1        # (V3.02) trình duyệt "ngoài" = Chrome anh đang mở TISA BOT: không có cổng riêng, đi qua tisa_browser_ngoai


def _ngoai(hs: str = "") -> str:
    """Mã loại trình duyệt (chrome, edge, brave) nếu đây là trình duyệt anh đang dùng; rỗng nếu là trình duyệt riêng của TISA."""
    h = hs or _hs()
    x = next((y for y in _doc_hs()["ds"] if y["id"] == h), None)
    return str(x.get("trinh") or "chrome") if (x and x.get("loai") == "ngoai") else ""


def _kn(hs: str = ""):
    import tisa_browser_ngoai as N
    return N.ket_noi(_ngoai(hs) or "chrome")


def tao_ho_so_ngoai(trinh: str) -> dict:
    """Thêm (hoặc lấy lại) mục "Chrome đang mở TISA BOT". Không tạo hồ sơ, không mở tiến trình nào."""
    import tisa_browser_ngoai as N
    trinh = trinh if trinh in N.TEN else "chrome"
    d = _doc_hs()
    x = next((y for y in d["ds"] if y.get("loai") == "ngoai" and y.get("trinh") == trinh), None)
    if x:
        return {"ok": True, "id": x["id"], "ten": x["ten"]}
    if len(d["ds"]) >= 10:
        return {"ok": False, "loi": "Tối đa 10 trình duyệt."}
    ma = "ngoai-" + trinh
    ten = "%s của anh" % {"chrome": "Chrome", "edge": "Edge", "brave": "Brave"}.get(trinh, "Chrome")
    d["ds"].append({"id": ma, "ten": ten[:40], "cong": CONG_NGOAI, "loai": "ngoai", "trinh": trinh})
    _luu_hs(d)
    _ghi_nk({"op": "ho_so", "ket_qua": "đã thêm", "mo_ta": "Dùng %s của anh" % N.TEN.get(trinh, trinh)})
    return {"ok": True, "id": ma, "ten": ten[:40]}


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
        for v in _tab_chat.values():
            v["tab"] = ""
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
    if x.get("loai") != "ngoai":       # trình duyệt của anh: chỉ bỏ khỏi danh sách, không đụng dữ liệu Chrome
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
        # Local State gốc liệt kê cả chục hồ sơ và có thể bật "hỏi chọn hồ sơ khi mở": Chrome sẽ mở màn hình chọn hồ sơ thay vì cửa sổ làm việc.
        # Chỉ giữ khóa giải mã cookie (os_crypt) và một hồ sơ Default, tắt màn hình chọn hồ sơ.
        ls = json.loads((goc / "Local State").read_text(encoding="utf-8"))
        toi_thieu = {"os_crypt": ls.get("os_crypt") or {}, "profile": {"last_used": "Default", "last_active_profiles": ["Default"], "picker_availability_on_startup": 1,
                                                                         "info_cache": {"Default": {"name": "TISA"}}}, "browser": {"enabled_labs_experiments": []}}
        (dich / "Local State").write_text(json.dumps(toi_thieu), encoding="utf-8")
    except (OSError, ValueError):
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
    if not x or not x.get("nhap_tu") or x.get("loai") == "ngoai":
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
        if muc == "toan_quyen":
            _tt["dung"] = False   # (V3.07) anh cấp Toàn quyền là muốn AI làm: cờ "Đã dừng" của lần bấm Dừng trước không được giữ lại và chặn mọi lệnh
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


# ---------------------------------------------------------------- hỏi anh chọn web để mở (hộp chọn hiện trong TISA BOT)
_chon: dict = {}
HIEU_LUC_CHON = 15 * 60


def _url_hop_le(u: str) -> str:
    u = str(u or "").strip()
    if not re.match(r"^https?://[^\s/@]+(?:[/?#]\S*)?$", u, re.I) or len(u) > 500:
        return ""
    return u


def _chuan_trang(raw) -> list:
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except ValueError:
            raw = [{"url": x} for x in re.findall(r"https?://\S+", raw)]
    out = []
    for x in (raw if isinstance(raw, list) else []):
        if isinstance(x, str):
            x = {"url": x}
        if not isinstance(x, dict):
            continue
        u = _url_hop_le(x.get("url"))
        if not u:
            continue
        host = urllib.parse.urlparse(u).netloc
        out.append({"ten": str(x.get("ten") or host)[:80], "url": u, "host": host, "mo_ta": str(x.get("mo_ta") or "")[:160]})
    return out[:6]


def xin_chon_web(ly_do: str, ds: list) -> str:
    with _khoa:
        for k in [k for k, v in _chon.items() if time.time() - v["luc"] > HIEU_LUC_CHON]:
            _chon.pop(k, None)
        k = uuid.uuid4().hex[:8]
        _chon[k] = {"luc": time.time(), "ly_do": str(ly_do or "")[:200], "trang": ds, "trang_thai": "cho", "url": "", "hoso": ""}
    _ghi_nk({"op": "hoi_mo", "ket_qua": "đang chờ anh chọn", "mo_ta": "%s (%s)" % (str(ly_do or "")[:80], ", ".join(x["host"] for x in ds))})
    return k


def tra_loi_chon(cid: str, url: str = "", hoso: str = "", huy: bool = False) -> dict:
    with _khoa:
        v = _chon.get(str(cid or ""))
        if not v or v["trang_thai"] != "cho":
            return {"ok": False, "loi": "Không còn hộp chọn này."}
        if huy:
            v["trang_thai"] = "huy"
        else:
            u = _url_hop_le(url)
            if not u:
                return {"ok": False, "loi": "Địa chỉ web không hợp lệ (cần bắt đầu bằng http:// hoặc https://)."}
            x = tim_ho_so(str(hoso)) if hoso else None
            v["url"], v["hoso"], v["trang_thai"] = u, (x["id"] if x else hs_dang_dung()), "da_chon"
        v["luc"] = time.time()
    _ghi_nk({"op": "hoi_mo", "ket_qua": "anh không mở" if huy else "anh đã chọn", "mo_ta": "" if huy else urllib.parse.urlparse(v["url"]).netloc})
    return {"ok": True}


def _host_goc(url: str) -> str:
    """Tên miền để so khớp tab: bỏ www. và cổng."""
    h = urllib.parse.urlparse(str(url or "")).netloc.lower().split("@")[-1].split(":")[0]
    return h[4:] if h.startswith("www.") else h


def _mien_chinh(host: str) -> str:
    p = [x for x in str(host or "").split(".") if x]
    if len(p) >= 3 and p[-2] in ("com", "net", "org", "edu", "gov", "co"):
        return ".".join(p[-3:])
    return ".".join(p[-2:])


def _tab_khop(ds_tab: list, url: str):
    """Tab ĐÃ MỞ SẴN đúng trang (cùng tên miền, bỏ www.) trong trình duyệt đang chạy: vào đúng tab đã đăng nhập, khỏi mở mới. None nếu không có."""
    h = _host_goc(url)
    if not h:
        return None
    for t in ds_tab or []:
        u = str(t.get("url") or "")
        if u.startswith(("http://", "https://")) and _host_goc(u) == h:
            return t
    return None


async def _bat_tieu_diem(p) -> None:
    """Cho trang tin là nó đang được xem và đang có tiêu điểm, KỂ CẢ khi anh đã mở tab khác lên hoặc cửa sổ khác che mất (V3.20, chủ yêu cầu 18/11/2026:
    anh làm việc ở tab khác, TISA BOT vẫn thao tác tab của nó). Không đổi tab anh đang xem; chỉ có hiệu lực trong kết nối này."""
    try:
        await p.gui("Emulation.setFocusEmulationEnabled", {"enabled": True}, timeout=3)
    except Exception:  # noqa: BLE001
        pass


async def _chuyen_tab(t: dict) -> None:
    # V3.20: chỉ đổi tab LÀM VIỆC của AI, KHÔNG lật tab anh đang xem (trước đây gọi Target.activateTarget, giành màn hình của anh).
    _dat_tab(t["id"])


async def _ghi_chu_trang(ds: list) -> list:
    """Gắn vào từng trang xin mở: đã có tab mở sẵn chưa, đã đăng nhập chưa (trong trình duyệt đang dùng). Chỉ đọc, không mở gì."""
    if not _cong_mo():
        return ds
    try:
        ds_tab = await asyncio.to_thread(_trang_dang_co)
    except Exception:  # noqa: BLE001
        ds_tab = []
    try:
        ck = await _doc_cookie(False) if ds_tab else []
    except Exception:  # noqa: BLE001
        ck = []
    mien_ck = {_mien_chinh(str(c.get("domain", "")).lstrip(".").lower()) for c in ck if c.get("name")}
    for x in ds:
        x["tab_san"] = bool(_tab_khop(ds_tab, x["url"]))
        x["da_dang_nhap"] = _mien_chinh(_host_goc(x["url"])) in mien_ck
        x["ten_hs"] = _ten_hs()
    return ds


async def _hoi_mo(a: dict) -> str:
    ds = _chuan_trang(a.get("trang"))
    if not ds and a.get("url"):
        ds = _chuan_trang([{"url": a.get("url"), "ten": a.get("ten") or ""}])
    if not ds:
        return "LOI: hoi_mo cần trang=[{\"ten\":\"Meta for Developers\",\"url\":\"https://developers.facebook.com/apps\",\"mo_ta\":\"tạo ứng dụng\"}, ...] (1 đến 6 địa chỉ https đầy đủ)."
    # (V3.02) Trình duyệt TISA đang chạy mà đã có tab của đúng trang cần: chuyển thẳng sang tab đó (tài khoản đã đăng nhập sẵn), không hỏi, không mở mới.
    if _cong_mo():
        try:
            ds_tab = await asyncio.to_thread(_trang_dang_co)
            for x in ds:
                t = _tab_khop(ds_tab, x["url"])
                if t:
                    await _chuyen_tab(t)
                    _ghi_nk({"op": "hoi_mo", "ket_qua": "chuyển sang tab đã mở sẵn", "mo_ta": x["host"], "host": x["host"]})
                    return ("Trình duyệt \"%s\" đang mở sẵn tab \"%s\" (%s): em đã chuyển sang đúng tab đó, tài khoản đã đăng nhập sẵn nên không mở mới và không cần đăng nhập lại.\n"
                            % (_ten_hs(), str(t.get("title") or x["ten"])[:60], str(t.get("url") or "")[:100])) + await nhin()
        except Exception:  # noqa: BLE001
            pass
    ds = await _ghi_chu_trang(ds)
    cid = xin_chon_web(str(a.get("ly_do") or ""), ds)
    han = max(30, min(int(a.get("giay") or 600), 900))
    t0 = time.time()
    while time.time() - t0 < han:
        with _khoa:
            v = _chon.get(cid) or {}
            dung = _tt["dung"]
        if dung:
            with _khoa:
                _chon.pop(cid, None)
            return "DA_DUNG: Anh đã bấm Dừng ngay. Không mở web."
        if v.get("trang_thai") == "da_chon":
            x = next((h for h in ds_ho_so() if h["id"] == v["hoso"]), None)
            chon_ho_so(v["hoso"])
            ten_web = next((t["ten"] for t in ds if t["url"] == v["url"]), urllib.parse.urlparse(v["url"]).netloc)
            dau = "Anh chọn mở \"%s\" (%s) bằng trình duyệt \"%s\". Từ giờ chỉ dùng trình duyệt này.\n" % (ten_web, v["url"], (x or {}).get("ten", "đã chọn"))
            if _cong_mo():
                # Trình duyệt đang chạy: vào tab đã có (đã đăng nhập) hoặc mở TAB MỚI, không đè lên tab anh đang dùng dở.
                ds_tab = await asyncio.to_thread(_trang_dang_co)
                t = _tab_khop(ds_tab, v["url"])
                if t:
                    await _chuyen_tab(t)
                    _ghi_nk({"op": "hoi_mo", "ket_qua": "chuyển sang tab đã mở sẵn", "mo_ta": urllib.parse.urlparse(v["url"]).netloc})
                    return dau + "Trình duyệt đã có sẵn tab của trang này, em chuyển sang đúng tab đó (đang ở: %s).\n" % str(t.get("url") or "")[:100] + await nhin()
                await _tab_moi(v["url"])
                await asyncio.sleep(1.5)
                _ghi_nk({"op": "open", "ket_qua": "ok (tab mới)", "mo_ta": v["url"][:140], "host": urllib.parse.urlparse(v["url"]).netloc})
                return dau + "Đã mở trong tab mới (các tab đang đăng nhập khác giữ nguyên).\n" + await nhin()
            return dau + await thuc_hien("open", {"url": v["url"], "trinh_duyet": v["hoso"]})
        if v.get("trang_thai") == "huy":
            return "TU_CHOI: Anh không chọn trang nào để mở. Hỏi anh muốn làm gì tiếp, đừng tự mở web."
        await asyncio.sleep(1.0)
    with _khoa:
        _chon.pop(cid, None)
    return "HET_GIO: Anh chưa chọn web nào sau %d giây. Nói với anh, hỏi lại khi anh quay lại." % han


# ---------------------------------------------------------------- dán mã thẳng vào cửa sổ TISA BOT (không qua mô hình)
# AI (điều khiển máy tính) bấm chọn một ô trong cửa sổ TISA BOT, rồi gọi op=dan_vao_tisa: giá trị đọc từ trang nền tảng, giữ trong RAM tối đa 20 giây,
# giao diện TISA BOT (cửa sổ có ô đang được chọn) lấy một lần, điền vào ô và che bằng chấm tròn. Mô hình chỉ nhận lại số ký tự và tên ô.
_dan_cho: dict = {}
HIEU_LUC_DAN = 20


def _don_dan() -> None:
    d = _dan_cho
    if d and time.time() - d.get("luc", 0) > HIEU_LUC_DAN and d.get("ket_qua") is None:
        d["ket_qua"] = {"ok": False, "loi": "Hết thời gian, không có cửa sổ TISA BOT nào có ô đang được chọn."}
        d["gia_tri"] = ""


def dan_dang_cho() -> str:
    with _khoa:
        _don_dan()
        return str(_dan_cho.get("id") or "") if _dan_cho and _dan_cho.get("ket_qua") is None and _dan_cho.get("gia_tri") else ""


def dan_lay(did: str) -> dict:
    """Giao diện lấy giá trị MỘT LẦN (chỉ cửa sổ đang có ô được chọn mới gọi)."""
    with _khoa:
        _don_dan()
        if not _dan_cho or _dan_cho.get("id") != did or _dan_cho.get("ket_qua") is not None or not _dan_cho.get("gia_tri"):
            return {"co": False}
        v = _dan_cho["gia_tri"]
        _dan_cho["gia_tri"] = ""          # dùng một lần
        return {"co": True, "gia_tri": v}


def dan_xong(did: str, ok: bool, nhan: str = "", so: int = 0, loi: str = "") -> dict:
    with _khoa:
        if not _dan_cho or _dan_cho.get("id") != did or _dan_cho.get("ket_qua") is not None:
            return {"ok": False}
        _dan_cho["ket_qua"] = {"ok": bool(ok), "nhan": str(nhan or "")[:80], "so": int(so or 0), "loi": str(loi or "")[:200]}
        return {"ok": True}


_SS = {"Strict": "Strict", "Lax": "Lax", "None": "None", "no_restriction": "None", "lax": "Lax", "strict": "Strict"}
_COOKIE_PHIEN_GOOGLE = {"sid", "ssid", "hsid", "sapisid", "apisid", "__secure-1psid", "__secure-3psid", "__secure-1papisid", "__secure-3papisid"}


async def _doc_cookie(tao_tab: bool = True) -> list:
    """Mọi cookie của trình duyệt đang chọn. Chrome có cửa sổ mà KHÔNG còn tab nào thì Storage.getCookies báo "Browser context management is not supported":
    khi đó mở tạm một tab trống để đọc rồi đóng lại."""
    tao = False
    if not await asyncio.to_thread(_trang_dang_co):
        if not tao_tab:
            return []              # chỉ liệt kê cho bảng điều khiển: không mở cửa sổ chỉ để đếm cookie
        await _tab_moi("about:blank")
        tao = True
        await asyncio.sleep(0.8)
    try:
        async with _Phien(await _ws_url_trinh_duyet()) as b:
            r = await b.gui("Storage.getCookies", timeout=20)
        return r.get("cookies", [])
    finally:
        if tao:
            try:
                async with _Phien(await _ws_url_trinh_duyet()) as b:
                    for t in await asyncio.to_thread(_trang_dang_co):
                        if str(t.get("url", "")).startswith("about:blank"):
                            await b.gui("Target.closeTarget", {"targetId": t["id"]}, timeout=8)
            except Exception:  # noqa: BLE001
                pass


async def _phien_playwright(mien: list) -> tuple:
    """Phiên đăng nhập của trình duyệt đã chọn, dạng storage_state của Playwright (cookies + origins). Trả (json, số cookie, đã đăng nhập Google?)."""
    cs, thay = [], False
    for c in await _doc_cookie():
        d = str(c.get("domain", "")).lstrip(".").lower()
        if not any(d == m or d.endswith("." + m) for m in mien):
            continue
        if str(c.get("name", "")).lower() in _COOKIE_PHIEN_GOOGLE:
            thay = True
        het = -1 if c.get("session") else float(c.get("expires", -1) or -1)
        cs.append({"name": c.get("name", ""), "value": c.get("value", ""), "domain": c.get("domain", ""), "path": c.get("path", "/"),
                   "expires": het, "httpOnly": bool(c.get("httpOnly")), "secure": bool(c.get("secure")), "sameSite": _SS.get(str(c.get("sameSite") or ""), "Lax")})
    return json.dumps({"cookies": cs, "origins": []}, ensure_ascii=False), len(cs), thay


async def _dan_phien(a: dict) -> str:
    """op=dan_vao_tisa kieu=phien_trinh_duyet: lấy PHIÊN ĐĂNG NHẬP của trình duyệt anh đã chọn (không mở trình duyệt nào khác) rồi chuyển vào ô đang chọn
    của TISA BOT, mô hình không nhìn thấy. Tương đương đưa chìa khóa tài khoản nên cần anh duyệt; riêng khi anh ĐÃ CẤP Toàn quyền thì tự duyệt (anh đã giao toàn quyền và chính anh nhờ nối)."""
    mien = [m.strip().lower().lstrip(".") for m in re.split(r"[,\s]+", str(a.get("mien") or "google.com,youtube.com")) if m.strip()][:6]
    if not mien or any(not re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", m) for m in mien):
        return "LOI: mien không hợp lệ (ví dụ mien=google.com)."
    nc = {"host": ",".join(mien), "ten": "Lấy phiên đăng nhập %s của %s đưa vào TISA BOT" % (mien[0], _ten_hs()), "tieu_de": "Phiên đăng nhập"}
    duyet_id = str(a.get("duyet_id") or "")
    if muc_hien_tai() == "toan_quyen":
        _ghi_nk({"op": "xuat_phien", "ket_qua": "tự duyệt (toàn quyền)", "mo_ta": nc["ten"], "host": nc["host"]})
    elif not dung_duyet(duyet_id, "xuat_phien", nc):
        k = xin_duyet("xuat_phien", nc, "Lấy phiên đăng nhập (cookie) %s từ trình duyệt \"%s\" đưa vào TISA BOT" % (", ".join(mien), _ten_hs()))
        _ghi_nk({"op": "xuat_phien", "ket_qua": "chờ duyệt", "mo_ta": nc["ten"], "host": nc["host"]})
        # Chờ anh bấm Duyệt ngay trong lệnh này (tối đa 5 phút) để AI tự làm tiếp, không đứng yên chờ anh nhắn lại.
        t0 = time.time()
        quyet = ""
        while time.time() - t0 < 300:
            with _khoa:
                quyet = (_duyet.get(k) or {}).get("trang_thai", "")
                dung = _tt["dung"]
            if dung:
                return "DA_DUNG: Anh đã bấm Dừng ngay."
            if quyet in ("dong_y", "tu_choi"):
                break
            await asyncio.sleep(1.0)
        if quyet == "tu_choi":
            return "TU_CHOI: Anh không duyệt lấy phiên đăng nhập. Hỏi anh muốn làm gì tiếp."
        if not (quyet == "dong_y" and dung_duyet(k, "xuat_phien", nc)):
            return ("CAN_DUYET: Anh chưa bấm Duyệt sau 5 phút. Đây là phiên đăng nhập của anh (tương đương đưa chìa khóa tài khoản %s cho TISA BOT). Nói rõ với anh: lấy từ trình duyệt \"%s\", "
                    "chỉ chuyển vào ô của TISA BOT, em không nhìn thấy. Khi anh bấm Duyệt thì gọi lại đúng lệnh này với duyet_id=\"%s\"." % (mien[0], _ten_hs(), k))
    gia_tri, so, dang_nhap = await _phien_playwright(mien)
    if not so or (mien[0].endswith("google.com") and not dang_nhap):
        return ("CHUA_DANG_NHAP: Trình duyệt \"%s\" chưa đăng nhập %s (không thấy cookie phiên). Mở trang %s trong trình duyệt này, nói anh đăng nhập (wait_user), rồi gọi lại. "
                "KHÔNG mở trình duyệt khác, KHÔNG chạy lệnh login của công cụ." % (_ten_hs(), mien[0], mien[0]))
    return await _cho_dan_va_cho(gia_tri, "phiên đăng nhập %s" % mien[0], "%d cookie" % so)


async def _dan_vao_tisa(a: dict) -> str:
    if str(a.get("kieu") or "") == "phien_trinh_duyet":
        return await _dan_phien(a)
    try:
        tu_id = int(a.get("tu_id") or 0)
    except (TypeError, ValueError):
        tu_id = 0
    tu_tab = str(a.get("tu_tab") or "")
    if not tu_tab or tu_id <= 0:
        return "LOI: dan_vao_tisa cần tu_tab (mã tab nguồn, xem op=tabs) và tu_id (số [n] của khối chứa mã, từ look)."
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
    host = urllib.parse.urlparse(nguon.get("url", "")).netloc
    if la_trang_cua_toi(host):
        return "LOI: tab nguồn là trang TISA BOT. Tab nguồn phải là trang nền tảng hiện mã."
    async with _Phien(nguon["webSocketDebuggerUrl"]) as ps:
        gia_tri = await ps.js("""(() => { const e = (window.__tisa && window.__tisa.marks || [])[%d - 1]; if (!e) return null;
          const v = (e.value !== undefined && String(e.value) !== '') ? e.value : (e.innerText || e.textContent || ''); return String(v).trim(); })()""" % tu_id)
    if not gia_tri:
        return "LOI: không đọc được giá trị ở [%d] của tab nguồn (số có thể đã cũ: look lại tab nguồn)." % tu_id
    if len(gia_tri) > 6000:
        return "LOI: giá trị dài bất thường (%d ký tự), không dán." % len(gia_tri)
    return await _cho_dan_va_cho(gia_tri, "mã", "", host)


async def _cho_dan_va_cho(gia_tri: str, mo_ta: str, them: str = "", host: str = "") -> str:
    did = uuid.uuid4().hex[:8]
    with _khoa:
        _dan_cho.clear()
        _dan_cho.update({"id": did, "gia_tri": gia_tri, "luc": time.time(), "ket_qua": None})
    gia_tri = ""
    t0 = time.time()
    while time.time() - t0 < HIEU_LUC_DAN + 2:
        with _khoa:
            kq = _dan_cho.get("ket_qua") if _dan_cho.get("id") == did else {"ok": False, "loi": "đã bị thay"}
        if kq is not None:
            with _khoa:
                _dan_cho.clear()
            if kq.get("ok"):
                _ghi_nk({"op": "dan_vao_tisa", "ket_qua": "ok", "mo_ta": "Dán %s (%d ký tự, ẩn) vào ô \"%s\" của TISA BOT" % (mo_ta, kq.get("so", 0), kq.get("nhan", "")), "host": host})
                return ("Đã dán %s (%d ký tự%s; giá trị được giấu, em không nhìn thấy) vào ô \"%s\" trong cửa sổ TISA BOT; ô hiện chấm tròn. "
                        "KHÔNG chụp rồi đọc lại ô đó. Bấm Lưu hoặc Kết nối ở TISA BOT để hoàn tất." % (mo_ta, kq.get("so", 0), (", " + them) if them else "", kq.get("nhan") or "ô đang chọn"))
            return ("KHONG_DAN_DUOC: %s Cách xử lý: dùng điều khiển máy tính đưa cửa sổ TISA BOT lên trước (focus_app), CLICK vào đúng ô cần dán để ô nhận con trỏ, rồi gọi lại dan_vao_tisa ngay."
                    % (kq.get("loi") or "cửa sổ TISA BOT không nhận."))
        await asyncio.sleep(0.5)
    with _khoa:
        _dan_cho.clear()
    return "KHONG_DAN_DUOC: Hết thời gian chờ cửa sổ TISA BOT. Click vào ô cần dán trong cửa sổ TISA BOT rồi gọi lại."


# ---------------------------------------------------------------- điều khiển giao diện TISA BOT bằng lệnh (không cần chuột, không bị cửa sổ khác đè)
# AI gọi op=ui_tisa lenh=mo_the|chon_o|bam|xem; cửa sổ TISA BOT đang mở (giao diện) nhận lệnh qua nhịp hỏi trạng thái, thực hiện rồi báo kết quả.
# Kết quả chỉ gồm chữ nhãn (tên hộp, ô, nút, thông báo), KHÔNG BAO GIỜ gồm giá trị trong các ô nhập.
_ui_cho: dict = {}
HIEU_LUC_UI = 25
LENH_UI = ("mo_the", "chon_o", "bam", "xem")


def ui_dang_cho() -> dict:
    with _khoa:
        v = _ui_cho
        if v and v.get("ket_qua") is None and not v.get("da_lay") and time.time() - v["luc"] < HIEU_LUC_UI:
            return {"id": v["id"], "lenh": v["lenh"], "args": v["args"]}
    return {}


def ui_lay(uid: str) -> dict:
    with _khoa:
        v = _ui_cho
        if not v or v.get("id") != uid or v.get("da_lay") or v.get("ket_qua") is not None or time.time() - v["luc"] >= HIEU_LUC_UI:
            return {"co": False}
        v["da_lay"] = True
        return {"co": True, "lenh": v["lenh"], "args": v["args"]}


def ui_xong(uid: str, ok: bool, ket_qua: str = "") -> dict:
    with _khoa:
        if not _ui_cho or _ui_cho.get("id") != uid or _ui_cho.get("ket_qua") is not None:
            return {"ok": False}
        _ui_cho["ket_qua"] = {"ok": bool(ok), "kq": str(ket_qua or "")[:1800]}
        return {"ok": True}


async def _ui_tisa(a: dict) -> str:
    lenh = str(a.get("lenh") or "").strip().lower()
    if lenh not in LENH_UI:
        return "LOI: ui_tisa cần lenh=" + "|".join(LENH_UI) + " (mo_the ten=<tên thẻ kết nối> [dich_vu] [truong]; chon_o truong=<nhãn ô>; bam nhan=<chữ trên nút>; xem)."
    args = {k: str(a.get(k) or "")[:120] for k in ("ten", "truong", "nhan", "dich_vu")}
    if lenh == "mo_the" and not args["ten"]:
        return "LOI: mo_the cần ten=<tên thẻ, ví dụ NotebookLM, Composio, Meta>."
    if lenh == "bam" and not args["nhan"]:
        return "LOI: bam cần nhan=<chữ trên nút>."
    uid = uuid.uuid4().hex[:8]
    with _khoa:
        _ui_cho.clear()
        _ui_cho.update({"id": uid, "lenh": lenh, "args": args, "luc": time.time(), "da_lay": False, "ket_qua": None})
    t0 = time.time()
    while time.time() - t0 < HIEU_LUC_UI:
        with _khoa:
            kq = _ui_cho.get("ket_qua") if _ui_cho.get("id") == uid else {"ok": False, "kq": "đã bị thay"}
        if kq is not None:
            with _khoa:
                _ui_cho.clear()
            _ghi_nk({"op": "ui_tisa", "ket_qua": "ok" if kq["ok"] else "lỗi", "mo_ta": "%s %s" % (lenh, args.get("ten") or args.get("nhan") or args.get("truong") or "")})
            return ("" if kq["ok"] else "LOI_UI: ") + kq["kq"]
        await asyncio.sleep(0.4)
    with _khoa:
        _ui_cho.clear()
    return "KHONG_CO_CUA_SO: Không có cửa sổ TISA BOT nào nhận lệnh trong %d giây (TISA BOT chưa mở trên màn hình, hoặc đang treo). Nhờ anh mở TISA BOT rồi gọi lại." % HIEU_LUC_UI


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
    if int(cong) == CONG_NGOAI:
        import tisa_browser_ngoai as N
        return any(k.song for k in N._KN.values())
    if not int(cong) and _ngoai():
        return _kn().song
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
    if x.get("loai") == "ngoai":
        import tisa_browser_ngoai as N
        k = _kn(hoso)
        if not await k.noi():
            return {"ok": False, "loi": N.loi_de_hieu(k)}
        if url:
            await _tab_moi(url)
        await len_truoc()
        return {"ok": True, "da_mo": True}
    if _cong_mo():
        if url:
            await _tab_moi(url)
        elif not await asyncio.to_thread(_trang_dang_co):
            await _tab_moi("about:blank")       # chạy nền mà không còn cửa sổ nào (anh bấm đóng cửa sổ): mở lại cửa sổ
        await len_truoc()
        if not url:
            await _trang_chu(hoso)       # cửa sổ còn trống thì vẽ trang chủ để biết đây là trình duyệt nào, đã đăng nhập gì
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
    if HEADLESS or x.get("khung"):
        args.append("--headless=new")
        if x.get("khung"):
            args.append("--user-agent=%s" % _ua_thuong(exe))
    args.append(url or "about:blank")
    try:
        subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, start_new_session=True)
    except OSError as e:
        return {"ok": False, "loi": "Không mở được trình duyệt: %s" % e}
    for _ in range(50):
        await asyncio.sleep(0.3)
        if _cong_mo():
            _ghi_nk({"op": "mo", "ket_qua": "đã mở", "mo_ta": "Mở %s" % _ten_hs(hoso)})
            await len_truoc()
            if not url:
                await _trang_chu(hoso)
            return {"ok": True, "da_mo": False}
    return {"ok": False, "loi": "Trình duyệt chưa sẵn sàng. Máy có màn hình không? Thử bấm Mở trình duyệt lại."}


_TRANG_NHANH = [("Facebook", "https://www.facebook.com/"), ("Meta Business Suite", "https://business.facebook.com/"), ("Quảng cáo Facebook", "https://adsmanager.facebook.com/"),
                ("Google", "https://www.google.com/"), ("YouTube", "https://studio.youtube.com/"), ("TikTok", "https://www.tiktok.com/"), ("Zalo OA", "https://oa.zalo.me/"), ("Canva", "https://www.canva.com/")]


async def _trang_chu(hs: str = "") -> None:
    """Trình duyệt mới mở chỉ có trang trắng nên trông như đứng yên. Vẽ trang chủ riêng: tên trình duyệt, các trang đã đăng nhập, lối vào nhanh."""
    import html as _h
    if _ngoai(hs):
        return
    try:
        await asyncio.sleep(1.2)
        ds = await asyncio.to_thread(_trang_dang_co, hs)
        if not ds or ds[0].get("url") not in ("about:blank", "chrome://new-tab-page/", "chrome://newtab/"):
            return
        dn = await trang_da_dang_nhap(hs)
        ten = _h.escape(_ten_hs(hs))
        co = [x for x in dn if x.get("phien")][:30]
        chips = "".join('<a href="https://%s/">%s</a>' % (_h.escape(x["mien"]), _h.escape(x["mien"])) for x in co) or "<p class='m'>Chưa thấy trang nào đã đăng nhập. Mở trang bên dưới và đăng nhập.</p>"
        nhanh = "".join('<a class="n" href="%s">%s</a>' % (u, _h.escape(t)) for t, u in _TRANG_NHANH)
        trang = ("<!doctype html><meta charset=utf-8><title>TISA · %s</title><style>body{font:16px system-ui,sans-serif;margin:0;padding:44px 6vw;background:#f4f6fc;color:#1b2350}"
                 "@media(prefers-color-scheme:dark){body{background:#101636;color:#e6eaff}a{background:#1c2552!important;color:#e6eaff!important}}h1{margin:0 0 6px;font-size:30px}.m{color:#6b7599}"
                 "div{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0 28px}a{padding:10px 16px;border-radius:999px;background:#fff;color:#1b2350;text-decoration:none;font-weight:600;border:1px solid #d6dcf0}"
                 "a.n{background:#ff6b35;border-color:#ff6b35;color:#fff!important}h2{font-size:14px;letter-spacing:.06em;text-transform:uppercase;color:#6b7599;margin:26px 0 0}</style>"
                 "<h1>Trình duyệt: %s</h1><p class='m'>Cửa sổ này do TISA BOT điều khiển. Anh đăng nhập tại đây, AI dùng lại phiên đăng nhập.</p>"
                 "<h2>Đã đăng nhập</h2><div>%s</div><h2>Mở nhanh</h2><div>%s</div>") % (ten, ten, chips, nhanh)
        url = "data:text/html;charset=utf-8;base64," + base64.b64encode(trang.encode("utf-8")).decode()
        async with _Phien(ds[0]["webSocketDebuggerUrl"]) as p:
            await p.gui("Page.navigate", {"url": url}, timeout=10)
    except Exception:  # noqa: BLE001 - trang chủ chỉ để dễ nhìn, lỗi thì bỏ qua
        pass


def _pid_cong(cong: int) -> int:
    """Mã tiến trình của đúng cửa sổ trình duyệt đang giữ cổng điều khiển này (máy có thể đang mở thêm Chrome cá nhân)."""
    try:
        if os.name == "nt":
            r = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'remote-debugging-port=%d ' -and $_.CommandLine -notmatch '--type=' } | Select-Object -First 1).ProcessId" % cong],
                               capture_output=True, text=True, timeout=8)
        else:
            r = subprocess.run(["pgrep", "-f", "remote-debugging-port=%d " % cong], capture_output=True, text=True, timeout=5)
        for x in (r.stdout or "").split():
            if x.strip().isdigit():
                return int(x.strip())
    except Exception:  # noqa: BLE001
        pass
    return 0


def _kich_hoat(pid: int) -> None:
    """Đưa cửa sổ của tiến trình này lên trước. Không dùng tên ứng dụng vì có thể kích hoạt nhầm Chrome cá nhân của anh."""
    try:
        if sys.platform == "darwin":
            import ctypes.util
            objc = ctypes.cdll.LoadLibrary(ctypes.util.find_library("objc"))
            ctypes.cdll.LoadLibrary("/System/Library/Frameworks/AppKit.framework/AppKit")
            objc.objc_getClass.restype = ctypes.c_void_p
            objc.objc_getClass.argtypes = [ctypes.c_char_p]
            objc.sel_registerName.restype = ctypes.c_void_p
            objc.sel_registerName.argtypes = [ctypes.c_char_p]
            msg = objc.objc_msgSend
            msg.restype, msg.argtypes = ctypes.c_void_p, [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]
            app = msg(objc.objc_getClass(b"NSRunningApplication"), objc.sel_registerName(b"runningApplicationWithProcessIdentifier:"), pid)
            if app:
                msg.restype, msg.argtypes = ctypes.c_bool, [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
                msg(app, objc.sel_registerName(b"activateWithOptions:"), 3)      # bỏ qua ứng dụng khác | mọi cửa sổ
        elif os.name == "nt":
            subprocess.run(["powershell", "-NoProfile", "-Command", "(New-Object -ComObject WScript.Shell).AppActivate(%d)" % pid], capture_output=True, timeout=8)
    except Exception:  # noqa: BLE001
        pass


async def len_truoc() -> None:
    """Đưa cửa sổ trình duyệt TISA lên trước (chỉ có MỘT trình duyệt dùng chung, anh đăng nhập mọi tài khoản vào đây)."""
    try:
        ds = await asyncio.to_thread(_trang_dang_co)
        if _ngoai():
            tab = _lay_tab()
            ds = [t for t in ds if t["id"] == tab]       # Chrome của anh: chỉ đưa lên tab AI đang dùng, không lật tab khác
        if ds:
            async with _Phien(ds[0]["webSocketDebuggerUrl"]) as p:
                await p.gui("Page.bringToFront", timeout=5)
    except Exception:  # noqa: BLE001
        pass
    if not HEADLESS and not _ngoai():
        pid = await asyncio.to_thread(_pid_cong, _cong())
        if pid:
            await asyncio.to_thread(_kich_hoat, pid)


def _trang_dang_co(hs: str = "") -> list:
    if _ngoai(hs):
        return _kn(hs).ds_trang()
    try:
        return [t for t in _http_json("/json/list", cong=_cong(hs)) if t.get("type") == "page" and not str(t.get("url", "")).startswith(("devtools://", "chrome-extension://"))]
    except Exception:  # noqa: BLE001
        return []


async def _ws_url_trinh_duyet() -> str:
    if _ngoai():
        return "ngoai:%s:" % _ngoai()
    return (await asyncio.to_thread(_http_json, "/json/version")).get("webSocketDebuggerUrl", "")


class _Phien:
    """Một kết nối DevTools tới MỘT trang (hoặc tới trình duyệt khi ws là cấp trình duyệt)."""

    def __new__(cls, ws_url: str = ""):
        if str(ws_url).startswith("ngoai:"):      # (V3.02) Chrome anh đang mở TISA BOT: đi qua một kết nối chung (tisa_browser_ngoai)
            import tisa_browser_ngoai as N
            return N.PhienNgoai(ws_url)
        return super().__new__(cls)

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
        if "/devtools/page/" in str(self.url):
            await _bat_tieu_diem(self)
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
    tab = _lay_tab()
    for t in ds:
        if t.get("id") == tab:
            sai = _tab_sai_ho_so(tab)
            if sai:
                raise RuntimeError(sai)
            return t
    if chat_hien_tai():
        raise RuntimeError("Ô chat này chưa có tab trình duyệt riêng (mỗi ô chat làm trên tab của riêng nó). Gọi tisa_browser_look op=open url=... để mở tab "
                           "cho ô chat này, hoặc op=tabs rồi switch_tab sang tab của ô chat này.")
    if _ngoai():
        raise RuntimeError("Đang dùng %s, chưa chọn tab nào để làm. Gọi op=tabs rồi op=switch_tab tab=<mã>, hoặc op=open url=... (mở tab mới). "
                           "Không tự đụng vào tab anh đang dùng." % _ten_hs())
    return ds[0]


def _tab_sai_ho_so(tab: str) -> str:
    """Anh đã chọn hồ sơ Chrome mà tab đang làm KHÔNG phải tab TISA mở trong hồ sơ đó thì chặn (V3.20, chủ báo 18/11/2026: chọn hồ sơ xong AI vẫn làm ở Chrome khác).
    Chrome không cho biết tab thuộc hồ sơ nào, nên chỉ tin tab do chính TISA BOT mở bằng --profile-directory. Rỗng = được làm."""
    try:
        import tisa_chong_chen as CC
        g = CC.doc_da_chon()
    except Exception:  # noqa: BLE001
        return ""
    if not g or not _ngoai():
        return ""
    with _khoa:
        ok = (_tt.get("tab_ho_so") or {}).get(tab) == g.get("thu_muc")
        xn = tab in (_tt.get("tab_xac_nhan") or set())
    if ok or xn:
        return ""
    return ("SAI_HO_SO: Anh đã chọn Chrome hồ sơ \"%s\" nhưng tab em đang làm không phải tab TISA BOT mở trong hồ sơ đó (Chrome không cho biết tab thuộc hồ sơ nào, có thể là tab của hồ sơ khác). "
            "Em DỪNG, không thao tác. Gọi op=mo_chrome (bỏ trống ho_so) hoặc op=open url=... để mở tab mới trong ĐÚNG hồ sơ rồi làm tiếp ở tab đó." % (g.get("ten") or g.get("thu_muc")))


async def ap_dung_ho_so_chrome(url: str = "about:blank") -> dict:
    """Anh vừa chọn hồ sơ Chrome (bấm ở hộp chọn, hoặc AI gọi mo_chrome): LÀM NGAY, không chỉ ghi nhớ. Chọn trình duyệt "Chrome của anh" thay vì trình duyệt riêng của TISA,
    bỏ tab đang làm (có thể ở hồ sơ khác), mở một tab trong ĐÚNG hồ sơ và chọn tab đó. Trả {"ok", "tab", "tin"}."""
    import tisa_chong_chen as CC
    g = CC.doc_da_chon()
    if not g:
        return {"ok": False, "tin": "Chưa chọn hồ sơ Chrome."}
    x = tao_ho_so_ngoai("chrome")
    if not x.get("ok"):
        return {"ok": False, "tin": "Không chọn được Chrome của anh làm trình duyệt đang dùng."}
    chon_ho_so(x["id"])                       # đồng thời bỏ tab đang làm
    _HS.set(x["id"])
    with _khoa:
        _tt["tab_ho_so"] = {}
        _tt["tab_xac_nhan"] = set()
    k = _kn()
    tid = await _tab_moi_ho_so_chrome(url) if await k.noi() else None
    if not tid:
        kq = await asyncio.to_thread(CC.mo_chrome, g["thu_muc"], "" if url == "about:blank" else url, True, False)
        _ghi_nk({"op": "mo_chrome", "ket_qua": "đã mở" if str(kq).startswith("Đã mở") else "lỗi", "mo_ta": "Mở Chrome hồ sơ %s" % (g.get("ten") or g["thu_muc"])})
        if not str(kq).startswith("Đã mở"):
            return {"ok": False, "tin": kq}
        for _ in range(16):
            if await k.noi():
                break
            await asyncio.sleep(0.5)
        if not await k.noi():
            import tisa_browser_ngoai as N
            return {"ok": False, "tin": "Đã mở Chrome hồ sơ %s nhưng chưa điều khiển được: %s" % (g.get("ten") or g["thu_muc"], N.loi_de_hieu(k))}
        return {"ok": True, "tab": "", "tin": "Đã mở Chrome hồ sơ %s. Mở trang bằng op=open url=... (tab mới trong đúng hồ sơ)." % (g.get("ten") or g["thu_muc"])}
    return {"ok": True, "tab": tid, "tin": "Đã mở tab mới trong Chrome hồ sơ %s và chọn làm tab đang làm." % (g.get("ten") or g["thu_muc"])}


async def _tab_moi_ho_so_chrome(url: str):
    """Chrome anh đang dùng có nhiều hồ sơ: Target.createTarget không chọn được hồ sơ nên tab có thể rơi vào hồ sơ khác. Khi anh đã chọn hồ sơ Chrome,
    mở bằng `chrome --profile-directory=<hồ sơ đã chọn> <url>` (Chrome đang chạy tự nhận) rồi bắt đúng tab mới. Trả mã tab hoặc None (dùng đường cũ)."""
    try:
        import tisa_chong_chen as CC
    except Exception:  # noqa: BLE001
        return None
    g = CC.doc_da_chon()
    if not g or not _ngoai() or not (re.match(r"^https?://", url or "") or url == "about:blank"):
        return None
    truoc = {t["id"] for t in await asyncio.to_thread(_trang_dang_co)}
    kq = await asyncio.to_thread(CC.mo_chrome, "", url, True, False)
    if not kq.startswith("Đã mở"):
        return None
    host = urllib.parse.urlparse(url).netloc
    for _ in range(24):
        await asyncio.sleep(0.5)
        moi = [t for t in await asyncio.to_thread(_trang_dang_co) if t["id"] not in truoc and (host in str(t.get("url", "")) or str(t.get("url", "")).startswith("chrome://newtab"))]
        if moi:
            _dat_tab(moi[0]["id"])
            with _khoa:
                _tt.setdefault("tab_ho_so", {})[moi[0]["id"]] = g.get("thu_muc")       # tab này CHẮC CHẮN thuộc hồ sơ đã chọn
            return moi[0]["id"]
    return None


async def _tab_moi(url: str) -> str:
    ma_ghim = await _tab_moi_ho_so_chrome(url)
    if ma_ghim:
        return ma_ghim
    co_trang = bool(await asyncio.to_thread(_trang_dang_co))
    async with _Phien(await _ws_url_trinh_duyet()) as b:
        r = await b.gui("Target.createTarget", {"url": url, "newWindow": not co_trang, **({"background": True} if co_trang else {})})     # anh đã đóng hết cửa sổ (Chrome vẫn chạy nền): mở lại cửa sổ mới
    _dat_tab(r.get("targetId", ""))
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
    dong = ["TRÌNH DUYỆT ĐANG DÙNG: %s" % _ten_hs(),
            "TRANG: %s | %s" % (d["title"][:100], d["url"][:200]),
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


def _doi_trinh_duyet(a: dict) -> str:
    """AI xin đổi trình duyệt đã chọn: LUÔN cần anh bấm Duyệt (đổi trình duyệt là đổi tài khoản đang đăng nhập), kể cả khi đang Toàn quyền."""
    x = tim_ho_so(str(a.get("trinh_duyet") or a.get("ten") or ""))
    if not x:
        return "LOI: không có trình duyệt đó. Các trình duyệt hiện có: %s." % ", ".join(y["ten"] for y in ds_ho_so())
    if x["id"] == hs_dang_dung():
        return "Trình duyệt \"%s\" đang là trình duyệt đã chọn rồi." % x["ten"]
    try:
        import tisa_chong_chen as _CC
        g = _CC.doc_da_chon()
        if g and _ngoai() and x.get("loai") != "ngoai":
            return ("KHOA_HO_SO: Anh đã chọn Chrome hồ sơ \"%s\" cho TISA BOT dùng, em không chuyển sang trình duyệt riêng của TISA \"%s\" (đó là cửa sổ trình duyệt khác, chưa đăng nhập tài khoản của anh). "
                    "Cần làm trong một hồ sơ Chrome khác của anh thì gọi op=mo_chrome ho_so=<tên hồ sơ Chrome>." % (g.get("ten") or g.get("thu_muc"), x["ten"]))
    except Exception:  # noqa: BLE001
        pass
    nc = {"host": "Trình duyệt TISA", "url": "", "tag": "", "ten": ("doi_trinh_duyet: %s" % x["ten"])[:100], "tieu_de": "chọn trình duyệt"}
    if not dung_duyet(str(a.get("duyet_id") or ""), "doi_trinh_duyet", nc):
        k = xin_duyet("doi_trinh_duyet", nc, "Đổi trình duyệt TISA BOT đang dùng từ \"%s\" sang \"%s\"" % (_ten_hs(hs_dang_dung()), x["ten"]))
        return ("CAN_DUYET: Đổi trình duyệt đang dùng sang \"%s\" (tài khoản đăng nhập khác). Anh phải bấm Duyệt trong TISA BOT. Gọi lại op=doi_trinh_duyet trinh_duyet=\"%s\" "
                "duyet_id=\"%s\" sau khi anh duyệt." % (x["ten"], x["ten"], k))
    chon_ho_so(x["id"])
    _ghi_nk({"op": "doi_trinh_duyet", "ket_qua": "đã đổi", "mo_ta": "Đã đổi sang %s sau khi anh duyệt" % x["ten"]})
    return "Đã đổi sang trình duyệt \"%s\"." % x["ten"]


async def _mo_chrome_ho_so(a: dict) -> str:
    """op=mo_chrome ho_so=<tên> [url=...]: anh nói "mở Google Chrome hồ sơ X" thì làm ĐÚNG việc đó trong MỘT lệnh (V3.20, chủ báo 18/11/2026).

    Lỗi cũ: AI không có lệnh nào gắn "hồ sơ Chrome thật của anh" với "trình duyệt TISA đang điều khiển", nên nó đổi sang trình duyệt RIÊNG của TISA (TK QC FB...)
    hoặc mở Chrome mà không điều khiển được trang. Nay: tìm đúng hồ sơ (kể cả chữ Chrome hiện ở menu hồ sơ), ghim làm hồ sơ đang dùng, chọn "Chrome của anh",
    mở trang trong ĐÚNG hồ sơ đó, chọn tab đó làm tab đang làm. Đổi hồ sơ và cấp Toàn quyền 2 giờ cần anh bấm Duyệt (tự duyệt nếu đang Toàn quyền)."""
    import tisa_chong_chen as CC
    ten = str(a.get("ho_so") or a.get("ten") or "").strip()
    url = str(a.get("url") or "").strip()
    ds = await asyncio.to_thread(CC.liet_ke_ho_so)
    if not ds:
        return "LOI: không đọc được danh sách hồ sơ Chrome (máy chưa cài Google Chrome, hoặc Chrome chưa mở lần nào)."
    liet = "; ".join("%s (%s)" % (x.get("hien_thi") or x["thu_muc"], x.get("email") or "chưa đăng nhập") for x in ds)
    ghim = CC.doc_da_chon()
    if ten:
        h = CC.tim_ho_so(ten, ds)
        if not h:
            return ("LOI: không thấy đúng MỘT hồ sơ Chrome tên \"%s\" (không có, hoặc có nhiều hồ sơ giống nhau). Các hồ sơ có: %s. "
                    "Hỏi anh đúng hồ sơ nào, hoặc dùng đúng chữ ở menu hồ sơ của Chrome." % (ten, liet))
    elif ghim:
        h = CC.tim_ho_so(ghim["thu_muc"], ds)
    else:
        return "CHUA_CHON: Anh chưa nói hồ sơ Chrome nào. Hỏi anh dùng hồ sơ nào rồi gọi op=mo_chrome ho_so=<tên>. Các hồ sơ có: %s." % liet
    if not h:
        return "LOI: hồ sơ Chrome đã chọn không còn. Các hồ sơ có: %s." % liet
    if url and not re.match(r"^https?://[^\s]+$", url):
        return "LOI: url phải bắt đầu bằng http:// hoặc https://."
    ten_h = "%s (%s)" % (h.get("hien_thi") or h["thu_muc"], h.get("email") or "chưa đăng nhập")
    doi_ghim = not ghim or ghim.get("thu_muc") != h["thu_muc"]
    chua_toan = muc_hien_tai() != "toan_quyen"
    if doi_ghim or chua_toan:
        nc = {"host": "Google Chrome", "url": "", "tag": "", "ten": ("mo_chrome: %s" % h["thu_muc"])[:100], "tieu_de": "mở hồ sơ Chrome"}
        if chua_toan and not dung_duyet(str(a.get("duyet_id") or ""), "mo_chrome", nc):
            k = xin_duyet("mo_chrome", nc, "Mở Google Chrome hồ sơ \"%s\" và cho TISA BOT điều khiển các trang trong hồ sơ đó (Toàn quyền 2 giờ, không xóa tệp)" % ten_h)
            _ghi_nk({"op": "mo_chrome", "ket_qua": "chờ duyệt", "mo_ta": "Mở Chrome hồ sơ %s" % ten_h})
            return ("CAN_DUYET: Mở Chrome hồ sơ \"%s\" và để AI điều khiển 2 giờ. Anh bấm Duyệt trong TISA BOT. Nói anh biết em sẽ mở đúng hồ sơ này, rồi gọi lại "
                    "op=mo_chrome ho_so=\"%s\" url=\"%s\" duyet_id=\"%s\" sau khi anh duyệt." % (ten_h, ten or h["thu_muc"], url, k))
        if doi_ghim:
            CC.dat_da_chon(h["thu_muc"], ds)
            _ghi_nk({"op": "mo_chrome", "ket_qua": "đã chọn", "mo_ta": "Chọn hồ sơ Chrome %s" % ten_h})
        if chua_toan:
            dat_muc("toan_quyen", 120)
            try:
                import tisa_desktop as _TD
                _TD.dat_muc("toan_quyen", 120)
            except Exception:  # noqa: BLE001
                pass
    x = tao_ho_so_ngoai("chrome")
    if not x.get("ok"):
        return "LOI: không chọn được Chrome của anh làm trình duyệt đang dùng (%s)." % (x.get("loi") or "lỗi lạ")
    chon_ho_so(x["id"])            # trình duyệt đang dùng = Chrome của anh (đúng cái anh đang đăng nhập), KHÔNG phải trình duyệt riêng của TISA
    _HS.set(x["id"])
    k = _kn()
    tid = None
    if url and await k.noi():
        tid = await _tab_moi_ho_so_chrome(url)
    if not tid:
        kq = await asyncio.to_thread(CC.mo_chrome, h["thu_muc"], url, True, False)
        if not str(kq).startswith("Đã mở"):
            return kq
        for _ in range(16):          # Chrome vừa mở: chờ nối
            if await k.noi():
                break
            await asyncio.sleep(0.5)
    if not await k.noi():
        import tisa_browser_ngoai as N
        return ("Đã mở Chrome hồ sơ %s%s nhưng CHƯA điều khiển được trang: %s" % (ten_h, (" tại " + url) if url else "", N.loi_de_hieu(k)))
    if not tid and url:
        host = urllib.parse.urlparse(url).netloc
        for _ in range(16):
            await asyncio.sleep(0.5)
            moi = [t for t in await asyncio.to_thread(_trang_dang_co) if host in str(t.get("url", ""))]
            if moi:
                _dat_tab(moi[-1]["id"])
                with _khoa:
                    _tt.setdefault("tab_ho_so", {})[moi[-1]["id"]] = h["thu_muc"]
                tid = moi[-1]["id"]
                break
    _ghi_nk({"op": "mo_chrome", "ket_qua": "đã mở", "mo_ta": "Chrome hồ sơ %s%s" % (ten_h, (": " + url[:80]) if url else "")})
    if tid:
        t = next((y for y in await asyncio.to_thread(_trang_dang_co) if y["id"] == tid), {})
        return ("Đã mở Chrome hồ sơ %s và đang điều khiển tab \"%s\" (%s). Trình duyệt đang dùng: Chrome của anh, đúng hồ sơ này, quyền Toàn quyền. "
                "Gọi tisa_browser_look để xem trang rồi tisa_browser_do để làm. KHÔNG đổi sang trình duyệt riêng của TISA." % (ten_h, str(t.get("title") or "")[:50], str(t.get("url") or url)[:80]))
    return ("Đã mở Chrome hồ sơ %s. Trình duyệt đang dùng: Chrome của anh. Gọi op=tabs rồi switch_tab tab=<mã> để chọn tab cần làm (hoặc op=open url=... để mở trang mới "
            "trong đúng hồ sơ này)." % ten_h)


async def thuc_hien(op: str, a: dict) -> str:
    op = str(op or "").strip().lower()
    a = a or {}
    chon = a.get("trinh_duyet") or a.get("browser") or ""
    if op == "doi_trinh_duyet":
        return _doi_trinh_duyet(a)
    if op == "mo_chrome":
        return await _mo_chrome_ho_so(a)
    c_goi = chat_hien_tai()
    if c_goi:
        with _khoa:      # khung Trình duyệt trên trang đang mở ô chat này tự hiện lên để anh thấy bot đang làm gì (không ghi đĩa)
            _tab_chat.setdefault(c_goi, {"tab": "", "tabs": []})["luc"] = time.time()
    ban = hs_cua_chat()
    if ban:
        # (V3.43) Ô chat này đã mở khung Trình duyệt: AI của ô chat làm trong trình duyệt ngầm của khung (anh thấy và điều khiển được ở khung bên phải).
        x = tim_ho_so(str(chon)) if chon else None
        if chon and x and x["id"] != ban and op != "profiles":
            return ("KHOA_TRINH_DUYET: Ô chat này dùng trình duyệt của khung Trình duyệt bên phải (\"%s\"), anh thấy và điều khiển được ở đó. Làm tiếp ở đó "
                    "(bỏ tham số trinh_duyet). Anh đăng nhập tài khoản ngay trong khung nếu trang đòi." % _ten_hs(ban))
        chon = ""
    if ban:
        pass
    elif op not in ("profiles", "status") and not _ngoai():
        # Anh đã ghim hồ sơ Chrome THẬT mà trình duyệt đang dùng lại là bản riêng của TISA (vd "TK QC FB" nhập cookie từ hồ sơ cũ): tự về "Chrome của anh" (V3.20).
        try:
            import tisa_chong_chen as _CC
            if _CC.doc_da_chon():
                x = tao_ho_so_ngoai("chrome")
                if x.get("ok"):
                    chon_ho_so(x["id"])
                    _HS.set(x["id"])
                    _ghi_nk({"op": "mo_chrome", "ket_qua": "tự về Chrome của anh", "mo_ta": "Đã ghim hồ sơ Chrome nên không dùng trình duyệt riêng của TISA"})
        except Exception:  # noqa: BLE001
            pass
    if chon:
        x = tim_ho_so(str(chon))
        if not x:
            return "LOI: không có trình duyệt \"%s\". Các trình duyệt hiện có: %s." % (chon, ", ".join("%s" % y["ten"] for y in ds_ho_so()))
        if x["id"] != hs_dang_dung() and op != "profiles":
            # (18/11/2026) Anh ĐÃ CHỌN một trình duyệt cho TISA BOT dùng: mỗi lệnh không được tự nhảy sang trình duyệt/hồ sơ khác (có thể chưa đăng nhập).
            _ghi_nk({"op": "khoa_trinh_duyet", "ket_qua": "từ chối đổi", "mo_ta": "Xin dùng \"%s\" trong khi anh đã chọn \"%s\"" % (x["ten"], _ten_hs(hs_dang_dung()))})
            return ("KHOA_TRINH_DUYET: Anh đã chọn trình duyệt \"%s\" cho TISA BOT dùng nên em không chuyển sang \"%s\". Làm tiếp bằng trình duyệt đã chọn (bỏ tham số trinh_duyet). "
                    "Cần trình duyệt khác thì hỏi anh, rồi gọi op=doi_trinh_duyet trinh_duyet=\"%s\" (anh phải bấm Duyệt)." % (_ten_hs(hs_dang_dung()), x["ten"], x["ten"]))
        _HS.set(x["id"])
    else:
        _HS.set(ban or hs_dang_dung())
    if op == "profiles":
        cur = hs_dang_dung()
        return "Các trình duyệt (mỗi cái đăng nhập tài khoản riêng):\n" + "\n".join("- %s%s: %s" % (y["ten"], " (đang dùng mặc định)" if y["id"] == cur else "", _tt_ho_so(y)) for y in ds_ho_so()) + \
            "\nTISA BOT chỉ dùng trình duyệt anh đã chọn (đánh dấu ở trên); không tự nhảy sang cái khác. Cần đổi: op=doi_trinh_duyet trinh_duyet=<tên> (anh phải bấm Duyệt)."
    with _khoa:
        dung = _tt["dung"]
    if dung and op not in ("status", "tabs"):
        return "DA_DUNG: Anh đã bấm Dừng ngay. Không thao tác tiếp. Nói anh bấm nút Cho AI làm tiếp trong cửa sổ trợ lý nổi (hoặc nhắn \"làm tiếp\"), rồi mới làm."
    if op == "ui_tisa":
        return await _ui_tisa(a)
    if op == "hoi_mo":
        return await _hoi_mo(a)
    if op == "status":
        return json.dumps(trang_thai(), ensure_ascii=False)
    if _ngoai() and not _kn().song:
        import tisa_browser_ngoai as N
        if not await _kn().noi():
            return N.loi_de_hieu(_kn())
    if op == "dan_vao_tisa":
        if not _cong_mo():
            return "CHUA_MO: %s chưa mở, không có trang nguồn để lấy mã." % _ten_hs()
        return await _dan_vao_tisa(a)
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
                ds_tab = await asyncio.to_thread(_trang_dang_co) if _trang_dang_co() else []
                t_san = _tab_khop(tab_cua_chat(ds_tab), url)      # (V3.02) đã có tab đúng trang (đã đăng nhập): dùng lại tab đó thay vì đè lên tab khác
                if t_san is not None:
                    await _chuyen_tab(t_san)
                    if str(t_san.get("url") or "").split("#")[0].rstrip("/") != url.split("#")[0].rstrip("/"):
                        async with _Phien(t_san["webSocketDebuggerUrl"]) as p:
                            await p.gui("Page.navigate", {"url": url})
                            await _doi_tai(p)
                    t = t_san
                elif _ngoai():
                    t = None          # Chrome của anh: luôn mở tab mới, không đè lên tab anh đang dùng
                elif chat_hien_tai() and not any(x["id"] == _lay_tab() for x in ds_tab):
                    t = None          # ô chat này chưa có tab: mở tab mới riêng cho ô chat, không đè tab của ô chat khác
                else:
                    t = await _trang_hien_tai() if _trang_dang_co() else None
                if t_san is not None:
                    pass
                elif t is None:
                    await _tab_moi(url)
                    await asyncio.sleep(2.0)       # chờ tab mới tải trước khi nhìn
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
            ds = tab_cua_chat(await asyncio.to_thread(_trang_dang_co))
            tab = _lay_tab() or ("" if (_ngoai() or chat_hien_tai()) else (ds[0]["id"] if ds else ""))
            return "\n".join("%s %s | %s | %s" % ("*" if t["id"] == tab else " ", t["id"][:8], t.get("title", "")[:60], t.get("url", "")[:100]) for t in ds) or "(chưa có tab nào%s)" % (" của ô chat này, mở bằng op=open url=..." if chat_hien_tai() else "")
        if op == "screenshot":
            t = await _trang_hien_tai()
            async with _Phien(t["webSocketDebuggerUrl"]) as p:
                f = await _chup(p)
            return "Ảnh chụp màn hình đã lưu: %s (ảnh gửi kèm ngay bên dưới để nhìn bố cục; nếu không thấy ảnh thì nói thật là chưa nhìn được, đừng đoán).\n\u27e6ANH:%s\u27e7" % (f, f)
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


_KEYCHAIN_CAM = {"mo-khoa"}      # mật khẩu mở khóa máy: chỉ anh tự thêm bằng lệnh security, AI không bao giờ ghi mục này


async def _luu_keychain(a: dict, t_nguon: dict) -> str:
    """Chép một giá trị (khóa API, client secret, refresh token) từ ô hoặc khối chữ ở tab NGUỒN thẳng vào macOS Keychain, mục tisa-bot-<ten>.
    Giá trị đi từ trang vào Keychain, KHÔNG BAO GIỜ trả về cho mô hình, không vào nhật ký, không vào tệp. truong=<khóa> thì gộp vào JSON của mục đó
    (ví dụ ten=drive-client truong=client_id rồi truong=client_secret). Cần anh duyệt (trừ khi đang Toàn quyền)."""
    import re as _re
    ten = str(a.get("ten") or "").strip().lower()
    truong = str(a.get("truong") or "").strip()
    if not _re.fullmatch(r"[a-z0-9-]{2,40}", ten) or ten in _KEYCHAIN_CAM:
        return "LOI: ten của mục Keychain chỉ gồm chữ thường, số, dấu gạch (ví dụ drive-client, bunny, heygen); mục mo-khoa bị cấm: mật khẩu máy anh tự thêm."
    if truong and not _re.fullmatch(r"[a-zA-Z0-9_]{1,40}", truong):
        return "LOI: truong không hợp lệ."
    tu_tab = str(a.get("tu_tab") or "")
    try:
        tu_id = int(a.get("tu_id") or 0)
    except (TypeError, ValueError):
        tu_id = 0
    if not tu_tab or tu_id <= 0:
        return "LOI: luu_keychain cần tu_tab (mã tab nguồn, op=tabs) và tu_id (số [n] của khối chứa giá trị, từ look) và ten."
    nc = {"host": "Keychain", "url": "", "tag": "", "ten": ("luu_keychain: tisa-bot-%s%s" % (ten, (" / " + truong) if truong else ""))[:100], "tieu_de": "keychain"}
    if muc_hien_tai() != "toan_quyen" and not dung_duyet(str(a.get("duyet_id") or ""), "luu_keychain", nc):
        k = xin_duyet("luu_keychain", nc, "Cất một khóa vào Keychain của máy (mục tisa-bot-%s)" % ten)
        _ghi_nk({"op": "luu_keychain", "ket_qua": "chờ duyệt", "mo_ta": "mục tisa-bot-" + ten, "ten": truong, "host": "Keychain"})
        return ("CAN_DUYET: Cất một khóa vào Keychain (mục tisa-bot-%s). Giá trị không hiện ra. Anh phải bấm Duyệt trong TISA BOT; gọi lại đúng lệnh này với duyet_id=\"%s\" sau khi anh duyệt." % (ten, k))
    ds = await asyncio.to_thread(_trang_dang_co)
    nguon = next((x for x in ds if x["id"].startswith(tu_tab)), None)
    if not nguon:
        return "LOI: không thấy tab nguồn %s (xem op=tabs)." % tu_tab
    async with _Phien(nguon["webSocketDebuggerUrl"]) as ps:
        gia_tri = await ps.js("""(() => { const e = (window.__tisa && window.__tisa.marks || [])[%d - 1]; if (!e) return null;
          const v = (e.value !== undefined && String(e.value) !== '') ? e.value : (e.innerText || e.textContent || ''); return String(v).trim(); })()""" % tu_id)
    if not gia_tri:
        return "LOI: không đọc được giá trị ở ô [%d] của tab nguồn (look lại tab nguồn)." % tu_id
    if len(gia_tri) > 6000:
        return "LOI: giá trị dài bất thường (%d ký tự), không cất." % len(gia_tri)
    import tisa_keychain as KC
    dich_vu = "tisa-bot-" + ten
    if truong:
        try:
            d = json.loads(KC.doc(dich_vu) or "{}")
            if not isinstance(d, dict):
                d = {}
        except ValueError:
            d = {}
        d[truong] = gia_tri
        ok = KC.luu(dich_vu, json.dumps(d))
    else:
        ok = KC.luu(dich_vu, gia_tri)
    gia_tri = ""
    _ghi_nk({"op": "luu_keychain", "ket_qua": "ok" if ok else "lỗi", "mo_ta": "Cất 1 giá trị (ẩn) vào Keychain mục %s%s" % (dich_vu, (" trường " + truong) if truong else ""), "ten": truong, "host": "Keychain"})
    return ("Đã cất giá trị (ẩn, em không nhìn thấy) vào Keychain, mục %s%s." % (dich_vu, (" trường " + truong) if truong else "")) if ok else "LOI: không ghi được vào Keychain (máy khóa Keychain, hoặc không phải macOS)."


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
    if op == "luu_keychain":
        return await _luu_keychain(a, t)
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
        ly_do = str(a.get("ly_do") or "làm bước cần anh")[:600]
        toi_da = min(max(int(a.get("giay") or 180), 10), 600)
        cho = str(a.get("text") or "")
        url0 = t.get("url", "")
        with _khoa:
            _tt["cho_nguoi"] = {"ly_do": ly_do, "luc": time.time()}
        _ghi_nk({"op": "wait_user", "ket_qua": "đang chờ anh", "mo_ta": ly_do, "host": urllib.parse.urlparse(url0).netloc})
        try:      # (18/11/2026) báo anh một tin ngắn (dashboard, Zalo) để anh làm giúp dù đang ở xa máy
            import tisa_bao_anh
            tisa_bao_anh.bao("TISA BOT đang chờ anh trên trình duyệt: %s. Anh làm giúp em rồi em tự làm tiếp." % ly_do)
        except Exception:  # noqa: BLE001
            pass
        try:
            t0 = time.time()
            while time.time() - t0 < toi_da:
                await asyncio.sleep(1.5)
                with _khoa:
                    if _tt["dung"]:
                        return "DA_DUNG: Anh đã bấm Dừng ngay."
                    if _tt.pop("nguoi_xong", False):          # (V3.04) anh bấm "Em làm xong rồi" ở cửa sổ trợ lý nổi
                        return "Anh báo đã làm xong (bấm Em làm xong rồi). Gọi look để kiểm tra trang."
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
        chu = chu_cua_tab(m["id"])
        if chat_hien_tai() and chu and chu != chat_hien_tai():
            return "LOI: tab %s là của ô chat khác. Mỗi ô chat chỉ làm trên tab của mình: mở tab mới bằng op=open url=..." % k
        _dat_tab(m["id"])
        with _khoa:
            if a.get("xac_nhan"):
                _tt.setdefault("tab_xac_nhan", set()).add(m["id"])
        sai = _tab_sai_ho_so(m["id"])
        if sai:
            _dat_tab("")
            return sai + " (Nếu anh xác nhận tab này đúng hồ sơ thì gọi lại switch_tab kèm xac_nhan=true.)"
        if a.get("hien"):          # chỉ khi anh muốn XEM tab đó (hien=true) mới lật tab trên màn hình
            async with _Phien(await _ws_url_trinh_duyet()) as b:
                await b.gui("Target.activateTarget", {"targetId": m["id"]})
        return "Đã chuyển sang làm việc ở tab %s (tab anh đang xem KHÔNG bị đổi; AI vẫn thao tác được tab này dù nó đang bị che hay ở sau tab khác)." % m.get("title", "")[:50]
    if op == "close_tab":
        async with _Phien(await _ws_url_trinh_duyet()) as b:
            await b.gui("Target.closeTarget", {"targetId": t["id"]})
        _dat_tab("")
        return "Đã đóng tab."
    return "LOI: op không hợp lệ: %s" % op


# ---------------------------------------------------------------- trạng thái cho bảng điều khiển
_DAU_PHIEN = {"c_user", "xs", "sessionid", "sid", "ssid", "auth_token", "li_at", "oauth_token", "session", "token", "access_token", "zpsid", "zpw_sek", "sapisid", "__secure-1psid", "login"}


def _tt_ho_so(y: dict) -> str:
    if y.get("loai") == "ngoai":
        return "trình duyệt anh đang mở TISA BOT, có sẵn các tài khoản anh đã đăng nhập; %s" % ("đã nối" if _kn(y["id"]).song else "chưa nối (lần đầu làm việc Chrome sẽ hỏi anh Cho phép)")
    return "đang mở" if _cong_mo(y["cong"]) else "chưa mở"


def _dong_hs(x: dict) -> dict:
    d = {"id": x["id"], "ten": x["ten"], "nhap_tu": (x.get("nhap_tu") or {}).get("ten_nguon", "")}
    if x.get("loai") == "ngoai":
        import tisa_browser_ngoai as N
        n = N.trang_thai(x.get("trinh") or "chrome")
        d.update(loai="ngoai", trinh=n["trinh"], ten_trinh=n["ten_trinh"], tinh_trang=n["tinh_trang"], dang_chay=n["tinh_trang"] == "da_noi", loi_noi=n["loi"] in ("CHUA_CHO_PHEP", "MAT_KET_NOI") or n["loi"].startswith("LOI"))
    else:
        d["dang_chay"] = _cong_mo(x["cong"])
    return d


def trang_thai(hs: str = "") -> dict:
    if hs:
        _HS.set(hs)
    mo = _cong_mo()
    out = {"dang_chay": mo, "chrome": Path(tim_chrome()).name if tim_chrome() else "", "dung": _tt["dung"], "hoso": _hs(), "muc": muc_hien_tai(), "muc_den": _tt["muc_den"],
           "cho_nguoi": _tt["cho_nguoi"], "trang": [], "cho_duyet": [], "cho_chon": [], "cho_dan": bool(dan_dang_cho()), "cho_ui": bool(ui_dang_cho()), "nhat_ky": doc_nk(14),
           "trang_tisa": ["http://127.0.0.1:%s" % os.getenv("TISA_PORT", "7777")] + ["https://" + h for h in sorted(_mien_toi) if h.split(":")[0] not in ("127.0.0.1", "localhost")],
           "ho_so_ds": [_dong_hs(x) for x in ds_ho_so()], "hoso_dang_dung": hs_dang_dung(), "hoso_xem": _hs(), "ten_xem": _ten_hs()}
    if mo:
        out["trang"] = [{"id": t["id"][:8], "tieu_de": t.get("title", "")[:70], "host": urllib.parse.urlparse(t.get("url", "")).netloc} for t in _trang_dang_co()][:8]
        out["khong_cua_so"] = not out["trang"]
    with _khoa:
        for k, v in _duyet.items():
            if v["trang_thai"] == "cho" and time.time() - v["luc"] < HIEU_LUC_DUYET:
                out["cho_duyet"].append({"id": k, "op": v["op"], "mo_ta": v["mo_ta"], "ten": v["ten"], "host": v["host"], "trang": v["trang"]})
        for k, v in _chon.items():
            if v["trang_thai"] == "cho" and time.time() - v["luc"] < HIEU_LUC_CHON:
                out["cho_chon"].append({"id": k, "ly_do": v["ly_do"], "trang": v["trang"]})
    return out


async def trang_da_dang_nhap(hs: str = "") -> list:
    """Tên miền có phiên đăng nhập (chỉ tên miền và số cookie, không bao giờ giá trị)."""
    if hs:
        _HS.set(hs)
    if not _cong_mo():
        return []
    try:
        ck = await _doc_cookie(False)
    except Exception:  # noqa: BLE001
        return []
    ds: dict = {}
    for c in ck:
        d = str(c.get("domain", "")).lstrip(".")
        ph = d.split(".")
        # com.vn, co.uk...: tên miền gốc gồm 3 phần (a.com.vn), không để chỉ còn "com.vn"
        goc = ".".join(ph[-3:]) if (len(ph) >= 3 and len(ph[-1]) == 2 and ph[-2] in ("com", "net", "org", "gov", "edu", "co", "ac")) else (".".join(ph[-2:]) if len(ph) >= 2 else d)
        e = ds.setdefault(goc, {"mien": goc, "so": 0, "phien": False})
        e["so"] += 1
        if str(c.get("name", "")).lower() in _DAU_PHIEN:
            e["phien"] = True
    return sorted(ds.values(), key=lambda x: (not x["phien"], -x["so"]))[:40]


async def dong_trinh_duyet(hs: str = "") -> dict:
    if hs:
        _HS.set(hs)
    if _ngoai():
        await _kn().ngat()       # Chrome của anh: chỉ ngắt kết nối, KHÔNG đóng Chrome
        _ghi_nk({"op": "dong", "ket_qua": "đã ngắt", "mo_ta": "Ngắt khỏi %s" % _ten_hs()})
        return {"ok": True}
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
_MO_TA_LAM = ("Điều khiển trình duyệt TISA như người thật. KHI ANH NÓI \"mở Google Chrome hồ sơ X\": gọi MỘT lệnh op=mo_chrome ho_so=<tên> [url=...] (ho_so đúng chữ menu hồ sơ Chrome, ví dụ Sang (TIÊU SANG QUẢNG CÁO)): nó mở ĐÚNG hồ sơ Chrome thật của anh, chọn làm trình duyệt đang dùng, chọn tab đó, cấp Toàn quyền 2 giờ sau khi anh duyệt; KHÔNG dùng doi_trinh_duyet sang trình duyệt riêng của TISA và KHÔNG mở Chrome mới. op=click id=n (hoặc x,y); op=type id=n text=... (xoa=false để không xóa chữ cũ); op=press key=Enter|Tab|Escape...; "
              "op=scroll huong=down|up px=600; op=select id=n value=...; op=upload id=n path=...; op=wait ms=... text=...; op=wait_user ly_do=... (chờ anh đăng nhập, nhập mã, giải CAPTCHA); op=ui_tisa lenh=mo_the ten=<tên thẻ> [dich_vu] [truong] | chon_o truong=<nhãn ô> | bam nhan=<chữ trên nút> | xem (điều khiển thẳng giao diện TISA BOT: mở trang Kết nối, mở thẻ, chọn ô, bấm nút; KHÔNG cần chuột; kết quả chỉ là chữ nhãn, không có giá trị trong ô); op=dan_vao_tisa tu_tab=<mã tab nguồn> tu_id=<số khối mã> (dán mã vào Ô ĐANG ĐƯỢC CHỌN trong cửa sổ TISA BOT; trước đó dùng điều khiển máy tính click vào ô cần dán; giá trị em không nhìn thấy); op=dan_vao_tisa kieu=phien_trinh_duyet mien=google.com (lấy PHIÊN ĐĂNG NHẬP của chính trình duyệt đã chọn, dạng storage_state, dán vào ô đang chọn; cần anh duyệt; dùng cho kết nối đòi cookie phiên như NotebookLM, cần anh duyệt trừ khi đang Toàn quyền; KHÔNG chạy lệnh login mở trình duyệt khác); op=hoi_mo ly_do=... trang=[{ten,url,mo_ta}] (nếu trình duyệt TISA đang chạy và ĐÃ CÓ SẴN tab của đúng trang thì tự chuyển sang tab đó, tài khoản đã đăng nhập sẵn, không hỏi; chưa có tab thì hiện hộp cho anh CHỌN web và trình duyệt, rồi mở trong TAB MỚI; dùng trước khi mở một web mới của nền tảng, và luôn xem op=tabs trước để tận dụng tab đã đăng nhập); "
              "op=luu_keychain tu_tab tu_id ten=<tên mục> [truong=<khóa JSON>] (cất khóa API/token từ trang nền tảng thẳng vào Keychain, giá trị không hiện ra; cần anh duyệt); op=dan_ma tu_tab=<mã tab nguồn> tu_id=<số ô nguồn> id=<số ô đích> (chép mã API, token từ trang nền tảng sang ô của TISA BOT mà em không nhìn thấy giá trị; chỉ dán vào trang TISA BOT); op=back|forward|reload|new_tab url|switch_tab tab|close_tab. Mọi lần bấm phải sau một lần look (số n chỉ đúng cho lần look gần nhất). Việc đăng, gửi, xóa, đổi bảo mật trả CAN_DUYET: "
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
            return "LOI: op của tisa_browser_do: click, type, press, scroll, select, upload, dan_ma, wait, wait_user, hoi_mo, dan_vao_tisa, ui_tisa, doi_trinh_duyet, mo_chrome, luu_keychain, back, forward, reload, new_tab, switch_tab, close_tab."
        return await thuc_hien(op, a)

    add("tisa_browser_look", _MO_TA_NHIN,
        {"op": {"type": "string", "description": "open | look | screenshot | tabs | status | profiles (mặc định look)"}, "url": {"type": "string"},
         "trinh_duyet": {"type": "string", "description": "tên hoặc số của trình duyệt cần dùng (xem op=profiles); bỏ trống = trình duyệt mặc định"}},
        [], _nhin, effect="write")
    add("tisa_browser_do", _MO_TA_LAM,
        {"op": {"type": "string"}, "id": {"type": "integer", "description": "số [n] từ look"}, "x": {"type": "integer"}, "y": {"type": "integer"},
         "text": {"type": "string"}, "key": {"type": "string"}, "value": {"type": "string"}, "path": {"type": "string"}, "url": {"type": "string"},
         "huong": {"type": "string"}, "px": {"type": "integer"}, "ms": {"type": "integer"}, "giay": {"type": "integer"}, "ho_so": {"type": "string", "description": "op=mo_chrome: tên hồ sơ Chrome THẬT của anh (đúng chữ menu hồ sơ Chrome, ví dụ Sang (TIÊU SANG QUẢNG CÁO), hoặc tên hồ sơ, email)"}, "xac_nhan": {"type": "boolean", "description": "switch_tab: true = anh đã xác nhận tab này đúng hồ sơ Chrome đã chọn"}, "hien": {"type": "boolean", "description": "switch_tab: true = lật tab đó lên màn hình cho anh xem; mặc định false = chỉ đổi tab AI làm việc, không đổi tab anh đang xem"}, "tab": {"type": "string"},
         "ly_do": {"type": "string"}, "lenh": {"type": "string", "description": "ui_tisa: mo_the | chon_o | bam | xem"}, "ten": {"type": "string"}, "truong": {"type": "string"}, "nhan": {"type": "string"}, "dich_vu": {"type": "string"}, "kieu": {"type": "string", "description": "dan_vao_tisa: phien_trinh_duyet = lấy phiên đăng nhập của trình duyệt đã chọn"}, "mien": {"type": "string", "description": "phien_trinh_duyet: tên miền, ví dụ google.com"}, "trang": {"type": "array", "items": {"type": "object"}, "description": "hoi_mo: các web đề xuất cho anh chọn, mỗi mục {ten, url, mo_ta}"}, "duyet_id": {"type": "string"}, "xoa": {"type": "boolean"}, "tu_tab": {"type": "string"}, "tu_id": {"type": "integer"},
         "trinh_duyet": {"type": "string", "description": "BỎ TRỐNG: dùng trình duyệt anh đã chọn. Khác với cái đã chọn thì bị KHOA_TRINH_DUYET (đổi bằng op=doi_trinh_duyet, anh phải duyệt)"}, "tu_trinh_duyet": {"type": "string", "description": "dan_ma: trình duyệt chứa trang nguồn"}},
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

    @app.post("/trinh-duyet/ngoai")
    async def tb_ngoai(request: Request):
        """(V3.02) Dùng Chrome anh đang mở TISA BOT. hanh=them (thêm vào danh sách và chọn), noi (nối, Chrome hỏi Cho phép), ngat, kiem (chỉ xem)."""
        from fastapi.responses import JSONResponse
        import tisa_browser_ngoai as N
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        trinh = str((d or {}).get("trinh") or "chrome")
        h = str((d or {}).get("hanh") or "kiem")
        if h == "them":
            kq = tao_ho_so_ngoai(trinh)
            if kq.get("ok"):
                chon_ho_so(kq["id"])
                if N.doc_cong(trinh):
                    asyncio.create_task(N.ket_noi(trinh).noi())       # nối nền: Chrome hiện hộp hỏi, bảng tự cập nhật
            return JSONResponse(dict(kq, **N.trang_thai(trinh)))
        if h == "noi":
            if not N.doc_cong(trinh):
                return JSONResponse(dict(N.trang_thai(trinh), ok=False))
            asyncio.create_task(N.ket_noi(trinh).noi())
            await asyncio.sleep(0.3)
            return JSONResponse(dict(N.trang_thai(trinh), ok=True))
        if h == "ngat":
            await N.ket_noi(trinh).ngat()
        return JSONResponse(dict(N.trang_thai(trinh), ok=True))

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

    @app.post("/trinh-duyet/nguoi-xong")
    async def tb_nguoi_xong():
        """Anh báo "em làm xong rồi" (cửa sổ trợ lý nổi): AI đang wait_user thì làm tiếp ngay, không phải chờ trang đổi."""
        from fastapi.responses import JSONResponse
        with _khoa:
            co = bool(_tt.get("cho_nguoi"))
            if co:
                _tt["nguoi_xong"] = True
        return JSONResponse({"ok": True, "dang_cho": co})

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

    @app.get("/trinh-duyet/ui-cho")
    async def tb_ui_cho():
        from fastapi.responses import JSONResponse
        return JSONResponse(ui_dang_cho())

    @app.post("/trinh-duyet/ui-lay")
    async def tb_ui_lay(request: Request):
        from fastapi.responses import JSONResponse
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        return JSONResponse(ui_lay(str((d or {}).get("id") or "")))

    @app.post("/trinh-duyet/ui-xong")
    async def tb_ui_xong(request: Request):
        from fastapi.responses import JSONResponse
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        d = d or {}
        return JSONResponse(ui_xong(str(d.get("id") or ""), bool(d.get("ok")), str(d.get("kq") or "")))

    @app.get("/trinh-duyet/dan-cho")
    async def tb_dan_cho():
        from fastapi.responses import JSONResponse
        return JSONResponse({"id": dan_dang_cho()})

    @app.post("/trinh-duyet/dan-lay")
    async def tb_dan_lay(request: Request):
        from fastapi.responses import JSONResponse
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        return JSONResponse(dan_lay(str((d or {}).get("id") or "")), headers={"Cache-Control": "no-store"})

    @app.post("/trinh-duyet/dan-xong")
    async def tb_dan_xong(request: Request):
        from fastapi.responses import JSONResponse
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        d = d or {}
        return JSONResponse(dan_xong(str(d.get("id") or ""), bool(d.get("ok")), str(d.get("nhan") or ""), d.get("so") or 0, str(d.get("loi") or "")))

    @app.post("/trinh-duyet/chon")
    async def tb_chon(request: Request):
        from fastapi.responses import JSONResponse
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        d = d or {}
        return JSONResponse(tra_loi_chon(str(d.get("id") or ""), str(d.get("url") or ""), str(d.get("hoso") or ""), bool(d.get("huy"))))

    @app.get("/trinh-duyet/nhat-ky")
    async def tb_nk(n: int = 60):
        from fastapi.responses import JSONResponse
        return JSONResponse({"nhat_ky": doc_nk(max(1, min(int(n), 300)))})


_nap_muc()
_nap_tab_chat()
