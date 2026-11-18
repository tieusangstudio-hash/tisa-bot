# 12. Meta Ads: thiết lập đúng thứ tự trên Ads Manager, Marketing API, Meta Ads MCP (cập nhật 19/11/2026)

Nhãn: **[CT]** chính thức (tài liệu hoặc mô tả tool Meta), **[TC]** bên thứ ba, **[UL]** ước lượng, **[XM]** cần xác minh trên màn hình thật.
Nhãn giao diện tiếng Việt chỉ là bản dịch hay gặp; Meta đổi chữ thường xuyên: mọi nhãn tiếng Việt đều **[XM]**.

Nguyên tắc bất biến của TISA BOT: **không bao giờ đưa chiến dịch vào trạng thái chạy** nếu chủ chưa gõ "duyệt". Xem mục 4 về chế độ nháp (draft) của tool Meta, vì "PAUSED" và "DRAFT" không giống nhau.

---

## 1. Trình tự chuẩn (Ads Manager và API tương ứng)

| Bước | Ads Manager (nhãn tiếng Việt [XM]) | Marketing API / MCP | Kiểm tra trước khi qua bước kế |
|---|---|---|---|
| 0 | Chọn tài khoản quảng cáo, Page, tài khoản Instagram | `ads_get_ad_accounts`, `ads_get_ad_account_pages`, `ads_get_ig_accounts` | Đúng tài khoản/tiền tệ; đọc `min_daily_budget_cents`; Page có `leadgen_tos_accepted=true` nếu chạy biểu mẫu tức thì |
| 1 | **Tạo** > **Chiến dịch**: chọn **Mục tiêu** (Nhận biết, Lưu lượng truy cập, Tương tác, Khách hàng tiềm năng, Doanh số, Quảng bá ứng dụng) | `ads_create_campaign` / `POST act_{id}/campaigns` | Có `special_ad_categories` (bắt buộc, `[]` nếu không có) |
| 2 | **Danh mục quảng cáo đặc biệt** (hộp "Khai báo danh mục quảng cáo đặc biệt") | `special_ad_categories`, `special_ad_category_country` | Xem file 11 mục 4 và file 14 |
| 3 | **Ngân sách chiến dịch Advantage+** (bật = CBO), chiến lược giá thầu | `campaign_daily_budget`, `campaign_bid_strategy` | Ngân sách đúng đơn vị nhỏ nhất của tiền tệ |
| 4 | **Nhóm quảng cáo**: Vị trí chuyển đổi, Mục tiêu hiệu quả, Ngân sách & lịch | `ads_create_ad_set` | `optimization_goal` hợp lệ với mục tiêu và `destination_type` |
| 5 | **Đối tượng**: địa điểm, tuổi, ngôn ngữ; Đối tượng Advantage+ | `targeting` (JSON), `targeting_automation` | Địa điểm là cứng; tuổi tối thiểu ≤ 25 |
| 6 | **Vị trí hiển thị**: Vị trí Advantage+ (mặc định) | bỏ trống `publisher_platforms` và `*_positions` | Chỉ chọn tay khi chủ yêu cầu |
| 7 | **Quảng cáo**: danh tính (Page, Instagram), định dạng, nội dung, nút kêu gọi, trang đích/biểu mẫu | `ads_creative_upload_media` hoặc `ads_creative_upload_local_image`, `ads_create_creative`, `ads_create_ad` | Ảnh/video đã tải, `url_tags`, CTA đúng |
| 8 | **Theo dõi**: Pixel, tham số URL | `url_tags` ở creative, `tracking_specs` ở ad | UTM gắn xong trước khi tạo creative: sau này không sửa được [CT] |
| 9 | **Xem trước** | `ads_get_ad_preview`, `ads_get_ad_preview_screenshot` | Gửi chủ xem |
| 10 | Kiểm tra lỗi, chờ duyệt | `ads_get_ad_entities` (trường `effective_status`, `active_errors`), `ads_get_opportunity_score` | Không còn lỗi chặn |
| 11 | **Chủ gõ "duyệt"** | `ads_activate_entity` | Chỉ sau xác nhận bằng văn bản của chủ |

---

## 2. Bản đồ trường: Ads Manager, API, ghi chú

### 2.1 Chiến dịch (`ads_create_campaign`) [CT]
Bắt buộc theo schema tool: `ad_account_id`, `campaign_name`, `objective`, `buying_type` (mặc định đặt `AUCTION`).
- `objective`: chỉ nhận `OUTCOME_AWARENESS | OUTCOME_TRAFFIC | OUTCOME_ENGAGEMENT | OUTCOME_LEADS | OUTCOME_SALES | OUTCOME_APP_PROMOTION`. Mục tiêu cũ (`LINK_CLICKS`, `REACH`, `LEAD_GENERATION`...) bị từ chối.
- `special_ad_categories`: chuỗi JSON, mặc định `"[]"`. Giá trị: `NONE, EMPLOYMENT, HOUSING, FINANCIAL_PRODUCTS_SERVICES, ISSUES_ELECTIONS_POLITICS, ONLINE_GAMBLING_AND_GAMING`. `CREDIT` đã bỏ, dùng `FINANCIAL_PRODUCTS_SERVICES`. `HOUSING` gồm cả vay mua nhà.
- `special_ad_category_country`: mảng mã nước; mọi nước trong `geo_locations` của nhóm phải nằm trong danh sách.
- Ngân sách: **CBO** điền `campaign_daily_budget` (hoặc `campaign_lifetime_budget`), tính bằng đơn vị nhỏ nhất của tiền tệ, **không tự suy ra** số tiền hay chu kỳ: chủ chưa nói rõ thì hỏi. **ABO** để trống ba trường ngân sách/bid ở chiến dịch.
- `campaign_bid_strategy` (CBO): `LOWEST_COST_WITHOUT_CAP` (mặc định, khuyên dùng), `COST_CAP`, `LOWEST_COST_WITH_BID_CAP`, `LOWEST_COST_WITH_MIN_ROAS` (khi đó mỗi nhóm cần `bid_constraints.roas_average_floor`, tỷ lệ × 10000, vd 20000 = 2,00x).
- `promoted_object` chiến dịch: tùy chọn, dùng cho catalog (`product_catalog_id`).
- Tài liệu API thô: chỉ `special_ad_categories` bắt buộc; `status` khi tạo chỉ `ACTIVE`/`PAUSED`; ghi chú: tài liệu thô nói mặc định bid là `LOWEST_COST_WITH_BID_CAP` nếu bỏ trống, **trái với tool MCP** (mặc định `LOWEST_COST_WITHOUT_CAP`): luôn truyền tường minh [CT, 2 nguồn lệch nhau].
- Kết quả tạo chiến dịch trả về `valid_optimization_goals` và `recommended_optimization_goal`: chỉ dùng giá trị trong danh sách.

### 2.2 Nhóm quảng cáo (`ads_create_ad_set`) [CT]
Bắt buộc theo schema: `ad_account_id`, `campaign_id`, `ad_set_name`, `billing_event`, `optimization_goal`, `targeting`.
- `billing_event`: dùng `IMPRESSIONS` (hợp lệ cho mọi mục tiêu); mục tiêu khác như `LINK_CLICKS`, `THRUPLAY` chỉ đi với goal tương ứng.
- `optimization_goal` theo mục tiêu chiến dịch (mặc định ghi đầu):
  - `OUTCOME_TRAFFIC`: `LINK_CLICKS`, `LANDING_PAGE_VIEWS`, `OFFSITE_CONVERSIONS`, `IMPRESSIONS`, `POST_ENGAGEMENT`, `REACH`, `CONVERSATIONS`, `THRUPLAY`, `VISIT_INSTAGRAM_PROFILE`, `PROFILE_VISIT`, `QUALITY_CALL`, `REMINDERS_SET`.
  - `OUTCOME_ENGAGEMENT`: `THRUPLAY`, `POST_ENGAGEMENT`, `EVENT_RESPONSES`, `PAGE_LIKES`, `IMPRESSIONS`, `REACH`, `TWO_SECOND_CONTINUOUS_VIDEO_VIEWS`, `LINK_CLICKS`, `CONVERSATIONS`, `OFFSITE_CONVERSIONS`, `LANDING_PAGE_VIEWS`, `QUALITY_CALL`.
  - `OUTCOME_LEADS`: `OFFSITE_CONVERSIONS`, `LEAD_GENERATION`, `QUALITY_LEAD`, `LANDING_PAGE_VIEWS`, `LINK_CLICKS`, `IMPRESSIONS`, `REACH`, `VALUE`, `CONVERSATIONS` (chỉ đích có WhatsApp), `QUALITY_CALL`.
  - `OUTCOME_SALES`: `OFFSITE_CONVERSIONS`, `VALUE`, `LANDING_PAGE_VIEWS`, `IMPRESSIONS`, `POST_ENGAGEMENT`, `REACH`, `LINK_CLICKS`, `CONVERSATIONS`; đích `WEBSITE` thì **bắt buộc** `promoted_object` có `pixel_id` + `custom_event_type` (hoặc `custom_conversion_id`), hoặc `product_set_id`; nếu không có tín hiệu chuyển đổi thì dùng Traffic.
  - `VIDEO_VIEWS` đã bỏ: dùng `THRUPLAY`.
- `destination_type`: `WEBSITE, APP, MESSENGER, INSTAGRAM_DIRECT, WHATSAPP, PHONE_CALL, ON_AD, ON_EVENT, ON_PAGE, ON_POST, ON_VIDEO, INSTAGRAM_PROFILE, FACEBOOK_PAGE, INSTAGRAM_PROFILE_AND_FACEBOOK_PAGE, LEAD_FORM_MESSENGER`. Ghép bắt buộc: `CONVERSATIONS` đi với `MESSENGER/WHATSAPP/INSTAGRAM_DIRECT`; `POST_ENGAGEMENT`↔`ON_POST`; `PAGE_LIKES`↔`ON_PAGE`; `THRUPLAY`/`TWO_SECOND...`↔`ON_VIDEO`; thiếu thì lỗi "Performance goal isn't available".
- `promoted_object`: **bắt buộc** với `OFFSITE_CONVERSIONS, VALUE, LEAD_GENERATION, QUALITY_LEAD, APP_INSTALLS, PROFILE_VISIT, PROFILE_AND_PAGE_ENGAGEMENT`. Ví dụ: `{"pixel_id":"...","custom_event_type":"LEAD"}`; `{"page_id":"..."}` cho biểu mẫu/messenger. Chuỗi JSON. Tin nhắn: nếu bỏ `page_id`, tool tự suy từ Page chính của tài khoản: nên truyền tường minh.
- Ngân sách ABO: `daily_budget` hoặc `lifetime_budget` (cái sau cần `end_time`). Dưới mức tối thiểu của tiền tệ bị từ chối. Với VND, đơn vị nhỏ nhất và `min_daily_budget_cents` **[XM bằng `ads_get_ad_accounts`]** trước khi nhập.
- `targeting`: chuỗi JSON; xem mục 3.
- `attribution_spec`: **bỏ trống** (mặc định 7 ngày nhấp + 1 ngày xem khi mục tiêu hỗ trợ) trừ khi chủ yêu cầu.
- `bid_strategy`, `bid_amount`: chỉ ABO; `COST_CAP`/`LOWEST_COST_WITH_BID_CAP` bắt buộc `bid_amount`.
- Biểu mẫu: `LEAD_GENERATION`/`QUALITY_LEAD` cần Page đã chấp nhận Điều khoản Lead Ads: https://www.facebook.com/legal/leadgen/tos.
- EU: nhắm quốc gia EU cần `dsa_beneficiary`, `dsa_payor`; Việt Nam không cần.
- Thái Lan: tuổi tối thiểu cứng 20 (ghi chú tool) [CT]: không áp dụng cho Việt Nam.

### 2.3 Mẫu quảng cáo (`ads_create_creative`) [CT]
Bắt buộc: `ad_account_id`. Kiểu: ảnh đơn, video đơn, carousel tĩnh (`cards` 2 đến 10), nhiều phương tiện `multi_media` (2 đến 10, để Meta chọn), tùy biến theo vị trí `placement_customizations`, tăng cường bài đăng có sẵn `object_story_id`, bài Instagram `source_instagram_media_id`.
- Ảnh đơn: `page_id`, `link_url`, một trong `image_hash` hoặc `image_url` (không cả hai).
- Video đơn: `page_id`, `video_id` + ảnh bìa `image_hash`/`image_url` (bắt buộc); `description` cho video cần `link_url`.
- Nhiều biến thể chữ: `primary_texts`, `headlines`, `descriptions` (tối đa 5 mỗi loại; các biến thể phải khác nhau); **từ 2 biến thể trở lên chỉ chạy dưới Awareness, Engagement, Leads, Sales, không dưới Traffic** [CT].
- `call_to_action_type`: mã IN HOA chính xác. Tin nhắn: `MESSAGE_PAGE`; biểu mẫu: `LEARN_MORE` (mặc định), `SIGN_UP`, `APPLY_NOW`, `GET_QUOTE`, `GET_OFFER`, `SUBSCRIBE`, `DOWNLOAD`, `CONTACT`, `GET_IN_TOUCH`, `BOOK_TRAVEL`; đặt lịch: `BOOK_NOW`, `BOOK_A_CONSULTATION`, `MAKE_AN_APPOINTMENT`. Nút gọi điện (`CALL_NOW`...) tool này **không hỗ trợ**: tạo trong Ads Manager.
- `lead_gen_form_id`: ID biểu mẫu tức thì sở hữu bởi `page_id`, cho nhóm `ON_AD`; chỉ ảnh/video đơn; không đi với đích tin nhắn.
- `instagram_user_id`: bắt buộc nếu quảng cáo chạy trên Instagram (kể cả Advantage+ placements); lấy từ `ads_get_ig_accounts`. Thiếu thì không hiển thị trên Instagram.
- `url_tags`: chuỗi tham số UTM (vd `utm_source=meta&utm_medium=paid_social&utm_campaign={{campaign.name}}`), **không thể thêm sau khi tạo** [CT]; có thể chưa mở cho mọi ứng dụng: nếu bị từ chối thì dùng Ads Manager [XM].
- `self_ai_disclosure`: `OPT_IN` (có nội dung do AI bên thứ ba tạo/sửa) hoặc `OPT_OUT`; **không tự suy**, hỏi chủ; không sửa được sau khi tạo. Có hiệu lực ở EU, Ấn Độ, Đài Loan, California, New York [CT].
- Tăng cường Advantage+ Creative: mặc định có thể tự bật 3 tính năng (`inline_comment`, `image_brightness_and_contrast`, `enhance_cta`) trên creative mới (qua `ads_create_ad`); báo cho chủ và tắt bằng `advantage_plus_creative_defaults=OFF` nếu họ không muốn [CT].
- Lời chào Messenger: tool **không đặt** lời chào ở cấp mẫu; Page dùng lời chào mặc định. Muốn lời chào riêng/câu hỏi mồi: cấu hình ở Page hoặc dùng `page_welcome_message` qua API thô (mục 3.3). Tham số `messaging_destination_type` được nhắc trong mô tả tool nhưng **không thấy trong schema**: cần kiểm tra bằng một lần gọi thử ở chế độ nháp [XM].

### 2.4 Quảng cáo (`ads_create_ad`) [CT]
Bắt buộc: `ad_account_id`, `ad_set_id`, `ad_name`. `creative`: chuỗi JSON, một trong: `{"creative_id":"..."}` (khuyên dùng sau khi tạo bằng `ads_create_creative`), `object_story_id`, `object_story_spec` (phải có `page_id`), `source_instagram_media_id`, `asset_feed_spec`.
- Quảng cáo nhiều phiên bản trong 1 nhóm: tạo creative `multi_media` hoặc có `primary_texts/headlines`, rồi truyền `creative_id`. Nhóm `is_dynamic_creative=true` chỉ nhận đúng 1 quảng cáo.
- Creative khớp với đích và mục tiêu của nhóm; link click phải là link ngoài thật + CTA thật.
- Xem lại lỗi: đọc `active_errors`, sửa bằng `ads_update_entity` trước khi kích hoạt.

---

## 3. JSON mẫu (tên trường theo tool/API; ID là ví dụ giả)

### 3.1 Chiến dịch tin nhắn Messenger (Engagement), CBO
```json
{"ad_account_id":"1234567890","campaign_name":"MSG | Nhà phố | Gò Vấp | 2026-11",
 "objective":"OUTCOME_ENGAGEMENT","buying_type":"AUCTION",
 "special_ad_categories":"[]",
 "campaign_daily_budget":300000,"campaign_bid_strategy":"LOWEST_COST_WITHOUT_CAP"}
```
Ngân sách 300000 chỉ đúng nếu VND có đơn vị nhỏ nhất là 1 đồng: **[XM]**.

### 3.2 Nhóm quảng cáo tin nhắn (A+ audience, A+ placements, địa lý ghim)
```json
{"ad_account_id":"1234567890","campaign_id":"CAMP_ID","ad_set_name":"Rộng | Gò Vấp 5km | 28-55",
 "billing_event":"IMPRESSIONS","optimization_goal":"CONVERSATIONS",
 "destination_type":"MESSENGER","promoted_object":"{\"page_id\":\"PAGE_ID\"}",
 "targeting":"{\"geo_locations\":{\"custom_locations\":[{\"latitude\":10.84,\"longitude\":106.66,\"radius\":5,\"distance_unit\":\"kilometer\"}]},\"age_min\":22,\"age_range\":[28,55],\"targeting_automation\":{\"advantage_audience\":1}}"}
```
Không điền `publisher_platforms`/`*_positions` (Advantage+ placements); không điền `daily_budget` (đang CBO); không điền `age_max`. Tọa độ minh họa: lấy tọa độ thật của khu vực.

### 3.3 API thô: creative Click-to-Messenger [CT, doc click-to-messenger]
```json
{"name":"MSG creative 1","object_story_spec":{"page_id":"PAGE_ID","link_data":{
 "image_hash":"HASH","link":"https://www.facebook.com/PAGE_ID",
 "message":"Nhà phố Gò Vấp, 4 tầng, sổ hồng riêng, giá từ ... Nhắn để nhận bảng giá.",
 "call_to_action":{"type":"MESSAGE_PAGE","value":{"app_destination":"MESSENGER"}},
 "page_welcome_message":"Chào anh/chị, em gửi bảng giá và vị trí nhà ngay đây ạ."}}}
```
Ghi chú: tài liệu mẫu dùng `LEARN_MORE` cho ảnh/video nhưng ví dụ lead dùng `MESSAGE_PAGE`; cả hai cùng có `app_destination: "MESSENGER"`. Giới hạn: lời chào tối đa 300 ký tự; câu hỏi mồi `ice_breakers` tiêu đề 80, trả lời 300 ký tự. Nhóm quảng cáo thô: `destination_type=MESSENGER`, `optimization_goal=CONVERSATIONS`, `promoted_object={"page_id"}`, `billing_event=IMPRESSIONS`, `status=PAUSED`.

### 3.4 Chiến dịch Leads với biểu mẫu tức thì [CT, doc lead-ads create]
1. Chiến dịch `OUTCOME_LEADS`; nhóm `LEAD_GENERATION` hoặc `QUALITY_LEAD`, `destination_type=ON_AD`, `promoted_object.page_id`.
2. Biểu mẫu: `POST /{PAGE_ID}/leadgen_forms` với `name`, `questions` (`FULL_NAME`, `PHONE`, `EMAIL`, `CUSTOM` có `label`), tùy chọn `is_optimized_for_quality=true` (thêm bước xem lại, lead ý định cao hơn), `block_display_for_non_targeted_viewer`, `tracking_parameters`.
3. Creative: `call_to_action.value.lead_gen_form_id`; với API thô, `link` phải là `https://fb.me/`. Qua MCP: `lead_gen_form_id` trong `ads_create_creative` (tính năng bật theo từng ứng dụng, có thể bị từ chối) [XM].
4. Không hỏi trong biểu mẫu: số tài khoản, thông tin sức khỏe/tài chính nhạy cảm, mật khẩu... (file 14).

---

## 4. Trạng thái "PAUSED" và chế độ nháp của tool Meta Ads MCP (đọc kỹ)

Mô tả tool chính chủ có hai mô hình, và **mô tả tool tự mâu thuẫn một phần**:
- Mô tả mở đầu: "Creates ... in PAUSED state" cho campaign/ad set/ad.
- Cùng mô tả nói thêm **DRAFT MODE**: với tài khoản đủ điều kiện, tool **không tạo đối tượng thật** mà "xếp vào bản nháp Ads Manager", trả `status=DRAFT`; chỉ khi gọi `ads_activate_entity` trên chiến dịch thì **xuất bản** cả chiến dịch+nhóm+quảng cáo và **các đối tượng chạy ngay ở trạng thái ACTIVE** (không có bước "xuất bản rồi tạm dừng").
- Ngoài chế độ nháp: ad tạo ra là PAUSED trên tài khoản; "không có trường status khi tạo, muốn chạy phải gọi `ads_activate_entity`".
- Nguồn thứ ba nói mọi thứ tạo qua MCP/CLI mặc định PAUSED [TC, mcp.directory 29/04/2026].

Hệ quả cho TISA BOT:
1. Sau mỗi lần tạo, **luôn đọc lại** bằng `ads_get_ad_entities` (`object_ids`, đúng `level`, trường `effective_status`, `status`; với bản nháp dùng `object_state=draft`) và báo cho chủ: đang là DRAFT hay PAUSED.
2. **Không gọi `ads_activate_entity`** nếu chưa có câu "duyệt" của chủ **trong cuộc trò chuyện hiện tại**. Với bản nháp, kích hoạt = chạy thật ngay: coi như bật quảng cáo.
3. Nếu chủ muốn "duyệt nội dung nhưng chưa bật": để ở nháp/PAUSED, hướng dẫn mở Ads Manager xem bản nháp. Có tạo được chiến dịch thật ở trạng thái PAUSED trong chế độ nháp hay không: **[XM] trên tài khoản thật**.
4. Mỗi lần tạo/sửa: đọc `active_errors`; tool từ chối kích hoạt khi còn lỗi chặn.
5. Gọi `ads_get_opportunity_score` sau khi dựng xong để lấy gợi ý [CT].
6. Gửi ở mọi cuộc gọi: `client_conversation_id` (20 ký tự chữ-số, sinh một lần, dùng lại) và `advertiser_request` (nguyên văn lời chủ, không chứa tên/liên lạc). Không đưa tên chủ hoặc thông tin cá nhân vào các trường này.

---

## 5. Quyền, tài khoản, giới hạn

- Kết nối MCP chính chủ dùng OAuth Meta Business, ba mức quyền theo từng tài khoản: chỉ đọc, đọc/ghi, đọc/ghi/tài chính. Chọn mức hẹp nhất; **giao tác tạo quảng cáo cần mức đọc/ghi** [TC, mcp.directory 04/2026].
- Đường API thô cần `ads_management`, `pages_manage_ads`, `pages_read_engagement`, `pages_show_list` và mã thông báo Page có quyền `ADVERTISE` [CT].
- Tải ảnh qua MCP cần URL công khai; ảnh trên máy dùng `ads_creative_upload_local_image` hoặc CLI [TC].
- API v25.0 từ 18/02/2026; mọi phiên bản cũ chặn tạo/sửa ASC/AAC từ 19/05/2026 [CT].
- Meta Ads MCP không phơi bày nội bộ đấu giá/tối ưu; sửa cấu trúc có thể reset học [TC].

---

## 6. Lỗi hay gặp khi dựng

1. Thiếu `promoted_object` cho Sales/Leads trang web: lỗi "Performance goal isn't available".
2. Đặt `daily_budget` ở nhóm khi chiến dịch đã có ngân sách: tool từ chối.
3. `CONVERSATIONS` dưới `OUTCOME_LEADS` với đích Messenger: không hợp lệ.
4. Truyền ngân sách theo đơn vị sai (đồng vs nghìn đồng vs "cents"): luôn kiểm tra `ads_get_ad_accounts`.
5. Nhóm có 2 biến thể chữ trở lên dưới mục tiêu Traffic: bị từ chối.
6. Quên `instagram_user_id`: quảng cáo không lên Instagram.
7. Quên `url_tags` rồi mới nhận ra thì không bổ sung được.
8. Gọi kích hoạt để "thử xem trước": nó chạy thật.
9. Dùng `age_max`/`age_min` > 25 mà vẫn bật A+ audience (xem file 11).
10. Tự bịa ID sở thích/khóa địa điểm (tool cảnh báo sẽ bị từ chối).

---

## 7. Nguồn (truy cập 19/11/2026)

- Mô tả tool `ads_create_campaign`, `ads_create_ad_set`, `ads_create_creative`, `ads_create_ad`, `ads_create_custom_audience` của Meta Ads MCP chính chủ (đọc trực tiếp trong phiên).
- Meta, tạo chiến dịch/nhóm: https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group/ và https://developers.facebook.com/docs/marketing-api/reference/ad-campaign/
- Meta, Click to Messenger: https://developers.facebook.com/documentation/ads-commerce/marketing-api/ad-creative/messaging-ads/click-to-messenger.md
- Meta, Lead ads (tạo): https://developers.facebook.com/documentation/ads-commerce/marketing-api/guides/lead-ads/create.md
- Meta, Advantage+ campaigns: https://developers.facebook.com/documentation/ads-commerce/marketing-api/advantage-campaigns.md
- Meta, v25.0 changelog: https://developers.facebook.com/documentation/ads-commerce/marketing-api/marketing-api-changelog/version25.0
- Chỉ mục tài liệu Meta Ads and Commerce: https://developers.facebook.com/documentation/ads-commerce/llms.txt
- mcp.directory, Meta Ads AI Connectors (29/04/2026): https://mcp.directory/blog/meta-ads-cli-mcp

Xem thêm: 10 (chiến lược), 11 (target), 13 (đo lường), 14 (chính sách).
