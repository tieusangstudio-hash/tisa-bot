"""tisa_desktop.py - Điều khiển máy tính (V2.99): AI Agent dùng chính máy của người dùng như người thật.

Mở màn hình, nhìn màn hình, di chuột, bấm, gõ, dùng phím tắt, mở ứng dụng và tệp, chuyển cửa sổ. Dùng khi việc cần thao tác trên máy
(tìm thư mục, bấm vào tệp, dùng ứng dụng không có MCP hay API). Chạy ngay trên máy chạy TISA BOT (macOS và Windows), không tải lên đâu.

Cách làm: không cài thêm gì. macOS dùng CoreGraphics qua ctypes (chuột, phím, gõ cả tiếng Việt), `screencapture`, `lsappinfo`, `open`.
Windows dùng user32 qua ctypes (SendInput), Pillow chụp màn hình, PowerShell cho danh sách cửa sổ. Hai công cụ cho hub:
  - tisa_desktop_look (chỉ xem): screenshot, windows, front, permissions, status
  - tisa_desktop_do   (thao tác): click, double_click, right_click, move, drag, scroll, type, key, open_app, open_path, focus_app, quit_app, wait,
                       mo_khoa (mở khóa màn hình đăng nhập macOS khi anh ở xa; mô-đun riêng tisa_mo_khoa.py, không nới chốt chặn loginwindow của các op khác)

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
_VAULT = {"root": None}          # thư mục brain (để lưu ảnh, video vào 04-ket-qua), đặt lúc đăng ký hub

# ---------------------------------------------------------------- luật phân loại
_APP_CHAN = re.compile(r"securityagent|coreautha|loginwindow|keychain|1password|bitwarden|lastpass|keepass|dashlane|metamask|exodus|ledger|trezor|binance|"
                       r"trustwallet|authenticator|momo|zalopay|vcb|vietcombank|techcombank|mbbank|bidv|tpbank|vpbank|banking|ngân hàng|ví điện tử|credential", re.I)
_APP_TEP = re.compile(r"^(finder|explorer|file explorer|windows explorer|files|nautilus|dolphin|thunar)$", re.I)
_APP_LENH = re.compile(r"terminal|iterm|warp|powershell|^cmd|command prompt|windows terminal|konsole|hyper|ghostty|kitty|alacritty|wezterm|pwsh|conhost", re.I)
_APP_TIN_NHAN = re.compile(r"messages|^mail$|outlook|zalo|telegram|slack|whatsapp|messenger|discord|teams|skype|viber|signal|^line$|facebook", re.I)
_APP_HE_THONG = re.compile(r"system settings|system preferences|cài đặt|^settings$|control panel|regedit|task manager|activity monitor|disk utility|installer|registry", re.I)
_TIEN_CUA_SO = re.compile(r"checkout|payment|thanh toán|thanh toan|nạp tiền|nap tien|billing|subscribe|subscription|nâng cấp gói|nang cap goi|purchase|buy now|mua ngay|add payment|credit card|thẻ tín dụng|the tin dung|paypal|stripe|đặt hàng|dat hang|top ?up", re.I)
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
        if muc == "toan_quyen":
            _tt["dung"] = False   # (V3.07) cấp Toàn quyền thì bỏ cờ "Đã dừng" của lần bấm Dừng trước
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
            try:       # (18/11/2026) phím gõ ra từ nguồn "phần cứng" (HID system state), màn hình đăng nhập chịu phím này hơn nguồn rỗng
                c.CGEventSourceCreate.argtypes = [ctypes.c_int32]
                c.CGEventSourceCreate.restype = ctypes.c_void_p
                self.src = c.CGEventSourceCreate(1)
            except (AttributeError, OSError):
                self.src = None
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
        time.sleep(0.05)
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
        e = self.cg.CGEventCreateKeyboardEvent(getattr(self, "src", None), ma, xuong)
        if flags:
            self.cg.CGEventSetFlags(e, flags)
        self._post(e)

    _SHIFT = {"+": "=", "*": "8", "(": "9", ")": "0", "_": "-", '"': "'", ":": ";", "<": ",", ">": ".", "?": "/", "!": "1", "@": "2", "#": "3", "$": "4", "%": "5", "^": "6", "&": "7", "|": "\\", "{": "[", "}": "]"}

    def go(self, text, kieu="chu", tre=0.03, pid=0):
        if pid:       # chuột riêng: gõ thẳng vào tiến trình của cửa sổ đích, không đụng bàn phím của anh
            import tisa_chuot_rieng as CR
            if kieu == "phim":
                for ch in text:
                    base, fl = None, 0
                    if ch == "\n":
                        base = "enter"
                    elif ch.lower() in self.KC and len(ch) == 1:
                        base, fl = ch.lower(), (self.FL["shift"] if ch.isupper() else 0)
                    elif ch in self._SHIFT:
                        base, fl = self._SHIFT[ch], self.FL["shift"]
                    if base is not None:
                        CR.phim(pid, self.KC[base], fl, True)
                        time.sleep(0.01)
                        CR.phim(pid, self.KC[base], fl, False)
                        time.sleep(tre)
            else:
                CR.go_chu(pid, text, 0.012)
            return
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
                    time.sleep(0.01)
                    self._phim(self.KC[base], fl, False)
                    time.sleep(tre)
                    continue
            u = ch.encode("utf-16-le")
            arr = (ctypes.c_uint16 * (len(u) // 2)).from_buffer_copy(u)
            for xuong in (True, False):
                e = self.cg.CGEventCreateKeyboardEvent(None, 0, xuong)
                self.cg.CGEventKeyboardSetUnicodeString(e, len(arr), arr)
                self._post(e)
            time.sleep(0.012)

    def nhan_phim(self, mods, phim, pid=0):
        ma = self.KC.get(phim)
        if ma is None:
            raise RuntimeError("Phím không biết: %s" % phim)
        flags = 0
        for m in mods:
            flags |= self.FL[m]
        if pid:
            import tisa_chuot_rieng as CR
            CR.phim(pid, ma, flags, True)
            time.sleep(0.03)
            CR.phim(pid, ma, flags, False)
            return
        self._phim(ma, flags, True)
        time.sleep(0.04)
        self._phim(ma, flags, False)

    def _chay(self, cmd, timeout=8):
        # TISA BOT chạy dưới launchd nên PATH rất ngắn (không có /usr/sbin, nơi chứa screencapture): gọi bằng đường dẫn đầy đủ.
        cmd = [_lenh_mac(cmd[0])] + list(cmd[1:])
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=_moi_truong_mac())
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()

    def dan_chu(self, text, pid=0):
        """Đưa chữ vào ô đang chọn bằng CLIPBOARD (pbcopy rồi cmd+v) thay vì gõ từng phím: bộ gõ Telex/VNI của macOS không biến chữ.
        Khôi phục clipboard cũ (chỉ phần chữ) sau khi dán."""
        cu = None
        try:
            r = subprocess.run([_lenh_mac("pbpaste")], capture_output=True, timeout=5, env=_moi_truong_mac())
            cu = r.stdout if r.returncode == 0 else None
        except (OSError, subprocess.SubprocessError):
            cu = None
        subprocess.run([_lenh_mac("pbcopy")], input=text.encode("utf-8"), timeout=5, check=True, env=_moi_truong_mac())
        try:
            time.sleep(0.06)
            self.nhan_phim({"cmd"}, "v", pid=pid)
            time.sleep(0.3)
        finally:
            if cu:
                try:
                    subprocess.run([_lenh_mac("pbcopy")], input=cu, timeout=5, env=_moi_truong_mac())
                except (OSError, subprocess.SubprocessError):
                    pass

    def chup(self, duong_dan):
        w, h = self.kich_thuoc()
        rc, _, err = self._chay(["screencapture", "-x", "-m", "-t", "jpg", str(duong_dan)], 15)
        if rc != 0 or not Path(duong_dan).exists():
            raise RuntimeError("Chụp màn hình lỗi: %s" % (err or "chưa cấp quyền Ghi màn hình"))
        self._chay(["sips", "--resampleHeightWidth", str(h), str(w), str(duong_dan)], 15)   # về đúng toạ độ điểm (không bị nhân đôi ở màn Retina)
        return w, h

    def man_hinh_khoa(self):
        """True nếu phiên đang khóa (macOS ghi cờ CGSSessionScreenIsLocked khi khóa). Chính xác hơn xem ứng dụng ở trước là loginwindow. None nếu không đọc được."""
        try:
            rc, out, _ = self._chay(["ioreg", "-n", "Root", "-d1", "-l"], 8)
        except Exception:  # noqa: BLE001
            return None
        if rc != 0 or not out:
            return None
        # 25/11/2026: đọc GIÁ TRỊ chứ không chỉ sự có mặt của khóa: khóa còn nằm lại với giá trị No/0 thì máy KHÔNG khóa
        # (trước đây `in out` coi là khóa mãi, báo "vẫn ở màn hình khóa" oan sau khi đã vào máy).
        m = re.search(r'"?CGSSessionScreenIsLocked"?\s*=\s*(\w+)', out)
        if not m:
            return False
        return m.group(1).strip().lower() in ("yes", "1", "true")

    def danh_thuc_man_hinh(self):
        """Báo macOS 'người dùng vừa thao tác' để màn hình sáng lên (caffeinate -u), tin cậy hơn nhích chuột."""
        try:
            self._chay(["caffeinate", "-u", "-t", "3"], 6)
        except Exception:  # noqa: BLE001
            pass

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

    def mo_ung_dung(self, ten, nen=False):
        g = ["-g"] if nen else []            # -g: mở ở NỀN, không giành màn hình của anh (chuột riêng)
        rc, _, err = self._chay(["open"] + g + ["-a", ten], 15)
        if rc != 0:
            bid = self._bundle_theo_ten(ten)
            rc, _, err = self._chay(["open"] + g + ["-b", bid], 15) if bid else (rc, "", err)
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

    def go(self, text, kieu="chu", tre=0.03, pid=0):
        if pid:       # chuột riêng: WM_CHAR thẳng vào cửa sổ đích, không đụng bàn phím của anh
            import tisa_chuot_rieng_win as CRW
            CRW.go_chu(pid, text, 0.012)
            return
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

    def nhan_phim(self, mods, phim, pid=0):
        if pid:
            import tisa_chuot_rieng_win as CRW
            CRW.nhan_phim_ten(pid, mods, phim)
            return
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

    def dan_chu(self, text, pid=0):
        """Đưa chữ vào ô đang chọn bằng clipboard (Set-Clipboard rồi ctrl+v), khôi phục clipboard chữ cũ. (Chưa kiểm trên Windows thật.)"""
        if pid:      # chuột riêng: gõ thẳng WM_CHAR (có dấu vẫn nguyên), không đụng clipboard của anh
            self.go(text, "chu", pid=pid)
            return
        ps = ["powershell", "-NoProfile", "-Command"]
        cu = None
        try:
            r = subprocess.run(ps + ["[Console]::OutputEncoding=[Text.Encoding]::UTF8; Get-Clipboard -Raw"], capture_output=True, timeout=8)
            cu = r.stdout if r.returncode == 0 else None
        except (OSError, subprocess.SubprocessError):
            cu = None
        dat = "[Console]::InputEncoding=[Text.Encoding]::UTF8; $t=[Console]::In.ReadToEnd(); Set-Clipboard -Value $t"
        subprocess.run(ps + [dat], input=text.encode("utf-8"), timeout=10, check=True)
        try:
            time.sleep(0.15)
            self.nhan_phim({"ctrl"}, "v")
            time.sleep(0.4)
        finally:
            if cu:
                try:
                    subprocess.run(ps + [dat], input=cu, timeout=10)
                except (OSError, subprocess.SubprocessError):
                    pass

    def chup(self, duong_dan):
        """Chụp màn hình chính ở độ phân giải thật. Có đường dự phòng PowerShell nếu Pillow lỗi; báo rõ khi ảnh đen (máy khoá, không có màn hình)."""
        im, loi_pil = None, ""
        try:
            from PIL import ImageGrab
            im = ImageGrab.grab()
        except Exception as e:  # noqa: BLE001
            loi_pil = "%s: %s" % (type(e).__name__, str(e)[:120])
        if im is not None:
            im = im.convert("RGB")
            if im.getbbox() is not None and im.getextrema() != ((0, 0), (0, 0), (0, 0)):
                im.save(str(duong_dan), "JPEG", quality=82)
                return im.size
            loi_pil = "ảnh chụp ra toàn màu đen"
        ps = ("Add-Type -AssemblyName System.Windows.Forms,System.Drawing\n"
              "Add-Type -TypeDefinition 'using System.Runtime.InteropServices; public class TisaDpi { [DllImport(\"user32.dll\")] public static extern bool SetProcessDPIAware(); }'\n"
              "[void][TisaDpi]::SetProcessDPIAware()\n"
              "$s=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds\n"
              "$b=New-Object System.Drawing.Bitmap $s.Width,$s.Height\n"
              "$g=[System.Drawing.Graphics]::FromImage($b)\n"
              "$g.CopyFromScreen($s.Location,[System.Drawing.Point]::Empty,$s.Size)\n"
              "$b.Save('%s',[System.Drawing.Imaging.ImageFormat]::Jpeg)\n"
              "Write-Output ($s.Width.ToString()+'x'+$s.Height.ToString())" % str(duong_dan).replace("'", "''"))
        import base64
        try:   # -EncodedCommand: không phụ thuộc cách Windows xử lý dấu nháy kép trong dòng lệnh
            r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-EncodedCommand", base64.b64encode(ps.encode("utf-16-le")).decode("ascii")],
                               capture_output=True, text=True, timeout=25)
            rc, out, err = r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()
        except Exception as e:  # noqa: BLE001
            rc, out, err = 1, "", "%s: %s" % (type(e).__name__, str(e)[:100])
        f = Path(duong_dan)
        if rc != 0 or not f.is_file() or f.stat().st_size < 2000:
            raise RuntimeError("Chụp màn hình lỗi (%s%s). Thường do máy đang khoá màn hình hoặc TISA BOT đang chạy ở phiên không có màn hình: mở khoá máy, mở lại TISA BOT trong phiên đang đăng nhập rồi thử lại." % (loi_pil or "không rõ", (" · " + err[:120]) if err else ""))
        try:
            from PIL import Image
            with Image.open(str(f)) as t:
                if t.convert("L").getextrema() == (0, 0):
                    raise RuntimeError("Màn hình chụp ra toàn màu đen: máy đang khoá hoặc tắt màn hình. Mở khoá máy rồi thử lại.")
                return t.size
        except RuntimeError:
            raise
        except Exception:  # noqa: BLE001
            m = re.match(r"(\d+)x(\d+)", out or "")
            return (int(m.group(1)), int(m.group(2))) if m else self.kich_thuoc()

    def _ps(self, script, timeout=10):
        r = subprocess.run(["powershell", "-NoProfile", "-Command", script], capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()

    # 26/11/2026: ba thao tác dưới đây trước mở một PowerShell MỖI LẦN gọi (0,5 đến 1,5 giây trên Windows). ung_dung_truoc chạy ít nhất
    # hai lần mỗi thao tác của AI (kiểm an toàn trước khi bấm, ghi kèm ảnh sau khi bấm): mỗi cú bấm tốn 1 đến 3 giây chỉ để đọc một cái
    # tên. Nay đọc thẳng bằng API hệ thống qua tisa_chuot_rieng_win (dưới 1 ms); không ra kết quả mới quay về PowerShell như cũ.
    @staticmethod
    def _cr():
        try:
            import tisa_chuot_rieng_win as CR
            return CR if CR._nap() else None
        except Exception:  # noqa: BLE001
            return None

    def ung_dung_truoc(self):
        h = self.u.GetForegroundWindow()
        pid = ctypes.c_ulong()
        self.u.GetWindowThreadProcessId(h, ctypes.byref(pid))
        CR = self._cr()
        if CR is not None and pid.value:
            try:
                ten = CR._ten_tien_trinh(pid.value)
                if ten:
                    return ten
            except Exception:  # noqa: BLE001
                pass
        rc, out, _ = self._ps("(Get-Process -Id %d).ProcessName" % pid.value, 6)
        return out if rc == 0 else ""

    def liet_ke_ung_dung(self):
        CR = self._cr()
        if CR is not None:
            try:
                ds, thay = [], set()
                for w in CR.liet_ke_cua_so():
                    dong = "%s | %s" % (w.get("ung_dung") or "?", w.get("tieu_de") or "")
                    if (w.get("tieu_de") or "").strip() and dong not in thay:
                        thay.add(dong)
                        ds.append(dong)
                if ds:
                    return ds[:40]
            except Exception:  # noqa: BLE001
                pass
        rc, out, _ = self._ps("Get-Process | Where-Object {$_.MainWindowTitle} | ForEach-Object { $_.ProcessName + ' | ' + $_.MainWindowTitle }", 10)
        return [x for x in out.splitlines() if x.strip()][:40] if rc == 0 else []

    def tieu_de_cua_so(self):
        buf = ctypes.create_unicode_buffer(256)
        self.u.GetWindowTextW(self.u.GetForegroundWindow(), buf, 256)
        return buf.value

    def mo_ung_dung(self, ten, nen=False):
        subprocess.Popen(["cmd", "/c", "start", "", ten], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def mo_duong_dan(self, p):
        os.startfile(p)  # type: ignore[attr-defined]

    def chuyen_ung_dung(self, ten):
        CR = self._cr()
        if CR is not None:
            try:
                w = CR.tim_cua_so(ten)
                if w:
                    h = int(w["id"])
                    self.u.keybd_event(0x12, 0, 0, 0)          # nhấn-thả Alt: Windows chỉ cho đưa cửa sổ lên trước khi vừa có thao tác phím
                    self.u.keybd_event(0x12, 0, 2, 0)
                    self.u.SetForegroundWindow(h)
                    time.sleep(0.05)
                    if int(self.u.GetForegroundWindow() or 0) == h:
                        return
            except Exception:  # noqa: BLE001
                pass
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


_OP_VAO = ("click", "double_click", "right_click", "drag", "type", "key", "open_app", "open_path", "focus_app", "quit_app", "mo_chrome", "chon_tep")


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
        return ("CAN_NGUOI_DUNG: %s Dừng ở đây, không bấm, không gõ. Gọi tisa_desktop_do op=cho_nguoi_that ly_do=\"...\" để em báo anh bằng tin ngắn (dashboard, Zalo) rồi chờ anh làm xong và tự làm tiếp." % mo_ta)
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


def _chong_chen(op: str, a: dict, front: str):
    """Trước khi gõ/nhấn phím vào trình duyệt: có thứ khác đang điều khiển trình duyệt thì dừng và nói rõ nguyên nhân (tisa_chong_chen.py)."""
    try:
        import tisa_chong_chen as CC
    except Exception:  # noqa: BLE001
        return None
    if not CC.la_trinh_duyet(front):
        return None
    kq = CC.phat_hien()
    if not kq["cung"]:
        return None
    if muc_hien_tai() == "toan_quyen":
        # (V3.43, chủ 22/11) Anh đã cấp Toàn quyền: không chặn, không hỏi lại; chỉ ghi nhật ký để biết lúc đó có gì đang chạy.
        _nk(op, "toàn quyền, gõ dù có công cụ khác", "; ".join(kq["cung"])[:180])
        return None
    if a.get("bo_qua_chen"):
        k = _can_duyet(op, a, front, "can_duyet", "Gõ vào trình duyệt dù đang có thứ khác điều khiển: %s" % "; ".join(kq["cung"])[:150])
        if k is None:
            _nk(op, "bỏ qua chặn chen (đã duyệt)", "; ".join(kq["cung"])[:150])
            return None
        return k
    _nk(op, "bị chen", "; ".join(kq["cung"])[:180])
    return CC.thong_bao(kq)


# ---------------------------------------------------------------- thực hiện
def _huong_dan_quyen(p) -> str:
    try:
        import tisa_cai_quyen as CQ
        return CQ.huong_dan(p)
    except Exception:  # noqa: BLE001
        return ""


def _quyen_loi(p) -> str:
    q = p.quyen()
    if sys.platform == "darwin" and not q.get("tro_nang"):
        return ("CHUA_CAP_QUYEN: macOS chưa cho TISA BOT điều khiển máy (Trợ năng). ĐỪNG chỉ nói \"em không làm được\": gọi tisa_desktop_do op=cai_dat_quyen (TISA BOT hiện hộp xin quyền, mở sẵn đúng trang Cài đặt và chờ), "
                "rồi hướng dẫn người dùng TỪNG BƯỚC theo đoạn sau, nói cụ thể bấm vào đâu, đợi họ làm xong rồi làm tiếp:\n%s" % (_huong_dan_quyen(p) or "Cài đặt Hệ thống > Quyền riêng tư & Bảo mật > Trợ năng, bật cho \"%s\"." % q.get("chuong_trinh")))
    return ""


CHO_BAT_QUYEN_GIAY = 120          # giây chờ người dùng bật công tắc trong một lần gọi cai_dat_quyen
CHU_KY_QUYEN = 2.0


async def _cai_dat_quyen(p) -> str:
    """Hiện hộp xin quyền của hệ điều hành, mở đúng trang Cài đặt rồi chờ người dùng bật công tắc (macOS không cho phần mềm tự cấp quyền cho chính nó)."""
    import tisa_cai_quyen as CQ
    if p.ten != "macOS":
        return "Windows không có công tắc quyền riêng cho việc điều khiển máy. " + CQ.huong_dan(p, "dieu_khien")
    ds = await asyncio.to_thread(CQ.trang_thai, p)
    thieu_bb = CQ.thieu(ds, True)
    if not thieu_bb:
        return "Đã đủ quyền bắt buộc (Trợ năng và Ghi màn hình). Làm tiếp được." + ((" Còn nên bật thêm: " + ", ".join(x["ten"].split(" (")[0] for x in CQ.thieu(ds)) + ".") if CQ.thieu(ds) else "")
    await asyncio.to_thread(CQ.yeu_cau_he_thong, p)
    for x in thieu_bb[:2]:
        await asyncio.to_thread(CQ.mo_cai_dat, x["id"])
        await asyncio.sleep(1.5)
    t0 = time.time()
    while time.time() - t0 < CHO_BAT_QUYEN_GIAY:
        await asyncio.sleep(CHU_KY_QUYEN)
        ds = await asyncio.to_thread(CQ.trang_thai, p)
        if not CQ.thieu(ds, True):
            return "Người dùng đã bật quyền xong (Trợ năng và Ghi màn hình). Nếu Ghi màn hình vừa bật mà vẫn báo thiếu thì cần thoát và mở lại TISA BOT. Làm tiếp được."
    ds = await asyncio.to_thread(CQ.trang_thai, p)
    return ("CAN_NGUOI_DUNG: Em đã hiện hộp xin quyền và mở sẵn trang Cài đặt nhưng chưa thấy người dùng bật. Hãy hướng dẫn họ TỪNG BƯỚC, cụ thể bấm vào đâu (đọc lại đúng các bước dưới, hỏi họ đang thấy gì trên màn hình nếu họ kẹt), "
            "chờ họ nói xong rồi gọi lại op=cai_dat_quyen để kiểm tra:\n%s" % CQ.huong_dan(p, ds=ds))


async def thuc_hien(op: str, a: dict) -> str:
    op = str(op or "").strip().lower()
    a = a or {}
    p = nen()
    if p is None:
        return "KHONG_HO_TRO: Máy này chưa hỗ trợ điều khiển máy tính (cần macOS hoặc Windows)."
    danh_dau_chat_dung_may()
    with _khoa:
        dung = _tt["dung"]
    if dung and op not in ("status", "permissions", "windows", "front"):
        return "DA_DUNG: Anh đã bấm Dừng AI ngay. Không thao tác tiếp. Nói anh bấm nút Cho AI làm tiếp trong cửa sổ trợ lý nổi (hoặc nhắn \"làm tiếp\"), rồi mới làm."
    if op == "cai_dat_quyen":
        return await _cai_dat_quyen(p)
    if op == "huong_dan_quyen":
        import tisa_cai_quyen as CQ
        ds = await asyncio.to_thread(CQ.trang_thai, p)
        return "Trạng thái quyền: " + "; ".join("%s: %s" % (x["ten"].split(" (")[0], {True: "ĐÃ CÓ", False: "CHƯA", None: "không rõ"}[x["ok"]]) for x in ds) + "\n" + await asyncio.to_thread(CQ.huong_dan, p, str(a.get("ma") or "") or None, ds)
    if p.ten == "macOS" and op not in ("status", "permissions", "windows", "front", "wait") and muc_hien_tai() != "tat":
        q = await asyncio.to_thread(p.quyen)
        if not q.get("tro_nang") or q.get("ghi_man_hinh") is False:
            return ("CAN_QUYEN: macOS chưa cấp quyền (Trợ năng: %s, Ghi màn hình: %s) nên em chưa nhìn và bấm được. ĐỪNG dừng ở câu \"em chưa làm được\": gọi ngay tisa_desktop_do op=cai_dat_quyen "
                    "(TISA BOT hiện hộp xin quyền, mở sẵn trang Cài đặt và chờ), nói người dùng MỘT câu là em cần họ bật công tắc, rồi hướng dẫn họ TỪNG BƯỚC, cụ thể bấm vào đâu, theo đoạn sau:\n%s" %
                    ("đã cấp" if q.get("tro_nang") else "chưa", "đã cấp" if q.get("ghi_man_hinh") is not False else "chưa", _huong_dan_quyen(p)))
    if muc_hien_tai() == "tat" and op not in ("status", "permissions"):
        return ("DA_TAT: Anh chưa cho AI dùng máy tính (mức \"Không cho\"). Không chụp màn hình, không bấm, không mở ứng dụng. "
                "Làm bằng trình duyệt TISA hoặc công cụ khác; cần dùng máy thì xin anh bật ở mục Điều khiển máy tính.")
    if op == "chuot_che_do":
        CR = _mod_chuot(p)
        if CR is None:
            return "Chuột riêng chưa làm cho hệ điều hành này, TISA BOT dùng chuột thật như trước."
        v = str(a.get("che_do") or "").strip().lower()
        if not v:
            return ("Chế độ chuột: %s (rieng = con chuột riêng của TISA BOT, không giành chuột và bàn phím của anh; that = dùng chuột thật như trước). "
                    "Đổi: op=chuot_che_do che_do=rieng|that." % CR.che_do())
        moi = CR.dat_che_do(v)
        _nk(op, "ok", "Chế độ chuột: %s" % moi)
        return ("Đã chuyển sang chế độ chuột %s. " % moi) + ("TISA BOT dùng con chuột riêng (mũi tên cam của TISA BOT), chuột và bàn phím thật của anh không bị động." if moi == "rieng"
                                                           else "TISA BOT dùng chuột và bàn phím thật như trước: lúc nó làm việc anh đừng chạm chuột.")
    if op == "chon_chrome":
        return await asyncio.to_thread(_chon_chrome, a)
    if op == "chon_tep":
        return await asyncio.to_thread(_chon_tep, p, a)
    if op in _OP_AD:
        return await asyncio.to_thread(_cay_tro_nang, p, op, a)
    if op in ("giu_may_thuc", "tha_may", "cho_nguoi_that"):
        return await _viec_dai(p, op, a)
    if op == "mo_khoa":
        # Đường RIÊNG, hẹp, để mở khóa màn hình đăng nhập khi anh ở xa (chốt chặn loginwindow của click/type/key giữ nguyên).
        # Xem tisa_mo_khoa.py: mật khẩu chỉ từ Keychain, chỉ kênh của anh, duyệt từng lần, tối đa 3 lần, có nhật ký.
        try:
            import tisa_mo_khoa
            try:
                import turn_context
                turn = turn_context.current()
            except Exception:  # noqa: BLE001
                turn = None
            return await tisa_mo_khoa.mo_khoa(p, a, muc_hien_tai(), turn)
        except Exception as e:  # noqa: BLE001
            _nk(op, "lỗi", "%s" % type(e).__name__)
            return "LOI: mo_khoa: %s" % type(e).__name__
    try:
        return await asyncio.to_thread(_lam, p, op, a)
    except Exception as e:  # noqa: BLE001
        _nk(op, "lỗi", "%s: %s" % (type(e).__name__, str(e)[:140]))
        return "LOI: %s: %s" % (type(e).__name__, str(e)[:240])



# ---------------------------------------------------------------- (V3.45) cây trợ năng qua agent-desktop: tìm nút theo tên, bấm theo mã
_OP_AD = ("tim", "cay", "cua_so", "cho", "bam_ma", "go_ma", "dat_ma", "chon_ma", "cuon_toi_ma")
_OP_AD_NHIEU = ("tim", "cho", "bam_ma", "go_ma", "dat_ma", "chon_ma", "cuon_toi_ma")   # bước theo mã dùng được trong nhieu_buoc (26/11/2026)
_OP_AD_LAM = {"bam_ma": "click", "go_ma": "type", "dat_ma": "type", "chon_ma": "click", "cuon_toi_ma": "scroll"}


def _cay_tro_nang(p, op: str, a: dict) -> str:
    """Đọc và bấm theo cây trợ năng (tisa_ad). Rẻ token hơn ảnh chụp rất nhiều khi biết cần nút nào. Đi qua đúng các chốt của điều khiển máy."""
    try:
        import tisa_ad as A
    except Exception as e:  # noqa: BLE001
        return "LOI: thiếu mô-đun cây trợ năng (%s). Dùng screenshot + click toạ độ." % type(e).__name__
    if not A.co_san():
        return "KHONG_CO_AD: Máy này chưa có agent-desktop đi kèm TISA BOT. Dùng screenshot + click toạ độ như cũ."
    loi_q = _quyen_loi(p)
    if loi_q:
        return loi_q
    chat = B.chat_hien_tai() if B else ""
    if op in ("tim", "cay", "cua_so", "cho"):
        app = str(a.get("ung_dung") or "").strip() or str(p.ung_dung_truoc() or "")
        if app and _APP_CHAN.search(app):
            _nk(op, "chặn", "Không đọc cây của ứng dụng mật khẩu/ví/ngân hàng: %s" % app)
            return "CAN_NGUOI_DUNG: %s là ứng dụng mật khẩu, ví hoặc ngân hàng: em không đọc nội dung của nó. Anh tự làm." % app
        if op == "cho":
            # 26/11/2026: CHỜ tới khi chữ / cửa sổ / phần tử xuất hiện (agent-desktop wait), thay cho chờ cố định rồi chụp ảnh xem lại.
            try:
                giay = max(1, min(60, int(a.get("giay") or 15)))
            except (TypeError, ValueError):
                giay = 15
            chu, tieu_de = str(a.get("chu") or "").strip(), str(a.get("tieu_de") or "").strip()
            ma_cho = A.ma_day_du(str(a.get("ma") or ""), chat) if a.get("ma") else ""
            if chu:
                dk, mo = ["--text", chu] + (["--app", app] if app else []), "chữ \"%s\"" % chu[:60]
            elif tieu_de:
                dk, mo = ["--window", tieu_de] + (["--app", app] if app else []), "cửa sổ \"%s\"" % tieu_de[:60]
            elif ma_cho:
                dk, mo = ["--element", ma_cho, "--predicate", str(a.get("trang_thai") or "exists")], "phần tử %s" % A._ma_ngan(ma_cho)
            else:
                return "LOI: op=cho cần chu= (chờ chữ xuất hiện), tieu_de= (chờ cửa sổ có tiêu đề này) hoặc ma= (chờ phần tử; trang_thai=exists|enabled|visible|actionable)."
            t0 = time.time()
            d = A.chay(["wait"] + dk + ["--timeout", str(giay * 1000)], giay + 10)
            gs = time.time() - t0
            if not d.get("ok"):
                _nk(op, "quá giờ", "Chờ %s trong %s: %s" % (mo, app, A.loi_ngan(d)[:80]))
                return "QUA_GIO: sau %d giây chưa thấy %s trong %s (%s). Thử op=tim xem giao diện đang ở đâu, hoặc chờ lâu hơn (giay=)." % (giay, mo, app or "ứng dụng đang ở trước", A.loi_ngan(d)[:120])
            _nk(op, "ok", "Đã thấy %s trong %s sau %.1f giây" % (mo, app, gs))
            return "DA_THAY: đã thấy %s trong %s sau %.1f giây. Làm tiếp (tìm nút bằng op=tim nếu cần mã mới)." % (mo, app or "ứng dụng đang ở trước", gs)
        if op == "cua_so":
            d = A.chay(["list-windows"] + (["--app", app] if app else []), 15)
            if not d.get("ok"):
                return A.loi_ngan(d)
            ws = d.get("data")
            ws = ws if isinstance(ws, list) else (ws or {}).get("windows", [])
            return "Cửa sổ%s:\n" % ((" của " + app) if app else "") + "\n".join("- %s: %s \"%s\"" % (w.get("id"), w.get("app_name"), str(w.get("title") or "")[:70]) for w in ws[:40])
        g = ["--app", app] if app else []
        if a.get("cua_so"):
            g += ["--window-id", str(a["cua_so"])]
        if op == "tim":
            g2 = []
            for k, co in (("ten", "--name"), ("vai_tro", "--role"), ("chu", "--text"), ("gia_tri", "--value")):
                if str(a.get(k) or "").strip():
                    g2 += [co, str(a[k]).strip()]
            if not g2:
                return "LOI: op=tim cần ít nhất ten=, chu= hoặc vai_tro= (ví dụ ten=\"Mở\" vai_tro=button)."
            vung = str(a.get("vung") or "").strip()
            d = A.chay(["find"] + g + g2 + (["--surface", vung] if vung else []), 20)
            if not d.get("ok"):
                return A.loi_ngan(d)
            A.ghi_anh_xa(d, chat)
            data = d.get("data") or {}
            ms = data.get("matches") or []
            if not ms:
                _nk(op, "không thấy", "Tìm %s trong %s" % (" ".join(g2[1::2])[:60], app))
                return "KHONG_THAY: không có phần tử khớp trong %s. Thử chu= (tìm theo chữ), bỏ vai_tro, hoặc op=cay để xem gọn cả cửa sổ." % (app or "ứng dụng đang ở trước")
            dong = []
            for m in ms[:25]:
                duong = [x for x in (m.get("path") or []) if ":" in x][-1:] if m.get("path") else []
                dong.append(A._mot_dong(m) + (("  · trong " + duong[0].split(":", 1)[1][:40]) if duong else ""))
            _nk(op, "ok", "Tìm %s trong %s: %d" % (" ".join(g2[1::2])[:60], app, len(ms)))
            return ("Kết quả tìm trong %s (%d%s). Bấm/gõ bằng mã ở đầu dòng: tisa_desktop_do op=bam_ma ma=<mã>, op=go_ma ma=<mã> text=...\n" %
                    (app or "ứng dụng đang ở trước", data.get("total_matches") or len(ms), ", đã cắt bớt" if data.get("truncated") else "")) + "\n".join(dong)
        goc = A.ma_day_du(str(a.get("goc") or ""), chat) if a.get("goc") else ""
        if goc:
            g = ["--root", goc]
        args = ["snapshot"] + g + ["-i", "--compact"] + (["--skeleton"] if not goc and not a.get("day_du") else [])
        d = A.chay(args, 30)
        if not d.get("ok"):
            return A.loi_ngan(d)
        A.ghi_anh_xa(d, chat)
        chu, n = A.cay_thanh_chu(d)
        _nk(op, "ok", "Đọc cây %s%s: %d dòng" % (app, " (vùng)" if goc else "", n))
        return ("Cây trợ năng của %s%s (mã ở đầu dòng dùng cho op=bam_ma/go_ma; {N con} = vùng đọc thêm bằng op=cay goc=<mã>):\n" %
                (app or "ứng dụng đang ở trước", " - vùng " + str(a.get("goc")) if goc else "")) + chu
    # ---- làm theo mã
    ma = A.ma_day_du(str(a.get("ma") or ""), chat)
    if not ma:
        return "LOI: thiếu ma (lấy từ op=tim hoặc op=cay, ví dụ ma=e8). Chưa tìm lần nào trong ô chat này thì gọi tisa_desktop_look op=tim trước."
    tt = A.ung_dung_cua_ma(ma)
    app = tt.get("app") or str(a.get("ung_dung") or "")
    tuong = _OP_AD_LAM[op]
    loai, mo_ta = phan_loai(tuong, {"text": a.get("text") or "", "key": ""}, app)
    if loai == "vo_hai" and tuong == "click" and _TIEN_CUA_SO.search(tt.get("cua_so") or ""):
        loai, mo_ta = "bi_mat", "Cửa sổ đang ở bước tiền bạc (thanh toán, mua, nạp, nâng gói): \"%s\". Người dùng tự bấm." % (tt.get("cua_so") or "")[:60]
    kq = _can_duyet(op, a, app, loai, mo_ta)
    if kq:
        return kq
    if tuong == "type":
        kq = _chong_chen(op, a, app)
        if kq:
            return kq
    text = str(a.get("text") or "")
    if op == "bam_ma":
        lenh = {"doi": "double-click", "phai": "right-click"}.get(str(a.get("kieu") or "").lower(), "click")
        d = A.chay([lenh, ma], 20)
    elif op == "go_ma":
        if not text:
            return "LOI: thiếu text."
        d = A.chay(["type", ma, "--stdin"], 30, nhap=text)       # chữ đi qua stdin, không nằm trong tham số tiến trình
    elif op == "dat_ma":
        d = A.chay(["set-value", ma, "--stdin"], 30, nhap=text)
    elif op == "chon_ma":
        if not text:
            return "LOI: thiếu text (giá trị cần chọn)."
        d = A.chay(["select", ma, text], 20)
    else:
        d = A.chay(["scroll-to", ma], 20)
    if not d.get("ok"):
        _nk(op, "lỗi", A.loi_ngan(d)[:150], ma)
        return A.loi_ngan(d)
    viec = {"bam_ma": "bấm", "go_ma": "gõ %d ký tự vào" % len(text), "dat_ma": "đặt giá trị cho", "chon_ma": "chọn \"%s\" ở" % text[:40], "cuon_toi_ma": "cuộn tới"}[op]
    _nk(op, "ok", "Đã %s %s trong %s (cây trợ năng)" % (viec, A._ma_ngan(ma), app), A._ma_ngan(ma))
    return ("Đã %s %s trong %s (không di chuột thật, không giành cửa sổ). Kiểm lại bằng op=tim (rẻ) thay vì screenshot; giao diện đã đổi thì mã cũ hết hạn, tìm lại." %
            (viec, A._ma_ngan(ma), app or "ứng dụng"))


def danh_dau_chat_dung_may() -> None:
    """(V3.44) Ghi lại ô chat nào vừa điều khiển máy tính, để khung Trình duyệt của ô chat đó (kể cả mở ở máy khác) chuyển sang xem màn hình máy chủ."""
    if B is None:
        return
    try:
        c = B.chat_hien_tai()
        if c:
            with B._khoa:
                B._tab_chat.setdefault(c, {"tab": "", "tabs": []})["may_luc"] = time.time()
    except Exception:  # noqa: BLE001
        pass


def chat_vua_dung_may(chat: str, giay: float = 120) -> bool:
    if B is None or not chat:
        return False
    return time.time() - float((B._tab_chat.get(chat) or {}).get("may_luc") or 0) < giay


def _hop_chon_tep_mo(front: str) -> bool:
    """Ứng dụng `front` (trình duyệt) đang mở hộp chọn tệp của hệ thống? Chỉ macOS."""
    if sys.platform != "darwin":
        return False
    try:
        import tisa_hop_thoai as H
        if front and front not in H.CHROME:
            return False
        h = H.tim_hop_chon_tep(front or "")
        if h:
            h["cay"].dong()
        return bool(h)
    except Exception:  # noqa: BLE001
        return False


def _chon_tep(p, a: dict) -> str:
    """Hộp chọn tệp (Mở / Tải lên) của hệ thống đang mở: đi tới đường dẫn, chọn tệp, bấm Mở. Bàn phím thường không vào được hộp này (nó chạy ở tiến trình riêng)."""
    if p.ten != "macOS":
        return "CHUA_HO_TRO: op=chon_tep mới làm cho macOS. Trên Windows dùng tisa_browser_do op=upload (không cần hộp chọn tệp)."
    import tisa_hop_thoai as H
    ung = str(a.get("ung_dung") or "").strip()
    if a.get("huy"):
        kq = H.huy_hop_chon_tep(ung)
        _nk("chon_tep", kq, "Huỷ hộp chọn tệp")
        return {"ok": "Đã bấm Huỷ trên hộp chọn tệp.", "khong_co": "Không có hộp chọn tệp nào đang mở."}.get(kq, "LOI: không bấm được Huỷ.")
    duong = str(a.get("path") or a.get("duong_dan") or "").strip()
    loai, mo_ta = ("can_duyet", "Chọn tệp %s để tải lên" % duong) if muc_hien_tai() == "hoi_het" else ("vo_hai", "")
    kq = _can_duyet("chon_tep", a, ung or "trình duyệt", loai, mo_ta)
    if kq:
        return kq
    kq = H.chon_tep(duong, bool(a.get("tat_ca")), ung, a.get("bam_mo") is not False)
    _nk("chon_tep", "ok" if not kq.startswith(("LOI", "KHONG", "CHUA")) else "lỗi", kq[:160], duong[-60:])
    return kq


def _chon_chrome(a: dict) -> str:
    """Xem hoặc ĐỔI hồ sơ Chrome TISA BOT được dùng. Đổi: chỉ từ kênh của anh và LUÔN cần anh duyệt (đổi hồ sơ là đổi tài khoản đang đăng nhập), kể cả Toàn quyền."""
    import tisa_chong_chen as CC
    ten = str(a.get("ho_so") or "").strip()
    ghim = CC.doc_da_chon()
    if not ten:
        ds = CC.liet_ke_ho_so()
        return "Hồ sơ Chrome đã chọn: %s. Các hồ sơ có: %s. Đổi: op=chon_chrome ho_so=<tên> (anh phải bấm Duyệt)." % (
            ("%s (%s)" % (ghim["ten"], ghim["thu_muc"])) if ghim else "CHƯA CHỌN", ", ".join("%s (%s)" % (x["ten"] or x["thu_muc"], x["thu_muc"]) for x in ds) or "không đọc được")
    h = CC.tim_ho_so(ten)
    if not h:
        return "LOI: không thấy hồ sơ Chrome \"%s\"." % ten
    if ghim and ghim["thu_muc"] == h["thu_muc"]:
        return "Hồ sơ \"%s\" đang là hồ sơ đã chọn rồi." % (h["ten"] or h["thu_muc"])
    try:
        import turn_context
        turn = turn_context.current()
    except Exception:  # noqa: BLE001
        turn = None
    import tisa_mo_khoa as MK
    ok, kenh, ly = MK.kiem_kenh(turn)
    if not ok:
        _nk("chon_chrome", "từ chối", ly[:100])
        return "TU_CHOI: Đổi hồ sơ Chrome chỉ làm khi chính anh nhắn từ dashboard hoặc Zalo của anh. %s" % ly
    if B is None:
        return "LOI: thiếu mô-đun duyệt."
    nc = {"host": "Máy tính", "url": "", "tag": "", "ten": ("chon_chrome: %s" % (h["ten"] or h["thu_muc"]))[:100], "tieu_de": "chrome"}
    if not B.dung_duyet(str(a.get("duyet_id") or ""), "may_chon_chrome", nc):
        k = B.xin_duyet("may_chon_chrome", nc, "Chọn hồ sơ Chrome \"%s\" cho TISA BOT dùng (kênh %s)" % (h["ten"] or h["thu_muc"], kenh))
        return ("CAN_DUYET: Chọn hồ sơ Chrome \"%s\" cho TISA BOT dùng từ giờ (mọi lần mở trang đều vào hồ sơ này). Anh phải bấm Duyệt trong TISA BOT. "
                "Gọi lại op=chon_chrome ho_so=\"%s\" duyet_id=\"%s\" sau khi anh duyệt." % (h["ten"] or h["thu_muc"], ten, k))
    r = CC.dat_da_chon(ten)
    _nk("chon_chrome", "đã đổi" if r["ok"] else "lỗi", "Hồ sơ Chrome đã chọn: %s (kênh %s)" % (h["ten"] or h["thu_muc"], kenh))
    return ("Đã chọn hồ sơ Chrome \"%s\". Từ giờ TISA BOT chỉ mở trang trong hồ sơ này." % (h["ten"] or h["thu_muc"])) if r["ok"] else "LOI: %s" % r["loi"]


def _quay_chup(p, op: str, a: dict) -> str:
    """Chụp theo cửa sổ/vùng, quay màn hình, lưu vào brain 04-ket-qua/<YYYY-MM>/<ngày>-<mô tả>/ (tisa_quay_man_hinh.py)."""
    import tisa_quay_man_hinh as Q
    if op == "quay_trang_thai":
        return json.dumps(Q.trang_thai(), ensure_ascii=False)
    if op == "quay_dung":
        ok, kq = Q.quay_dung()
        _nk(op, "ok" if ok else "lỗi", "Dừng quay: %s" % (Path(kq).name if ok else kq[:80]))
        return ("Đã dừng quay. Video lưu ở: %s" % kq) if ok else "LOI: %s" % kq
    front = str(p.ung_dung_truoc() or "")
    if _APP_CHAN.search(front):
        _nk(op, "chờ người dùng", "Cửa sổ mật khẩu, ví, ngân hàng (%s)" % front)
        return "CAN_NGUOI_DUNG: Đang ở cửa sổ mật khẩu, khóa, ví hoặc ngân hàng (%s): không quay, không chụp lưu lại. Anh tự làm." % front
    vung = None
    try:
        if a.get("w") is not None and a.get("h") is not None:
            vung = (int(a.get("x") or 0), int(a.get("y") or 0), int(a["w"]), int(a["h"]))
    except (TypeError, ValueError):
        return "LOI: x, y, w, h phải là số."
    mo_ta = str(a.get("mo_ta") or ("quay-man-hinh" if op == "quay_bat" else "chup-man-hinh"))
    ung_dung = str(a.get("ung_dung") or "").strip()
    if op == "chup_cua_so":
        ok, kq = Q.chup_cua_so(_VAULT["root"], mo_ta, ung_dung, vung)
        _nk(op, "ok" if ok else "lỗi", ("Chụp %s" % (ung_dung or "vùng")) if ok else kq[:80])
        return ("Đã chụp %s. Ảnh lưu ở: %s\n%s%s\u27e7" % (ung_dung or "vùng đã chọn", kq, _DAU_ANH, kq)) if ok else "LOI: %s" % kq
    giay = int(a.get("giay") or 60)
    ok, kq = Q.quay_bat(_VAULT["root"], mo_ta, giay, ung_dung, vung, str(a.get("engine") or "screencapture").lower(), bool(a.get("am_thanh")))
    _nk(op, "ok" if ok else "lỗi", ("Bắt đầu quay %d giây" % giay) if ok else kq[:80])
    return ("Đang quay (tối đa %d giây, tự dừng). Video sẽ lưu ở: %s. Muốn dừng sớm gọi op=quay_dung." % (min(giay, Q.TOI_DA_GIAY), kq)) if ok else "LOI: %s" % kq


def _gan_moc_thuc_giac(p, loop) -> None:
    """Cho tisa_thuc_giac biết cách xem máy có khóa không và cách mở khóa lại (chỉ dùng khi phiên giữ thức được cấp quyền)."""
    import tisa_thuc_giac as TG
    import tisa_mo_khoa as MK
    import tisa_bao_anh as BA
    TG.MOC["ung_dung_truoc"] = p.ung_dung_truoc
    TG.MOC["mo_khoa"] = lambda kenh: MK.mo_khoa_tu_dong(p, kenh, lambda t: BA.bao(t, loop))
    TG.MOC["bao"] = lambda t: BA.bao(t, loop)


async def _viec_dai(p, op: str, a: dict) -> str:
    """giu_may_thuc (caffeinate cho việc nền dài, tùy chọn tự mở khóa lại), tha_may, cho_nguoi_that (báo anh rồi chờ anh làm xong rồi làm tiếp)."""
    import tisa_thuc_giac as TG
    import tisa_bao_anh as BA
    loop = asyncio.get_running_loop()
    if op == "tha_may":
        ma = str(a.get("ma") or "").strip()
        if ma:
            ok = TG.tha(ma)
            _nk(op, "ok" if ok else "không thấy", "Tắt giữ thức phiên %s" % ma)
            return "Đã tắt giữ thức phiên %s." % ma if ok else "Không thấy phiên %s (đã hết hạn hoặc đã tắt)." % ma
        for x in TG.danh_sach():
            TG.tha(x["ma"])
        _nk(op, "ok", "Tắt mọi phiên giữ thức")
        return "Đã tắt mọi phiên giữ thức."
    if op == "giu_may_thuc":
        ly_do = str(a.get("ly_do") or "việc nền dài")[:100]
        phut = max(1, min(int(a.get("phut") or 240), 720))
        uy = ""
        if a.get("tu_mo_khoa"):
            import tisa_mo_khoa as MK
            try:
                import turn_context
                turn = turn_context.current()
            except Exception:  # noqa: BLE001
                turn = None
            ok, kenh, ly = MK.kiem_kenh(turn)
            if not ok:
                MK._ghi(kenh, "từ chối (giữ thức + mở khóa)", ly)
                return "TU_CHOI: Quyền tự mở khóa lại giữa việc nền chỉ cấp được khi chính anh nhắn từ dashboard TISA BOT hoặc Zalo của anh. %s" % ly
            if muc_hien_tai() != "toan_quyen":
                if B is None:
                    return "LOI: thiếu mô-đun duyệt."
                nc = {"host": "Máy tính", "url": "", "tag": "", "ten": ("giu_may_thuc+mo_khoa: %d phút (kênh %s)" % (phut, kenh))[:100], "tieu_de": "may"}
                if not B.dung_duyet(str(a.get("duyet_id") or ""), "may_giu_thuc_mo_khoa", nc):
                    k = B.xin_duyet("may_giu_thuc_mo_khoa", nc, "Giữ máy thức %d phút và CHO PHÉP TISA BOT tự mở khóa máy nếu khóa giữa chừng (kênh %s)" % (phut, kenh))
                    return ("CAN_DUYET: Cho phép tự mở khóa lại giữa việc nền (tối đa %d phút, 3 lần thử, mật khẩu lấy từ Keychain). Anh phải bấm Duyệt trong TISA BOT. "
                            "Gọi lại op=giu_may_thuc tu_mo_khoa=true duyet_id=\"%s\" sau khi anh duyệt." % (phut, k))
            uy = kenh
            _gan_moc_thuc_giac(p, loop)
        ma = TG.giu(ly_do, phut, uy)
        _nk(op, "ok", "Giữ máy thức %d phút%s" % (phut, " + được mở khóa lại (kênh %s)" % uy if uy else ""))
        return "Đã giữ máy thức tối đa %d phút (mã phiên %s)%s. Xong việc gọi op=tha_may ma=%s." % (phut, ma, (", được tự mở khóa lại nếu máy khóa (kênh %s)" % uy) if uy else "", ma)
    # cho_nguoi_that
    ly_do = str(a.get("ly_do") or "một bước chỉ anh làm được (Touch ID, mã khóa, CAPTCHA, OTP)")[:120]
    phut = max(1, min(int(a.get("phut") or 10), 30))
    truoc = str(await asyncio.to_thread(p.ung_dung_truoc) or "")
    chan = bool(re.search(r"loginwindow|securityagent|coreautha|touch ?id|usernotification", truoc, re.I) or _APP_CHAN.search(truoc))

    def het_chan():
        return chan and str(p.ung_dung_truoc() or "") != truoc

    xong = (lambda: bool(B and B._tt.pop("nguoi_xong", False))) if B is not None and hasattr(B, "_tt") else None
    dung = lambda: bool(_tt.get("dung"))   # noqa: E731
    _nk(op, "đang chờ anh", ly_do)
    kq = await asyncio.to_thread(BA.cho_nguoi_that, het_chan, ly_do, phut, loop, dung, xong)
    _nk(op, kq.lower(), ly_do)
    if kq in ("XONG", "ANH_BAO_XONG"):
        return "Anh đã làm xong (%s). Chụp màn hình kiểm tra rồi làm tiếp đúng chỗ đang dở." % ("ứng dụng ở trước đã đổi" if kq == "XONG" else "anh bấm Em làm xong rồi")
    if kq == "DA_DUNG":
        return "DA_DUNG: Anh đã bấm Dừng AI ngay."
    return "HET_GIO: Chờ %d phút chưa thấy anh làm xong (đã báo anh). Gọi lại op=cho_nguoi_that để chờ tiếp, hoặc hỏi anh." % phut


_DAU_ANH = "⟦ANH:"        # mcp_hub tách dòng này ra thành ảnh gửi thẳng cho AI (tisa_anh_tool.py)
_CANH_TOI_DA = 1280       # cạnh dài tối đa của ảnh đưa cho AI (V3.20: 1600 -> 1280, ít chữ ảnh hơn nên AI đọc nhanh hơn; ảnh to hơn bị AI tự thu nhỏ làm lệch toạ độ)


def _mod_chuot(p):
    """Mô-đun chuột riêng hợp với nền: macOS -> tisa_chuot_rieng, Windows -> tisa_chuot_rieng_win (cùng giao diện). Không có thì None."""
    try:
        if isinstance(p, _Mac):
            import tisa_chuot_rieng as M
            return M
        if isinstance(p, _Win):
            import tisa_chuot_rieng_win as M
            return M
    except Exception:  # noqa: BLE001
        pass
    return None


def _rieng_bat(p) -> bool:
    """Chuột riêng: TISA BOT gửi thao tác thẳng vào cửa sổ, KHÔNG động tới con trỏ và bàn phím thật của anh (tisa_chuot_rieng.py cho macOS, tisa_chuot_rieng_win.py
    cho Windows). Chỉ nền thật; đối tượng giả (bài kiểm thử) luôn đi đường cũ, không bao giờ chạm cửa sổ thật."""
    M = _mod_chuot(p)
    if M is None:
        return False
    try:
        return M.che_do() == "rieng" and bool(M.dung_duoc())
    except Exception:  # noqa: BLE001
        return False


def _chup_nhanh(p, ung_dung: str = "") -> dict:
    """Chụp để đưa cho AI, NHANH: {f, w, h, ti_le, ms, cua_so}. ung_dung: chỉ chụp cửa sổ đó, kể cả khi bị che; toạ độ trong ảnh khi đó là toạ độ TRONG cửa sổ."""
    t0 = time.time()
    ANH.mkdir(parents=True, exist_ok=True)
    f = ANH / (time.strftime("%Y%m%d-%H%M%S") + "-%03d.jpg" % (int(t0 * 1000) % 1000))
    goc = ANH / "goc.jpg"
    cua_so = None
    w2 = h2 = 0
    ti_le = 1.0
    nhanh = None
    if sys.platform == "darwin":
        try:
            import tisa_chup_nhanh as QN
        except Exception:  # noqa: BLE001
            QN = None
    else:
        QN = None
    if ung_dung:
        CR = _mod_chuot(p)
        if CR is None:
            raise RuntimeError("chụp riêng cửa sổ chưa làm cho hệ điều hành này")
        cua_so = CR.tim_cua_so(ung_dung)
        if not cua_so:
            raise RuntimeError("không thấy cửa sổ của \"%s\" (chưa mở, đã thu nhỏ, hoặc nằm ở màn hình ảo khác). Gọi op=windows xem tên đúng." % ung_dung)
        if sys.platform == "win32":
            if not CR.chup_cua_so_id(cua_so["id"], f):
                raise RuntimeError("Chụp cửa sổ lỗi (cửa sổ này không cho chụp khi bị che, hoặc ảnh đen). Đưa cửa sổ ra trước rồi chụp thường.")
            w2, h2, _k = _thu_nho_anh(f, int(cua_so["w"]), int(cua_so["h"]))
        else:
            if QN is not None:
                nhanh = QN.chup(f, _CANH_TOI_DA, goc, 0.74, cua_so["id"])
            if nhanh:
                w2, h2 = nhanh[2], nhanh[3]
            else:
                rc, _, err = p._chay(["screencapture", "-x", "-o", "-l", str(cua_so["id"]), str(f)], 15)
                if rc != 0 or not f.exists():
                    raise RuntimeError("Chụp cửa sổ lỗi: %s" % (err or "chưa cấp quyền Ghi màn hình"))
                w2, h2, _k = _thu_nho_anh(f, int(cua_so["w"]), int(cua_so["h"]))
        ti_le = float(cua_so["w"]) / max(1, w2)
        with _khoa:
            _tt.setdefault("cua_so_anh", {})[ung_dung.strip().lower()] = {"id": cua_so["id"], "ti_le": ti_le, "luc": time.time()}
    else:
        if QN is not None:
            nhanh = QN.chup(f, _CANH_TOI_DA, goc, 0.74, 0)
        if nhanh:
            wp, hp = p.kich_thuoc()
            w2, h2 = nhanh[2], nhanh[3]
            ti_le = float(wp) / max(1, w2)
        else:
            w, h = p.chup(f)
            w2, h2, ti_le = _thu_nho_anh(f, w, h)
        with _khoa:
            _tt["ti_le"] = ti_le
    for x in sorted(ANH.glob("2*.jpg"))[:-30]:
        try:
            x.unlink()
        except OSError:
            pass
    try:
        with open(ANH / "moi-nhat.txt", "w", encoding="utf-8") as fh:
            fh.write(str(f))
    except OSError:
        pass
    return {"f": f, "w": w2, "h": h2, "ti_le": ti_le, "ms": int((time.time() - t0) * 1000), "cua_so": cua_so, "nhanh": bool(nhanh)}


def _chu_anh(p, k: dict, day_du: bool = True) -> str:
    cs = k.get("cua_so")
    if day_du:
        goc = ("Ảnh chụp %s đã lưu: %s. Kích thước %dx%d, tọa độ (x,y) trong ảnh đúng bằng tọa độ để bấm (gốc ở góc trên trái)%s. "
               "Ảnh được gửi kèm ngay bên dưới để nhìn rồi mới bấm; chữ nhỏ khó đọc thì gọi tisa_desktop_look op=zoom x y x2 y2 để phóng to một vùng. "
               "Nếu KHÔNG thấy ảnh kèm theo thì nói thật với anh là em chưa nhìn được màn hình, đừng đoán nội dung." %
               ("cửa sổ " + str(cs["ung_dung"]) if cs else "màn hình", k["f"], k["w"], k["h"], (" (khi bấm vào cửa sổ này nhớ truyền ung_dung=\"%s\")" % cs["ung_dung"]) if cs else ""))
    else:
        goc = "Ảnh sau thao tác (tự chụp, %d ms), %dx%d%s:" % (k["ms"], k["w"], k["h"], (", cửa sổ " + str(cs["ung_dung"])) if cs else "")
    return "%s Ứng dụng đang ở trước: %s.\n%s%s\u27e7" % (goc, p.ung_dung_truoc() or "không rõ", _DAU_ANH, k["f"])


def _thu_nho_anh(f, w, h):
    """Giữ bản gốc ở goc.jpg (để phóng to), thu ảnh f về tối đa _CANH_TOI_DA. Trả (rộng, cao, tỉ lệ thật/ảnh): toạ độ trong ảnh nhân tỉ lệ ra toạ độ bấm."""
    try:
        from PIL import Image
    except Exception:  # noqa: BLE001
        return w, h, 1.0
    try:
        with Image.open(str(f)) as im:
            im = im.convert("RGB")
            im.save(str(ANH / "goc.jpg"), "JPEG", quality=88)
            k = max(im.size) / float(_CANH_TOI_DA)
            if k > 1.0:
                nw, nh = max(1, round(im.size[0] / k)), max(1, round(im.size[1] / k))
                im.resize((nw, nh), Image.LANCZOS).save(str(f), "JPEG", quality=80)
                return nw, nh, im.size[0] / float(nw)
            im.save(str(f), "JPEG", quality=80)
        return w, h, 1.0
    except Exception:  # noqa: BLE001
        return w, h, 1.0


def _phong_to(a: dict) -> str:
    try:
        import tisa_chup_nhanh as _QN
        _QN.cho_goc()
    except Exception:  # noqa: BLE001
        pass
    """op=zoom x y x2 y2 (toạ độ theo ảnh chụp gần nhất): cắt vùng đó từ bản gốc, phóng to để đọc chữ nhỏ."""
    goc = ANH / "goc.jpg"
    if not goc.is_file():
        return "LOI: chưa có ảnh chụp. Gọi tisa_desktop_look op=screenshot trước rồi mới phóng to."
    try:
        from PIL import Image
    except Exception:  # noqa: BLE001
        return "LOI: máy này thiếu Pillow nên chưa phóng to được. Chụp lại màn hình rồi nhìn ảnh gốc."
    with _khoa:
        k = float(_tt.get("ti_le") or 1.0)
    try:
        x, y, x2, y2 = (int(a[t]) for t in ("x", "y", "x2", "y2"))
    except Exception:  # noqa: BLE001
        return "LOI: thiếu vùng cần phóng to: x y x2 y2 (góc trên trái và góc dưới phải, theo toạ độ ảnh chụp)."
    with Image.open(str(goc)) as im:
        W, H = im.size
        l, t, r, b = sorted((x, x2))[0], sorted((y, y2))[0], sorted((x, x2))[1], sorted((y, y2))[1]
        box = (max(0, round(l * k)), max(0, round(t * k)), min(W, round(r * k)), min(H, round(b * k)))
        if box[2] - box[0] < 8 or box[3] - box[1] < 8:
            return "LOI: vùng phóng to quá nhỏ hoặc nằm ngoài màn hình."
        c = im.crop(box).convert("RGB")
        m = max(c.size)
        if m < 1200:
            e = min(4.0, 1200.0 / m)
            c = c.resize((round(c.size[0] * e), round(c.size[1] * e)), Image.LANCZOS)
        elif m > _CANH_TOI_DA:
            e = _CANH_TOI_DA / float(m)
            c = c.resize((round(c.size[0] * e), round(c.size[1] * e)), Image.LANCZOS)
        f = ANH / (time.strftime("z%Y%m%d-%H%M%S") + ".jpg")
        c.save(str(f), "JPEG", quality=85)
    for old in sorted(ANH.glob("z*.jpg"))[:-8]:
        try:
            old.unlink()
        except OSError:
            pass
    _nk("zoom", "ok", "Phóng to vùng (%d,%d)-(%d,%d)" % (x, y, x2, y2))
    return "Ảnh phóng to vùng (%d,%d)-(%d,%d), gửi kèm bên dưới.\n%s%s\u27e7" % (x, y, x2, y2, _DAU_ANH, f)


def _lam(p, op: str, a: dict) -> str:
    if op == "status":
        return json.dumps(dict(trang_thai(), may_dang_dieu_khien=_MAY_NAY), ensure_ascii=False)
    if op == "permissions":
        q = p.quyen()
        return "Hệ điều hành: %s. Quyền điều khiển (Trợ năng): %s. Quyền ghi màn hình: %s. Chương trình cần cấp quyền: %s" % (
            p.ten, "ĐÃ CẤP" if q.get("tro_nang") else "CHƯA", {True: "ĐÃ CẤP", False: "CHƯA", None: "không rõ"}[q.get("ghi_man_hinh")], q.get("chuong_trinh"))
    if op == "front":
        return "Ứng dụng đang ở trước: %s. Cửa sổ: %s" % (p.ung_dung_truoc() or "không rõ", p.tieu_de_cua_so() or "không rõ")
    if op == "windows":
        return "Ứng dụng đang mở:\n" + "\n".join("- " + x for x in p.liet_ke_ung_dung()) + "\nỨng dụng ở trước: %s" % (p.ung_dung_truoc() or "không rõ")
    if op == "screenshot":
        try:
            k = _chup_nhanh(p, str(a.get("ung_dung") or "").strip())
        except RuntimeError as e:
            return "LOI: %s" % e
        _nk("screenshot", "ok", "Chụp %s %dx%d (%d ms%s)" % ("cửa sổ" if k["cua_so"] else "màn hình", k["w"], k["h"], k["ms"], ", nhanh" if k["nhanh"] else ""))
        return _chu_anh(p, k, True)
    if op == "zoom":
        return _phong_to(a)
    if op == "wait":
        time.sleep(min(max(int(a.get("ms") or 1000), 100), 10000) / 1000)
        return "Đã chờ."
    if op == "kiem_chen":
        import tisa_chong_chen as CC
        kq = CC.phat_hien()
        _nk(op, "ok", "Kiểm chen ngang: %d cứng, %d mềm" % (len(kq["cung"]), len(kq["mem"])))
        if not kq["cung"] and not kq["mem"]:
            return "Không thấy thứ gì khác đang điều khiển trình duyệt. Gõ vào Chrome được."
        return "Thứ đang điều khiển trình duyệt (CHẶN gõ): %s. Chỉ báo (không chặn): %s." % ("; ".join(kq["cung"]) or "không có", "; ".join(kq["mem"]) or "không có")
    if op in ("chup_cua_so", "quay_bat", "quay_dung", "quay_trang_thai"):
        return _quay_chup(p, op, a)
    if op == "nhieu_buoc":
        return _nhieu_buoc(p, a)
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
    rieng = _rieng_bat(p)
    CR = _mod_chuot(p) if rieng else None
    w, h = p.kich_thuoc()
    with _khoa:
        ti_le = float(_tt.get("ti_le") or 1.0)
    sw, sh = int(round(w / ti_le)), int(round(h / ti_le))        # kích thước ảnh chụp mà AI đang nhìn
    ung_dung_chi = str(a.get("ung_dung") or "").strip()
    muc_tieu = None        # cửa sổ đích khi dùng chuột riêng: {id, pid, ung_dung, tieu_de, x, y, w, h}
    diem = {}              # toạ độ màn hình (điểm) đã đổi từ toạ độ AI đưa ra

    def toa_do(kx="x", ky="y"):
        """Toạ độ màn hình (điểm). Có ung_dung thì toạ độ AI đưa là toạ độ TRONG ảnh chụp cửa sổ đó (chụp bằng screenshot ung_dung=...)."""
        if a.get(kx) is None or a.get(ky) is None:
            raise RuntimeError("thiếu toạ độ %s,%s (lấy từ ảnh chụp màn hình)" % (kx, ky))
        x, y = int(a[kx]), int(a[ky])
        if ung_dung_chi and rieng:
            with _khoa:
                ca = (_tt.get("cua_so_anh") or {}).get(ung_dung_chi.lower())
            if not ca:
                raise RuntimeError("chưa chụp cửa sổ \"%s\": gọi tisa_desktop_look op=screenshot ung_dung=\"%s\" trước, rồi bấm theo toạ độ trong ảnh đó" % (ung_dung_chi, ung_dung_chi))
            cs = muc_tieu or CR.tim_cua_so(ung_dung_chi)
            if not cs:
                raise RuntimeError("không thấy cửa sổ của \"%s\" (đã đóng hoặc thu nhỏ)" % ung_dung_chi)
            return cs["x"] + x * ca["ti_le"], cs["y"] + y * ca["ti_le"]
        if not (0 <= x < sw and 0 <= y < sh):
            raise RuntimeError("toạ độ (%d,%d) nằm ngoài ảnh chụp %dx%d" % (x, y, sw, sh))
        return min(w - 1, int(round(x * ti_le))), min(h - 1, int(round(y * ti_le)))

    if rieng and op in ("click", "double_click", "right_click", "drag", "scroll", "move", "type", "key"):
        try:
            if op in ("click", "double_click", "right_click", "drag", "move") or (op == "scroll" and a.get("x") is not None):
                muc_tieu = CR.tim_cua_so(ung_dung_chi) if ung_dung_chi else None
                x0, y0 = toa_do()
                diem["x"], diem["y"] = x0, y0
                if muc_tieu is None:
                    muc_tieu = CR.cua_so_tai(x0, y0)
            elif op == "scroll":
                muc_tieu = CR.tim_cua_so(ung_dung_chi) if ung_dung_chi else None
                if muc_tieu is None:
                    mt = CR.muc_tieu()
                    muc_tieu = next((c for c in CR.liet_ke_cua_so() if c["id"] == mt.get("id")), None) if mt else None
                if muc_tieu:
                    diem["x"], diem["y"] = muc_tieu["x"] + muc_tieu["w"] / 2, muc_tieu["y"] + muc_tieu["h"] / 2
            else:        # type, key: vào cửa sổ chỉ định, hoặc cửa sổ vừa bấm gần nhất
                if ung_dung_chi:
                    muc_tieu = CR.tim_cua_so(ung_dung_chi)
                else:
                    mt = CR.muc_tieu()
                    muc_tieu = next((c for c in CR.liet_ke_cua_so() if c["id"] == mt.get("id")), None) if mt else None
        except RuntimeError as e:
            return "LOI: %s" % e
        if muc_tieu is None:
            if op in ("type", "key"):
                return ("CHUA_CO_DICH: Đang ở chế độ chuột riêng nên em không gõ vào ứng dụng anh đang dùng. Bấm vào ô cần gõ trước (click x y), hoặc truyền "
                        "ung_dung=\"tên ứng dụng\" để chỉ cửa sổ cần gõ. Muốn dùng bàn phím thật như trước thì op=chuot_che_do che_do=that.")
            return "LOI: không thấy cửa sổ nào tại điểm đó (có thể bị thu nhỏ, hoặc nằm ở màn hình ảo khác)."
    front = (muc_tieu or {}).get("ung_dung") if muc_tieu else p.ung_dung_truoc()
    loai, mo_ta = phan_loai(op, a, front)
    if loai == "vo_hai" and (op in ("click", "double_click", "right_click") or (op == "key" and _tach_phim(a.get("key"))[1] == "enter")):
        try:
            tieu_de = str((muc_tieu or {}).get("tieu_de") or "") if muc_tieu else str(p.tieu_de_cua_so() or "")
        except Exception:  # noqa: BLE001
            tieu_de = ""
        if _TIEN_CUA_SO.search(tieu_de):       # (18/11/2026) bước tiền bạc: không bấm, người dùng tự làm
            loai, mo_ta = "bi_mat", "Cửa sổ đang ở bước tiền bạc (thanh toán, mua, nạp, nâng gói): \"%s\". Người dùng tự bấm." % tieu_de[:60]
    kq = _can_duyet(op, a, front, loai, mo_ta)
    if kq:
        return kq
    if op in ("type", "key"):
        kq = _chong_chen(op, a, front)
        if kq:
            return kq
        if _hop_chon_tep_mo(front):
            # (V3.44, sự cố 22/11) Phím gửi vào trình duyệt không tới hộp chọn tệp (hộp chạy ở tiến trình riêng của macOS): bấm Enter/Esc hộp đứng im.
            if op == "key" and _tach_phim(a.get("key"))[1] == "escape":
                return _chon_tep(p, {"huy": True, "ung_dung": front})
            _nk(op, "hộp chọn tệp", "Đổi sang op=chon_tep")
            return ("HOP_CHON_TEP: %s đang mở hộp chọn tệp của hệ thống; phím và chữ gõ thường KHÔNG vào được hộp này. Gọi tisa_desktop_do op=chon_tep "
                    "path=\"<đường dẫn đầy đủ tới thư mục hoặc tệp>\" tat_ca=true (chọn hết tệp trong thư mục) — TISA BOT tự đi tới thư mục, chọn tệp và bấm Mở. "
                    "Huỷ hộp: op=chon_tep huy=true. KHÔNG nhờ anh bấm hộ." % front)
    with _khoa:
        moi = time.time() - _tt["lan_cuoi"] > 300
        _tt["lan_cuoi"] = time.time()
    if moi and sys.platform == "darwin":
        try:
            subprocess.Popen([_lenh_mac("osascript"), "-e", 'display notification "AI đang điều khiển máy. Đưa chuột về góc trên trái màn hình để dừng." with title "TISA BOT"'],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError:
            pass
    ten = ""
    cho_sau = 0.0        # chờ giao diện kịp đổi rồi mới tự chụp lại

    if op in ("click", "double_click", "right_click"):
        x, y = (diem["x"], diem["y"]) if rieng else toa_do()
        if rieng:
            cach = CR.bam(muc_tieu, x, y, "right" if op == "right_click" else "left", 2 if op == "double_click" else 1)
            ten = "(%d,%d) %s" % (x, y, muc_tieu["ung_dung"])
            kq = "Đã %s tại (%d,%d) trong %s bằng chuột riêng của TISA BOT (%s), chuột thật của anh không bị động." % (
                {"click": "bấm", "double_click": "bấm đúp", "right_click": "bấm chuột phải"}[op], x, y, muc_tieu["ung_dung"], cach)
        else:
            p.bam(x, y, "right" if op == "right_click" else "left", 2 if op == "double_click" else 1)
            ten = "(%d,%d)" % (x, y)
            kq = "Đã %s tại (%d,%d)." % ({"click": "bấm", "double_click": "bấm đúp", "right_click": "bấm chuột phải"}[op], x, y)
        cho_sau = 0.3
    elif op == "move":
        if rieng:
            CR.hien_con_tro(diem["x"], diem["y"], "di")
            kq = "Đã đưa con trỏ TISA BOT tới (%d,%d) (chuột thật của anh đứng yên)." % (diem["x"], diem["y"])
        else:
            x, y = toa_do()
            p.di_chuyen(x, y)
            kq = "Đã di chuột tới (%d,%d)." % (x, y)
    elif op == "drag":
        if rieng:
            x, y = diem["x"], diem["y"]
            x2, y2 = (lambda t: (t[0], t[1]))(toa_do("x2", "y2"))
            CR.keo(muc_tieu, x, y, x2, y2)
            kq = "Đã kéo từ (%d,%d) tới (%d,%d) bằng chuột riêng." % (x, y, x2, y2)
        else:
            x, y = toa_do()
            x2, y2 = toa_do("x2", "y2")
            p.keo(x, y, x2, y2)
            kq = "Đã kéo từ (%d,%d) tới (%d,%d)." % (x, y, x2, y2)
        cho_sau = 0.3
    elif op == "scroll":
        dy = int(a.get("dy") if a.get("dy") is not None else 5)
        if rieng:
            if not muc_tieu:
                return "CHUA_CO_DICH: Chưa biết cuộn cửa sổ nào. Truyền x y (trong cửa sổ cần cuộn) hoặc ung_dung=\"tên ứng dụng\"."
            CR.cuon(muc_tieu, diem["x"], diem["y"], dy)
        else:
            p.cuon(dy, int(round(int(a["x"]) * ti_le)) if a.get("x") is not None else None, int(round(int(a["y"]) * ti_le)) if a.get("y") is not None else None)
        kq = "Đã cuộn %s %d nấc." % ("xuống" if dy > 0 else "lên", abs(dy))
        cho_sau = 0.25
    elif op == "type":
        text = str(a.get("text") or "")
        if not text:
            return "LOI: thiếu text."
        if len(text) > 4000:
            return "LOI: chuỗi gõ quá dài (tối đa 4000 ký tự mỗi lần)."
        kieu = str(a.get("kieu") or "").lower()
        dich = ("cửa sổ %s (chuột riêng)" % muc_tieu["ung_dung"]) if muc_tieu else "ứng dụng đang ở trước (%s)" % (front or "không rõ")
        pid = muc_tieu["pid"] if muc_tieu else 0
        kw = {"pid": pid} if pid else {}        # đường cũ giữ nguyên chữ ký hàm (không truyền pid)
        if muc_tieu:
            CR.nho_muc_tieu(muc_tieu)           # Windows cần biết đúng cửa sổ đích trước khi gõ
        if kieu in ("phim", "key", "keys"):
            p.go(text, "phim", **kw)
            ten, kq = "gõ %d ký tự" % len(text), "Đã gõ %d ký tự vào %s." % (len(text), dich)
        elif kieu != "chu" and not pid and any(ord(c) > 127 for c in text):
            # (18/11/2026) Chữ có dấu tiếng Việt: LUÔN đưa qua clipboard (pbcopy + cmd+v), không gõ từng phím, vì bộ gõ Telex của macOS sẽ biến chữ.
            try:
                p.dan_chu(text, **kw)
                ten, kq = "dán %d ký tự" % len(text), "Đã dán %d ký tự (qua clipboard, giữ nguyên dấu) vào %s." % (len(text), dich)
            except Exception as e:  # noqa: BLE001
                p.go(text, "chu", **kw)
                ten, kq = "gõ %d ký tự" % len(text), "Đã gõ %d ký tự (clipboard lỗi %s nên gõ từng chữ; kiểm lại dấu) vào %s." % (len(text), type(e).__name__, dich)
        else:
            p.go(text, "chu", **kw)
            ten, kq = "gõ %d ký tự" % len(text), "Đã gõ %d ký tự vào %s." % (len(text), dich)
        if muc_tieu:
            CR.nho_muc_tieu(muc_tieu)
            CR.hien_con_tro(muc_tieu["x"] + muc_tieu["w"] / 2, muc_tieu["y"] + 40, "go")
        cho_sau = 0.25
    elif op == "key":
        mods, phim = _tach_phim(a.get("key"))
        if not phim:
            return "LOI: thiếu phím (ví dụ cmd+space, enter, ctrl+c, alt+tab)."
        if muc_tieu:
            CR.nho_muc_tieu(muc_tieu)
        p.nhan_phim(mods, phim, **({"pid": muc_tieu["pid"]} if muc_tieu else {}))
        ten = str(a.get("key"))
        kq = "Đã nhấn %s%s." % (a.get("key"), (" trong %s (chuột riêng)" % muc_tieu["ung_dung"]) if muc_tieu else "")
        if muc_tieu:
            CR.nho_muc_tieu(muc_tieu)
        cho_sau = 0.25
    elif op == "open_app":
        nm = str(a.get("name") or "").strip()
        if not nm:
            return "LOI: thiếu name (tên ứng dụng)."
        ghim = None
        if re.search(r"chrome", nm, re.I):
            import tisa_chong_chen as CC
            ghim = CC.doc_da_chon()
        if ghim:    # (18/11/2026) anh đã chọn hồ sơ Chrome: chỉ đưa ĐÚNG hồ sơ đó lên, không mở hồ sơ khác
            kq = CC.mo_chrome("", "", True, False)
            ten = nm
        else:
            p.mo_ung_dung(nm, **({"nen": True} if rieng else {}))
            ten = nm
            kq = ("Đã mở ứng dụng %s%s. Chờ 1 đến 2 giây, rồi chụp cửa sổ đó: screenshot ung_dung=\"%s\"." % (
                nm, " ở NỀN (không giành màn hình của anh)" if sys.platform == "darwin" else " (Windows chưa mở nền được: cửa sổ có thể hiện lên trước)", nm)) if rieng \
                else "Đã mở ứng dụng %s. Chờ 1 đến 2 giây rồi chụp màn hình." % nm
        cho_sau = 1.4
    elif op == "open_path":
        pt = os.path.expanduser(str(a.get("path") or "").strip())
        if not pt or not Path(pt).exists():
            return "LOI: không thấy đường dẫn %s" % pt
        p.mo_duong_dan(pt)
        ten = Path(pt).name
        kq = "Đã mở %s bằng ứng dụng mặc định. Chờ 1 đến 2 giây rồi chụp màn hình." % pt
        cho_sau = 1.4
    elif op == "mo_chrome":
        import tisa_chong_chen as CC
        kq = CC.mo_chrome(str(a.get("ho_so") or ""), str(a.get("url") or ""), True, not a.get("tab_moi"))
        ten = str(a.get("ho_so") or "")
        if kq.split(":", 1)[0] in ("LOI", "KHOA_HO_SO", "CHUA_CHON"):
            return kq
    elif op == "focus_app":
        nm = str(a.get("name") or "").strip()
        if rieng:
            ten = nm
            kq = ("Đang ở chế độ chuột riêng nên KHÔNG cần đưa %s ra trước (làm vậy là giành màn hình của anh). Chụp cửa sổ đó: screenshot ung_dung=\"%s\"; "
                  "rồi bấm, gõ với ung_dung=\"%s\"." % (nm, nm, nm))
        else:
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
    # Một lệnh làm xong luôn kèm ảnh mới (chủ yêu cầu 18/11/2026: nhanh nhất có thể): AI khỏi gọi thêm một lượt chỉ để chụp màn hình.
    if a.get("chup_sau") is not False and cho_sau > 0:
        try:
            cho = a.get("cho_ms")
            time.sleep((min(max(int(cho), 0), 5000) / 1000.0) if cho is not None else cho_sau)
            ung = ung_dung_chi if (rieng and ung_dung_chi) else ""
            k = _chup_nhanh(p, ung)
            kq += "\n" + _chu_anh(p, k, False)
        except Exception as e:  # noqa: BLE001
            kq += "\nChụp lại tự động không được (%s). Gọi screenshot để xem." % type(e).__name__
    else:
        kq += " Chụp lại để xem kết quả."
    return kq


def _nhieu_buoc(p, a: dict) -> str:
    """op=nhieu_buoc cac_buoc=[{op, ...}, ...]: chạy liền nhiều thao tác trong MỘT lệnh, chỉ chụp một ảnh ở cuối (chủ yêu cầu 18/11/2026: nhanh nhất có thể).
    Mỗi bước vẫn qua đủ chốt chặn như lệnh riêng (duyệt, chống chen, tiền bạc); bước nào bị chặn hoặc lỗi thì DỪNG và báo bước đó."""
    buoc = a.get("cac_buoc")
    if isinstance(buoc, str):
        try:
            buoc = json.loads(buoc)
        except ValueError:
            return "LOI: cac_buoc phải là danh sách JSON các bước, mỗi bước {op, x, y, text, ...}."
    if not isinstance(buoc, list) or not buoc:
        return "LOI: thiếu cac_buoc (danh sách bước, mỗi bước {op, x, y, text, key, ...}), tối đa 15 bước."
    if len(buoc) > 15:
        return "LOI: tối đa 15 bước mỗi lệnh."
    cho_phep = _OP_VAO + ("move", "scroll", "wait") + _OP_AD_NHIEU
    chi_theo_ma = all(isinstance(x, dict) and str(x.get("op") or "").lower() in _OP_AD_NHIEU for x in buoc)
    ket, dung, xong = [], False, 0
    for i, b in enumerate(buoc, 1):
        if not isinstance(b, dict):
            ket.append("%d. LOI: bước phải là đối tượng {op, ...}" % i)
            ket.append("DỪNG ở bước %d (các bước sau KHÔNG chạy)." % i)
            dung = True
            break
        op_i = str(b.get("op") or "").lower()
        if op_i not in cho_phep or op_i == "mo_chrome":
            ket.append("%d. LOI: op không dùng trong nhieu_buoc: %s" % (i, op_i))
            ket.append("DỪNG ở bước %d (các bước sau KHÔNG chạy)." % i)
            dung = True
            break
        b = dict(b)
        b["chup_sau"] = False
        if "ung_dung" not in b and a.get("ung_dung"):
            b["ung_dung"] = a.get("ung_dung")
        if op_i == "wait":
            time.sleep(min(max(int(b.get("ms") or 300), 50), 5000) / 1000)
            ket.append("%d. wait: ok" % i)
            xong += 1
            continue
        try:
            r = _cay_tro_nang(p, op_i, b) if op_i in _OP_AD_NHIEU else _lam(p, op_i, b)
        except Exception as e:  # noqa: BLE001
            r = "LOI: %s: %s" % (type(e).__name__, str(e)[:120])
        dong = str(r).splitlines()[0][:170]
        ket.append("%d. %s: %s" % (i, op_i, dong))
        if op_i in _OP_AD_NHIEU:
            thanh_cong = str(r).startswith("Kết quả tìm") if op_i == "tim" else str(r).startswith(("Đã ", "DA_THAY"))
            ma_loi = str(r).split(":", 1)[0]
            if not thanh_cong and ma_loi not in ("CAN_DUYET", "DA_DUNG", "BI_CHEN", "BI_CHAN_XOA", "CAN_NGUOI_DUNG", "DA_TAT", "CAN_QUYEN"):
                r = "LOI: " + str(r)             # tìm không thấy, chờ quá giờ, mã hết hạn...: các bước sau không còn nghĩa, dừng
        if op_i == "tim":
            ket[-1] = "%d. tim: %s" % (i, str(r).replace("Kết quả tìm", "kết quả tìm")[:1500])   # mã tìm được cần thấy để làm tiếp
        if str(r).split(":", 1)[0] in ("CAN_DUYET", "DA_DUNG", "LOI", "BI_CHEN", "BI_CHAN_XOA", "CAN_NGUOI_DUNG", "DA_TAT", "CAN_QUYEN", "KHONG_HO_TRO", "CHUA_CO_DICH"):
            dung = True
            ket.append("DỪNG ở bước %d (các bước sau KHÔNG chạy). Xử lý bước này (duyệt, sửa toạ độ...) rồi gọi lại phần còn lại." % i)
            if str(r).startswith("CAN_DUYET"):
                ket.append(str(r)[:600])
            break
        xong += 1
        time.sleep(0.12)
    ket_qua = "Đã chạy %d/%d bước.\n%s" % (xong, len(buoc), "\n".join(ket))
    # Lô chỉ gồm bước theo mã (cây trợ năng): mặc định KHÔNG chụp ảnh cuối (~1.200 token), kiểm lại bằng op=tim là đủ. Muốn ảnh thì chup_sau=true.
    if chi_theo_ma and a.get("chup_sau") is not True:
        _nk("nhieu_buoc", "dừng" if dung else "ok", "%d bước (theo mã)" % len(buoc))
        return ket_qua + "\nKiểm lại bằng tisa_desktop_look op=tim (rẻ) thay vì chụp ảnh."
    if a.get("chup_sau") is not False:
        try:
            time.sleep(min(max(int(a.get("cho_ms") if a.get("cho_ms") is not None else 300), 0), 5000) / 1000.0)
            k = _chup_nhanh(p, str(a.get("ung_dung") or "").strip() if _rieng_bat(p) else "")
            ket_qua += "\n" + _chu_anh(p, k, False)
        except Exception as e:  # noqa: BLE001
            ket_qua += "\nChụp lại tự động không được (%s). Gọi screenshot để xem." % type(e).__name__
    _nk("nhieu_buoc", "dừng" if dung else "ok", "%d bước" % len(buoc))
    return ket_qua


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
    try:
        CR = _mod_chuot(p)
        if CR is not None:
            d["chuot"] = {"che_do": CR.che_do(), "dung_duoc": bool(CR.dung_duoc())}
    except Exception:  # noqa: BLE001
        pass
    d["nhat_ky"] = [x for x in (B.doc_nk(80) if B else []) if str(x.get("op", "")).startswith("may_")][-12:]
    return d


def _ten_may_nay() -> str:
    """Tên máy đang chạy TISA BOT này (tên ở Nhiều máy nếu đã nối, kèm tên máy của hệ điều hành)."""
    ten_he = ""
    try:
        if sys.platform == "darwin":
            ten_he = subprocess.run(["scutil", "--get", "ComputerName"], capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception:  # noqa: BLE001
        pass
    if not ten_he:
        import platform
        ten_he = platform.node() or "máy này"
    try:
        import tisa_nhieu_may as _NM
        if _NM.dang_bat():
            ten_nm = _NM.ten_may()
            if ten_nm and ten_nm != ten_he:
                return "%s, máy %s" % (ten_nm, ten_he)
    except Exception:  # noqa: BLE001
        pass
    return ten_he


# Nhiều máy (21/11/2026): chủ mở TISA BOT 2 qua tên miền từ máy tính mới, nhờ "làm trên máy này" nhưng công cụ điều khiển
# MacBook đang chạy TISA BOT (đang khóa). Công cụ chỉ điều khiển được máy đang chạy TISA BOT, nên mô tả phải nói rõ máy nào.
try:
    _MAY_NAY = _ten_may_nay()
except Exception:  # noqa: BLE001
    _MAY_NAY = "máy này"
_MAY_NAO = ("CHỈ ĐIỀU KHIỂN ĐƯỢC MÁY ĐANG CHẠY TISA BOT NÀY: \"%s\". Anh có thể đang mở TISA BOT từ máy tính khác hoặc điện thoại qua tên miền; "
            "máy anh đang ngồi chỉ là màn hình xem, AI không điều khiển được máy đó. Khi anh nói \"máy này\", \"máy anh đang mở\", hoặc ảnh chụp không giống màn hình anh tả, "
            "hoặc máy báo đang khóa trong khi anh nói máy đang mở: nói rõ ngay em đang điều khiển máy \"%s\", KHÔNG cố mở khóa hay làm tiếp trên máy đó khi anh chưa đồng ý. "
            "Muốn AI làm trên máy anh đang ngồi: cài TISA BOT lên máy đó rồi ghép ở Hệ thống → Nhiều máy → Thêm máy, xong mở TISA BOT của chính máy đó "
            "(http://127.0.0.1:<cổng> trên máy đó, hoặc nút Mở máy này ở trang Nhiều máy). ") % (_MAY_NAY, _MAY_NAY)

_MO_TA_NHIN = (_MAY_NAO + "Nhìn máy tính của anh (macOS hoặc Windows). TIẾT KIỆM TOKEN (V3.45, cây trợ năng): biết cần nút/ô nào thì dùng op=tim ten=\"Mở\" [vai_tro=button] [chu=...] [ung_dung=<tên>] [vung=sheet|menu|alert] "
               "(khoảng 150 token, trả MÃ để bấm thẳng); cần xem bố cục thì op=cay ung_dung=<tên> (bản gọn ~400 token; dòng có {N con} đọc thêm bằng op=cay goc=<mã>; day_du=true đọc cả cửa sổ); "
               "op=cua_so liệt kê cửa sổ khi ứng dụng có nhiều cửa sổ. op=cho chu=\"...\" | tieu_de=\"...\" | ma=<mã> [giay=15] CHỜ tới khi chữ / cửa sổ / phần tử xuất hiện rồi mới làm tiếp (thay cho wait cố định rồi chụp ảnh xem lại). Ảnh chụp (~1.200 token) chỉ dùng khi tim/cay không thấy (ứng dụng vẽ riêng, trò chơi, ảnh, video, báo APP_UNRESPONSIVE) hoặc cần nhìn hình. Trang web: dùng tisa_browser, không dùng cách này. "
               "op=screenshot chụp màn hình (ảnh được gửi kèm để nhìn, biết bấm đâu; nhanh, khoảng 0,1 giây; thêm ung_dung=<tên> để chụp riêng một cửa sổ kể cả khi bị che); op=zoom x y x2 y2 phóng to một vùng của ảnh gần nhất để đọc chữ nhỏ; op=windows liệt kê ứng dụng đang mở; op=front ứng dụng đang ở trước; "
               "op=permissions kiểm tra quyền điều khiển; op=status; op=kiem_chen (có thứ khác đang điều khiển Chrome không); op=chup_cua_so ung_dung=<tên> hoặc x y w h, mo_ta=<tên thư mục> (chụp đúng cửa sổ, lưu vào brain 04-ket-qua); op=quay_trang_thai; op=huong_dan_quyen (quyền nào còn thiếu + hướng dẫn TỪNG BƯỚC để đọc lại cho người dùng). Thiếu quyền thì KHÔNG dừng ở \"em không làm được\": hướng dẫn họ bật. Làm theo kỹ năng dq-dieu-khien-may.")
_MO_TA_LAM = (_MAY_NAO + "Điều khiển máy tính của anh như người thật. ƯU TIÊN (V3.45, rẻ token, không di chuột thật, không giành cửa sổ): op=bam_ma ma=<mã từ tisa_desktop_look op=tim/cay> [kieu=doi|phai]; "
              "op=go_ma ma text (gõ vào ô theo mã, có dấu tiếng Việt vẫn đúng); op=dat_ma ma text (đặt cả giá trị ô); op=chon_ma ma text (chọn mục trong danh sách); op=cuon_toi_ma ma. Không kèm ảnh: kiểm lại bằng op=tim. "
              "Mã báo STALE_REF/SNAPSHOT_NOT_FOUND thì tìm lại. Chỉ khi không có mã (ứng dụng không trả cây) mới dùng toạ độ: "
              "op=click|double_click|right_click x y (toạ độ theo ảnh chụp); op=move x y; op=drag x y x2 y2; op=scroll dy (dương = xuống); "
              "op=type text (gõ được tiếng Việt; thêm kieu=phim để gõ từng phím thật cho máy tính bỏ túi, trò chơi); op=key key (ví dụ cmd+space, enter, ctrl+c, alt+tab); op=open_app name; op=open_path path (mở thư mục hoặc tệp); op=focus_app name; "
              "op=quit_app name; op=wait ms; op=cai_dat_quyen (macOS chưa cấp quyền: tự mở Cài đặt rồi chờ anh bật công tắc); "
              "op=mo_chrome [ho_so] url=... [tab_moi=true] (mở trang trong hồ sơ Chrome anh ĐÃ CHỌN; bỏ trống ho_so là đúng hồ sơ đó; xin hồ sơ khác bị KHOA_HO_SO, không tự mở hồ sơ khác); op=chon_chrome [ho_so] (xem hồ sơ đã chọn; đổi thì anh phải bấm Duyệt); "
              "op=quay_bat ung_dung|x y w h giay mo_ta [engine=ffmpeg] / op=quay_dung (quay video màn hình, lưu brain 04-ket-qua); "
              "op=chon_tep path=<thư mục hoặc tệp> [tat_ca=true] (V3.44: hộp CHỌN TỆP / Tải lên của hệ thống đang mở, ví dụ sau khi bấm nút thêm ảnh trên Facebook: TISA BOT tự đi tới thư mục, chọn tệp (tat_ca=true chọn hết tệp trong thư mục) và bấm Mở; huy=true để đóng hộp. Phím Enter/Esc/Cmd+Shift+G gõ thường KHÔNG vào được hộp này, đừng thử, đừng nhờ anh bấm hộ); "
              "op=giu_may_thuc ly_do phut [tu_mo_khoa=true] / op=tha_may (giữ máy thức khi việc nền dài; tu_mo_khoa cho phép tự mở khóa lại nếu khóa giữa chừng, cần anh duyệt); "
              "op=cho_nguoi_that ly_do phut (gặp Touch ID, mã khóa, CAPTCHA, OTP: báo anh bằng tin ngắn rồi chờ anh làm xong và tự làm tiếp; KHÔNG tự vượt các bước này); "
              "op=type có chữ tiếng Việt thì tự dán qua clipboard (không gõ từng phím, tránh Telex); gõ vào Chrome khi có thứ khác đang điều khiển thì trả BI_CHEN; "
              "op=mo_khoa (anh nói \"mở khóa máy / mở màn hình khóa\" thì gọi NGAY, không hỏi lại: máy Mac đang khóa, anh nhắn ở ô chat nào trong dashboard cũng được (kể cả chat với cộng sự) hoặc Zalo anh đã xác nhận ở Cài đặt; mật khẩu tự lấy từ Keychain (anh nhập ở Điều khiển của AI → Máy tính → Mở khóa máy), KHÔNG nhận mật khẩu qua tham số, KHÔNG xin mật khẩu trong chat; cần anh duyệt trừ Toàn quyền; kiểm đúng mật khẩu trước khi gõ, chờ máy mở tới 15 giây). Luôn chụp màn hình trước khi bấm và sau khi bấm để kiểm tra. KHÔNG xóa được tệp (công cụ chặn). Việc nhạy cảm trả CAN_DUYET: xin anh duyệt rồi gọi lại "
              "với duyet_id. Làm theo kỹ năng dq-dieu-khien-may. "
              "NHANH (V3.20): mỗi lệnh click/type/key/scroll/drag/open_app TỰ kèm ảnh chụp mới sau khi làm, KHÔNG gọi thêm screenshot chỉ để xem kết quả (đặt chup_sau=false nếu không cần ảnh, cho_ms=<ms> nếu giao diện đổi chậm); "
              "việc gồm nhiều thao tác liền nhau thì gọi MỘT lệnh op=nhieu_buoc, ƯU TIÊN bước theo mã: cac_buoc=[{op:\"go_ma\",ma:\"e5\",text:\"...\"},{op:\"go_ma\",ma:\"e6\",text:\"...\"},{op:\"bam_ma\",ma:\"e9\"},{op:\"cho\",chu:\"Đã lưu\"}] (bước theo mã: tim, cho, bam_ma, go_ma, dat_ma, chon_ma, cuon_toi_ma; lô chỉ gồm bước theo mã thì không kèm ảnh), hoặc theo toạ độ cac_buoc=[{op:\"click\",x:..,y:..},{op:\"type\",text:\"...\"},{op:\"key\",key:\"enter\"}] (tối đa 15 bước, chỉ chụp một ảnh cuối, bước bị chặn thì dừng). "
              "CHUỘT RIÊNG (macOS và Windows, mặc định bật; Windows chưa kiểm trên máy thật): TISA BOT dùng con chuột riêng (mũi tên cam của TISA BOT, viền cam quanh màn hình), KHÔNG động tới chuột và bàn phím thật của anh, nên anh vẫn làm việc ở ứng dụng khác. "
              "Bấm và gõ đi thẳng vào cửa sổ tại điểm đó; gõ phím (type, key) vào cửa sổ vừa bấm gần nhất, hoặc truyền ung_dung=<tên ứng dụng> để chỉ rõ. Cửa sổ bị che: screenshot ung_dung=<tên> chụp riêng cửa sổ đó, "
              "rồi click/drag/scroll/type kèm ung_dung=<tên> với toạ độ TRONG ảnh cửa sổ. Đừng focus_app (giành màn hình của anh); open_app mở ở nền. op=chuot_che_do che_do=that nếu một ứng dụng chỉ nhận chuột khi đang ở trước.")


def dang_ky_hub(add, vault_root=None) -> None:
    _VAULT["root"] = vault_root
    async def _nhin(args):
        a = args or {}
        op = str(a.get("op") or "screenshot").lower()
        if op not in ("screenshot", "zoom", "windows", "front", "permissions", "status", "kiem_chen", "chup_cua_so", "quay_trang_thai", "huong_dan_quyen", "tim", "cay", "cua_so", "cho"):
            return "LOI: op của tisa_desktop_look: tim, cay, cua_so, cho, screenshot, zoom, windows, front, permissions, status, kiem_chen, chup_cua_so, quay_trang_thai, huong_dan_quyen."
        return await thuc_hien(op, a)

    async def _lam(args):
        a = args or {}
        op = str(a.get("op") or "").lower()
        if op in ("screenshot", "zoom", "windows", "front", "permissions", "status", ""):
            return "LOI: op của tisa_desktop_do: click, double_click, right_click, move, drag, scroll, type, key, open_app, open_path, focus_app, quit_app, wait, nhieu_buoc, chuot_che_do, cai_dat_quyen, huong_dan_quyen, mo_khoa, mo_chrome, chon_chrome, quay_bat, quay_dung, giu_may_thuc, tha_may, cho_nguoi_that, chon_tep, bam_ma, go_ma, dat_ma, chon_ma, cuon_toi_ma."
        return await thuc_hien(op, a)

    add("tisa_desktop_look", _MO_TA_NHIN, {"op": {"type": "string", "description": "tim | cay | cua_so | cho | screenshot | zoom | windows | front | permissions | status (mặc định screenshot)"},
                                          "tieu_de": {"type": "string", "description": "op=cho: chờ cửa sổ có tiêu đề này"}, "ma": {"type": "string", "description": "op=cho: chờ phần tử có mã này"},
                                          "trang_thai": {"type": "string", "description": "op=cho ma=: exists | enabled | visible | actionable"}, "giay": {"type": "integer", "description": "op=cho: chờ tối đa bao nhiêu giây (1-60, mặc định 15)"},
                                          "ten": {"type": "string", "description": "op=tim: tên/nhãn nút cần tìm"}, "vai_tro": {"type": "string", "description": "op=tim: button, textfield, checkbox, menuitem..."},
                                          "chu": {"type": "string", "description": "op=tim: chữ xuất hiện trong tên, giá trị, mô tả; op=cho: chờ chữ này xuất hiện"}, "vung": {"type": "string", "description": "op=tim: sheet, menu, menubar, alert, popover (mặc định window)"},
                                          "goc": {"type": "string", "description": "op=cay: mã vùng cần đọc thêm (từ dòng có {N con})"}, "day_du": {"type": "boolean", "description": "op=cay: đọc cả cửa sổ thay vì bản gọn (tốn token hơn)"},
                                          "cua_so": {"type": "string", "description": "mã cửa sổ (từ op=cua_so) khi ứng dụng có nhiều cửa sổ"},
                                          "x": {"type": "integer"}, "y": {"type": "integer"}, "x2": {"type": "integer"}, "y2": {"type": "integer"},
                                          "w": {"type": "integer"}, "h": {"type": "integer"}, "ung_dung": {"type": "string"}, "mo_ta": {"type": "string"}}, [], _nhin, effect="write")
    add("tisa_desktop_do", _MO_TA_LAM,
        {"op": {"type": "string"}, "x": {"type": "integer"}, "y": {"type": "integer"}, "x2": {"type": "integer"}, "y2": {"type": "integer"}, "dy": {"type": "integer"},
         "text": {"type": "string"}, "key": {"type": "string"}, "name": {"type": "string"}, "path": {"type": "string"}, "ms": {"type": "integer"},
         "ly_do": {"type": "string"}, "duyet_id": {"type": "string"}, "kieu": {"type": "string", "description": "type: 'phim' = gõ từng phím thật (máy tính bỏ túi, phím tắt); mặc định: chữ có dấu tiếng Việt tự dán qua clipboard. bam_ma: doi = bấm đúp, phai = chuột phải"},
         "cua_so": {"type": "string"},
         "ho_so": {"type": "string"}, "tab_moi": {"type": "boolean"}, "url": {"type": "string"}, "ung_dung": {"type": "string"}, "mo_ta": {"type": "string"}, "w": {"type": "integer"}, "h": {"type": "integer"},
         "giay": {"type": "integer"}, "phut": {"type": "integer"}, "tu_mo_khoa": {"type": "boolean"}, "ma": {"type": "string"}, "bo_qua_chen": {"type": "boolean"},
         "engine": {"type": "string"}, "am_thanh": {"type": "boolean"},
         "tat_ca": {"type": "boolean", "description": "op=chon_tep: chọn hết tệp trong thư mục path"}, "huy": {"type": "boolean", "description": "op=chon_tep: bấm Huỷ trên hộp chọn tệp"},
         "chup_sau": {"type": "boolean", "description": "mặc định true: làm xong tự kèm ảnh chụp mới. false = không chụp."},
         "cho_ms": {"type": "integer", "description": "chờ bao nhiêu ms trước khi chụp lại (mặc định 250 đến 1400 tùy thao tác)"},
         "cac_buoc": {"type": "array", "items": {"type": "object"}, "description": "op=nhieu_buoc: danh sách bước {op, x, y, text, key, ung_dung...}, tối đa 15"},
         "che_do": {"type": "string", "description": "op=chuot_che_do: rieng | that"},
         "ma": {"type": "string", "description": "op=bam_ma/go_ma/dat_ma/chon_ma/cuon_toi_ma: mã phần tử từ tisa_desktop_look op=tim hoặc op=cay (ví dụ e8)"}},
        ["op"], _lam, effect="write")


def gan(app) -> None:
    from fastapi.responses import FileResponse, JSONResponse

    try:       # ô nhập mật khẩu mở khóa máy ở Cài đặt (tisa_mo_khoa.gan)
        import tisa_mo_khoa
        tisa_mo_khoa.gan(app)
    except Exception as e:  # noqa: BLE001
        print("[tisa_mo_khoa] không bật được đường cài đặt: %s: %s" % (type(e).__name__, e), file=sys.stderr)

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

    @app.get("/may-ai/chuot-che-do")
    async def ma_chuot_xem():
        CR = _mod_chuot(nen())
        if CR is None:
            return JSONResponse({"ok": True, "che_do": "that", "dung_duoc": False})
        return JSONResponse({"ok": True, "che_do": CR.che_do(), "dung_duoc": bool(CR.dung_duoc())})

    @app.post("/may-ai/chuot-che-do")
    async def ma_chuot_dat(request: Request):
        """Chuột riêng của TISA BOT (rieng) hay chuột thật như trước (that). Chỉ macOS."""
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        CR = _mod_chuot(nen())
        if CR is None:
            return JSONResponse({"ok": False, "error": "Chuột riêng chưa làm cho hệ điều hành này."}, status_code=400)
        v = CR.dat_che_do(str((d or {}).get("che_do") or ""))
        _nk("chuot_che_do", "ok", "Chế độ chuột: %s" % v)
        return JSONResponse({"ok": True, "che_do": v})

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

    @app.on_event("startup")
    async def _cai_quyen_khoi_dong():
        """(18/11/2026) Cài lần đầu: tự hiện hộp xin quyền, chạm thư mục, mở đúng trang Cài đặt và đợi người dùng bật; báo họ khi xong hoặc còn thiếu. Chỉ một lần."""
        if os.environ.get("TISA_BO_QUA_CAI_QUYEN") == "1":
            return
        loop = asyncio.get_running_loop()

        def lam():
            try:
                import tisa_cai_quyen as CQ
                import tisa_bao_anh as BA
                p = nen()
                if p is None or muc_hien_tai() == "tat" or CQ.da_chay_lan_dau():
                    return
                CQ.chay_lan_dau(p, lambda t: BA.bao(t, loop))
            except Exception as e:  # noqa: BLE001
                print("[tisa_cai_quyen] không chạy được lần đầu: %s" % type(e).__name__, file=sys.stderr)
        t = threading.Timer(25.0, lam)
        t.daemon = True
        t.start()

    @app.get("/may-ai/cai-quyen")
    async def ma_cai_quyen():
        import tisa_cai_quyen as CQ
        p = nen()
        ds = await asyncio.to_thread(CQ.trang_thai, p)
        return JSONResponse({"he": CQ._he(), "muc": ds, "thieu": [x["id"] for x in CQ.thieu(ds)], "huong_dan": await asyncio.to_thread(CQ.huong_dan, p, None, ds), "da_chay_lan_dau": CQ.da_chay_lan_dau()})

    @app.post("/may-ai/cai-quyen/chay")
    async def ma_cai_quyen_chay():
        import tisa_cai_quyen as CQ
        import tisa_bao_anh as BA
        loop = asyncio.get_running_loop()
        p = nen()
        return JSONResponse(await asyncio.to_thread(CQ.chay_lan_dau, p, lambda t: BA.bao(t, loop), True))

    @app.get("/may-ai/chrome-ho-so")
    async def ma_chrome_ds():
        import tisa_chong_chen as CC
        return JSONResponse({"da_chon": CC.doc_da_chon(), "ho_so": await asyncio.to_thread(CC.liet_ke_ho_so)})

    @app.post("/may-ai/chrome-ho-so")
    async def ma_chrome_chon(request: Request):
        """Anh chọn hồ sơ Chrome trên dashboard (chính anh bấm, không qua AI). ho_so rỗng = bỏ chọn."""
        import tisa_chong_chen as CC
        try:
            d = await request.json()
        except Exception:  # noqa: BLE001
            d = {}
        ten = str((d or {}).get("ho_so") or "").strip()
        if not ten:
            CC.bo_da_chon()
            _nk("chon_chrome", "bỏ chọn", "Anh bỏ chọn hồ sơ Chrome")
            return JSONResponse({"ok": True})
        r = await asyncio.to_thread(CC.dat_da_chon, ten)
        _nk("chon_chrome", "đã chọn" if r["ok"] else "lỗi", "Anh chọn hồ sơ Chrome %s trên dashboard" % ten[:40])
        if r.get("ok") and B is not None:
            # V3.20: chọn xong là LÀM NGAY (mở đúng hồ sơ, chuyển TISA BOT sang Chrome của anh, bỏ tab ở hồ sơ khác), không chỉ ghi nhớ.
            try:
                r["ap_dung"] = await asyncio.wait_for(B.ap_dung_ho_so_chrome(), 40)
            except Exception as e:  # noqa: BLE001
                r["ap_dung"] = {"ok": False, "tin": "Đã chọn hồ sơ nhưng chưa mở được Chrome ngay: %s" % type(e).__name__}
        return JSONResponse(r)

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
