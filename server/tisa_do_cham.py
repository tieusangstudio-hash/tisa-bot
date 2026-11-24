"""tisa_do_cham.py - Giữ máy chủ mượt trên máy học viên và để lại dấu vết khi nó bị đứng (Bộ TISA V3.53, 24/11/2026).

Gốc: học viên báo "làm việc cả sáng tốc độ rất yếu, báo chưa tải được tin mới nhất" mà máy chủ của anh Sang chạy cùng mã vẫn nhanh, nên
không biết chỗ nào chặn. Hai việc, đều nhẹ, tắt bằng TISA_DO_CHAM=0:

1. Canh vòng lặp của máy chủ. Một luồng riêng nhìn nhịp tim của vòng lặp (cập nhật mỗi 0,5 giây). Nhịp đứng quá NGUONG_CHAN giây nghĩa là có
   hàm đồng bộ nào đó đang chiếm vòng lặp: mọi yêu cầu khác phải chờ, đúng cảnh "chưa tải được". Luồng canh ghi vào `tisa_cham.log` đúng
   dòng mã đang chạy lúc đó (ngăn xếp luồng chính), nên lần sau học viên gửi file này là biết thủ phạm, không phải đoán. File tự giữ dưới ~1 MB.
2. Tự cắt `tisa.log`. Nhật ký này ghi mỗi yêu cầu và không bao giờ tự cắt (132 MB trên máy anh Sang sau 2 ngày). Quá TRAN_LOG thì giữ lại
   phần đuôi gần nhất, vứt phần cũ. Kiểm lúc khởi động và mỗi 30 phút. Không đụng gì khác.

Không ghi gì ra ngoài máy, không gọi mạng, lỗi nào cũng nuốt (không bao giờ làm hỏng máy chủ).
"""
from __future__ import annotations

import asyncio
import os
import sys
import threading
import time
import traceback
from pathlib import Path

from config import STATE_DIR

NGUONG_CHAN = float(os.getenv("TISA_NGUONG_CHAN") or 2.5)          # giây: vòng lặp đứng quá mức này thì ghi dấu
TRAN_LOG = int(float(os.getenv("TISA_LOG_TRAN_MB") or 60) * 1024 * 1024)   # tisa.log quá cỡ này thì cắt
GIU_LAI = 4 * 1024 * 1024                                          # phần đuôi giữ lại khi cắt
TRAN_CHAM = 1_000_000                                              # tisa_cham.log quá cỡ này thì giữ nửa đuôi
NHAC_LAI = 5.0                                                     # đứng kéo dài: ghi thêm một lần mỗi chừng này giây

FILE_CHAM = STATE_DIR / "tisa_cham.log"
FILE_LOG = STATE_DIR / "tisa.log"

_nhip = [time.monotonic()]
_luong_chinh = [0]
_da_bat = [False]


def _ghi_cham(text: str) -> None:
    try:
        FILE_CHAM.parent.mkdir(parents=True, exist_ok=True)
        if FILE_CHAM.exists() and FILE_CHAM.stat().st_size > TRAN_CHAM:
            data = FILE_CHAM.read_bytes()[-TRAN_CHAM // 2:]
            FILE_CHAM.write_bytes(data[data.find(b"\n") + 1:])
        with FILE_CHAM.open("a", encoding="utf-8") as f:
            f.write(text)
    except Exception:  # noqa: BLE001
        pass


def _dong_ma(frame, toi_da: int = 14) -> str:
    """Ngăn xếp của luồng chính, dòng mới nhất cuối cùng, bỏ khung của thư viện asyncio cho gọn."""
    try:
        ds = traceback.extract_stack(frame)
        ds = [x for x in ds if "asyncio" not in x.filename.replace("\\", "/").split("/")[-2:-1]][-toi_da:]
        return "".join("    %s:%d %s: %s\n" % (Path(x.filename).name, x.lineno, x.name, (x.line or "").strip()[:140]) for x in ds)
    except Exception:  # noqa: BLE001
        return "    (không đọc được ngăn xếp)\n"


def canh_vong_lap() -> None:
    """Chạy trong luồng riêng, mãi mãi."""
    dang_chan, bao_lan_cuoi, bat_dau = False, 0.0, 0.0
    while True:
        time.sleep(0.5)
        try:
            now = time.monotonic()
            tre = now - _nhip[0]
            if tre >= NGUONG_CHAN:
                if not dang_chan:
                    dang_chan, bat_dau, bao_lan_cuoi = True, _nhip[0], 0.0
                if now - bao_lan_cuoi >= NHAC_LAI:
                    bao_lan_cuoi = now
                    fr = sys._current_frames().get(_luong_chinh[0])
                    _ghi_cham("[%s] máy chủ đứng %.1f giây, đang chạy:\n%s\n" % (
                        time.strftime("%Y-%m-%d %H:%M:%S"), tre, _dong_ma(fr) if fr is not None else "    (không thấy luồng chính)\n"))
            elif dang_chan:
                dang_chan = False
                _ghi_cham("[%s] máy chủ chạy lại sau khoảng %.1f giây\n\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), time.monotonic() - bat_dau))
        except Exception:  # noqa: BLE001
            pass


async def _nhip_tim() -> None:
    while True:
        _nhip[0] = time.monotonic()
        await asyncio.sleep(0.5)


def cat_log(path: Path = None, tran: int = None, giu: int = None) -> bool:
    """Quá `tran` byte thì giữ lại `giu` byte cuối (từ đầu dòng nguyên). Trả True nếu đã cắt. Ghi tại chỗ để tiến trình đang ghi nhật ký
    (launchd, .bat) vẫn ghi tiếp vào cùng tệp."""
    p = Path(path or FILE_LOG)
    tran = TRAN_LOG if tran is None else tran
    giu = GIU_LAI if giu is None else giu
    try:
        size = p.stat().st_size
        if size <= tran:
            return False
        with p.open("rb") as f:
            f.seek(max(0, size - giu))
            data = f.read()
        data = data[data.find(b"\n") + 1:]
        with p.open("r+b") as f:
            f.write(data)
            f.truncate(len(data))
        return True
    except Exception:  # noqa: BLE001
        return False


def _vong_cat_log() -> None:
    while True:
        try:
            if cat_log():
                _ghi_cham("[%s] tisa.log quá %d MB, đã giữ lại phần mới nhất\n\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), TRAN_LOG // (1024 * 1024)))
        except Exception:  # noqa: BLE001
            pass
        time.sleep(1800)


def gan(app) -> None:
    if os.getenv("TISA_DO_CHAM") == "0":
        return

    @app.on_event("startup")
    async def _bat_do_cham():
        if _da_bat[0]:
            return
        _da_bat[0] = True
        _luong_chinh[0] = threading.get_ident()
        _nhip[0] = time.monotonic()
        asyncio.get_running_loop().create_task(_nhip_tim())
        threading.Thread(target=canh_vong_lap, name="tisa-canh-vong-lap", daemon=True).start()
        threading.Thread(target=_vong_cat_log, name="tisa-cat-log", daemon=True).start()
