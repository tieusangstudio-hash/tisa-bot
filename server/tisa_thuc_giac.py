"""tisa_thuc_giac.py - Giữ máy thức khi có việc nền dài (dựng video chạy nhiều giờ), tắt khi xong; mở khóa lại nếu máy khóa giữa chừng.

  giu(ly_do, toi_da_phut, uy_quyen_mo_khoa="")   bật giữ thức (macOS: caffeinate -dims -w <pid máy chủ>; Windows: SetThreadExecutionState). Trả mã phiên.
  tha(ma)                                        bỏ một phiên; hết phiên cuối thì tắt caffeinate.
  giu_viec(job) / tha_viec(job)                  móc tự động quanh MỖI việc nền của TISA BOT (tasks.py): việc chạy thì thức, xong thì thôi.

Mở khóa tự động giữa chừng: chỉ phiên có `uy_quyen_mo_khoa` (nhãn kênh đã xác thực cấp quyền, ví dụ "dashboard") mới được. Quyền này chỉ được cấp khi
anh yêu cầu từ kênh của anh và đã duyệt (tisa_desktop, op=giu_may_thuc tu_mo_khoa=true); hết phiên là hết quyền; vẫn giới hạn 3 lần thất bại của mo_khoa.
Nhật ký: dieu-khien-may/thuc-giac-nhat-ky.jsonl (giờ, mã phiên, việc gì, bật hay tắt; không có bí mật).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

try:
    import config as _cfg
    STATE_DIR = Path(_cfg.STATE_DIR)
except Exception:  # noqa: BLE001
    STATE_DIR = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)

DIR = STATE_DIR / "dieu-khien-may"
TEP_NK = DIR / "thuc-giac-nhat-ky.jsonl"
TOI_DA_PHUT = 12 * 60
CHU_KY = 20.0                       # giây giữa hai lần xem máy có khóa không
_lock = threading.RLock()
_phien: dict = {}
_cf = {"proc": None}
_theo_doi = {"thread": None, "dung": False}
# Móc cho mở khóa tự động (tisa_desktop đặt vào lúc đăng ký): ham_khoa() -> tên ứng dụng ở trước; ham_mo(nhan_kenh) -> chuỗi kết quả
MOC = {"ung_dung_truoc": None, "mo_khoa": None, "bao": None}


def _ghi(ma: str, hanh_dong: str, ly_do: str = "") -> None:
    try:
        DIR.mkdir(parents=True, exist_ok=True)
        with open(TEP_NK, "a", encoding="utf-8") as f:
            f.write(json.dumps({"luc": time.strftime("%Y-%m-%d %H:%M:%S"), "ma": ma, "hanh_dong": hanh_dong, "ly_do": str(ly_do)[:100]}, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _bat_caffeinate() -> None:
    if _cf["proc"] is not None and _cf["proc"].poll() is None:
        return
    if sys.platform == "darwin":
        try:
            _cf["proc"] = subprocess.Popen(["/usr/bin/caffeinate", "-dims", "-w", str(os.getpid())], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError:
            _cf["proc"] = None
    elif sys.platform == "win32":
        def _giu():
            import ctypes
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000003)    # ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
            while not _cf.get("ngung"):
                time.sleep(5)
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
        _cf["ngung"] = False
        t = threading.Thread(target=_giu, daemon=True)
        t.start()
        _cf["proc"] = t


def _tat_caffeinate() -> None:
    p = _cf["proc"]
    _cf["proc"] = None
    if p is None:
        return
    if sys.platform == "win32":
        _cf["ngung"] = True
        return
    try:
        p.terminate()
        p.wait(timeout=3)
    except Exception:  # noqa: BLE001
        pass


def dang_giu() -> bool:
    p = _cf["proc"]
    if p is None:
        return False
    return (p.poll() is None) if hasattr(p, "poll") else bool(getattr(p, "is_alive", lambda: False)())


def danh_sach() -> list:
    now = time.time()
    with _lock:
        return [{"ma": k, "ly_do": v["ly_do"], "con_phut": max(0, int((v["den"] - now) / 60)), "tu_mo_khoa": bool(v["uy_quyen"])} for k, v in _phien.items()]


def _het_han() -> None:
    now = time.time()
    for k in [k for k, v in _phien.items() if v["den"] < now]:
        _phien.pop(k, None)
        _ghi(k, "hết hạn", "")


def giu(ly_do: str, toi_da_phut: int = 240, uy_quyen_mo_khoa: str = "", ma: str = "") -> str:
    with _lock:
        _het_han()
        ma = ma or uuid.uuid4().hex[:8]
        _phien[ma] = {"ly_do": str(ly_do)[:100], "den": time.time() + max(1, min(int(toi_da_phut or 240), TOI_DA_PHUT)) * 60, "uy_quyen": str(uy_quyen_mo_khoa or "")}
        _bat_caffeinate()
        _ghi(ma, "bật giữ thức" + (" + cho phép mở khóa lại (kênh %s)" % uy_quyen_mo_khoa if uy_quyen_mo_khoa else ""), ly_do)
        _bat_theo_doi()
    return ma


def tha(ma: str) -> bool:
    with _lock:
        co = _phien.pop(ma, None) is not None
        _het_han()
        if co:
            _ghi(ma, "tắt giữ thức", "")
        if not _phien:
            _tat_caffeinate()
    return co


def giu_viec(job: str) -> str:
    """Móc trong tasks.py: một việc nền bắt đầu. Không bao giờ ném lỗi."""
    try:
        return giu("việc nền " + str(job)[:60], 12 * 60, "", "job:" + str(job)[:50])
    except Exception:  # noqa: BLE001
        return ""


def tha_viec(job: str) -> None:
    try:
        tha("job:" + str(job)[:50])
    except Exception:  # noqa: BLE001
        pass


# ---------------------------------------------------------------- mở khóa lại giữa chừng (chỉ phiên được cấp quyền)
def _vong_theo_doi() -> None:
    while not _theo_doi["dung"]:
        time.sleep(CHU_KY)
        with _lock:
            _het_han()
            if not _phien:
                _tat_caffeinate()
                _theo_doi["thread"] = None
                return
            kenh = next((v["uy_quyen"] for v in _phien.values() if v["uy_quyen"]), "")
        if not kenh or not MOC["ung_dung_truoc"] or not MOC["mo_khoa"]:
            continue
        try:
            truoc = str(MOC["ung_dung_truoc"]() or "").lower()
        except Exception:  # noqa: BLE001
            continue
        if truoc == "loginwindow":
            _ghi("theo-doi", "máy khóa giữa chừng", "thử mở khóa lại theo quyền của kênh " + kenh)
            try:
                kq = str(MOC["mo_khoa"](kenh))
            except Exception as e:  # noqa: BLE001
                kq = "LOI " + type(e).__name__
            _ghi("theo-doi", "kết quả mở khóa lại", kq.split(":", 1)[0][:30])
            if MOC["bao"]:
                try:
                    MOC["bao"]("Máy khóa giữa lúc làm việc nền. " + ("Em đã mở khóa lại, việc nền chạy tiếp." if kq.startswith("DA_MO_KHOA") else "Em chưa mở được (%s). Anh xem giúp em." % kq.split(":", 1)[0]))
                except Exception:  # noqa: BLE001
                    pass


def _bat_theo_doi() -> None:
    if _theo_doi["thread"] is not None and _theo_doi["thread"].is_alive():
        return
    _theo_doi["dung"] = False
    t = threading.Thread(target=_vong_theo_doi, daemon=True, name="tisa-thuc-giac")
    _theo_doi["thread"] = t
    t.start()
