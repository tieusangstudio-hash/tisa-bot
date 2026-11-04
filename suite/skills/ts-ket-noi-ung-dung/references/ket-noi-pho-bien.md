# Các kết nối phổ biến (dùng cho /ts-ket-noi-ung-dung)

> Tên menu và cách làm có thể thay đổi theo phiên bản. Trước khi hướng dẫn, AI kiểm tra lại tài liệu chính thức hiện hành
> của ứng dụng đó (nếu có công cụ tìm kiếm web). Mọi mã bí mật (token, khóa API, mật khẩu) **không bao giờ** dán vào chat,
> không ghi vào Bộ Não, không ghi vào file hướng dẫn.

## Bảng tổng hợp

| Ứng dụng | Thường dùng để | Cách kết nối ưu tiên | Quyền nên cấp lúc đầu | Lưu ý |
|---|---|---|---|---|
| Google Drive | Đọc/lưu tài liệu, Bộ Não trên Drive | Kết nối có sẵn (Connectors/Apps) của nền tảng | Chỉ đọc; thêm quyền ghi khi cần | Chọn đúng tài khoản Google công việc |
| Gmail | Đọc email khách, soạn nháp trả lời | Kết nối có sẵn | Đọc + tạo nháp | Không cho tự gửi khi chưa duyệt |
| Google Sheets | Đọc/ghi bảng khách, thu chi, báo cáo | Kết nối Google Drive/Sheets có sẵn | Chỉ đọc → ghi một file cụ thể | Ghi đúng sheet/vùng được phép |
| Google Calendar | Xem lịch, tạo lịch hẹn | Kết nối có sẵn | Chỉ đọc → tạo sự kiện | Kiểm tra múi giờ lịch |
| Facebook Page / Meta Business | Đọc bài, bình luận, đăng bài | Kết nối Meta chính thức (nếu nền tảng có) hoặc Meta Business Suite | Đọc nội dung + số liệu Trang | Chọn đúng Trang, không cấp toàn bộ Business khi không cần |
| Meta Ads (quảng cáo Facebook/Instagram) | Đọc số liệu, cảnh báo, chỉnh quảng cáo | Kết nối Meta Ads chính thức (nếu có) | Chỉ đọc số liệu (insights) | Quyền quản lý quảng cáo chỉ bật khi đã có quy tắc duyệt |
| TikTok Ads / TikTok | Đọc số liệu quảng cáo, đăng video | Kết nối chính thức nếu có; nếu không thì xuất file báo cáo | Chỉ đọc | Đa số học viên dùng xuất file là đủ |
| Zalo Official Account (OA) | Nhắn tin chăm sóc khách, nhận tin nhắn | Tài khoản OA + ứng dụng trên trang nhà phát triển Zalo; hoặc qua phần mềm quản lý hội thoại có tích hợp Zalo OA | Theo nhu cầu tối thiểu | Mã truy cập có thời hạn ngắn, cần làm mới; tin nhắn chủ động có thể cần mẫu được duyệt và tính phí — kiểm tra chính sách hiện hành |
| Telegram bot | Nhận thông báo đơn hàng, báo cáo | Tạo bot qua @BotFather | — | Mã bot (bot token) là bí mật, ai có mã là điều khiển được bot |
| Canva | Lấy/tạo thiết kế | Kết nối Canva có sẵn (nếu nền tảng có) | Đọc thiết kế | |
| Notion / Lark / phần mềm quản lý | Ghi chú, công việc, dữ liệu | Kết nối có sẵn hoặc máy chủ MCP chính thức của hãng | Một trang/không gian cụ thể | Chia quyền theo trang, không cấp cả workspace nếu không cần |
| Cổng thanh toán / ngân hàng | Đối soát giao dịch | Dịch vụ trung gian chính thức (vd webhook nhận biến động số dư) | Chỉ đọc giao dịch | Không bao giờ cấp quyền chuyển tiền cho AI |

## Thêm kết nối trong từng nền tảng (viết trung tính)

**Claude (claude.ai, Desktop, Cowork):**
1. Mở **Cài đặt** → mục **Kết nối / Connectors** (hoặc biểu tượng công cụ trong ô chat → quản lý kết nối).
2. Chọn ứng dụng trong danh sách (Google Drive, Gmail, Google Calendar…) → **Kết nối**.
3. Trang đăng nhập **chính thức** của ứng dụng mở ra → đăng nhập ở đó (không nhập vào chat) → xem danh sách quyền → **Cho phép**.
4. Ứng dụng không có sẵn: chọn **Thêm kết nối tùy chỉnh** (nếu gói tài khoản cho phép) và dán **địa chỉ máy chủ MCP chính thức** do hãng công bố.

**Claude Code / Codex (dùng trên máy tính, có cửa sổ lệnh):**
- Thêm máy chủ MCP bằng lệnh/tệp cấu hình theo tài liệu của công cụ. Khóa bí mật đặt trong **biến môi trường**, không ghi thẳng vào tệp chia sẻ.
- Đặt biến môi trường tạm thời trong phiên làm việc:
  - macOS/Linux: `export TEN_BIEN="giá-trị"` (gõ trong Terminal, không dán vào chat)
  - Windows (PowerShell): `$env:TEN_BIEN="giá-trị"`
  - Lưu lâu dài: dùng trình quản lý mật khẩu/kho bí mật của hệ thống, hoặc biến môi trường người dùng (Windows: System Properties → Environment Variables).

**ChatGPT:**
1. **Cài đặt** → mục **Ứng dụng / Apps** (trước đây gọi là Connectors).
2. Chọn ứng dụng → **Kết nối** → đăng nhập trên trang chính thức → cấp quyền.
3. Một số gói tài khoản cho thêm ứng dụng tùy chỉnh (máy chủ MCP) ở chế độ nhà phát triển — kiểm tra quyền của gói.

**Google Antigravity / công cụ lập trình có MCP khác:**
- Mở phần cài đặt **MCP / Kết nối / Tích hợp**, chọn máy chủ có sẵn hoặc thêm máy chủ theo tài liệu chính thức; khóa bí mật đặt qua biến môi trường hoặc ô nhập bí mật của công cụ.

## Telegram bot — từng bước (ví dụ nhận thông báo)

1. Mở Telegram, tìm **@BotFather** (có dấu tích xanh) → gõ `/newbot`.
2. Đặt tên hiển thị, rồi tên người dùng kết thúc bằng `bot` (vd `tiembanhmay_baodon_bot` — ví dụ).
3. BotFather gửi **mã bot (token)** → **giữ bí mật**, chỉ dán vào ô "bí mật/biến môi trường" của công cụ tự động hóa, không dán vào chat với AI.
4. Mở bot vừa tạo, bấm **Start** (hoặc thêm bot vào nhóm nhận thông báo).
5. Lấy **mã cuộc trò chuyện (chat ID)** theo hướng dẫn của công cụ đang dùng; chat ID không phải bí mật nhưng không nên công khai.
6. Gửi thử 1 tin "Kết nối thành công" → kiểm tra nhận được.
7. Lộ mã bot? Vào @BotFather → `/revoke` (hoặc `/token`) để đổi mã mới.
Chi tiết luồng báo đơn → `/ts-bao-don-telegram`.

## Zalo Official Account — điều cần biết trước

- Cần có **Zalo OA** (tài khoản doanh nghiệp) đã xác thực theo yêu cầu của Zalo.
- Kết nối kỹ thuật cần tạo ứng dụng trên **trang dành cho nhà phát triển của Zalo**, liên kết với OA, cấp quyền; mã truy cập có thời hạn và phải làm mới định kỳ.
- Cách dễ hơn cho người không rành kỹ thuật: dùng **phần mềm quản lý hội thoại/CRM** có sẵn tích hợp Zalo OA và Fanpage, rồi cho AI soạn nội dung để dán vào.
- Nhắn tin chủ động cho khách thường phải theo quy định (thời gian tương tác, mẫu tin được duyệt, có thể tính phí) — kiểm tra chính sách hiện hành trước khi lên kế hoạch.
Chăm sóc khách qua Zalo → `/ts-cham-soc-khach-zalo`.

## Kiểm tra sau khi kết nối (bắt buộc)

1. **Phép thử chỉ đọc**: liệt kê 3 tệp gần nhất / 3 email gần nhất / tên Trang / tên tài khoản quảng cáo.
2. Người dùng xác nhận "đúng tài khoản của tôi".
3. Chỉ khi cần ghi: **thử ghi nhỏ có thể hoàn tác** (tạo 1 bản nháp, 1 dòng thử, 1 sự kiện thử) → người dùng xem → xóa bản thử nếu cần (người dùng tự xóa hoặc xác nhận cho AI xóa đúng bản thử đó).
4. Ghi vào sổ kết nối: tên kết nối · tài khoản (email/tên Trang, không ghi mật khẩu) · quyền đã cấp · ngày kết nối · ngày hết hạn (nếu biết) · cách ngắt kết nối.

## Ngắt kết nối / thu hồi quyền

- Trong nền tảng AI: Cài đặt → Kết nối/Ứng dụng → chọn ứng dụng → **Ngắt kết nối**.
- Phía ứng dụng gốc: Google (Tài khoản Google → Bảo mật → Ứng dụng và dịch vụ bên thứ ba), Facebook (Cài đặt → Tiện ích tích hợp doanh nghiệp / Ứng dụng và trang web), Telegram (@BotFather đổi mã).
- Nghi lộ mã bí mật: thu hồi ngay, tạo mã mới, kiểm tra nhật ký hoạt động.
