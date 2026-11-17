"""Cho công cụ trả ẢNH thẳng cho AI nhìn (chủ yêu cầu 17/11/2026: AI điều khiển máy trên Windows không xem được màn hình).

Lỗi gốc: tisa_desktop_look và tisa_browser_look chỉ trả đường dẫn tệp ảnh và dặn AI "đọc bằng công cụ đọc tệp". Công cụ đọc của TISA BOT
chỉ mở được tệp trong kho brain, còn engine ChatGPT/Codex đọc tệp ảnh ra chữ vô nghĩa, nên AI không thấy gì. Ở đây công cụ ghi một dòng
đánh dấu "⟦ANH:<đường dẫn>⟧" vào kết quả; hub (mcp_hub) gọi tach_anh() để gỡ dòng đó và đính ảnh thật vào kết quả theo chuẩn MCP
(content type=image), AI nhìn được ngay như chụp ảnh bằng mắt.

Chỉ nhận ảnh nằm trong thư mục trạng thái của TISA BOT (dieu-khien-may/anh, trinh-duyet/anh...), tối đa 3 ảnh, tối đa ~1.6 MB mỗi ảnh.
"""
from __future__ import annotations

import base64
import io
import os
import re
from pathlib import Path

DAU = "⟦ANH:"
_RE = re.compile(r"\n?⟦ANH:([^⟧\n]+)⟧")
TOI_DA_ANH = 3
TOI_DA_BYTE = 1_600_000


def _goc() -> Path:
    try:
        import config as _cfg
        return Path(_cfg.STATE_DIR).resolve()
    except Exception:  # noqa: BLE001
        return Path(os.getenv("TISA_STATE_DIR") or Path(__file__).resolve().parent).resolve()


def _doc(p: Path):
    raw = p.read_bytes()
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    if len(raw) <= TOI_DA_BYTE:
        return mime, raw
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        for q in (70, 55, 40):
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=q)
            if buf.tell() <= TOI_DA_BYTE:
                return "image/jpeg", buf.getvalue()
        k = 0.7
        im = im.resize((max(1, int(im.size[0] * k)), max(1, int(im.size[1] * k))))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=55)
        return "image/jpeg", buf.getvalue()
    except Exception:  # noqa: BLE001
        return None


def tach_anh(ket_qua: str):
    """(chữ đã gỡ dòng đánh dấu, danh sách khối ảnh MCP). Không có đánh dấu thì trả nguyên chữ và danh sách rỗng."""
    text = str(ket_qua or "")
    if DAU not in text:
        return text, []
    goc = _goc()
    ra = []
    for m in _RE.finditer(text):
        if len(ra) >= TOI_DA_ANH:
            break
        try:
            p = Path(m.group(1).strip()).resolve()
            if goc not in p.parents or p.suffix.lower() not in (".jpg", ".jpeg", ".png") or not p.is_file():
                continue
            d = _doc(p)
            if d:
                ra.append({"type": "image", "data": base64.b64encode(d[1]).decode("ascii"), "mimeType": d[0]})
        except Exception:  # noqa: BLE001
            continue
    return _RE.sub("", text), ra
