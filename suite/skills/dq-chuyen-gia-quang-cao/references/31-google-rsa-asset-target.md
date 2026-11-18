# 31 - Google Ads: quảng cáo RSA, asset (tiện ích), target địa lý/lịch/thiết bị

Tra cứu ngày 19/11/2026. **[CH]** chính thức; **[BL]** bên thứ ba; **[UL]** ước lượng. Giao diện/tên menu: "cần xác minh trên màn hình thật".

## 1. Quảng cáo tìm kiếm thích ứng (RSA)

**Giới hạn [CH: [API asset requirements](https://developers.google.com/google-ads/api/performance-max/asset-requirements) cho PMax; [RSA overview](https://developers.google.com/google-ads/api/docs/responsive-search-ads/overview); [help 7684791](https://support.google.com/google-ads/answer/7684791)]:**
- **Tiêu đề (headline): 3-15**, mỗi cái <= **30 ký tự**. **Mô tả: 2-4**, mỗi cái <= **90 ký tự**. Khi hiển thị: tối đa 3 tiêu đề + 2 mô tả. **Đường dẫn hiển thị `path1`/`path2`** (mỗi đoạn <= 15 ký tự [BL, cần xác minh]).
- Giới hạn 30/90 ký tự do tài liệu PMax xác nhận cho văn bản; với RSA đa số nguồn khớp cùng con số (một số nguồn Google chỉ nêu "15 tiêu đề, 4 mô tả" nên **kiểm tra bằng bộ đếm trước khi tạo**).
- Đếm ký tự dạng chữ Unicode đã chuẩn hóa (NFC); dấu tiếng Việt vẫn tính 1 ký tự nhưng nên kiểm tra thực tế trước khi gửi API.
- **Ghim (pinning):** `HEADLINE_1/2/3`, `DESCRIPTION_1/2` (API `pinned_field`). Ghim giảm số kết hợp, ảnh hưởng ad strength; Google khuyên **không ghim cho hầu hết nhà quảng cáo**, hoặc ghim 2-3 tiêu đề vào mỗi vị trí. Chỉ ghim khi bắt buộc (ví dụ câu miễn trừ pháp lý, tên thương hiệu). Nếu ghim vị trí mà không đủ asset hợp lệ, API báo `NOT_ENOUGH_AVAILABLE_ASSET_LINKS_FOR_VALID_COMBINATION`. Với **AI Max + final URL expansion**, asset ghim có thể bị bỏ qua [CH: help AI Max].
- **Ad strength** (Kém/Trung bình/Tốt/Xuất sắc) **không quyết định việc được phát**; đặt mục tiêu "Tốt" trở lên cho mỗi nhóm, nhưng ưu tiên **thông điệp đúng và đủ biến thể** hơn là chạy theo điểm [CH: help 9921843].

**Chiến lược tiêu đề (đủ 15, không lặp ý) [UL]:**

| Nhóm | Số lượng | Ví dụ (đã đo <= 30 ký tự) |
|---|---|---|
| Từ khóa + địa danh | 3-4 | "Nhà Phố Gò Vấp Giá Tốt" (22), "Nhà Phố Hẻm Xe Hơi Gò Vấp" (25), "Nhà Phố Quận 12, Tân Bình" (25) |
| Lợi ích/bằng chứng | 3-4 | "Pháp Lý Rõ Ràng, Sổ Hồng Riêng" (30)*, "Hỗ Trợ Vay Ngân Hàng" (20)*, "Nhà Phố Gần Chợ, Gần Trường" (27) |
| Giá/ưu đãi | 2 | "Giá Từ [X] Tỷ - Xem Nhà Ngay" (28), "Nhận Bảng Giá Nhà Phố Mới" (25) |
| CTA | 3 | "Xem Nhà Phố Gò Vấp Hôm Nay" (26), "Hẹn Xem Nhà Trong Ngày" (22), "Gọi Ngay Để Xem Nhà" (19) |
| Thương hiệu | 1-2 | "[Tên thương hiệu] - Nhà Phố" (độ dài tùy tên) |

\* chỉ viết nếu **đúng sự thật và có thể chứng minh** (xem chính sách mục 6).

**Mô tả (2-4) mẫu (đã đo <= 90):**
- "Nhà phố Gò Vấp, Quận 12, Tân Bình. Pháp lý rõ ràng, hẻm xe hơi. Hẹn xem nhà ngay." (81)
- "Nhận bảng giá và hình ảnh thật. Tư vấn hỗ trợ vay ngân hàng, thủ tục sang tên." (78)
- "Danh sách nhà phố cập nhật hằng tuần theo ngân sách. Để lại SĐT để được gọi lại." (80)
- "Đội ngũ tư vấn đi xem nhà cùng bạn. Không phí tư vấn. Gọi hoặc nhắn Zalo ngay." (78)

**Quy tắc viết:**
- Mỗi nhóm quảng cáo có **2-3 RSA** khác hướng (giá / pháp lý-vị trí / câu chuyện khách). Mỗi RSA >= 8-10 tiêu đề độc lập (ít nhất 8 tiêu đề và 3 mô tả theo audit skill [BL: claude-ads]).
- **Chèn từ khóa chính trọn vẹn vào ít nhất một tiêu đề** (từ khóa đủ trong một tiêu đề mới được ad strength tính [BL]).
- Không dùng chữ in hoa toàn bộ, nhiều dấu chấm than, ký hiệu lạ; không cam kết lợi nhuận/giá "rẻ nhất"/"số 1" nếu không có bằng chứng (chính sách).
- Gửi **URL cuối (final URL)** đúng trang ứng với khu vực/sản phẩm; có thông điệp khớp tiêu đề (message match) - tăng điểm trải nghiệm trang đích.
- Lỗi hay gặp: tiêu đề giống nhau về ý; không có tiêu đề địa danh; để mọi ký tự gần chạm trần 30 (dễ vượt do dấu/ký tự lạ khi sao chép).

## 2. Asset (tiện ích) - nên gắn ở cấp chiến dịch

| Asset | Mô tả/giới hạn | Dùng thế nào |
|---|---|---|
| **Sitelink** | Tiêu đề <= 25 ký tự, 2 dòng mô tả <= 35 ký tự [BL, cần xác minh]; >= 4 sitelink | "Nhà phố Gò Vấp", "Nhà phố Q12", "Bảng giá", "Liên hệ tư vấn" |
| **Callout** | <= 25 ký tự, >= 4 | "Hỗ trợ vay", "Xem nhà cuối tuần", "Tư vấn miễn phí" |
| **Call** | Số điện thoại VN (+84); có thể đặt **lịch gọi theo giờ làm việc** | Thay quảng cáo chỉ gọi; theo dõi cuộc gọi từ quảng cáo |
| **Lead form** | Biểu mẫu trong Google (tên, SĐT...) | Dùng cho Search/Demand Gen/PMax; cần xác minh trên màn hình thật xem VN có bật; kết nối CRM/webhook tải dữ liệu |
| **Địa điểm (location)** | Liên kết **Google Business Profile** (Maps) | Rất quan trọng với BĐS có văn phòng/sàn |
| **Hình ảnh, logo, tên doanh nghiệp** | Ảnh vuông 1:1, ngang 1.91:1; logo 1:1; tên <= 25 ký tự | Với BĐS: ảnh nhà thật |
| **Giá/Quảng bá/Cấu trúc** | Tùy | Có thể chưa có ở VN: xác minh |
- **Call-only ads** đã bị gỡ => dùng **call asset** + RSA [CH: help 16619010].
- Mọi asset phải tuân thủ chính sách; sửa nội dung = duyệt lại.

## 3. Target địa lý

- **Chọn theo khu vực thật bạn phục vụ**: ví dụ TP.HCM > quận/huyện (Gò Vấp, Quận 12, Tân Bình) hoặc **bán kính** quanh văn phòng/dự án (`ProximityInfo` với `geo_point`, `radius`, `radius_units`).
- **Presence** (người thật sự ở khu vực) thay vì "Presence or interest": đặt `geo_target_type_setting.positive_geo_target_type = PRESENCE` (API) hoặc "Tùy chọn vị trí" trên giao diện. Mặc định "presence or interest" gồm cả người chỉ quan tâm đến khu vực (rác với BĐS) [BL: coreyhaines31].
- Tra mã bằng `GeoTargetConstantService.SuggestGeoTargetConstants` (không đoán mã; Việt Nam là một mã quốc gia cố định nhưng phải tra) [CH: Google Ads API].
- **Loại trừ vị trí** (exclusion): tỉnh/quận bạn không bán. Với BĐS: khách ở nước ngoài thường là người Việt kiều; quyết định theo mục tiêu.
- **Ngôn ngữ:** từ **tháng 9/2026**, `CampaignCriterion.language` **không còn hỗ trợ chỉnh thủ công** cho Search/AI Max/Search của PMax; thay vào đó dùng quảng cáo/từ khóa **bằng tiếng Việt** và vị trí [CH: Google Ads API deprecations, trích trong claude-ads audit; tháng ghi 9/2026, ngày cụ thể cần xác minh].

## 4. Lịch quảng cáo (ad schedule) và thiết bị

- **Lịch:** cho BĐS/dịch vụ phụ thuộc gọi điện: chỉ bật giờ có người nghe/gọi lại (ví dụ 7:30-21:30); khung 22:00-6:00 hạ giá thầu hoặc tắt nếu lead nguội. Thu thập dữ liệu **>= 2 tuần** trước khi cắt giờ [UL]. API: `AdSchedule` criterion (ngày, giờ bắt đầu/kết thúc).
- **Thiết bị:** phần lớn tìm kiếm BĐS ở VN từ **điện thoại**; để mặc định (không cắt), chỉnh **giá thầu thiết bị** sau khi có dữ liệu. Nếu trang đích kém trên điện thoại => sửa trang, đừng chỉ giảm giá thầu.
- **Quảng cáo gọi**: nên bật `call asset` có lịch hiển thị trùng giờ trực.

## 5. Điểm chất lượng (Quality Score)

Điểm 1-10 theo **từ khóa**: CTR dự kiến + mức liên quan quảng cáo + trải nghiệm trang đích. Điểm thấp => trả giá cao hơn cho cùng vị trí. Sửa thành phần yếu trước khi tăng giá thầu: nội dung tiêu đề khớp từ khóa, trang đích **một việc, một CTA, tải nhanh, có bằng chứng ở đầu trang**, thông điệp khớp quảng cáo. Độ dài form là cổng chất lượng: form ngắn = nhiều lead hơn, kém chất lượng hơn [BL: coreyhaines31].

## 6. Chính sách hay gặp (VN)

- Google yêu cầu nhà quảng cáo **hoàn tất chương trình xác minh** (danh tính/doanh nghiệp); nếu quá hạn tài khoản có thể bị tạm dừng [CH: [verification programs](https://support.google.com/adspolicy/topic/9646742?hl=vi)]. Danh tính nhà quảng cáo (tên, quốc gia) có thể hiển thị cho người xem.
- **BĐS không có chương trình xác minh riêng** trong kết quả tìm được (có cho tài chính, y tế, bầu cử) [cần xác minh trên màn hình thật; tra thêm "Real estate" trong Google Ads policy].
- Hay bị từ chối: **tuyên bố sai/không chứng minh được** (giá, pháp lý, lợi nhuận), cụm "cam kết lợi nhuận", "đảm bảo", "số 1", viết hoa lạ, ký hiệu; **trang đích** không khớp/không có thông tin liên hệ; link gãy; chính sách quyền riêng tư thiếu; chuyển hướng lạ. Dùng **chứng nhận pháp lý thật** thay vì khẳng định chung.
- Không dùng thương hiệu hay hình ảnh của dự án khác khi không có quyền.
- Bị từ chối: sửa theo "Lý do" trong tài khoản; không lách bằng tài khoản mới.

## Nguồn

- RSA: https://support.google.com/google-ads/answer/7684791 ; https://support.google.com/google-ads/answer/9921843 ; https://developers.google.com/google-ads/api/docs/responsive-search-ads/overview (tra 19/11/2026)
- Asset/giới hạn: https://developers.google.com/google-ads/api/performance-max/asset-requirements
- Xác minh nhà quảng cáo: https://support.google.com/adspolicy/topic/9646742?hl=vi
- Skill: https://github.com/coreyhaines31/marketingskills/blob/main/skills/ads/references/google-search-playbook.md ; https://github.com/openclaudia/openclaudia-skills (google-ads)
