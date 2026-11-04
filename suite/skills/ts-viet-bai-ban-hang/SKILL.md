---
name: ts-viet-bai-ban-hang
description: "Gọi bằng /ts-viet-bai-ban-hang. Viết bài bán hàng chuyển đổi cho sản phẩm/dịch vụ của bạn theo 5 dạng: bài kéo tin nhắn, bài thông báo mở bán/ra mắt/sự kiện, bài trả lời băn khoăn của khách, câu chuyện khách hàng, bài so sánh gói. Đúng giọng thương hiệu, có CTA rõ. Dùng khi cần bài đăng chốt đơn, mở bán, khai trương, khách còn phân vân. Từ khóa: viết bài bán, bài kéo inbox, bài mở bán, bài khai giảng, xử lý phản đối, case study khách hàng, bài chốt đơn, bài so sánh gói."
---

# /ts-viet-bai-ban-hang — Viết bài bán hàng chuyển đổi

> Viết bài đăng mạng xã hội nhằm một mục tiêu: biến người đọc thành người nhắn tin, đăng ký, đặt hàng.
> 5 dạng bài có sẵn khung, AI điền bằng sản phẩm, giá, khách hàng và giọng văn trong hồ sơ của bạn.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Cần bài kéo khách nhắn tin / đăng ký tư vấn.
- Sắp mở bán, ra mắt sản phẩm, khai trương, mở lớp, tổ chức sự kiện — cần bài thông báo.
- Khách hay băn khoăn (đắt, sợ không hợp, chưa có thời gian…) — cần bài trả lời trước băn khoăn.
- Có khách hàng có kết quả thật — muốn viết thành câu chuyện khách hàng.
- Có nhiều gói/hình thức (cơ bản/nâng cao, online/tại chỗ…) — cần bài so sánh giúp khách chọn.

**Không dùng khi:** cần trang bán hàng dài trên web → `/ts-trang-ban-hang`; cần nội dung quảng cáo ngắn
để chạy ads → `/ts-viet-quang-cao`; cần kịch bản video → `/ts-kich-ban-reels`; cần lời thoại trả lời từng
khách khi nhắn tin → `/ts-xu-ly-tu-choi`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `viet-bai-ban-hang` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

Thêm cho skill này: đọc `02-kien-thuc/khach-hang/` (băn khoăn của khách) và kết quả `…-xu-ly-tu-choi-…`,
`…-dinh-gia-offer-…` nếu có — dùng đúng giá, quà tặng, bảo hành đã chốt.

## Quy trình AI thực hiện

### Bước 1 — Chọn dạng bài
Hỏi (nếu người dùng chưa nói rõ):
> "Bạn cần dạng bài nào?
> A. Kéo tin nhắn / đăng ký tư vấn · B. Thông báo mở bán / ra mắt / sự kiện · C. Trả lời băn khoăn của khách ·
> D. Câu chuyện khách hàng · E. So sánh các gói / hình thức"

### Bước 2 — Hỏi phần còn thiếu (gộp 1 lần)
Tùy dạng bài, chỉ hỏi những gì hồ sơ chưa có: sản phẩm/gói nào; giá và ưu đãi **thật** (hạn chót, số
suất); ngày/giờ/địa điểm hoặc link (dạng B); băn khoăn cụ thể (dạng C); thông tin khách thật và việc khách
đồng ý chia sẻ (dạng D); kênh đăng (Fanpage, Zalo, TikTok, nhóm).

### Bước 3 — Viết theo khung của dạng bài
Đọc khung chi tiết + ví dụ ở `references/khung-5-dang-bai.md`. Tóm tắt:

**A. Kéo tin nhắn (150–250 từ)** — Hook nỗi đau → Khuếch đại (không giải quyết thì mất gì) → Giải pháp
(sản phẩm giúp làm được gì cụ thể) → Bằng chứng (1 câu khách thật nếu có) → CTA nhắn tin.

**B. Thông báo mở bán / ra mắt / sự kiện (200–350 từ)** — Tên + ngày (rõ, nổi bật) → Nhận được gì
(5–7 điểm) → Dùng xong làm được gì ngay → Thông tin thực tế (địa điểm/link/giờ/giao hàng) → Giá + ưu đãi +
hạn chót (chỉ khi có thật) → CTA + link/nhắn tin.

**C. Trả lời băn khoăn (100–200 từ, 1 băn khoăn/bài hoặc tổng hợp)** — Nhắc lại băn khoăn bằng lời của khách
→ Đồng cảm ("nhiều người cũng nghĩ vậy") → Câu trả lời thật + bằng chứng → CTA. Tự rút danh sách băn khoăn
theo phương pháp trong references.

**D. Câu chuyện khách hàng (200–300 từ)** — Ai (nghề/hoàn cảnh, ẩn tên nếu cần) → Trước (vấn đề cụ thể) →
Dùng gì, bao lâu → Sau (kết quả, có số càng tốt) → Lời khách (nguyên văn) → CTA "Bạn muốn kết quả tương tự?".
**Chỉ viết từ thông tin thật người dùng cung cấp.**

**E. So sánh gói / hình thức** — Bảng so sánh (giá, thời gian, nhận được gì, phù hợp với ai) → Kết luận
"ai nên chọn gói nào" → CTA.

### Bước 4 — Hoàn thiện theo giọng thương hiệu
- Xưng hô, người đại diện, CTA, hashtag theo `04-thuong-hieu-noi-dung.md`. Chưa có → dùng
  `references/mau-giong-thuong-hieu.md` và hỏi 3 câu nhanh (người đại diện, xưng hô, 3 tính từ).
- Kết bài luôn có **1 CTA** + 5–8 hashtag. Thông tin liên hệ (số điện thoại, link) lấy từ
  `05-muc-tieu-quy-tac-lien-he.md`; chưa có → `[CẦN BỔ SUNG: số điện thoại / link]`.
- Đưa **2 phương án hook** để người dùng chọn.

### Bước 5 — Cổng duyệt
Trình bài + 2 hook. Sửa theo yêu cầu ("ngắn lại", "giọng vui hơn", "thêm ưu đãi") đến khi người dùng gõ
**"duyệt"**. Gợi ý: muốn chạy quảng cáo cho bài này → `/ts-len-camp-facebook`; cần ảnh → `/ts-thiet-ke-anh-quang-cao`.

### Checklist chất lượng (AI tự kiểm trước khi trình)
- [ ] Hook chạm đúng nỗi đau/mong muốn của khách trong hồ sơ, ≤ 2 dòng.
- [ ] Nói kết quả khách nhận được, không chỉ liệt kê tính năng.
- [ ] Đúng giá, ưu đãi, ngày trong hồ sơ / người dùng cung cấp — không tự nghĩ ra.
- [ ] Không có lời khen, số liệu, khan hiếm bịa; thiếu thì `[CẦN BỔ SUNG: …]`.
- [ ] Không lời hứa tuyệt đối ("đảm bảo", "100%", "chắc chắn").
- [ ] Đúng độ dài của dạng bài; đúng 1 CTA.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** tên sản phẩm/gói, giá, ưu đãi đang có (nếu có), ngày mở bán/sự kiện; nếu viết câu
chuyện khách thì chuẩn bị tin nhắn/ảnh khách gửi và xin phép khách trước.
1. Gõ `/ts-viet-bai-ban-hang` kèm 1 câu, vd "bài thông báo khai trương chi nhánh 2 ngày 20/12".
2. Chọn dạng bài A–E nếu AI hỏi.
3. Trả lời các câu AI hỏi về giá, ưu đãi, ngày — chỉ đưa thông tin thật.
4. Chọn 1 trong 2 hook AI đưa.
5. Sửa bằng lời ("bớt emoji", "thêm phần giao hàng miễn phí").
6. Gõ **"duyệt"** để AI chốt bài và lưu vào Bộ Não.
7. Copy bài để đăng, hoặc gõ `/ts-len-camp-facebook` để chạy quảng cáo cho bài.

## Câu lệnh mẫu
- `/ts-viet-bai-ban-hang bài kéo tin nhắn cho dịch vụ dọn nhà theo giờ, khách là gia đình bận rộn`
- `/ts-viet-bai-ban-hang thông báo mở lớp luyện thi IELTS online khai giảng 5/1, học phí ưu đãi đến 25/12`
- `/ts-viet-bai-ban-hang bài trả lời băn khoăn 'mỹ phẩm handmade có an toàn không' cho shop của tôi`
- `/ts-viet-bai-ban-hang câu chuyện khách hàng: chị Hà giảm 6kg sau 2 tháng tập ở phòng gym, có ảnh trước sau`
- `/ts-viet-bai-ban-hang so sánh gói chụp ảnh cưới cơ bản và cao cấp giúp khách dễ chọn`

## Kết quả nhận được
- 1 bài (hoặc bộ bài) hoàn chỉnh theo đúng dạng, sẵn copy để đăng.
- 2 phương án hook để chọn.
- Gợi ý ảnh đi kèm (1 dòng mô tả) và bước tiếp theo (đăng / chạy quảng cáo).

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-viet-bai-ban-hang-<chu-de-khong-dau>/`.
2. Lưu bài bán hàng đã duyệt (ghi rõ dạng bài A–E, kênh đăng, hook đã chọn và hook dự phòng) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-viet-bai-ban-hang
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `bai-phu.md` (các bài khác trong cùng bộ, vd chuỗi bài trả lời băn khoăn).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-viet-bai-ban-hang · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Danh sách băn khoăn của khách + câu trả lời đã duyệt là tri thức dùng lại: đề xuất lưu/cập nhật `02-kien-thuc/khach-hang/bang-khoan-thuong-gap.md`. Câu chuyện khách thật (đã được khách đồng ý) đề xuất lưu vào `02-kien-thuc/khach-hang/cau-chuyen-khach-hang.md`. Hỏi trước khi ghi.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không bịa lời khen, số liệu, ảnh trước/sau, số suất còn lại, hạn ưu đãi.
- Câu chuyện khách hàng: chỉ đăng khi khách đồng ý; ẩn tên/ảnh nếu khách muốn.
- Tránh lời hứa tuyệt đối và so sánh hạ thấp đối thủ — dễ bị Facebook từ chối, mất uy tín.
- Ngành nhạy cảm (y tế, thẩm mỹ, thực phẩm chức năng, tài chính, bất động sản): nhắc kiểm tra quy định quảng cáo.

## Skill liên quan
- Trước: `/ts-lich-noi-dung` · `/ts-dinh-gia-offer` · `/ts-chan-dung-khach-hang` · `/ts-xu-ly-tu-choi`
- Sau: `/ts-thiet-ke-anh-quang-cao` · `/ts-len-camp-facebook` · `/ts-cham-soc-khach-zalo` · `/ts-email-cham-soc`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
