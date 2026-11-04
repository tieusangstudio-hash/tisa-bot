# Công thức & khung trình bày 5 loại phân tích

> Dùng ở Bước 2–4 của `/ts-phan-tich-doanh-thu`. Mọi số "tham khảo" bên dưới chỉ để định hướng khi doanh
> nghiệp chưa có số liệu; luôn ưu tiên so với mục tiêu và kỳ trước của chính doanh nghiệp. Ví dụ là
> **doanh nghiệp giả định**.

## 0. Từ điển chỉ số (giải thích bằng lời thường)

| Chỉ số | Nghĩa là | Công thức |
|---|---|---|
| **CPL** | Tiền bỏ ra để có 1 người để lại thông tin / nhắn tin | Chi phí quảng cáo ÷ Số khách tiềm năng |
| **Tỷ lệ chuyển đổi** | Trong 100 người xem/nhắn, bao nhiêu người mua | Số đơn ÷ Số người xem (hoặc số khách tiềm năng) × 100% |
| **ROAS** | 1 đồng quảng cáo mang về bao nhiêu đồng doanh thu | Doanh thu từ quảng cáo ÷ Chi phí quảng cáo |
| **ROAS hòa vốn** | ROAS tối thiểu để không lỗ | 1 ÷ Biên lợi nhuận gộp (vd lãi gộp 40% → 2,5 lần) |
| **CAC** | Tổng tiền marketing để có 1 khách mới | Tổng chi marketing ÷ Số khách mới |
| **LTV** | Tổng tiền 1 khách mang lại trong suốt thời gian mua | Giá trị đơn TB × Số lần mua TB (× biên lãi nếu tính theo lãi) |
| **LTV/CAC** | Khách mang lại gấp mấy lần tiền bỏ ra để có họ | LTV ÷ CAC (tham khảo: ≥ 3 là khỏe) |
| **RPL** | Mỗi khách tiềm năng mang về bao nhiêu doanh thu | Doanh thu ÷ Số khách tiềm năng |
| **ROI** | Lãi so với tiền bỏ ra | (Lợi nhuận ÷ Tổng chi phí) × 100% |
| **NPS** | Mức sẵn lòng giới thiệu (hỏi 0–10) | % chấm 9–10 trừ % chấm 0–6 (hoặc dùng điểm TB cho đơn giản) |
| **Điểm hòa vốn** | Số đơn cần bán để không lời không lỗ | Chi phí cố định ÷ (Giá − Chi phí biến đổi mỗi đơn) |

---

## A. Dự báo doanh thu 90 ngày

```
━━━ MÔ HÌNH DỰ BÁO 3 THÁNG ━━━
GIẢ ĐỊNH: Giá [X]đ · Tỷ lệ chốt [Y]% · CPL [Z]đ · Tỷ lệ để lại thông tin trên trang [W]%

THÁNG 1 — KHỞI ĐỘNG
Mục tiêu: [số đơn] × [giá] = [doanh thu]
Để đạt được:
  - Cần [X] khách tiềm năng (tỷ lệ chốt [Y]%)
  - Cần [X] lượt xem trang (tỷ lệ để lại thông tin [W]%)
  - Cần [X]đ quảng cáo (CPL [Z]đ)
Chi phí ước tính: [X]đ · Lợi nhuận ước tính: [X]đ · ROI: [X]%

THÁNG 2 — TĂNG TỐC   (giải thích vì sao số tăng: tối ưu quảng cáo, khách cũ mua lại…)
THÁNG 3 — MỞ RỘNG    (giải thích cách mở rộng: thêm kênh, tăng ngân sách dần…)

TỔNG 90 NGÀY: Doanh thu [X]đ · Chi phí [X]đ · Lợi nhuận ròng [X]đ · ROI [X]% · Hòa vốn tại tuần/tháng [X]
```

---

## B. Bảng 10 chỉ số KPI hằng tuần

| # | Chỉ số | Công thức | Hiện tại | Mục tiêu | Báo động khi | Cách cải thiện |
|---|---|---|---|---|---|---|
| 1 | CPL | Chi QC ÷ khách tiềm năng | | | > [X]đ | Đổi nội dung/ảnh quảng cáo, mở rộng đối tượng |
| 2 | Tỷ lệ chuyển đổi trang | Đơn ÷ lượt xem | | | < [X]% | Sửa tiêu đề, ưu đãi, bằng chứng trên trang |
| 3 | ROAS | Doanh thu QC ÷ chi QC | | ≥ ROAS hòa vốn | < ROAS hòa vốn | Tắt quảng cáo yếu, dồn tiền cho quảng cáo tốt |
| 4 | CAC | Chi marketing ÷ khách mới | | | > [X]đ | Tăng tỷ lệ chốt, kênh miễn phí, giới thiệu |
| 5 | LTV & LTV/CAC | xem từ điển | | LTV/CAC ≥ 3 | < 3 | Bán thêm, mua lại, gói định kỳ |
| 6 | Tỷ lệ dùng/học hết | Người hoàn thành ÷ người mua | | > 60% (khóa học) | < 30% | Chuỗi chăm sóc sau mua `/ts-email-cham-soc` |
| 7 | Tỷ lệ hoàn tiền / đổi trả | Đơn hoàn ÷ tổng đơn | | < 5% | > 10% | Mô tả sản phẩm đúng, hướng dẫn dùng |
| 8 | NPS / điểm hài lòng | Khảo sát 0–10 | | > 8 | < 6 | Hỏi lý do điểm thấp, sửa đúng chỗ |
| 9 | Tỷ lệ mở email | Mở ÷ gửi | | > 30% | < 20% | Tiêu đề, làm sạch danh sách, giờ gửi |
| 10 | RPL | Doanh thu ÷ khách tiềm năng | | | giảm 2 tuần liền | So sánh giữa các kênh, dồn sức kênh RPL cao |

Bỏ chỉ số không phù hợp loại hình (vd cửa hàng ăn uống không có "tỷ lệ học hết") và thay bằng chỉ số tương ứng
(vd "tỷ lệ khách quay lại trong 30 ngày").

---

## C. Lãi lỗ quảng cáo theo 4 kịch bản

```
GIẢ ĐỊNH: Ngân sách [X]đ/tháng · Giá [Y]đ · Biên lợi nhuận gộp [M]% → ROAS hòa vốn = 1 ÷ M

KỊCH BẢN 1 — XẤU (ROAS 1,5)
  Doanh thu [X]đ · Lãi gộp [X]đ · Trừ chi QC → lời/lỗ [X]đ
  Nguyên nhân thường gặp: […] · Việc cần làm ngay: […]
KỊCH BẢN 2 — TRUNG BÌNH (ROAS 3)    Dấu hiệu nhận biết · Cách lên kịch bản tốt
KỊCH BẢN 3 — TỐT (ROAS 5)           Khi nào nên tăng ngân sách
KỊCH BẢN 4 — XUẤT SẮC (ROAS 8+)     Cách duy trì · Khi nào nên mở thêm kênh
```
Lưu ý: lời/lỗ thật = Doanh thu × Biên lãi gộp − Chi phí quảng cáo (không phải Doanh thu − Chi phí quảng cáo).

**Ví dụ (giả định — shop giày online):** ngân sách 20.000.000đ, lãi gộp 40% → ROAS hòa vốn 2,5.
ROAS 3 → doanh thu 60.000.000đ → lãi gộp 24.000.000đ → trừ quảng cáo còn **lời 4.000.000đ**.
ROAS 1,5 → doanh thu 30.000.000đ → lãi gộp 12.000.000đ → **lỗ 8.000.000đ**.

---

## D. Chi phí vận hành + hòa vốn

**Chi phí cố định (mỗi tháng)**
| Khoản | Chi phí/tháng | Ghi chú |
|---|---|---|
| Mặt bằng / kho | | |
| Nhân sự | | |
| Phần mềm (bán hàng, email, thiết kế…) | | |
| Website / tên miền / nền tảng | | |
| Khác | | |
| **Tổng cố định** | | |

**Chi phí biến đổi (theo mỗi đơn)**
| Khoản | Mỗi đơn | Ghi chú |
|---|---|---|
| Giá vốn hàng / nguyên vật liệu | | |
| Phí thanh toán / phí sàn | % | |
| Đóng gói, vận chuyển | | |
| Hoa hồng cộng tác viên | % | |
| **Tổng biến đổi / đơn** | | |

**Tổng chi phí tháng (ước tính [X] đơn)** = Cố định + Biến đổi × số đơn + Quảng cáo
**Hòa vốn** = Chi phí cố định (+ quảng cáo cố định nếu có) ÷ (Giá − Chi phí biến đổi mỗi đơn)

**Ví dụ (giả định — tiệm nail):** cố định 30.000.000đ/tháng; giá TB 250.000đ/khách; biến đổi 70.000đ/khách
→ mỗi khách góp 180.000đ → hòa vốn = 30.000.000 ÷ 180.000 ≈ **167 khách/tháng** (~6 khách/ngày).

---

## E. Tìm nguyên nhân doanh thu giảm (5 câu theo phễu)

Hỏi lần lượt, dừng ở câu "Có" đầu tiên:
1. **Lượt xem / lượt tiếp cận có giảm không?** → Có: vấn đề ở **kênh** (quảng cáo, nội dung, mùa vụ, thuật toán).
2. **Số khách tiềm năng (tin nhắn, đăng ký) có giảm dù lượt xem không giảm?** → Có: vấn đề ở **trang bán / ưu đãi / nội dung quảng cáo**.
3. **Tỷ lệ chốt (khách tiềm năng → mua) có giảm không?** → Có: vấn đề ở **quy trình chốt** (tốc độ trả lời, kịch bản tư vấn, chăm sóc).
4. **Giá trị đơn trung bình có giảm không?** → Có: vấn đề ở **giá / gói / đối thủ giảm giá**.
5. **Khách cũ mua lại ít hơn không?** → Có: vấn đề ở **giữ chân khách / chất lượng sản phẩm**.
   Không câu nào "Có" → có thể là biến động mùa vụ; so cùng kỳ năm trước nếu có.

Sau khi tìm ra gốc → đưa **3 giải pháp xếp theo mức tác động**, mỗi giải pháp có lệnh `/ts-...` để làm ngay.

---

## Mức tham khảo khi chưa có số liệu (chỉ định hướng)
- Tỷ lệ mở email: 20–30% · Tỷ lệ bấm email: 2–5%.
- ROAS: luôn so với **ROAS hòa vốn** của chính doanh nghiệp, không dùng một con số chung.
- LTV/CAC ≥ 3 được xem là khỏe.
- Tỷ lệ hoàn tiền < 5%.
Ghi rõ: "Số tham khảo — cần cập nhật sau 30 ngày chạy thực tế."
