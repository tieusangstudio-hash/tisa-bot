"""tisa_quay_man_hinh.py - Quay video và chụp màn hình theo CỬA SỔ hoặc VÙNG, lưu vào brain: 04-ket-qua/<YYYY-MM>/<YYYY-MM-DD>-<mô-tả>/.

  chup_cua_so(ten_ung_dung|vung, mo_ta)   ảnh PNG đúng cửa sổ của một ứng dụng (lấy vị trí cửa sổ trước, rồi chụp vùng đó) hoặc đúng vùng x,y,w,h.
  quay_bat(ten_ung_dung|vung, giay, mo_ta) quay video MOV bằng `screencapture -v` (có -V giây để tự dừng); dự phòng ffmpeg avfoundation (engine="ffmpeg").
  quay_dung()                              dừng bản đang quay (SIGINT: screencapture tự đóng tệp cho đúng).
  trang_thai()                             đang quay không, tệp nào.

Cần quyền macOS "Ghi màn hình" cho chương trình chạy TISA BOT (giống chụp màn hình). Không quay khi ứng dụng ở trước là ứng dụng mật khẩu, khóa, ví, ngân hàng
(tisa_desktop kiểm trước khi gọi vào đây). Tối đa 1 giờ mỗi bản quay. Chỉ macOS (Windows chưa làm).
"""
from __future__ import annotations

import os
import re
import signal
import subprocess
import sys
import threading
import time
import unicodedata
from pathlib import Path

TOI_DA_GIAY = 3600
_lock = threading.Lock()
_dang = {"proc": None, "tep": "", "luc": 0.0, "thu_muc": ""}


def _slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s or "")).replace("đ", "d").replace("Đ", "D")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return (s or "man-hinh")[:50]


def goc_brain(vault_root=None) -> Path:
    for c in (vault_root, os.environ.get("TISA_BRAIN_ROOT"), Path.home() / "tisa-os" / "brains" / "Brain Default"):
        if c:
            p = Path(str(c)).expanduser()
            if p.is_dir():
                return p
    return Path.home() / "tisa-os" / "brains" / "Brain Default"


def thu_muc_ket_qua(vault_root, mo_ta: str, ngay: str = "") -> Path:
    ngay = ngay or time.strftime("%Y-%m-%d")
    d = goc_brain(vault_root) / "04-ket-qua" / ngay[:7] / ("%s-%s" % (ngay, _slug(mo_ta)))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _tep_moi(d: Path, tien_to: str, duoi: str) -> Path:
    return d / ("%s-%s.%s" % (tien_to, time.strftime("%H%M%S"), duoi))


def _chay(cmd, timeout=10):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()


def vung_cua_so(ten_ung_dung: str):
    """(x, y, w, h) của cửa sổ đầu của ứng dụng, hoặc None. Hỏi System Events (cần quyền Trợ năng đã có)."""
    ten = str(ten_ung_dung or "").replace('"', "").strip()
    if not ten:
        return None
    ma = ('tell application "System Events" to tell process "%s" to get {position, size} of window 1' % ten)
    try:
        rc, out, _ = _chay(["/usr/bin/osascript", "-e", ma], 8)
    except (OSError, subprocess.SubprocessError):
        return None
    so = re.findall(r"-?\d+", out)
    if rc != 0 or len(so) < 4:
        return None
    x, y, w, h = (int(v) for v in so[:4])
    return (max(0, x), max(0, y), max(8, w), max(8, h))


def _vung_chuoi(v) -> str:
    return "%d,%d,%d,%d" % tuple(int(i) for i in v)


def chup_cua_so(vault_root, mo_ta: str, ten_ung_dung: str = "", vung=None) -> tuple[bool, str]:
    """Chụp PNG. Trả (ok, đường dẫn hoặc lý do)."""
    if sys.platform != "darwin":
        return False, "Chụp theo cửa sổ hiện chỉ làm cho macOS."
    v = tuple(vung) if vung else (vung_cua_so(ten_ung_dung) if ten_ung_dung else None)
    if ten_ung_dung and not v:
        return False, "Không lấy được vị trí cửa sổ của \"%s\" (ứng dụng chưa mở, chưa có cửa sổ, hoặc chưa cấp quyền Trợ năng)." % ten_ung_dung
    d = thu_muc_ket_qua(vault_root, mo_ta)
    f = _tep_moi(d, "chup", "png")
    cmd = ["/usr/sbin/screencapture", "-x"] + (["-R", _vung_chuoi(v)] if v else []) + [str(f)]
    try:
        rc, _, err = _chay(cmd, 15)
    except (OSError, subprocess.SubprocessError) as e:
        return False, "Không chụp được: %s" % type(e).__name__
    if rc != 0 or not f.exists() or f.stat().st_size == 0:
        return False, "Không chụp được (%s). Kiểm tra quyền Ghi màn hình." % (err[:80] or "tệp rỗng")
    return True, str(f)


def quay_bat(vault_root, mo_ta: str, giay: int = 60, ten_ung_dung: str = "", vung=None, engine: str = "screencapture", am_thanh: bool = False) -> tuple[bool, str]:
    if sys.platform != "darwin":
        return False, "Quay màn hình hiện chỉ làm cho macOS."
    giay = max(2, min(int(giay or 60), TOI_DA_GIAY))
    with _lock:
        p = _dang["proc"]
        if p is not None and p.poll() is None:
            return False, "Đang quay dở (%s). Gọi quay_dung trước." % _dang["tep"]
        v = tuple(vung) if vung else (vung_cua_so(ten_ung_dung) if ten_ung_dung else None)
        if ten_ung_dung and not v:
            return False, "Không lấy được vị trí cửa sổ của \"%s\"." % ten_ung_dung
        d = thu_muc_ket_qua(vault_root, mo_ta)
        if engine == "ffmpeg":
            f = _tep_moi(d, "quay", "mp4")
            ff = "ffmpeg"
            cmd = [ff, "-y", "-loglevel", "error", "-f", "avfoundation", "-framerate", "30", "-capture_cursor", "1", "-i", "Capture screen 0:none", "-t", str(giay)]
            if v:
                cmd += ["-vf", "crop=%d:%d:%d:%d" % (v[2] * 2, v[3] * 2, v[0] * 2, v[1] * 2)]      # avfoundation tính theo điểm ảnh thật (màn Retina gấp đôi)
            cmd += ["-pix_fmt", "yuv420p", str(f)]
        else:
            f = _tep_moi(d, "quay", "mov")
            cmd = ["/usr/sbin/screencapture", "-x", "-v", "-V", str(giay)] + (["-g"] if am_thanh else []) + (["-R", _vung_chuoi(v)] if v else []) + [str(f)]
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, start_new_session=True)
        except OSError as e:
            return False, "Không bắt đầu quay được: %s" % type(e).__name__
        _dang.update({"proc": proc, "tep": str(f), "luc": time.time(), "thu_muc": str(d)})
    return True, str(f)


def quay_dung(cho_giay: float = 15.0) -> tuple[bool, str]:
    with _lock:
        p, f = _dang["proc"], _dang["tep"]
        if p is None:
            return False, "Không có bản quay nào đang chạy."
        if p.poll() is None:
            try:
                p.send_signal(signal.SIGINT)
            except OSError:
                pass
    try:
        p.wait(timeout=cho_giay)
    except subprocess.TimeoutExpired:
        p.kill()
    with _lock:
        _dang["proc"] = None
    fp = Path(f)
    if fp.exists() and fp.stat().st_size > 0:
        return True, f
    err = ""
    try:
        err = (p.stderr.read() or b"").decode("utf-8", "ignore")[:100] if p.stderr else ""
    except Exception:  # noqa: BLE001
        pass
    return False, "Không có tệp video (%s). Kiểm tra quyền Ghi màn hình." % (err or "tệp rỗng")


def trang_thai() -> dict:
    with _lock:
        p = _dang["proc"]
        dang = p is not None and p.poll() is None
        return {"dang_quay": dang, "tep": _dang["tep"], "giay_da_quay": int(time.time() - _dang["luc"]) if dang else 0}
