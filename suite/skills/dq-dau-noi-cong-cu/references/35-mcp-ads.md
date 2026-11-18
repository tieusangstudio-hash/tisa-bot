# 35 - MCP quảng cáo: Meta Ads, Google Ads, TikTok Ads

Ngày: 19/11/2026. Mục tiêu: nối được, phân biệt đọc/ghi, và luôn tạo chiến dịch ở trạng thái TẠM DỪNG để chủ duyệt.

## 1. Bảng so sánh nhanh
| Nền tảng | Server | Xác thực | Đọc/ghi | Độ khó | Thời gian |
|---|---|---|---|---|---|
| Meta | Chính chủ `https://mcp.facebook.com/ads` | OAuth (Facebook Login for Business) hoặc token | Đọc + ghi (cần `ads_management`) | Dễ (có thể chờ đợt bật) | 5-15 phút |
| Meta | Cộng đồng pipeboard-co/meta-ads-mcp | OAuth qua Pipeboard (bản host) hoặc app Meta riêng | Đọc + ghi, mặc định PAUSED | Dễ (host) / Khó (tự host) | 5 phút / 1 giờ+ |
| Google Ads | Chính chủ googleads/google-ads-mcp | gcloud ADC (OAuth) hoặc service account | Đọc (mặc định) + vài công cụ ghi có xác nhận | Khó | 1 giờ + chờ duyệt cấp truy cập |
| TikTok | Chính chủ TikTok for Business MCP | OAuth trình duyệt, không cần app dev | Đọc + ghi (~400 tool) | Dễ | 5-10 phút, gia hạn 30 ngày |

## 2. Meta Ads MCP chính chủ
Nguồn: https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-overview và ...-get-started; blog 16/07/2026.
- 7 nhóm công cụ: báo cáo, tạo/sửa quảng cáo-nhóm-chiến dịch, catalog, tín hiệu/dataset, trung tâm trợ giúp, A/B test và lift, nhật ký hoạt động.
- Nối: URL `https://mcp.facebook.com/ads` (không thêm `/` cuối hay đường dẫn). Claude Code có app riêng: `claude mcp add --transport http --client-id <META_APP_ID> meta-ads https://mcp.facebook.com/ads`. Không có app: thêm làm connector tuỳ chỉnh trong Claude, đăng nhập Facebook, tick đúng tài khoản quảng cáo (hướng dẫn BLOG 05/2026, màn hình có thể đã đổi: cần xác minh trên màn hình thật).
- Gói Claude miễn phí có thể giới hạn 1 connector tuỳ chỉnh; mục "Add custom connector" ẩn có thể do gói [BLOG].
- ĐỌC vs GHI: quyền tối thiểu `ads_mcp_management` + `ads_read` = chỉ đọc/báo cáo. Muốn tạo/sửa phải có `ads_management`. Cách an toàn: nối lần đầu chỉ với quyền đọc, kiểm tra, rồi mới nâng quyền nếu chủ yêu cầu (xem bảng quyền ở `30-meta-facebook-ads.md`).
- Rủi ro: [BLOG] thao tác ghi có hiệu lực ngay, không có chế độ nháp hay hoàn tác 1 chạm; vẫn qua kiểm duyệt quảng cáo của Meta; vẫn bị giới hạn tốc độ Marketing API; số liệu chi tiêu trễ. Tài liệu chính hãng không nêu "quy tắc giới hạn AI agent" rõ ràng.
- Cờ `is_ads_mcp_enabled: false` = tài khoản chưa được bật (triển khai theo đợt): vẫn thấy connector/OAuth/liệt kê tài khoản, nhưng truy vấn dữ liệu báo lỗi chưa bật.
- Token hết hạn có thể trả kết quả rỗng thay vì lỗi: nếu "tài khoản trống" lạ, nối lại.
- Thu hồi: gỡ connector ở Claude VÀ gỡ ứng dụng ở cài đặt tích hợp Meta (cần xác minh trên màn hình thật).

## 3. pipeboard-co/meta-ads-mcp
https://github.com/pipeboard-co/meta-ads-mcp (~1,4k sao, BSL 1.1).
- Host sẵn: `https://meta-ads.mcp.pipeboard.co/` (đăng nhập Facebook qua Pipeboard, không cần developer token). Cộng đồng, bên thứ ba giữ token của bạn: cân nhắc rủi ro; ưu tiên server chính chủ.
- Tự host: cần app Meta riêng, chạy streamable HTTP theo `STREAMABLE_HTTP_SETUP.md` của repo.
- Hành vi quan trọng: **chiến dịch, nhóm, quảng cáo mới mặc định PAUSED**; ngân sách tính bằng cent (đơn vị nhỏ nhất); mục tiêu phải kiểu `OUTCOME_*` (CONVERSIONS/LINK_CLICKS cũ gây lỗi 400); `bid_strategy` chỉ 4 giá trị; vài chiến lược cần `bid_amount`.
- Tên công cụ tiền tố `mcp_meta_ads_` (28 tool liệt kê, trang ghi lệch 42; cần xác minh).

## 4. Google Ads MCP chính chủ
Nguồn: https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server và https://github.com/googleads/google-ads-mcp (~1,2k sao).
- Chạy cục bộ stdio: `pipx run --spec google-ads-mcp==0.0.6 google-ads-mcp` (cần Python 3.10+ theo trang docs, README ghi 3.11+: dùng 3.11+; `pipx`; `gcloud`). Cấu hình `mcpServers` command `pipx`, env `GOOGLE_CLOUD_PROJECT`, `GOOGLE_APPLICATION_CREDENTIALS`.
- Đăng nhập: `gcloud auth application-default login --scopes=https://www.googleapis.com/auth/adwords,https://www.googleapis.com/auth/cloud-platform --client-id-file=client_secret.json` (OAuth client loại Desktop tạo trong dự án Cloud; thêm tài khoản vào Test users nếu consent screen đang Testing).
- Tài khoản quản lý (MCC): đặt `GOOGLE_ADS_LOGIN_CUSTOMER_ID` (10 số, không dấu gạch).
- Công cụ ĐỌC: `customers_list_accessible_customers`, `search_search` (câu lệnh GAQL), `metadata_get_resource_metadata`. Công cụ GHI (repo README): tạo asset, upload video (chỉ stdio), nhãn. Mọi thao tác ghi dùng luồng **đề xuất rồi xác nhận** với checksum: thiếu/sai checksum bị từ chối.
- Muốn chỉ đọc tuyệt đối: file `tools_config.yaml` bật `customers/search/metadata`, tắt `labels/assets`, đặt `GOOGLE_ADS_MCP_TOOLS_CONFIG`. Lưu ý: scope `adwords` vẫn rộng; "chỉ đọc" nằm ở bộ công cụ chứ không ở quyền OAuth.
- Quyền truy cập API: bật Google Ads API chỉ cho mức Test. Tài khoản thật cần mức Explorer/Basic/Standard của dự án Cloud, nếu không: lỗi `CLOUD_PROJECT_NOT_APPROVED_FOR_PRODUCTION` (hoặc `DEVELOPER_TOKEN_NOT_APPROVED` ở hướng dẫn cũ). Trang docs ghi Google khai tử developer token ngày 09/09/2026 và chuyển sang truy cập theo dự án Cloud: đã quá ngày, cần xác minh luật hiện hành trên màn hình thật. Duyệt có thể mất vài ngày [BLOG].
- Tên công cụ đổi từ v0.0.6 (có tiền tố như `search_search`): cập nhật danh sách cho phép.
- Gọi từ xa HTTP không có OAuth sẽ 401: dùng stdio cục bộ.
- Mẫu kiểm tra: gọi `list_accessible_customers`, rồi `search` một câu GAQL `SELECT campaign.name, campaign.status FROM campaign LIMIT 5`.

## 5. TikTok for Business MCP (TikTok Ads MCP)
Nguồn: https://ads.tiktok.com/resources/help/article/about-tiktok-for-business-mcp-server; blog 30/06/2026; hướng dẫn BLOG 17/08/2026 (mcpplaygroundonline).
- Hai endpoint: **flat** `https://business-api.tiktok.com/open_mcp/tt-ads-mcp-flat` (~400 tool, TikTok khuyên dùng với Claude) và **layer** `.../tt-ads-mcp-layer` (~40 tool lõi, tìm thêm theo nhu cầu; hợp khi ngân sách ngữ cảnh nhỏ).
- Nối: thêm URL làm server từ xa, lần đầu server trả 401, client dẫn tới màn hình đồng ý của TikTok Ads Manager -> người thật đăng nhập tài khoản TikTok for Business và bấm Cho phép. Không cần tài khoản developer hay app [BLOG].
- [BLOG] Ủy quyền hết hạn sau 30 ngày; khi quá hạn tác nhân có thể dừng giữa chừng mà không báo lỗi rõ: đăng nhập lại cùng tài khoản. Chưa thấy trong tài liệu chính hãng đã đọc: cần xác minh.
- Hạn chế đã báo: Smart+ (`smart_plus_ad_create/update/status_update`) giới hạn 1 thao tác/5 giây cho mỗi quảng cáo Smart+ (vòng lặp hàng loạt sẽ lỗi). Đầu 07/2026 Claude từng bỏ sót tool sau 256 tool đầu, đã sửa 20/07/2026: làm mới danh sách tool hoặc đổi sang endpoint layer. Ở endpoint flat mô hình có thể chọn nhầm tool mà không báo.
- Chưa thấy rõ quyền đọc/ghi tách bạch hoặc cách thu hồi trong trang chính hãng: cần xác minh trên màn hình thật (thu hồi nên làm ở TikTok Ads Manager > mục ứng dụng/ủy quyền).
- Không có hạn mức tốc độ công bố trong trang đã đọc.
- Hướng khác: Marketing API tự tạo app (`40-tiktok.md`).

## 6. Quy tắc đọc/ghi và TẠM DỪNG cho TISA BOT
1. Lần nối đầu: kiểm tra bằng công cụ đọc (liệt kê tài khoản + báo cáo 7 ngày).
2. Tạo chiến dịch: luôn ghi `status = PAUSED` rõ ràng (Meta chính chủ không đảm bảo mặc định; pipeboard mặc định PAUSED; TikTok chưa rõ). Sau khi tạo, đọc lại để xác nhận `PAUSED`, xem trước quảng cáo, rồi chờ chủ gõ "duyệt" mới bật.
3. Ngân sách và thời gian: đặt trần ngân sách ngày theo chỉ dẫn chủ; không sửa ngân sách bằng nhiều thao tác liên tiếp; tránh vòng lặp hàng loạt (giới hạn tốc độ).
4. Không tự bật chạy, không nạp tiền, không đổi phương thức thanh toán (người thật làm).
5. Mọi thao tác ghi: yêu cầu hiện nội dung sắp gửi cho chủ trước (đối tượng, ngân sách, nội dung chữ/ảnh).
6. Ghi nhật ký thay đổi (có công cụ nhật ký hoạt động của Meta).

## 7. Lỗi chung
- 401/Needs authentication: chưa đăng nhập hoặc hết ủy quyền -> `/mcp` đăng nhập lại.
- Tài khoản rỗng: sai Business/tài khoản đăng nhập, thiếu vai trò, hoặc token hết hạn.
- "Chưa bật tài khoản": Meta chưa mở cho tài khoản này.
- Giới hạn tốc độ: Meta 4/17, Inspector mã 11; chờ, gộp thao tác.
- Cài app 3 nơi (Meta/Google/TikTok): kiểm tra đúng profile Chrome đang đăng nhập.
