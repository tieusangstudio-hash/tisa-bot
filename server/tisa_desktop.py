"""tisa_desktop.py - Điều khiển máy tính (V2.99): AI Agent dùng chính máy của người dùng như người thật.

Mở màn hình, nhìn màn hình, di chuột, bấm, gõ, dùng phím tắt, mở ứng dụng và tệp, chuyển cửa sổ. Dùng khi việc cần thao tác trên máy
(tìm thư mục, bấm vào tệp, dùng ứng dụng không có MCP hay API). Chạy ngay trên máy chạy TISA BOT (macOS và Windows), không tải lên đâu.

Cách làm: không cài thêm gì. macOS dùng CoreGraphics qua ctypes (chuột, phím, gõ cả tiếng Việt), `screencapture`, `lsappinfo`, `open`.
Windows dùng user32 qua ctypes (SendInput), Pillow chụp màn hình, PowerShell cho danh sách cửa sổ. Hai công cụ cho hub:
  - tisa_desktop_look (chỉ xem): screenshot, windows, front, permissions, status
  - tisa_desktop_do   (thao tác): click, double_click, right_click, move, drag, scroll, type, key, open_app, open_path, focus_app, quit_app, wait

Ba mức tự động (anh chọn): hỏi mọi bước, hỏi bước quan trọng (mặc định), toàn quyền.

Rào chắn luôn có ở MỌI mức:
  - KHÔNG XÓA: không phím xóa, không Dọn thùng rác, không menu chuột phải hay kéo thả trong Finder/Explorer, không lệnh xóa gõ vào Terminal. Chỉ khi anh bật
    công tắc "Cho phép AI xóa tệp" (có hạn giờ, tự tắt) thì mới được. Lưu ý: không chặn được 100% mọi cách (ví dụ kéo thả vào Thùng rác ở Dock); công cụ
    khác của TISA BOT (chạy lệnh) có luật quyền riêng.
  - Mật khẩu, khóa, ví, ngân hàng: cửa sổ đăng nhập hệ thống, quản lý mật khẩu, ví coin, ứng dụng ngân hàng: AI không bấm, không gõ, người dùng tự làm.
  - Nút Dừng AI ngay; đưa chuột về góc trên trái màn hình cũng dừng ngay. Nhật ký từng bước.
"""
from __future__ import annotations

import asyncio
import ctypes
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
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

try:
    import tisa_browser as B       # dùng chung nhật ký và thẻ xin duyệt với Trình duyệt TISA
except Exception:  # noqa: BLE001
    B = None

DIR = STATE_DIR / "dieu-khien-may"
ANH = DIR / "anh"
TEP_MUC = DIR / "muc.json"
MUC = ("tat", "hoi_het", "quan_trong", "toan_quyen")
_khoa = threading.RLock()
_tt = {"muc": "quan_trong", "muc_den": 0.0, "cho_xoa_den": 0.0, "dung": False, "lan_cuoi": 0.0}
DAI_CHO_XOA = 15 * 60

# ---------------------------------------------------------------- luật phân loại
_APP_CHAN = re.compile(r"securityagent|coreautha|loginwindow|keychain|1password|bitwarden|lastpass|keepass|dashlane|metamask|exodus|ledger|trezor|binance|"
                       r"trustwallet|authenticator|momo|zalopay|vcb|vietcombank|techcombank|mbbank|bidv|tpbank|vpbank|banking|ngân hàng|ví điện tử|credential", re.I)
_APP_TEP = re.compile(r"^(finder|explorer|file explorer|windows explorer|files|nautilus|dolphin|thunar)$", re.I)
_APP_LENH = re.compile(r"terminal|iterm|warp|powershell|^cmd|command prompt|windows terminal|konsole|hyper|ghostty|kitty|alacritty|wezterm|pwsh|conhost", re.I)
_APP_TIN_NHAN = re.compile(r"messages|^mail$|outlook|zalo|telegram|slack|whatsapp|messenger|discord|teams|skype|viber|signal|^line$|facebook", re.I)
_APP_HE_THONG = re.compile(r"system settings|system preferences|cài đặt|^settings$|control panel|regedit|task manager|activity monitor|disk utility|installer|registry", re.I)
_LENH_XOA = re.compile(r"(^|[\s;&|(])(rm|rmdir|del|erase|rd|shred|unlink|trash|rimraf|remove-item|ri|format|mkfs|dd)(\s|$)|sudo\s+rm|find\s+.*-delete|git\s+clean|git\s+reset\s+--hard|truncate|diskutil\s+(erase|secure)", re.I)
_DUOI_NGUY_HIEM = (".dmg", ".pkg", ".exe", ".msi", ".bat", ".cmd", ".ps1", ".sh", ".command", ".scr", ".vbs", ".jar", ".app.zip", ".apk")
_PHIM_XOA = {"backspace", "delete", "forwarddelete", "del"}
_ten_phim = {"cmd": "cmd", "command": "cmd", "meta": "cmd", "win": "cmd", "windows": "cmd", "super": "cmd", "ctrl": "ctrl", "control": "ctrl", "alt": "alt", "option": "alt", "opt": "alt",
             "shift": "shift", "return": "enter", "enter": "enter", "esc": "escape", "escape": "escape", "del": "delete", "backspace": "backspace", "space": "space", "tab": "tab",
             "up": "up", "down": "down", "left": "left", "right": "right", "pageup": "pageup", "pagedown": "pagedown", "home": "home", "end": "end", "forwarddelete": "forwarddelete"}


def _tach_phim(combo: str) -> tuple[set, str]:
    bo = [x.strip().lower() for x in re.split(r"\+", str(combo or "")) if x.strip()]
    mods, phim = set(), ""
    for x in bo:
        n = _ten_phim.get(x, x)
        if n in ("cmd", "ctrl", "alt", "shift"):
            mods.add(n)
        else:
            phim = n
    return mods, phim


# ---------------------------------------------------------------- mức tự động
def _nap() -> None:
    try:
        d = json.loads(TEP_MUC.read_text(encoding="utf-8"))
        if d.get("muc") in MUC:
            _tt["muc"], _tt["muc_den"] = d["muc"], float(d.get("muc_den") or 0)
        _tt["cho_xoa_den"] = float(d.get("cho_xoa_den") or 0)
    except (OSError, ValueError):
        pass


def _luu() -> None:
    try:
        DIR.mkdir(parents=True, exist_ok=True)
        TEP_MUC.write_text(json.dumps({"muc": _tt["muc"], "muc_den": _tt["muc_den"], "cho_xoa_den": _tt["cho_xoa_den"]}), encoding="utf-8")
    except OSError:
        pass


def muc_hien_tai() -> str:
    with _khoa:
        if _tt["muc"] == "toan_quyen" and _tt["muc_den"] and time.time() > _tt["muc_den"]:
            _tt["muc"], _tt["muc_den"] = "quan_trong", 0.0
            _luu()
            _nk("muc", "hết hạn", "Toàn quyền hết hạn, về mức Hỏi bước quan trọng")
        return _tt["muc"]


def dat_muc(muc: str, phut: int = 0) -> dict:
    if muc not in MUC:
        return {"ok": False, "loi": "Mức không hợp lệ."}
    with _khoa:
        _tt["muc"] = muc
        _tt["muc_den"] = (time.time() + max(1, int(phut)) * 60) if (muc == "toan_quyen" and phut) else 0.0
        _luu()
    _nk("muc", "đã đổi", "Mức tự động điều khiển máy: %s" % {"tat": "Không cho AI dùng máy", "hoi_het": "Hỏi mọi bước", "quan_trong": "Hỏi bước quan trọng", "toan_quyen": "Toàn quyền"}[muc])
    return {"ok": True}


def cho_xoa_con() -> int:
    """Số giây còn lại của quyền xóa (0 = đang tắt)."""
    with _khoa:
        return max(0, int(_tt["cho_xoa_den"] - time.time())) if _tt["cho_xoa_den"] else 0


def dat_cho_xoa(phut: int) -> dict:
    with _khoa:
        _tt["cho_xoa_den"] = (time.time() + max(1, min(int(phut), 120)) * 60) if phut else 0.0
        _luu()
    _nk("cho_xoa", "bật" if phut else "tắt", "Quyền cho AI xóa tệp: %s" % (("bật %d phút" % phut) if phut else "tắt"))
    return {"ok": True}


def _nk(op: str, kq: str, mo_ta: str, ten: str = "") -> None:
    if B:
        B._ghi_nk({"op": "may_" + op, "ket_qua": kq, "mo_ta": mo_ta[:200], "ten": ten[:80], "host": "Máy tính"})


# ---------------------------------------------------------------- lớp macOS
_DIR_LENH_MAC = ("/usr/sbin", "/usr/bin", "/bin", "/sbin", "/System/Library/CoreServices", "/usr/local/bin", "/opt/homebrew/bin")


def _lenh_mac(ten: str) -> str:
    """Tên lệnh macOS -> đường dẫn đầy đủ (không phụ thuộc PATH của tiến trình, vì launchd chỉ cho PATH ngắn)."""
    if "/" in ten:
        return ten
    for d in _DIR_LENH_MAC:
        p = os.path.join(d, ten)
        if os.access(p, os.X_OK):
            return p
    return ten


def _moi_truong_mac() -> dict:
    e = dict(os.environ)
    cu = [x for x in str(e.get("PATH", "")).split(":") if x]
    e["PATH"] = ":".join(cu + [d for d in _DIR_LENH_MAC if d not in cu])
    return e


class _Mac:
    ten = "macOS"
    KC = {"a": 0, "s": 1, "d": 2, "f": 3, "h": 4, "g": 5, "z": 6, "x": 7, "c": 8, "v": 9, "b": 11, "q": 12, "w": 13, "e": 14, "r": 15, "y": 16, "t": 17, "1": 18, "2": 19,
          "3": 20, "4": 21, "6": 22, "5": 23, "=": 24, "9": 25, "7": 26, "-": 27, "8": 28, "0": 29, "]": 30, "o": 31, "u": 32, "[": 33, "i": 34, "p": 35, "l": 37, "j": 38,
          "'": 39, "k": 40, ";": 41, "\\": 42, ",": 43, "/": 44, "n": 45, "m": 46, ".": 47, "enter": 36, "tab": 48, "space": 49, "backspace": 51, "escape": 53, "left": 123,
          "right": 124, "down": 125, "up": 126, "delete": 117, "forwarddelete": 117, "home": 115, "end": 119, "pageup": 116, "pagedown": 121,
          "f1": 122, "f2": 120, "f3": 99, "f4": 118, "f5": 96, "f6": 97, "f7": 98, "f8": 100, "f9": 101, "f10": 109, "f11": 103, "f12": 111}
    FL = {"cmd": 0x100000, "shift": 0x20000, "alt": 0x80000, "ctrl": 0x40000}

    def __init__(self):
        self.cg = None
        try:
            c = ctypes.CDLL("/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices")

            class P(ctypes.Structure):
                _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]

            class S(ctypes.Structure):
                _fields_ = [("w", ctypes.c_double), ("h", ctypes.c_double)]

            class R(ctypes.Structure):
                _fields_ = [("o", P), ("s", S)]
            self.P, self.R = P, R
            c.CGEventCreateMouseEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint32, P, ctypes.c_uint32]
            c.CGEventCreateMouseEvent.restype = ctypes.c_void_p
            c.CGEventPost.argtypes = [ctypes.c_uint32, ctypes.c_void_p]
            c.CGEventSetIntegerValueField.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int64]
            c.CGEventCreate.argtypes = [ctypes.c_void_p]
            c.CGEventCreate.restype = ctypes.c_void_p
            c.CGEventGetLocation.argtypes = [ctypes.c_void_p]
            c.CGEventGetLocation.restype = P
            c.CGEventCreateScrollWheelEvent2.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
            c.CGEventCreateScrollWheelEvent2.restype = ctypes.c_void_p
            c.CGEventCreateKeyboardEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint16, ctypes.c_bool]
            c.CGEventCreateKeyboardEvent.restype = ctypes.c_void_p
            c.CGEventKeyboardSetUnicodeString.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(ctypes.c_uint16)]
            c.CGEventSetFlags.argtypes = [ctypes.c_void_p, ctypes.c_uint64]
            c.CGMainDisplayID.restype = ctypes.c_uint32
            c.CGDisplayBounds.argtypes = [ctypes.c_uint32]
            c.CGDisplayBounds.restype = R
            try:
                c.AXIsProcessTrusted.restype = ctypes.c_bool
            except AttributeError:
                pass
            self.cg = c
            self.cf = ctypes.CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
            self.cf.CFRelease.argtypes = [ctypes.c_void_p]
        except OSError:
            self.cg = None

    def _post(self, e):
        self.cg.CGEventPost(0, e)
        self.cf.CFRelease(e)

    def kich_thuoc(self):
        r = self.cg.CGDisplayBounds(self.cg.CGMainDisplayID())
        return int(r.s.w), int(r.s.h)

    def vi_tri_chuot(self):
        e = self.cg.CGEventCreate(None)
        p = self.cg.CGEventGetLocation(e)
        self.cf.CFRelease(e)
        return int(p.x), int(p.y)

    def _chuot(self, tipo, x, y, nut=0, lan=1):
        e = self.cg.CGEventCreateMouseEvent(None, tipo, self.P(x, y), nut)
        self.cg.CGEventSetIntegerValueField(e, 1, lan)
        self._post(e)

    def di_chuyen(self, x, y):
        try:
            self.cg.CGWarpMouseCursorPosition.argtypes = [self.P]
            self.cg.CGWarpMouseCursorPosition(self.P(x, y))
        except Exception:  # noqa: BLE001
            pass
        self._chuot(5, x, y)

    def bam(self, x, y, nut="left", lan=1):
        self.di_chuyen(x, y)
        time.sleep(0.12)
        xuong, len_, k = (3, 4, 1) if nut == "right" else (1, 2, 0)
        for i in range(1, lan + 1):
            self._chuot(xuong, x, y, k, i)
            time.sleep(0.04)
            self._chuot(len_, x, y, k, i)
            time.sleep(0.06)

    def keo(self, x, y, x2, y2):
        self.di_chuyen(x, y)
        time.sleep(0.1)
        self._chuot(1, x, y)
        for i in range(1, 9):
            self._chuot(6, x + (x2 - x) * i // 8, y + (y2 - y) * i // 8)
            time.sleep(0.03)
        self._chuot(2, x2, y2)

    def cuon(self, dy, x=None, y=None):
        if x is not None and y is not None:
            self.di_chuyen(x, y)
        e = self.cg.CGEventCreateScrollWheelEvent2(None, 1, 1, int(-dy), 0, 0)
        self._post(e)

    def _phim(self, ma, flags=0, xuong=True):
        e = self.cg.CGEventCreateKeyboardEvent(None, ma, xuong)
        if flags:
            self.cg.CGEventSetFlags(e, flags)
        self._post(e)

    _SHIFT = {"+": "=", "*": "8", "(": "9", ")": "0", "_": "-", '"': "'", ":": ";", "<": ",", ">": ".", "?": "/", "!": "1", "@": "2", "#": "3", "$": "4", "%": "5", "^": "6", "&": "7", "|": "\\", "{": "[", "}": "]"}

    def go(self, text, kieu="chu"):
        for ch in text:
            if ch == "\n":
                self._phim(36, 0, True)
                self._phim(36, 0, False)
                continue
            if kieu == "phim":                   # gõ từng PHÍM thật (máy tính bỏ túi, trò chơi, ứng dụng ăn phím tắt)
                base, fl = None, 0
                if ch.lower() in self.KC and len(ch) == 1:
                    base, fl = ch.lower(), (self.FL["shift"] if ch.isupper() else 0)
                elif ch in self._SHIFT:
                    base, fl = self._SHIFT[ch], self.FL["shift"]
                if base is not None:
                    self._phim(self.KC[base], fl, True)
                    self._phim(self.KC[base], fl, False)
                    time.sleep(0.03)
                    continue
            u = ch.encode("utf-16-le")
            arr = (ctypes.c_uint16 * (len(u) // 2)).from_buffer_copy(u)
            for xuong in (True, False):
                e = self.cg.CGEventCreateKeyboardEvent(None, 0, xuong)
                self.cg.CGEventKeyboardSetUnicodeString(e, len(arr), arr)
                self._post(e)
            time.sleep(0.012)

    def nhan_phim(self, mods, phim):
        ma = self.KC.get(phim)
        if ma is None:
            raise RuntimeError("Phím không biết: %s" % phim)
        flags = 0
        for m in mods:
            flags |= self.FL[m]
        self._phim(ma, flags, True)
        time.sleep(0.04)
        self._phim(ma, flags, False)

    def _chay(self, cmd, timeout=8):
        # TISA BOT chạy dưới launchd nên PATH rất ngắn (không có /usr/sbin, nơi chứa screencapture): gọi bằng đường dẫn đầy đủ.
        cmd = [_lenh_mac(cmd[0])] + list(cmd[1:])
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=_moi_truong_mac())
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()

    def chup(self, duong_dan):
        w, h = self.kich_thuoc()
        rc, _, err = self._chay(["screencapture", "-x", "-m", "-t", "jpg", str(duong_dan)], 15)
        if rc != 0 or not Path(duong_dan).exists():
            raise RuntimeError("Chụp màn hình lỗi: %s" % (err or "chưa cấp quyền Ghi màn hình"))
        self._chay(["sips", "--resampleHeightWidth", str(h), str(w), str(duong_dan)], 15)   # về đúng toạ độ điểm (không bị nhân đôi ở màn Retina)
        return w, h

    def ung_dung_truoc(self):
        rc, out, _ = self._chay(["lsappinfo", "front"], 4)
        asn = out.strip()
        if rc != 0 or not asn:
            return ""
        rc, out, _ = self._chay(["lsappinfo", "info", "-only", "name", asn], 4)
        m = re.search(r'"LSDisplayName"\s*=\s*"(.+?)"', out)
        return m.group(1) if m else ""

    def liet_ke_ung_dung(self):
        rc, out, _ = self._chay(["lsappinfo", "list"], 6)
        ds = []
        for blk in re.split(r"(?m)^\s*\d+\)\s", out)[1:]:
            m = re.match(r'"(.+?)"\s', blk)
            if m and 'type="Foreground"' in blk:
                ds.append(m.group(1))
        return ds

    def tieu_de_cua_so(self):
        rc, out, _ = self._chay(["osascript", "-e", 'tell application "System Events" to get name of every window of (first process whose frontmost is true)'], 4)
        return out if rc == 0 else ""

    def mo_ung_dung(self, ten):
        rc, _, err = self._chay(["open", "-a", ten], 15)
        if rc != 0:
            bid = self._bundle_theo_ten(ten)
            rc, _, err = self._chay(["open", "-b", bid], 15) if bid else (rc, "", err)
        if rc != 0:
            raise RuntimeError("Không mở được ứng dụng %s: %s (dùng tên tiếng Anh của ứng dụng, ví dụ Calculator, hoặc op=windows để xem tên đang chạy)" % (ten, err[:120]))

    def mo_duong_dan(self, p):
        rc, _, err = self._chay(["open", p], 15)
        if rc != 0:
            raise RuntimeError("Không mở được %s: %s" % (p, err[:120]))

    def _bundle_theo_ten(self, ten):
        """Tên hiển thị tiếng Việt (ví dụ "Máy tính") không dùng được với open -a: tra mã gói của ứng dụng đang chạy rồi mở theo mã."""
        rc, out, _ = self._chay(["lsappinfo", "list"], 6)
        t = ten.strip().lower()
        for blk in re.split(r"(?m)^\s*\d+\)\s", out)[1:]:
            m = re.match(r'"(.+?)"\s', blk)
            b = re.search(r'bundleID="(.+?)"', blk)
            if m and b and m.group(1).lower() == t:
                return b.group(1)
        return ""

    def chuyen_ung_dung(self, ten):
        bid = self._bundle_theo_ten(ten)
        rc, _, err = self._chay(["open", "-b", bid] if bid else ["open", "-a", ten], 10)
        if rc != 0:
            raise RuntimeError("Không chuyển được sang %s: %s" % (ten, err[:120]))

    def thoat_ung_dung(self, ten):
        self.chuyen_ung_dung(ten)       # thoát bằng Cmd+Q của chính ứng dụng: nếu có tệp chưa lưu, ứng dụng tự hỏi lưu
        time.sleep(0.6)
        self.nhan_phim({"cmd"}, "q")

    def quyen(self):
        tro_nang = False
        try:
            tro_nang = bool(self.cg.AXIsProcessTrusted())
        except Exception:  # noqa: BLE001
            pass
        man_hinh = None
        try:
            f = self.cg.CGPreflightScreenCaptureAccess
            f.restype = ctypes.c_bool
            man_hinh = bool(f())
        except Exception:  # noqa: BLE001
            man_hinh = None
        return {"tro_nang": tro_nang, "ghi_man_hinh": man_hinh, "chuong_trinh": os.path.realpath(sys.executable)}

    def mo_cai_dat_quyen(self, loai):
        pane = "Privacy_ScreenCapture" if loai == "man_hinh" else "Privacy_Accessibility"
        self._chay(["open", "x-apple.systempreferences:com.apple.preference.security?" + pane], 6)


# ---------------------------------------------------------------- lớp Windows
class _Win:
    ten = "Windows"
    VK = {"enter": 0x0D, "tab": 0x09, "space": 0x20, "backspace": 0x08, "escape": 0x1B, "left": 0x25, "up": 0x26, "right": 0x27, "down": 0x28, "delete": 0x2E,
          "forwarddelete": 0x2E, "home": 0x24, "end": 0x23, "pageup": 0x21, "pagedown": 0x22, "cmd": 0x5B, "ctrl": 0x11, "alt": 0x12, "shift": 0x10}

    def __init__(self):
        self.u = ctypes.windll.user32
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:  # noqa: BLE001
            try:
                self.u.SetProcessDPIAware()
            except Exception:  # noqa: BLE001
                pass

        class KB(ctypes.Structure):
            _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort), ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("extra", ctypes.c_void_p)]

        class MS(ctypes.Structure):
            _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long), ("mouseData", ctypes.c_ulong), ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("extra", ctypes.c_void_p)]

        class U(ctypes.Union):
            _fields_ = [("ki", KB), ("mi", MS)]

        class IN(ctypes.Structure):
            _fields_ = [("type", ctypes.c_ulong), ("u", U)]
        self.IN, self.KB, self.U = IN, KB, U

    def kich_thuoc(self):
        return self.u.GetSystemMetrics(0), self.u.GetSystemMetrics(1)

    def vi_tri_chuot(self):
        class PT(ctypes.Structure):
            _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
        p = PT()
        self.u.GetCursorPos(ctypes.byref(p))
        return p.x, p.y

    def di_chuyen(self, x, y):
        self.u.SetCursorPos(int(x), int(y))

    def bam(self, x, y, nut="left", lan=1):
        self.di_chuyen(x, y)
        time.sleep(0.12)
        xuong, len_ = (0x0008, 0x0010) if nut == "right" else (0x0002, 0x0004)
        for _ in range(lan):
            self.u.mouse_event(xuong, 0, 0, 0, 0)
            time.sleep(0.04)
            self.u.mouse_event(len_, 0, 0, 0, 0)
            time.sleep(0.06)

    def keo(self, x, y, x2, y2):
        self.di_chuyen(x, y)
        time.sleep(0.1)
        self.u.mouse_event(0x0002, 0, 0, 0, 0)
        for i in range(1, 9):
            self.di_chuyen(x + (x2 - x) * i // 8, y + (y2 - y) * i // 8)
            time.sleep(0.03)
        self.u.mouse_event(0x0004, 0, 0, 0, 0)

    def cuon(self, dy, x=None, y=None):
        if x is not None and y is not None:
            self.di_chuyen(x, y)
        self.u.mouse_event(0x0800, 0, 0, int(-dy * 120) & 0xFFFFFFFF, 0)

    def _gui(self, vk=0, scan=0, flags=0):
        i = self.IN(1, self.U(ki=self.KB(vk, scan, flags, 0, None)))
        self.u.SendInput(1, ctypes.byref(i), ctypes.sizeof(i))

    def go(self, text, kieu="chu"):
        for ch in text:
            if ch == "\n":
                self.nhan_phim(set(), "enter")
                continue
            raw = ch.encode("utf-16-le")
            for k in range(0, len(raw), 2):
                u = int.from_bytes(raw[k:k + 2], "little")
                self._gui(0, u, 0x0004)
                self._gui(0, u, 0x0004 | 0x0002)
            time.sleep(0.012)

    def nhan_phim(self, mods, phim):
        vk = self.VK.get(phim) or (ord(phim.upper()) if len(phim) == 1 else None)
        if vk is None:
            raise RuntimeError("Phím không biết: %s" % phim)
        ms = [self.VK[m] for m in mods]
        for m in ms:
            self._gui(m)
        self._gui(vk)
        time.sleep(0.04)
        self._gui(vk, 0, 0x0002)
        for m in reversed(ms):
            self._gui(m, 0, 0x0002)

    def chup(self, duong_dan):
        from PIL import ImageGrab
        im = ImageGrab.grab()
        im.convert("RGB").save(str(duong_dan), "JPEG", quality=62)
        return im.size

    def _ps(self, script, timeout=10):
        r = subprocess.run(["powershell", "-NoProfile", "-Command", script], capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()

    def ung_dung_truoc(self):
        h = self.u.GetForegroundWindow()
        pid = ctypes.c_ulong()
        self.u.GetWindowThreadProcessId(h, ctypes.byref(pid))
        rc, out, _ = self._ps("(Get-Process -Id %d).ProcessName" % pid.value, 6)
        return out if rc == 0 else ""

    def liet_ke_ung_dung(self):
        rc, out, _ = self._ps("Get-Process | Where-Object {$_.MainWindowTitle} | ForEach-Object { $_.ProcessName + ' | ' + $_.MainWindowTitle }", 10)
        return [x for x in out.splitlines() if x.strip()][:40] if rc == 0 else []

    def tieu_de_cua_so(self):
        buf = ctypes.create_unicode_buffer(256)
        self.u.GetWindowTextW(self.u.GetForegroundWindow(), buf, 256)
        return buf.value

    def mo_ung_dung(self, ten):
        subprocess.Popen(["cmd", "/c", "start", "", ten], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def mo_duong_dan(self, p):
        os.startfile(p)  # type: ignore[attr-defined]

    def chuyen_ung_dung(self, ten):
        self._ps("(New-Object -ComObject WScript.Shell).AppActivate('%s')" % ten.replace("'", ""), 8)

    def thoat_ung_dung(self, ten):
        subprocess.run(["taskkill", "/im", ten if ten.lower().endswith(".exe") else ten + ".exe"], capture_output=True, timeout=8)

    def quyen(self):
        return {"tro_nang": True, "ghi_man_hinh": True, "chuong_trinh": os.path.realpath(sys.executable)}

    def mo_cai_dat_quyen(self, loai):
        return None


def _nen():
    try:
        if sys.platform == "darwin":
            p = _Mac()
            return p if p.cg else None
        if os.name == "nt":
            return _Win()
    except Exception:  # noqa: BLE001
        return None
    return None


_P = None


def nen():
    global _P
    if _P is None:
        _P = _nen() or False
    return _P or None


# ---------------------------------------------------------------- kiểm tra an toàn
def phan_loai(op: str, a: dict, front: str) -> tuple[str, str]:
    """(loại, mô tả): vo_hai | can_duyet | bi_mat | xoa."""
    front = str(front or "")
    if op in ("click", "double_click", "right_click", "drag", "type", "key", "scroll") and _APP_CHAN.search(front):
        return "bi_mat", "Cửa sổ mật khẩu, khóa, ví hoặc ngân hàng (%s): anh tự làm." % front
    tep = bool(_APP_TEP.match(front.strip()))
    lenh = bool(_APP_LENH.search(front))
    cho_xoa = cho_xoa_con() > 0
    if op == "key":
        mods, phim = _tach_phim(a.get("key"))
        if phim in _PHIM_XOA and not cho_xoa:
            if {"cmd", "alt", "shift"} <= mods:
                return "xoa", "Dọn Thùng rác"
            if tep:
                return "xoa", "Xóa tệp trong %s (phím xóa)" % front
        if tep and phim in ("delete", "backspace", "forwarddelete") and mods & {"cmd", "ctrl", "shift"} and not cho_xoa:
            return "xoa", "Xóa tệp trong %s" % front
        if (("cmd" in mods and phim == "q") or ("alt" in mods and phim == "f4")):
            return "can_duyet", "Thoát ứng dụng (%s)" % front
        if phim == "enter" and lenh:
            return "can_duyet", "Chạy lệnh trong %s" % front
        if phim == "enter" and _APP_TIN_NHAN.search(front):
            return "can_duyet", "Gửi tin nhắn trong %s" % front
        if _APP_HE_THONG.search(front):
            return "can_duyet", "Thao tác trong %s" % front
    if op == "type":
        text = str(a.get("text") or "")
        if lenh and _LENH_XOA.search(text) and not cho_xoa:
            return "xoa", "Lệnh xóa gõ vào %s" % front
        if lenh:
            return "can_duyet", "Gõ lệnh vào %s" % front
        if _APP_HE_THONG.search(front):
            return "can_duyet", "Gõ trong %s" % front
    if op in ("right_click", "drag") and tep and not cho_xoa:
        return "xoa", "%s trong %s có thể chuyển tệp vào Thùng rác (dùng phím Cmd+C, Cmd+V thay thế)" % ("Menu chuột phải" if op == "right_click" else "Kéo thả", front)
    if op in ("click", "double_click", "right_click", "drag") and (_APP_HE_THONG.search(front) or (_APP_TIN_NHAN.search(front)) or lenh):
        return "can_duyet", "Bấm trong %s" % front
    if op in ("open_app", "open_path"):
        ten = str(a.get("name") or a.get("path") or "")
        if any(ten.lower().endswith(d) for d in _DUOI_NGUY_HIEM):
            return "can_duyet", "Mở tệp chạy được hoặc cài đặt: %s" % Path(ten).name
        if _APP_CHAN.search(ten):
            return "bi_mat", "Ứng dụng mật khẩu, ví, ngân hàng: anh tự mở và làm."
    if op == "quit_app":
        return "can_duyet", "Thoát ứng dụng %s" % a.get("name", "")
    return "vo_hai", ""


_OP_VAO = ("click", "double_click", "right_click", "drag", "type", "key", "open_app", "open_path", "focus_app", "quit_app")


def _can_duyet(op: str, a: dict, front: str, loai: str, mo_ta: str):
    muc = muc_hien_tai()
    if loai == "vo_hai" and muc == "hoi_het" and op in _OP_VAO:
        loai, mo_ta = "can_duyet", "Bước thao tác trên máy (mức Hỏi mọi bước)"
    if loai == "vo_hai":
        return None
    if loai == "xoa":
        _nk(op, "chặn xóa", mo_ta)
        return ("BI_CHAN_XOA: %s. AI không được xóa tệp trên máy. Muốn xóa, anh phải bật công tắc \"Cho phép AI xóa tệp\" trong bảng Điều khiển máy tính. "
                "Không tìm cách vòng, không dùng cách khác để xóa." % mo_ta)
    if loai == "bi_mat":
        _nk(op, "chờ người dùng", mo_ta)
        return "CAN_NGUOI_DUNG: %s Dừng ở đây, nói với anh việc cần làm, không bấm, không gõ." % mo_ta
    if muc == "toan_quyen":
        _nk(op, "tự duyệt (toàn quyền)", mo_ta, str(a.get("text") or a.get("key") or a.get("name") or a.get("path") or "")[:60])
        return None
    if B is None:
        return "LOI: thiếu mô-đun duyệt."
    nc = {"host": "Máy tính", "url": "", "tag": "", "ten": ("%s: %s" % (op, str(a.get("text") or a.get("key") or a.get("name") or a.get("path") or a.get("ly_do") or ""))[:100]),
          "tieu_de": front}
    if B.dung_duyet(str(a.get("duyet_id") or ""), "may_" + op, nc):
        return None
    k = B.xin_duyet("may_" + op, nc, mo_ta)
    _nk(op, "chờ duyệt", mo_ta)
    return ("CAN_DUYET: %s (ứng dụng đang mở: %s, mức tự động: %s). Anh phải bấm Duyệt trong TISA BOT (có thẻ nổi; anh cũng có thể chọn Duyệt và cho AI tự làm tiếp). "
            "Nói rõ với anh sẽ làm gì rồi gọi lại đúng lệnh này với duyet_id=\"%s\" sau khi anh duyệt. Chưa duyệt thì KHÔNG làm." %
            (mo_ta, front or "không rõ", {"hoi_het": "hỏi mọi bước", "quan_trong": "hỏi bước quan trọng"}.get(muc, muc), k))


# ---------------------------------------------------------------- thực hiện
def _quyen_loi(p) -> str:
    q = p.quyen()
    if sys.platform == "darwin" and not q.get("tro_nang"):
        return ("CHUA_CAP_QUYEN: macOS chưa cho TISA BOT điều khiển máy (Trợ năng). Nói anh mở Cài đặt hệ thống > Quyền riêng tư và bảo mật > Trợ năng, bật cho \"%s\" "
                "(bấm dấu + nếu chưa có), rồi thử lại. Trong bảng Điều khiển máy tính có nút mở thẳng trang đó." % q.get("chuong_trinh"))
    return ""


async def _cai_dat_quyen(p) -> str:
    """Tự mở đúng chỗ trong Cài đặt Hệ thống rồi chờ anh bật công tắc (macOS không cho phần mềm tự cấp quyền cho chính nó)."""
    if p.ten != "macOS":
        return "Không cần cấp quyền riêng trên %s." % p.ten
    q = await asyncio.to_thread(p.quyen)
    thieu = [("tro_nang", "Trợ năng") for _ in [0] if not q.get("tro_nang")] + [("man_hinh", "Ghi màn hình") for _ in [0] if q.get("ghi_man_hinh") is False]
    if not thieu:
        return "Đã đủ quyền (Trợ năng và Ghi màn hình). Làm tiếp được."
    for loai, _ten in thieu:
        await asyncio.to_thread(p.mo_cai_dat_quyen, loai)
        await asyncio.sleep(1.5)
    t0 = time.time()
    while time.time() - t0 < 120:
        await asyncio.sleep(2.0)
        q = await asyncio.to_thread(p.quyen)
        if q.get("tro_nang") and q.get("ghi_man_hinh") is not False:
            return "Anh đã bật quyền xong (Trợ năng và Ghi màn hình). Làm tiếp được."
    return ("CAN_NGUOI_DUNG: Em đã mở Cài đặt Hệ thống > Quyền riêng tư và bảo mật (%s). Anh bật công tắc cho chương trình \"%s\" (bấm dấu + nếu chưa có trong danh sách; macOS có thể hỏi mật khẩu máy hoặc Touch ID, em không thể tự làm bước này). "
            "Nếu bật Ghi màn hình mà vẫn báo thiếu thì cần khởi động lại TISA BOT. Anh bật xong nhắn em, em kiểm tra lại." % (", ".join(n for _l, n in thieu), q.get("chuong_trinh")))


async def thuc_hien(op: str, a: dict) -> str:
    op = str(op or "").strip().lower()
    a = a or {}
    p = nen()
    if p is None:
        return "KHONG_HO_TRO: Máy này chưa hỗ trợ điều khiển máy tính (cần macOS hoặc Windows)."
    with _khoa:
        dung = _tt["dung"]
    if dung and op not in ("status", "permissions", "windows", "front"):
        return "DA_DUNG: Anh đã bấm Dừng AI ngay. Không thao tác tiếp, hỏi anh khi nào cho làm tiếp."
    if op == "cai_dat_quyen":
        return await _cai_dat_quyen(p)
    if p.ten == "macOS" and op not in ("status", "permissions", "windows", "front", "wait") and muc_hien_tai() != "tat":
        q = await asyncio.to_thread(p.quyen)
        if not q.get("tro_nang") or q.get("ghi_man_hinh") is False:
            return ("CAN_QUYEN: macOS chưa cấp quyền (Trợ năng: %s, Ghi màn hình: %s) nên em chưa nhìn và bấm được. Gọi tisa_desktop_do op=cai_dat_quyen: TISA BOT mở sẵn Cài đặt và chờ anh bật công tắc, "
                    "có quyền xong em tự làm tiếp. Nói với anh một câu là em đang cần anh bật công tắc." % ("đã cấp" if q.get("tro_nang") else "chưa", "đã cấp" if q.get("ghi_man_hinh") is not False else "chưa"))
    if muc_hien_tai() == "tat" and op not in ("status", "permissions"):
        return ("DA_TAT: Anh chưa cho AI dùng máy tính (mức \"Không cho\"). Không chụp màn hình, không bấm, không mở ứng dụng. "
                "Làm bằng trình duyệt TISA hoặc công cụ khác; cần dùng máy thì xin anh bật ở mục Điều khiển máy tính.")
    try:
        return await asyncio.to_thread(_lam, p, op, a)
    except Exception as e:  # noqa: BLE001
        _nk(op, "lỗi", "%s: %s" % (type(e).__name__, str(e)[:140]))
        return "LOI: %s: %s" % (type(e).__name__, str(e)[:240])


def _lam(p, op: str, a: dict) -> str:
    if op == "status":
        return json.dumps(trang_thai(), ensure_ascii=False)
    if op == "permissions":
        q = p.quyen()
        return "Hệ điều hành: %s. Quyền điều khiển (Trợ năng): %s. Quyền ghi màn hình: %s. Chương trình cần cấp quyền: %s" % (
            p.ten, "ĐÃ CẤP" if q.get("tro_nang") else "CHƯA", {True: "ĐÃ CẤP", False: "CHƯA", None: "không rõ"}[q.get("ghi_man_hinh")], q.get("chuong_trinh"))
    if op == "front":
        return "Ứng dụng đang ở trước: %s. Cửa sổ: %s" % (p.ung_dung_truoc() or "không rõ", p.tieu_de_cua_so() or "không rõ")
    if op == "windows":
        return "Ứng dụng đang mở:\n" + "\n".join("- " + x for x in p.liet_ke_ung_dung()) + "\nỨng dụng ở trước: %s" % (p.ung_dung_truoc() or "không rõ")
    if op == "screenshot":
        ANH.mkdir(parents=True, exist_ok=True)
        f = ANH / (time.strftime("%Y%m%d-%H%M%S") + ".jpg")
        w, h = p.chup(f)
        for x in sorted(ANH.glob("*.jpg"))[:-30]:
            try:
                x.unlink()
            except OSError:
                pass
        with open(ANH / "moi-nhat.txt", "w", encoding="utf-8") as fh:
            fh.write(str(f))
        _nk("screenshot", "ok", "Chụp màn hình %dx%d" % (w, h))
        return ("Ảnh chụp màn hình đã lưu: %s. Kích thước %dx%d, tọa độ (x,y) trong ảnh đúng bằng tọa độ để bấm (gốc ở góc trên trái). "
                "Đọc ảnh bằng công cụ đọc tệp để nhìn màn hình rồi mới bấm. Ứng dụng đang ở trước: %s." % (f, w, h, p.ung_dung_truoc() or "không rõ"))
    if op == "wait":
        time.sleep(min(max(int(a.get("ms") or 1000), 100), 10000) / 1000)
        return "Đã chờ."
    if op not in _OP_VAO + ("move", "scroll"):
        return "LOI: op không hợp lệ: %s" % op
    loi_q = _quyen_loi(p)
    if loi_q:
        return loi_q
    vt = p.vi_tri_chuot()
    if vt[0] <= 2 and vt[1] <= 2:               # chuột ở góc trên trái = người dùng muốn dừng
        with _khoa:
            _tt["dung"] = True
        _nk("dung", "đã dừng", "Chuột ở góc trên trái màn hình: tự dừng")
        return "DA_DUNG: Chuột đang ở góc trên trái màn hình, coi như anh muốn dừng. Hỏi anh khi nào cho làm tiếp."
    front = p.ung_dung_truoc()
    loai, mo_ta = phan_loai(op, a, front)
    kq = _can_duyet(op, a, front, loai, mo_ta)
    if kq:
        return kq
    with _khoa:
        moi = time.time() - _tt["lan_cuoi"] > 300
        _tt["lan_cuoi"] = time.time()
    if moi and sys.platform == "darwin":
        try:
            subprocess.Popen([_lenh_mac("osascript"), "-e", 'display notification "AI đang điều khiển máy. Đưa chuột về góc trên trái màn hình để dừng." with title "TISA BOT"'],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError:
            pass
    w, h = p.kich_thuoc()
    ten = ""

    def toa_do(kx="x", ky="y"):
        if a.get(kx) is None or a.get(ky) is None:
            raise RuntimeError("thiếu toạ độ %s,%s (lấy từ ảnh chụp màn hình)" % (kx, ky))
        x, y = int(a[kx]), int(a[ky])
        if not (0 <= x < w and 0 <= y < h):
            raise RuntimeError("toạ độ (%d,%d) nằm ngoài màn hình %dx%d" % (x, y, w, h))
        return x, y

    if op in ("click", "double_click", "right_click"):
        x, y = toa_do()
        p.bam(x, y, "right" if op == "right_click" else "left", 2 if op == "double_click" else 1)
        ten = "(%d,%d)" % (x, y)
        kq = "Đã %s tại (%d,%d). Chụp màn hình lại để xem kết quả." % ({"click": "bấm", "double_click": "bấm đúp", "right_click": "bấm chuột phải"}[op], x, y)
    elif op == "move":
        x, y = toa_do()
        p.di_chuyen(x, y)
        kq = "Đã di chuột tới (%d,%d)." % (x, y)
    elif op == "drag":
        x, y = toa_do()
        x2, y2 = toa_do("x2", "y2")
        p.keo(x, y, x2, y2)
        kq = "Đã kéo từ (%d,%d) tới (%d,%d)." % (x, y, x2, y2)
    elif op == "scroll":
        dy = int(a.get("dy") if a.get("dy") is not None else 5)
        p.cuon(dy, int(a["x"]) if a.get("x") is not None else None, int(a["y"]) if a.get("y") is not None else None)
        kq = "Đã cuộn %s %d nấc." % ("xuống" if dy > 0 else "lên", abs(dy))
    elif op == "type":
        text = str(a.get("text") or "")
        if not text:
            return "LOI: thiếu text."
        if len(text) > 4000:
            return "LOI: chuỗi gõ quá dài (tối đa 4000 ký tự mỗi lần)."
        p.go(text, "phim" if str(a.get("kieu") or "").lower() in ("phim", "key", "keys") else "chu")
        ten = "gõ %d ký tự" % len(text)
        kq = "Đã gõ %d ký tự vào ứng dụng đang ở trước (%s)." % (len(text), front or "không rõ")
    elif op == "key":
        mods, phim = _tach_phim(a.get("key"))
        if not phim:
            return "LOI: thiếu phím (ví dụ cmd+space, enter, ctrl+c, alt+tab)."
        p.nhan_phim(mods, phim)
        ten = str(a.get("key"))
        kq = "Đã nhấn %s." % a.get("key")
    elif op == "open_app":
        nm = str(a.get("name") or "").strip()
        if not nm:
            return "LOI: thiếu name (tên ứng dụng)."
        p.mo_ung_dung(nm)
        ten = nm
        kq = "Đã mở ứng dụng %s. Chờ 1 đến 2 giây rồi chụp màn hình." % nm
    elif op == "open_path":
        pt = os.path.expanduser(str(a.get("path") or "").strip())
        if not pt or not Path(pt).exists():
            return "LOI: không thấy đường dẫn %s" % pt
        p.mo_duong_dan(pt)
        ten = Path(pt).name
        kq = "Đã mở %s bằng ứng dụng mặc định. Chờ 1 đến 2 giây rồi chụp màn hình." % pt
    elif op == "focus_app":
        nm = str(a.get("name") or "").strip()
        p.chuyen_ung_dung(nm)
        ten = nm
        kq = "Đã chuyển sang %s." % nm
    elif op == "quit_app":
        nm = str(a.get("name") or "").strip()
        p.thoat_ung_dung(nm)
        ten = nm
        kq = "Đã gửi lệnh thoát %s." % nm
    else:
        return "LOI: op không hợp lệ."
    _nk(op, "ok", kq[:120], ten)
    return kq


# ---------------------------------------------------------------- trạng thái, hub, máy chủ
def trang_thai() -> dict:
    p = nen()
    d = {"ho_tro": bool(p), "he": p.ten if p else "", "muc": muc_hien_tai(), "muc_den": _tt["muc_den"], "dung": _tt["dung"], "cho_xoa_giay": cho_xoa_con(), "quyen": {}, "truoc": ""}
    if p:
        try:
            d["quyen"] = p.quyen()
            d["truoc"] = p.ung_dung_truoc()
        except Exception:  # noqa: BLE001
            pass
    d["nhat_ky"] = [x for x in (B.doc_nk(80) if B else []) if str(x.get("op", "")).startswith("may_")][-12:]
    return d


_MO_TA_NHIN = ("Nhìn máy tính của anh (macOS hoặc Windows). op=screenshot chụp màn hình (đọc ảnh để biết bấm đâu); op=windows liệt kê ứng dụng đang mở; op=front ứng dụng đang ở trước; "
               "op=permissions kiểm tra quyền điều khiển; op=status. Làm theo kỹ năng dq-dieu-khien-may.")
_MO_TA_LAM = ("Điều khiển máy tính của anh như người thật. op=click|double_click|right_click x y (toạ độ theo ảnh chụp); op=move x y; op=drag x y x2 y2; op=scroll dy (dương = xuống); "
              "op=type text (gõ được tiếng Việt; thêm kieu=phim để gõ từng phím thật cho máy tính bỏ túi, trò chơi); op=key key (ví dụ cmd+space, enter, ctrl+c, alt+tab); op=open_app name; op=open_path path (mở thư mục hoặc tệp); op=focus_app name; "
              "op=quit_app name; op=wait ms; op=cai_dat_quyen (macOS chưa cấp quyền: tự mở Cài đặt rồi chờ anh bật công tắc). Luôn chụp màn hình trước khi bấm và sau khi bấm để kiểm tra. KHÔNG xóa được tệp (công cụ chặn). Việc nhạy cảm trả CAN_DUYET: xin anh duyệt rồi gọi lại "
              "với duyet_id. Làm theo kỹ năng dq-dieu-khien-may.")


def dang_ky_hub(add, vault_root=None) -> None:
    async def _nhin(args):
        a = args or {}
        op = str(a.get("op") or "screenshot").lower()
        if op not in ("screenshot", "windows", "front", "permissions", "status"):
            return "LOI: op của tisa_desktop_look: screenshot, windows, front, permissions, status."
        return await thuc_hien(op, a)

    async def _lam(args):
        a = args or {}
        op = str(a.get("op") or "").lower()
        if op in ("screenshot", "windows", "front", "permissions", "status", ""):
            return "LOI: op của tisa_desktop_do: click, double_click, right_click, move, drag, scroll, type, key, open_app, open_path, focus_app, quit_app, wait, cai_dat_quyen."
        return await thuc_hien(op, a)

    add("tisa_desktop_look", _MO_TA_NHIN, {"op": {"type": "string", "description": "screenshot | windows | front | permissions | status (mặc định screenshot)"}}, [], _nhin, effect="write")
    add("tisa_desktop_do", _MO_TA_LAM,
        {"op": {"type": "string"}, "x": {"type": "integer"}, "y": {"type": "integer"}, "x2": {"type": "integer"}, "y2": {"type": "integer"}, "dy": {"type": "integer"},
         "text": {"type": "string"}, "key": {"type": "string"}, "name": {"type": "string"}, "path": {"type": "string"}, "ms": {"type": "integer"},
         "ly_do": {"type": "string"}, "duyet_id": {"type": "string"}, "kieu": {"type": "string", "description": "type: 'phim' = gõ từng phím thật (máy tính bỏ túi, phím tắt); mặc định gõ chữ"}},
        ["op"], _lam, effect="write")


def gan(app) -> None:
    from fastapi.responses import FileResponse, JSONResponse

    @app.get("/may-ai/trang-thai")
    async def ma_trang_thai():
        return JSONResponse(await asyncio.to_thread(trang_thai))

    @app.post("/may-ai/muc")
    async def ma_muc(request: Request):
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        try:
            phut = int((d or {}).get("phut") or 0)
        except (TypeError, ValueError):
            phut = 0
        return JSONResponse(dat_muc(str((d or {}).get("muc") or ""), max(0, min(phut, 24 * 60))))

    @app.post("/may-ai/cho-xoa")
    async def ma_cho_xoa(request: Request):
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        try:
            phut = int((d or {}).get("phut") or 0)
        except (TypeError, ValueError):
            phut = 0
        return JSONResponse(dat_cho_xoa(phut))

    @app.post("/may-ai/dung")
    async def ma_dung():
        with _khoa:
            _tt["dung"] = True
        _nk("dung", "đã dừng", "Anh bấm Dừng AI ngay")
        return JSONResponse({"ok": True})

    @app.post("/may-ai/tiep-tuc")
    async def ma_tiep():
        with _khoa:
            _tt["dung"] = False
        _nk("tiep", "cho làm tiếp", "Anh cho AI điều khiển máy tiếp")
        return JSONResponse({"ok": True})

    @app.post("/may-ai/cai-dat-quyen")
    async def ma_cai_dat_quyen():
        p = nen()
        if p is None or p.ten != "macOS":
            return JSONResponse({"ok": True})
        q = await asyncio.to_thread(p.quyen)
        for loai, can in (("tro_nang", not q.get("tro_nang")), ("man_hinh", q.get("ghi_man_hinh") is False)):
            if can:
                await asyncio.to_thread(p.mo_cai_dat_quyen, loai)
                await asyncio.sleep(1.2)
        return JSONResponse({"ok": True, "quyen": await asyncio.to_thread(p.quyen)})

    @app.post("/may-ai/mo-quyen")
    async def ma_mo_quyen(request: Request):
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        p = nen()
        if p:
            await asyncio.to_thread(p.mo_cai_dat_quyen, str((d or {}).get("loai") or "tro_nang"))
        return JSONResponse({"ok": bool(p)})

    @app.post("/may-ai/thu")
    async def ma_thu():
        return JSONResponse({"kq": await thuc_hien("screenshot", {})})

    @app.get("/may-ai/anh-moi")
    async def ma_anh():
        try:
            f = Path((ANH / "moi-nhat.txt").read_text(encoding="utf-8").strip())
            if f.is_file() and ANH in f.parents:
                return FileResponse(str(f), media_type="image/jpeg", headers={"Cache-Control": "no-store"})
        except OSError:
            pass
        return JSONResponse({"loi": "chưa có ảnh"}, status_code=404)


_nap()
