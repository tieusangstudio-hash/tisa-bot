"""Mở tệp kết quả bằng ứng dụng trên chính máy chủ TISA BOT (bộ TISA).

Bấm link slide/Word/Excel trong chat trên máy tính đang chạy TISA BOT thì mở thẳng bằng PowerPoint,
Word, Excel..., hoặc mở thư mục chứa tệp, không phải tải về. Máy khác vào qua tên miền vẫn tải về như cũ.

Hàng rào:
- Chỉ nhận yêu cầu làm ngay trên máy này: địa chỉ 127.0.0.1, không có header chuyển tiếp của đường hầm,
  Host là localhost, và trình duyệt báo cùng nguồn (chặn trang lạ đổi DNS về 127.0.0.1).
- Vẫn đòi phiên đăng nhập của chủ như mọi đường khác.
- Đường dẫn khoá trong bộ não (_safe_serve_path). Chỉ mở bằng ứng dụng các đuôi tài liệu, ảnh, âm thanh,
  video; tệp chạy được (.app, .command, .sh, .exe...) chỉ được "mở thư mục", không bao giờ chạy.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

from typing import List

from fastapi import Query, Request
from fastapi.responses import FileResponse, JSONResponse

DUOI_MO = {
    "pptx", "ppt", "key", "docx", "doc", "pages", "rtf", "xlsx", "xls", "csv", "numbers", "pdf", "txt", "md",
    "png", "jpg", "jpeg", "gif", "webp", "bmp", "heic", "svg",
    "mp4", "mov", "m4v", "webm", "mkv", "avi", "mp3", "wav", "m4a", "ogg", "flac",
}
_LOOP = ("127.0.0.1", "localhost", "::1")
_CHUYEN_TIEP = ("x-forwarded-for", "x-real-ip", "forwarded", "cf-connecting-ip")


def _host(h):
    h = (h or "").strip().lower()
    if h.startswith("["):
        return h[1:h.find("]")] if "]" in h else h
    return h.rsplit(":", 1)[0] if h.count(":") == 1 else h


def tren_may_chu(request: Request) -> bool:
    ip = request.client.host if request.client else ""
    if ip not in ("127.0.0.1", "::1"):
        return False
    if any(request.headers.get(h) for h in _CHUYEN_TIEP):
        return False
    if _host(request.headers.get("host")) not in _LOOP:
        return False
    site = request.headers.get("sec-fetch-site")
    return site in (None, "", "same-origin")


def _mo(duong, cach):
    duong = str(duong)
    if sys.platform == "darwin":
        # "thu-muc" trên một TỆP thì chỉ ra tệp trong Finder; trên một THƯ MỤC thì mở thẳng thư mục đó.
        lenh = ["open", "-R", duong] if (cach == "thu-muc" and not os.path.isdir(duong)) else ["open", duong]
        subprocess.Popen(lenh, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif os.name == "nt":
        if cach == "thu-muc":
            subprocess.Popen(["explorer", duong] if os.path.isdir(duong) else ["explorer", "/select,", duong])
        else:
            os.startfile(duong)  # noqa: S606 - đuôi đã lọc theo DUOI_MO
    else:
        dich = os.path.dirname(duong) if cach == "thu-muc" else duong
        subprocess.Popen(["xdg-open", dich], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def gan(app, safe_path, brain_root):

    @app.get("/tisa-mo-tep/may-chu")
    async def _may_chu(request: Request):
        return JSONResponse({"may_chu": tren_may_chu(request)}, headers={"cache-control": "no-store"})

    @app.post("/tisa-mo-tep")
    async def _mo_tep(request: Request):
        if not tren_may_chu(request):
            return JSONResponse({"ok": False, "error": "Chỉ mở được trên máy đang chạy TISA BOT"}, status_code=403)
        try:
            body = await request.json()
        except Exception:  # noqa: BLE001
            body = {}
        cach = "thu-muc" if body.get("cach") == "thu-muc" else "mo"
        try:
            f = safe_path(str(body.get("brain") or "brain"), str(body.get("path") or ""))
        except ValueError as e:
            return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
        try:
            goc = Path(brain_root(str(body.get("brain") or "brain"))).resolve()
            that = f.resolve()
        except Exception:  # noqa: BLE001
            return JSONResponse({"ok": False, "error": "Đường dẫn không hợp lệ"}, status_code=400)
        if that != goc and goc not in that.parents:
            return JSONResponse({"ok": False, "error": "Chỉ mở tệp trong bộ não"}, status_code=403)
        f = that
        if not f.exists():
            return JSONResponse({"ok": False, "error": "Không tìm thấy tệp"}, status_code=404)
        if cach == "mo" and (not f.is_file() or f.suffix.lower().lstrip(".") not in DUOI_MO):
            return JSONResponse({"ok": False, "error": "Loại tệp này chỉ mở thư mục"}, status_code=400)
        try:
            _mo(f, cach)
        except Exception as e:  # noqa: BLE001
            return JSONResponse({"ok": False, "error": "Không mở được: %s" % type(e).__name__}, status_code=500)
        return {"ok": True}

    # V2.95: tải NHIỀU tệp một lần thành một .zip (trình xem tệp, trang Kết quả: "Tải tất cả"). Mỗi đường dẫn đi qua đúng hàng rào của /files/raw
    # (_safe_serve_path) và phải nằm trong bộ não; tệp thôi, thư mục bỏ qua; tối đa 300 tệp và 2GB. Video, ảnh, nén sẵn thì lưu không nén cho nhanh.
    @app.get("/tisa-mo-tep/xem-duong")
    async def _xem_duong(brain: str = Query("brain"), p: str = Query("")):
        """AI trả lời bằng ĐƯỜNG DẪN thư mục/tệp (vd `04-ket-qua/.../`): liệt kê ảnh, video, tài liệu bên trong để khung chat hiện thẻ có ảnh thật,
        chủ không phải đi mở thư mục. Chỉ ĐỌC TÊN, khoá trong bộ não, tối đa 300 tệp, sâu 4 tầng, bỏ tệp ẩn."""
        from starlette.concurrency import run_in_threadpool
        DUOI = {"png", "jpg", "jpeg", "webp", "gif", "bmp", "heic", "mp4", "mov", "m4v", "webm", "mp3", "m4a", "wav",
                "pdf", "doc", "docx", "xls", "xlsx", "csv", "ppt", "pptx", "key", "numbers", "pages"}

        def _lam():
            r = _lam_nao()
            if not r.get("files"):      # tệp ở thư mục chủ cho xem thêm ngoài bộ não (tisa_thu_muc_xem.py, 23/11/2026)
                try:
                    import tisa_thu_muc_xem
                    r2 = tisa_thu_muc_xem.xem_duong(p)
                    if r2:
                        return r2
                except Exception:  # noqa: BLE001
                    pass
            return r

        def _lam_nao():
            khong = {"loai": "khong", "files": []}
            try:
                goc = Path(brain_root(brain)).resolve()
            except Exception:  # noqa: BLE001
                return khong
            raw = (p or "").strip().strip("`'\"")
            if not raw or len(raw) > 400 or "://" in raw or ".." in raw.split("/"):
                return khong
            sg = str(goc)
            if raw.startswith(sg + "/"):
                raw = raw[len(sg) + 1:]
            try:
                f = safe_path(brain, raw).resolve()
            except Exception:  # noqa: BLE001
                f = None
            if (f is None or not f.exists()) and "." in raw.rsplit("/", 1)[-1]:
                # (V3.08) AI hay ghi TÊN tệp trần hoặc thiếu thư mục con: dò theo tên trong bộ não, như link tệp trong chat.
                try:
                    import tisa_tim_tep
                    f = tisa_tim_tep.tim(goc, raw)
                except Exception:  # noqa: BLE001
                    f = None
            if f is None or f == goc or goc not in f.parents:
                return khong
            rel = lambda x: x.relative_to(goc).as_posix()  # noqa: E731
            if f.is_file():
                if f.suffix.lower().lstrip(".") not in DUOI:
                    return khong
                return {"loai": "tep", "ten": f.name, "files": [{"path": rel(f), "name": f.name, "size": f.stat().st_size, "sub": ""}], "cat": False}
            if not f.is_dir():
                return khong
            out, cat = [], False

            def di(d, sau):
                nonlocal cat
                try:
                    con = sorted(os.scandir(d), key=lambda e: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", e.name.lower())])
                except OSError:
                    return
                for e in con:
                    if len(out) >= 300:
                        cat = True
                        return
                    if e.name.startswith(".") or e.name in ("node_modules", "__pycache__"):
                        continue
                    try:
                        if e.is_dir(follow_symlinks=False):
                            if sau < 4:
                                di(Path(e.path), sau + 1)
                        elif e.is_file() and e.name.rsplit(".", 1)[-1].lower() in DUOI and "." in e.name:
                            x = Path(e.path)
                            out.append({"path": rel(x), "name": e.name, "size": e.stat().st_size, "sub": x.parent.relative_to(f).as_posix() if x.parent != f else ""})
                    except (OSError, ValueError):
                        continue
            di(f, 0)
            return {"loai": "thu-muc", "ten": f.name, "files": out, "cat": cat}
        return JSONResponse(await run_in_threadpool(_lam))

    @app.get("/tisa-mo-tep/zip")
    async def _zip_nhieu(brain: str = Query("brain"), p: List[str] = Query(default=[]), name: str = Query("tep")):
        import re
        import tempfile
        import zipfile
        from starlette.background import BackgroundTask
        from starlette.concurrency import run_in_threadpool
        if not p:
            return JSONResponse({"ok": False, "error": "Chưa chọn tệp nào"}, status_code=400)
        try:
            goc = Path(brain_root(brain)).resolve()
        except Exception:  # noqa: BLE001
            return JSONResponse({"ok": False, "error": "Không tìm thấy bộ não"}, status_code=400)
        ds, tong = [], 0
        for rel in p[:300]:
            try:
                f = safe_path(brain, str(rel)).resolve()
            except (ValueError, OSError):
                continue
            if f != goc and goc not in f.parents:
                continue
            if f.is_file():
                ds.append(f)
                tong += f.stat().st_size
        if not ds:
            return JSONResponse({"ok": False, "error": "Không có tệp hợp lệ để nén"}, status_code=404)
        if tong > 2 * 1024 ** 3:
            return JSONResponse({"ok": False, "error": "Các tệp nặng quá 2GB, hãy tải từng nhóm nhỏ hơn"}, status_code=413)
        sach = re.sub(r"[^\w\-. ]+", "", name or "tep", flags=re.U).strip()[:60] or "tep"
        fd, tmp = tempfile.mkstemp(prefix="tisa-tep-", suffix=".zip")
        os.close(fd)
        NEN_SAN = {".mp4", ".mov", ".m4v", ".webm", ".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp3", ".m4a", ".zip", ".docx", ".xlsx", ".pptx", ".pdf"}

        def _lam():
            dung = set()
            with zipfile.ZipFile(tmp, "w") as z:
                for f in ds:
                    ten, i = f.name, 2
                    while ten.lower() in dung:
                        ten = "%s (%d)%s" % (f.stem, i, f.suffix)
                        i += 1
                    dung.add(ten.lower())
                    z.write(f, ten, compress_type=zipfile.ZIP_STORED if f.suffix.lower() in NEN_SAN else zipfile.ZIP_DEFLATED)

        def _xoa():
            try:
                os.unlink(tmp)
            except OSError:
                pass
        try:
            await run_in_threadpool(_lam)
        except Exception as e:  # noqa: BLE001
            _xoa()
            return JSONResponse({"ok": False, "error": "Nén thất bại: %s" % type(e).__name__}, status_code=500)
        return FileResponse(tmp, media_type="application/zip", filename=sach + ".zip", background=BackgroundTask(_xoa))
