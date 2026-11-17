"""Nói xong là phải LÀM THẬT (chủ báo 15/11/2026).

Bộ não giọng là model nhỏ, không có công cụ. Nó hay trả lời kiểu "Ừ, để mình kiểm tra nhé" mà quên
viết dòng TISA_ASK_MAIN, nên lượt kết thúc ở câu nói: không ai đi làm cả. Hai hàm ở đây là LƯỚI Ở
MÁY CHỦ, không dựa vào việc model nhớ viết dòng lệnh:

  nen_giao_viec(user, reply): câu trả lời vừa HỨA làm (không có kèm dòng lệnh), hoặc người dùng vừa RA LỆNH
                              làm / hỏi số liệu mà câu trả lời không phải câu hỏi lại.
  yeu_cau(user):              yêu cầu đầy đủ, tự đứng được, giao cho bộ não chính chạy thật.
"""
from __future__ import annotations

import re

_DONG_TU = (r"xem|kiểm tra|check|làm|tìm|lấy|chạy|tra|soạn|viết|tạo|gửi|đọc|lên|dựng|phân tích|"
            r"tổng hợp|rà soát|rà|lục|thống kê|tải|cập nhật|đăng|đặt|nhắc|kéo|quét|sửa|thêm|xuất")

# Câu trả lời hứa làm: "để mình kiểm tra", "em sẽ làm", "đang xem", "làm ngay".
_HUA = re.compile(
    r"(?:để|cho|xin)\s+(?:mình|em|tôi|tui)\s+(?:" + _DONG_TU + r")"
    r"|(?:mình|em|tôi|tui)\s+(?:sẽ|đang|xin|làm)\s+(?:" + _DONG_TU + r")"
    r"|(?:" + _DONG_TU + r")\s+(?:ngay|liền|luôn)\b"
    r"|đang\s+(?:" + _DONG_TU + r")",
    re.I)

# Người dùng RA LỆNH hoặc hỏi dữ liệu sống.
_LENH = re.compile(
    r"\b(?:đấu nối|kết nối|liên kết|nối|cài đặt|thiết lập|cấu hình|kiểm tra|check|xem (?:giúp|giùm|lại|cho)|làm (?:giúp|giùm|cho|đi|ngay)|tạo|viết|soạn|gửi|chạy|dựng|"
    r"đăng|lấy (?:số|dữ liệu)|báo cáo|thống kê|tổng hợp|phân tích|tìm|tra cứu|nhắc anh|đặt lịch|lên (?:kế hoạch|bài|camp|chiến dịch)|"
    r"cập nhật|kéo số|quét|xuất|liệt kê|cho anh (?:xem|biết)|(?:chi|tiêu) bao nhiêu|bao nhiêu (?:tiền|đơn|lead|inbox|khách)|"
    r"triển khai|thiết kế|thực hiện|tiến hành|bắt đầu (?:đi|làm|ngay|luôn)|tiếp tục (?:đi|làm|nhé|luôn)|làm luôn|làm tiếp|xử lý|duyệt|lên đi)\b",
    re.I)

_HOI_LAI = re.compile(r"\b(?:chưa|không|hả|nhỉ|chứ)\s*[?.!]*$|\?\s*$", re.I)
_TU_CHOI = re.compile(r"\b(?:đừng|không cần|thôi|khoan|dừng|hủy|huỷ)\b", re.I)


def _dong_dau_cau(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def nen_giao_viec(user: str, reply: str) -> bool:
    r = _dong_dau_cau(reply)
    u = _dong_dau_cau(user)
    if not r or not u:
        return False
    if _TU_CHOI.search(u[:200]) and not _LENH.search(u):
        return False
    if _HUA.search(r):
        return True
    if len(u.split()) >= 4 and _LENH.search(u) and not r.endswith("?"):
        return True
    return False


def yeu_cau(user: str) -> str:
    u = _dong_dau_cau(user)[:1800]
    return ("Anh vừa nói bằng giọng: \"" + u + "\". Làm thật ngay bằng công cụ và dữ liệu có sẵn "
            "(không chỉ trả lời bằng lời), rồi báo kết quả cụ thể: đã làm gì, số liệu hoặc tệp ở đâu, "
            "còn thiếu gì cần anh. Việc đăng bài, chạy quảng cáo, gửi tin, tiêu tiền thì chuẩn bị xong và hỏi anh duyệt trước.")


NHAC_PROMPT = (
    "QUY TẮC CỨNG: người dùng RA LỆNH làm gì (kiểm tra, xem số liệu, tạo, viết, gửi, chạy, dựng, tìm, báo cáo...) "
    "hoặc hỏi một con số thật thì BẮT BUỘC giao ngay bằng dòng " + "TISA_ASK_MAIN: ... " +
    "ngay trong lượt này, KHÔNG hỏi lại 'anh muốn em làm luôn không'. Cấm nói 'để em kiểm tra', 'em xem ngay', "
    "'em làm đây' mà không kèm dòng lệnh đó: nói xong mà không giao là lời hứa suông, người dùng sẽ ngồi chờ một việc không ai làm.\n"
)


def la_lenh(user: str) -> bool:
    """Câu nói LÀ LỆNH làm việc (không phải chỉ hỏi tiến độ, đồng ý chờ hay từ chối)."""
    u = _dong_dau_cau(user)
    if not u or (_TU_CHOI.search(u[:200]) and not _LENH.search(u)):
        return False
    if _HOI_LAI.search(u):      # "xong chưa", "làm được không": câu hỏi, không phải lệnh
        return False
    return bool(_LENH.search(u))
