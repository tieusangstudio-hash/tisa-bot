"""tisa_chuot_rieng_win.py - CON CHUỘT RIÊNG của TISA BOT trên WINDOWS (V3.20, chủ yêu cầu 18/11/2026: "không riêng macbook").

Cùng giao diện với tisa_chuot_rieng.py (macOS) để tisa_desktop dùng chung một đường:
- KHÔNG dùng SendInput / mouse_event / SetCursorPos (những lệnh đó kéo con trỏ thật của anh và giành bàn phím).
  Thay vào đó gửi THẲNG tin nhắn cửa sổ (PostMessage) tới đúng cửa sổ con ở điểm cần bấm: con trỏ thật của anh đứng yên, cửa sổ anh đang làm không bị đổi.
- Nút bấm Win32 (class Button): gửi BM_CLICK, bấm được cả khi cửa sổ nằm sau.
- Gõ chữ: WM_CHAR vào ô đang có tiêu điểm của cửa sổ đích (kể cả tiếng Việt có dấu, không qua bộ gõ).
- Chụp RIÊNG một cửa sổ kể cả khi bị che (PrintWindow với PW_RENDERFULLCONTENT).
- Con trỏ của TISA BOT: một mũi tên cam và viền cam nhẹ quanh màn hình (cửa sổ trong suốt, xuyên chuột) do một tiến trình PowerShell vẽ.

CHƯA KIỂM TRÊN WINDOWS THẬT (phát triển trên máy Mac, chỉ kiểm phần logic bằng đối tượng giả). Mọi lỗi đều rơi về chuột thật như trước, riêng con trỏ cam lỗi thì
chỉ mất phần hiển thị. Giới hạn thật: ứng dụng tự vẽ (một số game, ứng dụng UWP/Electron cũ) có thể không nhận tin nhắn chuột khi ở nền; phím tắt kiểu ctrl+c cần cửa
sổ ở trước (Windows không cho đặt trạng thái phím ctrl cho cửa sổ nền). Khi đó đổi sang chuột thật: op=chuot_che_do che_do=that.
"""
from __future__ import annotations

import ctypes
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

STATE_DIR = Path(os.getenv("TISA_STATE_DIR") or str(Path(__file__).resolve().parent))
DIR = STATE_DIR / "dieu-khien-may"
TEP_CHE_DO = DIR / "chuot-che-do.json"
TEP_VI_TRI = DIR / "chuot-ai-vi-tri.json"
TEP_DONG = DIR / "chuot-ai-dong.flag"
TEP_PID = DIR / "chuot-ai.pid"
TUOI_MUC_TIEU = 600

WIN = sys.platform == "win32"
_L = {"ok": None}
_khoa = threading.Lock()
_muc_tieu = {"pid": 0, "id": 0, "ten": "", "luc": 0.0, "con": 0}
_cursor = {"proc": None}

# tin nhắn cửa sổ
WM_MOUSEMOVE, WM_LBUTTONDOWN, WM_LBUTTONUP, WM_LBUTTONDBLCLK = 0x0200, 0x0201, 0x0202, 0x0203
WM_RBUTTONDOWN, WM_RBUTTONUP, WM_MOUSEWHEEL = 0x0204, 0x0205, 0x020A
WM_KEYDOWN, WM_KEYUP, WM_CHAR = 0x0100, 0x0101, 0x0102
BM_CLICK = 0x00F5
MK_LBUTTON, MK_RBUTTON = 0x0001, 0x0002
VK = {"enter": 0x0D, "tab": 0x09, "space": 0x20, "backspace": 0x08, "escape": 0x1B, "left": 0x25, "up": 0x26, "right": 0x27, "down": 0x28, "delete": 0x2E,
      "forwarddelete": 0x2E, "home": 0x24, "end": 0x23, "pageup": 0x21, "pagedown": 0x22, "cmd": 0x5B, "ctrl": 0x11, "alt": 0x12, "shift": 0x10}


# ---------------------------------------------------------------- chế độ (dùng chung tệp với macOS)
def che_do() -> str:
    try:
        v = json.loads(TEP_CHE_DO.read_text(encoding="utf-8")).get("che_do")
        return "that" if v == "that" else "rieng"
    except (OSError, ValueError):
        return "rieng"


def dat_che_do(v: str) -> str:
    v = "that" if str(v).lower() in ("that", "thật", "real") else "rieng"
    DIR.mkdir(parents=True, exist_ok=True)
    TEP_CHE_DO.write_text(json.dumps({"che_do": v, "luc": time.time()}), encoding="utf-8")
    return v


def dung_duoc() -> bool:
    return WIN and _nap()


# ---------------------------------------------------------------- hàm thuần (kiểm được trên mọi máy)
def lparam(x: int, y: int) -> int:
    """MAKELPARAM: hai số 16 bit có dấu (toạ độ trong cửa sổ có thể âm) gộp thành một số."""
    return ((int(y) & 0xFFFF) << 16) | (int(x) & 0xFFFF)


def don_vi_utf16(ch: str) -> list:
    """Một ký tự -> các đơn vị UTF-16 (ký tự ngoài BMP như emoji thành hai đơn vị) để gửi WM_CHAR."""
    raw = ch.encode("utf-16-le")
    return [int.from_bytes(raw[k:k + 2], "little") for k in range(0, len(raw), 2)]


def ma_phim(ten: str):
    ten = str(ten or "").lower()
    if ten in VK:
        return VK[ten]
    if len(ten) == 1 and ten.isalnum():
        return ord(ten.upper())
    return None


# ---------------------------------------------------------------- nạp thư viện Windows
def _nap() -> bool:
    if _L["ok"] is not None:
        return _L["ok"]
    _L["ok"] = False
    if not WIN:
        return False
    try:
        from ctypes import wintypes as wt
        u, k, g = ctypes.windll.user32, ctypes.windll.kernel32, ctypes.windll.gdi32
        try:
            dwm = ctypes.windll.dwmapi
        except OSError:
            dwm = None
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:  # noqa: BLE001
            try:
                u.SetProcessDPIAware()
            except Exception:  # noqa: BLE001
                pass
        ENUM = ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
        u.EnumWindows.argtypes = [ENUM, wt.LPARAM]
        u.GetWindowTextW.argtypes = [wt.HWND, wt.LPWSTR, ctypes.c_int]
        u.GetClassNameW.argtypes = [wt.HWND, wt.LPWSTR, ctypes.c_int]
        u.IsWindowVisible.argtypes = [wt.HWND]
        u.IsIconic.argtypes = [wt.HWND]
        u.GetWindowRect.argtypes = [wt.HWND, ctypes.POINTER(wt.RECT)]
        u.GetWindowThreadProcessId.argtypes = [wt.HWND, ctypes.POINTER(wt.DWORD)]
        u.GetWindowLongW.argtypes = [wt.HWND, ctypes.c_int]
        u.ScreenToClient.argtypes = [wt.HWND, ctypes.POINTER(wt.POINT)]
        u.ChildWindowFromPointEx.argtypes = [wt.HWND, wt.POINT, wt.UINT]
        u.ChildWindowFromPointEx.restype = wt.HWND
        u.PostMessageW.argtypes = [wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM]
        u.PostMessageW.restype = wt.BOOL
        u.GetGUIThreadInfo.argtypes = [wt.DWORD, ctypes.c_void_p]
        u.PrintWindow.argtypes = [wt.HWND, wt.HDC, wt.UINT]
        u.GetDC.argtypes = [wt.HWND]
        u.GetDC.restype = wt.HDC
        u.ReleaseDC.argtypes = [wt.HWND, wt.HDC]
        g.CreateCompatibleDC.argtypes = [wt.HDC]
        g.CreateCompatibleDC.restype = wt.HDC
        g.CreateCompatibleBitmap.argtypes = [wt.HDC, ctypes.c_int, ctypes.c_int]
        g.CreateCompatibleBitmap.restype = wt.HBITMAP
        g.SelectObject.argtypes = [wt.HDC, wt.HGDIOBJ]
        g.SelectObject.restype = wt.HGDIOBJ
        g.DeleteObject.argtypes = [wt.HGDIOBJ]
        g.DeleteDC.argtypes = [wt.HDC]
        k.OpenProcess.argtypes = [wt.DWORD, wt.BOOL, wt.DWORD]
        k.OpenProcess.restype = wt.HANDLE
        k.CloseHandle.argtypes = [wt.HANDLE]
        k.QueryFullProcessImageNameW.argtypes = [wt.HANDLE, wt.DWORD, wt.LPWSTR, ctypes.POINTER(wt.DWORD)]
        _L.update(u=u, k=k, g=g, dwm=dwm, wt=wt, ENUM=ENUM, ok=True)
        return True
    except Exception:  # noqa: BLE001 - thiếu thư viện nào thì coi như không dùng được, tisa_desktop tự quay về chuột thật
        _L["ok"] = False
        return False


def _ten_tien_trinh(pid: int) -> str:
    L = _L
    h = L["k"].OpenProcess(0x1000, False, int(pid))         # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return ""
    try:
        buf = ctypes.create_unicode_buffer(520)
        n = L["wt"].DWORD(520)
        if L["k"].QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(n)):
            return os.path.splitext(os.path.basename(buf.value))[0]
    finally:
        L["k"].CloseHandle(h)
    return ""


def _chu(hwnd, ham) -> str:
    buf = ctypes.create_unicode_buffer(300)
    ham(hwnd, buf, 300)
    return buf.value


def liet_ke_cua_so(tat_ca: bool = False) -> list:
    """Cửa sổ ứng dụng đang mở, TRƯỚC ra SAU (thứ tự xếp lớp): [{id (hwnd), pid, ung_dung, tieu_de, x, y, w, h, lop, alpha}]. Bỏ cửa sổ thu nhỏ, ẩn,
    cửa sổ công cụ, cửa sổ bị Windows 'cloak' (ở màn hình ảo khác) và con trỏ cam của TISA BOT."""
    if not _nap():
        return []
    L = _L
    u, wt = L["u"], L["wt"]
    ra = []
    mypid = os.getpid()

    def cb(hwnd, _lp):
        try:
            if not u.IsWindowVisible(hwnd) or u.IsIconic(hwnd):
                return True
            ex = u.GetWindowLongW(hwnd, -20) & 0xFFFFFFFF
            if ex & 0x80 and not ex & 0x40000:         # WS_EX_TOOLWINDOW mà không phải APPWINDOW
                return True
            if ex & 0x08000000 and ex & 0x20:           # NOACTIVATE + TRANSPARENT: lớp phủ xuyên chuột (kể cả của chính mình)
                return True
            if L["dwm"] is not None:
                cl = ctypes.c_int(0)
                L["dwm"].DwmGetWindowAttribute(hwnd, 14, ctypes.byref(cl), 4)     # DWMWA_CLOAKED
                if cl.value:
                    return True
            r = wt.RECT()
            if L["dwm"] is None or L["dwm"].DwmGetWindowAttribute(hwnd, 9, ctypes.byref(r), ctypes.sizeof(r)) != 0:   # DWMWA_EXTENDED_FRAME_BOUNDS
                u.GetWindowRect(hwnd, ctypes.byref(r))
            w, h = r.right - r.left, r.bottom - r.top
            if w < 20 or h < 20:
                return True
            pid = wt.DWORD()
            u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if pid.value == mypid:
                return True
            tieu = _chu(hwnd, u.GetWindowTextW)
            lop_ten = _chu(hwnd, u.GetClassNameW)
            if lop_ten in ("Shell_TrayWnd", "Progman", "WorkerW") or (not tieu and lop_ten.startswith("Windows.UI")):
                return True
            ra.append({"id": int(hwnd), "pid": int(pid.value), "ung_dung": _ten_tien_trinh(pid.value), "tieu_de": tieu, "lop_cua_so": lop_ten,
                       "x": float(r.left), "y": float(r.top), "w": float(w), "h": float(h), "lop": 0, "alpha": 1.0})
        except Exception:  # noqa: BLE001
            pass
        return True
    u.EnumWindows(L["ENUM"](cb), 0)
    return ra


def cua_so_tai(x: float, y: float):
    for w in liet_ke_cua_so():
        if w["x"] <= x < w["x"] + w["w"] and w["y"] <= y < w["y"] + w["h"]:
            return w
    return None


def tim_cua_so(ten: str):
    """Cửa sổ của ứng dụng (tên tiến trình, vd chrome, notepad) HOẶC có tiêu đề chứa `ten`; khớp tiêu đề được ưu tiên, rồi cửa sổ lớn nhất."""
    ten = (ten or "").strip().lower()
    if ten.endswith(".exe"):
        ten = ten[:-4]
    if not ten:
        return None
    ds = [w for w in liet_ke_cua_so() if w["w"] > 80 and w["h"] > 80 and (ten in (w["ung_dung"] or "").lower() or ten in (w.get("tieu_de") or "").lower())]
    ds.sort(key=lambda w: (0 if ten in (w.get("tieu_de") or "").lower() else 1, -(w["w"] * w["h"])))
    return ds[0] if ds else None


# ---------------------------------------------------------------- mục tiêu
def nho_muc_tieu(w: dict, con: int = 0) -> None:
    with _khoa:
        giu = _muc_tieu.get("con", 0) if _muc_tieu.get("id") == w["id"] else 0
        _muc_tieu.update(pid=w["pid"], id=w["id"], ten=w["ung_dung"], luc=time.time(), con=int(con or giu))


def muc_tieu() -> dict:
    with _khoa:
        if _muc_tieu["pid"] and time.time() - _muc_tieu["luc"] < TUOI_MUC_TIEU:
            return dict(_muc_tieu)
    return {}


# ---------------------------------------------------------------- gửi tin nhắn tới đúng cửa sổ con
def _cua_so_con_tai(hwnd: int, x: float, y: float):
    """Đi xuống cây cửa sổ con tới cửa sổ SÂU NHẤT chứa điểm màn hình (x, y). Trả (hwnd_con, x_trong_con, y_trong_con)."""
    L = _L
    u, wt = L["u"], L["wt"]
    cur = hwnd
    for _ in range(12):
        pt = wt.POINT(int(x), int(y))
        u.ScreenToClient(cur, ctypes.byref(pt))
        con = u.ChildWindowFromPointEx(cur, wt.POINT(pt.x, pt.y), 0x1 | 0x2 | 0x4)       # bỏ ẩn, bỏ bị khóa, bỏ trong suốt
        if not con or int(con) == int(cur):
            return int(cur), pt.x, pt.y
        cur = con
    pt = wt.POINT(int(x), int(y))
    u.ScreenToClient(cur, ctypes.byref(pt))
    return int(cur), pt.x, pt.y


def _gui(hwnd, msg, wp=0, lp=0) -> bool:
    return bool(_L["u"].PostMessageW(hwnd, msg, wp, lp))


def bam(w: dict, x: float, y: float, nut: str = "left", lan: int = 1, uu_tien_axpress: bool = True) -> str:
    """Bấm tại toạ độ màn hình (x, y) trong cửa sổ w KHÔNG động tới con trỏ thật. Trả mô tả cách đã bấm."""
    con, cx, cy = _cua_so_con_tai(w["id"], x, y)
    nho_muc_tieu(w, con)
    hien_con_tro(x, y, "bam")
    if uu_tien_axpress and nut == "left" and lan == 1 and _chu(con, _L["u"].GetClassNameW).lower() == "button":
        _gui(con, BM_CLICK, 0, 0)
        return "BM_CLICK, bấm đúng nút Win32"
    lp = lparam(cx, cy)
    phai = nut == "right"
    xuong, len_, mk = (WM_RBUTTONDOWN, WM_RBUTTONUP, MK_RBUTTON) if phai else (WM_LBUTTONDOWN, WM_LBUTTONUP, MK_LBUTTON)
    _gui(con, WM_MOUSEMOVE, 0, lp)
    time.sleep(0.03)
    for i in range(1, lan + 1):
        _gui(con, WM_LBUTTONDBLCLK if (i == 2 and not phai) else xuong, mk, lp)
        time.sleep(0.04)
        _gui(con, len_, 0, lp)
        time.sleep(0.05)
    return "tin nhắn chuột gửi thẳng vào %s" % (w.get("ung_dung") or "cửa sổ")


def keo(w: dict, x: float, y: float, x2: float, y2: float) -> None:
    con, cx, cy = _cua_so_con_tai(w["id"], x, y)
    nho_muc_tieu(w, con)
    hien_con_tro(x, y, "keo")
    _gui(con, WM_MOUSEMOVE, 0, lparam(cx, cy))
    _gui(con, WM_LBUTTONDOWN, MK_LBUTTON, lparam(cx, cy))
    for i in range(1, 9):
        xi, yi = cx + (x2 - x) * i / 8, cy + (y2 - y) * i / 8
        _gui(con, WM_MOUSEMOVE, MK_LBUTTON, lparam(int(xi), int(yi)))
        hien_con_tro(x + (x2 - x) * i / 8, y + (y2 - y) * i / 8, "keo")
        time.sleep(0.03)
    _gui(con, WM_LBUTTONUP, 0, lparam(int(cx + (x2 - x)), int(cy + (y2 - y))))


def cuon(w: dict, x: float, y: float, dy: int) -> None:
    con, _cx, _cy = _cua_so_con_tai(w["id"], x, y)
    nho_muc_tieu(w, con)
    hien_con_tro(x, y, "cuon")
    delta = int(-dy * 120) & 0xFFFF
    _gui(con, WM_MOUSEWHEEL, (delta << 16), lparam(int(x), int(y)))       # cuộn dùng toạ độ MÀN HÌNH


def _hwnd_go(pid: int) -> int:
    """Cửa sổ nhận chữ: ô đang có tiêu điểm của luồng cửa sổ đích, hoặc cửa sổ con vừa bấm, hoặc cửa sổ chính."""
    mt = muc_tieu()
    top = int(mt.get("id") or 0) if mt and (not pid or mt.get("pid") == pid) else 0
    if not top:
        w = next((c for c in liet_ke_cua_so() if c["pid"] == pid), None)
        top = w["id"] if w else 0
    if not top:
        return 0
    try:
        L = _L
        wt = L["wt"]

        class GTI(ctypes.Structure):
            _fields_ = [("cbSize", wt.DWORD), ("flags", wt.DWORD), ("hwndActive", wt.HWND), ("hwndFocus", wt.HWND), ("hwndCapture", wt.HWND),
                        ("hwndMenuOwner", wt.HWND), ("hwndMoveSize", wt.HWND), ("hwndCaret", wt.HWND), ("rcCaret", wt.RECT)]
        gi = GTI()
        gi.cbSize = ctypes.sizeof(GTI)
        tid = L["u"].GetWindowThreadProcessId(top, None)
        if L["u"].GetGUIThreadInfo(tid, ctypes.byref(gi)) and gi.hwndFocus:
            return int(gi.hwndFocus)
    except Exception:  # noqa: BLE001
        pass
    return int(mt.get("con") or top) if mt else top


def go_chu(pid: int, text: str, tre: float = 0.012) -> None:
    """Gõ chữ vào cửa sổ đích (WM_CHAR, không qua bộ gõ nên tiếng Việt có dấu giữ nguyên)."""
    hw = _hwnd_go(pid)
    if not hw:
        raise RuntimeError("không thấy cửa sổ để gõ")
    for ch in text:
        if ch == "\n":
            _gui(hw, WM_KEYDOWN, 0x0D, 0x001C0001)
            _gui(hw, WM_CHAR, 0x0D, 0x001C0001)
            _gui(hw, WM_KEYUP, 0x0D, 0xC01C0001)
        else:
            for dv in don_vi_utf16(ch):
                _gui(hw, WM_CHAR, dv, 1)
        time.sleep(tre)


def phim(pid: int, vk: int, flags: int = 0, xuong: bool = True) -> None:
    hw = _hwnd_go(pid)
    if not hw:
        raise RuntimeError("không thấy cửa sổ để nhấn phím")
    scan = _L["u"].MapVirtualKeyW(vk, 0) if hasattr(_L["u"], "MapVirtualKeyW") else 0
    lp = 1 | (scan << 16) | (0 if xuong else (3 << 30))
    _gui(hw, WM_KEYDOWN if xuong else WM_KEYUP, vk, lp)


def nhan_phim_ten(pid: int, mods, phim_ten: str) -> None:
    vk = ma_phim(phim_ten)
    if vk is None:
        raise RuntimeError("Phím không biết: %s" % phim_ten)
    ms = [VK[m] for m in mods if m in VK]
    for m in ms:
        phim(pid, m, 0, True)
    phim(pid, vk, 0, True)
    time.sleep(0.03)
    phim(pid, vk, 0, False)
    for m in reversed(ms):
        phim(pid, m, 0, False)


# ---------------------------------------------------------------- chụp một cửa sổ kể cả khi bị che
def chup_cua_so_id(hwnd: int, tep: Path) -> bool:
    if not _nap():
        return False
    try:
        from PIL import Image
        L = _L
        u, g, wt = L["u"], L["g"], L["wt"]
        r = wt.RECT()
        u.GetWindowRect(hwnd, ctypes.byref(r))
        w, h = r.right - r.left, r.bottom - r.top
        if w < 10 or h < 10:
            return False
        sdc = u.GetDC(None)
        mdc = g.CreateCompatibleDC(sdc)
        bmp = g.CreateCompatibleBitmap(sdc, w, h)
        cu = g.SelectObject(mdc, bmp)
        ok = bool(u.PrintWindow(hwnd, mdc, 2))               # PW_RENDERFULLCONTENT
        buf = ctypes.create_string_buffer(w * h * 4)

        class BIH(ctypes.Structure):
            _fields_ = [("biSize", wt.DWORD), ("biWidth", ctypes.c_long), ("biHeight", ctypes.c_long), ("biPlanes", wt.WORD), ("biBitCount", wt.WORD),
                        ("biCompression", wt.DWORD), ("biSizeImage", wt.DWORD), ("a", ctypes.c_long), ("b", ctypes.c_long), ("c", wt.DWORD), ("d", wt.DWORD)]
        bi = BIH(40, w, -h, 1, 32, 0, 0, 0, 0, 0, 0)
        g.GetDIBits.argtypes = [wt.HDC, wt.HBITMAP, wt.UINT, wt.UINT, ctypes.c_void_p, ctypes.c_void_p, wt.UINT]
        n = g.GetDIBits(mdc, bmp, 0, h, buf, ctypes.byref(bi), 0)
        g.SelectObject(mdc, cu)
        g.DeleteObject(bmp)
        g.DeleteDC(mdc)
        u.ReleaseDC(None, sdc)
        if not ok or not n:
            return False
        im = Image.frombuffer("RGBA", (w, h), buf, "raw", "BGRA", 0, 1).convert("RGB")
        e = wt.RECT()
        if L["dwm"] is not None and L["dwm"].DwmGetWindowAttribute(hwnd, 9, ctypes.byref(e), ctypes.sizeof(e)) == 0:
            im = im.crop((max(0, e.left - r.left), max(0, e.top - r.top), min(w, e.right - r.left), min(h, e.bottom - r.top)))     # bỏ viền vô hình
        if im.getbbox() is None or im.getextrema() == ((0, 0), (0, 0), (0, 0)):
            return False
        im.save(str(tep), "JPEG", quality=82)
        return tep.exists() and tep.stat().st_size > 0
    except Exception:  # noqa: BLE001
        return False


# ---------------------------------------------------------------- con trỏ cam và viền cam (PowerShell, cửa sổ trong suốt xuyên chuột)
_PS = r'''
$ErrorActionPreference = "Stop"
Add-Type -ReferencedAssemblies System.Windows.Forms,System.Drawing -TypeDefinition @"
using System; using System.Windows.Forms; using System.Drawing; using System.Drawing.Drawing2D; using System.Runtime.InteropServices;
public class TisaDpi { [DllImport("user32.dll")] public static extern bool SetProcessDPIAware(); }
public class TisaOv : Form {
  public TisaOv() { FormBorderStyle = FormBorderStyle.None; ShowInTaskbar = false; StartPosition = FormStartPosition.Manual; TopMost = true; }
  protected override CreateParams CreateParams { get { CreateParams cp = base.CreateParams; cp.ExStyle |= 0x80 | 0x20 | 0x08000000 | 0x80000; return cp; } }
  protected override bool ShowWithoutActivation { get { return true; } }
}
public class TisaMui : TisaOv {
  protected override void OnPaint(PaintEventArgs e) {
    e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
    Point[] p = new Point[] { new Point(3,3), new Point(3,32), new Point(11,25), new Point(17,38), new Point(22,36), new Point(16,23), new Point(28,23) };
    using (var b = new SolidBrush(Color.FromArgb(255,107,53))) e.Graphics.FillPolygon(b, p);
    using (var pen = new Pen(Color.White, 2)) e.Graphics.DrawPolygon(pen, p);
  }
}
"@
[void][TisaDpi]::SetProcessDPIAware()
$VT = "__VT__"; $DONG = "__DONG__"
$scr = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$N = 12; $B = 4
$vien = @()
for ($i = 0; $i -lt $N; $i++) {
  $f = New-Object TisaOv; $f.Bounds = $scr; $f.BackColor = [System.Drawing.Color]::FromArgb(255,107,53)
  $in = [System.Drawing.Rectangle]::new($scr.X + ($i+1)*$B, $scr.Y + ($i+1)*$B, $scr.Width - 2*($i+1)*$B, $scr.Height - 2*($i+1)*$B)
  $rg = New-Object System.Drawing.Region([System.Drawing.Rectangle]::new($scr.X, $scr.Y, $scr.Width, $scr.Height)); $rg.Exclude($in); $f.Region = $rg
  $f.Tag = [double](0.55 * [Math]::Pow(1 - $i / $N, 1.7)); $f.Opacity = 0; $f.Show(); $vien += $f
}
$cur = New-Object TisaMui; $cur.Size = New-Object System.Drawing.Size(40,40); $cur.BackColor = [System.Drawing.Color]::Magenta; $cur.TransparencyKey = [System.Drawing.Color]::Magenta; $cur.Opacity = 0; $cur.Show()
$st = @{ x = -300.0; y = -300.0; mx = -300.0; my = -300.0; hien = 0; luc = 0.0; aV = 0.0; aC = 0.0 }
$t0 = [DateTime]::UtcNow
$tm = New-Object System.Windows.Forms.Timer; $tm.Interval = 33
$tm.Add_Tick({
  if (Test-Path $DONG) { $tm.Stop(); [System.Windows.Forms.Application]::Exit(); return }
  try { $j = Get-Content -Raw -Path $VT | ConvertFrom-Json; $st.mx = [double]$j.x; $st.my = [double]$j.y; $st.hien = [int]$j.hien; $st.luc = [double]$j.luc } catch {}
  $now = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() / 1000.0
  $tuoi = $now - $st.luc
  if ($st.luc -gt 0 -and $tuoi -gt 900) { $tm.Stop(); [System.Windows.Forms.Application]::Exit(); return }
  $bat = ($st.hien -gt 0 -and $tuoi -lt 10); $batC = ($st.hien -gt 0 -and $tuoi -lt 6)
  $st.aV += ($(if ($bat) {1.0} else {0.0}) - $st.aV) * 0.1
  $st.aC += ($(if ($batC) {1.0} else {0.0}) - $st.aC) * 0.2
  $nhip = 0.82 + 0.18 * [Math]::Sin(([DateTime]::UtcNow - $t0).TotalMilliseconds / 450.0)
  foreach ($f in $vien) { $f.Opacity = [Math]::Min(1.0, [Math]::Max(0.0, $f.Tag * $st.aV * $nhip)) }
  $st.x += ($st.mx - $st.x) * 0.35; $st.y += ($st.my - $st.y) * 0.35
  $cur.Opacity = [Math]::Min(1.0, [Math]::Max(0.0, $st.aC))
  $cur.Location = New-Object System.Drawing.Point([int]($st.x - 3), [int]($st.y - 3))
})
$tm.Start()
[System.Windows.Forms.Application]::Run()
'''


def _con_tro_dang_chay() -> bool:
    p = _cursor["proc"]
    if p is not None and p.poll() is None:
        return True
    try:
        pid = int(TEP_PID.read_text().strip())
        r = subprocess.run(["tasklist", "/FI", "PID eq %d" % pid, "/FO", "CSV", "/NH"], capture_output=True, text=True, timeout=8)
        return str(pid) in (r.stdout or "")
    except (OSError, ValueError, subprocess.SubprocessError):
        return False


def _tao_con_tro() -> bool:
    if not WIN:
        return False
    if _con_tro_dang_chay():
        return True
    DIR.mkdir(parents=True, exist_ok=True)
    try:
        TEP_DONG.unlink()
    except OSError:
        pass
    tep = DIR / "chuot-ai.ps1"
    tep.write_text(_PS.replace("__VT__", str(TEP_VI_TRI)).replace("__DONG__", str(TEP_DONG)), encoding="utf-8-sig")
    try:
        _cursor["proc"] = subprocess.Popen(["powershell", "-NoProfile", "-NonInteractive", "-WindowStyle", "Hidden", "-ExecutionPolicy", "Bypass", "-File", str(tep)],
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, creationflags=0x08000000)    # CREATE_NO_WINDOW
        TEP_PID.write_text(str(_cursor["proc"].pid), encoding="utf-8")
        return True
    except OSError:
        return False


def hien_con_tro(x: float, y: float, nhan: str = "") -> None:
    try:
        if not _tao_con_tro():
            return
        TEP_VI_TRI.write_text(json.dumps({"x": float(x), "y": float(y), "hien": 1, "luc": time.time()}), encoding="utf-8")
    except (OSError, ValueError):
        pass


def giau_con_tro() -> None:
    try:
        TEP_VI_TRI.write_text(json.dumps({"x": -300, "y": -300, "hien": 0, "luc": time.time()}), encoding="utf-8")
    except OSError:
        pass


def tat_con_tro() -> None:
    try:
        DIR.mkdir(parents=True, exist_ok=True)
        TEP_DONG.write_text("1", encoding="utf-8")
    except OSError:
        pass
    p = _cursor["proc"]
    _cursor["proc"] = None
    if p is not None:
        try:
            p.wait(timeout=3)
        except Exception:  # noqa: BLE001
            try:
                p.kill()
            except OSError:
                pass
