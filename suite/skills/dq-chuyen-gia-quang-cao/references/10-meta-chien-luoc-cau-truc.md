# 10. Meta Ads: chiến lược, chọn mục tiêu, cấu trúc tài khoản (cập nhật 19/11/2026)

Dành cho: chuyên viên quảng cáo của TISA BOT, chủ doanh nghiệp nhỏ Việt Nam, ngân sách 200 đến 500 nghìn đồng/ngày.
Nhãn độ tin cậy dùng xuyên suốt:
- **[CT]** = tài liệu/công cụ chính thức của Meta.
- **[TC]** = kinh nghiệm thực chiến hoặc blog bên thứ ba, chưa có xác nhận của Meta.
- **[UL]** = ước lượng của tài liệu này, phải đối chiếu số tài khoản thật.
- **[XM]** = cần xác minh trên màn hình thật.

---

## 1. Bức tranh 2026 (đọc trước khi lên bất kỳ chiến dịch nào)

1. **Creative là targeting mới.** Meta nói trọng tâm đã chuyển từ nhắm đối tượng ngách sang đa dạng hóa nội dung quảng cáo; hệ thống truy xuất Andromeda chọn vài nghìn quảng cáo phù hợp từ hàng chục triệu ứng viên cho từng người [CT, qua tóm tắt của Jon Loomer]. Hệ quả: nhóm quảng cáo rộng, nhiều ý tưởng khác nhau thật sự.
2. **Entity ID.** Các nguồn thực chiến mô tả Andromeda gom các quảng cáo giống nhau (cùng khung hình, cùng nền, chỉ đổi chữ) thành một "thực thể". Tức 10 ảnh cùng một mẫu chỉ tính là 1 ý tưởng [TC; Meta không công bố ngưỡng. Con số "độ giống nhau trên 60% bị phạt" là của bên thứ ba, chưa có nguồn Meta].
3. **Advantage+ là mặc định.** Chiến dịch Sales, Leads, App theo cấu trúc Advantage+ khi bật đủ 3 cần gạt: ngân sách ở cấp chiến dịch, Advantage+ audience, Advantage+ placements. Từ API v25.0 (18/02/2026) không còn tạo được chiến dịch ASC/AAC kiểu cũ; sau 19/05/2026 áp dụng mọi phiên bản; v26.0 (dự kiến khoảng 09/2026; nay có thể đã phát hành, [XM]) sẽ tạm dừng các chiến dịch cũ còn lại [CT].
4. **Targeting chi tiết bị thu hẹp.** Một nguồn ghi Meta gỡ hàng chục nhóm sở thích chi tiết từ 15/01/2026, không có danh sách [TC, adlibrary; cần xác minh]. Quy tắc làm việc: đừng dựa vào sở thích; dựa vào địa lý, nội dung quảng cáo, tệp khách thật.
5. **Meta bỏ khuyến nghị tối đa 6 quảng cáo/nhóm** (theo Jon Loomer, "tháng 2", bài không ghi rõ năm) [TC]. Không có con số chính thức mới.
6. **Công cụ Meta Ads chính chủ (MCP/CLI)** ra mắt 29/04/2026, tạo chiến dịch/nhóm/mẫu ở trạng thái chờ, người phải kích hoạt [TC, mcp.directory]. Chi tiết trường ở file 12.

---

## 2. Chọn mục tiêu theo ngữ cảnh người bán Việt Nam

Nguyên tắc: chọn **hành động có giá trị gần tiền nhất mà ngân sách đủ để máy học**. Ngân sách nhỏ mà chọn sự kiện quá sâu (mua hàng, đặt cọc) thì không đủ tín hiệu, xem mục 4.

| Ngữ cảnh | Mục tiêu nên dùng (Ads Manager, nhãn tiếng Việt [XM]) | API | Khi nào dùng | Lưu ý |
|---|---|---|---|---|
| BĐS nhà phố, dịch vụ nhà ở, bán lẻ giá trị cao, khách quen chốt qua chat | **Tương tác (Engagement) > Tin nhắn**, tối ưu "Cuộc trò chuyện" | `OUTCOME_ENGAGEMENT`, `destination_type=MESSENGER`, `optimization_goal=CONVERSATIONS` | Mặc định cho kênh Messenger. Meta mô tả Engagement là điểm bắt đầu trực tiếp nhất cho doanh nghiệp mới [TC] | Tối ưu cuộc trò chuyện hút người hay nhắn nhưng ít mua; phải lọc bằng nội dung quảng cáo nêu rõ giá, khu vực |
| Cần khách để lại SĐT, đủ điều kiện mới báo giá (đào tạo, thiết kế, sửa nhà) | **Khách hàng tiềm năng > Biểu mẫu tức thì** | `OUTCOME_LEADS`, `destination_type=ON_AD`, `optimization_goal=LEAD_GENERATION` hoặc `QUALITY_LEAD` | Khi bạn gọi điện/Zalo lại cho khách được | Page phải chấp nhận Điều khoản Lead Ads. `QUALITY_LEAD` (Conversion Leads) cần dữ liệu CRM gửi về qua CAPI, xem file 13 |
| Có website/landing page, đo được sự kiện Lead | **Khách hàng tiềm năng > Website** | `OUTCOME_LEADS`, `destination_type=WEBSITE`, `OFFSITE_CONVERSIONS` + `pixel_id` + `custom_event_type=LEAD` | Có Pixel chạy đúng, đủ lượng sự kiện | Khâu cài đặt Pixel/CAPI là điều kiện, không phải tùy chọn |
| Bán sản phẩm online, có Pixel/catalog | **Doanh số (Sales)** | `OUTCOME_SALES`, `OFFSITE_CONVERSIONS` hoặc `VALUE`, với catalog thêm `product_set_id` | Có ít nhất vài chục đơn/tháng | Chưa đủ dữ liệu mua hàng thì Sales sẽ học rất chậm |
| Chốt qua Zalo | **Lưu lượng (Traffic)** tới liên kết Zalo, hoặc dẫn Messenger trước rồi mời kết bạn Zalo | `OUTCOME_TRAFFIC`, `LINK_CLICKS` | Click-to-message chỉ hỗ trợ Messenger, Instagram, WhatsApp, không có Zalo [TC, tương tự LINE] | Traffic chỉ tối ưu cú nhấp, không đo chất lượng; liên kết zalo.me có bị chặn không: [XM] |
| Tăng người theo dõi, bình luận, video | **Tương tác** (`THRUPLAY`, `POST_ENGAGEMENT`, `PAGE_LIKES`) | `OUTCOME_ENGAGEMENT` | Làm tệp remarketing, tăng uy tín trang. Không dùng làm nguồn khách chính | Dễ thu về lượt thích rẻ nhưng không ra khách |
| Giới thiệu thương hiệu, tạo tệp quảng bá | **Nhận biết** | `OUTCOME_AWARENESS`, `REACH`/`THRUPLAY` | Chỉ khi có ngân sách lớn; với 200 đến 500k/ngày không nên dùng làm chiến dịch chính | |

**Quy tắc chọn nhanh cho bot:**
- Chủ nói "kéo inbox" thì Engagement + Messenger. Chủ nói "lấy số điện thoại" thì Leads + biểu mẫu tức thì.
- Không chọn Sales khi chưa có Pixel chạy ổn và chưa có đơn thật.
- Dưới 2 chiến dịch đang chạy cùng lúc cho ngân sách dưới 500k/ngày, tránh chia nhỏ tín hiệu.

Ghi chú API [CT, mô tả tool Meta Ads MCP 19/11/2026]: dưới `OUTCOME_LEADS`, đích `MESSENGER` chỉ hỗ trợ `LEAD_GENERATION` (chat thu lead); tối ưu `CONVERSATIONS` dưới Leads chỉ với đích có WhatsApp. Messenger hội thoại thuần thì dùng `OUTCOME_ENGAGEMENT` (hoặc Sales/Traffic).

---

## 3. Cấu trúc tài khoản kiểu 2026 cho ngân sách nhỏ

### 3.1 Khung đề xuất (200 đến 500k/ngày)

```
Tài khoản
└── 1 chiến dịch "Khách mới" (Advantage+ nếu loại Leads/Sales; Engagement thì A+ audience + A+ placements)
    ├── Ngân sách: ở cấp chiến dịch (CBO) [mặc định của tool MCP]
    ├── 1 nhóm quảng cáo: tệp rộng theo địa lý, A+ audience, A+ placements
    │     └── 4 đến 8 quảng cáo, mỗi cái là MỘT ý tưởng khác hẳn
    └── (Tuần 3 trở đi, khi có dữ liệu) 1 chiến dịch "Remarketing": tệp nhắn tin/tương tác 30 ngày, ngân sách 15 đến 20% tổng
```

- **Số chiến dịch:** 1 đến 2. Đừng tách theo sở thích/độ tuổi như thời trước: Jon Loomer khuyên một chiến dịch/mục tiêu, hiếm khi nhiều nhóm theo targeting, dồn công sức cho quảng cáo [TC].
- **Số nhóm:** 1 (ngân sách dưới 300k) đến 2 (300 đến 500k, nếu thật sự có 2 khu vực/2 sản phẩm khác nhau).
- **Số quảng cáo/nhóm:** 4 đến 8 ý tưởng khác nhau cho ngân sách này. Các nguồn bên thứ ba khuyên 6 đến 8 tối thiểu, 15 đến 25 cho tài khoản chi trên 5.000 USD/tháng; không có số chính thức [TC]. Với 300k/ngày (~9 triệu/tháng, khoảng 350 USD) thì 15 mẫu là quá nhiều, mỗi mẫu không có đủ lượt hiển thị.
- **Đa dạng thật sự:** khác góc tiếp cận (giá, vị trí, pháp lý, câu chuyện khách), khác định dạng (video ngắn 9:16, ảnh 4:5, carousel), khác người nói/bối cảnh. Không chỉ đổi dòng chữ trên cùng một ảnh.

### 3.2 CBO hay ABO

| | CBO (ngân sách chiến dịch) | ABO (ngân sách nhóm) |
|---|---|---|
| Dùng khi | Mặc định; 1 đến 2 nhóm; muốn máy chia | Muốn kiểm tra riêng từng ý tưởng với ngân sách đều (mỗi nhóm 1 ý tưởng) |
| Tool MCP | Điền `campaign_daily_budget`, mặc định bid `LOWEST_COST_WITHOUT_CAP` | Để trống ngân sách chiến dịch, điền `daily_budget` ở nhóm. Tool từ chối nếu CBO mà nhóm cũng có ngân sách [CT] |
| Lưu ý | Một nhóm có thể "ăn" hết ngân sách; bình thường với 1 nhóm | Thử nghiệm kiểu ABO: 20 đến 50 USD/nhóm mỗi ngày theo bài The Optimizer [TC], quá lớn cho ngân sách 200 đến 500k; thu nhỏ: 1 chiến dịch thử riêng, 3 nhóm × 100k |

Với ngân sách chỉ 200 đến 500k: **CBO, 1 nhóm** là mặc định. Chỉ dùng ABO khi chủ muốn thử 3 ý tưởng lớn trong tuần đầu.

### 3.3 Giai đoạn học (learning phase)

- Mốc phổ biến: khoảng **50 sự kiện tối ưu/nhóm trong 7 ngày** để thoát học; có nhóm thoát ở 20 đến 30; nhãn "Học có giới hạn" là dự báo, không phải hình phạt [TC; mô tả chính thức cần xác minh tại Business Help Center, không tải được trang gốc ngày 19/11/2026].
- Công thức tham chiếu: ngân sách ngày tối thiểu ≈ chi phí mỗi kết quả mục tiêu × 50 ÷ 7.
- Chỉnh sửa lớn (đổi mục tiêu tối ưu, đổi mạnh ngân sách/đối tượng, thêm bớt quảng cáo nhiều) có thể reset học [TC]. Tài liệu hướng dẫn MCP cũng khuyên hạn chế đổi ngân sách và đối tượng [TC, mcp.directory].

### 3.4 Ví dụ tính nhanh [UL, thay bằng số thật của tài khoản]

| Mục tiêu tối ưu | Giả định chi phí/kết quả | 300k/ngày được | Một tuần | Thoát học? |
|---|---|---|---|---|
| Cuộc trò chuyện | 30.000 đ | ~10/ngày | ~70 | Có thể |
| Cuộc trò chuyện | 60.000 đ | ~5/ngày | ~35 | Sát ngưỡng |
| Khách tiềm năng (biểu mẫu) | 100.000 đ | ~3/ngày | ~21 | Khó, dễ "học có giới hạn" |
| Chuyển đổi web "Lead" | 150.000 đ | ~2/ngày | ~14 | Không, dùng sự kiện nông hơn |

Nếu ra "học có giới hạn": (a) hạ xuống sự kiện nông hơn, (b) gom nhóm lại, (c) tăng ngân sách, (d) bỏ bớt chỉnh sửa. Đừng tắt chỉ vì nhãn này [TC].

---

## 4. Luật tắt / giữ / tăng ngân sách (ngưỡng cụ thể)

Đặt **chi phí mục tiêu (CPA mục tiêu)** trước khi chạy = số tiền tối đa sẵn sàng trả cho 1 tin nhắn/lead đủ chuẩn. Chủ chưa có: hỏi "mỗi khách chốt được lãi bao nhiêu, bao nhiêu % tin nhắn thành khách" rồi tính. [UL cho mọi ngưỡng bên dưới, tổng hợp từ Corey Haines marketingskills (tăng ~20%, chờ 3 đến 5 ngày, không dừng trong lúc học) và bài The Optimizer].

| Tình huống | Hành động |
|---|---|
| Chưa chi đủ **2 ngày** và dưới **1.000 lượt hiển thị/mẫu** | GIỮ, chưa đánh giá |
| Chi ≥ **2 lần CPA mục tiêu**, 0 kết quả, CTR link < 0,5% | TẮT mẫu đó (không tắt cả nhóm nếu mẫu khác đã có kết quả) |
| Chi ≥ 2 lần CPA, 0 kết quả, CTR ổn (≥ 1%) | KIỂM TRA khâu sau click: trang đích, câu chào Messenger, tốc độ trả lời. Đừng tắt vội |
| CPA ≤ mục tiêu sau ≥ 3 ngày và ≥ 10 kết quả | GIỮ; sẵn sàng TĂNG |
| CPA ≤ 80% mục tiêu, ổn định 3 ngày liên tiếp | TĂNG ngân sách **20%**; chờ **3 đến 5 ngày** rồi mới tăng tiếp. Không tăng ≥30% một lần |
| CPA 100 đến 130% mục tiêu | GIỮ, kiểm tra chất lượng tin nhắn, thêm ý tưởng mới |
| CPA > 130% mục tiêu liên tục 5 ngày, đã qua học | THAY ý tưởng, không đổi đối tượng đầu tiên |
| Tần suất > 3 trong 7 ngày (đối tượng nhỏ) hoặc CPM tăng + CTR giảm 3 ngày | Nghi mỏi quảng cáo: thêm ý tưởng mới trước |
| Tin nhắn nhiều nhưng ≥ 70% là rác/hỏi giá rồi mất | Quảng cáo kéo sai người: nêu giá, khu vực, điều kiện rõ trong nội dung |

Quy tắc bắt buộc cho bot: mỗi thay đổi ngân sách/trạng thái cần chủ duyệt; không tự chạy lại sau khi tắt; ghi lý do và số liệu vào báo cáo.

Thứ tự kiểm tra hằng tuần [TC, Corey Haines]: chi tiêu, lưu lượng, kết quả, nội dung, trang đích, đo lường. Kết luận mỗi lần bằng một chữ: GIỮ, SỬA, THỬ hoặc ĐIỀU TRA. Đừng coi CPA tăng đột ngột là lý do tắt ngay: kiểm tra cỡ mẫu, độ trễ chuyển đổi, trạng thái học trước.

---

## 5. Lỗi hay gặp

- Chọn Sales/chuyển đổi sâu cho tài khoản mới, không đủ sự kiện nên học mãi.
- Chia 5 nhóm × 1 quảng cáo với ngân sách 300k/ngày: mỗi nhóm 60k, không nhóm nào thoát học.
- 10 ảnh cùng một khuôn đổi chữ, tưởng là đa dạng.
- Sửa nội dung/ngân sách mỗi ngày, liên tục reset học.
- Đo chiến dịch tin nhắn chỉ bằng "chi phí/tin nhắn" mà không ghi nhận tin nhắn nào thành khách.
- Không trả lời tin nhắn trong vài phút đầu: sự quan tâm cao nhất ngay lúc nhấp [TC, Relevant Audience].
- Đặt targeting quá hẹp theo sở thích cũ thay vì tin vào nội dung quảng cáo.

---

## 6. Nguồn (truy cập 19/11/2026 trừ khi ghi khác)

- Meta, API v25.0 changelog (18/02/2026): https://developers.facebook.com/documentation/ads-commerce/marketing-api/marketing-api-changelog/version25.0
- Meta, bài ASC/AAC (13/02/2026): https://developers.facebook.com/blog/post/2026/02/13/asc-and-aac-deprecation-mapi-v25/
- Meta, Advantage+ campaigns (cần gạt ngân sách/đối tượng/vị trí): https://developers.facebook.com/documentation/ads-commerce/marketing-api/advantage-campaigns.md
- Meta, Click to Messenger API: https://developers.facebook.com/documentation/ads-commerce/marketing-api/ad-creative/messaging-ads/click-to-messenger.md
- Mô tả tool `ads_create_campaign`, `ads_create_ad_set` của Meta Ads MCP chính chủ (đọc trực tiếp trong phiên).
- Jon Loomer, Andromeda: https://www.jonloomer.com/meta-andromeda/
- The Optimizer, kiểm thử creative sau Andromeda: https://theoptimizer.io/blog/how-to-test-ad-creatives-on-meta-after-the-andromeda-update-2026-playbook
- Corey Haines marketingskills, skill `ads` (qua bản mirror, file GitHub gốc không tải được): https://skills.sh/coreyhaines31/marketingskills/ads
- Relevant Audience, click-to-message: https://www.relevantaudience.com/facebook-ads/facebook-click-to-message-ads-guide/
- mcp.directory, Meta Ads AI Connectors: https://mcp.directory/blog/meta-ads-cli-mcp
- adlibrary, gỡ nhóm sở thích 01/2026 (độ tin cậy thấp): https://adlibrary.com/posts/meta-interest-targeting-removed

Xem tiếp: 11 (đối tượng), 12 (thiết lập), 13 (đo lường, thử nghiệm), 14 (chính sách).
