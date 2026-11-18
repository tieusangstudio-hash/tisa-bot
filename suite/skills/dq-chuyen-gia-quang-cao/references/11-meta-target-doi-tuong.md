# 11. Meta Ads: target và đối tượng (cập nhật 19/11/2026)

Nhãn: **[CT]** chính thức Meta, **[TC]** thực chiến/bên thứ ba, **[UL]** ước lượng, **[XM]** cần xác minh trên màn hình thật.

---

## 1. Cách Meta hiểu "đối tượng" năm 2026

Khi bật **Advantage+ audience** (mặc định, nhãn tiếng Việt thường là "Đối tượng Advantage+" [XM]), hệ thống tự tìm người có khả năng làm hành động mục tiêu và coi lựa chọn của bạn là **gợi ý**, không phải rào chắn [CT, mô tả tool `ads_create_ad_set`].

| Nhóm | Gồm | Hành vi |
|---|---|---|
| **Kiểm soát cứng** (Controls) | Vị trí địa lý, ngôn ngữ, độ tuổi tối thiểu (từ 18 đến **25**), loại trừ tệp (excluded custom audiences), danh mục quảng cáo đặc biệt | Luôn được tuân thủ |
| **Gợi ý** (Suggestions) | Độ tuổi tối đa (hàm ý: không nên đặt `age_max`), giới tính, sở thích/hành vi, tệp tùy chỉnh, tệp tương tự | Meta có thể phục vụ ngoài nhóm này nếu dự đoán tốt hơn |

Nguồn: tool MCP chính chủ (`age_min` đến 25 là cứng, bỏ `age_max`), Linear Design (cùng cách chia) [CT + TC].

**Khi nào PHẢI tắt Advantage+ audience** (`targeting_automation.advantage_audience = 0`, kèm `advantage_audience_off_reason`) theo tool chính chủ:
1. Chủ yêu cầu tắt, hoặc muốn dùng kiểm soát thủ công.
2. Chủ nói rõ người ngoài một độ tuổi **không được** thấy quảng cáo, mà mức đó là tối đa dưới 65 hoặc tối thiểu trên 25 (vd: khóa học dành riêng cho 30 đến 55).
3. Nhóm chỉ được phép chạy cho một tệp (remarketing thuần: khách đã nhắn tin, người xem trang, danh sách khách).
4. Backend báo A+ không khả dụng.

**Không phải lý do để tắt:** "khách của tôi là nữ 25 đến 45", chọn placement thủ công, dùng tệp tương tự để tiếp cận người mới, danh mục đặc biệt đơn thuần. Dùng độ tuổi/giới tính làm **gợi ý** (`age_range`: [30,50]) thay vì cứng [CT].

---

## 2. Địa lý: quận huyện cho BĐS và dịch vụ địa phương

Đây là phần quan trọng nhất cho nhà phố và dịch vụ tại chỗ vì vị trí là kiểm soát cứng.

**Các cấp địa lý trong `geo_locations`** [CT, Marketing API basic targeting]:
- `countries`, `regions` (tỉnh/thành; tối đa 200), `cities` (kèm `radius` 10 đến 50 dặm hay 17 đến 80 km, `distance_unit`; tối đa 250).
- `custom_locations`: ghim tọa độ hoặc `address_string` với `radius` 1 đến 80 km (0,63 đến 50 dặm), `distance_unit`, `name`.
- `location_types`: chỉ còn `home` (sống ở đây) và `recent` (vừa ở đây); mặc định cả hai. Có thể chọn riêng `home` để loại khách du lịch.
- Loại trừ địa lý: `excluded_geo_locations`.

**Cách dùng thực tế [UL + XM]:**
- Nhà phố theo quận (Gò Vấp, Quận 12, Tân Bình): thả ghim vào khu vực/dự án + bán kính **2 đến 5 km** (khu dân cư dày), hoặc chọn cả quận nếu Ads Manager cho chọn dưới dạng thành phố/khu vực con. Meta có tìm được "quận" làm địa điểm ở Việt Nam không và dưới dạng nào: **[XM]**, dùng công cụ tìm kiếm địa điểm trong Ads Manager rồi lấy khóa thật; không tự bịa khóa.
- Khách hay tìm nhà khu mình ở nhưng sống nơi khác: thêm ghim/bán kính lớn hơn hoặc cả TP.HCM, với nội dung nêu rõ khu vực để tự lọc.
- Dịch vụ tại nhà (sửa chữa, thiết kế): bán kính 5 đến 10 km quanh cơ sở.
- Đào tạo online: cả nước, hoặc TP lớn; nội dung nêu rõ online/offline.
- **Không đặt Danh mục đặc biệt Nhà ở khi chỉ chạy tại Việt Nam**, xem mục 4.

**Ngôn ngữ:** `locales` (tiếng Việt) là kiểm soát cứng; chỉ đặt khi khách thật sự chỉ đọc tiếng Việt, vì người Việt ở nước ngoài/dùng giao diện tiếng Anh sẽ bị loại [XM, không có số liệu].

---

## 3. Chọn tệp theo từng loại sản phẩm

Quy ước: **A** = tệp rộng theo địa lý (khách mới); **B** = tệp tùy chỉnh (remarketing); **C** = tệp tương tự.

| Sản phẩm | Khách mới (A) | Remarketing (B) | Tệp tương tự (C) | Ghi chú |
|---|---|---|---|---|
| BĐS nhà phố giá trị cao | Rộng theo khu vực + A+ audience; gợi ý tuổi 28 đến 55; để nội dung lọc | Người nhắn tin/tương tác trang 30 đến 90 ngày; người xem ≥ 50% video | Chỉ khi có ≥ 100 khách thật trong tệp nguồn | Chu kỳ chốt dài: remarketing 60 đến 90 ngày |
| Khóa học, đào tạo | Rộng cả nước/TP lớn; gợi ý tuổi theo chân dung học viên | Người xem video, người nhắn tin, người điền biểu mẫu chưa chốt | Từ danh sách học viên cũ | Cảnh giác chính sách thu nhập/cam kết (file 14) |
| Dịch vụ địa phương (spa, sửa chữa, thiết kế) | Bán kính quanh cơ sở | Khách cũ (danh sách), người nhắn tin | Từ khách cũ | Thêm trả lời tức thì trong giờ làm việc |
| Bán hàng online | Rộng + A+ audience | Người xem sản phẩm, thêm giỏ (cần Pixel) | Từ người mua | Tách "khách mới" và "khách cũ" bằng loại trừ tệp |
| Tương tác/uy tín | Rộng | Người tương tác trang/Instagram | Không cần | Chỉ để tạo tệp B |

### Các loại đối tượng và cách tạo (qua tool `ads_create_custom_audience` [CT])
- **Website (WEBSITE):** cần `pixel`; mẫu `ALL_VISITORS` (lọc `url` `i_contains` giá trị rỗng, không dùng PageView), `VISITORS_BY_URL`, `TOP_TIME_SPENDERS`. Điền tự động từ sự kiện Pixel.
- **Tương tác (ENGAGEMENT):** nguồn `page`, `ig_business`, `lead` (biểu mẫu tức thì), `ig_lead_generation`, `canvas`... Mặc định lấy cả `lead` và `ig_lead_generation` cho biểu mẫu. Người theo dõi hiện tại dùng `retention_seconds=0`. "Người đã nhắn tin cho Page" là một sự kiện tương tác Page: tên sự kiện chính xác [XM], không tự đặt.
- **Danh sách khách (CUSTOM):** tạo được tệp rỗng (`customer_file_source`, `retention_days` 1 đến 180); **việc tải email/SĐT lên phải làm trong Ads Manager > Đối tượng > Thêm khách hàng** (tool không nạp được thành viên). Chuẩn hóa định dạng SĐT/email trước khi tải. Cập nhật có thể mất vài giờ.
- **Tương tự (LOOKALIKE):** cần `origin_audience_id` (nguồn là CUSTOM/WEBSITE/ENGAGEMENT, không phải tệp tương tự), `lookalike_ratio` 0,01 đến 0,20; không hỏi quốc gia. Mặc định 1%. Tạo bất đồng bộ, đợi vài phút đến vài giờ.

### Quy tắc tệp tùy chỉnh
- Nguồn tệp tương tự nên là **khách đã chốt**, không phải mọi người tương tác (khuyến nghị theo giá trị trọn đời, Corey Haines [TC]). Cần số lượng đủ lớn: thông lệ ≥ 100 người cùng quốc gia, tốt từ 500 đến 1.000 [TC, XM: giới hạn tối thiểu thực tế do Meta quy định].
- **Cửa sổ remarketing** [TC, Corey Haines]: nóng 1 đến 7 ngày; ấm 7 đến 30 ngày, tần suất 3 đến 5 lần/tuần; lạnh 30 đến 90 ngày, 1 đến 2 lần/tuần. Dùng **nội dung khác** với khách mới, không lặp lại cùng lời mời.
- **Loại trừ nên có:** khách đã chốt gần đây (7 đến 14 ngày), người đã điền biểu mẫu/nhắn tin trong 7 ngày cho chiến dịch khách mới, nhân viên/đối tác (qua danh sách). Loại trừ tệp là kiểm soát cứng.
- Với ngân sách dưới 500k/ngày, tệp remarketing thường rất nhỏ: gộp tất cả nguồn (nhắn tin, xem video, tương tác trang, biểu mẫu) vào 1 nhóm, đừng chia nhỏ.

---

## 4. Danh mục đặc biệt và hệ quả với target

Theo tài liệu Meta [CT, developers.facebook.com special-ad-category]: bắt buộc khai báo danh mục đặc biệt (Nhà ở `HOUSING`, Việc làm, Sản phẩm/dịch vụ tài chính, Chính trị) với doanh nghiệp **đặt tại Hoa Kỳ hoặc nhắm tới Hoa Kỳ, Canada, châu Âu**; doanh nghiệp khác có thể chọn `NONE` hoặc chủ động chọn danh mục. Tài liệu không nhắc Việt Nam.

Nếu **vẫn chọn** `HOUSING` (kể cả chạy trong nước), các hạn chế sẽ áp dụng cứng [CT]:
- Tuổi 18 đến 65, không chọn giới tính, không tệp tương tự, không loại trừ vị trí, không nhắm hành vi/nhân khẩu, sở thích chỉ từ danh sách cho phép.
- Địa điểm: bán kính tối thiểu 15 dặm/25 km quanh thành phố, địa chỉ, ghim; cấm zips, tiểu khu, khu phố, vùng đô thị nhỏ.
- Mọi quốc gia nhắm tới phải có trong `special_ad_category_country`.

Hệ quả cho nhà phố theo quận: nếu chọn Nhà ở, **không thể** khoanh ghim nhỏ 2 đến 5 km. Với quảng cáo nhà phố chỉ nhắm Việt Nam: mặc định **không khai báo** (mảng rỗng/`NONE`), nhưng ghi chú: nếu Meta yêu cầu hoặc gắn nhãn sau khi duyệt thì **tuân theo ngay** và chuyển sang bán kính ≥ 25 km. Có chính sách nào của Meta bắt chủ BĐS Việt Nam khai báo không: **[XM]**.

Khi chạy sản phẩm/dịch vụ tài chính nhắm Việt Nam (cho vay, bảo hiểm...), xem file 14 (giấy phép, xác minh).

---

## 5. Lỗi hay gặp về target

1. Đặt `age_max` rồi ngạc nhiên vì quảng cáo vẫn tới người ngoài khoảng: nó là gợi ý.
2. Đặt độ tuổi tối thiểu trên 25 mà không tắt A+ audience: không có hiệu lực cứng [CT].
3. Ghim bán kính 1 đến 2 km cho khu dân cư thưa: tệp quá nhỏ, CPM cao, tần suất cao.
4. Tin vào sở thích chi tiết: nhiều nhóm đã bị gỡ hoặc chỉ còn là gợi ý [TC]; không tự bịa ID sở thích, chỉ dùng ID lấy từ công cụ tìm kiếm của Meta (tool MCP cảnh báo rõ).
5. Tệp tương tự dựng từ 30 người nhắn tin chưa chốt.
6. Không loại trừ khách đã nhắn tin khỏi chiến dịch khách mới: trả tiền hai lần cho cùng một người.
7. Chia nhỏ remarketing thành nhiều nhóm với ngân sách vài chục nghìn mỗi nhóm.
8. Chọn Danh mục Nhà ở khi chỉ chạy trong nước rồi mất khả năng khoanh vùng nhỏ.

---

## 6. Nguồn (truy cập 19/11/2026)

- Meta, basic targeting (trường `geo_locations`, `age_min`, `genders`...): https://developers.facebook.com/docs/marketing-api/audiences/reference/basic-targeting/
- Meta, danh mục quảng cáo đặc biệt: https://developers.facebook.com/documentation/ads-commerce/marketing-api/audiences/special-ad-category
- Meta, Advantage+ campaigns (A+ audience, `targeting_automation`): https://developers.facebook.com/documentation/ads-commerce/marketing-api/advantage-campaigns.md
- Mô tả tool `ads_create_ad_set`, `ads_create_custom_audience` của Meta Ads MCP (đọc trực tiếp trong phiên).
- Linear Design, Advantage+ audience: https://lineardesign.com/blog/metas-advantage-audience/
- Corey Haines marketingskills, skill `ads` (mirror): https://skills.sh/coreyhaines31/marketingskills/ads
- adlibrary, gỡ sở thích 01/2026 (tin cậy thấp): https://adlibrary.com/posts/meta-interest-targeting-removed

Xem thêm: 10 (cấu trúc), 12 (thiết lập, JSON `targeting`), 14 (chính sách).
