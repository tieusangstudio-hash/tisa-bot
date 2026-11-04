---
name: ts-prompt-video-ai
description: "Gọi bằng /ts-prompt-video-ai. Đọc kịch bản (hoặc khối VIDEO_SCRIPT_HANDOFF), chia thành các cảnh khoảng 8 giây và viết từng prompt JSON cho công cụ video AI (Flow/Veo và tương tự): mô tả bằng tiếng Anh, lời thoại giữ tiếng Việt, nhân vật và trang phục nhất quán theo hồ sơ thương hiệu, âm thanh môi trường và hiệu ứng, LUÔN tắt nhạc nền. Xuất theo lô để sao chép. Dùng khi muốn làm video AI từ kịch bản. Từ khóa: prompt video AI, prompt Veo, Flow, tách cảnh, video AI tiếng Việt, JSON prompt, nhân vật nhất quán, video 8 giây."
---

# /ts-prompt-video-ai — Prompt video AI

> Biến kịch bản thành chuỗi prompt JSON, mỗi cảnh ~8 giây, sẵn sàng dán vào công cụ video AI: mô tả tiếng
> Anh, lời thoại tiếng Việt, nhân vật – sản phẩm giữ nguyên qua mọi cảnh, có âm thanh môi trường nhưng
> **không bao giờ có nhạc nền**.

**Loại Bộ Não:** CHỈ LƯU (đọc `04-thuong-hieu-noi-dung.md` nếu cần nhân vật)

## Khi nào dùng
- Đã có kịch bản (từ `/ts-kich-ban-video-quang-cao`, `/ts-kich-ban-reels` hoặc tự viết), muốn làm video bằng AI.
- Cần nhân vật/sản phẩm giống nhau ở mọi cảnh.
- Cần lời thoại tiếng Việt khớp khẩu hình.
- Muốn nhận prompt theo lô (3 cảnh/lần) để làm dần và kiểm tra.

**Không dùng khi:** chưa có kịch bản → `/ts-kich-ban-video-quang-cao` hoặc `/ts-kich-ban-reels` trước.
Đã quay video thật, cần dựng/cắt/thêm chữ → `/ts-dung-video`. Cần ảnh tĩnh → `/ts-thiet-ke-anh-quang-cao`.

## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.

**Ngoại lệ — nhân vật:** nếu có Bộ Não và kịch bản cần nhân vật/người đại diện, đọc
`01-ho-so/04-thuong-hieu-noi-dung.md` mục *Nhân vật đại diện* (ngoại hình, trang phục mặc định, giọng nói,
mô tả tiếng Anh cho AI, ảnh tham chiếu trong `03-tai-lieu-tho/dinh-kem/`) và dùng làm mô tả mặc định.
Người dùng mô tả khác trong lượt này → ưu tiên lời người dùng.

## Quy trình AI thực hiện

### Quy tắc âm thanh bất biến
Mọi cảnh phải có:
- Lời thoại tiếng Việt nếu cảnh có lời.
- Âm thanh môi trường và hiệu ứng phù hợp khi cần (nhỏ hơn giọng nói).
- `"background_music": false`.
- `"music": "none"`.
- Ràng buộc âm trong `negative_constraints`: `no music`, `no background score`, `do not generate music`.

Không thêm nhạc nền kể cả khi kịch bản hay phong cách thường có nhạc. Người dùng muốn nhạc → hướng dẫn ghép
nhạc có bản quyền ở bước dựng (`/ts-dung-video`), **không** đổi quy tắc trong prompt.

### Quy tắc ngôn ngữ
- Mọi mô tả (bối cảnh, nhân vật, hành động, máy quay, ánh sáng, âm thanh) viết **tiếng Anh**.
- `dialogue.text` giữ **nguyên tiếng Việt có dấu** đúng kịch bản. Không dịch lời thoại.
- Chữ trên màn hình (nếu có) tiếng Việt đúng dấu, ngắn.

### Bước 1 — Xác nhận trước khi tạo JSON
Đọc kịch bản người dùng gửi hoặc khối `VIDEO_SCRIPT_HANDOFF`. Chỉ hỏi phần chưa biết (gộp 1 lượt, có gợi ý):
1. Video **dọc 9:16** hay **ngang 16:9**?
2. Nhận **3 prompt mỗi lần**, số lượng tùy chọn, hay **toàn bộ**?
3. Đã có ảnh nhân vật và ảnh sản phẩm chưa? Ảnh nào là tham chiếu chính?
4. Phong cách hình ảnh (vd tự nhiên đời thường / quảng cáo sáng sạch / điện ảnh tối)?
5. Một bối cảnh xuyên suốt hay nhiều bối cảnh?
6. Bản **đầy đủ** (JSON) hay **rút gọn** (cho công cụ giới hạn độ dài lệnh)?

Nhân vật: lấy từ tệp 04 (nếu có), nêu lại để người dùng xác nhận. Tóm tắt lựa chọn → 👉 chờ xác nhận.

### Bước 2 — Tách cảnh
1. Chia kịch bản thành các cảnh **khoảng 8 giây**, mỗi cảnh **một hành động chính**.
2. Lời thoại mỗi cảnh đủ ngắn để nói tự nhiên — thường tối đa **18–22 từ tiếng Việt**. Vượt → tách thêm cảnh.
3. Lập **bảng kế hoạch cảnh**: số cảnh · mục tiêu · lời thoại · bối cảnh · hành động · chuyển cảnh.
4. Giữ liên tục: nhân vật, trang phục, sản phẩm, ánh sáng, hướng nhìn, vị trí đạo cụ.
👉 Trình bảng kế hoạch cảnh, chờ "duyệt" (người dùng có thể gộp/tách/bỏ cảnh).

### Bước 3 — Bám ảnh tham chiếu
Mô tả rõ: bám sát ảnh nhân vật và ảnh sản phẩm người dùng tải lên; không đổi khuôn mặt, tóc, tuổi, trang phục,
tỷ lệ cơ thể, hình dáng/màu sản phẩm, logo hoặc chữ. Không tự "làm đẹp", biến dạng hay thiết kế lại. Ảnh thiếu
hoặc mâu thuẫn (vd ảnh nhân vật mặc khác trang phục trong tệp 04) → dừng và hỏi.

### Bước 4 — Xuất JSON theo lô
Đọc schema, ví dụ và bản rút gọn trong `references/json-flow.md`. Mỗi cảnh = **một khối mã `json` riêng** để
giao diện có nút sao chép (không hứa nút giao diện tùy chỉnh). JSON hợp lệ: không chú thích bên trong, không
dấu phẩy thừa. Đủ số prompt của một lô thì **dừng** để người dùng thử, rồi mới làm tiếp. Chọn toàn bộ → vẫn
nhóm theo thứ tự rõ ràng (S01, S02…).

### Bước 5 — Kiểm tra trước khi gửi
- [ ] Đúng tỷ lệ khung hình và thời lượng ~8 giây mọi cảnh.
- [ ] Lời thoại không quá dài, khớp khẩu hình; đúng tiếng Việt có dấu.
- [ ] Mô tả bằng tiếng Anh; chỉ lời thoại/chữ trên hình là tiếng Việt.
- [ ] Nhân vật/sản phẩm nhất quán với ảnh và tệp 04.
- [ ] Có ambient/SFX hợp lý, không lấn giọng.
- [ ] `background_music` là `false`, `music` là `"none"`, `negative_constraints` đủ 3 lệnh cấm nhạc.
- [ ] Không bịa logo, chữ trên bao bì hoặc tuyên bố quảng cáo.
- [ ] JSON hợp lệ (mở/đóng ngoặc đủ, không dấu phẩy thừa).

### Bước 6 — Hỗ trợ khi công cụ báo lỗi
Công cụ báo vi phạm chính sách → đổi cách diễn đạt phần mô tả tiếng Anh nhưng giữ nguyên ý (gợi ý cuối
`references/json-flow.md`). Nhân vật bị đổi mặt giữa các cảnh → nhắc dùng cùng ảnh tham chiếu, thêm câu
continuity, giảm chuyển động máy quay. Video tự sinh nhạc → nhắc lại 3 lệnh cấm nhạc và tắt nhạc ở bước dựng.

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị:** kịch bản (hoặc khối `VIDEO_SCRIPT_HANDOFF` từ `/ts-kich-ban-video-quang-cao`); 1 ảnh nhân vật
rõ mặt, chính diện; 1 ảnh sản phẩm nền sạch. Nếu đã điền *Nhân vật đại diện* trong hồ sơ, AI tự dùng.

1. Gõ `/ts-prompt-video-ai` rồi dán kịch bản (hoặc khối bàn giao), đính kèm ảnh nhân vật/sản phẩm.
2. Trả lời các câu chọn: dọc hay ngang, 3 cảnh/lần hay toàn bộ, bản đầy đủ hay rút gọn.
3. Xem bảng kế hoạch cảnh, gõ "duyệt" (hoặc "gộp cảnh 2 và 3").
4. Bấm nút sao chép trên từng khối JSON → dán vào công cụ video AI, tải ảnh tham chiếu lên cùng lúc.
5. Thử 3 cảnh đầu; báo lại AI nếu nhân vật bị đổi mặt hoặc có nhạc lạ → AI sửa prompt.
6. Gõ "tiếp" để nhận lô tiếp theo.
7. Ghép các đoạn video lại (và thêm chữ, logo nếu cần) bằng `/ts-dung-video` hoặc phần mềm dựng quen dùng.

## Câu lệnh mẫu
- `/ts-prompt-video-ai đây là kịch bản 60 giây quảng cáo tiệm bánh, video dọc, mỗi lần 3 cảnh` (kèm kịch bản)
- `/ts-prompt-video-ai dùng nhân vật đại diện trong hồ sơ, làm video giới thiệu khóa học 30 giây, toàn bộ cảnh`
- `/ts-prompt-video-ai video ngang 16:9 giới thiệu showroom nội thất, không có người, chỉ quay sản phẩm`
- `/ts-prompt-video-ai bản rút gọn cho công cụ giới hạn độ dài, kịch bản spa 45 giây`

## Kết quả nhận được
- Bảng kế hoạch cảnh (số cảnh, lời thoại, hành động, chuyển cảnh).
- Prompt JSON từng cảnh (hoặc bản rút gọn), mỗi cảnh một khối sao chép được.
- Ghi chú ảnh tham chiếu cần tải lên cho từng cảnh.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-prompt-video-ai-<chu-de-khong-dau>/`.
2. Lưu bảng kế hoạch cảnh + toàn bộ prompt (theo thứ tự S01, S02…) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-prompt-video-ai
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề video>
   the: [video-ai, prompt, <tỷ lệ khung hình>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `prompts.json` (mảng tất cả cảnh), ảnh tham chiếu đã dùng.
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|Prompt video <chủ đề>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-prompt-video-ai · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Nếu người dùng vừa chốt mô tả nhân vật mới (ngoại hình, trang phục, giọng) mà tệp 04 chưa có hoặc khác,
   đề xuất cập nhật mục *Nhân vật đại diện* trong `01-ho-so/04-thuong-hieu-noi-dung.md` — hỏi trước khi ghi đè.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không tạo nội dung tình dục hóa người chưa thành niên, quảng bá hàng hóa/dịch vụ hạn chế độ tuổi cho người
  chưa thành niên, hoạt động nguy hiểm hoặc biến đổi ngoại hình gây hại.
- Tôn trọng quyền hình ảnh: chỉ dùng ảnh người thật khi có sự đồng ý; không giả mạo người thật gây hiểu nhầm.
- Không bịa logo, nhãn, chữ trên bao bì, tuyên bố công dụng.
- Không có nhạc nền trong prompt — quy tắc này không đổi.

## Skill liên quan
- Trước: `/ts-kich-ban-video-quang-cao` · `/ts-kich-ban-reels` · `/ts-tao-ho-so-doanh-nghiep` (nhân vật đại diện)
- Sau: `/ts-dung-video` · `/ts-len-camp-facebook` · `/ts-chay-tiktok-ads`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
