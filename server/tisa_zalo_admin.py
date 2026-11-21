"""tisa_zalo_admin.py - Tự nhận ra Zalo admin (Kênh Admin) để gửi báo cáo định kỳ đúng người, đúng giờ (V3.41, chủ yêu cầu 21/11/2026).

Trước đây một lịch báo cáo (vd Đại Quảng Cáo báo lúc 23h) chỉ trả kết quả vào ô chat trên máy tính, hoặc cộng sự tự đi tìm "công cụ gửi Zalo"
và gửi nhầm bằng Zalo cá nhân. Nay:
  - Máy nhớ ai đã nhắn vào bot Zalo admin (chỉ các chat nằm trong "ID được phép") để biết Zalo admin ĐANG DÙNG là chat nào, mã gì.
  - Nơi nhận `zalo:admin` (hay `zalo_admin`) là địa chỉ ảo, được đổi thành mã thật ngay lúc GỬI, nên đổi người hay đổi mã cũng không phải sửa lịch.
  - Lịch đặt từ chính khung chat Zalo admin thì tự nhận khung chat đó làm nơi nhận.
  - Tin dài được chia thành nhiều tin (Zalo giới hạn khoảng 2000 ký tự một tin) thay vì cắt cụt.
Không dùng ký tự em dash.
"""
from __future__ import annotations

import json
import os
import re
import threading
import time
from pathlib import Path

ALIAS = ("admin", "zalo_admin", "kenh_admin", "zalo-admin", "kenh-admin")
CHUNK = 1800
TOI_DA_TIN = 6
_khoa = threading.RLock()


def la_dia_chi_admin(raw) -> bool:
    """`zalo:admin`, `zalo_admin`, `admin`... (không phân biệt hoa thường, bỏ tiền tố zalo:)."""
    s = str(raw or "").strip().lower()
    if s.startswith("zalo:"):
        s = s[5:]
    return s in ALIAS


def chuan_dia_chi(raw) -> str:
    """Địa chỉ ảo về một dạng duy nhất `zalo:admin`; mã thật và giá trị khác giữ nguyên."""
    return "zalo:admin" if la_dia_chi_admin(raw) else str(raw or "").strip()


def _thu_muc() -> Path:
    try:
        import config as _cfg
        d = Path(_cfg.STATE_DIR)
    except Exception:  # noqa: BLE001
        d = Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent)
    d.mkdir(parents=True, exist_ok=True)
    return d


def _tep() -> Path:
    return _thu_muc() / "zalo-admin.json"


def _doc() -> dict:
    try:
        d = json.loads(_tep().read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def _cai_dat() -> dict:
    try:
        import config as cfgmod
        return (cfgmod.read_settings() or {}).get("zalo_bot") or {}
    except Exception:  # noqa: BLE001
        return {}


def ds_duoc_phep(cai_dat: dict | None = None) -> list:
    """Các chat_id trong ô "ID được phép" của Kênh Admin Zalo (cách nhau bằng dấu phẩy, khoảng trắng hay xuống dòng)."""
    z = cai_dat if cai_dat is not None else _cai_dat()
    return [x for x in re.split(r"[\s,;]+", str(z.get("chat_id") or "")) if x]


def ghi_thay(chat_id: str) -> None:
    """Gọi khi một chat ĐƯỢC PHÉP nhắn vào bot: nhớ mốc gần nhất. Không bao giờ ném lỗi (không làm hỏng lượt trả lời)."""
    try:
        cid = str(chat_id or "").strip()
        if not cid:
            return
        with _khoa:
            d = _doc()
            thay = d.get("thay") if isinstance(d.get("thay"), dict) else {}
            thay[cid] = time.time()
            d["thay"] = thay
            t = _tep().with_suffix(".tmp")
            t.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            os.replace(t, _tep())
    except Exception:  # noqa: BLE001
        pass


def nguoi_nhan(cai_dat: dict | None = None, thay: dict | None = None) -> list:
    """Mã Zalo admin sẽ nhận báo cáo. Thứ tự tin cậy:
      1. `owner_chat_id` chủ đã chỉ định (nếu còn nằm trong danh sách được phép);
      2. chat ĐƯỢC PHÉP đã nhắn vào bot gần đây nhất (đang dùng thật);
      3. chỉ có một ID được phép thì là ID đó;
      4. còn lại: mọi ID được phép (đây đều là admin do chủ tự khai).
    Trả danh sách rỗng khi chưa khai ID nào."""
    z = cai_dat if cai_dat is not None else _cai_dat()
    ids = ds_duoc_phep(z)
    if not ids:
        return []
    own = str(z.get("owner_chat_id") or "").strip()
    if own and own in ids:
        return [own]
    if thay is None:
        thay = _doc().get("thay") or {}
    da_thay = [(float(thay.get(i) or 0), i) for i in ids if thay.get(i)]
    if da_thay:
        return [max(da_thay)[1]]
    if len(ids) == 1:
        return ids
    return ids


def tach_tin(text: str, chunk: int = CHUNK, toi_da: int = TOI_DA_TIN) -> list:
    """Chia tin dài thành nhiều tin <= chunk ký tự, ưu tiên cắt ở xuống dòng rồi dấu cách; đánh số (1/n). Quá `toi_da` tin thì nói rõ đã gộp."""
    t = str(text or "").strip()
    if len(t) <= chunk:
        return [t] if t else []
    out, cur = [], t
    while cur and len(out) < toi_da:
        if len(cur) <= chunk:
            out.append(cur)
            cur = ""
            break
        cat = cur.rfind("\n", 0, chunk)
        if cat < chunk // 2:
            cat = cur.rfind(" ", 0, chunk)
        if cat < chunk // 2:
            cat = chunk
        out.append(cur[:cat].rstrip())
        cur = cur[cat:].lstrip()
    if cur:
        out[-1] = out[-1][:chunk - 90].rstrip() + "\n... (còn nữa, xem đầy đủ ở TISA BOT)"
    n = len(out)
    return [f"({i + 1}/{n}) {x}" for i, x in enumerate(out)] if n > 1 else out


def mo_ta() -> dict:
    """Để hiển thị / kiểm tra: ai được phép, ai đang dùng, báo cáo sẽ gửi cho ai."""
    z = _cai_dat()
    thay = _doc().get("thay") or {}
    return {"duoc_phep": ds_duoc_phep(z), "da_thay": thay, "nguoi_nhan": nguoi_nhan(z, thay), "owner_chat_id": str(z.get("owner_chat_id") or "")}
