---
name: ts-email-cham-soc
description: "Gọi bằng /ts-email-cham-soc. Viết chuỗi email chăm sóc khách hàng hoàn chỉnh: hâm nóng trước mở bán, email mở bán 3 ngày, chào mừng và hướng dẫn sau khi mua 14–30 ngày, đánh thức khách im lặng, xin đánh giá, giới thiệu sản phẩm tiếp theo — có tiêu đề, dòng xem trước, giờ gửi, CTA. Dùng cho khóa học, sản phẩm số, dịch vụ, cửa hàng. Từ khóa: chuỗi email, email marketing, email chào mừng, email onboarding, email mở bán, email nurture, email upsell, email chăm sóc khách, welcome sequence."
---

# /ts-email-cham-soc — Chuỗi email chăm sóc khách hàng

> Viết trọn chuỗi email theo hành trình khách: trước khi mua (hâm nóng), lúc mở bán, sau khi mua (chào mừng,
> hướng dẫn, giữ chân) và khi khách im lặng. Mỗi email đủ tiêu đề, dòng xem trước, nội dung, 1 CTA và giờ gửi.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Sắp mở bán sản phẩm/khóa học/dịch vụ — cần chuỗi email hâm nóng danh sách chờ.
- Đang mở bán — cần 3 email chốt (mở cửa, trả lời câu hỏi, nhắc lần cuối).
- Khách vừa mua — cần email chào mừng, hướng dẫn dùng, giữ chân, xin đánh giá, giới thiệu gói tiếp theo.
- Khách mua rồi nhưng không dùng / không mở email — cần chuỗi đánh thức.
- Muốn cài chuỗi email tự động trên Mailchimp, Brevo, GetResponse, ActiveCampaign…

**Không dùng khi:** cần tin nhắn ngắn Zalo/Messenger → `/ts-cham-soc-khach-zalo`; cần bài đăng mạng xã hội →
`/ts-viet-bai-ban-hang`; cần trang bán hàng → `/ts-trang-ban-hang`; cần cài hệ thống gửi sản phẩm tự động sau
thanh toán → `/ts-giao-hang-tu-dong`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `email-cham-soc` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

Thêm cho skill này — dùng lại kết quả các lệnh trước nếu có trong `04-ket-qua/`:
- `…-chan-dung-khach-hang-…` → nỗi đau, mong muốn, ngôn ngữ khách (thay cho hỏi lại đối tượng).
- `…-dinh-gia-offer-…` → giá, quà tặng, bảo hành, hạn ưu đãi (dùng nguyên văn, không tự đổi).
- `…-xu-ly-tu-choi-…` và `02-kien-thuc/khach-hang/bang-khoan-thuong-gap.md` → câu hỏi thường gặp cho email trả lời câu hỏi.
- `02-kien-thuc/khach-hang/cau-chuyen-khach-hang.md` → câu chuyện khách thật cho email câu chuyện.
Chưa có các kết quả này mà cần → gợi ý chạy `/ts-chan-dung-khach-hang`, `/ts-dinh-gia-offer`, `/ts-xu-ly-tu-choi`.

## Quy trình AI thực hiện

### Bước 1 — Thu thập thông tin (hỏi gộp 1 lần, chỉ phần còn thiếu)
```
Để viết chuỗi email hiệu quả, mình cần biết:
1. Sản phẩm / dịch vụ / khóa học nào?
2. Khách nhận email là ai? (danh sách chờ / khách mới mua / khách lâu không tương tác…)
3. Giá + quà tặng + bảo hành / hoàn tiền (nếu có)?
4. Công cụ gửi email: A. Mailchimp · B. Brevo · C. GetResponse / ActiveCampaign · D. Gmail thường · E. Chưa có
5. Mục tiêu chuỗi: A. Hâm nóng trước mở bán · B. Mở bán · C. Chào mừng sau mua · D. Đánh thức khách im lặng
6. Đã có đánh giá / câu chuyện khách thật chưa?
```

### Bước 2 — Chọn và viết chuỗi
Đọc `references/mau-email.md` (cấu trúc email, công thức tiêu đề) trước khi viết. Chi tiết từng email ở
`references/chuoi-email-4-loai.md`. Tóm tắt:

| Chuỗi | Số email | Lịch gửi | Mục tiêu |
|---|---|---|---|
| **A. Hâm nóng trước mở bán** | 4 | Ngày −7, −5, −3, −1 | Gây tò mò, kết nối, hé lộ giải pháp, ưu đãi đăng ký sớm |
| **B. Mở bán** | 3 | Ngày 1, 2, 3 | Mở cửa + ưu đãi đầy đủ → trả lời câu hỏi + bằng chứng → nhắc lần cuối |
| **C. Chào mừng sau mua** | 7 | Ngày 0, 2, 4, 7, 10, 12, 14 | Bắt đầu ngay → thắng nhỏ đầu tiên → hỏi thăm → câu chuyện → mẹo nâng cao → xin đánh giá → gợi ý bước tiếp theo |
| **D. Đánh thức** | 3 | Sau 7, 14, 21 ngày im lặng | Hỏi thăm → có gì mới → lời chào cuối |

Điều chỉnh theo loại hình kinh doanh:
- **Khóa học / sản phẩm số:** "bắt đầu" = vào học, xem bài 1; "thắng nhỏ" = hoàn thành 1 bài tập.
- **Sản phẩm vật lý:** "bắt đầu" = nhận hàng, mở hộp, dùng lần đầu; "thắng nhỏ" = mẹo dùng đúng; "bước tiếp theo" = phụ kiện, mua lại.
- **Dịch vụ:** "bắt đầu" = chuẩn bị trước buổi hẹn; "thắng nhỏ" = việc tự làm ở nhà để giữ kết quả; "bước tiếp theo" = gói định kỳ.
- Muốn hành trình dài 30 ngày → `references/hanh-trinh-cham-soc-30-ngay.md`.

### Bước 3 — Trình bày đúng định dạng
Đầu chuỗi:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 [TÊN CHUỖI EMAIL]
Sản phẩm: [Tên] | Số email: [X]
Người nhận: [Danh sách chờ / Khách mới mua / Khách im lặng…]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
Mỗi email:
```
📨 EMAIL [Số] — [Tên email]
Gửi lúc: [Thời điểm cụ thể + điều kiện kích hoạt]
Tiêu đề: "[≤ 50 ký tự]"
Dòng xem trước: "[80–100 ký tự]"
─────────────────────────────
[Nội dung đầy đủ — đoạn ≤ 3 dòng, xuống dòng nhiều]
─────────────────────────────
CTA: [1 hành động + link]
```
Cuối chuỗi — **Bước tiếp theo gợi ý** (thay cho bàn giao):
- Đo tỷ lệ mở / tỷ lệ bấm sau 1–2 tuần → `/ts-phan-tich-doanh-thu`.
- Câu hỏi khách hỏi lại qua email → đưa vào `/ts-xu-ly-tu-choi` hoặc `/ts-cham-soc-fanpage` làm kho trả lời.
- Lý do khách chưa mua lộ ra trong email → cải thiện trang bán hàng bằng `/ts-trang-ban-hang`.

### Bước 4 — Tình huống đặc biệt
- **Chỉ dùng Gmail thường:** viết email bình thường; gợi ý công cụ miễn phí (Brevo, Mailchimp gói miễn phí — số
  liên hệ tối đa thay đổi theo thời gian, kiểm tra trên web của họ); số lượng ít thì hướng dẫn lên lịch gửi trong
  Gmail (*mũi tên cạnh nút Gửi → Lên lịch gửi*).
- **Muốn email ngắn (< 100 chữ):** viết dạng thư thuần chữ, không ảnh, không tiêu đề lớn — thường được mở nhiều hơn.
- **Hỏi tần suất:** hâm nóng 1 email/2 ngày · mở bán 1 email/ngày (tối đa 3–5 ngày) · sau mua theo lịch chuỗi ·
  bản tin định kỳ tối đa 2–3 lần/tuần.
- **Muốn tự động:** ghi rõ **điều kiện kích hoạt** cho từng email (vừa mua / vừa đăng ký danh sách / không mở email
  X ngày) và hướng dẫn tạo chuỗi tự động (Automation / Workflow) trong công cụ người dùng chọn.

### Bước 5 — Cổng duyệt
Trình chuỗi. Sửa theo yêu cầu đến khi người dùng gõ **"duyệt"**. Skill **chỉ viết**; gửi thật / bật chuỗi tự động
qua công cụ chỉ khi người dùng duyệt danh sách người nhận + nội dung.

### Checklist chất lượng (AI tự kiểm trước khi trình)
- [ ] Mỗi email có tiêu đề + dòng xem trước; tiêu đề ≤ 50 ký tự (không bị cắt trên điện thoại).
- [ ] Mỗi email đúng **1 CTA**.
- [ ] Có giá trị thật, không chỉ bán; ghi thời điểm gửi cụ thể.
- [ ] Giọng văn khớp `04-thuong-hieu-noi-dung.md`, xưng hô nhất quán.
- [ ] Giá, ưu đãi, hạn chót, bảo hành đúng hồ sơ — không tự nghĩ ra.
- [ ] Không bịa đánh giá, câu chuyện, số liệu; thiếu thì `[CẦN BỔ SUNG: …]`.
- [ ] Có link hủy đăng ký ở cuối (nhắc người dùng bật trong công cụ).

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** tên sản phẩm, giá, quà tặng, chính sách hoàn tiền; link mua / link truy cập / số hỗ trợ;
1–3 đánh giá khách thật (nếu có); biết bạn dùng công cụ email nào (chưa có thì AI gợi ý).
1. Gõ `/ts-email-cham-soc` kèm mục tiêu, vd "chuỗi chào mừng cho khách vừa mua khóa học".
2. Trả lời 6 câu AI hỏi (chọn chữ cái A–E cho nhanh).
3. Xem chuỗi email; sửa bằng lời ("email 2 ngắn lại", "tiêu đề bớt giật gân").
4. Gõ **"duyệt"** để AI chốt và lưu vào Bộ Não.
5. Dán từng email vào công cụ gửi theo đúng giờ/điều kiện AI ghi (nhờ AI hướng dẫn từng nút nếu cần).
6. Gửi thử email cho chính mình trước, kiểm tra link và hiển thị trên điện thoại.
7. Sau 1–2 tuần, gõ `/ts-phan-tich-doanh-thu` kèm tỷ lệ mở/bấm để AI đánh giá.

## Câu lệnh mẫu
- `/ts-email-cham-soc chuỗi chào mừng 14 ngày cho học viên khóa học làm nến thơm online, dùng Brevo`
- `/ts-email-cham-soc 4 email hâm nóng trước khi mở bán bộ sưu tập túi da thủ công ngày 1/12`
- `/ts-email-cham-soc chuỗi chăm sóc sau mua cho khách mua máy lọc không khí, tháng thứ 6 nhắc thay lõi`
- `/ts-email-cham-soc khách thuê dịch vụ kế toán đã 2 tháng không phản hồi email, viết chuỗi đánh thức`

## Kết quả nhận được
- Chuỗi email hoàn chỉnh (3–7 email, hoặc hành trình 30 ngày) đúng định dạng: tiêu đề, xem trước, nội dung, CTA, giờ gửi.
- Điều kiện kích hoạt từng email để cài tự động.
- Gợi ý bước tiếp theo (đo hiệu quả, cải thiện trang bán, kho trả lời).

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-email-cham-soc-<chu-de-khong-dau>/`.
2. Lưu chuỗi email đã duyệt (đầu chuỗi + toàn bộ email + điều kiện kích hoạt) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-email-cham-soc
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `lich-gui-email.csv` (email-so, tieu-de, gui-luc, dieu-kien-kich-hoat), mỗi email dài thành `email-01.md`, `email-02.md`…
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-email-cham-soc · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Tiêu đề email có tỷ lệ mở cao (khi người dùng báo lại số liệu) → đề xuất lưu vào `02-kien-thuc/cong-thuc/tieu-de-email-hieu-qua.md`. Công cụ email đang dùng chưa có trong `01-ho-so/05-muc-tieu-quy-tac-lien-he.md` → đề xuất ghi (không ghi mật khẩu/khóa API). Hỏi trước khi ghi.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Chỉ gửi cho người **đã đồng ý nhận email**; luôn có link hủy đăng ký. Người hủy không phải khách xấu — danh sách sạch tốt hơn danh sách đông.
- Không xin/lưu mật khẩu, khóa API của công cụ email trong chat hay Bộ Não.
- Không bịa đánh giá, số học viên, kết quả; không tạo khan hiếm giả ("chỉ còn 2 suất" khi không đúng).
- Email chào mừng chứa mật khẩu tạm của khách: nhắc người dùng để hệ thống tự điền, không gõ tay vào mẫu.

## Skill liên quan
- Trước: `/ts-chan-dung-khach-hang` · `/ts-dinh-gia-offer` · `/ts-xu-ly-tu-choi` · `/ts-pheu-qua-tang`
- Sau: `/ts-phan-tich-doanh-thu` · `/ts-cham-soc-khach-zalo` · `/ts-giao-hang-tu-dong` · `/ts-trang-ban-hang`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
