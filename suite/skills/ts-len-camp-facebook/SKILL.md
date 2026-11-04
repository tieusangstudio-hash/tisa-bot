---
name: ts-len-camp-facebook
description: "Gọi bằng /ts-len-camp-facebook. Dựng chiến dịch quảng cáo Facebook kéo tin nhắn Messenger qua công cụ Meta Ads đã kết nối: chọn đúng tài khoản quảng cáo và Page, tạo chiến dịch, nhóm quảng cáo, mẫu quảng cáo ở trạng thái TẠM DỪNG, xem trước, báo cáo — chỉ bật chạy khi bạn gõ 'duyệt'. Ngân sách mặc định 200.000–500.000đ/ngày. Dùng khi muốn chạy ads kéo inbox. Từ khóa: chạy quảng cáo, lên camp, chạy ads kéo inbox, tạo chiến dịch Facebook, quảng cáo Messenger, dựng campaign, lên QC tự động."
---

# /ts-len-camp-facebook — Lên chiến dịch quảng cáo Facebook kéo tin nhắn

> AI dựng sẵn chiến dịch quảng cáo Facebook đưa khách bấm "Gửi tin nhắn" vào Messenger của Page bạn.
> Mọi thứ được tạo ở trạng thái **TẠM DỪNG (PAUSED) — chưa tốn đồng nào**. AI báo cáo, bạn xem trước,
> chỉ khi bạn gõ **"duyệt"** AI mới bật chạy.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Có bài viết + hình, muốn chạy quảng cáo để khách nhắn tin hỏi mua / đăng ký tư vấn.
- Muốn AI dựng đủ cấu trúc chiến dịch → nhóm quảng cáo → mẫu quảng cáo, khỏi tự mò Trình quản lý quảng cáo.
- Đã có bảng (Google Sheets / Excel) liệt kê nhiều quảng cáo cần lên.
- Đã chạy 24–48 giờ, muốn xem nhanh chi phí mỗi tin nhắn và nên tăng/giảm/tắt camp nào.

**Không dùng khi:** chỉ đăng bài thường (không trả tiền) → `/ts-noi-dung-tu-dong-7-ngay`; chỉ cần viết nội dung
quảng cáo → `/ts-viet-quang-cao`; phân tích sâu số liệu nhiều chiến dịch → `/ts-bao-cao-facebook-ads`;
cài quy tắc tự động, Pixel → `/ts-tu-dong-hoa-meta`; quảng cáo TikTok → `/ts-chay-tiktok-ads`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `len-camp-facebook` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

Thêm cho skill này, lấy từ `05-muc-tieu-quy-tac-lien-he.md`: **ID tài khoản quảng cáo, ID Page, khoảng ngân sách,
KPI (vd chi phí/tin nhắn mong muốn), khu vực bán hàng**. Từ `03-khach-hang-muc-tieu.md`: tuổi, giới tính, sở thích,
khu vực của khách. Đọc thêm kết quả `…-viet-quang-cao-…`, `…-viet-bai-ban-hang-…` nếu có để lấy nội dung.

## Quy trình AI thực hiện

### ⛔ Nguyên tắc an toàn — đọc trước, KHÔNG BAO GIỜ vi phạm
1. **KHÔNG tự bật chạy.** AI chỉ tạo mọi thứ ở trạng thái **PAUSED**. Bật chạy (tiêu tiền thật) chỉ khi người
   dùng nói rõ "duyệt" / "chạy đi" / "ok bật". Trước khi bật, đọc lại **tài khoản, ngân sách/ngày, đối tượng**
   một lần nữa.
2. **Luôn báo cáo trước khi xin duyệt:** tên chiến dịch, mục tiêu, đối tượng, ngân sách/ngày, xem trước. Không
   bao giờ bật "âm thầm".
3. **Ngân sách mặc định 200.000–500.000đ/ngày/chiến dịch.** Người dùng nhập số ngoài khoảng này hoặc quên
   nhập → **HỎI LẠI** trước khi tạo. Không tự nâng ngân sách.
4. **Nhập đúng đơn vị tiền:** kiểm tra tiền tệ của tài khoản. Tài khoản **VND** → nhập số đồng nguyên
   (200k → `200000`, 500k → `500000`). Tài khoản tiền tệ khác (vd USD) → báo người dùng, hỏi lại số tiền
   theo đúng tiền tệ đó, không tự quy đổi. Mức tối thiểu Meta cho phép khoảng 26.500đ/ngày (có thể thay đổi).
5. **Chỉ dùng tài khoản quảng cáo đang hoạt động** (ACTIVE). Tài khoản bị vô hiệu hóa/hạn chế → không dùng, báo người dùng.
6. Không xin mật khẩu Facebook, mã OTP, token, số thẻ trong chat. Không đổi phương thức thanh toán.

### Bước 1 — Kiểm tra kết nối và chọn đúng tài khoản
1. Kiểm tra môi trường có **công cụ Meta Ads đã kết nối** không. Chưa có → dừng, đưa hướng dẫn ở
   `references/huong-dan-ket-noi-meta-ads.md`, đề nghị: trong lúc chờ, AI soạn sẵn nội dung + đối tượng + ngân
   sách để người dùng tự lên camp.
2. **Có ID trong hồ sơ** → dùng công cụ đọc thông tin tài khoản đó, xác nhận: tên, trạng thái ACTIVE, tiền tệ.
   Page: xác nhận tên Page đúng.
3. **Chưa có ID** → dùng công cụ liệt kê **tài khoản quảng cáo** (tên, ID, trạng thái, tiền tệ) và **Page**
   người dùng quản lý; trình bảng, cho người dùng chọn. Loại khỏi danh sách tài khoản không ACTIVE (ghi chú lý do).
4. Sau khi chọn: đề xuất **ghi lại ID tài khoản quảng cáo + ID Page + tiền tệ** vào `05-muc-tieu-quy-tac-lien-he.md`
   để lần sau không phải chọn lại (hỏi trước khi ghi).

### Bước 2 — Lấy nguyên liệu (nội dung + hình)
Nguồn tốt nhất: **1 bảng "Bảng điều khiển quảng cáo"** (Google Sheets/Excel), mỗi dòng = 1 quảng cáo:

| Cột | Mô tả |
|---|---|
| Tên camp | vd `TenThuongHieu_SanPham_Messenger_T12` |
| Nội dung chính | Hook + Thân + CTA (xem `references/mau-noi-dung-quang-cao.md`) |
| Tiêu đề | Câu ngắn dưới ảnh |
| Đối tượng | Bộ đối tượng A/B/C (xem `references/bo-doi-tuong-mau.md`) |
| Ngân sách/ngày | 200000–500000 |
| Hình | Ảnh đã có trên tài khoản quảng cáo / link ảnh / ID bài đăng có sẵn |
| Tin nhắn chào | Câu Messenger tự gửi khi khách bấm |
| Trạng thái | Chờ tạo / Đã tạo (PAUSED) / Đã duyệt / Đang chạy |

- Chưa có bảng → nhận nội dung + hình ngay trong chat (hoặc đề nghị tạo bảng nếu có công cụ bảng tính).
- Nội dung thiếu hook/CTA → tự bổ sung theo `references/mau-noi-dung-quang-cao.md`, giọng theo
  `04-thuong-hieu-noi-dung.md`, cho người dùng xem trước khi tạo.
- Thiếu ngân sách hoặc ngoài 200.000–500.000đ → hỏi lại (nguyên tắc 3).

**Xử lý hình (chỗ hay vướng):**
1. **Tốt nhất:** dùng ảnh đã có sẵn trên tài khoản quảng cáo (lấy mã ảnh — *image hash*).
2. **Hoặc:** quảng cáo bằng bài đã đăng sẵn trên Page (khỏi tải ảnh mới).
3. **Hoặc:** nếu công cụ có chức năng tải ảnh lên thì thử tải; lỗi thì hướng dẫn người dùng tải ảnh 1 lần vào
   *Trình quản lý quảng cáo → Thư viện phương tiện (Media library)* rồi AI lấy mã ảnh.

### Bước 3 — Dựng cấu trúc chiến dịch (TẤT CẢ ở trạng thái PAUSED)
Đọc mô tả từng chức năng của công cụ Meta Ads để điền đúng tên trường. Giá trị mặc định cho camp kéo tin nhắn:
1. **Chiến dịch (campaign):** mục tiêu `OUTCOME_LEADS` (hoặc mục tiêu tin nhắn tương đương mà công cụ hỗ trợ) ·
   trạng thái `PAUSED` · danh mục đặc biệt `[]` — **trừ khi** quảng cáo về nhà ở/bất động sản, tuyển dụng,
   tín dụng/vay, vấn đề xã hội/chính trị: hỏi người dùng và khai báo đúng danh mục Meta yêu cầu.
2. **Nhóm quảng cáo (ad set):** trạng thái `PAUSED` · điểm đến `MESSENGER` · đối tượng được quảng bá = ID Page
   đã chọn · tối ưu cho `CONVERSATIONS` (cuộc trò chuyện) · tính phí theo `IMPRESSIONS` · ngân sách ngày = số
   tiền nguyên theo đúng tiền tệ · đối tượng theo bộ A/B/C đã chọn · vị trí hiển thị tự động (Advantage+).
3. **Mẫu quảng cáo (creative):** ID Page đã chọn · nội dung chính + mã ảnh + tiêu đề · nút `MESSAGE_PAGE`
   (Gửi tin nhắn) · kèm tin nhắn chào nếu công cụ cho phép.
4. **Quảng cáo (ad):** gắn mẫu quảng cáo vào nhóm quảng cáo · trạng thái `PAUSED`.

Lỗi ở bước nào → đọc thông báo lỗi, sửa đúng trường đó, tạo lại; **không** bật chạy để "thử".

### Bước 4 — Xem trước
Dùng chức năng xem trước quảng cáo của công cụ (bảng tin di động + Messenger). Lỗi (ảnh vỡ, sai chữ tiếng Việt,
thiếu nút) → sửa mẫu quảng cáo, xem trước lại.

### Bước 5 — Kiểm tra 10 mục + báo cáo xin duyệt
Chạy `references/checklist-truoc-khi-duyet.md`; còn mục chưa đạt thì sửa, không xin duyệt. Rồi trình:
```
✅ Đã dựng xong (đang TẠM DỪNG — chưa tốn tiền):
• Tài khoản: <tên> (<tiền tệ>) · Page: <tên Page>
• Chiến dịch: <tên> | Mục tiêu: Tin nhắn Messenger
• Đối tượng: <tóm tắt>
• Ngân sách: <X>đ/ngày
• Xem trước: <link/ảnh>
👉 Bạn duyệt chạy không? Gõ "duyệt" để tôi bật.
```

### Bước 6 — Sau khi người dùng gõ "duyệt" → bật và theo dõi
1. Đọc lại tài khoản + ngân sách/ngày + đối tượng lần cuối, rồi bật (activate) **chiến dịch, nhóm quảng cáo, quảng cáo** vừa tạo.
2. Cập nhật cột Trạng thái trong bảng → "Đang chạy" (nếu có quyền ghi).
3. Sau 24–48 giờ, khi người dùng hỏi: dùng chức năng xem hiệu quả/xu hướng của công cụ, báo cáo
   **chi phí/1.000 lượt hiển thị (CPM), tỷ lệ bấm (CTR), số tin nhắn, chi phí/tin nhắn**, so với KPI trong hồ sơ,
   gợi ý camp nên giữ/giảm/tắt. **Mọi thay đổi ngân sách hoặc tắt camp cũng phải chờ "duyệt".**
   Phân tích sâu hơn → `/ts-bao-cao-facebook-ads`.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước (làm 1 lần):**
- Có tài khoản quảng cáo đang hoạt động, đã gắn phương thức thanh toán, và bạn là quản trị viên Page.
- Kết nối Meta Ads vào AI: vào phần **Kết nối / Connectors** của ứng dụng AI → **thêm Meta Ads** →
  **đăng nhập Facebook** → **cấp quyền tài khoản quảng cáo** (và Page). Chi tiết: `references/huong-dan-ket-noi-meta-ads.md`.
- Chuẩn bị nội dung quảng cáo + 1 ảnh (hoặc bài đã đăng muốn chạy).
1. Gõ `/ts-len-camp-facebook` kèm sản phẩm cần chạy và ngân sách/ngày.
2. Chọn tài khoản quảng cáo và Page trong danh sách AI đưa (chỉ lần đầu).
3. Chọn bộ đối tượng A / B / C AI gợi ý.
4. Xem nội dung, ảnh, bản xem trước; sửa bằng lời ("đổi tiêu đề", "giảm còn 300k/ngày").
5. Kiểm tra lại báo cáo — **lúc này quảng cáo vẫn TẠM DỪNG, chưa tốn tiền**.
6. Gõ **"duyệt"** để AI bật chạy. Muốn dừng lại thì gõ "chưa", không có gì xảy ra.
7. Sau 1–2 ngày gõ "camp chạy sao rồi?" để AI báo cáo chi phí/tin nhắn.

## Câu lệnh mẫu
- `/ts-len-camp-facebook chạy quảng cáo kéo tin nhắn cho bộ sưu tập váy công sở, 300k/ngày, khách nữ 25–40 ở Hà Nội`
- `/ts-len-camp-facebook dùng bài đăng hôm qua về gói chăm sóc da để chạy ads Messenger, khu vực bán kính 5km quanh spa`
- `/ts-len-camp-facebook lên camp cho khóa học kế toán online toàn quốc, 400k/ngày, nội dung trong bảng điều khiển`
- `/ts-len-camp-facebook camp tuần trước chạy sao rồi, chi phí mỗi tin nhắn bao nhiêu?`

## Kết quả nhận được
- Chiến dịch → nhóm quảng cáo → quảng cáo đã dựng sẵn ở trạng thái TẠM DỪNG trên đúng tài khoản/Page.
- Bản xem trước quảng cáo + báo cáo gọn để duyệt.
- Sau khi duyệt: camp đang chạy; sau 24–48h có báo cáo chi phí/tin nhắn và gợi ý tối ưu.
- Nếu chưa kết nối: bộ nội dung + đối tượng + ngân sách soạn sẵn để tự lên camp.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-len-camp-facebook-<chu-de-khong-dau>/`.
2. Lưu biên bản chiến dịch (tài khoản, Page, tên + ID chiến dịch/nhóm/quảng cáo, đối tượng, ngân sách, nội dung, trạng thái, thời điểm duyệt) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-len-camp-facebook
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `bang-dieu-khien.csv` (các dòng quảng cáo), `xem-truoc.png`, `bao-cao-48h.md`.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-len-camp-facebook · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu ID tài khoản quảng cáo, ID Page, tiền tệ hoặc bộ đối tượng hiệu quả chưa có trong `01-ho-so/05-muc-tieu-quy-tac-lien-he.md`, đề xuất ghi vào và hỏi trước khi ghi đè. Có thể theo dõi chiến dịch dài hạn ở `05-du-an/`.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Nhắc lại: **không bao giờ tự bật, tự tăng ngân sách, tự tắt/xóa** quảng cáo — mọi việc tốn tiền chờ "duyệt".
- Không hứa hẹn kết quả ("chắc chắn ra đơn"); số liệu ít ngày chưa đủ kết luận — giữ ổn định 2–3 ngày rồi mới chỉnh.
- Nội dung quảng cáo tránh lời hứa tuyệt đối, ảnh trước/sau ở ngành nhạy cảm, nhắm vào đặc điểm cá nhân
  ("Bạn đang béo?") — dễ bị Meta từ chối.
- Không lưu mật khẩu, token, số thẻ vào Bộ Não. ID tài khoản/Page không phải mật khẩu, lưu được.

## Skill liên quan
- Trước: `/ts-viet-quang-cao` · `/ts-viet-bai-ban-hang` · `/ts-thiet-ke-anh-quang-cao` · `/ts-ket-noi-ung-dung`
- Sau: `/ts-bao-cao-facebook-ads` · `/ts-tu-dong-hoa-meta` · `/ts-cham-soc-khach-zalo` · `/ts-xu-ly-tu-choi`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
