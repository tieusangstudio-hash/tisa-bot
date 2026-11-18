# 33 - Google Ads: Performance Max, Demand Gen, tối ưu hằng tuần, chỉ số

Tra cứu ngày 19/11/2026. **[CH]** chính thức; **[BL]** bên thứ ba; **[UL]** ước lượng. Tên menu/tính năng: "cần xác minh trên màn hình thật".

## 1. Khi nào dùng PMax / Demand Gen (thứ tự ưu tiên ngân sách)

Thứ tự giá trị cho chủ nhỏ [BL: coreyhaines31 playbook, UL]: **Search thương hiệu > Search ý định cao > remarketing > PMax > Demand Gen/nhận diện rộng.** PMax chỉ khi: đã có chuyển đổi sạch, có >= vài chục chuyển đổi/tháng, đủ creative (ảnh/video thật), ngân sách đủ lớn để Smart Bidding học. **Không chạy PMax làm chiến dịch đầu**, hay khi tracking yếu.

## 2. Performance Max (PMax)

**Yêu cầu asset của một nhóm asset (asset group) [CH: [API asset requirements](https://developers.google.com/google-ads/api/performance-max/asset-requirements), tra 19/11/2026]:**

| Loại | Giới hạn | Tối thiểu | Tối đa |
|---|---|---|---|
| Tiêu đề (HEADLINE) | <= 30 ký tự (ít nhất một cái <= 15 ký tự [BL, cần xác minh]) | 3 | 15 |
| Tiêu đề dài | <= 90 ký tự | 1 | 5 |
| Mô tả | <= 90 ký tự | 2 | 5 |
| Ảnh ngang 1.91:1 | 1200x628 (tối thiểu 600x314), <= 5120KB | 1 | 20 |
| Ảnh vuông 1:1 | 1200x1200 (tối thiểu 300x300) | 1 | 20 |
| Ảnh dọc 4:5 (tùy chọn) | 960x1200 | - | 20 |
| Logo vuông 1:1 | 1200x1200 (tối thiểu 128x128) | 1* | 5 |
| Logo ngang 4:1 (tùy chọn) | 1200x300 | - | 20 |
| Tên doanh nghiệp | <= 25 ký tự | 1* | 1 |
| Video YouTube | 16:9, 1:1 hoặc 9:16, **>= 10 giây** | - (nên có) | 15 |

\* bắt buộc khi tắt "brand guidelines"; khi bật, gắn `BUSINESS_NAME`/`LOGO` ở cấp chiến dịch. **Không có video thì Google tự tạo video từ asset** (thường kém) => tự cung cấp [CH + BL]. Một chiến dịch có tối đa 100 nhóm asset; một nhóm asset không dùng chung giữa chiến dịch. Chiến dịch không bán lẻ phải tạo **toàn bộ asset tối thiểu trong cùng một lệnh mutate** (không tạo rời) [CH].

**Tín hiệu đối tượng và search themes:** thêm **audience signal** (danh sách khách cũ, người truy cập web, đối tượng sở thích tùy chỉnh) và **search themes** (cụm từ gợi ý như "mua nhà phố Gò Vấp") để định hướng. Tín hiệu chỉ là **gợi ý**, không giới hạn phát hành [BL; chưa kiểm chứng trên tài liệu Google ở lần tra này - cần xác minh trên màn hình thật].

**Hàng rào bắt buộc [UL, theo playbook]:**
- Cài **loại trừ thương hiệu** (brand exclusions) cấp tài khoản/chiến dịch để PMax không ăn lưu lượng Search thương hiệu và "nhận công".
- Từ phủ định ngay từ ngày đầu (cấp chiến dịch/tài khoản).
- Nhập **chuyển đổi offline** trước khi mở rộng; kiểm tra chất lượng lead của PMax theo CRM: nếu lead PMax thành hẹn xem nhà chỉ bằng nửa Search thì PMax "rẻ trên báo cáo, đắt thật".
- **Final URL expansion** (mở rộng URL): tắt nếu có trang không muốn nhận lưu lượng (tuyển dụng, blog) hoặc dùng URL exclusions.
- Kiểm tra **chồng lấn Search-PMax**: Search exact thắng PMax khi cùng truy vấn [CH: help 13389795]; nhưng nghiên cứu hãng (Optmyzr 2/2025) cho thấy 91% tài khoản có chồng lấn từ khóa [BL].
- API: `advertising_channel_type=PERFORMANCE_MAX`, tạo AssetGroup + liên kết `AssetGroupAsset` (loại HEADLINE, LONG_HEADLINE, DESCRIPTION, MARKETING_IMAGE, SQUARE_MARKETING_IMAGE, LOGO, YOUTUBE_VIDEO, BUSINESS_NAME) trong **một mutate**; `status=PAUSED` ở chiến dịch và nhóm asset; v25.2 thêm tùy chọn URL cho AssetGroup (tracking template, final URL suffix) và cài đặt thu thập video tự động [CH: release notes].
- Smart campaign cũ => `GeneratePMaxDraftCampaign` (v25.2) tạo bản nháp PMax **paused, chưa hoàn chỉnh**; một số cờ chưa hỗ trợ.

**Lỗi hay gặp:** ảnh sai tỉ lệ (`ASPECT_RATIO_NOT_ALLOWED` khi liên kết, không khi tải lên); thiếu asset bắt buộc; dùng ảnh stock; không có logo; bỏ qua loại trừ thương hiệu.

## 3. Demand Gen (video và hình ảnh trên YouTube/Shorts/Discover/Gmail)

- **Vị trí:** YouTube Shorts, in-feed, Home, Watch next, Search; Discover; Gmail; đối tác video [CH: [help](https://support.google.com/google-ads/answer/13695777)]. Dùng để **tạo cầu** và **remarketing** người xem video/khách web.
- **Ngân sách tối thiểu 5 USD/ngày** (từ 1/4/2026); lỗi `BUDGET_BELOW_DAILY_MINIMUM` (v21+). Ngân sách không được dùng chung (`explicitly_shared=false`). Khuyến nghị ~**15 x CPA mục tiêu**/ngày [CH]; blog khác nêu 10x hoặc 100 USD/ngày là "sàn" thực chiến [BL: ppc.land]; với chủ nhỏ hãy bắt đầu bằng remarketing/đối tượng hẹp, không bật rộng.
- **Giá thầu hỗ trợ:** Maximize clicks, Maximize conversions, Target CPA, Target ROAS. Mới: **Maximize conversions**, chuyển sang tCPA/tROAS sau >= ~50 chuyển đổi [CH/BL].
- **Asset:** video (ngang/vuông/dọc, nên có >= 3 ngang + 3 dọc [BL, nguồn thứ hai]), ảnh 1.91:1, 1:1, 4:5; logo 1:1; tên doanh nghiệp. Loại quảng cáo API: `DemandGenVideoResponsiveAdInfo` (bắt buộc `business_name`; từ **v24 bắt buộc `videos` và `logo_images`**), `DemandGenMultiAssetAdInfo`, `DemandGenCarouselAdInfo`, `DemandGenProductAdInfo` (có feed) [CH: [Demand Gen API](https://developers.google.com/google-ads/api/docs/demand-gen/create-campaign)]. **Điều khiển kênh** ở cấp nhóm QC (`channel_controls.selected_channels`: Gmail, Discover, Display, YouTube in-feed/in-stream/Shorts) => cho chủ nhỏ thường chỉ bật **YouTube + Shorts**.
- **Tạo API:** một mutate, ID tạm; chiến dịch `advertising_channel_type=DEMAND_GEN` (không đặt subtype), nhóm QC **không đặt `AdGroupType`**; đối tượng/vị trí/ngôn ngữ ở cấp nhóm QC; chiến dịch **PAUSED**; **các ví dụ chính thức tạo nhóm/quảng cáo ở ENABLED nên bot phải đặt PAUSED**. Chiến dịch Video Action cũ nâng cấp thành Demand Gen: bản nâng cấp bắt đầu **PAUSED**, kích hoạt chỉ khi chiến dịch gốc đã bị gỡ (lỗi `CANNOT_ACTIVATE_MIGRATED_CAMPAIGN` v26+).
- **v26.2:** tự động hóa chữ phủ lên video (`OVERLAY_TEXT_ON_VIDEOS`) **mặc định bật** cho Demand Gen video mới => kiểm tra/tắt nếu muốn kiểm soát chữ [CH: release notes].
- **Lead form** dùng được với Demand Gen; yêu cầu và giới hạn **cần xác minh trên màn hình thật**.

## 4. AI Max cho Search (tóm tắt thực hành)

Xem thêm file 30. Khi dùng: ngân sách **không bị giới hạn**; kiểm tra **báo cáo AI Max** (kiểu so khớp "AI Max", cột nguồn, báo cáo trang đích "Selected by", báo cáo asset); loại trừ URL/ thương hiệu; kiểm tra tracking template để tránh 404; chạy **thử nghiệm A/B** (experiment) với bản không AI Max. API: `Campaign.ai_max_setting.enable_ai_max=true`, `TEXT_ASSET_AUTOMATION=OPTED_IN`; v25.1 thêm `broad_match_migration_date_time`/`aca_migration_date_time` [CH: release notes].

## 5. Chỉ số theo dõi

| Chỉ số | Cách đọc |
|---|---|
| **CTR** | Search ý định cao thường 2-6% (B2B, tham khảo); thương hiệu 8-20% [BL: coreyhaines31 playbook; **không phải VN**] |
| **CPC** | So với khoảng giá Keyword Planner; CPC tăng đột biến = chất lượng/cạnh tranh |
| **CVR** | Chuyển đổi/click; Search 3-10% (B2B tham khảo) [BL]; BĐS thực tế thường thấp hơn; so trong tài khoản |
| **CPA/CPL** | So với **CPA chấp nhận được** do chủ cung cấp |
| **Impression share** | **Lost IS (budget)** vs **Lost IS (rank)**: thiếu ngân sách hay thiếu Ad Rank - khác cách sửa |
| **Quality Score** | Sửa thành phần yếu (CTR dự kiến/liên quan/trang đích) |
| **Search terms** | Cột quan trọng nhất cho Search/AI Max |
| **Chất lượng lead** | Tỷ lệ nghe máy, hẹn xem nhà, chốt (từ CRM) |

Bảng điểm tuần gồm đúng 8 số: **chi tiêu, lead, CPL, % lead thành hẹn (CRM), số hẹn, chi phí/hẹn, impression share Search, top cụm từ lãng phí** [BL: coreyhaines31, đã rút gọn].

## 6. Luật tối ưu hằng tuần (khởi điểm [UL])

1. **Thứ Hai - cụm từ tìm kiếm** (3 lượt): (a) **Lãng phí**: >= 3 click, 0 chuyển đổi, không liên quan => thêm phủ định; (b) **Thắng**: cụm đã chuyển đổi chưa là từ khóa => thêm Exact/Phrase; (c) **Trôi**: broad/AI Max khớp ý khác => siết kiểu so khớp/phủ định.
2. **Chuyển đổi:** xác nhận hành động còn "ghi nhận"; so lead Google với CRM. Nếu lệch > 20-30% => kiểm tra gắn tag/GCLID.
3. **Giá thầu/ngân sách:** đổi **một thứ mỗi lần**, ±10-20%, chờ 1-2 tuần; không đổi trong thời gian học (khoảng 7 ngày). Nếu "bị giới hạn ngân sách" và CPA đạt => tăng ngân sách (CPA thường **giảm** khi bỏ giới hạn).
4. **Quảng cáo:** tắt RSA/tiêu đề "Kém" lâu sau >= vài nghìn hiển thị; giữ 2-3 RSA/nhóm; viết biến thể mới theo mẫu thắng.
5. **Trang đích:** CVR thấp + CTR tốt => sửa trang/form trước khi tăng ngân sách.
6. **Lịch/thiết bị/vị trí:** sau >= 2 tuần mới điều chỉnh; cắt vị trí/giờ có chi lớn, không lead.
7. **Gỡ rủi ro:** nếu 14 ngày chi >= 2-3 x CPA chấp nhận được mà 0 lead => tạm dừng và báo chủ nguyên nhân (từ khóa, trang, tracking).
8. **Tháng:** xem lại nhóm cấu trúc, gộp chiến dịch < 15-30 chuyển đổi/tháng.

**Lỗi hay gặp:** sửa mọi thứ mỗi ngày; tin "đề xuất tự động" của Google (nhiều đề xuất nhằm tăng chi tiêu); thêm từ khóa broad hàng loạt; không kiểm tra cụm từ tìm kiếm; dùng PMax thay Search khi chưa đủ dữ liệu.

## 7. Chính sách và rủi ro (tóm tắt)

- **Xác minh nhà quảng cáo** quá hạn => có thể bị tạm dừng tài khoản [CH: [verification programs](https://support.google.com/adspolicy/topic/9646742?hl=vi)].
- BĐS/đào tạo: tránh cam kết lợi nhuận/thu nhập, khẳng định không chứng minh, dùng hình ảnh không có quyền; thông tin pháp lý/giá phải khớp trang đích.
- **Cuộc gọi:** call-only ads ngừng phát 2/2027; dùng call asset trong RSA.
- Xem file 31 (mục 6) về lý do từ chối phổ biến.

## 8. Việc cần xác minh trên màn hình thật

- PMax/Demand Gen có ẩn/hiện loại, tên menu và mục tiêu cho tài khoản VN (VND).
- Lead form assets ở VN; mức tối thiểu cuộc gọi; tên hành động chuyển đổi.
- Giới hạn ngân sách tối thiểu bằng VND cho Demand Gen (`CurrencyConstant.demand_gen_info.minimum_budget_per_day_micros`, v26+).
- Audience signals/search themes (cách Google mô tả chính thức); tính năng URL exclusions.
- Trạng thái Data Manager API cho offline conversions.

## Nguồn

- PMax asset requirements: https://developers.google.com/google-ads/api/performance-max/asset-requirements
- Demand Gen API: https://developers.google.com/google-ads/api/docs/demand-gen/create-campaign
- Demand Gen budget: https://developers.google.com/ads/blog/posts/2026/02/minimum-budget-requirement-for-demand
- Demand Gen help: https://support.google.com/google-ads/answer/13695777
- AI Max help: https://support.google.com/google-ads/answer/15910187
- Release notes: https://developers.google.com/google-ads/api/docs/release-notes (v26.2, 11/11/2026)
- Playbook Search: https://github.com/coreyhaines31/marketingskills/blob/main/skills/ads/references/google-search-playbook.md
