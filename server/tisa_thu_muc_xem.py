"""tisa_thu_muc_xem.py - Cho khung chat XEM video, ảnh, âm thanh, PDF nằm ở một vài THƯ MỤC CHỈ ĐỊNH ngoài bộ não (chủ chọn 23/11/2026).

Lỗi gốc: video dựng xong để ở Desktop/MKT AI AGENT K01/..., ngoài bộ não. /files/raw bắt đăng nhập nên khoá vùng đọc tệp trong bộ não (đúng chủ ý: mở cả ổ đĩa là
lộ khoá và mật khẩu cho mọi phiên đăng nhập), nên ô video trong chat trả 404 và hiện ô xám.

Cách sửa hẹp: chủ tự thêm từng thư mục cụ thể vào danh sách (trang "Thư mục xem trong chat"). /files/raw hỏi tim(path) trước luật cũ. CHỈ phục vụ tệp:
  - nằm đúng trong một thư mục trong danh sách (đã resolve nên không đi qua ../ và không theo liên kết ra ngoài),
  - có đuôi video, ảnh, âm thanh hoặc PDF (không bao giờ .json, .py, .env, tệp khoá...).
Thư mục thêm vào phải: nằm trong thư mục người dùng, sâu ít nhất 2 cấp (không cho cả Desktop, Documents, cả thư mục người dùng), không có thành phần ẩn (bắt đầu bằng .),
không nằm trong Library và không nằm trong thư mục cài TISA BOT. Vẫn đòi đăng nhập như mọi đường /files/*.
Không ghi khoá hay dữ liệu cá nhân ở đây; danh sách nằm ở server/thu-muc-xem.json (không lên git).
"""
from __future__ import annotations

import json
import os
import re
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEP = ROOT / "server" / "thu-muc-xem.json"
DUOI = {
    ".mp4", ".mov", ".m4v", ".webm", ".mkv",            # video
    ".mp3", ".wav", ".m4a", ".aac", ".ogg",             # âm thanh
    ".jpg", ".jpeg", ".png", ".gif", ".webp",           # ảnh
    ".pdf",
}
_khoa = threading.RLock()


def _nha() -> Path:
    return Path.home().resolve()


def _doc() -> list:
    try:
        d = json.loads(TEP.read_text(encoding="utf-8"))
        return [str(x) for x in (d.get("ds") or []) if isinstance(x, str)]
    except (OSError, ValueError, AttributeError):
        return []


def _ghi(ds: list) -> None:
    with _khoa:
        TEP.parent.mkdir(parents=True, exist_ok=True)
        tmp = TEP.with_suffix(".tmp")
        tmp.write_text(json.dumps({"ds": ds}, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(tmp, TEP)


def kiem_tra(p) -> tuple:
    """(Path đã resolve | None, lý do nếu không hợp lệ)."""
    s = str(p or "").strip()
    if not s or "\x00" in s or len(s) > 500:
        return None, "Chưa nhập đường dẫn thư mục."
    try:
        r = Path(s).expanduser().resolve(strict=True)
    except (OSError, RuntimeError):
        return None, "Không thấy thư mục này trên máy."
    if not r.is_dir():
        return None, "Đây không phải thư mục."
    nha = _nha()
    try:
        con = r.relative_to(nha).parts
    except ValueError:
        return None, "Chỉ cho thêm thư mục nằm trong thư mục người dùng của máy này."
    if len(con) < 2:
        return None, "Thư mục này quá rộng (cả Desktop, Documents hay cả thư mục người dùng). Chọn một thư mục dự án cụ thể, ví dụ Desktop/MKT AI AGENT K01."
    if any(x.startswith(".") for x in con):
        return None, "Không cho thêm thư mục ẩn."
    if con[0].lower() == "library":
        return None, "Không cho thêm thư mục hệ thống (Library)."
    try:
        r.relative_to(ROOT.resolve())
        return None, "Không cho thêm thư mục nằm trong nơi cài TISA BOT."
    except ValueError:
        pass
    try:
        ROOT.resolve().relative_to(r)
        return None, "Thư mục này chứa cả nơi cài TISA BOT, quá rộng."
    except ValueError:
        pass
    return r, ""


def danh_sach() -> list:
    """[{path, co}] co=False khi thư mục không còn trên máy."""
    out = []
    for s in _doc():
        try:
            co = Path(s).is_dir()
        except OSError:
            co = False
        out.append({"path": s, "co": co})
    return out


def them(p) -> dict:
    r, ly_do = kiem_tra(p)
    if r is None:
        return {"ok": False, "loi": ly_do}
    ds = _doc()
    if str(r) not in ds:
        ds.append(str(r))
        _ghi(ds)
    return {"ok": True, "ds": danh_sach()}


def xoa(p) -> dict:
    s = str(p or "").strip()
    ds = [x for x in _doc() if x != s]
    _ghi(ds)
    return {"ok": True, "ds": danh_sach()}


def _cac_thu_muc() -> list:
    out = []
    for s in _doc():
        r, _ = kiem_tra(s)            # kiểm lại mỗi lần: thư mục bị xoá hoặc thành liên kết ra ngoài thì thôi
        if r is not None:
            out.append(r)
    return out


# V3.56 (23/11/2026): AI hay RÚT GỌN tên tệp khi nhắn chat: `023_BacSiTuan_..._V4.mp4` (thật ra là 023_BacSiTuan_NHE_30MB_V4.mp4 và
# 023_BacSiTuan_FULLHD_16x9_V4.mp4). Tên rút gọn không có thật nên khung chat hiện ô xám và bấm xem ra 404. Nay "..." / "…" / "*" trong TÊN tệp
# là ký tự đại diện: khớp mọi tệp media trong thư mục cho xem có đúng phần đầu và phần cuối đó (không vượt qua dấu /).
_TEN_DAI_DIEN = re.compile(r"\.{3,}|…|\*")
_NHO_TIM = {}          # chuỗi tìm -> (giờ, [Path]); /files/raw bị gọi nhiều lần cho một video (Range) nên nhớ 60 giây


def _mau_ten(ten: str):
    """(regex khớp đuôi đường dẫn, có ký tự đại diện không)."""
    t = str(ten or "").replace("\\", "/").strip().lstrip("/")
    phan = _TEN_DAI_DIEN.split(t)
    mau = "[^/]*".join(re.escape(x) for x in phan)
    return re.compile("(^|/)" + mau + "$", re.I), len(phan) > 1


def tim_theo_ten(ten: str, dirs: list | None = None, tran: int = 12) -> list:
    """Mọi tệp media trong thư mục cho xem mà đường dẫn KẾT THÚC bằng `ten` (tên trần hoặc thư-mục/tên, có thể có "..."), mới nhất trước.
    Sâu 4 tầng, tối đa 20000 mục, bỏ tệp/thư mục ẩn, đã resolve và phải nằm trong thư mục cho xem."""
    t = str(ten or "").strip()
    if not t or Path(t.replace("…", ".").rstrip("*")).suffix.lower() not in DUOI and Path(t).suffix.lower() not in DUOI:
        return []
    dirs = _cac_thu_muc() if dirs is None else dirs
    if not dirs:
        return []
    k = t.lower()
    nho = _NHO_TIM.get(k)
    if nho and time.time() - nho[0] < 60 and all(x.is_file() for x in nho[1]):
        return list(nho[1])
    mau, _ = _mau_ten(t)
    dem, thay = 0, []
    for d in dirs:
        for dp, dn, fn in os.walk(d):
            dn[:] = [x for x in dn if not x.startswith(".")]
            if len(Path(dp).relative_to(d).parts) >= 4:
                dn[:] = []
            for n in fn:
                dem += 1
                if dem > 20000:
                    break
                x = Path(dp) / n
                if n.startswith(".") or x.suffix.lower() not in DUOI or not mau.search(x.as_posix()):
                    continue
                try:
                    r = x.resolve()
                    if r.is_file() and any(dd == r.parent or dd in r.parents for dd in dirs) and r not in thay:
                        thay.append(r)
                except OSError:
                    continue
            if dem > 20000:
                break
    thay.sort(key=lambda r: -r.stat().st_mtime)
    thay, thay_cu, da = [], thay, set()          # cùng tên cùng dung lượng ở hai thư mục (bản chép): chỉ lấy bản mới nhất
    for r in thay_cu:
        kk = (r.name.lower(), r.stat().st_size)
        if kk not in da:
            da.add(kk)
            thay.append(r)
    thay = thay[:tran]
    if len(_NHO_TIM) > 200:
        _NHO_TIM.clear()
    if thay:                                    # không nhớ kết quả rỗng: tệp mới ghi xong vài giây sau phải hiện ngay
        _NHO_TIM[k] = (time.time(), thay)
    return list(thay)


def tim(path):
    """Trả Path tệp media nếu `path` trỏ đúng vào một thư mục trong danh sách, ngược lại None (để luật cũ chạy như trước).
    `path` có thể là đường dẫn đầy đủ (có hoặc mất dấu / đầu, khung chat hay bỏ) hoặc tương đối so với thư mục người dùng ("Desktop/...")."""
    p = str(path or "").replace("\\", "/").strip()
    if not p or "\x00" in p or len(p) > 800:
        return None
    if Path(p.lstrip("/")).suffix.lower() not in DUOI:
        return None
    dirs = _cac_thu_muc()
    if not dirs:
        return None
    ung = [Path("/" + p.lstrip("/")), _nha() / p.lstrip("/")]
    for c in ung:
        try:
            r = c.resolve()
        except (OSError, RuntimeError):
            continue
        if r.suffix.lower() in DUOI and any(d == r.parent or d in r.parents for d in dirs):
            try:
                if r.is_file():
                    return r
            except OSError:
                continue
    # Đường dẫn tương đối so với thư mục cho xem ("VIDEO DA DUNG/x.mp4"), tên trần, hoặc tên rút gọn có "...": dò theo tên.
    try:
        kq = tim_theo_ten(p, dirs)
    except (OSError, RuntimeError):
        kq = []
    if kq:
        if _mau_ten(p)[1]:                       # nhiều tệp cùng khớp một tên rút gọn: lấy tệp NHẸ nhất cho xem nhanh
            return min(kq, key=lambda r: r.stat().st_size)
        return kq[0]
    return None


def _rel_nha(r: Path) -> str:
    """Đường dẫn để khung chat gửi lại cho /files/raw: tính từ thư mục người dùng ("Desktop/...") cho gọn."""
    try:
        return r.relative_to(_nha()).as_posix()
    except ValueError:
        return r.as_posix()


def xem_duong(p) -> dict | None:
    """Cho trình xem tệp trong chat (/tisa-mo-tep/xem-duong): AI nhắc TÊN tệp trần, đường dẫn tệp hoặc thư mục nằm ở thư mục chủ đã cho xem.
    Trả cùng dạng với phần bộ não ({loai, ten, files:[{path,name,size,sub}], cat}) hoặc None nếu không khớp gì. Chỉ đuôi media trong DUOI, chỉ trong thư mục danh sách."""
    raw = str(p or "").strip().strip("`'\"").replace("\\", "/")
    if not raw or len(raw) > 500 or "://" in raw or "\x00" in raw or ".." in raw.split("/"):
        return None
    dirs = _cac_thu_muc()
    if not dirs:
        return None

    def mot(r: Path) -> dict:
        return {"path": _rel_nha(r), "name": r.name, "size": r.stat().st_size, "sub": ""}

    # 1. đường dẫn đầy đủ hoặc tính từ thư mục người dùng: tệp (qua tim) hoặc thư mục nằm trong danh sách
    f = None if _mau_ten(raw)[1] else tim(raw)      # tên rút gọn có "...": để bước 2 trả mọi tệp khớp
    if f is not None:
        return {"loai": "tep", "ten": f.name, "files": [mot(f)], "cat": False}
    for c in (Path("/" + raw.lstrip("/")), _nha() / raw.lstrip("/")):
        try:
            r = c.resolve()
            if r.is_dir() and any(d == r or d in r.parents for d in dirs):
                out, cat = [], False
                for dp, dn, fn in os.walk(r):
                    dn[:] = [x for x in sorted(dn) if not x.startswith(".")]
                    if len(Path(dp).relative_to(r).parts) >= 4:
                        dn[:] = []
                    for n in sorted(fn):
                        x = Path(dp) / n
                        if n.startswith(".") or x.suffix.lower() not in DUOI or not x.is_file():
                            continue
                        if len(out) >= 300:
                            cat = True
                            break
                        e = mot(x)
                        e["sub"] = x.parent.relative_to(r).as_posix() if x.parent != r else ""
                        out.append(e)
                    if cat:
                        break
                if out:
                    return {"loai": "thu-muc", "ten": r.name, "files": out, "cat": cat}
        except (OSError, RuntimeError, ValueError):
            continue
    # 2. tên trần ("a.mp4"), "thu-muc-con/a.mp4" hoặc tên rút gọn "a_..._V4.mp4": dò theo tên trong các thư mục cho xem (sâu 4 tầng)
    ten = raw.lstrip("/")
    thay = tim_theo_ten(ten, dirs)
    if not thay:
        return None
    if _mau_ten(ten)[1]:                           # tên rút gọn: trả MỌI tệp khớp (vd bản nhẹ và bản Full HD) để chủ chọn
        return {"loai": "tep", "ten": thay[0].name, "files": [mot(r) for r in thay], "cat": False}
    return {"loai": "tep", "ten": thay[0].name, "files": [mot(thay[0])], "cat": False}   # trùng tên: lấy bản mới nhất


def gan(app) -> None:
    from fastapi import Request
    from fastapi.responses import HTMLResponse, JSONResponse

    trang = ROOT / "dashboard" / "tisa-thu-muc-xem.html"

    @app.get("/tisa-thu-muc-xem/")
    async def _trang():
        try:
            return HTMLResponse(trang.read_text(encoding="utf-8"), headers={"cache-control": "no-cache"})
        except OSError:
            return HTMLResponse("Thiếu trang Thư mục xem trong chat", status_code=500)

    @app.get("/tisa-thu-muc-xem/api/ds")
    async def _ds():
        return JSONResponse({"ok": True, "ds": danh_sach(), "duoi": sorted(DUOI)})

    @app.post("/tisa-thu-muc-xem/api/them")
    async def _them(request: Request):
        try:
            b = await request.json()
        except Exception:  # noqa: BLE001
            b = {}
        r = them((b or {}).get("path"))
        return JSONResponse(r, status_code=200 if r.get("ok") else 400)

    @app.post("/tisa-thu-muc-xem/api/xoa")
    async def _xoa(request: Request):
        try:
            b = await request.json()
        except Exception:  # noqa: BLE001
            b = {}
        return JSONResponse(xoa((b or {}).get("path")))
