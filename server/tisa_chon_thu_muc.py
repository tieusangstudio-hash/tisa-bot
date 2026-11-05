"""Lối tắt và gợi ý cho hộp chọn thư mục bộ não: học viên không phải đi từ gốc ổ đĩa xuống."""
import os
import string
import time
import unicodedata
from pathlib import Path

BO_QUA = {"node_modules", "library", "applications", "appdata", "pictures", "movies", "music", "public"}
TU_KHOA = ("bo nao", "brain", "obsidian", "vault")
HAN_GIAY = 2.0
TOI_DA = 6


def _khong_dau(s):
    s = unicodedata.normalize("NFD", s.lower()).replace("đ", "d")
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def _co_ve_bo_nao(p):
    """Thư mục mở bằng Obsidian, có sổ tay AI, hoặc tên có chữ bộ não."""
    try:
        if (p / ".obsidian").is_dir() or (p / "CLAUDE.md").is_file() or ((p / "wiki").is_dir() and (p / "raw").is_dir()):
            return True
    except OSError:
        return False
    ten = _khong_dau(p.name)
    return any(k in ten for k in TU_KHOA)


def _noi_quen(home):
    cap = [("Màn hình", ["Desktop", "OneDrive/Desktop"]), ("Tài liệu", ["Documents", "OneDrive/Documents"]), ("Tải về", ["Downloads"]),
           ("iCloud", ["Library/Mobile Documents/com~apple~CloudDocs"]), ("OneDrive", ["OneDrive"])]
    ds = []
    for ten, ten_con in cap:
        for con in ten_con:
            p = home / con
            if p.is_dir():
                ds.append({"ten": ten, "duong_dan": str(p)})
                break
    ds.append({"ten": "Thư mục cá nhân", "duong_dan": str(home)})
    if os.name == "nt":
        ds += [{"ten": "Ổ %s:" % d, "duong_dan": d + ":\\"} for d in string.ascii_uppercase if os.path.exists(d + ":\\")]
    return ds


def _quet(goc, sau, het_gio, thay):
    """Đi xuống tối đa `sau` tầng, có hạn giờ vì có máy cả chục nghìn thư mục."""
    try:
        con = sorted(os.scandir(goc), key=lambda e: e.name.lower())
    except OSError:
        return
    for e in con:
        if time.monotonic() > het_gio or len(thay) >= TOI_DA:
            return
        if e.name.startswith((".", "$")) or e.name.lower() in BO_QUA:
            continue
        try:
            if not e.is_dir():
                continue
        except OSError:
            continue
        p = Path(e.path)
        if _co_ve_bo_nao(p):
            thay[str(p)] = {"ten": unicodedata.normalize("NFC", p.name), "duong_dan": str(p)}
        elif sau > 1:
            _quet(p, sau - 1, het_gio, thay)


def goi_y():
    home = Path(os.path.expanduser("~"))
    noi = _noi_quen(home)
    thay, het_gio = {}, time.monotonic() + HAN_GIAY
    for n in noi:
        if os.name != "nt" or not n["ten"].startswith("Ổ "):
            _quet(Path(n["duong_dan"]), 3 if n["ten"] != "Thư mục cá nhân" else 1, het_gio, thay)
    return {"noi": noi, "goi_y": list(thay.values())}
