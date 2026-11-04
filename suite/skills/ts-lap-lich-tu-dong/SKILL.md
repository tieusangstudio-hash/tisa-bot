---
name: ts-lap-lich-tu-dong
description: "Gọi bằng /ts-lap-lich-tu-dong. Biến yêu cầu theo thời gian thành lời nhắc, tác vụ định kỳ hoặc theo điều kiện: chốt giờ, múi giờ, tần suất, nội dung đủ để lần chạy sau tự hiểu, cổng duyệt trước khi gửi/đăng; dùng tính năng hẹn lịch của nền tảng (Claude, ChatGPT…) hoặc hướng dẫn nhắc bằng Google Calendar/điện thoại. Từ khóa: nhắc tôi, hẹn giờ, mỗi ngày, mỗi tuần, mỗi tháng, lịch tự động, tác vụ định kỳ, báo cáo hằng tuần, khi nào thì báo."
---

# /ts-lap-lich-tu-dong — Lập lịch, nhắc việc và tác vụ tự động

> Giúp bạn đặt lời nhắc và việc tự chạy theo lịch (mỗi sáng, mỗi thứ Hai, cuối tháng…) mà không bị nhầm giờ, chạy trùng hay tự gửi bừa.
> Kết quả: lịch đã tạo (hoặc cấu hình sẵn để bạn tự cài), nội dung tác vụ đầy đủ, 3 lần chạy kế tiếp để đối chiếu và cách tạm dừng/xóa.

**Loại Bộ Não:** CHỈ LƯU

## Khi nào dùng
- "Nhắc tôi 9 giờ sáng mai gọi lại khách", "nhắc đóng tiền quảng cáo ngày 25 hằng tháng".
- "Mỗi sáng thứ Hai soạn giúp tôi kế hoạch nội dung tuần", "mỗi tối Chủ nhật tổng hợp tin nhắn khách".
- "Mỗi ngày 8 giờ báo cáo quảng cáo hôm qua", "cuối tháng làm báo cáo doanh thu".
- "Khi nào chi phí quảng cáo vượt X thì báo tôi" (theo điều kiện).
- Muốn ghép nhiều bước: soạn bài → chờ duyệt → đăng.

**Không dùng khi:** cần thiết kế luồng tự động Facebook/Instagram/quảng cáo chi tiết → `/ts-tu-dong-hoa-meta`;
chưa kết nối ứng dụng mà tác vụ cần dùng (Gmail, Google Sheets, Telegram…) → `/ts-ket-noi-ung-dung` trước;
chỉ cần lịch nội dung (ngày nào đăng gì) → `/ts-lich-noi-dung`.

## Bước 0 — Bộ Não Thứ 2

Skill này không cần đọc hồ sơ để làm việc. Chỉ kiểm tra xem có Bộ Não không (thư mục tên bắt đầu
bằng `Bộ Não Thứ 2`, có file `00-DOC-TRUOC.md`) để lưu kết quả ở bước cuối.

## Quy trình AI thực hiện

### Bước 1 — Chốt 6 thông tin của lịch
| Thông tin | Câu hỏi | Ví dụ |
|---|---|---|
| Việc cần làm | Làm gì, ra kết quả gì? | Soạn 5 ý tưởng bài đăng cho tuần |
| Thời điểm / tần suất | Một lần hay lặp lại? Giờ nào? | 8:30 sáng thứ Hai hằng tuần |
| Múi giờ | Giờ ở đâu? | Giờ Việt Nam (UTC+7) — mặc định nếu người dùng ở Việt Nam, vẫn xác nhận |
| Bắt đầu / kết thúc | Từ ngày nào, đến khi nào? | Từ 10/11/2026, không kết thúc |
| Ngày loại trừ | Bỏ ngày lễ, Tết, cuối tuần? | Bỏ qua tuần Tết |
| Đầu ra / người nhận | Kết quả gửi đâu, cho ai? | Gửi vào chat, kèm email |

Hỏi phần thiếu bằng gợi ý A-B-C-D. Không tạo lịch mơ hồ thiếu múi giờ khi thời gian quan trọng.
Trường hợp đặc biệt cần làm rõ: "ngày 31 hằng tháng" (tháng không có ngày 31 → chạy ngày cuối tháng?), "cuối tháng", "thứ Hai đầu tiên của tháng", "mỗi 2 tuần" (bắt đầu từ tuần nào).

### Bước 2 — Phân loại tác vụ
- **Một lần**: nhắc gọi khách lúc 9:00 ngày 12/11.
- **Định kỳ**: mỗi ngày / mỗi tuần / mỗi tháng.
- **Theo điều kiện**: kiểm tra định kỳ (vd mỗi 3 giờ), chỉ báo khi điều kiện đúng (vd chi phí/tin nhắn > 60k).
- **Quy trình nhiều bước**: soạn → chờ duyệt → đăng/gửi. **Tách tác vụ tạo nội dung khỏi tác vụ gửi/đăng**; tạo bản nháp đủ sớm để người dùng kịp duyệt (vd soạn tối Chủ nhật, đăng sáng thứ Hai sau khi duyệt).

### Bước 3 — Kiểm tra ứng dụng/kết nối cần dùng
- Tác vụ chỉ cần AI suy nghĩ/viết → không cần kết nối.
- Tác vụ đọc Gmail, Google Sheets, Facebook, quảng cáo… → kiểm tra kết nối đang có; **chạy thử một lần chỉ đọc ngay bây giờ** để chắc lần chạy sau không lỗi.
- Thiếu kết nối → chuyển `/ts-ket-noi-ung-dung` hoặc rút gọn tác vụ (vd chỉ nhắc người dùng tự mở báo cáo).

### Bước 4 — Viết nội dung tác vụ "tự đủ ngữ cảnh"
Mỗi lần chạy theo lịch thường là một phiên mới, **không nhớ cuộc trò chuyện này**. Nội dung tác vụ phải tự đủ:
- Mục tiêu, dữ liệu vào (lấy từ đâu), các bước làm, định dạng kết quả, gửi cho ai.
- Tên doanh nghiệp/sản phẩm cần thiết (hoặc chỉ dẫn "đọc Bộ Não Thứ 2 trong thư mục …").
- Quy tắc an toàn: "chỉ soạn bản nháp, không đăng/gửi", "không thay đổi quảng cáo".
- Điều kiện chạy, điều kiện dừng; nếu lỗi thì báo lỗi gì.

Ví dụ nội dung tác vụ (tiệm bánh Mây — giả định):
> "Mỗi thứ Hai 8:30 giờ Việt Nam: đọc Bộ Não Thứ 2 (hồ sơ sản phẩm và thương hiệu), soạn 5 ý tưởng bài Fanpage cho tuần này
> theo 5 trụ cột: giáo dục, hậu trường, bằng chứng, tương tác, bán hàng. Mỗi ý gồm hook, nội dung chính, CTA. Chỉ soạn bản nháp,
> không đăng. Kết quả dạng bảng. Nếu không đọc được Bộ Não thì vẫn soạn và ghi chú 'thiếu hồ sơ'."

### Bước 5 — Chọn nơi tạo lịch (theo nền tảng đang dùng)
| Nền tảng | Công cụ hẹn lịch | Ghi chú |
|---|---|---|
| Claude (claude.ai, Desktop, Cowork, Claude Code) | Tính năng tác vụ định kỳ / hẹn lịch (Scheduled tasks) nếu tài khoản có | Mỗi lần chạy là phiên mới; có thể cần bật quyền tự duyệt để chạy khi bạn vắng mặt |
| ChatGPT | Tính năng Tasks (Tác vụ) nếu tài khoản có | Kết quả gửi về thông báo/ứng dụng ChatGPT |
| Google Antigravity / môi trường khác | Công cụ lập lịch của môi trường nếu có | Kiểm tra trong phần cài đặt/tính năng |
| Không có công cụ hẹn lịch | Google Calendar hoặc ứng dụng Lịch/Lời nhắc trên điện thoại | AI soạn sẵn tiêu đề, giờ, lặp lại, nội dung câu lệnh để bạn dán vào AI khi được nhắc |

Nếu môi trường có công cụ hẹn lịch: AI tự tạo sau khi duyệt (Bước 6). Nếu không: **nói rõ "chưa tạo"** và đưa hướng dẫn thay thế:
- **Google Calendar** (máy tính): mở lịch → bấm **Tạo** → nhập tiêu đề (vd "Chạy /ts-lich-noi-dung tuần này") → chọn ngày giờ →
  **Không lặp lại** đổi thành **Hằng tuần vào thứ Hai** → **Thêm thông báo** (vd 0 phút) → dán câu lệnh mẫu vào phần mô tả → **Lưu**.
- **Điện thoại**: ứng dụng Lời nhắc (iPhone) hoặc Google Tasks/Đồng hồ báo thức (Android) → tạo lời nhắc lặp lại, ghi câu lệnh vào ghi chú.

### Bước 6 — Trình bản xác nhận (CỔNG DUYỆT)
Trình:
- Cách hiểu lịch bằng lời: "Mỗi thứ Hai lúc 8:30 sáng giờ Việt Nam, bắt đầu 10/11/2026".
- Cấu hình máy đọc (nếu có), vd biểu thức lặp `30 8 * * 1` kèm múi giờ `Asia/Ho_Chi_Minh` — giải thích ngắn: phút 30, giờ 8, thứ Hai.
- **3 lần chạy kế tiếp** để đối chiếu (vd 10/11, 17/11, 24/11/2026 lúc 8:30).
- Nội dung tác vụ (Bước 4), đầu ra, người nhận, quyền cần dùng.
- Tác động: có gửi/đăng/thay đổi gì ra bên ngoài không (mặc định: KHÔNG).
- Cách tạm dừng, sửa, xóa.

Chỉ tạo khi người dùng đã yêu cầu rõ và gõ **"duyệt"**.

### Bước 7 — Tạo và xác nhận trạng thái
- Tạo lịch bằng công cụ của nền tảng; đọc lại để xác nhận trạng thái "đang bật", giờ chạy kế tiếp đúng.
- Nếu nền tảng cho chạy thử ngay → chạy thử 1 lần để người dùng xem kết quả mẫu.
- Báo rõ: lịch tên gì, chạy khi nào, xem/sửa/tạm dừng/xóa ở đâu (mục lịch/tác vụ của nền tảng).

### Độ tin cậy của lịch
- Chống chạy trùng: trước khi tạo, xem đã có lịch giống chưa; tác vụ gửi/đăng phải kiểm tra "đã làm hôm nay chưa".
- Thử lại có giới hạn khi lỗi (vd 1–2 lần), sau đó báo lỗi thay vì im lặng.
- Mỗi lần chạy ghi nhật ký ngắn: thời gian, việc đã làm, kết quả, lỗi.
- Không tự động gửi/đăng/thay quảng cáo nếu quy trình chưa có cổng duyệt và quyền phù hợp.

### Checklist chất lượng trước khi giao
- [ ] Có múi giờ, ngày bắt đầu, (ngày kết thúc nếu có), ngày loại trừ.
- [ ] Nội dung tác vụ tự đủ ngữ cảnh, có quy tắc an toàn.
- [ ] Đã đối chiếu 3 lần chạy kế tiếp với người dùng.
- [ ] Tạo nội dung tách khỏi gửi/đăng; có cổng duyệt.
- [ ] Người dùng biết cách tạm dừng/sửa/xóa; nếu chưa tạo được thì đã nói rõ "chưa tạo".

## Hướng dẫn cho học viên (làm theo từng bước)
**Chuẩn bị trước:** biết việc muốn lặp lại là gì, giờ nào, bao lâu một lần; nếu việc cần đọc Gmail/Google Sheets/Facebook thì kết nối trước bằng `/ts-ket-noi-ung-dung`.

1. Gõ `/ts-lap-lich-tu-dong` kèm 1 câu theo mẫu: **"<việc> + <khi nào> + <gửi kết quả đâu>"**.
2. Trả lời các câu hỏi AI (giờ, múi giờ, ngày bắt đầu, có bỏ ngày lễ không…) — chọn chữ cái nếu có gợi ý.
3. Đọc kỹ **3 lần chạy kế tiếp** AI liệt kê. Sai ngày giờ thì nói ngay ("không, là 8 giờ tối").
4. Gõ **"duyệt"** để AI tạo lịch (nếu nền tảng có tính năng hẹn lịch).
5. Nếu AI báo "nền tảng chưa có hẹn lịch": mở Google Calendar hoặc ứng dụng Lời nhắc trên điện thoại, làm theo hướng dẫn AI đưa, dán câu lệnh mẫu vào phần ghi chú.
6. Lần chạy đầu tiên: xem kết quả, muốn sửa thì gõ `/ts-lap-lich-tu-dong sửa lịch <tên lịch>: …`.
7. Muốn dừng: vào mục lịch/tác vụ của nền tảng bấm tạm dừng hoặc xóa, hoặc nhờ AI làm giúp.

## Câu lệnh mẫu
- `/ts-lap-lich-tu-dong nhắc tôi 9 giờ sáng thứ Năm gọi lại 3 khách hỏi gói chăm sóc da của spa Hồng`
- `/ts-lap-lich-tu-dong mỗi tối Chủ nhật 20:00 soạn 5 ý tưởng bài đăng tuần sau cho shop quần áo trẻ em, chỉ soạn nháp`
- `/ts-lap-lich-tu-dong ngày cuối mỗi tháng làm báo cáo học viên mới và học phí còn nợ của khóa học quay video từ Google Sheets`
- `/ts-lap-lich-tu-dong mỗi ngày 8 giờ kiểm tra quảng cáo tiệm bánh Mây, chỉ báo khi chi phí/tin nhắn vượt 50k`

## Kết quả nhận được
- Lịch/tác vụ đã tạo trên nền tảng (hoặc cấu hình + hướng dẫn tự cài trên Google Calendar/điện thoại, ghi rõ "chưa tạo").
- Nội dung tác vụ tự đủ ngữ cảnh, có quy tắc an toàn.
- Cách hiểu lịch bằng lời, cấu hình máy đọc, 3 lần chạy kế tiếp.
- Đầu vào, đầu ra, điều kiện chạy/dừng, người nhận, cách tạm dừng/sửa/xóa.

## Bước cuối — Lưu vào Bộ Não Thứ 2

Chỉ làm khi đã có Bộ Não và kết quả đã được người dùng duyệt:

1. Tạo thư mục `04-ket-qua/<YYYY-MM-DD>-lap-lich-tu-dong-<chu-de-khong-dau>/`.
2. Lưu bản mô tả lịch đã duyệt (tên lịch, tần suất, múi giờ, nội dung tác vụ, đầu ra, nơi tạo, trạng thái, cách tạm dừng/xóa) thành `ket-qua.md`, mở đầu bằng:
   ```yaml
   ---
   loai: ket-qua
   skill: /ts-lap-lich-tu-dong
   ngay: <YYYY-MM-DD>
   chu-de: <chủ đề>
   the: [<2–4 thẻ, vd lich, nhac-viec, tu-dong>]
   ---
   ```
   Kèm theo các file phụ (nếu có): `noi-dung-tac-vu.md` (câu lệnh đầy đủ để tạo lại lịch khi cần).
3. Thêm 1 dòng vào cuối mục **Kết quả** trong `muc-luc.md`:
   `- [[04-ket-qua/<thư-mục>/ket-qua|<Tên ngắn>]] — <mô tả 1 câu>`
4. Thêm 1 dòng vào cuối `nhat-ky.md`:
   `- <YYYY-MM-DD HH:mm> · /ts-lap-lich-tu-dong · <chủ đề> · 04-ket-qua/<thư-mục>/`
5. Đề xuất ghi danh sách các lịch đang bật vào `05-du-an/lich-tu-dong.md` (tên, tần suất, ngày tạo, nơi tạo) để dễ quản lý — hỏi trước khi ghi.
6. Báo cho người dùng đường dẫn đã lưu. Không có Bộ Não thì bỏ qua bước này (đã nhắc ở Bước 0).

## Lưu ý & an toàn
- Không tạo lịch mơ hồ thiếu múi giờ khi thời gian quan trọng.
- Không tự động gửi/đăng/thay quảng cáo nếu quy trình chưa có cổng duyệt và quyền phù hợp.
- Nếu công cụ lập lịch không có, cung cấp cấu hình/hướng dẫn thay thế và nói rõ **chưa tạo** — không giả vờ đã tạo.
- Không ghi mật khẩu, mã OTP, token vào nội dung tác vụ hay lời nhắc.
- Tác vụ định kỳ có thể tốn lượt dùng/chi phí của nền tảng — nhắc người dùng chọn tần suất vừa đủ.

## Skill liên quan
- Trước: `/ts-ket-noi-ung-dung` · Sau: `/ts-tu-dong-hoa-meta`, `/ts-lich-noi-dung`, `/ts-bao-cao-facebook-ads`, `/ts-dieu-phoi-cong-viec`

---
*Bộ skill TISA AI Agent — Học Viện TISA.*
