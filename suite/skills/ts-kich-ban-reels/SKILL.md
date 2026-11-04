---
name: ts-kich-ban-reels
description: "Gọi bằng /ts-kich-ban-reels. Viết kịch bản video ngắn 30–90 giây cho Reels, TikTok, Shorts: hook 3 giây đầu, lời thoại theo từng cảnh, gợi ý góc quay, chữ trên màn hình, caption và hashtag — đúng giọng người đại diện của thương hiệu bạn. Dùng khi cần video mẹo, video bán hàng, câu chuyện khách hàng, thông báo dạng video, hoặc không biết hôm nay quay gì. Từ khóa: kịch bản video, script Reels, script TikTok, viết lời thoại, kịch bản 30 giây, hook video, quay video gì hôm nay."
---

# /ts-kich-ban-reels — Kịch bản video ngắn Reels / TikTok / Shorts

> Viết kịch bản video ngắn sẵn để quay bằng điện thoại: câu mở đầu giữ chân người xem, lời thoại từng cảnh
> theo giây, gợi ý cách quay, chữ hiện trên màn hình, caption và hashtag — đúng giọng người đại diện của bạn.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Cần kịch bản video 30–90 giây cho TikTok, Facebook Reels, YouTube Shorts, Instagram Reels.
- Cần hook (câu mở đầu) đủ mạnh để người xem không lướt qua.
- Muốn quay video mẹo, video bán hàng, câu chuyện khách hàng, hậu trường, thông báo ra mắt/ưu đãi.
- Không biết hôm nay quay gì — cần danh sách chủ đề video theo ngành của mình.

**Không dùng khi:** cần kịch bản video quảng cáo trả phí theo công thức chuyển đổi → `/ts-kich-ban-video-quang-cao`;
cần tạo video bằng AI (không quay người thật) → `/ts-prompt-video-ai`; cần dựng/cắt video đã quay → `/ts-dung-video`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `02-san-pham-dich-vu.md`, `03-khach-hang-muc-tieu.md`, `04-thuong-hieu-noi-dung.md`, `05-muc-tieu-quy-tac-lien-he.md`;
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `kich-ban-reels` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

Thêm cho skill này: nếu có lịch nội dung (`…-lich-noi-dung-…`) hoặc `02-kien-thuc/cong-thuc/chu-de-noi-dung.md`,
lấy chủ đề video từ đó. Người quay và cách xưng hô lấy từ phần "người đại diện" trong `04-thuong-hieu-noi-dung.md`.

## Quy trình AI thực hiện

### Bước 1 — Xác định video
Hỏi gộp (chỉ phần chưa có):
1. Chủ đề video? (chưa có ý → AI đưa 10 chủ đề theo Bước 2)
2. Mục tiêu: A. Tăng người biết đến · B. Kéo tin nhắn · C. Thông báo ra mắt/ưu đãi · D. Tạo niềm tin.
3. Ai đứng quay, xưng hô thế nào? (bỏ qua nếu hồ sơ đã có)
4. Thời lượng: A. 30 giây · B. 45–60 giây · C. 90 giây (nhiều bước).
5. Nền tảng chính: TikTok / Reels / Shorts.

### Bước 2 — (Nếu cần) Gợi ý chủ đề video theo ngành
Tự rút 10 chủ đề từ hồ sơ theo 4 mảng (chi tiết ở `references/cong-thuc-hook-va-chu-de.md`):
- **Mẹo thực tế** — khách dùng được ngay (cách chọn, cách dùng, cách bảo quản…).
- **Lỗi thường gặp** — "3 lỗi khi … khiến …".
- **Câu chuyện / hậu trường** — quy trình làm, một ngày ở cửa hàng, khách thật (có đồng ý).
- **Bán hàng nhẹ** — trước/sau, giới thiệu sản phẩm qua vấn đề nó giải quyết.

### Bước 3 — Chọn hook
Đưa **3 hook** theo 4 công thức (câu hỏi nỗi đau · khẳng định ngược · con số · kết quả), xem
`references/cong-thuc-hook-va-chu-de.md`. Hook ≤ 12 chữ, nói được trong 3 giây. Người dùng chọn 1, hoặc AI
đề xuất hook mạnh nhất kèm 1 câu lý do.

### Bước 4 — Viết kịch bản theo khung chuẩn
```
THÔNG TIN VIDEO
- Chủ đề:            - Mục tiêu:
- Thời lượng:        - Nền tảng:
- Người quay:        - Xưng hô:

[HOOK — 0:00–0:03]
Lời thoại: "…"
Cảnh quay: [góc máy, biểu cảm, hành động]
Chữ trên màn hình: [3–5 chữ]

[THÂN — 0:03–0:45]  (chia 2–4 ý, mỗi ý 8–12 giây)
Ý 1 (0:03–0:15) — Lời thoại: "…" · Cảnh quay: […] · Chữ: […]
Ý 2 (0:15–0:27) — Lời thoại: "…" · Cảnh quay: […] · Chữ: […]
Ý 3 (0:27–0:40) — Lời thoại: "…" · Cảnh quay: […] · Chữ: […]

[CTA — 0:40–0:50]
Lời thoại: "…"
Cảnh quay: […]
Chữ: [hành động cụ thể]

CAPTION ĐI KÈM (50–100 từ) + 5–8 HASHTAG
GỢI Ý DỰNG: nhịp cắt, nhạc nền (loại nhạc, không ghi bài có bản quyền cụ thể), hiệu ứng, phụ đề.
```
Điều chỉnh mốc thời gian theo thời lượng đã chọn.

### Bước 5 — Chỉnh lời thoại cho tự nhiên
- Nói như đang trò chuyện, không đọc như văn viết. Mỗi câu ≤ 10–12 từ.
- Không từ chuyên ngành khó; bắt buộc dùng thì giải thích ngay.
- Đúng xưng hô của người đại diện (vd "tôi" khi nói với người lạ, "mình" khi thân mật, "em – anh chị" khi bán hàng).
  Hồ sơ chưa có giọng văn → hỏi nhanh 3 câu theo `references/mau-giong-thuong-hieu.md`.
- CTA mặc định: video mẹo → mời theo dõi/nhắn tin nhận thêm mẹo; video bán hàng/ra mắt → ngày + link/nhắn tin
  cụ thể (lấy từ `05-muc-tieu-quy-tac-lien-he.md`).

### Bước 6 — Cổng duyệt
Trình kịch bản. Sửa theo yêu cầu ("ngắn còn 30 giây", "hook gắt hơn", "bỏ cảnh ngoài trời") đến khi người
dùng gõ **"duyệt"**. Hỏi có muốn viết thêm 2–3 biến thể hook để quay thử không.

### Checklist chất lượng (AI tự kiểm trước khi trình)
- [ ] Hook nói trong ≤ 3 giây, rõ chủ đề, gây tò mò đúng người cần.
- [ ] Mỗi cảnh có lời thoại + cách quay + chữ trên màn hình.
- [ ] Tổng thời lượng khớp lựa chọn (≈ 2,5 từ/giây lời nói).
- [ ] Quay được bằng điện thoại, không đòi hỏi thiết bị đắt tiền.
- [ ] Chữ trên màn hình tiếng Việt đủ dấu, 3–5 chữ/dòng.
- [ ] Không bịa kết quả khách hàng, không hứa hẹn tuyệt đối.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** chọn người đứng quay (bạn, nhân viên, hay chỉ quay tay/sản phẩm); điện thoại, giá đỡ,
chỗ có ánh sáng cửa sổ.
1. Gõ `/ts-kich-ban-reels` kèm chủ đề, hoặc chỉ gõ "hôm nay quay gì" để AI gợi ý 10 chủ đề.
2. Chọn mục tiêu và thời lượng (gõ chữ cái A/B/C).
3. Chọn 1 trong 3 hook AI đưa.
4. Đọc to kịch bản 1 lần — chỗ nào nói vấp thì bảo AI sửa ("câu 2 khó nói quá").
5. Gõ **"duyệt"** để AI chốt và lưu vào Bộ Não.
6. Quay theo từng cảnh, mỗi cảnh quay 2–3 lần để chọn.
7. Dựng video (CapCut hoặc `/ts-dung-video`), dán caption AI đã viết rồi đăng.

## Câu lệnh mẫu
- `/ts-kich-ban-reels video 45 giây: 3 lỗi khi chọn kem chống nắng, tôi là chủ shop mỹ phẩm tự quay`
- `/ts-kich-ban-reels quán phở mới khai trương, video 30 giây giới thiệu nước dùng ninh 12 tiếng`
- `/ts-kich-ban-reels gia sư toán lớp 9, video mẹo giải nhanh dạng bài hệ phương trình, kéo phụ huynh nhắn tin`
- `/ts-kich-ban-reels hôm nay quay gì cho tiệm sửa điện thoại? gợi ý 10 chủ đề`

## Kết quả nhận được
- 3 hook để chọn (hoặc 10 chủ đề video nếu chưa có ý).
- Kịch bản đầy đủ theo mốc giây: lời thoại, cảnh quay, chữ trên màn hình, CTA.
- Caption 50–100 từ + hashtag.
- Gợi ý dựng: nhịp cắt, loại nhạc, hiệu ứng, phụ đề.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-kich-ban-reels-<chu-de-khong-dau>/`.
2. Lưu kịch bản đã duyệt (thông tin video + hook đã chọn + kịch bản theo cảnh + caption + gợi ý dựng) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-kich-ban-reels
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `hook-du-phong.md` (các hook chưa dùng), `danh-sach-chu-de.md` (10 chủ đề gợi ý).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-kich-ban-reels · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Hook đã được người dùng khen hoặc video có kết quả tốt: đề xuất thêm vào `02-kien-thuc/cong-thuc/hook-hieu-qua.md` để dùng lại. Nếu người đại diện / xưng hô vừa chốt khác `01-ho-so/04-thuong-hieu-noi-dung.md`, đề xuất cập nhật và hỏi trước khi ghi đè.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không bịa kết quả, lời khách, số liệu trong video. Câu chuyện khách chỉ dùng khi khách đồng ý.
- Nhạc nền: khuyên dùng nhạc trong thư viện của nền tảng để tránh vi phạm bản quyền.
- Quay người khác (khách, nhân viên, trẻ em) phải xin phép trước.
- Ngành nhạy cảm (y tế, thẩm mỹ, tài chính): tránh hứa hẹn kết quả, nhắc kiểm tra quy định nền tảng.

## Skill liên quan
- Trước: `/ts-lich-noi-dung` · `/ts-chan-dung-khach-hang` · `/ts-nghien-cuu-youtube`
- Sau: `/ts-dung-video` · `/ts-prompt-video-ai` · `/ts-kich-ban-video-quang-cao` · `/ts-phan-tich-mang-xa-hoi`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
