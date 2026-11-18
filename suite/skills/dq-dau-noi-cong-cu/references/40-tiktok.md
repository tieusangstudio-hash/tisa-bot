# 40 - Sổ tay đấu nối TikTok (Ads MCP, Marketing API, Content Posting API, Login Kit)

Ngày: 19/11/2026. Tài liệu TikTok chủ yếu là trang JavaScript nên một phần chỉ đọc được qua bài thứ ba. Chỗ nào chưa đối chiếu được ghi "cần xác minh".

## 1. Ba cửa vào
| Cửa | Mục đích | Độ khó |
|---|---|---|
| TikTok for Business MCP (Ads MCP) | Quản lý quảng cáo qua chat | Dễ |
| Marketing API (TikTok API for Business) | Chạy ads bằng mã/server riêng | Khó |
| Content Posting API (TikTok for Developers) | Đăng video/ảnh lên tài khoản TikTok | Khó (kiểm duyệt) |
Chi tiết MCP ads: `35-mcp-ads.md`. Phần này tập trung hai API còn lại.

## 2. Ads MCP - tóm tắt
- Endpoint flat `https://business-api.tiktok.com/open_mcp/tt-ads-mcp-flat`, layer `.../tt-ads-mcp-layer`. OAuth trên trình duyệt bằng tài khoản TikTok for Business. Hướng dẫn kỹ thuật chính hãng: https://business-api.tiktok.com/portal/docs/tiktok-ads-mcp-server/v1.3 (không đọc được trong đợt này).
- Hết ủy quyền sau 30 ngày theo [BLOG 17/08/2026]; cần xác minh.

## 3. Marketing API (TikTok for Business)
Nguồn đọc được: chỉ bài thứ ba (unified.to, docs.nexla.com, docs.treasure.ai, docs.owox.com); cổng chính hãng https://business-api.tiktok.com/portal/docs.
Quy trình người thật làm (cần xác minh giao diện):
1. Có tài khoản TikTok for Business + Business Center, quyền quản trị tài khoản quảng cáo.
2. Đăng ký tài khoản nhà phát triển ở cổng business-api.tiktok.com (Marketing API) -> tạo ứng dụng: tên, mô tả, mục đích, **Redirect URL**, chọn nhóm quyền (scope) cần dùng (Ads Management, Reporting...). Gửi **duyệt** ứng dụng (bài thứ ba: cần chương trình phát triển TikTok phê duyệt; thời gian không rõ, có thể nhiều ngày).
3. Nhà quảng cáo bấm link ủy quyền của app -> được `auth_code`.
4. Đổi mã lấy token: POST tới `/open_api/v1.3/oauth2/access_token/` với app id, secret, auth_code (từ bài thứ ba). Gọi `advertiser/get` để lấy danh sách advertiser_id đã ủy quyền.
5. Gọi API với header `Access-Token: <token>`.
- Thời hạn token Marketing API: chưa xác nhận bằng nguồn chính hãng (bài thứ ba: access ngắn, refresh khoảng 1 năm). Cần xác minh trên màn hình thật.
- Lỗi hay gặp (từ kinh nghiệm chung, chưa kiểm trong đợt này): sai advertiser_id (tài khoản chưa ủy quyền cho app), app chưa duyệt nên thiếu quyền, redirect URL không khớp, gọi vượt tần suất.

## 4. Content Posting API và Login Kit (TikTok for Developers)
Nguồn đọc trực tiếp: https://developers.tiktok.com/doc/content-posting-api-get-started ; https://developers.tiktok.com/doc/oauth-get-a-user-access-token ; https://developers.tiktok.com/doc/oauth-user-access-token-management.
1. developers.tiktok.com > đăng ký app: thêm sản phẩm **Content Posting API** và Login Kit; bật cấu hình **Direct Post**.
2. Scope: `video.publish` (đăng trực tiếp; cần được duyệt) và `video.upload` (đưa vào nháp; trang đã đọc không nói chi tiết: cần xác minh). Người dùng đích phải ủy quyền.
3. **Chưa qua audit = mọi nội dung chỉ ở chế độ riêng tư.** Phải qua audit của TikTok để đăng công khai. Có thể thử trước khi audit.
4. Đăng: gọi Creator Info trước (lấy mức riêng tư cho phép), rồi `/v2/post/publish/video/init/` (FILE_UPLOAD hoặc PULL_FROM_URL) hoặc `/v2/post/publish/content/init/` cho ảnh. Theo dõi bằng Get Post Status với `publish_id`.
5. Kéo từ URL và mọi ảnh phải từ **tên miền/tiền tố URL đã xác minh** trong cấu hình app.
6. Token: đổi code tại `POST https://open.tiktokapis.com/v2/oauth/token/` (form-urlencoded), tham số `client_key`, `client_secret`, `code`, `grant_type=authorization_code`, `redirect_uri` (phải KHỚP từng ký tự với lúc xin mã), `code_verifier` (bắt buộc với ứng dụng desktop/mobile, dùng PKCE).
7. Thời hạn (trang tài liệu fetch ngày 19/11/2026): **access token 2 giờ, refresh token 180 ngày**, refresh sẽ trả refresh token MỚI và vô hiệu cái cũ -> phải lưu lại mỗi lần. (Mâu thuẫn: một nguồn thứ ba ghi 24 giờ/1 năm; bản chính hãng đã đọc ghi 2 giờ/180 ngày. Xác minh lại.) Chỉ gọi endpoint token từ máy chủ (có client secret).
- Lỗi: `invalid_request` khi `redirect_uri` không khớp; thông báo lỗi có `error`, `error_description`, `log_id` (dùng `log_id` khi hỏi hỗ trợ).
- Sandbox, hạn mức đăng, thời gian audit: trang đã đọc không nêu -> cần xác minh trên màn hình thật.

## 5. Kiểm tra đã nối thật
- Ads MCP: liệt kê tài khoản quảng cáo/Business Center rồi lấy báo cáo 7 ngày.
- Marketing API: `advertiser/get` trả đúng danh sách tài khoản.
- Content Posting: Creator Info trả thông tin người dùng; thử đăng một video riêng tư (chủ duyệt), rồi Get Post Status.

## 6. Thu hồi
- Ads MCP/Marketing API: tại TikTok Ads Manager hoặc Business Center, mục ứng dụng/ủy quyền (cần xác minh trên màn hình thật); xoá token lưu trên máy.
- Content Posting: endpoint revoke theo tài liệu `oauth-revoke-a-user-access-token`; người dùng cũng gỡ trong cài đặt TikTok > Bảo mật > Quản lý quyền ứng dụng (cần xác minh).

## 7. Việc chỉ người thật làm
Đăng nhập TikTok, đồng ý điều khoản nhà phát triển, gửi hồ sơ duyệt/audit (có thể cần quay video demo), bấm cấp quyền, CAPTCHA/OTP, xác minh tên miền (DNS), thanh toán tiền quảng cáo.
