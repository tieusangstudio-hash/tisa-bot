---
name: ts-kich-ban-video-quang-cao
description: "Gọi bằng /ts-kich-ban-video-quang-cao. Đọc hồ sơ doanh nghiệp rồi viết kịch bản video quảng cáo 60, 90 hoặc 120 giây: thông điệp trung tâm, 5 hook cho 5 tệp khách/nỗi đau khác nhau, thân bài thuyết phục có mốc thời gian, CTA, bản đọc liền mạch (teleprompter), bảng cảnh và khối bàn giao để tạo video AI. Dùng khi cần lời thoại quảng cáo chuyển đổi, video bán hàng dài, hoặc đầu vào cho /ts-prompt-video-ai. Từ khóa: kịch bản quảng cáo, kịch bản video ads, lời thoại quảng cáo, video 60 giây, 5 hook, script bán hàng, video chuyển đổi."
---

# /ts-kich-ban-video-quang-cao — Kịch bản video quảng cáo

> AI viết trọn kịch bản quảng cáo 60/90/120 giây đúng sản phẩm và giọng thương hiệu của bạn: 5 hook để test
> 5 nhóm khách, thân bài thuyết phục, CTA, bảng cảnh để quay — và khối bàn giao để chuyển thẳng sang làm video AI.

**Loại Bộ Não:** ĐỌC + LƯU

## Khi nào dùng
- Chuẩn bị quay video chạy quảng cáo Facebook/TikTok/YouTube.
- Muốn test nhiều góc nội dung (nhiều hook) với cùng một thân bài.
- Cần kịch bản đầu vào cho video AI (`/ts-prompt-video-ai`) hoặc cho người quay.
- Video quảng cáo cũ không hiệu quả, muốn viết lại theo cấu trúc rõ ràng.

**Không dùng khi:** video ngắn 30–90 giây đăng tự nhiên (không chạy quảng cáo) → `/ts-kich-ban-reels`.
Chỉ cần chữ quảng cáo (tiêu đề, nội dung bài quảng cáo) → `/ts-viet-quang-cao`.

## Bước 0 — Đọc Bộ Não Thứ 2

1. Tìm Bộ Não: thư mục đang làm việc hoặc folder đã kết nối có tên bắt đầu bằng `Bộ Não Thứ 2`
   và có file `00-DOC-TRUOC.md` ở gốc.
2. Nếu tìm thấy, đọc theo thứ tự:
   - `00-DOC-TRUOC.md` (quy tắc chung) và `muc-luc.md` (mục lục);
   - trong `01-ho-so/`: `02-san-pham-dich-vu.md` (offer, giá, bằng chứng), `03-khach-hang-muc-tieu.md` (nỗi đau, rào cản), `04-thuong-hieu-noi-dung.md` (giọng văn, xưng hô, nhân vật đại diện), `05-muc-tieu-quy-tac-lien-he.md` (kênh, quy tắc nói);
   - trong `04-ket-qua/`: các lần chạy trước cùng chủ đề (tìm theo tên thư mục chứa `kich-ban-video-quang-cao` hoặc từ khóa) để không làm lại từ đầu.
3. Tóm tắt trong 3–5 dòng những gì đã biết, rồi **chỉ hỏi phần còn thiếu**.
4. Nếu không thấy Bộ Não: nói một câu "Bạn chưa kết nối Bộ Não Thứ 2 — chạy `/ts-cai-dat-bo-nao` để AI nhớ thông tin doanh nghiệp cho mọi lần sau", rồi vẫn tiếp tục bằng cách hỏi trực tiếp.

**Riêng skill này:** đọc thêm kết quả `/ts-chan-dung-khach-hang` (cụm nỗi đau) và `/ts-viet-quang-cao`
(góc nội dung đã test) trong `04-ket-qua/` nếu có.

## Quy trình AI thực hiện

### Bước 1 — Thu thập thông tin
Từ Bộ Não; nếu thiếu, hỏi ngắn (gộp 1 lượt, có gợi ý):
1. Muốn video dài **1 phút**, **1 phút 30 giây** hay **2 phút**?
2. Sản phẩm/dịch vụ, khách hàng, vấn đề chính?
3. Mục tiêu và kênh quảng cáo (nhắn tin / mua hàng / đăng ký; Facebook / TikTok / YouTube)? Tỷ lệ khung hình?
4. Offer, giá, CTA, bằng chứng **đã được xác minh**?
5. Ai nói trong video (nhân vật đại diện ở tệp 04, người thật, hay giọng đọc)?

Không hỏi lại thông tin đã có.

### Bước 2 — Chọn cấu trúc
Đọc `references/framework-kich-ban.md`. Chọn 1 trong: AIDA, PAS, Before–After–Bridge,
Problem–Solution–Proof–Offer, Story–Offer. Giải thích lựa chọn trong 1–2 câu. Áp dụng nguyên lý bán hàng phổ
biến, không sao chép câu chữ độc quyền, không gán sai cho người nổi tiếng.

### Bước 3 — Thông điệp trung tâm
Một câu: khách hàng + kết quả + lý do tin.

### Bước 4 — Năm hook
Hook 1 → Hook 5, mỗi hook nhắm **một tệp khách hoặc một nỗi đau riêng** (5 góc gợi ý trong reference).
Không chỉ thay vài từ; mỗi hook phải có góc nhìn và động cơ khác nhau. Ghi rõ hook nào cho tệp khách nào.
👉 Cổng duyệt 1: người dùng chọn hook chính (các hook khác dùng để test quảng cáo).

### Bước 5 — Thân bài
Lời thoại tự nhiên theo giọng văn và xưng hô ở tệp 04: vấn đề → hệ quả → cơ chế giải pháp → giá trị/lợi ích →
điểm khác biệt → bằng chứng thật → giảm rủi ro → offer. Gắn **mốc thời gian** cho từng đoạn, giữ số chữ hợp
thời lượng (60s ≈ 120–150 từ · 90s ≈ 180–220 từ · 120s ≈ 240–300 từ).

### Bước 6 — Kết bài
Một CTA cụ thể, hợp mục tiêu, không gây áp lực sai lệch (không đếm ngược giả, không "chỉ còn 2 suất" nếu không thật).

### Bước 7 — Bản bàn giao
- **Bản teleprompter** liền mạch (đọc được ngay).
- **Bảng cảnh sơ bộ:** thời gian · hình ảnh · lời thoại · chữ trên màn hình · mục tiêu cảnh.
- **Khối `VIDEO_SCRIPT_HANDOFF`** (mẫu trong reference): duration, aspect_ratio, selected_hook, character,
  product, narration, scene_intents, on_screen_text, cta, `music: none` — để `/ts-prompt-video-ai` làm tiếp.
👉 Cổng duyệt 2: trình toàn bộ, chờ "duyệt".

### Checklist chất lượng
- [ ] Đọc thử đúng thời lượng (đếm chữ theo nhịp tham khảo).
- [ ] 5 hook khác nhau thật sự về tệp khách/nỗi đau; mỗi hook ≤ 2 câu.
- [ ] Không bịa số liệu, chứng nhận, đánh giá; không bảo đảm kết quả. Thiếu → `[CẦN BỔ SUNG: …]`.
- [ ] Phân biệt tính năng với lợi ích; có bằng chứng cho mọi tuyên bố mạnh.
- [ ] Nếu dùng hình người thật: không nhận xét tiêu cực về cơ thể, không biến đổi ngoại hình nhạy cảm.
- [ ] Ngành có quy định (mỹ phẩm, thực phẩm chức năng, y tế, tài chính): không dùng từ cấm trong tệp 04.
- [ ] Giọng văn, xưng hô đúng hồ sơ.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** hồ sơ doanh nghiệp; biết offer/giá/ưu đãi đang chạy; nếu có, 1–2 feedback thật của khách
(được phép dùng) và ảnh/video sản phẩm.

1. Gõ `/ts-kich-ban-video-quang-cao` kèm sản phẩm và thời lượng (vd "gói chăm sóc da, video 60 giây").
2. Trả lời câu hỏi còn thiếu (mục tiêu quảng cáo, ai nói trong video).
3. Đọc 5 hook, chọn hook chính (gõ số).
4. Đọc kịch bản; sửa bằng lời ("bớt dài dòng", "thêm câu về bảo hành", "xưng em – chị").
5. Gõ "duyệt" để nhận bản đọc liền mạch + bảng cảnh.
6. Quay thật: dùng bản teleprompter. Làm video AI: gõ `/ts-prompt-video-ai` và dán khối `VIDEO_SCRIPT_HANDOFF`.
7. Muốn test quảng cáo: dùng 4 hook còn lại làm 4 phiên bản mở đầu khác nhau.

## Câu lệnh mẫu
- `/ts-kich-ban-video-quang-cao gói chăm sóc da 6 buổi của spa Hồng, video 60 giây, chạy kéo tin nhắn`
- `/ts-kich-ban-video-quang-cao khóa học quay video bằng điện thoại, video 90 giây, người nói là chủ khóa học`
- `/ts-kich-ban-video-quang-cao máy lọc nước gia đình, video 2 phút cho YouTube, khách hay sợ giá cao`
- `/ts-kich-ban-video-quang-cao viết lại kịch bản tháng trước, đổi sang cấu trúc câu chuyện khách hàng`

## Kết quả nhận được
- Thông điệp trung tâm + giải thích cấu trúc đã chọn.
- 5 hook (ghi rõ tệp khách/nỗi đau của từng hook).
- Thân bài có mốc thời gian + CTA.
- Bản teleprompter, bảng cảnh sơ bộ, khối `VIDEO_SCRIPT_HANDOFF`.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-kich-ban-video-quang-cao-<chu-de-khong-dau>/`.
2. Lưu kịch bản đầy đủ (thông điệp, 5 hook, thân bài, CTA, bảng cảnh) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-kich-ban-video-quang-cao
   ngay: <YYYY-MM-DD>
   chu-de: <sản phẩm — thời lượng>
   the: [kich-ban, video-quang-cao, <kênh>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `teleprompter.txt`, `video-script-handoff.txt`.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|Kịch bản QC <sản phẩm>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-kich-ban-video-quang-cao · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Khi người dùng báo hook nào chạy tốt (từ báo cáo quảng cáo), đề xuất lưu vào
   `02-kien-thuc/cong-thuc/hook-hieu-qua.md` (hook, tệp khách, chỉ số, ngày) — hỏi trước khi ghi.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không viết quảng cáo nhắm người chưa thành niên cho hàng hóa/dịch vụ hạn chế độ tuổi, cờ bạc, chất gây
  nghiện hoặc hoạt động nguy hiểm. Không tạo nội dung tình dục hóa người chưa thành niên.
- Không bịa số liệu, chứng nhận, đánh giá; không cam kết kết quả.
- Tuân thủ chính sách quảng cáo của nền tảng (vd không nhắm vào đặc điểm cá nhân kiểu "Bạn bị béo?").

## Skill liên quan
- Trước: `/ts-tao-ho-so-doanh-nghiep` · `/ts-chan-dung-khach-hang` · `/ts-viet-quang-cao`
- Sau: `/ts-prompt-video-ai` · `/ts-dung-video` · `/ts-len-camp-facebook` · `/ts-chay-tiktok-ads`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
