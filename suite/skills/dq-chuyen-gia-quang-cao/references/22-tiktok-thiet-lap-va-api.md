# 22 - TikTok Ads: thiết lập đúng thứ tự, Pixel/Events API, API/MCP, chính sách VN

Tra cứu ngày 19/11/2026. **[CH]** chính thức; **[BL]** bên thứ ba; **[UL]** ước lượng. TikTok Business API portal (business-api.tiktok.com/portal) hiển thị bằng JavaScript nên **không đọc tự động được**; phần tên trường/enum API dưới đây tổng hợp từ tài liệu bên thứ ba và hiểu biết chung, **đều phải xác minh với tài liệu API/Enumeration chính thức hoặc gọi thử với `validate`/tài khoản test trước khi dùng**.

## 1. Điều kiện trước khi lên chiến dịch

1. Tài khoản **TikTok For Business + Ads Manager** (advertiser) đã xác minh doanh nghiệp, có **phương thức thanh toán** (nạp trước hoặc thẻ). Với VN: đơn vị tiền, VAT/CIT xem [help: Vietnam VAT](https://ads.tiktok.com/help/article/vietnam-vat-cit?lang=en).
2. Tài khoản TikTok thương hiệu (cho Spark/identity); trang đích HTTPS có **thông tin doanh nghiệp** (tên, địa chỉ, SĐT, chính sách).
3. **Pixel** cài trên web (nếu có landing) và **nơi nhận lead** (xem file 21).
4. Có video (9:16) đã sẵn sàng, hoặc mã Spark.
5. Chủ xác nhận: mục tiêu, ngân sách/ngày, thời gian, đích nhận lead.

## 2. Thứ tự thiết lập trên Ads Manager (giao diện; cần xác minh trên màn hình thật)

1. **Create** > chọn **mục tiêu** (Lead generation / Website conversions-Sales / Traffic / Video views...). Có thể bật **Smart+** (automated) hoặc **Manual**.
2. **Chiến dịch:** đặt tên (quy ước: `TT | LeadGen | NhaPho-GoVap | 2026-11`), chọn ngân sách cấp chiến dịch (nếu dùng) - nhớ mức tối thiểu 50 USD (file 20).
3. **Nhóm QC:** (a) **Vị trí tối ưu**: Instant Form / Website / Messaging (Zalo); (b) Pixel + sự kiện tối ưu (nếu web); (c) **vị trí hiển thị** tự động; (d) **đối tượng** (vị trí, tuổi, ngôn ngữ...); (e) **ngân sách & lịch** (ngày bắt đầu, kết thúc; không chạy nối tiếp vô hạn khi chưa theo dõi); (f) **bid** (Maximum Delivery/Cost Cap).
4. **Quảng cáo:** chọn danh tính (tài khoản TikTok), thêm video (thư viện/Spark/dựng), **chữ quảng cáo** (khuyến nghị <= ~100 ký tự, tên hiển thị <= 40 ký tự [BL: adspirer docs]), nút **CTA**, đích (form/URL/Zalo), theo dõi (Pixel/UTM).
5. **Xem trước** các vị trí; kiểm tra chữ không bị che.
6. **Publish** => TikTok **duyệt** (thường trong ~24 giờ [CH: [first things to note](https://ads.tiktok.com/help/article/advertising-on-tiktok-first-things-to-note?lang=vi)]). Chạy thủ công **bằng giao diện** thì ở bước publish phải **chuyển trạng thái nhóm/quảng cáo sang tắt** nếu muốn giữ TẠM DỪNG; kiểm tra tab Campaign: trạng thái "Tắt/Off".
7. Chủ nói "duyệt" => bật; ghi giờ bật.

## 3. API (TikTok API for Business, v1.3) - bản đồ endpoint và trường

Xác thực: **access token** (OAuth do advertiser cấp quyền cho ứng dụng) gửi trong header `Access-Token`; Base `https://business-api.tiktok.com/open_api/v1.3/`; mọi lệnh có `advertiser_id`. [BL + SDK chính thức: [github.com/tiktok/tiktok-business-api-sdk](https://github.com/tiktok/tiktok-business-api-sdk) (Python/JS/Java, có `campaign_create`, `ad_aco_create`)]. **Cần ứng dụng được duyệt** (có thể 2-3 ngày làm việc [BL: mintmcp]) và token của advertiser; **bot không nhập hay in token**; lưu trong kho khóa của máy.

Thứ tự gọi: `campaign/create/` > `adgroup/create/` > (tải video: `file/video/ad/upload/`, ảnh bìa) > `ad/create/` > xem `campaign|adgroup|ad/get/` > bật bằng `.../status/update/` hoặc `update`.

| Bước | Endpoint | Trường chính (**xác minh enum**) |
|---|---|---|
| Chiến dịch | `POST campaign/create/` | `advertiser_id`, `campaign_name`, `objective_type` (REACH, TRAFFIC, VIDEO_VIEWS, ENGAGEMENT, LEAD_GENERATION, WEB_CONVERSIONS hoặc `CONVERSIONS` theo wrapper bên thứ ba, PRODUCT_SALES, APP_PROMOTION...), `budget_mode` (BUDGET_MODE_INFINITE / _DAY / _TOTAL), `budget` (khi cấp chiến dịch), `operation_status` = **`DISABLE`** |
| Nhóm QC | `POST adgroup/create/` | `campaign_id`, `adgroup_name`, `promotion_type` (WEBSITE/LEAD_GENERATION...), `placement_type`, `pixel_id`+`optimization_event` (web), `optimization_goal`(CLICK/CONVERT/LEAD_GENERATION/REACH/VIDEO_VIEW...), `billing_event` (CPC/OCPM/CPM/CPV), `bid_type`(no-bid/custom...), `bid_price`/`conversion_bid_price`, `budget_mode`, `budget`, `schedule_type`, `schedule_start_time`, `schedule_end_time`, `location_ids`, `age_groups`, `gender`, `languages`, `interest_category_ids`, `audience_ids`, `excluded_audience_ids`, `operating_systems`, `operation_status`=**`DISABLE`** |
| Quảng cáo | `POST ad/create/` | `adgroup_id`, `creatives[]`: `ad_name`, `identity_type`/`identity_id` (tài khoản TikTok), `ad_format`(SINGLE_VIDEO), `video_id`, `image_ids` (bìa), `ad_text`, `call_to_action`, `landing_page_url` hoặc form (`lead_gen_form_id`/`page_id` Instant Page), `tiktok_item_id` (Spark), `display_name`; trạng thái `operation_status`=**`DISABLE`** (**cần xác minh** trường này có ở cấp ad) |
| Bật/tắt | `POST campaign/status/update/`, `adgroup/status/update/`, `ad/status/update/` | `*_ids`, `operation_status` (ENABLE / DISABLE / DELETE) |
| Báo cáo | `GET report/integrated/get/` | `report_type=BASIC`, `data_level=AUCTION_CAMPAIGN/ADGROUP/AD`, `dimensions`, `metrics` (spend, impressions, clicks, ctr, cpc, cpm, conversion, cost_per_conversion, ...) |
| Tra cứu | `tool/region/`, `tool/interest_category/`, `tool/language/` | Lấy **mã vị trí** (`location_ids`: tra "Việt Nam"/"TP. Hồ Chí Minh"/"Gò Vấp" **không đoán mã**) |

Ghi chú thực tế:
- Wrapper bên thứ ba: mặc định tạo **bật** hay **tắt** khác nhau (ví dụ docs ghi mặc định DISABLE nhưng ví dụ lại ENABLE [BL: lava.so, adspirer]). => **Luôn đặt `operation_status` rõ ràng là `DISABLE` ở cả 3 cấp**, rồi **đọc lại (get)** để xác nhận trước khi báo chủ.
- Ngân sách: `budget` theo đơn vị tiền của tài khoản; wrapper khuyến cáo 20-50 USD/ngày tùy vùng; lỗi dưới mức tối thiểu sẽ trả mã lỗi: bắt lỗi và nói rõ với chủ.
- API Smart+ (tự động hóa) có tham số riêng cho chiến dịch Smart+; **chưa xác minh được** => dùng chiến dịch thủ công qua API, Smart+ làm trên giao diện.
- **Idempotency**: không gọi lặp khi lỗi mạng; đọc lại danh sách chiến dịch theo tên trước khi tạo lại (tránh nhân đôi chiến dịch thật).
- Báo cáo `conversion` đếm **sự kiện tối ưu đã chọn**, không đổi nghĩa với các định nghĩa khác (kiểm chứng 7/10/2026 trong tài liệu v1.3 [BL: AgriciDaniel/claude-ads/ads/references/tiktok-audit.md]).

## 4. MCP chính thức của TikTok for Business (cách khuyến nghị cho TISA BOT)

- TikTok ra **TikTok Ads MCP** (công bố khoảng 13/5/2026 tại TikTok World; **Agentic Hub** - chợ AI Skills - công bố 30/6/2026) [CH: [blog](https://ads.tiktok.com/business/en/blog/tiktok-agentic-hub-ai-agents-skills-mcp), [help](https://ads.tiktok.com/resources/help/article/about-tiktok-for-business-mcp-server)].
- Hai endpoint: **đầy đủ** `https://business-api.tiktok.com/open_mcp/tt-ads-mcp-flat` (~400 công cụ, cần ngữ cảnh lớn, khuyên dùng với Claude) và **tải dần** `https://business-api.tiktok.com/open_mcp/tt-ads-mcp-layer` (~40 công cụ lõi, khám phá thêm khi cần).
- Khả năng: tạo chiến dịch, báo cáo, chỉnh ngân sách/bid, đối tượng, tạm dừng nhóm, thao tác creative. Có connector trên Claude, Perplexity, Manus... Xác thực **OAuth qua trình duyệt** bằng tài khoản TikTok for Business, không cần tự quản API key (có nguồn bên thứ ba nói hiệu lực ~30 ngày phải cấp lại, nguồn khác nói không hết hạn: **cần xác minh**).
- Hướng dẫn kết nối chi tiết nằm ở trang "How to connect to TikTok for Business MCP Server" (chưa đọc được); địa chỉ hỗ trợ MCP có ghi trên trang blog Agentic Hub (xem link nguồn).
- **Rủi ro:** trang chính thức không mô tả cổng duyệt/phạm vi quyền; MCP có thể chạy tự động nhiều bước. => TISA BOT phải **tự áp luật**: (1) mọi lệnh tạo luôn kèm trạng thái tắt; (2) cấm gọi công cụ bật chạy/tăng ngân sách khi chủ chưa gõ "duyệt"; (3) in bản tóm tắt (đối tượng, ngân sách, video, link) trước khi tạo; (4) ghi nhật ký mọi lệnh ghi.
- Nhiều MCP "TikTok Ads" của cộng đồng (AdsMCP, PaidSync, markifact...) **không thuộc TikTok**; không dùng khi đã có bản chính thức, nếu dùng phải rà quyền và nguồn.

## 5. Pixel và Events API

- **Pixel** (mã web) gửi sự kiện từ trình duyệt: PageView, ViewContent, SubmitForm/CompleteRegistration/Lead, Contact, ClickButton... Với landing nhận form/Zalo: tối thiểu **PageView + sự kiện hoàn thành** (SubmitForm hoặc Lead) và nên gắn sự kiện **bấm nút Zalo/Gọi** (Contact) vì khách VN hay nhắn thay vì điền form [UL].
- **Events API** gửi từ máy chủ, chống mất dữ liệu do trình chặn/iOS; yêu cầu: gửi cả `ttclid`, email/SĐT băm SHA-256 (chuẩn hóa trước: chữ thường, số điện thoại E.164 như +84...) [CH: [Events API](https://ads.tiktok.com/help/article/events-api)].
- **Khử trùng lặp:** khi gửi **cùng một sự kiện** qua cả Pixel và Events API, phải dùng **cùng `event_id` và cùng tên sự kiện**; cửa sổ trùng lặp ~48 giờ; mỗi hành động thật một `event_id` duy nhất [CH: [event deduplication](https://ads.tiktok.com/help/article/event-deduplication)].
- Kiểm tra bằng **Events Manager > Test events** và theo dõi "Potential duplicate events". 
- Lead offline (chốt qua điện thoại): đẩy lại sự kiện "đã hẹn/đã chốt" (nếu có tính năng/CRM Events API) để tối ưu theo chất lượng; cần xác minh trên màn hình thật.
- Thiếu Pixel vẫn chạy Instant Form (TikTok tự đo lead trong form), nhưng không biết hành vi sau đó.

## 6. Chính sách quảng cáo hay gặp ở VN

Nguồn chính: [Ad policy index](https://ads.tiktok.com/help/article/ad-policy-handbook-metap?lang=en) (cập nhật 8/2025), [Financial services](https://ads.tiktok.com/help/article/tiktok-ads-policy-financial-services?lang=en), [Industries with certificate requirements - SEA/NEA](https://ads.tiktok.com/help/article/industries-with-certificate-requirements-sea-nea?lang=en), [HEC](https://ads.tiktok.com/help/article/housing-employment-credit-hec-ad-policy), [ad review checklist](https://ads.tiktok.com/help/article/ad-review-checklist?lang=vi).

- **Danh sách ngành cần giấy phép tại VN** (trang chính thức) gồm: ngân hàng, chứng khoán (SSC), y tế/thuốc/thiết bị y tế, thực phẩm chức năng/sữa, tuyển dụng/xuất khẩu lao động, mỹ phẩm, phân bón... **Không thấy BĐS và đào tạo trong danh sách** [CH, tra 19/11/2026]; nhưng chính sách chung vẫn bắt buộc **tuân thủ luật** và có giấy phép theo cơ quan địa phương. BĐS/đào tạo: cần xác minh trên màn hình thật nếu bị yêu cầu thêm giấy tờ.
- **Tài chính:** cấm hoặc hạn chế (sửa điểm tín dụng, làm giàu nhanh, đa cấp...). Quảng cáo "đầu tư BĐS sinh lời/cam kết lợi nhuận" dễ bị hiểu là dịch vụ tài chính/lừa đảo => **không viết**.
- **Hay bị từ chối:** cam kết tuyệt đối (100%, đảm bảo kết quả), "trước-sau" cường điệu, dữ liệu sai/không bằng chứng, **trang đích thiếu thông tin doanh nghiệp hoặc không khớp với quảng cáo**, liên kết gãy, nội dung thành phẩm khác với mô tả, nhạc không bản quyền, ảnh/video của người khác, từ ngữ nhạy cảm, gọi tên đối thủ [CH: ad review checklist; BL: megadigital.ai/vi/blog/nguyen-nhan-quang-cao-tiktok-khong-duyet].
- **BĐS (thực chiến [UL]):** nêu đúng thông tin pháp lý thật (sổ hồng/giấy tờ) và **không hứa lợi nhuận, không "quy hoạch sắp có" nếu chưa có văn bản**; tên dự án/chủ đầu tư phải đúng; giá phải khớp trang đích; không dùng hình dự án không phải của mình.
- **Đào tạo:** không hứa "chắc chắn có thu nhập X", không dùng lời chứng thực giả; có điều khoản học phí/hoàn tiền rõ.
- Nếu bị từ chối: xem lý do trong Ads Manager, sửa rồi nộp lại; không tạo hàng loạt tài khoản mới (vi phạm chính sách tài khoản). Theo dõi quy định VN (luật quảng cáo, kinh doanh BĐS); công ty TikTok VN từng bị phạt về vi phạm bảo vệ người tiêu dùng [BL: vietnamnet.vn].

## 7. Danh sách kiểm tra trước khi xin chủ duyệt

- [ ] Mục tiêu, đích lead, người nhận lead và thời gian phản hồi
- [ ] Ngân sách/ngày >= mức tối thiểu TikTok; tổng ngân sách thử; ngày bắt đầu/kết thúc
- [ ] Vị trí (mã đã tra), tuổi, loại trừ
- [ ] Video 9:16, phụ đề, nhạc hợp lệ, CTA, không cam kết bị cấm
- [ ] Trang đích/form kiểm thử; Pixel nhận sự kiện
- [ ] Trạng thái cả 3 cấp = DISABLE (đã đọc lại bằng `get`)
- [ ] Ghi lại ID chiến dịch/nhóm/quảng cáo và đường dẫn xem trước cho chủ
