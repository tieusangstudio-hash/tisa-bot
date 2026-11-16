"""Duyệt ổ đĩa, thư mục và tệp trên CHÍNH máy đang chạy TISA BOT (bộ TISA, V2.96).

Dùng cho cửa sổ "Lấy dữ liệu từ máy tính" ở nút + của khung chat: chọn thư mục hoặc tệp ngay trên máy để AI làm việc
tại chỗ, không phải tải lên. Việc ghim thư mục làm việc do đường /coding/session/{sid}/pin sẵn có đảm nhiệm, file này
chỉ LIỆT KÊ (đọc), không đọc nội dung, không ghi, không xoá, không chạy gì.

- /may-tinh/diem : lối tắt (Màn hình nền, Tài liệu, Tải xuống, Ảnh, Video, Bộ não...), ổ đĩa, tên máy.
- /may-tinh/duyet: liệt kê thư mục con và tệp của một thư mục (ẩn tệp ẩn, tệp hệ thống), kèm đường dẫn cha và đường dẫn từng tầng.

Hàng rào: vẫn đòi phiên đăng nhập như mọi đường khác của TISA BOT (do lớp bảo vệ chung), chỉ đọc tên, cỡ, ngày sửa.
"""
import os
import platform
import socket
import string
import sys
import time
from pathlib import Path

from fastapi import Query
from fastapi.responses import JSONResponse

TOI_DA = 3000          # tối đa số dòng trả về một lần
HAN_GIAY = 4.0         # quét thư mục khổng lồ hay ổ mạng chậm thì dừng, báo "bị cắt"
AN = {".ds_store", "thumbs.db", "desktop.ini", "ntuser.dat", "$recycle.bin", "system volume information", "lost+found"}

LOAI = {
    "anh": {"png", "jpg", "jpeg", "gif", "webp", "bmp", "heic", "heif", "svg", "tif", "tiff", "psd", "ai", "raw", "cr2", "nef", "dng"},
    "video": {"mp4", "mov", "m4v", "webm", "mkv", "avi", "wmv", "flv", "mts", "m2ts", "3gp", "prproj", "drp", "fcpbundle"},
    "am": {"mp3", "wav", "m4a", "aac", "ogg", "flac", "aiff"},
    "van-ban": {"doc", "docx", "pdf", "txt", "rtf", "odt", "pages", "md", "epub"},
    "bang": {"xls", "xlsx", "csv", "numbers", "ods", "tsv"},
    "slide": {"ppt", "pptx", "key", "odp"},
    "ma": {"py", "js", "ts", "tsx", "jsx", "json", "html", "css", "sh", "yml", "yaml", "xml", "sql", "php", "java", "go", "rs", "swift", "kt", "c", "cpp", "h"},
    "nen": {"zip", "rar", "7z", "tar", "gz", "dmg", "iso", "pkg", "exe", "msi", "apk"},
}
DUOI_LOAI = {e: k for k, ds in LOAI.items() for e in ds}


def _loai(ten: str) -> str:
    return DUOI_LOAI.get(ten.rsplit(".", 1)[-1].lower(), "khac") if "." in ten else "khac"


def _la_thu_muc(p: Path) -> bool:
    try:
        return p.is_dir()
    except OSError:
        return False


def _o_dia():
    """Danh sách ổ đĩa / nơi gắn có thật, mỗi dòng {ten, duong_dan, loai}."""
    ds = []
    if os.name == "nt":
        for d in string.ascii_uppercase:
            p = d + ":\\"
            try:
                if os.path.exists(p):
                    ds.append({"ten": "Ổ %s:" % d, "duong_dan": p, "loai": "o"})
            except OSError:
                continue
        return ds
    if sys.platform == "darwin":
        ds.append({"ten": "Máy này (Macintosh HD)", "duong_dan": "/", "loai": "o"})
        try:
            for e in sorted(os.scandir("/Volumes"), key=lambda x: x.name.lower()):
                try:
                    if e.is_symlink() and os.path.realpath(e.path) == "/":
                        continue          # "Macintosh HD" trỏ về gốc, đã có dòng trên
                    if e.is_dir():
                        ds.append({"ten": e.name, "duong_dan": e.path, "loai": "ngoai"})
                except OSError:
                    continue
        except OSError:
            pass
        return ds
    ds.append({"ten": "Máy này (/)", "duong_dan": "/", "loai": "o"})
    for goc in ("/mnt", "/media", "/media/" + (os.environ.get("USER") or "")):
        try:
            for e in sorted(os.scandir(goc), key=lambda x: x.name.lower()):
                if e.is_dir() and not e.name.startswith("."):
                    ds.append({"ten": e.name, "duong_dan": e.path, "loai": "ngoai"})
        except OSError:
            continue
    return ds


def _loi_tat(home: Path):
    """Lối tắt hay dùng: chỉ những chỗ có thật trên máy."""
    cap = [
        ("man-hinh", "Màn hình nền", ["Desktop", "OneDrive/Desktop"]),
        ("tai-lieu", "Tài liệu", ["Documents", "OneDrive/Documents"]),
        ("tai-ve", "Tải xuống", ["Downloads"]),
        ("anh", "Ảnh", ["Pictures", "OneDrive/Pictures"]),
        ("video", "Phim và video", ["Movies", "Videos"]),
        ("nhac", "Nhạc", ["Music"]),
        ("icloud", "iCloud Drive", ["Library/Mobile Documents/com~apple~CloudDocs"]),
        ("onedrive", "OneDrive", ["OneDrive"]),
        ("dropbox", "Dropbox", ["Dropbox"]),
        ("gdrive", "Google Drive", ["Google Drive", "My Drive", "Library/CloudStorage/GoogleDrive"]),
    ]
    ds = []
    for ma, ten, cons in cap:
        for con in cons:
            p = home / con
            if _la_thu_muc(p):
                ds.append({"ma": ma, "ten": ten, "duong_dan": str(p)})
                break
    return ds


def _tang(p: str):
    """Đường dẫn từng tầng để bấm quay lại: [{ten, duong_dan}]."""
    out = []
    if os.name == "nt":
        drive, rest = os.path.splitdrive(p)
        cur = drive + "\\"
        if drive:
            out.append({"ten": drive, "duong_dan": cur})
        for part in [x for x in rest.replace("/", "\\").split("\\") if x]:
            cur = os.path.join(cur, part)
            out.append({"ten": part, "duong_dan": cur})
        return out
    out.append({"ten": "/", "duong_dan": "/"})
    cur = ""
    for part in [x for x in p.split("/") if x]:
        cur += "/" + part
        out.append({"ten": part, "duong_dan": cur})
    return out


def _loi_quyen(p: str) -> str:
    if sys.platform == "darwin":
        return ("macOS đang chặn TISA BOT mở thư mục này. Mở Cài đặt hệ thống > Quyền riêng tư và bảo mật > "
                "Truy cập toàn bộ ổ đĩa (hoặc Tệp và thư mục), bật cho TISA BOT rồi bấm Làm mới.")
    return "Không có quyền mở thư mục này. Thử thư mục khác, hoặc chạy TISA BOT bằng tài khoản có quyền."


def _duyet(path: str, hien_an: bool, brain_root: str) -> dict:
    home = Path.home()
    raw = (path or "").strip()
    if not raw:
        if os.name == "nt":      # gốc của Windows = danh sách ổ đĩa
            ds = [{"ten": o["ten"], "path": o["duong_dan"], "dir": True, "size": 0, "mtime": 0, "kind": "o"} for o in _o_dia()]
            return {"path": "", "ten": "Máy này", "parent": None, "crumbs": [], "items": ds, "thu_muc": len(ds), "tep": 0, "cat": False}
        raw = str(home)
    try:
        p = os.path.abspath(os.path.expanduser(raw))
    except Exception:
        return {"loi": "Đường dẫn không hợp lệ.", "items": []}
    if not os.path.isdir(p):
        return {"loi": "Thư mục này không còn nữa.", "path": p, "parent": os.path.dirname(p) or None, "crumbs": _tang(p), "items": []}
    cha = os.path.dirname(p.rstrip("\\/")) or None
    if cha == p:
        cha = None
    if os.name == "nt" and cha and len(cha.rstrip("\\/")) <= 2:
        cha = ""        # lên một tầng nữa là danh sách ổ đĩa
    kq = {"path": p, "ten": os.path.basename(p.rstrip("\\/")) or p, "parent": cha, "crumbs": _tang(p), "items": [], "cat": False,
          "trong_bo_nao": bool(brain_root and (p == brain_root or p.startswith(brain_root.rstrip("\\/") + os.sep)))}
    han = time.monotonic() + HAN_GIAY
    try:
        with os.scandir(p) as it:
            for e in it:
                ten = e.name
                if not hien_an and (ten.startswith(".") or ten.startswith("$") or ten.startswith("~$") or ten.lower() in AN):
                    continue
                if ten.lower() in AN and ten.lower() != "lost+found":
                    continue
                try:
                    la_dir = e.is_dir()
                    st = e.stat()
                except OSError:
                    continue
                kq["items"].append({"name": ten, "path": e.path, "dir": la_dir, "size": 0 if la_dir else int(st.st_size),
                                    "mtime": int(st.st_mtime), "kind": "thu-muc" if la_dir else _loai(ten)})
                if len(kq["items"]) >= TOI_DA or time.monotonic() > han:
                    kq["cat"] = True
                    break
    except PermissionError:
        kq["loi"] = _loi_quyen(p)
    except OSError as e:
        kq["loi"] = "Không đọc được thư mục này: %s" % e
    kq["items"].sort(key=lambda x: (not x["dir"], x["name"].lower()))
    kq["thu_muc"] = sum(1 for x in kq["items"] if x["dir"])
    kq["tep"] = len(kq["items"]) - kq["thu_muc"]
    return kq


def gan(app, brain_root_fn=None):
    def _goc_nao():
        try:
            return str(brain_root_fn("brain")) if brain_root_fn else ""
        except Exception:
            return ""

    @app.get("/may-tinh/diem")
    def may_tinh_diem():
        home = Path.home()
        nao = _goc_nao()
        ds = _loi_tat(home)
        if nao and _la_thu_muc(Path(nao)):
            ds.insert(0, {"ma": "bo-nao", "ten": "Bộ não TISA BOT", "duong_dan": nao})
        ds.append({"ma": "home", "ten": "Thư mục cá nhân", "duong_dan": str(home)})
        try:
            ten_may = socket.gethostname().replace(".local", "")
        except Exception:
            ten_may = ""
        he = {"darwin": "Mac", "win32": "Windows"}.get(sys.platform, platform.system() or "Linux")
        return JSONResponse({"may": ten_may, "he": he, "loi_tat": ds, "o_dia": _o_dia(), "home": str(home)})

    @app.get("/may-tinh/duyet")
    def may_tinh_duyet(path: str = Query("", description="Thư mục cần liệt kê; rỗng = thư mục cá nhân (Windows: danh sách ổ đĩa)"),
                       hien_an: int = Query(0, description="1 = hiện cả tệp ẩn")):
        return JSONResponse(_duyet(path, bool(hien_an), _goc_nao()))
