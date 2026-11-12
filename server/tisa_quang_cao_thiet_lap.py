"""tisa_quang_cao_thiet_lap.py - phần "Thiết lập quảng cáo" của trang Quảng Cáo (V2.78).

Làm được gì:
  - KHUNG: bộ khung thiết lập riêng cho từng nền tảng (Facebook, TikTok, Google): tên các cấp, mục tiêu, dạng chiến dịch, mẫu cấu
    trúc (1-1-1, 1-1-3, 1-3-3...), nút kêu gọi, đối tượng tuỳ chỉnh, các lựa chọn AI tự tối ưu có thể tắt. Trang đọc khung này nên
    chọn nền tảng nào thì chữ, lựa chọn và lời nhắc đổi theo nền tảng đó.
  - Gợi ý đối tượng (target) theo ngành: luật có sẵn, không gọi AI, trả ngay.
  - Tải lên hình, video (nhiều tệp), danh sách khách hàng; lưu trên máy chủ này.
  - Quét kết nối: API đã nhập và kết nối MCP quảng cáo trong TISA BOT, để trang tự cập nhật khi nối xong.
  - Phiếu thiết lập đời 2 và lời nhờ trợ lý tạo chiến dịch. TRANG KHÔNG TỰ TẠO / BẬT QUẢNG CÁO: lời nhờ luôn yêu cầu tạo ở trạng
    thái tạm dừng và chờ chủ duyệt.

Các tên nút, mục tiêu, dạng chiến dịch là cách gọi thông dụng trên từng nền tảng; giao diện của nền tảng đổi theo thời gian nên
trợ lý luôn được dặn đối chiếu với màn hình thật khi tạo.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import threading
import time
import unicodedata
from pathlib import Path

import tisa_quang_cao as Q

try:
    from fastapi import Request
except Exception:  # noqa: BLE001
    Request = None

TEP_NHAP = Q.KHO / "phieu-thiet-lap.json"
THU_MUC_TAI = Q.KHO / "tai-len"
TEP_TAI = Q.KHO / "tai-len.json"
_khoa = threading.RLock()

# ---------------------------------------------------------------- khung theo nền tảng
MAU_CAU_TRUC = [
    {"id": "1-1-1", "nhom": 1, "bai": 1, "ten": "1 chiến dịch, 1 nhóm, 1 bài", "hop": "Ngân sách nhỏ, mới bắt đầu. Dồn hết tiền vào một bài để dễ theo dõi.",
     "so_bai": 1},
    {"id": "1-1-3", "nhom": 1, "bai": 3, "ten": "1 chiến dịch, 1 nhóm, 3 bài", "hop": "Muốn thử xem bài nào hay hơn. Cùng một đối tượng, 3 bài khác nhau, nền tảng tự dồn tiền cho bài tốt.",
     "so_bai": 3},
    {"id": "1-3-1", "nhom": 3, "bai": 1, "chung": True, "ten": "1 chiến dịch, 3 nhóm, cùng 1 bài", "hop": "Muốn biết kiểu đối tượng nào hợp nhất. Cả 3 nhóm chạy CÙNG một bài, chỉ khác người xem.",
     "so_bai": 1},
    {"id": "1-3-3", "nhom": 3, "bai": 1, "ten": "1 chiến dịch, 3 nhóm, 3 bài (mỗi nhóm 1 bài)", "hop": "Muốn thử 3 kiểu đối tượng khác nhau, mỗi nhóm một bài. Cần ngân sách ngày cao hơn.",
     "so_bai": 3},
]

KHUNG = {
    "facebook": {
        "ten": "Facebook / Meta", "cap": ["Chiến dịch", "Nhóm quảng cáo", "Quảng cáo"], "gach": "Ad set, Ad",
        "kieu": [{"id": "thuong", "ten": "Chiến dịch thường", "mo_ta": "Anh chọn từng thứ: đối tượng, vị trí, nội dung. Hợp khi muốn kiểm soát."},
                 {"id": "advantage_plus", "ten": "Advantage+ (AI tự tối ưu nhiều thứ)", "mo_ta": "Meta tự tìm người, tự chọn vị trí. Hợp bán hàng khi đã có Pixel."}],
        "muc_tieu": [
            {"id": "tin_nhan", "ten": "Nhận tin nhắn", "mo_ta": "Khách nhắn vào Messenger, Zalo hoặc Instagram.", "goc": "Tương tác hoặc Khách hàng tiềm năng, đích Tin nhắn"},
            {"id": "khach", "ten": "Khách để lại thông tin", "mo_ta": "Khách điền biểu mẫu để lại tên, số điện thoại.", "goc": "Khách hàng tiềm năng, Biểu mẫu tức thì"},
            {"id": "ban_hang", "ten": "Bán hàng, đơn hàng", "mo_ta": "Khách mua trên website hoặc cửa hàng.", "goc": "Doanh số"},
            {"id": "truy_cap", "ten": "Kéo người vào website", "mo_ta": "Nhiều lượt bấm vào trang web.", "goc": "Lượt truy cập"},
            {"id": "tuong_tac", "ten": "Tăng tương tác bài viết", "mo_ta": "Thêm thích, bình luận, chia sẻ.", "goc": "Tương tác"},
            {"id": "xem_video", "ten": "Nhiều người xem video", "mo_ta": "Video được xem lâu.", "goc": "Tương tác, Lượt xem video"},
            {"id": "nhan_dien", "ten": "Nhiều người biết đến", "mo_ta": "Phủ rộng, chưa cần khách ngay.", "goc": "Mức độ nhận biết"}],
        "cta": ["Gửi tin nhắn", "Xem thêm", "Mua ngay", "Đăng ký", "Liên hệ chúng tôi", "Gọi ngay", "Nhận báo giá", "Đặt ngay", "Đăng ký ngay", "Tải xuống", "Xem video"],
        "cta_theo_muc_tieu": {"tin_nhan": "Gửi tin nhắn", "khach": "Đăng ký", "ban_hang": "Mua ngay", "truy_cap": "Xem thêm", "tuong_tac": "Xem thêm", "xem_video": "Xem thêm", "nhan_dien": "Xem thêm"},
        "tuy_chinh": [
            {"id": "fanpage", "ten": "Người từng tương tác Fanpage", "mo_ta": "Thích, bình luận, nhắn tin, bấm vào Fanpage trong 365 ngày.", "can": "Fanpage đã nối với tài khoản quảng cáo"},
            {"id": "instagram", "ten": "Người từng tương tác Instagram", "mo_ta": "Xem, lưu, nhắn tin tới tài khoản Instagram doanh nghiệp.", "can": "Instagram doanh nghiệp đã nối"},
            {"id": "video", "ten": "Người đã xem video của anh", "mo_ta": "Xem ít nhất 3 giây, 50% hoặc 95% video.", "can": ""},
            {"id": "form", "ten": "Người đã mở biểu mẫu khách hàng", "mo_ta": "Mở hoặc gửi biểu mẫu của anh.", "can": ""},
            {"id": "web", "ten": "Người đã vào website", "mo_ta": "Khách từng vào trang web, xem sản phẩm, bỏ giỏ hàng.", "can": "Đã cài Pixel Meta trên website"},
            {"id": "danh_sach", "ten": "Danh sách khách hàng của anh", "mo_ta": "Tải file số điện thoại, email khách cũ lên để chạy lại.", "can": "Có file khách hàng (CSV)"}],
        "tuong_tu": {"ten": "Đối tượng tương tự (Lookalike)", "mo_ta": "Meta tìm thêm người giống nhóm khách tốt của anh. 1% giống nhất, 5% rộng hơn.", "phan_tram": [1, 2, 3, 5]},
        "loai_tru": ["Khách đã mua", "Khách đã để lại thông tin", "Người đã nhắn tin gần đây", "Nhân viên và người nhà"],
        "ai": [
            {"id": "doi_tuong", "ten": "Advantage+ đối tượng", "mac_dinh": False, "khuyen": True, "bat": "Meta tự tìm thêm người có khả năng mua, ngoài gợi ý của anh.", "tat": "Chỉ chạy đúng đối tượng anh chọn. Kiểm soát hơn, nhưng có thể đắt hơn."},
            {"id": "vi_tri", "ten": "Advantage+ vị trí hiển thị", "mac_dinh": False, "khuyen": True, "bat": "Meta tự đặt quảng cáo ở nơi rẻ nhất: Facebook, Instagram, Messenger.", "tat": "Anh chọn nơi hiển thị. Hợp khi chỉ muốn một nơi."},
            {"id": "noi_dung", "ten": "Advantage+ tối ưu nội dung", "mac_dinh": False, "khuyen": False, "bat": "Meta tự chỉnh sáng, cắt, thêm chữ, tạo biến thể từ hình và video của anh.", "tat": "Giữ nguyên hình và chữ anh làm."},
            {"id": "ngan_sach", "ten": "Ngân sách chiến dịch tự chia (Advantage+)", "mac_dinh": False, "khuyen": True, "bat": "Anh đặt một ngân sách chung, Meta tự chia cho các nhóm.", "tat": "Anh đặt ngân sách riêng cho từng nhóm."}],
        "luu_y": ["Nên có Pixel và Fanpage nối đúng trước khi chạy.", "Mục tiêu tin nhắn: kiểm tra Zalo hoặc Messenger có người trực.", "Mỗi nhóm cần đủ ngân sách để Meta học (khoảng 50 kết quả mỗi tuần)."],
        "chi_tiet_bai": "Mỗi bài gồm: nội dung chính, tiêu đề, hình hoặc video, nút kêu gọi.",
        "can_media": "hinh_video"},
    "tiktok": {
        "ten": "TikTok", "cap": ["Chiến dịch", "Nhóm quảng cáo", "Quảng cáo"], "gach": "Ad group, Ad",
        "kieu": [{"id": "thu_cong", "ten": "Thủ công", "mo_ta": "Anh chọn đối tượng, ngân sách, nội dung từng nhóm."},
                 {"id": "smart_plus", "ten": "Smart+ (AI chạy tự động)", "mo_ta": "TikTok tự ghép nội dung, tự tìm người. Chỉ cần đưa video, chữ và ngân sách."}],
        "muc_tieu": [
            {"id": "tin_nhan", "ten": "Nhận tin nhắn", "mo_ta": "Khách nhắn tin hoặc bấm nút liên hệ.", "goc": "Khách hàng tiềm năng (tin nhắn) hoặc Lưu lượng"},
            {"id": "khach", "ten": "Khách để lại thông tin", "mo_ta": "Khách điền biểu mẫu ngay trong TikTok.", "goc": "Khách hàng tiềm năng"},
            {"id": "ban_hang", "ten": "Bán hàng, đơn hàng", "mo_ta": "Khách mua trên website hoặc TikTok Shop.", "goc": "Chuyển đổi trang web hoặc Doanh số sản phẩm"},
            {"id": "truy_cap", "ten": "Kéo người vào website", "mo_ta": "Nhiều lượt bấm vào trang web.", "goc": "Lưu lượng"},
            {"id": "xem_video", "ten": "Nhiều người xem video", "mo_ta": "Video được xem trọn vẹn.", "goc": "Lượt xem video"},
            {"id": "tuong_tac", "ten": "Tăng theo dõi và tương tác", "mo_ta": "Thêm người theo dõi kênh, thích, bình luận.", "goc": "Tương tác cộng đồng"},
            {"id": "nhan_dien", "ten": "Nhiều người biết đến", "mo_ta": "Phủ rộng, chưa cần khách ngay.", "goc": "Phạm vi tiếp cận"}],
        "cta": ["Xem thêm", "Mua ngay", "Đăng ký", "Liên hệ chúng tôi", "Đặt hàng ngay", "Ứng tuyển ngay", "Tải xuống", "Xem ngay"],
        "cta_theo_muc_tieu": {"tin_nhan": "Liên hệ chúng tôi", "khach": "Đăng ký", "ban_hang": "Mua ngay", "truy_cap": "Xem thêm", "tuong_tac": "Xem ngay", "xem_video": "Xem ngay", "nhan_dien": "Xem thêm"},
        "tuy_chinh": [
            {"id": "video", "ten": "Người đã xem video", "mo_ta": "Xem 6 giây, 15 giây hoặc xem hết video quảng cáo.", "can": ""},
            {"id": "ca_nhan", "ten": "Người đã vào trang cá nhân hoặc thích, bình luận", "mo_ta": "Tương tác với kênh TikTok của anh.", "can": "Kênh TikTok đã nối"},
            {"id": "form", "ten": "Người đã mở biểu mẫu", "mo_ta": "Mở hoặc gửi biểu mẫu khách hàng.", "can": ""},
            {"id": "web", "ten": "Người đã vào website", "mo_ta": "Khách từng vào web, xem sản phẩm, bỏ giỏ.", "can": "Đã cài TikTok Pixel"},
            {"id": "danh_sach", "ten": "Danh sách khách hàng của anh", "mo_ta": "Tải file số điện thoại, email khách cũ.", "can": "Có file khách hàng (CSV)"}],
        "tuong_tu": {"ten": "Đối tượng tương tự (Lookalike)", "mo_ta": "TikTok tìm thêm người giống nhóm khách tốt của anh.", "phan_tram": [1, 3, 5]},
        "loai_tru": ["Khách đã mua", "Khách đã để lại thông tin", "Người đã xem video gần đây"],
        "ai": [
            {"id": "doi_tuong", "ten": "Tự tìm đối tượng (Automated targeting)", "mac_dinh": False, "khuyen": True, "bat": "TikTok tự mở rộng đối tượng khi thấy người phù hợp.", "tat": "Chỉ chạy đúng đối tượng anh chọn."},
            {"id": "noi_dung", "ten": "Tự tối ưu nội dung (Automated creative)", "mac_dinh": False, "khuyen": True, "bat": "TikTok tự ghép hình, video, chữ, nút kêu gọi và thay bài khi người xem chán.", "tat": "Giữ nguyên từng bài anh làm."},
            {"id": "ngan_sach", "ten": "Ngân sách chiến dịch tự chia", "mac_dinh": False, "khuyen": True, "bat": "Một ngân sách chung, TikTok tự chia cho các nhóm.", "tat": "Đặt ngân sách riêng cho từng nhóm."},
            {"id": "vi_tri", "ten": "Tự chọn vị trí hiển thị", "mac_dinh": False, "khuyen": True, "bat": "Hiện trên TikTok và các ứng dụng đối tác nơi rẻ nhất.", "tat": "Chỉ hiện trên TikTok."}],
        "luu_y": ["TikTok ưu tiên video dọc 9:16, 15 đến 60 giây, mở đầu hấp dẫn trong 2 giây đầu.", "Cần cài TikTok Pixel nếu mục tiêu là bán hàng trên website.", "Smart+ hợp khi đã có vài video tốt và muốn đỡ phải chỉnh."],
        "chi_tiet_bai": "Mỗi bài gồm: video dọc (hoặc hình), lời dẫn, nút kêu gọi. Có thể dùng video đang đăng trên kênh (Spark Ads).",
        "can_media": "video_truoc"},
    "google": {
        "ten": "Google Ads", "cap": ["Chiến dịch", "Nhóm quảng cáo (hoặc nhóm tài sản)", "Quảng cáo"], "gach": "Ad group, Asset group, Ad",
        "kieu": [{"id": "search", "ten": "Tìm kiếm", "mo_ta": "Quảng cáo chữ hiện khi người ta gõ từ khoá trên Google. Hợp khách đang cần mua ngay."},
                 {"id": "pmax", "ten": "Performance Max (AI chạy khắp Google)", "mo_ta": "Google tự đặt ở Tìm kiếm, YouTube, Gmail, Bản đồ. Cần hình, video, chữ."},
                 {"id": "demand_gen", "ten": "Demand Gen (YouTube, Discover, Gmail)", "mo_ta": "Quảng cáo hình ảnh và video để gợi nhu cầu. Hợp phủ rộng."}],
        "muc_tieu": [
            {"id": "khach", "ten": "Khách để lại thông tin, gọi điện", "mo_ta": "Khách điền biểu mẫu hoặc gọi điện.", "goc": "Khách hàng tiềm năng"},
            {"id": "ban_hang", "ten": "Bán hàng, đơn hàng", "mo_ta": "Khách mua trên website.", "goc": "Doanh số"},
            {"id": "truy_cap", "ten": "Kéo người vào website", "mo_ta": "Nhiều lượt bấm vào trang web.", "goc": "Lưu lượng truy cập trang web"},
            {"id": "tin_nhan", "ten": "Khách liên hệ (tin nhắn, gọi)", "mo_ta": "Khách bấm gọi hoặc nhắn tin từ quảng cáo.", "goc": "Khách hàng tiềm năng, Lượt gọi"},
            {"id": "xem_video", "ten": "Nhiều người xem video (YouTube)", "mo_ta": "Video được xem trên YouTube.", "goc": "Cân nhắc sản phẩm và thương hiệu"},
            {"id": "nhan_dien", "ten": "Nhiều người biết đến", "mo_ta": "Phủ rộng thương hiệu.", "goc": "Mức độ nhận biết"}],
        "cta": ["Tìm hiểu thêm", "Liên hệ chúng tôi", "Gọi ngay", "Nhận báo giá", "Đăng ký", "Mua ngay", "Đặt ngay", "Xem thêm", "Tải xuống"],
        "cta_theo_muc_tieu": {"khach": "Liên hệ chúng tôi", "ban_hang": "Mua ngay", "truy_cap": "Tìm hiểu thêm", "tin_nhan": "Gọi ngay", "xem_video": "Xem thêm", "nhan_dien": "Tìm hiểu thêm"},
        "tuy_chinh": [
            {"id": "web", "ten": "Người đã vào website (tiếp thị lại)", "mo_ta": "Khách từng vào web, xem sản phẩm, bỏ giỏ.", "can": "Đã gắn thẻ Google (Google tag)"},
            {"id": "youtube", "ten": "Người đã xem video YouTube của anh", "mo_ta": "Xem video hoặc theo dõi kênh YouTube.", "can": "Kênh YouTube đã nối"},
            {"id": "danh_sach", "ten": "Danh sách khách hàng của anh (Customer Match)", "mo_ta": "Tải file số điện thoại, email khách cũ.", "can": "Có file khách hàng (CSV)"},
            {"id": "ung_dung", "ten": "Người dùng ứng dụng", "mo_ta": "Người đã cài hoặc dùng app của anh.", "can": "Có ứng dụng"}],
        "tuong_tu": {"ten": "Phân khúc tương tự (Demand Gen)", "mo_ta": "Google tìm người giống danh sách khách của anh. Chỉ có ở Demand Gen.", "phan_tram": [1, 3, 5]},
        "loai_tru": ["Khách đã mua", "Khách đã để lại thông tin", "Từ khoá không liên quan (ví dụ: miễn phí, việc làm)"],
        "ai": [
            {"id": "ai_max", "ten": "AI Max cho Tìm kiếm", "mac_dinh": False, "khuyen": False, "bat": "Google mở rộng từ khoá và sửa chữ quảng cáo theo người tìm. Nhiều khách hơn, ít kiểm soát hơn.", "tat": "Chỉ chạy đúng từ khoá anh chọn."},
            {"id": "tai_san_tu_tao", "ten": "Tự tạo thêm chữ và hình (tài sản tự động)", "mac_dinh": False, "khuyen": False, "bat": "Google tự viết thêm tiêu đề, mô tả từ trang web của anh.", "tat": "Chỉ dùng chữ và hình anh đưa."},
            {"id": "gia_thau", "ten": "Đặt giá thầu thông minh", "mac_dinh": False, "khuyen": True, "bat": "Google tự điều giá để có nhiều kết quả nhất.", "tat": "Anh tự đặt giá mỗi lượt bấm. Cần quen việc."},
            {"id": "doi_tuong", "ten": "Tối ưu đối tượng", "mac_dinh": False, "khuyen": True, "bat": "Google tự mở rộng ra người giống người đã chuyển đổi.", "tat": "Chỉ dùng đối tượng và tín hiệu anh đưa."}],
        "luu_y": ["Tìm kiếm: cần danh sách từ khoá và từ khoá loại trừ cho từng nhóm.", "Quảng cáo chữ gồm nhiều tiêu đề (tối đa 15) và mô tả (tối đa 4), Google tự ghép.", "Tìm kiếm không dùng video; hình và video dành cho Performance Max, Demand Gen."],
        "chi_tiet_bai": "Mỗi bài gồm: các tiêu đề và mô tả ngắn (Tìm kiếm), hoặc hình, video, chữ (Performance Max, Demand Gen).",
        "can_media": "chu_truoc"},
}

# Ngành: từ khoá nhận diện (không dấu) -> gợi ý đối tượng
NGANH = [
    {"id": "bat_dong_san", "ten": "Bất động sản", "tu": ["nha pho", "bat dong san", "can ho", "dat nen", "mua nha", "ban nha", "chung cu", "du an", "bds"],
     "tuoi": [28, 55], "gt": "Cả nam và nữ", "so_thich": ["Bất động sản", "Mua nhà", "Đầu tư", "Vay mua nhà", "Nội thất, trang trí nhà"], "hanh_vi": ["Chủ doanh nghiệp nhỏ", "Người có ý định mua nhà"],
     "tu_khoa": ["mua nhà phố", "bán nhà phố giá tốt", "nhà phố gần trung tâm", "tư vấn mua nhà"], "loai_tru": ["cho thuê", "việc làm", "miễn phí"],
     "nhom": [("Người quan tâm mua nhà", "Sở thích Bất động sản, Mua nhà, Đầu tư"), ("Người có thu nhập ổn định", "Chủ doanh nghiệp nhỏ, nhân viên văn phòng 30 đến 50 tuổi"), ("Khu vực quan tâm", "Người đang ở gần khu vực dự án")]},
    {"id": "dao_tao", "ten": "Đào tạo, khoá học", "tu": ["khoa hoc", "dao tao", "hoc vien", "lop hoc", "giang day", "hoc truc tuyen", "workshop", "dao tao"],
     "tuoi": [22, 45], "gt": "Cả nam và nữ", "so_thich": ["Học trực tuyến", "Khởi nghiệp", "Marketing", "Phát triển bản thân", "Kinh doanh online"], "hanh_vi": ["Chủ doanh nghiệp nhỏ", "Người dùng điện thoại thông minh"],
     "tu_khoa": ["khoá học", "học online", "lớp học ngắn hạn", "đào tạo kỹ năng"], "loai_tru": ["miễn phí", "việc làm", "tải về"],
     "nhom": [("Người muốn học kỹ năng", "Sở thích Học trực tuyến, Phát triển bản thân"), ("Chủ shop, người bán hàng", "Sở thích Kinh doanh online, Marketing"), ("Người đi làm muốn đổi nghề", "22 đến 40 tuổi, sở thích Khởi nghiệp")]},
    {"id": "thoi_trang", "ten": "Thời trang, phụ kiện", "tu": ["thoi trang", "quan ao", "ao ", "vay ", "giay", "tui xach", "phu kien"],
     "tuoi": [18, 40], "gt": "Nữ là chính", "so_thich": ["Thời trang", "Mua sắm trực tuyến", "Làm đẹp", "Xu hướng"], "hanh_vi": ["Người hay mua hàng online", "Người dùng Instagram"],
     "tu_khoa": ["mua áo online", "váy đẹp", "thời trang nữ giá tốt"], "loai_tru": ["sỉ", "việc làm"],
     "nhom": [("Người thích mua sắm online", "Sở thích Mua sắm trực tuyến, Thời trang"), ("Người theo dõi các thương hiệu thời trang", "Sở thích Xu hướng, Làm đẹp"), ("Khách đã mua và người giống họ", "Đối tượng tuỳ chỉnh và Lookalike")]},
    {"id": "my_pham_spa", "ten": "Làm đẹp, spa, thẩm mỹ", "tu": ["my pham", "spa", "tham my", "lam dep", "cham soc da", "toc", "nail"],
     "tuoi": [22, 50], "gt": "Nữ là chính", "so_thich": ["Làm đẹp", "Chăm sóc da", "Spa và sức khoẻ", "Mỹ phẩm"], "hanh_vi": ["Người hay mua hàng online"],
     "tu_khoa": ["spa gần đây", "chăm sóc da mặt", "trị mụn", "làm đẹp giá tốt"], "loai_tru": ["tự làm tại nhà", "việc làm"],
     "nhom": [("Người quan tâm làm đẹp", "Sở thích Làm đẹp, Chăm sóc da"), ("Người ở gần cơ sở", "Bán kính 5 đến 10 km quanh cơ sở"), ("Khách cũ và người giống họ", "Đối tượng tuỳ chỉnh và Lookalike")]},
    {"id": "an_uong", "ten": "Ăn uống, nhà hàng, quán cà phê", "tu": ["nha hang", "quan an", "cafe", "ca phe", "do an", "thuc don", "tra sua", "am thuc"],
     "tuoi": [18, 45], "gt": "Cả nam và nữ", "so_thich": ["Ẩm thực", "Ăn uống bên ngoài", "Cà phê", "Giao đồ ăn"], "hanh_vi": ["Người hay đi ăn ngoài"],
     "tu_khoa": ["quán ăn ngon gần đây", "nhà hàng", "đặt bàn", "cà phê view đẹp"], "loai_tru": ["công thức nấu", "việc làm"],
     "nhom": [("Người ở gần quán", "Bán kính 3 đến 5 km quanh quán"), ("Người thích ăn uống", "Sở thích Ẩm thực, Cà phê"), ("Khách cũ và người giống họ", "Đối tượng tuỳ chỉnh và Lookalike")]},
    {"id": "du_lich", "ten": "Du lịch, khách sạn", "tu": ["du lich", "khach san", "tour", "resort", "homestay", "ve may"],
     "tuoi": [24, 55], "gt": "Cả nam và nữ", "so_thich": ["Du lịch", "Nghỉ dưỡng", "Chụp ảnh", "Ẩm thực"], "hanh_vi": ["Người hay đi du lịch", "Người đi du lịch thường xuyên"],
     "tu_khoa": ["tour du lịch", "đặt phòng khách sạn", "resort giá tốt"], "loai_tru": ["việc làm", "xin visa"],
     "nhom": [("Người thích du lịch", "Sở thích Du lịch, Nghỉ dưỡng"), ("Gia đình có con nhỏ", "Phụ huynh 28 đến 45 tuổi"), ("Khách cũ và người giống họ", "Đối tượng tuỳ chỉnh và Lookalike")]},
    {"id": "giao_duc_tre", "ten": "Giáo dục trẻ em", "tu": ["tre em", "be ", "mam non", "tieng anh tre", "hoc sinh", "gia su"],
     "tuoi": [25, 45], "gt": "Cả nam và nữ (phụ huynh)", "so_thich": ["Nuôi dạy con", "Giáo dục", "Trẻ em"], "hanh_vi": ["Phụ huynh có con nhỏ", "Phụ huynh có con tuổi đi học"],
     "tu_khoa": ["lớp học cho bé", "trung tâm tiếng Anh trẻ em", "gia sư"], "loai_tru": ["việc làm", "miễn phí"],
     "nhom": [("Phụ huynh có con nhỏ", "Hành vi Phụ huynh, 25 đến 40 tuổi"), ("Người quan tâm giáo dục", "Sở thích Giáo dục, Nuôi dạy con"), ("Khu vực quanh trung tâm", "Bán kính 5 đến 8 km")]},
    {"id": "cong_nghe", "ten": "Phần mềm, công nghệ, dịch vụ cho doanh nghiệp", "tu": ["phan mem", "cong nghe", "app", "website", "thiet ke web", "crm", "tu dong hoa", "ai "],
     "tuoi": [25, 50], "gt": "Cả nam và nữ", "so_thich": ["Khởi nghiệp", "Công nghệ", "Marketing số", "Quản lý doanh nghiệp"], "hanh_vi": ["Chủ doanh nghiệp nhỏ", "Quản trị trang Facebook"],
     "tu_khoa": ["phần mềm quản lý bán hàng", "thiết kế website", "tự động hoá marketing"], "loai_tru": ["miễn phí", "crack", "việc làm"],
     "nhom": [("Chủ doanh nghiệp nhỏ", "Hành vi Chủ doanh nghiệp nhỏ"), ("Người quan tâm công nghệ", "Sở thích Công nghệ, Marketing số"), ("Khách đã dùng thử và người giống họ", "Đối tượng tuỳ chỉnh và Lookalike")]},
    {"id": "dich_vu", "ten": "Dịch vụ chung", "tu": [],
     "tuoi": [22, 55], "gt": "Cả nam và nữ", "so_thich": ["Mua sắm trực tuyến"], "hanh_vi": ["Người dùng điện thoại thông minh"],
     "tu_khoa": [], "loai_tru": ["việc làm", "miễn phí"],
     "nhom": [("Người ở khu vực phục vụ", "Theo khu vực anh chọn"), ("Người có sở thích liên quan", "Anh thêm sở thích gần với sản phẩm"), ("Khách cũ và người giống họ", "Đối tượng tuỳ chỉnh và Lookalike")]},
]


def _khong_dau(s: str) -> str:
    x = unicodedata.normalize("NFD", str(s)).replace("đ", "d").replace("Đ", "D").encode("ascii", "ignore").decode().lower()
    return " " + re.sub(r"\s+", " ", x) + " "


def goi_y_target(nen: str, mo_ta: str = "", khu_vuc: str = "") -> dict:
    """Gợi ý đối tượng từ mô tả sản phẩm. Luật theo ngành, không gọi AI nên trả ngay. Anh chỉnh lại được mọi thứ."""
    t = _khong_dau(mo_ta)
    nganh = next((n for n in NGANH if any(" " + k.lstrip() in t for k in n["tu"])), NGANH[-1])
    kh = KHUNG.get(nen) or KHUNG["facebook"]
    ra = {"nganh": nganh["ten"], "tuoi_tu": nganh["tuoi"][0], "tuoi_den": nganh["tuoi"][1], "gioi_tinh": nganh["gt"], "khu_vuc": khu_vuc.strip(),
          "loai_tru": nganh["loai_tru"], "nhom": [{"ten": a, "mo_ta": b} for a, b in nganh["nhom"]]}
    if nen == "google":
        ra["tu_khoa"] = nganh["tu_khoa"] or ["(anh nhập từ khoá khách hay gõ)"]
        ra["so_thich"] = []
        ra["hanh_vi"] = []
        ra["ghi_chu"] = "Google Tìm kiếm nhắm theo từ khoá người ta gõ. Gợi ý từ khoá bên dưới, nhớ thêm tên khu vực. Phần tuổi, giới tính dùng khi chạy Performance Max hoặc Demand Gen."
    else:
        ra["so_thich"] = nganh["so_thich"]
        ra["hanh_vi"] = nganh["hanh_vi"]
        ra["tu_khoa"] = []
        ra["ghi_chu"] = ("Chạy rộng trước, xem 3 đến 5 ngày rồi mới thu hẹp. Đối tượng quá hẹp thì nền tảng khó tìm được người." if nen != "tiktok"
                         else "TikTok hợp đối tượng rộng, để TikTok tự tìm người theo video. Thu hẹp quá thì video ít được đẩy.")
    ra["tong"] = "%s: tuổi %d đến %d, %s." % (kh["ten"], ra["tuoi_tu"], ra["tuoi_den"], ra["gioi_tinh"].lower())
    return ra


# ---------------------------------------------------------------- tải lên hình, video, danh sách
LOAI_TAI = {"anh": ({".jpg", ".jpeg", ".png", ".webp", ".gif"}, 15 * 1024 * 1024), "video": ({".mp4", ".mov", ".m4v", ".webm"}, 600 * 1024 * 1024),
            "danh_sach": ({".csv", ".txt", ".xlsx"}, 20 * 1024 * 1024)}


def _doc_tai() -> list:
    try:
        d = json.loads(TEP_TAI.read_text(encoding="utf-8"))
        return d if isinstance(d, list) else []
    except (OSError, ValueError):
        return []


def tep_cong_khai(t: dict) -> dict:
    return {"id": t["id"], "loai": t["loai"], "ten": t["ten"], "kich_thuoc": t["kich_thuoc"], "luc": t["luc"]}


def danh_sach_tep() -> list:
    return [tep_cong_khai(t) for t in _doc_tai() if Path(t["duong_dan"]).is_file()]


def tim_tep(tid: str):
    return next((t for t in _doc_tai() if t["id"] == tid and Path(t["duong_dan"]).is_file()), None)


def xoa_tep(tid: str) -> bool:
    with _khoa:
        ds = _doc_tai()
        t = next((x for x in ds if x["id"] == tid), None)
        if not t:
            return False
        try:
            Path(t["duong_dan"]).unlink()
        except OSError:
            pass
        Q._ghi(TEP_TAI, [x for x in ds if x["id"] != tid])
    return True


async def nhan_tep(request, loai: str, ten: str) -> dict:
    if loai not in LOAI_TAI:
        raise ValueError("Loại tệp không đúng.")
    duoi, tran = LOAI_TAI[loai]
    ten = re.sub(r"[^\w.\- ()À-ỹ]", "_", os.path.basename(ten or "tep"))[:120] or "tep"
    ext = os.path.splitext(ten)[1].lower()
    if ext not in duoi:
        raise ValueError("Chỉ nhận: " + ", ".join(sorted(duoi)))
    tid = "tl-" + hashlib.sha1(("%s%s" % (ten, time.time())).encode()).hexdigest()[:10]
    THU_MUC_TAI.mkdir(parents=True, exist_ok=True)
    dich = THU_MUC_TAI / (tid + ext)
    n = 0
    try:
        with open(dich, "wb") as f:
            async for chunk in request.stream():
                n += len(chunk)
                if n > tran:
                    raise ValueError("Tệp quá lớn (tối đa %d MB)." % (tran // 1024 // 1024))
                f.write(chunk)
        if n == 0:
            raise ValueError("Tệp rỗng.")
    except Exception:
        try:
            dich.unlink()
        except OSError:
            pass
        raise
    try:
        os.chmod(dich, 0o600)
    except OSError:
        pass
    t = {"id": tid, "loai": loai, "ten": ten, "kich_thuoc": n, "duong_dan": str(dich), "luc": int(time.time())}
    with _khoa:
        ds = _doc_tai()
        ds.append(t)
        Q._ghi(TEP_TAI, ds[-300:])
    return tep_cong_khai(t)


# ---------------------------------------------------------------- quét kết nối (API đã nhập và MCP trong TISA BOT)
_LA_NEN = {"facebook": re.compile(r"(meta|facebook|fb).{0,14}ads|ads.{0,14}(meta|facebook)", re.I),
           "tiktok": re.compile(r"tiktok.{0,14}ads|ads.{0,14}tiktok", re.I), "google": re.compile(r"google.{0,3}ads", re.I)}


def ket_noi() -> dict:
    out = {n: {"api": [], "mcp": [], "ok": False} for n in Q.NEN}
    for t in Q.danh_sach():
        k = t.get("kiem_tra") or {}
        out[t["nen"]]["api"].append({"id": t["id"], "ten": t["ten"], "ma_tk": t["ma_tk"], "ok": bool(k.get("ok")), "da_kiem_tra": bool(k)})
    try:
        import connect_health
        import mcp_store
        suc_khoe = connect_health.snapshot()
        for c in mcp_store.list_connections():
            ten = "%s %s %s" % (c.get("connector_id") or "", c.get("name") or "", c.get("label") or "")
            for n, rx in _LA_NEN.items():
                if rx.search(ten):
                    s = suc_khoe.get(c.get("id")) or {}
                    out[n]["mcp"].append({"id": c.get("id"), "ten": c.get("name") or c.get("connector_id"), "bat": bool(c.get("enabled")),
                                          "ok": bool(c.get("enabled")) and bool(s.get("ok")), "da_kiem_tra": bool(s), "thong_bao": s.get("message") or "",
                                          "chi_doc": c.get("perm") == "read"})
    except Exception:  # noqa: BLE001 - không đọc được kho MCP thì chỉ báo phần API
        pass
    for n, v in out.items():
        v["ok"] = any(x["ok"] for x in v["api"]) or any(x["ok"] for x in v["mcp"])
        v["co"] = bool(v["api"] or v["mcp"])
    return out


# ---------------------------------------------------------------- phiếu thiết lập đời 2
def doc_phieu() -> list:
    try:
        d = json.loads(TEP_NHAP.read_text(encoding="utf-8"))
        return d if isinstance(d, list) else []
    except (OSError, ValueError):
        return []


def _so_nguyen(v, lo, hi, mac_dinh):
    try:
        return max(lo, min(hi, int(v)))
    except (TypeError, ValueError):
        return mac_dinh


def _chuoi(v, n):
    return str(v or "").strip()[:n]


def _ds_chuoi(v, n=60, toi_da=30):
    return [_chuoi(x, n) for x in (v or []) if _chuoi(x, n)][:toi_da] if isinstance(v, list) else []


def luu_phieu(d: dict) -> dict:
    nen = _chuoi(d.get("nen"), 12)
    if nen not in Q.NEN:
        raise ValueError("Chọn nền tảng.")
    ten = _chuoi(d.get("ten"), 120)
    if not ten:
        raise ValueError("Đặt tên chiến dịch.")
    try:
        ns = float(d.get("ngan_sach_ngay") or 0)
    except (TypeError, ValueError):
        raise ValueError("Ngân sách mỗi ngày phải là số.")
    if ns <= 0:
        raise ValueError("Nhập ngân sách mỗi ngày lớn hơn 0.")
    kh = KHUNG[nen]
    ct = d.get("cau_truc") if isinstance(d.get("cau_truc"), dict) else {}
    nhom = _so_nguyen(ct.get("nhom"), 1, 5, 1)
    bai_n = _so_nguyen(ct.get("bai"), 1, 5, 1)
    ids_tep = {t["id"] for t in _doc_tai()}
    bai = []
    for b in (d.get("bai") or [])[:25]:
        if not isinstance(b, dict):
            continue
        mid = _chuoi(b.get("media_id"), 20)
        bai.append({"nhom": _so_nguyen(b.get("nhom"), 1, 5, 1), "stt": _so_nguyen(b.get("stt"), 1, 25, len(bai) + 1), "media_id": mid if mid in ids_tep else "",
                    "tieu_de": _chuoi(b.get("tieu_de"), 200), "noi_dung": _chuoi(b.get("noi_dung"), 2000), "cta": _chuoi(b.get("cta"), 40), "link": _chuoi(b.get("link"), 400),
                    "slides": [{"media_id": (_chuoi(x.get("media_id"), 20) if _chuoi(x.get("media_id"), 20) in ids_tep else ""), "tieu_de": _chuoi(x.get("tieu_de"), 80), "mo_ta": _chuoi(x.get("mo_ta"), 300)}
                               for x in (b.get("slides") or [])[:10] if isinstance(x, dict)]})
    nhom_ds = []
    for g in (d.get("nhom") or [])[:5]:
        if isinstance(g, dict):
            nhom_ds.append({"ten": _chuoi(g.get("ten"), 80), "mo_ta": _chuoi(g.get("mo_ta"), 400)})
    tg = d.get("target") if isinstance(d.get("target"), dict) else {}
    ai = {k: bool(v) for k, v in (d.get("ai") or {}).items() if k in {a["id"] for a in kh["ai"]}} if isinstance(d.get("ai"), dict) else {}
    tc = [k for k in (d.get("tuy_chinh") or []) if k in {a["id"] for a in kh["tuy_chinh"]}] if isinstance(d.get("tuy_chinh"), list) else []
    tt = d.get("tuong_tu") if isinstance(d.get("tuong_tu"), dict) else {}
    hs = d.get("ho_so") if isinstance(d.get("ho_so"), dict) else {}
    p = {"v": 2, "id": _chuoi(d.get("id"), 20) or "ph-" + hashlib.sha1(("%s%s" % (ten, time.time())).encode()).hexdigest()[:8], "nen": nen, "ten": ten,
         "che_do": "tu_dong" if d.get("che_do") == "tu_dong" else "tu_chon", "kieu": _chuoi(d.get("kieu"), 20), "muc_tieu": _chuoi(d.get("muc_tieu"), 20),
         "cau_truc": {"id": _chuoi(ct.get("id"), 10), "nhom": nhom, "bai": bai_n, "chung": bool(ct.get("chung"))}, "ngan_sach_ngay": ns, "tu_ngay": _chuoi(d.get("tu_ngay"), 10), "den_ngay": _chuoi(d.get("den_ngay"), 10),
         "tai_khoan": _chuoi(d.get("tai_khoan"), 60), "mo_ta_san_pham": _chuoi(d.get("mo_ta_san_pham"), 1500), "dich_den": _chuoi(d.get("dich_den"), 400),
         "bai": bai, "nhom": nhom_ds, "tuy_chinh": tc, "tuong_tu": {"bat": bool(tt.get("bat")), "nguon": _chuoi(tt.get("nguon"), 20), "phan_tram": _so_nguyen(tt.get("phan_tram"), 1, 10, 1)},
         "loai_tru": _ds_chuoi(d.get("loai_tru")), "ai": ai,
         "target": {"khu_vuc": _chuoi(tg.get("khu_vuc"), 200), "tuoi_tu": _so_nguyen(tg.get("tuoi_tu"), 13, 65, 18), "tuoi_den": _so_nguyen(tg.get("tuoi_den"), 13, 65, 65),
                    "gioi_tinh": _chuoi(tg.get("gioi_tinh"), 40), "so_thich": _ds_chuoi(tg.get("so_thich")), "hanh_vi": _ds_chuoi(tg.get("hanh_vi")), "tu_khoa": _ds_chuoi(tg.get("tu_khoa"), 80, 60)},
         "file_khach": [x for x in _ds_chuoi(d.get("file_khach"), 20, 5) if x in ids_tep], "ghi_chu": _chuoi(d.get("ghi_chu"), 800), "sua": time.strftime("%Y-%m-%d %H:%M"),
         "ui": d["ui"] if isinstance(d.get("ui"), dict) and len(json.dumps(d["ui"])) < 60000 else {},
         "nguon": d.get("nguon") if d.get("nguon") in ("moi", "bai_dang", "ai") else "moi",
         "ho_so": ({k: _chuoi(hs.get(k), 300) for k in ("id", "ten", "link", "giong_van")} if isinstance(hs, dict) else {}),
         "bai_dang": [{"url": _chuoi(x.get("url"), 400), "loai": _chuoi(x.get("loai"), 20), "ma_bai": _chuoi(x.get("ma_bai"), 80), "trang": _chuoi(x.get("trang"), 120), "rut_gon": bool(x.get("rut_gon"))}
                      for x in (d.get("bai_dang") or [])[:10] if isinstance(x, dict) and _chuoi(x.get("url"), 400)]}
    with _khoa:
        ds = [x for x in doc_phieu() if x.get("id") != p["id"]]
        ds.insert(0, p)
        Q._ghi(TEP_NHAP, ds[:100])
    return p


def xoa_phieu(pid: str) -> bool:
    with _khoa:
        ds = doc_phieu()
        moi = [x for x in ds if x.get("id") != pid]
        Q._ghi(TEP_NHAP, moi)
    return len(moi) < len(ds)


def _ten_muc(kh, lst, mid):
    return next((x["ten"] for x in kh[lst] if x["id"] == mid), mid)


def loi_nhac(p: dict) -> str:
    """Lời nhờ trợ lý tạo chiến dịch theo phiếu. Luôn tạm dừng, chờ chủ duyệt rồi mới bật."""
    nen = p["nen"]
    kh = KHUNG[nen]
    skill = {"facebook": "/ts-len-camp-facebook (và công cụ Meta Ads đã nối nếu có)", "tiktok": "/ts-chay-tiktok-ads (và công cụ TikTok Ads đã nối nếu có)",
             "google": "công cụ Google Ads đã nối (MCP hoặc API)"}[nen]
    cap = kh["cap"]
    ct = p.get("cau_truc") or {}
    L = ["Hãy chuẩn bị chiến dịch quảng cáo %s theo phiếu bên dưới, dùng %s." % (kh["ten"], skill),
         "QUY TẮC BẮT BUỘC: tạo ở trạng thái TẠM DỪNG hoặc NHÁP. Không bật, không đăng, không tiêu tiền cho tới khi anh trả lời đồng ý trong chat này. Không đổi hay xoá chiến dịch đang chạy.",
         "Nếu thiếu thông tin hoặc màn hình nền tảng khác với phiếu thì hỏi lại anh, không tự đoán những thứ tốn tiền.",
         "Xong thì báo: mã từng cấp, thứ đã tạo, thứ chưa tạo được, và các bước để bật.", ""]
    if p.get("che_do") == "tu_dong":
        L += ["CHẾ ĐỘ TỰ ĐỘNG: anh không rành quảng cáo. Hãy tự quyết các chi tiết kỹ thuật theo phiếu, giải thích ngắn gọn bằng tiếng Việt dễ hiểu đã chọn gì và vì sao.", ""]
    L += ["PHIẾU (%s):" % kh["ten"], "- %s: %s" % (cap[0], p["ten"]), "- Mục tiêu: %s" % _ten_muc(kh, "muc_tieu", p.get("muc_tieu")),
          "- Dạng chiến dịch: %s" % _ten_muc(kh, "kieu", p.get("kieu")),
          ("- Cấu trúc: 1 %s, %d %s, cùng chạy 1 bài giống nhau ở mọi nhóm (chỉ khác đối tượng)" % (cap[0].lower(), ct.get("nhom", 1), cap[1].lower())) if ct.get("chung") else
          "- Cấu trúc: 1 %s, %d %s, mỗi nhóm %d bài (%d bài)" % (cap[0].lower(), ct.get("nhom", 1), cap[1].lower(), ct.get("bai", 1), ct.get("nhom", 1) * ct.get("bai", 1)),
          "- Ngân sách mỗi ngày: {:,.0f}".format(p["ngan_sach_ngay"]).replace(",", ".")]
    for nhan, k in (("Chạy từ ngày", "tu_ngay"), ("Đến ngày", "den_ngay"), ("Tài khoản quảng cáo", "tai_khoan"), ("Sản phẩm, dịch vụ", "mo_ta_san_pham"), ("Đích đến (link, Zalo, số điện thoại)", "dich_den")):
        if p.get(k):
            L.append("- %s: %s" % (nhan, p[k]))
    t = p.get("target") or {}
    hs = p.get("ho_so") or {}
    if hs.get("ten"):
        L.append("- %s: %s%s" % ({"facebook": "Quảng cáo cho Fanpage", "tiktok": "Quảng cáo cho kênh TikTok", "google": "Quảng cáo cho website, thương hiệu"}[nen], hs["ten"], (" (" + hs["link"] + ")") if hs.get("link") else ""))
    if p.get("nguon") == "bai_dang":
        L += ["", "NGUỒN BÀI: CHẠY ĐÚNG BÀI ĐÃ ĐĂNG, không tạo bài mới.",
              {"facebook": "Dùng bài viết có sẵn trên Fanpage làm quảng cáo (tạo quảng cáo từ bài có sẵn, giữ nguyên lượt thích, bình luận). Nếu là link rút gọn thì mở ra để lấy mã bài thật. Bài phải ở chế độ Công khai và thuộc đúng Fanpage trên.",
               "tiktok": "Dùng đúng video TikTok đã đăng làm quảng cáo (Spark Ads). Nếu cần mã ủy quyền video thì hướng dẫn anh lấy trong TikTok (Cài đặt, Quyền riêng tư, Quảng cáo), đừng tự đoán.",
               "google": "Dùng đúng video YouTube đã đăng làm quảng cáo video, kênh YouTube phải được nối với tài khoản Google Ads."}[nen]]
    L += ["", "ĐỐI TƯỢNG:", "- Khu vực: %s" % (t.get("khu_vuc") or "(chưa ghi, hãy hỏi anh)"), "- Tuổi: %s đến %s, giới tính: %s" % (t.get("tuoi_tu"), t.get("tuoi_den"), t.get("gioi_tinh") or "cả hai")]
    if t.get("so_thich"):
        L.append("- Sở thích: " + ", ".join(t["so_thich"]))
    if t.get("hanh_vi"):
        L.append("- Hành vi: " + ", ".join(t["hanh_vi"]))
    if t.get("tu_khoa"):
        L.append("- Từ khoá: " + ", ".join(t["tu_khoa"]))
    if p.get("loai_tru"):
        L.append("- Loại trừ: " + ", ".join(p["loai_tru"]))
    if p.get("tuy_chinh"):
        L.append("- Đối tượng tuỳ chỉnh (chạy cho họ): " + ", ".join(_ten_muc(kh, "tuy_chinh", x) for x in p["tuy_chinh"]))
    if (p.get("tuong_tu") or {}).get("bat"):
        tt = p["tuong_tu"]
        L.append("- %s: nguồn %s, mức %d%%" % (kh["tuong_tu"]["ten"], _ten_muc(kh, "tuy_chinh", tt.get("nguon")) if tt.get("nguon") else "khách tốt nhất", tt.get("phan_tram", 1)))
    for i, g in enumerate(p.get("nhom") or [], 1):
        if g.get("ten") or g.get("mo_ta"):
            L.append("- %s %d: %s. %s" % (cap[1], i, g.get("ten") or "", g.get("mo_ta") or ""))
    tep = {x["id"]: x for x in _doc_tai()}
    L += ["", "BÀI QUẢNG CÁO (%d bài), nút kêu gọi ghi theo từng bài:" % len(p.get("bai") or [])]
    for b in p.get("bai") or []:
        m = tep.get(b.get("media_id"))
        if b.get("slides"):
            L.append("- %s %d, bài %d: QUẢNG CÁO NHIỀU TẤM (carousel %d tấm) | nội dung chính: %s | nút: %s" % (cap[1], b["nhom"], b["stt"], len(b["slides"]), (b.get("noi_dung") or "(trợ lý đề xuất)")[:300].replace("\n", " "), b.get("cta") or "(theo mục tiêu)"))
            for i, sl in enumerate(b["slides"], 1):
                m = tep.get(sl.get("media_id"))
                L.append("    Tấm %d: %s | tiêu đề: %s | mô tả: %s" % (i, ("hình %s (tệp trên máy này: %s)" % (m["ten"], m["duong_dan"])) if m else "chưa có hình", sl.get("tieu_de") or "", sl.get("mo_ta") or ""))
            continue
        if b.get("link"):
            L.append("- %s %d, bài %d: BÀI ĐÃ ĐĂNG %s | nút: %s" % (cap[1], b["nhom"], b["stt"], b["link"], b.get("cta") or "(theo mục tiêu)"))
            continue
        L.append("- %s %d, bài %d: %s | tiêu đề: %s | nội dung: %s | nút: %s" % (cap[1], b["nhom"], b["stt"], ("%s %s (tệp trên máy này: %s)" % ("video" if m["loai"] == "video" else "hình", m["ten"], m["duong_dan"])) if m else "chưa có hình/video (hãy hỏi anh)",
                                                                           b.get("tieu_de") or "(trợ lý đề xuất)", (b.get("noi_dung") or "(trợ lý đề xuất, chờ anh duyệt)")[:400].replace("\n", " "), b.get("cta") or "(theo mục tiêu)"))
    if p.get("file_khach"):
        L.append("- Danh sách khách hàng dùng cho đối tượng tuỳ chỉnh: " + ", ".join("%s (%s)" % (tep[i]["ten"], tep[i]["duong_dan"]) for i in p["file_khach"] if i in tep) + ". Dữ liệu khách hàng chỉ dùng cho tài khoản này, không gửi đi đâu khác.")
    L += ["", "TỰ TỐI ƯU CỦA AI (BẬT hay TẮT, theo đúng lựa chọn của anh):"]
    for a in kh["ai"]:
        bat = p.get("ai", {}).get(a["id"], a["mac_dinh"])
        L.append("- %s: %s" % (a["ten"], "BẬT" if bat else "TẮT"))
    if p.get("ghi_chu"):
        L += ["", "Ghi chú thêm: " + p["ghi_chu"]]
    L += ["", "Lưu ý riêng cho %s:" % kh["ten"]] + ["- " + x for x in kh["luu_y"]]
    return "\n".join(L)


def khung_cong_khai() -> dict:
    return {"khung": KHUNG, "mau_cau_truc": MAU_CAU_TRUC, "nganh": [{"id": n["id"], "ten": n["ten"]} for n in NGANH]}


# ---------------------------------------------------------------- đường dẫn
def gan(app) -> None:
    from fastapi.responses import FileResponse, JSONResponse

    def loi(msg, ma=400):
        return JSONResponse({"ok": False, "error": msg}, status_code=ma)

    @app.get("/tisa-quang-cao/api/khung")
    async def _khung():
        return {"ok": True, **khung_cong_khai()}

    @app.get("/tisa-quang-cao/api/goi-y-target")
    async def _gy(request: Request):
        q = request.query_params
        return {"ok": True, **goi_y_target(q.get("nen", "facebook"), q.get("mo_ta", ""), q.get("khu_vuc", ""))}

    @app.get("/tisa-quang-cao/api/ket-noi")
    async def _kn():
        import asyncio
        return {"ok": True, "ket_noi": await asyncio.to_thread(ket_noi), "luc": int(time.time())}

    @app.get("/tisa-quang-cao/api/tep")
    async def _ds_tep():
        return {"ok": True, "tep": danh_sach_tep()}

    @app.post("/tisa-quang-cao/api/tai-len")
    async def _tai_len(request: Request):
        q = request.query_params
        try:
            return {"ok": True, "tep": await nhan_tep(request, q.get("loai", ""), q.get("ten", ""))}
        except ValueError as e:
            return loi(str(e))

    @app.get("/tisa-quang-cao/api/tep/{tid}")
    async def _xem_tep(tid: str):
        t = tim_tep(tid)
        if not t:
            return loi("Không có tệp này.", 404)
        return FileResponse(t["duong_dan"], headers={"cache-control": "private, max-age=3600", "x-content-type-options": "nosniff"})

    @app.post("/tisa-quang-cao/api/tep/{tid}/xoa")
    async def _xoa_tep(tid: str):
        return {"ok": xoa_tep(tid)}

    @app.get("/tisa-quang-cao/api/phieu")
    async def _ds_phieu():
        return {"ok": True, "phieu": doc_phieu()}

    @app.post("/tisa-quang-cao/api/phieu")
    async def _luu_phieu(request: Request):
        try:
            p = luu_phieu(await request.json())
        except ValueError as e:
            return loi(str(e))
        return {"ok": True, "phieu": p, "loi_nhac": loi_nhac(p)}

    @app.post("/tisa-quang-cao/api/phieu/{pid}/xoa")
    async def _xoa_phieu(pid: str):
        return {"ok": xoa_phieu(pid)}

    try:
        import tisa_quang_cao_ai
        tisa_quang_cao_ai.gan(app)
    except Exception as e:  # noqa: BLE001 - phần AI hỏng không được làm hỏng phần thiết lập
        print(f"[tisa_quang_cao_ai] không bật được: {type(e).__name__}: {e}")
