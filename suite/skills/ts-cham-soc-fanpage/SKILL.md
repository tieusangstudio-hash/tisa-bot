---
name: ts-cham-soc-fanpage
description: "Gọi bằng /ts-cham-soc-fanpage. Lập kế hoạch chăm sóc Fanpage: trụ cột và lịch nội dung, thư viện câu trả lời mẫu, phân loại bình luận/tin nhắn, quy tắc chuyển cho người bán và tổng hợp insight hằng tuần; chỉ đăng/trả lời thật khi có kết nối và được duyệt. Dùng khi muốn chăm Fanpage đều đặn, trả lời khách nhanh và đúng giọng. Từ khóa: chăm sóc fanpage, trả lời bình luận, trả lời inbox, mẫu trả lời khách, FAQ fanpage, lịch đăng bài, quản lý trang, tăng tương tác."
---

# /ts-cham-soc-fanpage — Chăm sóc Fanpage và trả lời khách

> Giúp bạn chăm Fanpage đều đặn và trả lời khách nhanh, đúng giọng thương hiệu. Kết quả: lịch nội dung theo trụ cột,
> thư viện câu trả lời mẫu, bảng phân loại bình luận/tin nhắn, quy tắc chuyển cho người bán và mẫu tổng hợp insight cuối tuần.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Fanpage đăng bài thất thường, không biết tuần này đăng gì.
- Khách hỏi giá, địa chỉ, lịch… mỗi người trả lời một kiểu, trả lời chậm.
- Muốn có bộ câu trả lời mẫu (FAQ) cho nhân viên hoặc để cài tin nhắn tự động.
- Có bình luận tiêu cực/khiếu nại, cần cách xử lý bình tĩnh, đúng chính sách.
- Cuối tuần muốn tổng hợp khách hỏi gì nhiều để sửa bài viết, sản phẩm, ưu đãi.

**Không dùng khi:** xây Fanpage mới từ đầu (ảnh bìa, phần giới thiệu, định vị) → dùng `/ts-xay-dung-fanpage`;
cần lịch nội dung đa kênh cả tháng → `/ts-lich-noi-dung`; chăm khách qua Zalo → `/ts-cham-soc-khach-zalo`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md`, `05-muc-tieu-quy-tac-lien-he.md` (giờ trực, thông tin liên hệ, ai chốt đơn);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `cham-soc-fanpage` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

## Quy trình AI thực hiện

### Bước 1 — Chốt phạm vi và xem hiện trạng Fanpage
Chỉ hỏi phần Bộ Não chưa có, mỗi câu kèm gợi ý chọn nhanh:
- Mục tiêu 30 ngày tới? (A) Tăng tin nhắn hỏi mua · (B) Tăng tương tác, người theo dõi · (C) Chăm khách cũ mua lại · (D) Xử lý nhiều bình luận tiêu cực.
- Nguồn lực: mấy người làm, mỗi tuần làm được mấy bài? Ai trực tin nhắn, giờ nào?
- Đã kết nối Fanpage với AI chưa? (có/không — không biết thì coi là chưa).

Xem hiện trạng:
- Có kết nối đọc → lấy 10–20 bài gần nhất và bình luận: chủ đề nào được tương tác, câu hỏi nào lặp lại, bình luận nào chưa trả lời.
- Không có kết nối → nhờ học viên chụp 5 bài gần nhất và dán 10–20 câu khách hay hỏi (copy từ hộp thư).
- Chỉ dùng dữ liệu khách cần cho việc phân loại; không chép số điện thoại, địa chỉ khách vào kế hoạch.

### Bước 2 — Trụ cột nội dung và lịch đăng
Chia nội dung theo 6 trụ cột (tỉ lệ là gợi ý, chỉnh theo mục tiêu ở Bước 1):

| Trụ cột | Mục đích | Tỉ lệ gợi ý | Ví dụ (tiệm bánh Mây — giả định) |
|---|---|---|---|
| Nhận biết | Người lạ biết tới mình | 20% | Video 15 giây hậu trường làm bánh |
| Giáo dục | Khách hiểu cách chọn, cách dùng | 25% | "3 lỗi khiến bánh kem chảy khi mang đi" |
| Tương tác | Khách bình luận, chia sẻ | 15% | Bình chọn mẫu bánh tháng tới |
| Bằng chứng | Khách tin | 15% | Ảnh khách nhận bánh (đã xin phép) |
| Chuyển đổi | Khách nhắn tin đặt hàng | 15% | Menu tuần + cách đặt |
| Chăm sóc sau mua | Khách quay lại | 10% | Cách bảo quản, ưu đãi khách cũ (nếu có) |

Số bài theo nguồn lực (gợi ý): 1 người làm bán thời gian → 3 bài/tuần; 1 người toàn thời gian → 5–7 bài/tuần.
Lịch đăng mỗi dòng phải đủ cột:

| Ngày | Trụ cột | Chủ đề | Định dạng | Hook (câu mở đầu) | CTA | Người phụ trách | KPI |
|---|---|---|---|---|---|---|---|
| T2 | Giáo dục | Bảo quản bánh kem | Ảnh + chữ | "Bánh kem để tủ lạnh ngăn nào mới đúng?" | Lưu bài | Lan | 30 lượt lưu |

Kiểm tra lặp: không có 2 bài cùng chủ đề hoặc cùng hook trong 14 ngày; không đăng 2 bài "chuyển đổi" liền nhau.
Cần kịch bản video chi tiết → `/ts-kich-ban-reels`; cần bài bán hàng dài → `/ts-viet-bai-ban-hang`.

### Bước 3 — Thư viện câu trả lời mẫu
Soạn mẫu cho 8 nhóm: hỏi giá · địa chỉ/giờ mở cửa · lịch/còn hàng/còn chỗ · giao hàng/thanh toán · bảo hành/đổi trả ·
phản đối (đắt, để suy nghĩ) · khiếu nại · spam/quấy rối. Mỗi mẫu có 2 bản:
- **Trả lời bình luận công khai** (1–2 câu, lịch sự, mời nhắn tin — không chỉ ghi cộc lốc "ib").
- **Tin nhắn riêng** (đầy đủ thông tin, có câu hỏi mở để tư vấn tiếp).

Ví dụ (tiệm bánh Mây — giả định):
> Bình luận: "Dạ Mây cảm ơn chị ạ! Mây vừa nhắn chị bảng giá và mẫu mới nhất, chị xem tin nhắn giúp Mây nha!"
> Tin nhắn: "Dạ chào chị {tên}, bánh sinh nhật bên Mây có giá từ [CẦN BỔ SUNG: giá] tùy size. Chị đặt cho mấy người
> ăn và cần nhận ngày nào để Mây gợi ý mẫu hợp nhất ạ?"

Quy tắc soạn mẫu:
- Giá, ưu đãi, chính sách đổi trả, bảo hành **chỉ lấy từ hồ sơ** (`02-san-pham-dich-vu.md`, `05-muc-tieu-quy-tac-lien-he.md`). Thiếu thì ghi `[CẦN BỔ SUNG: …]`, không tự đặt.
- Giọng và cách xưng hô theo `04-thuong-hieu-noi-dung.md`. Không giả danh chủ shop khi trả lời bằng AI.
- Có biến cá nhân hóa `{tên}`, `{sản phẩm}` để nhân viên thay nhanh.
- Mẫu xử lý phản đối chi tiết hơn → `/ts-xu-ly-tu-choi`.

### Bước 4 — Phân loại bình luận/tin nhắn và quy tắc chuyển
| Nhóm | Dấu hiệu | Rủi ro | Phản hồi trong (gợi ý) | Ai xử lý | Việc tiếp theo |
|---|---|---|---|---|---|
| CẦN THÔNG TIN | Hỏi giá, địa chỉ, giờ | Thấp | 15 phút giờ trực | Mẫu/AI nháp | Gửi mẫu + câu hỏi mở |
| TIỀM NĂNG | Hỏi ngày nhận, số lượng, xin số tài khoản | Trung bình | 5–15 phút | Người bán | Chuyển sales, ghi CRM |
| CẦN NGƯỜI XỬ LÝ | Câu hỏi lạ, ngoài mẫu, đơn lớn | Trung bình | 30 phút | Chủ shop | Không trả lời bằng mẫu |
| KHIẾU NẠI | Chê chất lượng, giao trễ, đòi hoàn tiền | Cao | Càng sớm càng tốt | Chủ shop | Xin lỗi + chuyển tin nhắn riêng |
| RÁC | Quảng cáo lạ, link độc, chửi bới | Thấp | Không cần | Quản trị | Ẩn theo quy tắc đã duyệt |

Ghi chú CRM tối thiểu cho mỗi khách tiềm năng: Ngày · Kênh · Tên hiển thị · Nhu cầu · Nhóm · Bước tiếp theo ·
Người phụ trách · Trạng thái. Muốn thành file quản lý khách → `/ts-bang-tinh-excel`.

### Bước 5 — Cài trả lời tự động có sẵn của Meta (tùy chọn, không cần code)
Trong Meta Business Suite → **Hộp thư** → **Tự động hóa** (tên mục có thể đổi theo phiên bản) thường có:
- **Trả lời tức thì**: chào khách khi nhắn lần đầu.
- **Tin nhắn vắng mặt**: báo giờ trực khi ngoài giờ.
- **Câu hỏi thường gặp**: 3–4 nút hỏi nhanh (giá, địa chỉ, giao hàng…).
- **Trả lời theo từ khóa / bình luận** (nếu tài khoản có).

AI soạn sẵn nội dung cho từng mục từ thư viện ở Bước 3. Học viên tự dán vào, hoặc AI cài giúp khi đã kết nối và được duyệt.
Lưu ý chính sách Messenger: sau 24 giờ kể từ tin nhắn cuối của khách, Trang bị giới hạn gửi tin chủ động —
kiểm tra quy định hiện hành trước khi lên kế hoạch nhắn lại khách cũ.

### Bước 6 — Cổng duyệt trước khi đăng hoặc gửi
- Luôn trình bản nháp (bài đăng, câu trả lời) và chờ người dùng gõ **"duyệt"**.
- Chỉ trả lời tự động khi người dùng đã duyệt **phạm vi** cụ thể, ghi rõ: dùng mẫu nào, cho nhóm nào (vd chỉ "CẦN THÔNG TIN"), trong khung giờ nào.
- Không tự xóa bình luận, ẩn/chặn người dùng hoặc gửi tin hàng loạt nếu chưa nằm trong phạm vi đã duyệt.

### Bước 7 — Tổng hợp insight cuối tuần
Từ bình luận/tin nhắn trong tuần (kết nối đọc hoặc ảnh chụp học viên gửi), lập bảng:
- Top 5 câu hỏi lặp lại → bổ sung vào FAQ.
- Top 3 phản đối/lý do chưa mua → gợi ý sửa offer hoặc làm bài giải đáp.
- Từ ngữ khách hay dùng (giữ nguyên câu chữ) → dùng làm hook cho bài sau.
- Bài tốt nhất/kém nhất tuần và giả thuyết vì sao.
- 3 việc đề xuất cho tuần sau (nội dung, ưu đãi, FAQ).

### Checklist chất lượng trước khi giao
- [ ] Lịch đăng đủ cột Chủ đề, Định dạng, Hook, CTA, Người phụ trách, KPI; không lặp chủ đề trong 14 ngày.
- [ ] Mọi giá, ưu đãi, chính sách trong mẫu trả lời đều có trong hồ sơ, hoặc ghi `[CẦN BỔ SUNG]`.
- [ ] Mỗi nhóm phân loại có người xử lý và thời gian phản hồi.
- [ ] Khiếu nại luôn chuyển người thật, không trả lời bằng mẫu tự động.
- [ ] Không có dữ liệu cá nhân của khách trong file kế hoạch.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước (5 phút):** link Fanpage; 10–20 câu khách hay hỏi (copy từ hộp thư); bảng giá và chính sách
đổi trả/giao hàng; giờ trực tin nhắn; tên người chốt đơn.

1. Gõ `/ts-cham-soc-fanpage` kèm 1 câu mô tả, ví dụ: "lên kế hoạch chăm Fanpage tiệm bánh tháng này".
2. Trả lời các câu hỏi AI đưa ra (có gợi ý A-B-C-D thì chỉ cần gõ chữ cái).
3. Xem lịch nội dung. Muốn sửa thì nói bằng lời: "bớt bài bán hàng", "thêm video", "tuần này bận, chỉ 3 bài".
4. Xem thư viện câu trả lời. Điền các chỗ `[CẦN BỔ SUNG]` (giá, phí ship…) rồi đọc thử xem giọng đã giống mình chưa.
5. Gõ **"duyệt"** để AI hoàn tất và lưu vào Bộ Não.
6. Mở Meta Business Suite → Hộp thư → Tự động hóa, dán các mẫu AI đã soạn (hoặc để AI làm giúp nếu đã kết nối).
7. Cuối tuần gõ `/ts-cham-soc-fanpage tổng hợp tuần` và dán/chụp các bình luận, tin nhắn đáng chú ý để nhận insight.

## Câu lệnh mẫu
- `/ts-cham-soc-fanpage lên lịch 4 tuần cho Fanpage shop quần áo trẻ em, mỗi tuần 4 bài, ưu tiên tăng tin nhắn`
- `/ts-cham-soc-fanpage soạn bộ câu trả lời mẫu cho spa Hồng: hỏi giá, đặt lịch, khách chê đắt, khách phàn nàn`
- `/ts-cham-soc-fanpage khách bình luận chê khóa học quay video bằng điện thoại không như quảng cáo, gợi ý cách trả lời`
- `/ts-cham-soc-fanpage tổng hợp tuần: đây là 20 tin nhắn khách hỏi tiệm bánh Mây tuần qua [dán vào]`

## Kết quả nhận được
- Bảng trụ cột nội dung và lịch đăng 2–4 tuần (đủ hook, CTA, người phụ trách, KPI).
- Thư viện câu trả lời mẫu 8 nhóm (bản bình luận công khai + bản tin nhắn riêng).
- Bảng phân loại 5 nhóm, thời gian phản hồi, người xử lý và mẫu ghi chú CRM.
- Nội dung cài sẵn cho Trả lời tức thì, Tin nhắn vắng mặt, Câu hỏi thường gặp.
- (Hằng tuần) Báo cáo insight: câu hỏi, phản đối, ngôn ngữ khách và 3 việc nên làm.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-cham-soc-fanpage-<chu-de-khong-dau>/`.
2. Lưu kế hoạch chăm sóc Fanpage (trụ cột, lịch đăng, bảng phân loại, quy tắc chuyển sales, phạm vi tự động đã duyệt) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-cham-soc-fanpage
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ, vd fanpage, cham-soc-khach, faq>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `lich-dang.csv`, `thu-vien-tra-loi.md`, `insight-tuan.md`.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-cham-soc-fanpage · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Thư viện câu trả lời đã duyệt là tri thức dùng lâu dài: đề xuất lưu thêm bản vào `02-kien-thuc/khach-hang/cau-hoi-thuong-gap.md`; insight về nỗi lo/ngôn ngữ khách khác với `01-ho-so/03-khach-hang-muc-tieu.md` thì đề xuất cập nhật — luôn hỏi trước khi ghi đè.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Luôn hiển thị bản nháp trước khi đăng hoặc gửi, trừ khi người dùng đã duyệt mẫu và phạm vi tự động hóa cụ thể.
- Không tranh cãi với khách, không giả danh người dùng, không hứa ưu đãi hoặc bồi thường ngoài chính sách.
- Không tự xóa bình luận, ẩn/chặn người dùng hoặc gửi tin nếu hành động đó chưa nằm trong phạm vi được duyệt.
- Không thu thập hoặc tiết lộ dữ liệu khách không cần thiết; không đăng thông tin khách lên bình luận công khai.
- Ảnh/feedback khách chỉ dùng khi đã xin phép. Không bịa đánh giá, số lượng khách, "chỉ còn 2 suất" khi không đúng.
- Không xin mật khẩu Facebook, mã đăng nhập hay token trong chat; kết nối Fanpage làm qua `/ts-ket-noi-ung-dung`.

## Skill liên quan
- Trước: `/ts-xay-dung-fanpage`, `/ts-lich-noi-dung` · Sau: `/ts-xu-ly-tu-choi`, `/ts-cham-soc-khach-zalo`, `/ts-tu-dong-hoa-meta`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
