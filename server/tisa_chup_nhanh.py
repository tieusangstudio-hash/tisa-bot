"""tisa_chup_nhanh.py - Chụp màn hình / cửa sổ NHANH trên macOS, bằng thư viện hệ thống (ctypes), không gọi chương trình ngoài (V3.20, chủ yêu cầu 18/11/2026).

Cách cũ: screencapture (một tiến trình) -> sips (thêm một tiến trình đổi cỡ) -> Pillow mở lại, lưu bản gốc, thu nhỏ bằng LANCZOS, lưu lần nữa: ~340 ms.
Cách mới: lấy ảnh thẳng từ bộ nhớ đồ hoạ (CGDisplayCreateImage / CGWindowListCreateImage), vẽ nhỏ lại bằng CoreGraphics, ghi JPEG bằng ImageIO: ~120 ms.
Bản GỐC (để phóng to chữ nhỏ) ghi ở luồng riêng, không làm chậm lượt trả lời.

Mọi hàm trả None khi không làm được (thiếu quyền, hệ điều hành không còn hàm này): nơi gọi tự quay về cách cũ.
"""
from __future__ import annotations

import ctypes
import sys
import threading
from pathlib import Path

_L = {"ok": None}
MAC = sys.platform == "darwin"


def _nap():
    if _L["ok"] is not None:
        return _L["ok"]
    _L["ok"] = False
    if not MAC:
        return False
    try:
        cg = ctypes.CDLL("/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics")
        cf = ctypes.CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
        io = ctypes.CDLL("/System/Library/Frameworks/ImageIO.framework/ImageIO")
    except OSError:
        return False
    V = ctypes.c_void_p

    class Pt(ctypes.Structure):
        _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]

    class Sz(ctypes.Structure):
        _fields_ = [("w", ctypes.c_double), ("h", ctypes.c_double)]

    class Rc(ctypes.Structure):
        _fields_ = [("o", Pt), ("s", Sz)]
    try:
        cg.CGMainDisplayID.restype = ctypes.c_uint32
        cg.CGDisplayCreateImage.argtypes = [ctypes.c_uint32]
        cg.CGDisplayCreateImage.restype = V
        cg.CGImageGetWidth.argtypes = [V]
        cg.CGImageGetWidth.restype = ctypes.c_size_t
        cg.CGImageGetHeight.argtypes = [V]
        cg.CGImageGetHeight.restype = ctypes.c_size_t
        cg.CGImageRelease.argtypes = [V]
        cg.CGColorSpaceCreateDeviceRGB.restype = V
        cg.CGColorSpaceRelease.argtypes = [V]
        cg.CGBitmapContextCreate.argtypes = [V, ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t, V, ctypes.c_uint32]
        cg.CGBitmapContextCreate.restype = V
        cg.CGContextSetInterpolationQuality.argtypes = [V, ctypes.c_int]
        cg.CGContextDrawImage.argtypes = [V, Rc, V]
        cg.CGBitmapContextCreateImage.argtypes = [V]
        cg.CGBitmapContextCreateImage.restype = V
        cg.CGContextRelease.argtypes = [V]
        cf.CFStringCreateWithCString.argtypes = [V, ctypes.c_char_p, ctypes.c_uint32]
        cf.CFStringCreateWithCString.restype = V
        cf.CFURLCreateWithFileSystemPath.argtypes = [V, V, ctypes.c_long, ctypes.c_bool]
        cf.CFURLCreateWithFileSystemPath.restype = V
        cf.CFNumberCreate.argtypes = [V, ctypes.c_int, V]
        cf.CFNumberCreate.restype = V
        cf.CFDictionaryCreate.argtypes = [V, ctypes.POINTER(V), ctypes.POINTER(V), ctypes.c_long, V, V]
        cf.CFDictionaryCreate.restype = V
        cf.CFRelease.argtypes = [V]
        io.CGImageDestinationCreateWithURL.argtypes = [V, V, ctypes.c_size_t, V]
        io.CGImageDestinationCreateWithURL.restype = V
        io.CGImageDestinationAddImage.argtypes = [V, V, V]
        io.CGImageDestinationFinalize.argtypes = [V]
        io.CGImageDestinationFinalize.restype = ctypes.c_bool
        _L.update(cg=cg, cf=cf, io=io, Rc=Rc, Pt=Pt, Sz=Sz, V=V,
                  k_chat_luong=V.in_dll(io, "kCGImageDestinationLossyCompressionQuality"),
                  k_khoa=V.in_dll(cf, "kCFTypeDictionaryKeyCallBacks"), k_gia_tri=V.in_dll(cf, "kCFTypeDictionaryValueCallBacks"))
        # CGWindowListCreateImage đã bị Apple gỡ ở bản macOS mới: chỉ dùng khi còn
        try:
            cg.CGWindowListCreateImage.argtypes = [Rc, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32]
            cg.CGWindowListCreateImage.restype = V
            _L["co_cua_so"] = True
        except AttributeError:
            _L["co_cua_so"] = False
    except (AttributeError, ValueError):
        return False
    _L["ok"] = True
    return True


def _ghi_jpeg(img, tep: Path, chat_luong: float) -> bool:
    cf, io, V = _L["cf"], _L["io"], _L["V"]
    duong = cf.CFStringCreateWithCString(None, str(tep).encode("utf-8"), 0x08000100)
    url = cf.CFURLCreateWithFileSystemPath(None, duong, 0, False)
    kieu = cf.CFStringCreateWithCString(None, b"public.jpeg", 0x08000100)
    dest = io.CGImageDestinationCreateWithURL(url, kieu, 1, None)
    ok = False
    try:
        if dest:
            q = ctypes.c_double(chat_luong)
            so = cf.CFNumberCreate(None, 6, ctypes.byref(q))
            khoa = (V * 1)(_L["k_chat_luong"].value)
            gia = (V * 1)(so)
            props = cf.CFDictionaryCreate(None, khoa, gia, 1, ctypes.addressof(_L["k_khoa"]), ctypes.addressof(_L["k_gia_tri"]))
            io.CGImageDestinationAddImage(dest, img, props)
            ok = bool(io.CGImageDestinationFinalize(dest))
            cf.CFRelease(props)
            cf.CFRelease(so)
    finally:
        if dest:
            cf.CFRelease(dest)
        for r in (kieu, url, duong):
            cf.CFRelease(r)
    return ok and tep.exists() and tep.stat().st_size > 0


def _thu_nho(img, nw: int, nh: int):
    cg = _L["cg"]
    cs = cg.CGColorSpaceCreateDeviceRGB()
    ctx = cg.CGBitmapContextCreate(None, nw, nh, 8, 0, cs, 5)          # 5 = kCGImageAlphaNoneSkipLast
    cg.CGColorSpaceRelease(cs)
    if not ctx:
        return None
    cg.CGContextSetInterpolationQuality(ctx, 3)                          # cao: chữ nhỏ vẫn đọc được
    cg.CGContextDrawImage(ctx, _L["Rc"](_L["Pt"](0, 0), _L["Sz"](nw, nh)), img)
    nho = cg.CGBitmapContextCreateImage(ctx)
    cg.CGContextRelease(ctx)
    return nho


def cho_goc(toi_da: float = 3.0) -> None:
    """Chờ luồng ghi bản gốc xong (dùng trước khi phóng to một vùng)."""
    lg = _L.get("luong")
    if lg is not None and lg.is_alive():
        lg.join(toi_da)


def chup(tep_nho: Path, canh_toi_da: int, tep_goc: Path | None = None, chat_luong: float = 0.74, wid: int = 0):
    """Chụp màn hình chính (hoặc cửa sổ wid) -> `tep_nho` (cạnh dài <= canh_toi_da). Trả (rộng_gốc_điểm_ảnh, cao_gốc, rộng_nhỏ, cao_nhỏ) hoặc None.
    tep_goc: bản đủ độ phân giải, ghi ở luồng nền."""
    if not _nap():
        return None
    cg = _L["cg"]
    if wid:
        if not _L.get("co_cua_so"):
            return None
        # kCGWindowListOptionIncludingWindow = 8, kCGWindowImageBoundsIgnoreFraming = 1: đúng nội dung cửa sổ, kể cả khi bị che
        img = cg.CGWindowListCreateImage(_L["Rc"](_L["Pt"](float("inf"), float("inf")), _L["Sz"](0, 0)), 8, int(wid), 1)
    else:
        img = cg.CGDisplayCreateImage(cg.CGMainDisplayID())
    if not img:
        return None
    try:
        w, h = int(cg.CGImageGetWidth(img)), int(cg.CGImageGetHeight(img))
        if w < 10 or h < 10:
            return None
        k = max(w, h) / float(canh_toi_da)
        nw, nh = (max(1, round(w / k)), max(1, round(h / k))) if k > 1.0 else (w, h)
        nho = _thu_nho(img, nw, nh) if k > 1.0 else img
        if not nho:
            return None
        try:
            ok = _ghi_jpeg(nho, tep_nho, chat_luong)
        finally:
            if nho is not img:
                cg.CGImageRelease(nho)
        if not ok:
            return None
        if tep_goc is not None:
            cg.CGImageRetain.argtypes = [_L["V"]]
            cg.CGImageRetain.restype = _L["V"]
            cg.CGImageRetain(img)

            def ghi_goc(i=img):
                try:
                    _ghi_jpeg(i, tep_goc, 0.86)
                finally:
                    cg.CGImageRelease(i)
            lg = threading.Thread(target=ghi_goc, daemon=True)
            _L["luong"] = lg
            lg.start()
        return w, h, nw, nh
    finally:
        cg.CGImageRelease(img)
