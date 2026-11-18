"""tisa_chuot_rieng.py - CON CHUỘT RIÊNG của TISA BOT (V3.20, chủ yêu cầu 18/11/2026).

Chủ dặn: "TISA BOT dùng con chuột của nó để điều khiển, không giành con chuột của anh. Anh đang làm việc ở app khác, TISA BOT làm việc ở cửa sổ kia."

Cách làm trên macOS (chỉ dùng ctypes, không cần cài thêm gì):
- KHÔNG đưa sự kiện qua hệ thống chung (CGEventPost với HID: cái này kéo con trỏ thật của anh đi và giành bàn phím).
  Thay vào đó gửi THẲNG vào tiến trình của cửa sổ cần làm việc bằng CGEventPostToPid: con trỏ thật của anh đứng yên, ứng dụng anh đang dùng
  không bị đổi, anh gõ và bấm bình thường ở nơi khác.
- Nút bấm, ô tích, liên kết, mục menu: ưu tiên "bấm bằng Trợ năng" (AXPress), chạy được cả khi cửa sổ nằm sau lưng ứng dụng khác.
- Chụp riêng một cửa sổ kể cả khi bị che (screencapture -l), để TISA BOT thấy cửa sổ nó đang làm mà không bắt anh nhường màn hình.
- Con trỏ của TISA BOT là một mũi tên cam nổi trên màn hình, kèm viền cam nhẹ quanh màn hình khi nó đang thao tác (cửa sổ trong suốt, xuyên chuột), để anh thấy nó đang bấm ở đâu.

Giới hạn thật (nói thẳng với anh): vài ứng dụng chỉ nhận chuột khi là cửa sổ đang ở trước (game, một số ứng dụng vẽ riêng). Với những ứng dụng đó
bấm nền có thể không ăn; khi đó bật "dùng chuột thật" (op=chuot_che_do che_do=that) rồi làm như cũ.
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
TEP_VI_TRI = DIR / "chuot-ai-vi-tri.json"       # đọc bởi cửa sổ con trỏ (chuot-ai.js)
TEP_DONG = DIR / "chuot-ai-dong.flag"            # có tệp này thì con trỏ tự thoát
NHAN = "TISA BOT"
TUOI_MUC_TIEU = 600                              # giây: gõ phím vào cửa sổ vừa bấm gần nhất trong 10 phút

_P = {"ok": False}
_khoa = threading.Lock()
_muc_tieu = {"pid": 0, "id": 0, "ten": "", "luc": 0.0}
_cursor = {"proc": None}

MAC = sys.platform == "darwin"
KCG_WINDOW_ID = 91
KCG_WINDOW_ID_CAN_HANDLE = 92


# ---------------------------------------------------------------- chế độ
def che_do() -> str:
    """'rieng' (mặc định: con chuột riêng, không động tới chuột thật) hoặc 'that' (như trước đây)."""
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
    return MAC and _nap()


# ---------------------------------------------------------------- ctypes
def _nap() -> bool:
    if _P["ok"]:
        return True
    if not MAC:
        return False
    try:
        ag = ctypes.CDLL("/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices")
        cf = ctypes.CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
        cg = ctypes.CDLL("/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics")
    except OSError:
        return False
    V = ctypes.c_void_p

    class Pt(ctypes.Structure):
        _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]
    cf.CFStringCreateWithCString.argtypes = [V, ctypes.c_char_p, ctypes.c_uint32]
    cf.CFStringCreateWithCString.restype = V
    cf.CFStringGetCString.argtypes = [V, ctypes.c_char_p, ctypes.c_long, ctypes.c_uint32]
    cf.CFStringGetCString.restype = ctypes.c_bool
    cf.CFArrayGetCount.argtypes = [V]
    cf.CFArrayGetCount.restype = ctypes.c_long
    cf.CFArrayGetValueAtIndex.argtypes = [V, ctypes.c_long]
    cf.CFArrayGetValueAtIndex.restype = V
    cf.CFDictionaryGetValue.argtypes = [V, V]
    cf.CFDictionaryGetValue.restype = V
    cf.CFNumberGetValue.argtypes = [V, ctypes.c_int, V]
    cf.CFNumberGetValue.restype = ctypes.c_bool
    cf.CFRelease.argtypes = [V]
    cf.CFGetTypeID.argtypes = [V]
    cf.CFGetTypeID.restype = ctypes.c_ulong
    cf.CFStringGetTypeID.restype = ctypes.c_ulong
    cf.CFBooleanGetValue.argtypes = [V]
    cf.CFBooleanGetValue.restype = ctypes.c_bool
    cg.CGWindowListCopyWindowInfo.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
    cg.CGWindowListCopyWindowInfo.restype = V
    ag.CGEventCreateMouseEvent.argtypes = [V, ctypes.c_uint32, Pt, ctypes.c_uint32]
    ag.CGEventCreateMouseEvent.restype = V
    ag.CGEventCreateKeyboardEvent.argtypes = [V, ctypes.c_uint16, ctypes.c_bool]
    ag.CGEventCreateKeyboardEvent.restype = V
    ag.CGEventKeyboardSetUnicodeString.argtypes = [V, ctypes.c_ulong, ctypes.POINTER(ctypes.c_uint16)]
    ag.CGEventSetIntegerValueField.argtypes = [V, ctypes.c_uint32, ctypes.c_int64]
    ag.CGEventSetFlags.argtypes = [V, ctypes.c_uint64]
    ag.CGEventCreateScrollWheelEvent2.argtypes = [V, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
    ag.CGEventCreateScrollWheelEvent2.restype = V
    ag.CGEventSetLocation.argtypes = [V, Pt]
    ag.CGEventPostToPid.argtypes = [ctypes.c_int32, V]
    ag.AXIsProcessTrusted.restype = ctypes.c_bool
    ag.AXUIElementCreateApplication.argtypes = [ctypes.c_int32]
    ag.AXUIElementCreateApplication.restype = V
    ag.AXUIElementCopyElementAtPosition.argtypes = [V, ctypes.c_float, ctypes.c_float, ctypes.POINTER(V)]
    ag.AXUIElementCopyElementAtPosition.restype = ctypes.c_int32
    ag.AXUIElementCopyAttributeValue.argtypes = [V, V, ctypes.POINTER(V)]
    ag.AXUIElementCopyAttributeValue.restype = ctypes.c_int32
    ag.AXUIElementCopyActionNames.argtypes = [V, ctypes.POINTER(V)]
    ag.AXUIElementCopyActionNames.restype = ctypes.c_int32
    ag.AXUIElementSetAttributeValue.argtypes = [V, V, V]
    ag.AXUIElementSetAttributeValue.restype = ctypes.c_int32
    ag.AXUIElementPerformAction.argtypes = [V, V]
    ag.AXUIElementPerformAction.restype = ctypes.c_int32
    _P.update(ag=ag, cf=cf, cg=cg, Pt=Pt, ok=True)
    return True


def _s(txt: str):
    return _P["cf"].CFStringCreateWithCString(None, txt.encode("utf-8"), 0x08000100)


def _chuoi(ref) -> str:
    if not ref:
        return ""
    buf = ctypes.create_string_buffer(512)
    return buf.value.decode("utf-8", "ignore") if _P["cf"].CFStringGetCString(ref, buf, 512, 0x08000100) else ""


def _so(ref, kieu=4):
    if not ref:
        return 0
    if kieu == 6:
        v = ctypes.c_double()
    else:
        v = ctypes.c_int64()
    _P["cf"].CFNumberGetValue(ref, kieu, ctypes.byref(v))
    return v.value


def liet_ke_cua_so(tat_ca: bool = False) -> list:
    """Cửa sổ đang hiện trên màn hình, TRƯỚC ra SAU: [{id, pid, ung_dung, x, y, w, h, lop}]. Bỏ cửa sổ của chính con trỏ TISA BOT."""
    if not _nap():
        return []
    cf, cg = _P["cf"], _P["cg"]
    mang = cg.CGWindowListCopyWindowInfo(16 if tat_ca else (1 | 16), 0)      # tat_ca: cả cửa sổ ở màn hình ảo (Space) khác
    if not mang:
        return []
    k_id, k_pid, k_ten, k_bd, k_lop, k_alpha, k_tieude = (_s(x) for x in ("kCGWindowNumber", "kCGWindowOwnerPID", "kCGWindowOwnerName", "kCGWindowBounds", "kCGWindowLayer", "kCGWindowAlpha", "kCGWindowName"))
    kx, ky, kw, kh = (_s(x) for x in ("X", "Y", "Width", "Height"))
    ra = []
    try:
        for i in range(cf.CFArrayGetCount(mang)):
            d = cf.CFArrayGetValueAtIndex(mang, i)
            bd = cf.CFDictionaryGetValue(d, k_bd)
            if not bd:
                continue
            ten = _chuoi(cf.CFDictionaryGetValue(d, k_ten))
            ra.append({"id": int(_so(cf.CFDictionaryGetValue(d, k_id))), "tieu_de": _chuoi(cf.CFDictionaryGetValue(d, k_tieude)), "pid": int(_so(cf.CFDictionaryGetValue(d, k_pid))), "ung_dung": ten,
                       "x": _so(cf.CFDictionaryGetValue(bd, kx), 6), "y": _so(cf.CFDictionaryGetValue(bd, ky), 6),
                       "w": _so(cf.CFDictionaryGetValue(bd, kw), 6), "h": _so(cf.CFDictionaryGetValue(bd, kh), 6),
                       "lop": int(_so(cf.CFDictionaryGetValue(d, k_lop))), "alpha": _so(cf.CFDictionaryGetValue(d, k_alpha), 6)})
    finally:
        cf.CFRelease(mang)
        for r in (k_id, k_pid, k_ten, k_bd, k_lop, k_alpha, k_tieude, kx, ky, kw, kh):
            cf.CFRelease(r)
    return [w for w in ra if w["pid"] != os.getpid() and not _la_con_tro(w)]


def _la_con_tro(w: dict) -> bool:
    return w.get("ung_dung") in ("osascript",) and w.get("w", 0) <= 80 and w.get("h", 0) <= 80


def cua_so_tai(x: float, y: float):
    """Cửa sổ thường (lớp 0, không trong suốt) nằm TRÊN CÙNG tại điểm (x, y) của màn hình."""
    for w in liet_ke_cua_so():
        if w["lop"] == 0 and w["alpha"] > 0.05 and w["w"] > 40 and w["h"] > 40 and w["x"] <= x < w["x"] + w["w"] and w["y"] <= y < w["y"] + w["h"]:
            return w
    return None


def tim_cua_so(ten: str):
    """Cửa sổ của ứng dụng HOẶC có tiêu đề chứa `ten` (không phân biệt hoa thường), lớp 0. Khớp theo TIÊU ĐỀ được ưu tiên (vd "Facebook" chọn đúng cửa sổ
    Chrome đang mở Facebook), rồi tới cửa sổ lớn nhất. Cửa sổ bị che vẫn tìm thấy."""
    ten = (ten or "").strip().lower()
    if not ten:
        return None
    ds = [w for w in liet_ke_cua_so() if w["lop"] == 0 and w["w"] > 80 and w["h"] > 80
          and (ten in (w["ung_dung"] or "").lower() or ten in (w.get("tieu_de") or "").lower())]
    ds.sort(key=lambda w: (0 if ten in (w.get("tieu_de") or "").lower() else 1, -(w["w"] * w["h"])))
    return ds[0] if ds else None


# ---------------------------------------------------------------- mục tiêu
def nho_muc_tieu(w: dict) -> None:
    with _khoa:
        _muc_tieu.update(pid=w["pid"], id=w["id"], ten=w["ung_dung"], luc=time.time())


def muc_tieu() -> dict:
    with _khoa:
        if _muc_tieu["pid"] and time.time() - _muc_tieu["luc"] < TUOI_MUC_TIEU:
            return dict(_muc_tieu)
    return {}


# ---------------------------------------------------------------- gửi sự kiện thẳng vào tiến trình
def _gui(pid: int, e) -> None:
    _P["ag"].CGEventPostToPid(int(pid), e)
    _P["cf"].CFRelease(e)


def _chuot(pid: int, wid: int, tipo: int, x: float, y: float, nut: int = 0, lan: int = 1):
    ag = _P["ag"]
    e = ag.CGEventCreateMouseEvent(None, tipo, _P["Pt"](x, y), nut)
    ag.CGEventSetIntegerValueField(e, 1, lan)
    ag.CGEventSetIntegerValueField(e, KCG_WINDOW_ID, wid)
    ag.CGEventSetIntegerValueField(e, KCG_WINDOW_ID_CAN_HANDLE, wid)
    _gui(pid, e)


_VAI_TRO_NHAP = ("AXTextField", "AXTextArea", "AXComboBox", "AXSearchField", "AXSecureTextField")
_VAI_TRO_VUNG = ("AXWebArea", "AXScrollArea", "AXGroup", "AXStaticText", "AXImage", "AXRow", "AXCell", "AXSplitGroup", "AXWindow", "AXList", "AXTable", "AXOutline")


def _thuoc_tinh(el, ten: str):
    v = ctypes.c_void_p()
    k = _s(ten)
    kr = _P["ag"].AXUIElementCopyAttributeValue(el, k, ctypes.byref(v))
    _P["cf"].CFRelease(k)
    return v if kr == 0 and v.value else None


def _vai_tro(el) -> str:
    v = _thuoc_tinh(el, "AXRole")
    if not v:
        return ""
    r = _chuoi(v.value)
    _P["cf"].CFRelease(v)
    return r


def _co_hanh_dong(el, ten: str) -> bool:
    ds = ctypes.c_void_p()
    if _P["ag"].AXUIElementCopyActionNames(el, ctypes.byref(ds)) != 0 or not ds.value:
        return False
    co = any(_chuoi(_P["cf"].CFArrayGetValueAtIndex(ds.value, i)) == ten for i in range(_P["cf"].CFArrayGetCount(ds.value)))
    _P["cf"].CFRelease(ds)
    return co


def bam_tro_nang(pid: int, x: float, y: float):
    """Bấm / đặt tiêu điểm bằng Trợ năng, KHÔNG cần cửa sổ ở trước. Trả (hành động, vai trò): 'bam' (nút, liên kết, ô tích, menu),
    'tieu_diem' (ô nhập chữ: đã đặt con trỏ gõ vào đó), hoặc ('', vai_trò) nếu phải bấm bằng sự kiện chuột."""
    ag, cf = _P["ag"], _P["cf"]
    app = ag.AXUIElementCreateApplication(int(pid))
    if not app:
        return "", ""
    el = ctypes.c_void_p()
    giu = []                                   # mọi phần tử đã lấy, thả hết khi xong (tránh thả hai lần)
    try:
        if ag.AXUIElementCopyElementAtPosition(app, ctypes.c_float(x), ctypes.c_float(y), ctypes.byref(el)) != 0 or not el.value:
            return "", ""
        giu.append(el)
        vai_dau = _vai_tro(el.value)
        cur = el
        for _ in range(5):          # phần tử con (chữ, biểu tượng trong nút) thường không có AXPress: đi lên tối đa 4 cấp cha
            vt = _vai_tro(cur.value)
            if vt in _VAI_TRO_NHAP:
                kp, kt = _s("AXFocused"), ctypes.c_void_p.in_dll(cf, "kCFBooleanTrue")
                ag.AXUIElementSetAttributeValue.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
                ag.AXUIElementSetAttributeValue.restype = ctypes.c_int32
                kq = ag.AXUIElementSetAttributeValue(cur.value, kp, kt)
                cf.CFRelease(kp)
                return ("tieu_diem" if kq == 0 else ""), vt
            if vt not in _VAI_TRO_VUNG and _co_hanh_dong(cur.value, "AXPress"):
                kp = _s("AXPress")
                kq = ag.AXUIElementPerformAction(cur.value, kp)
                cf.CFRelease(kp)
                return ("bam" if kq == 0 else ""), vt
            cha = _thuoc_tinh(cur.value, "AXParent")
            if not cha:
                break
            giu.append(cha)
            cur = cha
        return "", vai_dau
    finally:
        for g in giu:
            if g.value:
                cf.CFRelease(g)
        cf.CFRelease(app)


def bam(w: dict, x: float, y: float, nut: str = "left", lan: int = 1, uu_tien_axpress: bool = True) -> str:
    """Bấm tại toạ độ màn hình (x, y) trong cửa sổ w mà KHÔNG động tới con trỏ thật. Trả mô tả cách đã bấm."""
    nho_muc_tieu(w)
    hien_con_tro(x, y, "bam")
    if uu_tien_axpress and nut == "left" and lan == 1:
        hd, vt = bam_tro_nang(w["pid"], x, y)
        if hd == "bam":
            return "Trợ năng, bấm đúng nút (%s)" % vt
        if hd == "tieu_diem":
            return "Trợ năng, đã đặt con trỏ gõ vào ô nhập (%s)" % vt
    k = 1 if nut == "right" else 0
    xuong, len_ = (3, 4) if nut == "right" else (1, 2)
    _chuot(w["pid"], w["id"], 5, x, y)
    time.sleep(0.05)
    for i in range(1, lan + 1):
        _chuot(w["pid"], w["id"], xuong, x, y, k, i)
        time.sleep(0.04)
        _chuot(w["pid"], w["id"], len_, x, y, k, i)
        time.sleep(0.06)
    return "sự kiện chuột gửi thẳng vào %s" % (w.get("ung_dung") or "cửa sổ")


def keo(w: dict, x: float, y: float, x2: float, y2: float) -> None:
    nho_muc_tieu(w)
    hien_con_tro(x, y, "keo")
    _chuot(w["pid"], w["id"], 5, x, y)
    time.sleep(0.05)
    _chuot(w["pid"], w["id"], 1, x, y, 0, 1)
    for i in range(1, 9):
        xi, yi = x + (x2 - x) * i / 8, y + (y2 - y) * i / 8
        _chuot(w["pid"], w["id"], 6, xi, yi, 0, 1)
        hien_con_tro(xi, yi, "keo")
        time.sleep(0.03)
    _chuot(w["pid"], w["id"], 2, x2, y2, 0, 1)


def cuon(w: dict, x: float, y: float, dy: int) -> None:
    nho_muc_tieu(w)
    hien_con_tro(x, y, "cuon")
    ag = _P["ag"]
    e = ag.CGEventCreateScrollWheelEvent2(None, 1, 1, int(-dy), 0, 0)
    ag.CGEventSetLocation(e, _P["Pt"](x, y))
    ag.CGEventSetIntegerValueField(e, KCG_WINDOW_ID, w["id"])
    ag.CGEventSetIntegerValueField(e, KCG_WINDOW_ID_CAN_HANDLE, w["id"])
    _gui(w["pid"], e)


def phim(pid: int, ma: int, flags: int = 0, xuong: bool = True, unicode_chu: str = "") -> None:
    ag = _P["ag"]
    e = ag.CGEventCreateKeyboardEvent(None, ma, xuong)
    if flags:
        ag.CGEventSetFlags(e, flags)
    if unicode_chu:
        b = unicode_chu.encode("utf-16-le")
        arr = (ctypes.c_uint16 * (len(b) // 2)).from_buffer_copy(b)
        ag.CGEventKeyboardSetUnicodeString(e, len(arr), arr)
    _gui(pid, e)


def go_chu(pid: int, text: str, tre: float = 0.02) -> None:
    """Gõ chữ vào ứng dụng `pid` (không cần nó ở trước, không đụng bàn phím của anh)."""
    for ch in text:
        if ch == "\n":
            phim(pid, 36, 0, True)
            phim(pid, 36, 0, False)
        else:
            phim(pid, 0, 0, True, ch)
            phim(pid, 0, 0, False, ch)
        time.sleep(tre)


# ---------------------------------------------------------------- chụp một cửa sổ (kể cả khi bị che)
def chup_cua_so_id(wid: int, tep: Path) -> bool:
    try:
        r = subprocess.run(["/usr/sbin/screencapture", "-x", "-o", "-l", str(int(wid)), str(tep)], capture_output=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return False
    return r.returncode == 0 and tep.exists() and tep.stat().st_size > 0


# ---------------------------------------------------------------- con trỏ của TISA BOT (cửa sổ trong suốt, xuyên chuột)
_JXA = r"""
ObjC.import('AppKit'); ObjC.import('Foundation'); ObjC.import('QuartzCore');
var app = $.NSApplication.sharedApplication; app.setActivationPolicy($.NSApplicationActivationPolicyAccessory);
var fm = $.NSFileManager.defaultManager;
var VT = "__VT__", DONG = "__DONG__";
var sf = $.NSScreen.screens.objectAtIndex(0).frame, SW = sf.size.width, SH = sf.size.height;
var CAM = $.NSColor.colorWithSRGBRedGreenBlueAlpha(1, 0.42, 0.13, 1);
function cam(a) { return $.NSColor.colorWithSRGBRedGreenBlueAlpha(1, 0.42, 0.13, a); }
var HOP = $.NSWindowCollectionBehaviorCanJoinAllSpaces | $.NSWindowCollectionBehaviorStationary | $.NSWindowCollectionBehaviorFullScreenAuxiliary | $.NSWindowCollectionBehaviorIgnoresCycle;
function cuaSo(rect) {
  var w = $.NSWindow.alloc.initWithContentRectStyleMaskBackingDefer(rect, $.NSWindowStyleMaskBorderless, $.NSBackingStoreBuffered, false);
  w.setOpaque(false); w.setBackgroundColor($.NSColor.clearColor); w.setIgnoresMouseEvents(true); w.setHasShadow(false);
  w.setLevel(2147483000); w.setCollectionBehavior(HOP); w.setReleasedWhenClosed(false); return w;
}
// ---- viền cam nhẹ quanh cả màn hình (gradient từ mép vào trong, trong suốt dần)
var vienWin = cuaSo($.NSMakeRect(sf.origin.x, sf.origin.y, SW, SH));
var vv = $.NSView.alloc.initWithFrame($.NSMakeRect(0, 0, SW, SH)); vv.setWantsLayer(true);
var N = 26, B = 2;                                       // 26 dải mỏng mỗi cạnh, mỗi dải 2 điểm: đậm ở mép, nhạt dần vào trong (gradient cam nhẹ)
for (var i = 0; i < N; i++) {
  var al = 0.62 * Math.pow(1 - i / N, 1.7), d = i * B;
  var cs = [[0, SH - d - B, SW, B], [0, d, SW, B], [d, 0, B, SH], [SW - d - B, 0, B, SH]];
  for (var k = 0; k < 4; k++) {
    var L = $.CALayer.layer; L.setFrame($.NSMakeRect(cs[k][0], cs[k][1], cs[k][2], cs[k][3]));
    L.setBackgroundColor(cam(al).CGColor); vv.layer.addSublayer(L);
  }
}
vienWin.setContentView(vv); vienWin.setAlphaValue(0);
// ---- con trỏ chuột cam của TISA BOT: chỉ một mũi tên cam (không chữ)
var W = 40, H = 40;
var cur = cuaSo($.NSMakeRect(0, 0, W, H));
var cv = $.NSView.alloc.initWithFrame($.NSMakeRect(0, 0, W, H)); cv.setWantsLayer(true);
var mui = $.NSImage.imageWithSystemSymbolNameAccessibilityDescription("cursorarrow", "TISA BOT");
var iv = $.NSImageView.alloc.initWithFrame($.NSMakeRect(0, 2, 36, 36));
if (mui) { iv.setImage(mui); iv.setContentTintColor(CAM); iv.setImageScaling($.NSImageScaleProportionallyUpOrDown); iv.setSymbolConfiguration($.NSImageSymbolConfiguration.configurationWithPointSizeWeight(30, 7)); }
cv.addSubview(iv); cur.setContentView(cv); cur.setAlphaValue(0);
var cx = -300, cy = -300, mx = -300, my = -300, hien = 0, luc = 0, aVien = 0, aCur = 0, t0 = Date.now();
function doc() {
  try {
    var s = $.NSString.stringWithContentsOfFileEncodingError(VT, $.NSUTF8StringEncoding, null);
    if (s && s.length) { var j = JSON.parse(ObjC.unwrap(s)); mx = j.x; my = j.y; hien = j.hien; luc = j.luc || 0; }
  } catch (e) {}
}
$.NSTimer.scheduledTimerWithTimeIntervalRepeatsBlock(0.016, true, function (t) {
  if (fm.fileExistsAtPath(DONG)) { $.NSApplication.sharedApplication.terminate(null); return; }
  doc();
  if (luc > 0 && Date.now() / 1000 - luc > 900) { $.NSApplication.sharedApplication.terminate(null); return; }    // 15 phút không thao tác: tự thoát, lần sau bật lại
  var tuoi = Date.now() / 1000 - luc;
  var bat = hien > 0 && tuoi < 10;                       // TISA BOT vừa thao tác trong 10 giây qua
  aVien += ((bat ? 1 : 0) - aVien) * 0.08;
  aCur += ((hien > 0 && tuoi < 6 ? 1 : 0) - aCur) * 0.2;
  var nhip = 0.82 + 0.18 * Math.sin((Date.now() - t0) / 450);          // thở nhẹ cho biết đang hoạt động
  vienWin.setAlphaValue(aVien * nhip);
  if (aVien > 0.02) { vienWin.orderFrontRegardless; } else { vienWin.orderOut(null); }
  cx += (mx - cx) * 0.35; cy += (my - cy) * 0.35;
  cur.setAlphaValue(aCur);
  if (aCur > 0.02) { cur.setFrameOrigin($.NSMakePoint(sf.origin.x + cx - 6, sf.origin.y + SH - cy - 36)); cur.orderFrontRegardless; } else { cur.orderOut(null); }
});
doc(); app.run;
"""


def _con_tro_dang_chay() -> bool:
    """Có con trỏ đang chạy (kể cả từ lần chạy máy chủ trước) thì dùng lại, không đẻ thêm."""
    p = _cursor["proc"]
    if p is not None and p.poll() is None:
        return True
    try:
        pid = int((DIR / "chuot-ai.pid").read_text().strip())
        r = subprocess.run(["/bin/ps", "-p", str(pid), "-o", "command="], capture_output=True, text=True, timeout=5)
        return "chuot-ai.js" in (r.stdout or "")
    except (OSError, ValueError, subprocess.SubprocessError):
        return False


def _tao_con_tro() -> bool:
    if not MAC:
        return False
    if _con_tro_dang_chay():
        return True
    DIR.mkdir(parents=True, exist_ok=True)
    try:
        TEP_DONG.unlink()
    except OSError:
        pass
    ma = _JXA.replace("__VT__", str(TEP_VI_TRI)).replace("__DONG__", str(TEP_DONG))
    tep = DIR / "chuot-ai.js"
    tep.write_text(ma, encoding="utf-8")
    try:
        _cursor["proc"] = subprocess.Popen(["/usr/bin/osascript", "-l", "JavaScript", str(tep)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                           start_new_session=True)
        (DIR / "chuot-ai.pid").write_text(str(_cursor["proc"].pid), encoding="utf-8")
        return True
    except OSError:
        return False


def hien_con_tro(x: float, y: float, nhan: str = "") -> None:
    """Đưa con trỏ TISA BOT tới (x, y). Không có con trỏ thì bỏ qua: việc chính vẫn làm."""
    try:
        if not _tao_con_tro():
            return
        TEP_VI_TRI.write_text(json.dumps({"x": float(x), "y": float(y), "hien": 1, "nhan": NHAN, "luc": time.time()}), encoding="utf-8")
    except (OSError, ValueError):
        pass


def giau_con_tro() -> None:
    try:
        TEP_VI_TRI.write_text(json.dumps({"x": -200, "y": -200, "hien": 0, "nhan": NHAN, "luc": time.time()}), encoding="utf-8")
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
            p.wait(timeout=2)
        except Exception:  # noqa: BLE001
            try:
                p.kill()
            except OSError:
                pass
