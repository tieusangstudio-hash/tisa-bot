"""tisa_bao_anh.py - Báo anh khi gặp bước chỉ người thật làm được (Touch ID, mã khóa, CAPTCHA, OTP) rồi chờ tới khi anh làm xong.

  bao(noi_dung, loop)            gửi MỘT tin ngắn tới anh: chuông và khung chat TISA Core trên dashboard (+ Telegram của chủ nếu có), và Zalo của anh nếu đã khai
                                  trong dieu-khien-may/mo-khoa-cau-hinh.json (zalo_ids). Luôn ghi dieu-khien-may/bao-anh.jsonl. Trùng nội dung trong 10 phút chỉ gửi một lần.
  cho_nguoi_that(het_chan, ...)  tạm dừng đúng chỗ: chờ tới khi het_chan() trả True (anh đã làm xong), nhắc lại sau mỗi 10 phút, tối đa N phút; anh bấm
                                  "Em làm xong rồi" (cờ nguoi_xong của Trình duyệt TISA) hoặc "Dừng AI ngay" thì thoát ngay.

Tin báo CHỈ chứa lý do (ví dụ "Máy hiện hộp Touch ID, anh xác thực giúp em"). Không bao giờ chứa mật khẩu, mã, khóa.
"""
from __future__ import annotations

import asyncio
import json
import sys
import threading
import time
from pathlib import Path

try:
    import config as _cfg
    STATE_DIR = Path(_cfg.STATE_DIR)
except Exception:  # noqa: BLE001
    import os
    STATE_DIR = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)

DIR = STATE_DIR / "dieu-khien-may"
TEP = DIR / "bao-anh.jsonl"
TEP_CH = DIR / "mo-khoa-cau-hinh.json"
NHAC_LAI = 10 * 60
_lock = threading.Lock()
_gan_day: dict = {}
CACH_KIEM = 3.0           # giây giữa hai lần kiểm "anh xong chưa" (kiểm thử đặt nhỏ)
GUI_THAT = True           # kiểm thử đặt False để không đẩy tin thật


def _zalo_dau() -> str:
    try:
        ids = [str(x).strip().split(":")[-1] for x in (json.loads(TEP_CH.read_text(encoding="utf-8")).get("zalo_ids") or []) if str(x).strip()]
        return ids[0] if ids else ""
    except (OSError, ValueError, AttributeError):
        return ""


def _ghi(noi_dung: str, ket_qua: str) -> None:
    try:
        with _lock:
            DIR.mkdir(parents=True, exist_ok=True)
            with open(TEP, "a", encoding="utf-8") as f:
                f.write(json.dumps({"luc": time.strftime("%Y-%m-%d %H:%M:%S"), "noi_dung": noi_dung[:300], "ket_qua": ket_qua[:80]}, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _main():
    for ten in ("main", "__main__"):
        m = sys.modules.get(ten)
        if m is not None and hasattr(m, "_notify_owner"):
            return m
    return None


async def _gui_async(m, noi_dung: str) -> list:
    kq = []
    ok, err = await m._notify_owner("", noi_dung, kind="system", label="TISA BOT cần anh", source="may", level="urgent", dedup="bao-anh:" + noi_dung[:60])
    kq.append("dashboard+chuông %s" % ("ok" if ok else "lỗi:" + str(err)[:30]))
    z = _zalo_dau()
    if z:
        ok2, err2 = await m._notify_owner("zalo:" + z, noi_dung, kind="system", label="TISA BOT cần anh", source="may", level="urgent", dedup="bao-anh-zalo:" + noi_dung[:60])
        kq.append("zalo %s" % ("ok" if ok2 else "lỗi:" + str(err2)[:30]))
    return kq


def bao(noi_dung: str, loop=None) -> dict:
    """Gửi một tin ngắn tới anh. Gọi được từ luồng nền (cần `loop` = vòng lặp của máy chủ) hoặc từ chính luồng async của máy chủ (loop=None)."""
    noi_dung = str(noi_dung or "").strip()[:300]
    if not noi_dung:
        return {"ok": False, "ly_do": "trống"}
    now = time.time()
    with _lock:
        if now - _gan_day.get(noi_dung, 0) < NHAC_LAI:
            return {"ok": True, "trung": True}
        _gan_day[noi_dung] = now
    kq = ["chỉ ghi nhật ký"]
    m = _main() if GUI_THAT else None
    if m is not None:
        try:
            if loop is not None:
                kq = asyncio.run_coroutine_threadsafe(_gui_async(m, noi_dung), loop).result(25)
            else:
                lp = asyncio.get_event_loop()
                lp.create_task(_gui_async(m, noi_dung))
                kq = ["đã xếp hàng gửi"]
        except Exception as e:  # noqa: BLE001
            kq = ["lỗi gửi: " + type(e).__name__]
    _ghi(noi_dung, "; ".join(kq))
    return {"ok": True, "kenh": kq}


def cho_nguoi_that(het_chan, ly_do: str, phut: int = 15, loop=None, dung=None, xong=None, bao_fn=None) -> str:
    """Chặn (ở luồng nền) tới khi het_chan() True. Trả "XONG" | "ANH_BAO_XONG" | "DA_DUNG" | "HET_GIO". `bao_fn` thay `bao` khi kiểm thử."""
    gui = bao_fn or (lambda t: bao(t, loop))
    gui("TISA BOT đang chờ anh: %s. Anh làm giúp em rồi em tự làm tiếp." % ly_do)
    t0 = last = time.time()
    while time.time() - t0 < max(0.01, phut) * 60:
        if dung and dung():
            return "DA_DUNG"
        if xong and xong():
            return "ANH_BAO_XONG"
        try:
            if het_chan():
                return "XONG"
        except Exception:  # noqa: BLE001
            pass
        if time.time() - last >= NHAC_LAI:
            last = time.time()
            gui("Em vẫn đang chờ anh: %s." % ly_do)
        time.sleep(CACH_KIEM)
    return "HET_GIO"
