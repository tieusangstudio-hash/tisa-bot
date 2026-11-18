# 32 - Google Ads: thiết lập đúng thứ tự, đo lường chuyển đổi, API và MCP

Tra cứu ngày 19/11/2026. **[CH]** chính thức; **[BL]** bên thứ ba; **[UL]** ước lượng. **Thay đổi lớn 2026: Developer Token đã bị khai tử (9/9/2026); quyền truy cập API nay gắn với Google Cloud project.** Xem mục 4.

## 1. Điều kiện và thứ tự thiết lập trên giao diện

1. **Tài khoản Google Ads** (chế độ chuyên gia, không dùng "Smart campaign" - API đã ngừng tạo Smart từ 23/9/2026), múi giờ/đơn vị tiền **VND** (không đổi được sau này), **thanh toán** (thẻ/chuyển khoản), hoàn tất **xác minh nhà quảng cáo** nếu được yêu cầu.
2. **Đo lường trước, chiến dịch sau**: tạo hành động chuyển đổi (mục 3) rồi mới tạo chiến dịch; nếu không, Smart Bidding "mù".
3. **Tạo chiến dịch** (Campaigns > New campaign) - thứ tự màn hình [cần xác minh trên màn hình thật]:
   1. Mục tiêu: **Leads** (hoặc "Tạo chiến dịch không cần mục tiêu") > loại **Search**.
   2. Cách đạt mục tiêu: chọn **Website visits/Phone calls/Form submissions** tùy đích.
   3. **Mục tiêu chuyển đổi** (chỉ để hành động **primary** quan trọng).
   4. Tên (quy ước: `GG | Search | NhaPho-GoVap | 2026-11`).
   5. **Giá thầu**: Maximize conversions (dữ liệu < 15-30/tháng), Maximize clicks (mới hoàn toàn, có trần CPC), hoặc Manual CPC (rất ít dữ liệu).
   6. **Mạng:** bỏ chọn **Search Partners** và **Display Network** khi chưa có bằng chứng.
   7. **Vị trí** (Presence), **lịch**, **thiết bị**; ngôn ngữ: xem file 31.
   8. **AI Max**: mặc định để TẮT với chủ mới; chỉ bật khi đủ điều kiện (file 30).
   9. **Ngân sách/ngày**.
   10. Nhóm quảng cáo > từ khóa (phrase/exact) > RSA > asset > **phủ định** > xem lại.
   11. **Publish** và **tạm dừng** ngay (hoặc đặt ngày bắt đầu tương lai). Cách an toàn: dựng bằng **Google Ads Editor** ngoại tuyến (trạng thái Paused) hoặc nhập CSV rồi mới **Post** [BL: goose-skills `google-search-ads-builder` xuất CSV Editor], hoặc dùng API tạo PAUSED (mục 4).
4. Chủ gõ "duyệt" => bật chiến dịch; ghi giờ bật và ngân sách.

## 2. Ngân sách khởi điểm và bid [UL, cần chủ chốt theo số liệu VN]

- Không có mức tối thiểu cho Search; **Demand Gen >= 5 USD/ngày** [CH: [dev blog](https://developers.google.com/ads/blog/posts/2026/02/minimum-budget-requirement-for-demand)], tương đương ~125.000đ; Google khuyên ngân sách Demand Gen khoảng **15 lần CPA mục tiêu** [CH: [Demand Gen API](https://developers.google.com/google-ads/api/docs/demand-gen/create-campaign)].
- Công thức khởi điểm Search: **ngân sách/ngày >= 10-20 click mong đợi x CPC trong Keyword Planner**, và nếu dùng Maximize conversions/tCPA: >= **3-5 lần CPA mục tiêu**/ngày (blog hãng, không phải ngưỡng bắt buộc [BL: groas.ai, techwyse]). Chưa có CPC VN cho "nhà phố Gò Vấp" trong các nguồn tìm được; benchmark BĐS Mỹ ~3,22 USD/click **không dùng cho VN** [BL: dev.to/localiq]. **Phải chạy Keyword Planner với VN/VND và ghi lại khoảng giá thầu.**
- Ngân sách có thể bị tiêu đến **2x/ngày** (Google cân bằng theo tháng) [BL: coreyhaines31].
- Bid theo lượng chuyển đổi/tháng của chiến dịch [BL: coreyhaines31, UL]: 0-15 => Manual CPC hoặc Maximize conversions không mục tiêu; 15-30 => Maximize conversions; 30+ ổn định => **Target CPA** bằng thực tế 30 ngày (+0-10%); có giá trị thật => Target ROAS. Đổi mục tiêu theo bước ±10-15%, chờ 1-2 tuần.
- Học Smart Bidding: tài liệu Google nói ~**7 ngày** hiệu chuẩn, có thể rút ngắn nếu có dữ liệu chuyển đổi lịch sử; "50 chuyển đổi" chỉ là quy tắc blog [CH: [help 13020501](https://support.google.com/google-ads/answer/13020501); BL: techwyse].

## 3. Đo lường chuyển đổi (làm TRƯỚC khi chạy)

**Hành động chuyển đổi:**
- **Gửi form** trên web (sự kiện thành công/trang cảm ơn). **Cuộc gọi**: (a) quảng cáo có call asset (cuộc gọi từ quảng cáo, đặt thời lượng tối thiểu, mặc định thường 60 giây [UL, cần xác minh]); (b) bấm số trên web (event). **Nhắn tin**: nhấp nút Zalo/Messenger = sự kiện tùy chọn (là chuyển đổi **phụ** để theo dõi, không dùng làm mục tiêu chính vì dễ bấm nhầm) [UL].
- Chỉ đặt hành động **primary** cho thứ gần doanh thu nhất (gửi form hoàn chỉnh/cuộc gọi đủ dài); các hành động nhẹ để **secondary**.

**Cài đặt kỹ thuật:**
- **Google tag** (gtag) hoặc **Google Tag Manager**; kiểm tra bằng **Tag Assistant**.
- **GA4** liên kết với Google Ads (nhập sự kiện từ GA4 hoặc dùng tag trực tiếp; không đếm hai lần cùng một sự kiện).
- **Enhanced conversions (nâng cao)**: gửi **email/SĐT băm** để khớp người dùng; từ 2026 các thiết lập web và lead hợp nhất thành **một công tắc** [BL: ppc.land]. Với lead gen: Google tag thu dữ liệu băm khi gửi form, sau đó tải chuyển đổi offline khớp danh tính; **vẫn nên gửi GCLID** [CH: [help 15713840](https://support.google.com/google-ads/answer/15713840)]. API v26 gỡ trường `enhanced_conversions_for_leads_enabled`, dùng `enablement_setting` [CH: release notes].
- **Offline conversions import (đẩy kết quả chốt về Google)**: tác động lớn nhất cho BĐS/đào tạo vì chốt qua điện thoại. Nguồn nói **từ 15/6/2026 import offline/enhanced for leads chuyển sang Data Manager API và bị chặn trong Google Ads API** [BL: tổng hợp từ ppc.land/relevantaudience, **cần xác minh**: ppc.land khác nêu "hạn chế import mới với token không hoạt động gần đây"]. Kiểm tra trên màn hình thật (Goals > Uploads) và docs Data Manager API trước khi hứa với chủ.
- **Chặn lead rác**: form có xác thực SĐT; không đo "xem trang"/"cuộn" như chuyển đổi.
- Kiểm thử: gửi form thật, xem **trạng thái hành động chuyển đổi = "Đang ghi nhận"**.

## 4. Google Ads API - truy cập (thay đổi 2026)

- **Developer Token đã khai tử 9/9/2026** (Google công bố; chuyển nhanh 10/9/2026): quyền truy cập nay gắn với **Cloud project**; header developer-token **không cần/được bỏ qua**; một phiên bản lớn tương lai sẽ từ chối token [CH: [access levels](https://developers.google.com/google-ads/api/docs/access-levels); BL: [ppc.land](https://ppc.land/google-drops-developer-tokens-from-ads-api-access-decisions/)].
- **Mức truy cập (theo Cloud project) [CH]:**
  - **Test**: tự có khi bật API; chỉ tài khoản **test**; 15.000 thao tác/ngày.
  - **Explorer**: tài khoản test + **thật**; tài khoản thật **2.880 thao tác/ngày**; **bị hạn chế**: tạo tài khoản, quản lý người dùng, **công cụ lập kế hoạch (Keyword Planner)**, thanh toán. Duyệt thường tự động.
  - **Basic**: 15.000 thao tác/ngày; cần **xác minh thương hiệu** (brand verification).
  - **Standard**: không giới hạn thao tác; cần kiểm toán thủ công ~10 ngày làm việc.
- Dự án Test gọi tài khoản thật trên v25+ => lỗi `CLOUD_PROJECT_NOT_APPROVED_FOR_PRODUCTION`; bản cũ `ACTION_NOT_PERMITTED`.
- **Chính sách 31/8/2026:** mỗi tích hợp phải dùng **Cloud project riêng** [BL: ppc.land]. Với TISA BOT (chạy trên máy từng học viên): thiết kế mô hình quyền (ai là chủ project/OAuth client) rõ ràng; cần xác minh với đội phát triển trước khi phát hành. Cấp độ tối thiểu hợp lý: **Explorer** cho tài khoản nhỏ.
- **Xác thực:** OAuth 2.0 (người dùng đồng ý, scope `adwords`) hoặc service account; header `login-customer-id` khi dùng tài khoản quản lý (MCC). **Bot không nhập/in/lưu bí mật trong prompt**; để người dùng đăng nhập qua trình duyệt, token lưu trong kho khóa hệ điều hành.
- Phiên bản mới nhất (tra 19/11/2026): **v26.2 (11/11/2026)**, v26 (14/10/2026), v25.2 (23/9/2026) [CH: [release notes](https://developers.google.com/google-ads/api/docs/release-notes)].

## 5. Tạo chiến dịch Search qua API (luôn PAUSED)

Dùng **một lệnh `GoogleAdsService.Mutate`** với ID tạm âm để các thực thể thành/bại cùng nhau [CH: [create campaigns](https://developers.google.com/google-ads/api/docs/campaigns/create-campaigns); Demand Gen doc xác nhận cách làm]. Thứ tự:

1. `CampaignBudget` (`name`, `delivery_method=STANDARD`, `amount_micros` = số tiền x 1.000.000, `explicitly_shared=false`).
2. `Campaign`: `name` (duy nhất), `advertising_channel_type=SEARCH` (bất biến), **`status=PAUSED`**, `campaign_budget`, giá thầu (`maximize_conversions` | `target_spend` (Maximize clicks, có `cpc_bid_ceiling_micros`) | `manual_cpc`), `network_settings` {`target_google_search=true`, `target_search_network=false`, `target_content_network=false`, `target_partner_search_network=false`}, `geo_target_type_setting.positive_geo_target_type=PRESENCE`, `contains_eu_political_advertising` (**bắt buộc ở bản cũ**, từ v26 tùy chọn nếu không nhắm EU) = `DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING`, ngày bắt đầu/kết thúc (`start_date_time`, `end_date_time`). Một số chiến dịch mới chỉ tạo được khi **tiêu chí đi kèm trong cùng request** [CH: release notes v26].
3. `CampaignCriterion`: vị trí (`location`/`proximity`), lịch (`ad_schedule`), **từ phủ định** (`negative=true`, `keyword`).
4. `AdGroup` (`status=PAUSED`, `type=SEARCH_STANDARD`, `cpc_bid_micros` nếu thủ công).
5. `AdGroupCriterion`: từ khóa (`keyword.text`, `match_type=PHRASE|EXACT`).
6. `AdGroupAd` (`status=PAUSED`): `ad.responsive_search_ad` {`headlines[]` (`text`, `pinned_field` tùy chọn), `descriptions[]`, `path1`, `path2`}, `final_urls`.
7. `Asset` + `CampaignAsset`/`AdGroupAsset`: sitelink, callout, call, lead form; liên kết cấp chiến dịch.

Lưu ý: đặt cả chiến dịch, nhóm và quảng cáo **PAUSED** (mặc định `ENABLED` nếu bỏ trống!). Sau khi tạo: truy vấn `GoogleAdsService.SearchStream` trên `campaign` để kiểm tra `campaign.status`, ngân sách, `network_settings`, **không kèm `segments`** (loại trừ chiến dịch chưa có hiển thị) [CH: create campaigns]. Dùng `validate_only=true` trước để kiểm tra không ghi. Bắt `PolicyViolationError`, `BUDGET_BELOW_DAILY_MINIMUM`, `RESOURCE_NOT_FOUND`. Không gọi lại khi timeout: đọc lại theo tên.

## 6. MCP

- **MCP chính thức Google `googleads/google-ads-mcp`** ([GitHub](https://github.com/googleads/google-ads-mcp), [docs](https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server)): chạy cục bộ bằng `pipx` (stdio) hoặc HTTP/Cloud Run. **Đọc**: liệt kê tài khoản, chạy GAQL (`search`), metadata. **Ghi hạn chế**: tạo **asset** (text/ảnh/video/sitelink/callout), tải video YouTube (chỉ stdio), nhãn. **KHÔNG tạo/sửa chiến dịch, nhóm, quảng cáo, ngân sách, giá thầu** [CH]. Ghi theo **Đề xuất rồi Xác nhận** (checksum), tắt ghi bằng `tools_config.yaml`. Biến môi trường chính: `GOOGLE_CLOUD_PROJECT`, `GOOGLE_APPLICATION_CREDENTIALS`, `GOOGLE_ADS_LOGIN_CUSTOMER_ID`; **không cần developer token**. Cần Python 3.10-3.11+, `gcloud auth application-default login` với scope Google Ads. Phiên bản ví dụ 0.0.5-0.0.6.
- Vì vậy để **tạo** chiến dịch phải dùng REST/thư viện Google Ads API (mục 5), MCP bên thứ ba, hoặc Google Ads Editor/giao diện. Đọc báo cáo bằng MCP chính thức là hợp lý.
- Tránh repo cũ `google-marketing-solutions/google_ads_mcp_server` (đã lưu trữ) [BL]. Các MCP cộng đồng: kiểm quyền, đừng cấp quyền ghi rộng.

## 7. Danh sách kiểm tra trước khi xin chủ duyệt

- [ ] Hành động chuyển đổi đang "ghi nhận", primary đúng
- [ ] Ngân sách/ngày, giá thầu, tổng ngân sách thử, ngày bắt đầu/kết thúc
- [ ] Vị trí (Presence), lịch, từ khóa (phrase/exact), phủ định >= 8
- [ ] RSA đủ 15/4 trong giới hạn ký tự, không cam kết sai; trang đích khớp
- [ ] Search Partners/Display tắt; AI Max tắt (hoặc ghi rõ vì sao bật)
- [ ] Chiến dịch + nhóm + quảng cáo = PAUSED (đã đọc lại); ghi ID

## Nguồn

- Tạo chiến dịch API: https://developers.google.com/google-ads/api/docs/campaigns/create-campaigns
- Access levels: https://developers.google.com/google-ads/api/docs/access-levels
- MCP: https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server ; https://github.com/googleads/google-ads-mcp
- Release notes: https://developers.google.com/google-ads/api/docs/release-notes
- Enhanced conversions for leads: https://support.google.com/google-ads/answer/15713840
- Tổng hợp thay đổi 2026: https://github.com/AgriciDaniel/claude-ads/blob/main/ads/references/google-audit.md (kiểm 12/10/2026)
