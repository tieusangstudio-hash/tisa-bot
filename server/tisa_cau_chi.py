"""tisa_cau_chi.py - Cầu chì giới hạn số bước mỗi giờ của MỘT phiên (V3.42, chủ yêu cầu 21/11/2026).

Sự cố 17/11/2026: một phiên ChatGPT (Codex) chạy 16.203 lượt trong đúng 1 giờ, đọc vào 65 triệu token. Một vòng lặp như vậy ăn hết điểm
của người dùng mà không ai hay biết. Cầu chì này đếm số bước (tool_call / progress) của từng phiên trong 60 phút trượt; vượt ngưỡng thì
dừng lượt đang chạy và báo rõ, rồi đặt lại bộ đếm để người dùng nhắn tiếp được ngay (vòng lặp tự chạy lại thì bị cắt tiếp ở ngưỡng kế).

Ngưỡng mặc định 4000 sự kiện mỗi giờ mỗi phiên (một bước Codex báo hai sự kiện: bắt đầu và xong). Số thật hiếm thấy: chat dài nhất của
chủ cũng chỉ vài trăm bước mỗi lượt. Đổi bằng biến môi trường TISA_CAU_CHI_LUOT hoặc settings `cau_chi.luot_moi_gio`; 0 = tắt.
Không bao giờ ném lỗi ra ngoài (một cái đồng hồ đo không được làm hỏng lượt chat). Không dùng ký tự em dash.
"""
from __future__ import annotations

import collections
import functools
import os
import sys
import threading
import time

MAC_DINH = 4000
CUA_SO_S = 3600.0
SU_KIEN = ("tool_call", "progress")
_khoa = threading.Lock()
_cua_so: dict = {}


def gioi_han() -> int:
    """Số sự kiện tối đa mỗi giờ cho một phiên; 0 hoặc âm = tắt cầu chì."""
    v = os.environ.get("TISA_CAU_CHI_LUOT")
    if v is None:
        try:
            import config as cfgmod
            v = ((cfgmod.read_settings() or {}).get("cau_chi") or {}).get("luot_moi_gio")
        except Exception:  # noqa: BLE001
            v = None
    try:
        return int(v) if v not in (None, "") else MAC_DINH
    except (TypeError, ValueError):
        return MAC_DINH


def them(khoa: str, now: float | None = None, cua_so: float = CUA_SO_S) -> int:
    """Ghi một sự kiện cho phiên `khoa`, trả số sự kiện trong cửa sổ (đã tính sự kiện này)."""
    now = time.monotonic() if now is None else now
    with _khoa:
        q = _cua_so.setdefault(khoa, collections.deque())
        q.append(now)
        han = now - cua_so
        while q and q[0] < han:
            q.popleft()
        if len(_cua_so) > 2000:       # phiên cũ không còn hoạt động: dọn bớt, khỏi phình bộ nhớ
            for k in [k for k, v in _cua_so.items() if not v or v[-1] < han][:500]:
                _cua_so.pop(k, None)
        return len(q)


def dat_lai(khoa: str) -> None:
    with _khoa:
        _cua_so.pop(khoa, None)


def khoa_phien(engine) -> str:
    tag = str(getattr(engine, "tag", "") or "")
    return "%s:%s" % (type(engine).__name__, tag) if tag else "%s:%s" % (type(engine).__name__, id(engine))


def cau_noi(so: int, han: int) -> str:
    return ("TISA BOT đã DỪNG lượt này vì phiên chạy %d bước trong 1 giờ (quá ngưỡng %d), nghi vòng lặp không dừng. "
            "Việc làm dở vẫn được giữ. Anh đọc lại kết quả rồi nhắn tiếp nếu muốn chạy tiếp." % (so, han))


def _boc(fn, ten_engine: str):
    @functools.wraps(fn)
    async def query(self, *args, **kwargs):
        agen = fn(self, *args, **kwargs)
        try:
            async for ev in agen:
                try:
                    if isinstance(ev, dict) and ev.get("type") in SU_KIEN:
                        han = gioi_han()
                        if han > 0:
                            k = khoa_phien(self)
                            so = them(k)
                            if so > han:
                                dat_lai(k)
                                print("[cầu chì] %s %s dừng: %d sự kiện trong 1 giờ (ngưỡng %d)" % (ten_engine, k, so, han), file=sys.stderr)
                                yield {"type": "error", "content": cau_noi(so, han)}
                                return
                except Exception:  # noqa: BLE001 - cái đo không được làm hỏng lượt
                    pass
                yield ev
        finally:
            try:
                await agen.aclose()
            except Exception:  # noqa: BLE001
                pass
    query._tisa_cau_chi = True
    return query


def cai_vao(cls, ten_engine: str = "") -> bool:
    """Gắn cầu chì vào cls.query một lần (an toàn khi gọi nhiều lần)."""
    f = getattr(cls, "query", None)
    if f is None or getattr(f, "_tisa_cau_chi", False):
        return False
    cls.query = _boc(f, ten_engine or cls.__name__)
    return True
