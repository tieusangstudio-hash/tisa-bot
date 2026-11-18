# 60 - Sổ tay đấu nối thanh toán (SePay, PayOS, Stripe)

Ngày: 19/11/2026. Nguyên tắc cứng: AI chỉ ĐỌC giao dịch, tạo link thanh toán, nhận webhook. Việc chuyển tiền, rút tiền, hoàn tiền, nhập số tài khoản/thẻ, mã OTP ngân hàng là việc của NGƯỜI THẬT.

## 1. SePay (nhận biết tiền vào qua chuyển khoản ngân hàng VN)
Nguồn: https://developer.sepay.vn (đọc: /sepay-webhooks/xac-thuc, /sepay-api/v1/bat-dau-nhanh, docs.sepay.vn/lap-trinh-webhooks.html). Không thấy MCP chính hãng.
Độ khó: Vừa. Thời gian: 20-60 phút.
1. Người thật: đăng ký my.sepay.vn, **liên kết tài khoản ngân hàng** (bước có OTP/ứng dụng ngân hàng; AI không làm).
2. Chuẩn bị máy nhận webhook: một URL HTTPS công khai (có thể là Cloudflare Worker, xem `70-cloudflare-deploy-web.md`).
3. Tạo webhook: menu **WebHooks** (hoặc "Tích hợp Webhook") > thêm mới > nhập URL nhận, chọn tài khoản ngân hàng, chọn kiểu xác thực ở bước **Security**. (Tên menu cần xác minh trên màn hình thật.)
4. Bốn kiểu xác thực: None (chỉ test), **API Key** (SePay gửi `Authorization: Apikey <KEY>`; khóa chỉ hiện đủ một lần), **HMAC-SHA256 (khuyến nghị)** (header `X-SePay-Signature: sha256=<hex>` và `X-SePay-Timestamp` giây Unix; ký trên chuỗi `{timestamp}.{raw_body}` bằng Secret Key; phải dùng raw body; từ chối lệch quá 300 giây), **OAuth 2.0** (SePay gọi token endpoint của bạn với `client_credentials`, rồi gửi `Authorization: Bearer`). Trang docs cũ còn nhắc whitelist IP.
5. Phản hồi bắt buộc: HTTP **200 hoặc 201** + JSON `{"success": true}`; khác là thất bại. Lịch gửi lại khi thất bại: không rõ trong trang đã đọc, cần xác minh.
6. Dữ liệu giao dịch (docs.sepay.vn): `gateway`, `transactionDate`, `accountNumber`, `subAccount`, `transferType` (in/out), `transferAmount`, `accumulated`, `code`, `content`, `referenceCode`, `description`. Nên chống trùng bằng `referenceCode` (hoặc id) với ràng buộc UNIQUE (khuyến nghị của người viết, trang không nói).
7. Thử: bật **Test Mode** (môi trường `my.dev.sepay.vn` theo trang bắt đầu nhanh), thêm tài khoản thử, dùng **Mô phỏng giao dịch**; xem kết quả ở **Giao dịch** hoặc tab **Lịch sử gửi** của Tích hợp Webhook (giao dịch giả lập không hiện trong nhật ký môi trường thật).
8. API token: my.sepay.vn > **API Access** > tạo token, gửi ở header Authorization. API v1 không phát triển thêm, tích hợp mới dùng v2 (cần xác minh). OAuth2 của SePay có scope kiểu `webhook:read/write/delete` cho API quản lý webhook; client ID/secret cấp qua Developer Portal.
9. Lỗi hay gặp: URL webhook không HTTPS hoặc không tới được; trả sai định dạng (thiếu `success: true`); xác thực HMAC sai do dùng body đã parse; nội dung chuyển khoản thiếu mã đơn nên không khớp đơn; trùng webhook; test mode lẫn production.
10. Thu hồi: xoá webhook, tạo lại/đổi API Key/Secret, thu hồi token; huỷ liên kết ngân hàng tại my.sepay.vn (cần xác minh).
11. Kiểm tra nối thật: tạo giao dịch giả lập trong Test Mode và thấy bản ghi ở máy nhận; sau đó với tiền thật chỉ dùng số tiền nhỏ do chủ tự chuyển.

## 2. payOS
Nguồn: https://payos.vn/docs/ (trang bắt đầu), SDK: github.com/payOSHQ, https://app.unpkg.com/@payos/node@2.0.3/files/README.md, https://pypi.org/project/payos/. Không tìm thấy MCP chính hãng.
Độ khó: Vừa -> Khó (xác minh kênh thanh toán). Thời gian: 30 phút + chờ duyệt (không rõ).
1. Người thật: tạo tài khoản payOS (my.payos.vn), tạo **kênh thanh toán**, liên kết tài khoản ngân hàng/xác minh theo yêu cầu (OTP, giấy tờ nếu có). Trang đã đọc không mô tả các bước này chi tiết: cần xác minh trên màn hình thật.
2. Lấy 3 khóa của kênh: **Client ID, API Key, Checksum Key**. Đặt vào biến môi trường `PAYOS_CLIENT_ID`, `PAYOS_API_KEY`, `PAYOS_CHECKSUM_KEY` (tên theo SDK Go/Java), không ghi vào mã/wiki/chat.
3. Luồng: website gọi API tạo link thanh toán -> khách chuyển sang trang thanh toán -> kết quả về `returnUrl` và **webhook** thiết lập trên my.payos.vn.
4. Đăng ký webhook: SDK `payos.webhooks.confirm("https://.../webhook")` (Node/Python); khi nhận, **luôn xác thực** bằng `webhooks.verify()` (dựa trên Checksum Key); sai chữ ký trả 400.
5. Môi trường thử: có mục "Môi trường test payOS" (nội dung chưa đọc được).
6. Giới hạn: gọi quá nhiều trả HTTP 429 (docs bắt đầu).
7. Cảnh báo chuỗi cung ứng: một trang Socket.dev hiển thị bài nghiên cứu về tấn công chuỗi cung ứng trên `axios` cạnh trang gói `@payos/node` (có thể chỉ là biểu ngữ chung). Không kết luận gói bị ảnh hưởng; khi cài SDK: ghim phiên bản, dùng lockfile, `npm audit`, đối chiếu repo chính hãng payOSHQ. Cần xác minh.
8. Lỗi hay gặp (kinh nghiệm chung, chưa kiểm): webhook URL chưa trả 200 khi confirm; sai Checksum Key (mỗi kênh một bộ khóa); nhầm khóa kênh này với kênh khác; `orderCode` trùng.
9. Thu hồi: đổi khóa trong kênh payOS, xoá kênh/webhook.

## 3. Stripe
Nguồn: https://docs.stripe.com/mcp (đọc đầy đủ).
Độ khó: Dễ (OAuth) / Vừa (khóa agent). Thời gian: 5-15 phút.
- Server từ xa: `https://mcp.stripe.com`. Claude Code: `claude mcp add --transport http stripe https://mcp.stripe.com/` rồi `/mcp` để đăng nhập OAuth. Claude Desktop/web: connector Stripe chính thức trong thư mục Claude, bấm **Connect**, đăng nhập Stripe, cấp quyền (bài Team/Enterprise: chủ gói phải thêm connector cho workspace trước).
- Cách nhanh cho máy phát triển: cài Stripe CLI rồi `stripe agent setup` tự cấu hình MCP và skill.
- OAuth cho phép chọn một hoặc nhiều tài khoản live hoặc sandbox và quyền khác nhau cho từng môi trường: nên nối **sandbox** trước.
- Khóa thay thế: **agent API key** (nhãn Agent trong Dashboard), cấp quyền tối thiểu, đặt qua biến môi trường: `.mcp.json` `"headers": {"Authorization": "Bearer ${AGENT_API_KEY}"}`.
- **Hạn chót 30/11/2026**: từ tháng 12 Stripe MCP ngừng nhận khóa bí mật toàn quyền và khóa giới hạn không có thẻ Agent; trả 401. Thay bằng khóa agent mới hoặc OAuth.
- Công cụ: tra API, đọc (`stripe_api_read`) và ghi (`stripe_api_write`) mọi phương thức, thông tin tài khoản, phân tích, tài liệu. **Treasury** (xem trước công khai): `send_money`, `transfer_money`, `convert_currency` có "xác nhận người thật". Với TISA BOT: TẮT hoặc không cấp quyền nhóm này; tạo hoàn tiền cũng cần xác nhận trên Dashboard.
- Xác nhận người thật: Stripe gửi URL để chủ bấm Approve trong Dashboard (hết hạn 24 giờ), rồi bảo AI thử lại.
- Quản lý/thu hồi: Dashboard > cài đặt người dùng > **OAuth sessions** > ⋯ > Revoke access; quản trị có thể thu hồi cho nhân viên và bật/tắt quyền MCP toàn đội ở dashboard.stripe.com/settings/mcp-and-cli-access.
- Lỗi hay gặp: IT chặn miền (nhờ cho phép `mcp.stripe.com`); 401 vì dùng khóa cũ sau hạn; làm trong live thay vì sandbox; prompt injection khi dùng chung server khác (bật chế độ duyệt từng tool).
- Kiểm tra nối thật: `get_stripe_account_info` hoặc đọc danh sách sản phẩm/số dư (chỉ đọc).

## 4. Việc chỉ người thật làm
Đăng ký, xác minh doanh nghiệp/ngân hàng, OTP ngân hàng, nhập thẻ/số tài khoản, duyệt hoàn tiền/chuyển tiền, nạp tiền, kích hoạt chế độ live, đồng ý điều khoản. AI không nhập khóa/token/thẻ hộ; chủ tự dán khóa vào chỗ cấu hình an toàn.

## 5. Thang chọn nhanh cho học viên bán hàng nhỏ
- Chỉ nhận chuyển khoản VN và đối soát: SePay (webhook) là đủ.
- Cần link thanh toán/QR cho đơn trên web: payOS hoặc SePay + QR.
- Thẻ quốc tế/đăng ký định kỳ: Stripe (kiểm tra điều kiện sử dụng tại Việt Nam: cần xác minh).
