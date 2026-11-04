# Từ số liệu đến hành động — /ts-phan-tich-mang-xa-hoi

> Số liệu đơn thuần không giúp chủ shop. File này biến chỉ số thành **chẩn đoán + 3 việc làm tuần này**.
> (Thay cho đường dẫn chéo sang skill khác trong bộ gốc — nay tự chứa trong skill này.)

## Nguyên tắc
Không bao giờ kết thúc báo cáo bằng một bảng số. Mọi báo cáo kết thúc bằng **"Nghĩa là gì → Làm gì"**.

## Luồng
```
Số liệu vào (mạng xã hội + doanh thu nếu có)
  → Tìm khâu yếu nhất trong phễu
  → Đoán nguyên nhân có khả năng nhất
  → Ra 3 việc làm trong tuần này
```

## Tìm khâu yếu trong phễu
Đi từ trên xuống; khâu yếu **đầu tiên** là chỗ cần sửa trước:

| Khâu | Chỉ số nhìn vào | Nếu yếu → nguyên nhân hay gặp | Lệnh hỗ trợ |
|---|---|---|---|
| Tiếp cận | Lượt xem / người tiếp cận thấp | Câu mở đầu yếu, đăng quá ít, sai giờ | `/ts-lich-noi-dung` · `/ts-kich-ban-reels` |
| Tương tác | Xem nhiều nhưng ít thích/bình luận/lưu | Nội dung chưa đủ giá trị, chưa nói đúng chữ khách hay dùng | `/ts-chan-dung-khach-hang` · `/ts-viet-bai-ban-hang` |
| Bấm link | Tương tác tốt nhưng ít bấm | Lời kêu gọi yếu, ưu đãi chưa rõ | `/ts-viet-quang-cao` · `/ts-dinh-gia-offer` |
| Trang đích | Nhiều người vào trang, ít để lại thông tin | Trang chưa thuyết phục, chậm, rối | `/ts-trang-ban-hang` · `/ts-landing-page` |
| Thanh toán | Nhiều người hỏi/đặt, ít người trả tiền | Khó trả tiền, thiếu tin tưởng, giá | `/ts-cai-thanh-toan` · `/ts-xu-ly-tu-choi` |
| Mua lại | Mua 1 lần rồi thôi | Trải nghiệm sau mua, không chăm sóc | `/ts-giao-hang-tu-dong` · `/ts-email-cham-soc` · `/ts-cham-soc-khach-zalo` |

> Mốc "tốt/xấu" khác nhau theo ngành và quy mô kênh — ưu tiên so với **chính kênh mình kỳ trước**; cần mốc ngành thì
> tìm số liệu thật theo `_chung/data-sourcing-protocol.md` (ghi nguồn + ngày), không lấy con số cố định.

## Mẫu kết quả (luôn dùng)
```
📊 Chuyện gì đang xảy ra
- [2–3 câu đọc số bằng lời thường]

🔍 Khâu yếu nhất
- [1 khâu đang làm mất nhiều nhất + vì sao có khả năng]

✅ Làm trong tuần này (3 việc)
1. [việc cụ thể, đo được] → lệnh hỗ trợ: /ts-…
2. …
3. …
```

## Nói số bằng lời thường
- Không viết "CTR 1,2%" trơ trọi → "Cứ 100 người thấy bài, chỉ khoảng 1 người bấm vào — câu mở đầu đang yếu."
- Không viết "ER 0,4%" → "1.000 người xem mà chỉ 4 người thả tim/bình luận — bài chưa chạm đúng điều khách quan tâm."
- Mỗi con số phải gắn với một quyết định.
