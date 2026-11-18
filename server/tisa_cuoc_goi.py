"""tisa_cuoc_goi.py - Cuộc gọi giọng nói bớt phiền (V3.12, chủ 18/11/2026).

Ba lỗi chủ báo khi đang nói chuyện bằng mic:
  1. Việc nền giao từ 4-5 ô chat trước xong giữa lúc anh nói chuyện khác: bot chen vào đọc kết quả, không nói rõ là việc nào.
  2. Bot đọc dài, lan man, anh nói "em ơi" hay chen vào mà nó vẫn đọc cho hết.
  3. Không có cách dừng bot đang nói ngoài việc cúp máy.

Mô-đun này chỉ chứa phần LUẬT, thuần chữ, không đụng mạng, để thử được:
  la_lenh_dung(text)           câu anh nói có phải lệnh "dừng nói" không ("em ơi dừng lại", "thôi", "đủ rồi", "stop"...). Chỉ nhận câu NGẮN
                               gồm đúng các từ dừng; câu dài như "thôi anh hỏi cái khác" KHÔNG tính (không bắt bot im nhầm).
  ten_viec(yeu_cau)            tên ngắn của việc để nói ra ("việc: viết kịch bản video").
  loi_bao_viec_cu(ten, kq)     câu bot nói khi việc cũ xong lúc anh đang bàn chuyện khác: nêu rõ việc nào, rút gọn, chi tiết ở khung chat.
Phần nối vào máy chủ và trình duyệt do build.py vá (voice_live.py, main.py, voice-live.js, call-bar.js).
"""
from __future__ import annotations

import re
import unicodedata

_DEM_TU_TOI_DA = 5
_DEM = {"em", "oi", "a", "alo", "nay", "da", "vang", "nha", "nhe", "ne", "ha", "anh", "bot", "tisa", "bo", "oi"}
_LENH = [
    re.compile(r"^(dung|ngung|tam dung)( (lai|noi|doc|nua|roi|di))*$"),
    re.compile(r"^(im|im lang|im di|im roi|im di nha)$"),
    re.compile(r"^thoi( (roi|di|dung|dung noi|dung doc|du roi|khong noi|khong doc|khong can noi|khong can doc))?( nua)?$"),
    re.compile(r"^(du roi|du roi nha|khong can (noi|doc) nua|khong (noi|doc) nua|dung (noi|doc) nua)$"),
    re.compile(r"^(khoan|khoan da|stop|stop it|stop talking|be quiet|shut up|enough)$"),
]


def _chuan(text: str) -> str:
    s = unicodedata.normalize("NFD", str(text or "").lower().replace("đ", "d"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def la_lenh_dung(text) -> bool:
    s = _chuan(text)
    if not s:
        return False
    tu = s.split(" ")
    while tu and tu[0] in _DEM:
        tu.pop(0)
    while tu and tu[-1] in _DEM:
        tu.pop()
    if not tu or len(tu) > _DEM_TU_TOI_DA:
        return False
    return any(r.match(" ".join(tu)) for r in _LENH)


def ten_viec(yeu_cau, gioi_han: int = 70) -> str:
    t = re.sub(r"\s+", " ", str(yeu_cau or "")).strip().strip("\"'")
    if not t:
        return "việc anh giao trước đó"
    if len(t) > gioi_han:
        t = t[:gioi_han].rsplit(" ", 1)[0] + "..."
    return t


def loi_bao_viec_cu(ten: str, tom_tat: str) -> str:
    """Câu để bot đọc. `tom_tat` đã được rút gọn bên gọi (speakable). Không lặp lại cả kết quả dài: chi tiết nằm ở khung chat."""
    ten = ten_viec(ten)
    tom_tat = str(tom_tat or "").strip()
    if not tom_tat:
        return "Em báo anh, việc \"%s\" em làm xong rồi ạ, chi tiết em để ở khung chat." % ten
    return "Em báo anh việc trước đó nhé, việc \"%s\" đã xong. %s Chi tiết em để ở khung chat, anh xem sau cũng được ạ." % (ten, tom_tat)
