"""Anh bảo DỪNG hoặc ĐỔI VIỆC giữa chừng thì việc cũ phải dừng thật (chủ báo 17/11/2026).

Lỗi gốc: nói "dừng lại đi, đấu nối MCP trước" trong lúc việc nền đang chạy, câu đó bị coi là một việc MỚI chạy SONG SONG
(voice_live.parallel_request còn dặn bộ não "đừng ghi đè việc đang chạy"), nên việc cũ (đăng bài, tạo quảng cáo) vẫn chạy
tiếp và còn tranh trình duyệt với việc mới. Ở đây là luật CỨNG ở máy chủ, không dựa vào việc model nói nhớ:

  la_doi_y(text)       câu nói có phải lệnh dừng hoặc đổi việc không.
  co_viec_moi(text)    ngoài lệnh dừng còn có việc mới để làm không ("dừng đi" thì không, "dừng đi, đấu nối MCP" thì có).
  ghi_chu_doi_y(...)   dòng dặn bộ não: việc cũ đã BỊ DỪNG, chỉ làm việc anh vừa nói.
"""
from __future__ import annotations

import re
import unicodedata

_THUONG = "[^\\W\\d_]"


def _chuan(text: str) -> str:
    s = unicodedata.normalize("NFC", str(text or "")).lower()
    return re.sub(r"\s+", " ", s).strip()


# Cụm dừng rõ ràng. Cố ý HẸP: nhận nhầm một câu thường thành lệnh dừng là giết mất việc đang làm tốt.
_DUNG = re.compile("|".join((
    r"(?<!\w)(?:dừng|ngừng|ngưng|tạm dừng|tạm ngưng|tạm ngừng)(?!\w)",
    r"(?<!\w)(?:hủy|huỷ|bỏ|bỏ qua|thôi)\s+(?:cái\s+)?(?:việc|đó|này|nó|lệnh|bước|đi|luôn|hết)(?!\w)",
    r"^(?:thôi|khoan)(?:\s+(?:đã|đi|nào|dừng|đừng|làm|cái|chuyện|việc))(?!\w)",
    r"(?<!\w)đừng\s+(?:làm|đăng|tạo|gửi|chạy|bấm|tiếp|mở|vào|chọn|bài|viết)(?!\w)",
    r"(?<!\w)không\s+(?:cần\s+)?(?:làm|đăng|tạo|gửi|chạy)\s+(?:nữa|cái đó|cái này|vậy|thế)(?!\w)",
    r"(?<!\w)(?:đổi ý|thay đổi ý định|làm cái khác|làm việc khác)(?!\w)",
    r"(?<!\w)(?:chuyển|đổi)\s+(?:qua|sang)\s+(?:việc|cái|làm|đấu|nối|kết)",
    r"(?<!\w)(?:trước đã|trước tiên|làm trước|nối trước|đấu nối trước|kết nối trước)(?!\w)",
    r"(?<!\w)(?:stop|cancel|abort|halt)(?!\w)",
)))

# Có "dừng" nhưng KHÔNG phải ra lệnh dừng việc: hỏi, kể, dặn sau này.
_KHONG_PHAI = re.compile("|".join((
    r"\?\s*$",
    r"(?<!\w)(?:có dừng|dừng chưa|dừng chưa|dừng được không|sao dừng|vì sao|tại sao|tại sao lại)(?!\w)",
    r"(?<!\w)(?:đừng quên|đừng có quên|nhớ đừng|đừng lo|đừng ngại)(?!\w)",
    r"(?<!\w)(?:thôi được rồi|thôi ok|thôi cảm ơn|thôi cám ơn)(?!\w)",
    r"(?<!\w)(?:dừng xe|dừng chân|dừng đèn đỏ)(?!\w)",
)))

# Động từ ra việc mới.
_VIEC_MOI = re.compile(
    r"(?<!\w)(?:đấu nối|nối|kết nối|liên kết|cài đặt|cài|thiết lập|cấu hình|làm|tạo|viết|soạn|kiểm tra|xem|tìm|chạy|gửi|mở|vào|"
    r"báo cáo|thống kê|phân tích|thiết kế|dựng|lên|đăng|cập nhật|sửa|thêm|xuất|tải|lấy|tổng hợp|check|connect|setup|install)(?!\w)")

# Từ đệm không mang việc.
_DEM = frozenset("""lại đi nhé nha nhá nghen đã em anh chị ơi à ạ vậy thế rồi thì là cái việc đó này nó luôn hết với cho mình
dạ vâng ừ ờ ok oke được thôi khoan đừng không nữa tiếp bước""".split())


def la_doi_y(text: str) -> bool:
    """Câu này là lệnh DỪNG hoặc ĐỔI việc đang làm."""
    s = _chuan(text)
    if not s or len(s) > 400:
        return False
    if _KHONG_PHAI.search(s):
        return False
    return bool(_DUNG.search(s))


def co_viec_moi(text: str) -> bool:
    """Ngoài lệnh dừng còn có việc mới để làm. "dừng lại đi" thì không; "dừng lại đi, đấu nối MCP trước" thì có."""
    s = _chuan(text)
    if not s:
        return False
    con_lai = _DUNG.sub(" ", s)
    tu = [w for w in re.findall(r"[^\W_]+", con_lai) if w not in _DEM]
    if not tu:
        return False
    return bool(_VIEC_MOI.search(con_lai)) and len(tu) >= 2


def ghi_chu_doi_y(viec_cu, yeu_cau_moi: str = "") -> str:
    """Dòng gắn vào yêu cầu gửi bộ não chính sau khi việc cũ đã bị dừng."""
    cu = "; ".join('"' + str(r).strip()[:140] + '"' for r in (viec_cu or []) if str(r or "").strip())
    return ("[ANH VỪA ĐỔI Ý GIỮA CHỪNG] Việc đang làm dở " + (cu or "trước đó") + " ĐÃ BỊ DỪNG theo lệnh của anh: "
            "KHÔNG làm tiếp, KHÔNG nhắc lại, KHÔNG bấm thêm gì ở trang đang mở trừ khi việc mới cần. "
            "Chỉ làm đúng việc anh vừa nói dưới đây, bắt đầu từ đầu việc đó (nếu trình duyệt đang dở một biểu mẫu của việc cũ "
            "thì đóng hoặc hủy biểu mẫu đó, không gửi đi). Nói thật việc cũ đã dừng ở đâu nếu cần.]\n\n")
