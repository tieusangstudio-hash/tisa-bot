"""tisa_anh_ngoai.py - Cho khung chat (kể cả trên điện thoại, qua tên miền) XEM ẢNH CHỤP MÀN HÌNH mà TISA BOT lưu ở thư mục trạng thái (chủ báo 19/11/2026).

Lỗi gốc: ảnh chụp màn hình do tisa_desktop_look / tisa_browser_look lưu ở <thư mục trạng thái>/dieu-khien-may/anh và trinh-duyet/anh, NGOÀI kho brain.
Khung chat dựng link /files/raw?brain=...&path=Users/.../anh/xxx.jpg cho ảnh đó, nhưng /files/raw chỉ phục vụ tệp trong kho brain nên trả 404: trên máy tính thì
còn "bấm mở bằng ứng dụng", còn trên điện thoại (không cùng máy) ảnh chỉ hiện "ảnh hết hạn".

Cách sửa hẹp: /files/raw hỏi hàm tim(path) trước. CHỈ phục vụ tệp ảnh (jpg, png, webp, gif) nằm đúng trong các thư mục ảnh chụp của TISA BOT; mọi đường dẫn khác
trả None để luật cũ chạy như trước. Vẫn đòi đăng nhập như mọi đường /files/*, không đi qua thư mục cha, không theo liên kết ra ngoài.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

THU_MUC_ANH = ("dieu-khien-may/anh", "trinh-duyet/anh")
DUOI = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def _goc() -> Path:
    try:
        import config as _cfg
        return Path(_cfg.STATE_DIR).resolve()
    except Exception:  # noqa: BLE001
        return Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent).resolve()


def _cac_thu_muc() -> list:
    g = _goc()
    return [(g / d).resolve() for d in THU_MUC_ANH]


def tim(path) -> "Path | None":
    """Trả Path tệp ảnh chụp màn hình nếu `path` trỏ đúng vào đó, ngược lại None. `path` có thể là đường dẫn đầy đủ (có hoặc mất dấu / đầu) hoặc chỉ tên tệp."""
    p = str(path or "").replace("\\", "/").strip()
    if not p or "\x00" in p or len(p) > 600:
        return None
    if Path(p.lstrip("/")).suffix.lower() not in DUOI:
        return None
    dirs = _cac_thu_muc()
    if "/" not in p:                                   # chỉ có tên tệp: thử từng thư mục ảnh chụp
        ung = [d / p for d in dirs]
    elif re.match(r"^[A-Za-z]:/", p):                  # Windows: C:/Users/...
        ung = [Path(p)]
    else:                                              # macOS, Linux: khung chat bỏ dấu / đầu
        ung = [Path("/" + p.lstrip("/"))]
    for c in ung:
        try:
            r = c.resolve()
        except (OSError, RuntimeError):
            continue
        if any(d in r.parents for d in dirs) and r.is_file() and r.suffix.lower() in DUOI:
            return r
    return None
