"""tisa_chong_chen.py - Chống chen ngang khi gõ vào Chrome (chủ báo 18/11/2026: thẻ tự mở và đóng, hộp "Đóng thẻ và xoá nhóm?", phím gõ bị chen).

Trước khi tisa_desktop gõ hay nhấn phím vào một trình duyệt Chromium (Chrome, Edge, Brave...), kiểm xem có thứ KHÁC đang điều khiển trình duyệt đó không.
Có thì DỪNG và nói rõ nguyên nhân, không gõ mù. Thứ đang điều khiển nhận ra qua danh sách tiến trình (macOS, Linux; Windows chưa kiểm):

  CỨNG (chặn gõ):  cầu nối tiện ích trình duyệt (chrome-native-host, ví dụ tiện ích Claude in Chrome), chromedriver, playwright-mcp chạy kiểu --extension
                   hoặc --cdp-endpoint (nối vào Chrome đang mở), chrome-devtools-mcp, puppeteer, selenium, Chrome đang mở cổng gỡ lỗi
                   (--remote-debugging-port/pipe) hoặc cờ tự động hóa (--enable-automation) mà KHÔNG phải trình duyệt riêng của TISA BOT.
  MỀM (chỉ báo):    playwright-mcp chạy với hồ sơ riêng (--user-data-dir): mở Chrome RIÊNG, không đụng Chrome chính của anh.

Trình duyệt riêng của chính TISA BOT (thư mục trinh-duyet/ho-so) không tính là chen.

Ưu tiên cửa sổ riêng: mo_chrome(ho_so, url) mở MỘT cửa sổ mới của đúng hồ sơ Chrome cần dùng (tên hồ sơ như thấy trong Chrome, ví dụ TIEUSANGSTUDIO).
Dùng đúng tiến trình Chrome đang chạy (không mở Chrome thứ hai, không đụng phiên đăng nhập).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

try:
    import config as _cfg
    STATE_DIR = Path(_cfg.STATE_DIR)
except Exception:  # noqa: BLE001
    STATE_DIR = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)

TEP_GHIM = STATE_DIR / "dieu-khien-may" / "chrome-da-chon.json"

_TRINH_DUYET = re.compile(r"google chrome|chrome|chromium|microsoft edge|msedge|brave|vivaldi|opera|arc", re.I)
_CUNG = [
    (re.compile(r"chrome-native-host|native-messaging-host|chrome_native_host", re.I), "Cầu nối tiện ích trình duyệt đang chạy (%s): một tiện ích như Claude in Chrome có thể đang mở, đóng thẻ và gõ phím trong Chrome của anh"),
    (re.compile(r"chromedriver", re.I), "chromedriver đang chạy: một chương trình tự động hóa (Selenium) đang điều khiển Chrome"),
    (re.compile(r"chrome-devtools-mcp", re.I), "chrome-devtools-mcp đang chạy: một công cụ AI đang nối vào Chrome"),
    (re.compile(r"(puppeteer|selenium)", re.I), "Công cụ tự động hóa trình duyệt (%s) đang chạy"),
]
_PW_MCP = re.compile(r"playwright[-/ ]mcp|@playwright/mcp", re.I)
_CO_NOI_CHROME = re.compile(r"--extension\b|--cdp-endpoint|--cdp-url", re.I)
_CO_RIENG = re.compile(r"--user-data-dir|--isolated", re.I)
_CO_TU_DONG = re.compile(r"--remote-debugging-(port|pipe)|--enable-automation|--test-type=webdriver", re.I)
_CO_PHU = re.compile(r"--type=|Helper|crashpad|--utility-sub-type", re.I)


def doc_tien_trinh() -> str:
    """Toàn bộ dòng lệnh các tiến trình (pid + lệnh). Không có thì trả chuỗi rỗng."""
    try:
        if sys.platform == "win32":
            r = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_Process | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                               capture_output=True, text=True, timeout=15)
        else:
            r = subprocess.run(["/bin/ps", "-axo", "pid=,command="], capture_output=True, text=True, timeout=8)
        return r.stdout or ""
    except (OSError, subprocess.SubprocessError):
        return ""


def _ten_ngan(dong: str) -> str:
    m = re.search(r"/([^/ ]+?)(?: |$)", dong.split(" ", 1)[-1].strip() + " ")
    return (m.group(1) if m else dong.strip().split(" ", 1)[-1])[:40]


def phat_hien(ps_text: str | None = None, ho_so_tisa: str = "") -> dict:
    """{"cung": [lý do...], "mem": [lý do...]} từ danh sách tiến trình (truyền ps_text khi kiểm thử)."""
    ps = doc_tien_trinh() if ps_text is None else ps_text
    ho_tisa = [x for x in (ho_so_tisa, "trinh-duyet/ho-so", "trinh-duyet\\ho-so") if x]
    cung, mem = [], []
    thay = set()
    for dong in ps.splitlines():
        dong = dong.strip()
        if not dong:
            continue
        if any(x in dong for x in ho_tisa):
            continue                                     # trình duyệt riêng của TISA BOT
        if "grep " in dong or "tisa_chong_chen" in dong:
            continue
        for mau, mo_ta in _CUNG:
            if mau.search(dong):
                ly_do = mo_ta % _ten_ngan(dong) if "%s" in mo_ta else mo_ta
                if ly_do not in thay:
                    thay.add(ly_do)
                    cung.append(ly_do)
                break
        else:
            if _PW_MCP.search(dong) and "node " in dong:
                if _CO_NOI_CHROME.search(dong):
                    ly_do = "playwright-mcp đang nối vào Chrome đang mở (--extension hoặc --cdp-endpoint)"
                    if ly_do not in thay:
                        thay.add(ly_do)
                        cung.append(ly_do)
                else:
                    ly_do = "playwright-mcp đang chạy với trình duyệt RIÊNG (không đụng Chrome chính của anh)"
                    if ly_do not in thay:
                        thay.add(ly_do)
                        mem.append(ly_do)
            elif _CO_TU_DONG.search(dong) and _TRINH_DUYET.search(dong) and not _CO_PHU.search(dong):
                ly_do = "Một cửa sổ trình duyệt đang mở cổng gỡ lỗi hoặc cờ tự động hóa (%s)" % (_CO_TU_DONG.search(dong).group(0))
                if ly_do not in thay:
                    thay.add(ly_do)
                    cung.append(ly_do)
    return {"cung": cung, "mem": mem}


def la_trinh_duyet(ten_ung_dung: str) -> bool:
    return bool(_TRINH_DUYET.search(str(ten_ung_dung or "")))


def thong_bao(kq: dict) -> str:
    return ("BI_CHEN: Có thứ khác đang điều khiển trình duyệt nên em KHÔNG gõ (gõ lúc này dễ bị chen phím, đóng nhầm thẻ). Nguyên nhân: " + "; ".join(kq["cung"]) +
            ". Cách xử lý: tắt thứ đó (ví dụ tắt tiện ích trong Chrome), hoặc dùng cửa sổ Chrome riêng của hồ sơ cần dùng (tisa_desktop_do op=mo_chrome ho_so=<tên hồ sơ>), "
            "hoặc làm bằng Trình duyệt TISA (tisa_browser_do). Anh muốn gõ vẫn gõ: gọi lại với bo_qua_chen=true, em sẽ xin anh duyệt trước.")


# ---------------------------------------------------------------- cửa sổ Chrome riêng của một hồ sơ
def _thu_muc_chrome() -> Path:
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Google" / "Chrome"
    if sys.platform == "win32":
        return Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))) / "Google" / "Chrome" / "User Data"
    return Path.home() / ".config" / "google-chrome"


def liet_ke_ho_so(thu_muc: Path | None = None) -> list:
    """[{thu_muc: 'Profile 2', ten: 'TIÊU SANG QUẢNG CÁO', email: '...', gaia: 'Sang Tiêu Hồng', hien_thi: 'Sang (TIÊU SANG QUẢNG CÁO)'}] đọc từ Local State của Chrome (chỉ đọc).
    hien_thi là đúng chữ Chrome hiện ở menu hồ sơ (tên Google + tên hồ sơ trong ngoặc), để anh nói theo chữ nhìn thấy."""
    p = (thu_muc or _thu_muc_chrome()) / "Local State"
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        ic = (d.get("profile") or {}).get("info_cache") or {}
    except (OSError, ValueError):
        return []
    ra = []
    for k, v in ic.items():
        ten, gaia = str(v.get("name") or ""), str(v.get("gaia_name") or "")
        dau = str(v.get("gaia_given_name") or "") or (gaia.split(" ")[0] if gaia else "")
        ra.append({"thu_muc": k, "ten": ten, "email": str(v.get("user_name") or ""), "gaia": gaia,
                   "hien_thi": ("%s (%s)" % (dau, ten)) if (dau and dau != ten) else ten})
    return ra


def _chuan(t: str) -> str:
    """Chữ thường, bỏ dấu tiếng Việt, đ -> d, gộp khoảng trắng và dấu câu: 'Sang (TIÊU SANG QUẢNG CÁO)' khớp 'tieu sang quang cao'."""
    import unicodedata
    t = unicodedata.normalize("NFD", str(t or "")).replace("đ", "d").replace("Đ", "D")
    t = "".join(c for c in t if unicodedata.category(c) != "Mn").lower()
    return " ".join(re.sub(r"[^a-z0-9@._ ]+", " ", t).split())


def tim_ho_so(ten: str, ds: list | None = None) -> dict | None:
    """Tìm hồ sơ Chrome theo mã thư mục, tên hồ sơ, email hoặc đúng chữ Chrome hiện ('Sang (TIÊU SANG QUẢNG CÁO)'); không phân biệt hoa thường và dấu.
    Mơ hồ (nhiều hồ sơ cùng khớp) thì trả None để không mở nhầm."""
    q = _chuan(ten)
    if not q:
        return None
    ds = liet_ke_ho_so() if ds is None else ds

    def khoa(h):
        return [_chuan(h.get("thu_muc", "")), _chuan(h.get("ten", "")), _chuan(h.get("email", "")), _chuan(h.get("hien_thi", ""))]
    for i in (0, 1, 2, 3):                                  # khớp CHÍNH XÁC trước (mã, tên hồ sơ, email, chữ hiển thị)
        kq = [h for h in ds if khoa(h)[i] == q]
        if len(kq) == 1:
            return kq[0]
        if len(kq) > 1:
            return None if i != 3 else None
    kq = [h for h in ds if q in _chuan(h.get("ten", "")) or q in _chuan(h.get("email", "")) or q in _chuan(h.get("hien_thi", ""))]
    if len(kq) == 1:
        return kq[0]
    tu = q.split()
    kq = [h for h in ds if all(t in " ".join(khoa(h)) for t in tu)]      # đủ mọi từ anh nói
    return kq[0] if len(kq) == 1 else None


def _file_chrome() -> str:
    if sys.platform == "darwin":
        return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if sys.platform == "win32":
        for x in (os.environ.get("PROGRAMFILES", ""), os.environ.get("PROGRAMFILES(X86)", ""), os.environ.get("LOCALAPPDATA", "")):
            p = Path(x) / "Google" / "Chrome" / "Application" / "chrome.exe"
            if x and p.exists():
                return str(p)
    return "google-chrome"


def lenh_mo_chrome(ho_so_thu_muc: str, url: str = "", cua_so_moi: bool = True) -> list:
    """Dòng lệnh mở trang trong ĐÚNG hồ sơ. Gọi thẳng tệp Chrome: nếu Chrome đang chạy thì nó chuyển yêu cầu cho tiến trình đang chạy rồi thoát (không có Chrome thứ hai).
    cua_so_moi=False: mở thành TAB MỚI trong cửa sổ đang có của hồ sơ đó."""
    cmd = [_file_chrome(), "--profile-directory=%s" % ho_so_thu_muc] + (["--new-window"] if cua_so_moi else [])
    if url:
        cmd.append(url)
    return cmd


# ---------------------------------------------------------------- hồ sơ Chrome anh ĐÃ CHỌN (ghim): TISA BOT chỉ dùng đúng hồ sơ này
def doc_da_chon() -> dict | None:
    try:
        d = json.loads(TEP_GHIM.read_text(encoding="utf-8"))
        return d if d.get("thu_muc") else None
    except (OSError, ValueError):
        return None


def dat_da_chon(ten: str, ds: list | None = None) -> dict:
    """Anh (hoặc AI sau khi anh duyệt) chọn hồ sơ Chrome. Trả {"ok", "ho_so"|"loi"}."""
    h = tim_ho_so(ten, ds)
    if not h:
        return {"ok": False, "loi": "Không thấy hồ sơ Chrome \"%s\"." % ten}
    try:
        TEP_GHIM.parent.mkdir(parents=True, exist_ok=True)
        TEP_GHIM.write_text(json.dumps({"thu_muc": h["thu_muc"], "ten": h["ten"], "email": h["email"], "luc": int(time.time())}, ensure_ascii=False), encoding="utf-8")
    except OSError:
        return {"ok": False, "loi": "Không lưu được lựa chọn."}
    return {"ok": True, "ho_so": h}


def bo_da_chon() -> None:
    try:
        TEP_GHIM.unlink()
    except OSError:
        pass


def mo_chrome(ten_ho_so: str = "", url: str = "", chay: bool = True, cua_so_moi: bool = True) -> str:
    """Mở trang trong hồ sơ Chrome. Bỏ trống ten_ho_so thì dùng hồ sơ anh đã chọn. Đã chọn rồi mà xin hồ sơ KHÁC thì từ chối (không nhảy sang hồ sơ khác)."""
    ghim = doc_da_chon()
    if ghim and ten_ho_so and not (tim_ho_so(ten_ho_so, [{"thu_muc": ghim["thu_muc"], "ten": ghim["ten"], "email": ghim.get("email", "")}])):
        return ("KHOA_HO_SO: Anh đã chọn hồ sơ Chrome \"%s\" cho TISA BOT dùng, em không mở hồ sơ \"%s\" (có thể chưa đăng nhập tài khoản nào). "
                "Muốn đổi, anh chọn lại trong bảng Điều khiển máy tính của TISA BOT." % (ghim["ten"] or ghim["thu_muc"], ten_ho_so))
    if not ten_ho_so:
        if not ghim:
            return "CHUA_CHON: Anh chưa chọn hồ sơ Chrome nào cho TISA BOT dùng. Hỏi anh dùng hồ sơ nào (op=chon_chrome ho_so=<tên> sau khi anh đồng ý), hoặc dùng Trình duyệt TISA."
        ten_ho_so = ghim["thu_muc"]
    h = tim_ho_so(ten_ho_so)
    if not h:
        ds = ", ".join("%s (%s)" % (x["ten"] or x["thu_muc"], x["thu_muc"]) for x in liet_ke_ho_so()) or "không đọc được danh sách hồ sơ Chrome"
        return "LOI: không thấy hồ sơ Chrome \"%s\". Các hồ sơ có: %s." % (ten_ho_so, ds)
    if url and not re.match(r"^https?://[^\s]+$", url):
        return "LOI: url phải bắt đầu bằng http:// hoặc https://."
    cmd = lenh_mo_chrome(h["thu_muc"], url, cua_so_moi)
    if chay:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    return "Đã mở %s của hồ sơ Chrome \"%s\" (%s)%s. Chụp màn hình xem rồi thao tác trong đó." % ("cửa sổ mới" if cua_so_moi else "tab mới", h["ten"] or h["thu_muc"], h["thu_muc"], (" tại " + url) if url else "")
