---
name: ts-noi-dung-tu-dong-7-ngay
description: "Gọi bằng /ts-noi-dung-tu-dong-7-ngay. Làm trọn 7 ngày nội dung Fanpage: gợi ý chủ đề 7 ngày, viết caption, thiết kế ảnh (Canva hoặc công cụ tạo ảnh nếu có, không có thì giao prompt ảnh), rồi đăng bài khi đã kết nối Facebook và bạn duyệt từng bài — chưa kết nối thì giao bộ bài để đăng tay và hẹn giờ. Dùng khi muốn có bài đăng sẵn cả tuần. Từ khóa: content 7 ngày, gợi ý content tuần này, tạo bài đăng fanpage, thiết kế và đăng bài, autopilot content, đăng bài tự động."
---

# /ts-noi-dung-tu-dong-7-ngay — Nội dung tự động 7 ngày (gợi ý → viết → thiết kế → đăng)

> Một lệnh làm trọn tuần nội dung cho Fanpage: AI gợi ý 7 chủ đề, viết caption theo giọng thương hiệu của
> bạn, làm ảnh 1 ảnh/bài, và đăng (hoặc giao bộ bài để bạn tự đăng / hẹn giờ). Không bài nào lên mạng khi
> bạn chưa nói "duyệt".

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Muốn có đủ 7 bài (ảnh + caption) cho Fanpage trong tuần, làm một lần xong.
- Đã có lịch từ `/ts-lich-noi-dung` và muốn biến 7 ngày đầu thành bài hoàn chỉnh.
- Muốn AI thiết kế ảnh bài đăng theo màu thương hiệu.
- Đã kết nối Facebook/Meta vào AI và muốn AI đăng giúp sau khi duyệt từng bài.

**Không dùng khi:** chỉ cần kế hoạch cả tháng chưa viết bài → `/ts-lich-noi-dung`; cần bài bán hàng dài →
`/ts-viet-bai-ban-hang`; cần kịch bản video → `/ts-kich-ban-reels`; cần chạy quảng cáo trả phí → `/ts-len-camp-facebook`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `01-ho-so-doanh-nghiep.md`, `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `noi-dung-tu-dong-7-ngay` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

Thêm cho skill này: tìm trong `04-ket-qua/` thư mục `…-lich-noi-dung-…` gần nhất — nếu có lịch tuần đang
chạy thì dùng luôn 7 ngày đó làm Bước 1. Đọc `02-kien-thuc/cong-thuc/chu-de-noi-dung.md` nếu có.

## Quy trình AI thực hiện

### Bước 1 — Gợi ý 7 ngày nội dung
Nếu chưa có lịch, hỏi **đúng 1 câu**:
> "Tuần này bạn muốn tập trung vào gì? (vd: ra mắt sản phẩm mới / mẹo dùng sản phẩm / ưu đãi cuối tuần /
> câu chuyện khách hàng / xây thương hiệu)"

Tạo bảng 7 ngày:

| Ngày | Loại nội dung | Chủ đề cụ thể | Mục tiêu | Tầng phễu |
|---|---|---|---|---|
| Thứ 2 | Kiến thức / giáo dục | … | Tạo niềm tin | Nhận biết |
| Thứ 3 | Câu chuyện / khách hàng | … | Tạo cảm xúc | Quan tâm |
| Thứ 4 | Mẹo nhanh | … | Được lưu, chia sẻ | Nhận biết |
| Thứ 5 | Bán hàng nhẹ | … | Kéo tin nhắn | Cân nhắc → Mua |
| Thứ 6 | Hậu trường | … | Gần gũi | Cân nhắc |
| Thứ 7 | Giải trí / bình chọn | … | Tăng tương tác | Khách trung thành |
| Chủ nhật | Truyền cảm hứng | … | Gắn kết cộng đồng | Nhận biết |

Chủ đề lấy từ sản phẩm (`02-…`), nỗi đau khách (`03-…`) và trọng tâm tuần. Hỏi tiếp:
> "Bạn muốn làm ngày nào trước? (gõ số thứ tự, tên ngày, hoặc 'làm hết')"

### Bước 2 — Viết caption (làm trước, không cần công cụ)
Cấu trúc **Hook – Thân – CTA**:
```
[HOOK — 1 dòng gây tò mò / chạm nỗi đau, ≤ 10 chữ]

[THÂN — 3–5 ý ngắn, mỗi ý 1 dòng, emoji vừa phải]
✅ …
✅ …
✅ …

[CTA — 1 hành động cụ thể]
👇 [nhắn tin / bình luận từ khóa / đặt lịch / xem link]

#[2 hashtag thương hiệu] #[3 hashtag chủ đề]
```
Quy tắc:
- Giọng văn, cách xưng hô, CTA, hashtag lấy từ `04-thuong-hieu-noi-dung.md`. Chưa có → hỏi nhanh 3 câu
  theo `references/mau-giong-thuong-hieu.md` (người đại diện, xưng hô, 3 tính từ).
- Không dùng từ sáo rỗng: "chất lượng", "uy tín", "hàng đầu", "số 1".
- Không bịa con số, lời khen của khách, ưu đãi. Thiếu thì ghi `[CẦN BỔ SUNG: …]`.

### Bước 3 — Thiết kế ảnh (1 ảnh/bài, vuông 1080×1080 hoặc dọc 1080×1350)
Lấy **màu, phông, logo, phong cách ảnh** từ `04-thuong-hieu-noi-dung.md`. Chưa có màu → hỏi chọn 1:
A. Đen – vàng · B. Gradient tím · C. Xanh dương · D. Cam – vàng · E. Đỏ – cam · F. Trắng – cam ·
G. Tôi tự đưa mã màu.

Viết **prompt ảnh** theo mẫu ở `references/mau-prompt-anh.md` (prompt tiếng Anh, chữ trên ảnh tiếng Việt có dấu).
Rồi chọn đường đi theo công cụ đang có:
1. **Có công cụ Canva đã kết nối** → tạo thiết kế dạng bài đăng Facebook/Instagram bằng prompt trên.
2. **Có công cụ tạo ảnh khác** → tạo ảnh bằng prompt trên; kiểm tra chữ tiếng Việt không lỗi dấu.
3. **Không có công cụ nào** → giao prompt ảnh để người dùng dán vào Canva (canva.com → *Tạo thiết kế* →
   *Bài đăng Facebook* → *Magic Design*) hoặc công cụ tạo ảnh họ đang dùng; gợi ý chạy `/ts-thiet-ke-anh-quang-cao`
   nếu cần bộ ảnh kỹ hơn.

Cho xem trước và hỏi: "Ảnh này ổn chưa? Muốn chỉnh gì không?" — **không bao giờ bỏ qua bước xem trước**.

### Bước 4 — Cổng duyệt từng bài
Trình bài hoàn chỉnh: ảnh (hoặc prompt) + caption + ngày/giờ đề xuất đăng. Chờ người dùng gõ **"duyệt"**
cho **từng bài**. Sửa bao nhiêu lần cũng được.

### Bước 5 — Đăng bài hoặc giao bộ bài
**Trường hợp A — Đã kết nối Facebook/Meta có chức năng đăng bài lên Page** (hoặc công cụ lên lịch mạng xã hội):
1. Liệt kê các Page người dùng quản lý; lấy Page mặc định trong `05-muc-tieu-quy-tac-lien-he.md` nếu có;
   nhiều Page thì hỏi chọn.
2. Xác nhận lần cuối: "Sắp đăng lên **[Tên Page]** lúc **[giờ]**: caption + ảnh như trên. Đăng không?"
3. Chỉ đăng khi người dùng trả lời rõ ràng ("đăng đi", "ok", "duyệt"). Báo kết quả + link bài.
4. Hỏi: "Làm tiếp ngày nào trong 7 ngày?"

Lưu ý: nhiều kết nối Meta chỉ quản lý **quảng cáo**, không đăng bài thường. Nếu công cụ không có chức năng
đăng bài → chuyển sang Trường hợp B, nói rõ lý do, không cố thử.

**Trường hợp B — Chưa kết nối / không đăng được:** giao **bộ bài đăng tay** gồm ảnh (hoặc prompt) + caption
sẵn copy + giờ đăng gợi ý, và hướng dẫn hẹn giờ:
- Vào **business.facebook.com** (Meta Business Suite) → chọn Page → **Tạo bài viết** → dán caption,
  tải ảnh lên → bấm mũi tên cạnh **Đăng** → **Lên lịch** → chọn ngày giờ → **Lên lịch**.
- Hẹn giờ cả 7 bài trong 15 phút là xong một tuần.

### Bước 6 — Tổng kết tuần
Bảng 7 dòng: ngày · chủ đề · trạng thái (Đã đăng / Đã hẹn giờ / Chờ duyệt / Chờ ảnh) · link (nếu có).

### Checklist chất lượng (AI tự kiểm trước khi trình mỗi bài)
- [ ] Hook ≤ 10 chữ, đọc là muốn đọc tiếp.
- [ ] Đúng 1 CTA, đúng giọng và xưng hô trong hồ sơ.
- [ ] Ảnh đúng màu thương hiệu, chữ tiếng Việt đủ dấu, không quá 12 chữ trên ảnh.
- [ ] Không có số liệu, lời khen, ưu đãi bịa.
- [ ] Bài chỉ được đăng sau khi có "duyệt" cho chính bài đó.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** logo và màu thương hiệu (nếu có); ảnh sản phẩm thật bỏ vào `03-tai-lieu-tho/dinh-kem/`;
muốn AI đăng giúp thì kết nối Facebook trước: vào phần **Kết nối / Connectors** của ứng dụng AI → thêm
**Meta / Facebook** (hoặc công cụ lên lịch mạng xã hội) → đăng nhập Facebook → cấp quyền Page.
1. Gõ `/ts-noi-dung-tu-dong-7-ngay` kèm trọng tâm tuần, vd "tuần này đẩy món mới".
2. Xem bảng 7 ngày, sửa bằng lời ("thứ 7 đổi thành minigame").
3. Chọn ngày muốn làm trước (hoặc gõ "làm hết").
4. Xem caption + ảnh từng bài; sửa bằng lời ("hook mạnh hơn", "đổi nền sáng").
5. Gõ **"duyệt"** cho từng bài.
6. Nếu đã kết nối: xác nhận "đăng đi" khi AI hỏi lần cuối. Nếu chưa: tải bộ bài và hẹn giờ trên
   Meta Business Suite theo hướng dẫn AI đưa.
7. Cuối tuần gõ `/ts-phan-tich-mang-xa-hoi` để xem bài nào hiệu quả nhất.

## Câu lệnh mẫu
- `/ts-noi-dung-tu-dong-7-ngay tuần này shop thời trang của tôi ra bộ sưu tập thu đông, làm hết 7 bài`
- `/ts-noi-dung-tu-dong-7-ngay quán cà phê, tập trung kéo khách đến buổi sáng, màu nâu kem`
- `/ts-noi-dung-tu-dong-7-ngay trung tâm tiếng Anh trẻ em, tuần này mời học thử miễn phí, tôi chưa kết nối Facebook`
- `/ts-noi-dung-tu-dong-7-ngay dùng lịch tuần 2 đã lưu, làm bài thứ 2 và thứ 4 trước`

## Kết quả nhận được
- Bảng 7 ngày nội dung theo tầng phễu.
- 7 caption hoàn chỉnh (Hook – Thân – CTA + hashtag) đúng giọng thương hiệu.
- 7 ảnh (hoặc 7 prompt ảnh sẵn dán) đúng màu thương hiệu.
- Bài đã đăng / đã hẹn giờ, hoặc bộ bài đăng tay kèm hướng dẫn hẹn giờ.
- Bảng tổng kết trạng thái tuần.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-noi-dung-tu-dong-7-ngay-<chu-de-khong-dau>/`.
2. Lưu bảng 7 ngày + 7 caption đã duyệt + bảng trạng thái đăng thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-noi-dung-tu-dong-7-ngay
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `prompt-anh.md` (7 prompt ảnh), ảnh `ngay-1.png` … `ngay-7.png`, `lich-dang.csv` (ngay, gio, chu-de, trang-thai, link).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-noi-dung-tu-dong-7-ngay · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu người dùng vừa chọn màu, giọng văn, CTA hoặc Page mặc định mà hồ sơ chưa có, đề xuất ghi vào `01-ho-so/04-thuong-hieu-noi-dung.md` (màu, giọng) hoặc `01-ho-so/05-muc-tieu-quy-tac-lien-he.md` (Page) và hỏi trước khi ghi đè.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- **Không bao giờ đăng bài khi chưa có "duyệt" cho chính bài đó** và chưa xác nhận đúng Page.
- Không xin mật khẩu Facebook, mã OTP hay token trong chat — chỉ kết nối qua phần Kết nối/Connectors của ứng dụng AI.
- Công cụ thiết kế lỗi → vẫn giao prompt ảnh đầy đủ để người dùng tự làm, không bỏ dở.
- Ảnh có người thật / logo thương hiệu khác: chỉ dùng khi người dùng có quyền sử dụng.
- Ngành nhạy cảm (y tế, thẩm mỹ, tài chính): tránh hứa hẹn kết quả, nhắc kiểm tra quy định quảng cáo.

## Skill liên quan
- Trước: `/ts-lich-noi-dung` · `/ts-tao-ho-so-doanh-nghiep`
- Sau: `/ts-thiet-ke-anh-quang-cao` · `/ts-cham-soc-fanpage` · `/ts-phan-tich-mang-xa-hoi` · `/ts-len-camp-facebook`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
