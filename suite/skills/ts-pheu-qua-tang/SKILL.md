---
name: ts-pheu-qua-tang
description: "Gọi bằng /ts-pheu-qua-tang. Thiết kế và triển khai phễu quà tặng 0 đồng qua 4 cổng duyệt: chọn quà (chấm điểm 3–7 ý tưởng), đóng gói quà hoàn chỉnh, dựng trang nhận quà + form có đồng ý + trang cảm ơn + nhóm Zalo + chuỗi 5–7 tin nuôi dưỡng, rồi phối hợp nội dung, quảng cáo, tự động hóa, đưa web lên mạng và đo lường. Dùng khi muốn thu số điện thoại/email khách tiềm năng bằng quà giá trị. Từ khóa: phễu quà tặng, lead magnet, quà miễn phí, thu lead, thu số điện thoại, ebook miễn phí, nuôi dưỡng khách, phễu 0 đồng."
---

# /ts-pheu-qua-tang — Phễu quà tặng 0 đồng

> Tạo một phễu chạy được: món quà miễn phí thật sự hữu ích → trang nhận quà có đồng ý → trang cảm ơn →
> nhóm/kênh giữ chân → chuỗi tin nuôi dưỡng → offer chính → đo lường. Mỗi giai đoạn bạn duyệt rồi mới làm tiếp.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Muốn có danh sách khách tiềm năng (số điện thoại/Zalo/email) trước khi bán.
- Sản phẩm giá vừa–cao, khách cần thời gian tìm hiểu.
- Quảng cáo bán thẳng đắt, muốn chuyển sang "tặng trước, bán sau".
- Đã chọn chiến lược "phễu quà tặng" ở `/ts-chien-luoc-marketing`.

**Không dùng khi:** chỉ cần thiết kế toàn bộ bậc thang sản phẩm và tính LTV → `/ts-thiet-ke-pheu`.
Chỉ cần viết trang nhận quà → `/ts-trang-ban-hang`. Chỉ cần viết chuỗi tin → `/ts-email-cham-soc` hoặc `/ts-cham-soc-khach-zalo`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `pheu-qua-tang` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

**Riêng skill này:** đọc thêm kết quả `/ts-chan-dung-khach-hang` (nỗi đau ưu tiên), `/ts-thiet-ke-pheu`,
`/ts-phan-tich-doi-thu` (đối thủ đang tặng gì) trong `04-ket-qua/` nếu có.

## Quy trình AI thực hiện

**Kết quả cần đạt:** một phễu chạy được gồm quà hữu ích, trang nhận quà, biểu mẫu có đồng ý, trang cảm ơn,
điểm giữ chân (nhóm Zalo/kênh/email), chuỗi nuôi dưỡng, nguồn khách và đo lường.

### Cổng 1 — Chọn quà
1. Tóm tắt sản phẩm chính, khách hàng, nỗi đau ưu tiên từ Bộ Não.
2. Đề xuất **3–7 quà** từ thư viện trong `references/thu-vien-qua-tang.md` (định dạng, gợi ý theo ngành).
   Đặt tên theo công thức: `[Kết quả cụ thể] trong [thời gian hợp lý] mà không cần [rào cản phổ biến]`.
3. Chấm từng quà 1–5 theo: sức hút với đúng khách · liên quan tới offer chính · khả năng tạo hành động tiếp ·
   tốc độ hoàn thiện · nguồn lực sản xuất. Trình bảng ma trận.
4. 👉 Chờ người dùng **chọn 1 quà**.

### Cổng 2 — Đóng gói và duyệt quà
1. Lập đề cương quà và định dạng bàn giao (PDF, video, bảng tính, ảnh, công cụ nhỏ).
2. Dùng lệnh phù hợp để đóng gói hoàn chỉnh: ebook → `/ts-tao-ebook` · bảng mẫu/máy tính → `/ts-bang-tinh-excel` ·
   slide → `/ts-thiet-ke-thuyet-trinh` · ảnh kiến thức → `/ts-infographic` · công cụ nhỏ/quiz → `/ts-tao-app`.
   (Lệnh không có trong môi trường → AI tự làm theo đề cương.)
3. Kiểm tra: đúng sự thật, áp dụng được ngay, có CTA dẫn sang bước tiếp theo.
4. 👉 Gửi bản xem trước, chờ "duyệt".

### Cổng 3 — Duyệt phễu
1. Viết trang nhận quà, biểu mẫu, trang cảm ơn, lời mời vào nhóm Zalo/kênh (có thể dùng `/ts-trang-ban-hang`
   biến thể trang nhận quà).
2. Biểu mẫu chỉ hỏi trường thật cần; nêu mục đích dùng dữ liệu; ô đồng ý không tích sẵn.
3. Thiết kế chuỗi **5–7 tin/email** nuôi dưỡng (mẫu 7 điểm chạm trong `references/thu-vien-qua-tang.md`), offer
   chuyển đổi có hạn **thật**, lịch nhắc lại quảng cáo (remarketing — quảng cáo nhắm lại người đã đăng ký/xem trang).
4. Lập sơ đồ đo lường: lượt xem trang → đăng ký → nhận quà → vào nhóm → tương tác → đặt lịch/mua.
5. 👉 Trình sơ đồ phễu + nội dung từng điểm chạm, chờ "duyệt".

### Cổng 4 — Triển khai
1. Sau xác nhận, phối hợp lệnh: trang web `/ts-landing-page` · giao quà tự động `/ts-giao-hang-tu-dong` ·
   báo lead `/ts-bao-don-telegram` · đưa lên mạng `/ts-dua-web-len-mang` · nội dung `/ts-lich-noi-dung` ·
   ảnh `/ts-thiet-ke-anh-quang-cao` · quảng cáo `/ts-viet-quang-cao` → `/ts-len-camp-facebook` · kết nối
   `/ts-ket-noi-ung-dung` · báo cáo `/ts-bao-cao-facebook-ads`.
2. Luôn tạo **bản xem trước** trước khi đưa lên hosting (Vercel, Netlify hoặc nền tảng phù hợp).
3. **Không** xuất bản, kết nối tài khoản, gửi tin hay chạy quảng cáo khi chưa được phép rõ ràng.
4. Kiểm thử theo checklist QA trong `references/thu-vien-qua-tang.md`: form, link tải, link nhóm, giao diện
   điện thoại, thông báo quyền riêng tư, mã đo lường.

### Checklist chất lượng
- [ ] Quà giải quyết **một** vấn đề nhỏ, cấp bách, dùng được trong ≤ 15 phút, dẫn tự nhiên tới sản phẩm chính.
- [ ] Tên quà theo công thức, không cam kết phi thực tế.
- [ ] Form tối thiểu, có đồng ý rõ ràng, có cách hủy nhận.
- [ ] Chuỗi nuôi dưỡng có giá trị trước, bán sau; ưu đãi/hạn chót là thật.
- [ ] Có sơ đồ đo lường và KPI từng bước.
- [ ] Qua hết checklist QA trước khi mở phễu.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** hồ sơ doanh nghiệp đã có sản phẩm chính và khách hàng. Nghĩ trước: bạn có sẵn tài liệu,
kinh nghiệm, mẹo nào có thể tặng? Có nhóm Zalo/kênh nào để mời khách vào chưa?

1. Gõ `/ts-pheu-qua-tang` kèm sản phẩm muốn bán sau cùng (vd "khóa học quay video 1,5 triệu").
2. **Cổng 1:** xem 3–7 ý tưởng quà và bảng điểm, chọn 1 (gõ số thứ tự).
3. **Cổng 2:** xem bản nháp quà, góp ý ("thêm ví dụ", "ngắn lại"), gõ "duyệt".
4. **Cổng 3:** đọc trang nhận quà, trang cảm ơn, chuỗi tin nhắn; sửa bằng lời rồi gõ "duyệt".
5. **Cổng 4:** AI hướng dẫn/kết nối để đưa trang lên mạng, tự gửi quà, báo lead. Mỗi việc công khai hoặc tốn
   tiền, AI hỏi lại — đọc kỹ rồi mới "duyệt".
6. Tự đăng ký thử 1 lần bằng số của mình để kiểm tra quà về đúng.
7. Sau 7 ngày, gõ `/ts-pheu-qua-tang xem kết quả phễu tuần đầu` kèm số liệu để AI đề xuất sửa.

## Câu lệnh mẫu
- `/ts-pheu-qua-tang khóa học quay video bằng điện thoại, muốn tặng checklist để thu số Zalo`
- `/ts-pheu-qua-tang spa Hồng muốn tặng phiếu soi da miễn phí để kéo khách mới tại quận`
- `/ts-pheu-qua-tang dịch vụ kế toán cho hộ kinh doanh, tặng bộ mẫu sổ sách để thu email`
- `/ts-pheu-qua-tang shop mỹ phẩm thiên nhiên, chưa biết tặng gì, gợi ý giúp tôi`

## Kết quả nhận được
- Ma trận chọn quà và quà đã đóng gói.
- Sơ đồ phễu và nội dung từng điểm chạm.
- Trang nhận quà + form + trang cảm ơn + lời mời vào nhóm.
- Chuỗi nuôi dưỡng 5–7 tin, kế hoạch nguồn khách, KPI và checklist QA.
- (Nếu đã kết nối và duyệt) phễu đang chạy với link công khai.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-pheu-qua-tang-<ten-qua-khong-dau>/`.
2. Lưu bản tổng hợp phễu (ma trận quà, sơ đồ, nội dung trang, chuỗi nuôi dưỡng, KPI, trạng thái QA, link công khai nếu có) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-pheu-qua-tang
   ngay: <YYYY-MM-DD>
   chu-de: <tên quà — sản phẩm chính>
   the: [pheu, qua-tang, lead, <ngành>]
   ---
   ```
   Kèm theo các file phụ (nếu có): tệp quà (`qua-tang.pdf`, `.xlsx`…), `trang-nhan-qua.md` hoặc `.html`,
   `chuoi-nuoi-duong.md`, `so-do-pheu.md`.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|Phễu quà <tên quà>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-pheu-qua-tang · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Thêm quà vào `01-ho-so/02-san-pham-dich-vu.md` (vai trò "mồi", giá 0đ, CTA) — hỏi trước khi ghi. Phễu chạy
   nhiều tuần → đề xuất trang theo dõi `05-du-an/pheu-<ten-qua>.md` (số liệu từng tuần).
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không thu thập dữ liệu nhạy cảm không cần thiết; không mua/bán danh sách; không gửi tin rác.
- Luôn có cách hủy nhận tin; tôn trọng người từ chối.
- Không thiết kế phễu cho hàng hóa/dịch vụ hạn chế độ tuổi hoặc nguy hiểm đối với người chưa thành niên.
- Ưu đãi, số lượng, hạn chót phải là thật; không dùng khan hiếm giả.
- Không xin mật khẩu/token trong chat; kết nối qua luồng chính thức.

## Skill liên quan
- Trước: `/ts-chien-luoc-marketing` · `/ts-chan-dung-khach-hang` · `/ts-thiet-ke-pheu`
- Sau: `/ts-trang-ban-hang` · `/ts-landing-page` · `/ts-giao-hang-tu-dong` · `/ts-email-cham-soc` · `/ts-len-camp-facebook`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
