"""tisa_ban_phim.py - Đọc và đổi nguồn nhập bàn phím macOS (Text Input Source) bằng ctypes, để lúc gõ mật khẩu không bị bộ gõ Telex/VNI biến chữ.

  hien_tai()            id nguồn nhập đang dùng, ví dụ "com.apple.keylayout.ABC" hoặc "com.apple.inputmethod.VietnameseIM.VietnameseTelex"; "" nếu không đọc được.
  chon(id)              chuyển sang nguồn nhập đó; True nếu được.
  tam_dung_abc()        context manager: chuyển sang bàn phím ABC (không bộ gõ) trong khối lệnh, thoát ra thì trả lại nguồn cũ.

Chỉ macOS. Lỗi thì trả rỗng/False và không làm hỏng việc đang làm (gõ tiếp bằng nguồn hiện có).
"""
from __future__ import annotations

import contextlib
import ctypes
import sys

ABC = "com.apple.keylayout.ABC"
_lib = {}


def _nap():
    if _lib:
        return _lib
    if sys.platform != "darwin":
        return None
    try:
        hit = ctypes.CDLL("/System/Library/Frameworks/Carbon.framework/Versions/A/Frameworks/HIToolbox.framework/HIToolbox")
        cf = ctypes.CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
    except OSError:
        return None
    vp = ctypes.c_void_p
    hit.TISCopyCurrentKeyboardInputSource.restype = vp
    hit.TISGetInputSourceProperty.argtypes = [vp, vp]
    hit.TISGetInputSourceProperty.restype = vp
    hit.TISCreateInputSourceList.argtypes = [vp, ctypes.c_bool]
    hit.TISCreateInputSourceList.restype = vp
    hit.TISSelectInputSource.argtypes = [vp]
    hit.TISSelectInputSource.restype = ctypes.c_int32
    cf.CFStringCreateWithCString.argtypes = [vp, ctypes.c_char_p, ctypes.c_uint32]
    cf.CFStringCreateWithCString.restype = vp
    cf.CFStringGetCString.argtypes = [vp, ctypes.c_char_p, ctypes.c_long, ctypes.c_uint32]
    cf.CFStringGetCString.restype = ctypes.c_bool
    cf.CFDictionaryCreate.argtypes = [vp, ctypes.POINTER(vp), ctypes.POINTER(vp), ctypes.c_long, vp, vp]
    cf.CFDictionaryCreate.restype = vp
    cf.CFArrayGetCount.argtypes = [vp]
    cf.CFArrayGetCount.restype = ctypes.c_long
    cf.CFArrayGetValueAtIndex.argtypes = [vp, ctypes.c_long]
    cf.CFArrayGetValueAtIndex.restype = vp
    cf.CFRelease.argtypes = [vp]
    try:
        khoa = vp.in_dll(hit, "kTISPropertyInputSourceID")
    except ValueError:
        return None
    _lib.update({"hit": hit, "cf": cf, "khoa": khoa})
    return _lib


def _chuoi(cf, ref) -> str:
    if not ref:
        return ""
    buf = ctypes.create_string_buffer(256)
    return buf.value.decode("utf-8", "ignore") if cf.CFStringGetCString(ref, buf, 256, 0x08000100) else ""


def hien_tai() -> str:
    L = _nap()
    if not L:
        return ""
    try:
        src = L["hit"].TISCopyCurrentKeyboardInputSource()
        if not src:
            return ""
        idv = L["hit"].TISGetInputSourceProperty(src, L["khoa"])
        kq = _chuoi(L["cf"], idv)
        L["cf"].CFRelease(src)
        return kq
    except Exception:  # noqa: BLE001
        return ""


def chon(id_muon: str) -> bool:
    L = _nap()
    if not L or not id_muon:
        return False
    cf, hit = L["cf"], L["hit"]
    try:
        gia_tri = cf.CFStringCreateWithCString(None, id_muon.encode(), 0x08000100)
        keys = (ctypes.c_void_p * 1)(L["khoa"].value)
        vals = (ctypes.c_void_p * 1)(gia_tri)
        flt = cf.CFDictionaryCreate(None, keys, vals, 1, None, None)
        ds = hit.TISCreateInputSourceList(flt, False)
        ok = False
        if ds and cf.CFArrayGetCount(ds) > 0:
            ok = hit.TISSelectInputSource(cf.CFArrayGetValueAtIndex(ds, 0)) == 0
        for r in (ds, flt, gia_tri):
            if r:
                cf.CFRelease(r)
        return ok
    except Exception:  # noqa: BLE001
        return False


@contextlib.contextmanager
def tam_dung_abc():
    """Trong khối lệnh: bàn phím ABC. Thoát: trả lại nguồn cũ. Dùng khi gõ mật khẩu để Telex không biến chữ (aa, dd, ow...)."""
    cu = hien_tai()
    doi = bool(cu and cu != ABC and chon(ABC))
    try:
        yield {"truoc": cu, "da_doi": doi}
    finally:
        if doi:
            chon(cu)
