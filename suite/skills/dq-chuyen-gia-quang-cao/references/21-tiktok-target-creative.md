# 21 - TikTok Ads: đối tượng, Spark Ads, creative, lead form

Tra cứu ngày 19/11/2026. Nhãn nguồn: **[CH]** chính thức TikTok; **[BL]** blog/bên thứ ba; **[UL]** ước lượng thực chiến.

## 1. Target (đối tượng)

Các lớp có trên Ads Manager (nhóm quảng cáo, thiết lập thủ công):
- **Nhân khẩu:** vị trí, giới tính, độ tuổi, ngôn ngữ, sức chi tiêu, thu nhập hộ (các lựa chọn có thể khác theo nước) [CH: [list of ad group settings](https://ads.tiktok.com/help/article/list-of-ad-group-settings?lang=en), mới phần website conversions].
- **Sở thích và hành vi, thiết bị** (Android/iOS), **Custom audience** (danh sách SĐT/email, người xem video, người tương tác, khách web qua Pixel), **Lookalike**, **Mở rộng đối tượng (targeting expansion)**.
- **Automatic targeting** (mặc định của Smart+): chỉ cần vị trí, tuổi, ngôn ngữ, AI tự tìm.

Gợi ý theo ngữ cảnh VN [UL]:

| Ngành | Vị trí | Tuổi | Cách target |
|---|---|---|---|
| BĐS nhà phố (Gò Vấp, Q12, Tân Bình) | Chọn **quận/huyện hoặc thành phố** TP.HCM; không rải cả nước | 28-55 | **Rộng** (không chọn sở thích) trước; để video tự chọn người. Sau đó thêm Custom audience từ người đã nhắn/tương tác |
| Đào tạo (quay dựng, AI marketing) | Toàn quốc hoặc TP lớn | 22-45 | Rộng + thử sở thích "kinh doanh, khởi nghiệp, marketing" ở nhóm thứ 2 |
| Dịch vụ địa phương | Bán kính/quận gần nơi phục vụ | theo tệp khách | Rộng + custom audience khách cũ + lookalike (khi có >= vài trăm dòng) |

- **Giữ rộng với ngân sách nhỏ**: ít ràng buộc giúp thoát học nhanh hơn; ràng buộc bằng **nội dung video** (nói đúng người cần) hơn là bằng thiết lập. [UL, phổ biến trong hướng dẫn Smart+/broad]
- **Lookalike** cần nguồn đủ lớn và sạch (khách thật, không phải tất cả người tương tác). Với danh sách < ~100-200 dòng thì thường không đủ [UL, cần xác minh kích thước tối thiểu trên màn hình thật].
- **Tải danh sách khách:** chủ tải file SĐT/email của chính họ có đồng ý; TikTok băm (hash) khi tải. Bot **không tự tải dữ liệu khách** khi chưa được chủ cho phép.
- Loại trừ: người đã để lại thông tin trong 30-90 ngày (tránh trả tiền hiển thị lại cho lead cũ).
- Giới hạn chính sách: không phân biệt đối xử trong nhà ở/tuyển dụng/tín dụng (chính sách HEC); với BĐS tại VN hãy tránh target hay loại trừ dựa trên đặc điểm nhạy cảm (tôn giáo, giới...) [CH: [HEC policy](https://ads.tiktok.com/help/article/housing-employment-credit-hec-ad-policy), cập nhật 4/2026; cần xác minh áp dụng cho VN].
- **Vị trí hiển thị:** để **tự động** (TikTok, kèm Pangle/Global App Bundle theo vùng). Thủ công chỉ khi cần loại Pangle. Brand-safety/ inventory filter: chọn "tiêu chuẩn" hoặc "mở rộng" (cần xác minh nhãn).
- **Lịch (dayparting)** hầu như không cần với ngân sách nhỏ; cân nhắc khi nhân sự trả lời lead chỉ làm giờ hành chính (lead đêm nguội đi).

## 2. Spark Ads (dùng video organic)

- **Là gì:** quảng bá bài đăng sẵn có (của mình hoặc của người sáng tạo được phép) giữ nguyên lượt tim/bình luận/follow. Hiệu quả vì "nhìn như video tự nhiên".
- **Thiết lập [CH: [spark-ads-creation-guide](https://ads.tiktok.com/resources/help/article/spark-ads-creation-guide)]:**
  1. Trong Ads Manager > Create > chọn mục tiêu > đến phần creative.
  2. **Pull:** chọn bài từ tab "TikTok posts"; thêm bài khác bằng **mã video (video code)**. **Push:** chọn từ thư viện rồi đăng.
  3. Với video của **tài khoản khác**: người tạo bật cho phép quảng cáo (video > ba chấm > Ad settings > Generate) để lấy mã; mỗi mã gắn **một video**, chọn thời hạn (các nguồn nêu 7/30/60/365 ngày [BL]); dán mã ở Tools > Creative assets > Spark Ads posts; duyệt hàng loạt tối đa 20 mã.
- **Quy tắc quan trọng:** không sửa chú thích sau khi đã ủy quyền; video riêng tư sẽ thành công khai khi chạy; mỗi tài khoản tối đa 10.000 Spark; **hết hạn mã hoặc người tạo hủy thì quảng cáo dừng** => đặt nhắc nhở gia hạn.
- **Danh tính (identity):** chọn tài khoản TikTok thật làm danh tính. Tùy chọn **Custom Identity đang bị thu hẹp từ đầu 2026** [BL: insense.pro, cần xác minh]; nên dùng tài khoản TikTok thương hiệu thật.
- **Dùng khi nào:** (a) video organic đã có lượt xem/tương tác tốt, (b) cần bằng chứng xã hội, (c) thử nhanh. Với Smart+ có hướng dẫn Spark riêng, và Smart+ Web có thể không cho trộn Spark/không-Spark [BL, cần xác minh].
- Lỗi hay gặp: dùng video có nhạc không có bản quyền thương mại (xem mục 4), mã hết hạn, video có ảnh/giọng người khác chưa được phép.

## 3. Creative chuẩn TikTok

**Thông số [BL, nhiều nguồn khớp; luôn kiểm tra khi tải lên]:** dọc **9:16, 1080x1920** (tối thiểu thường ghi 540x960); MP4/MOV; thời lượng 5-60 giây (quảng cáo hiệu quả thường **9-15 giây** theo TikTok SMB Creative Playbook [CH: [SMB creative playbook 2025](https://ads.tiktok.com/business/library/TikTok_SMB_Creative_Playbook_2025.pdf)]); dung lượng thường <= 500MB (có nguồn ghi giới hạn khác; cần xác minh trên màn hình thật). Bitrate cao (5-10 Mbps) cho nét [BL]. Giao diện đè chữ ở đáy/bên phải: chừa vùng an toàn, **xem trước trong Ads Manager** thay vì dùng tọa độ cũ.

**Nguyên tắc [CH: [creative best practices](https://ads.tiktok.com/business/en/blog/creative-best-practices-top-performing-ads)]:**
- 3-6 giây đầu quyết định (TikTok nêu ~90% tác động nhớ quảng cáo nằm trong 6 giây đầu). Dùng người thật, chuyển động, âm thanh ngay đầu.
- TikTok là **sound-on**: giọng nói/nhạc có bản quyền thương mại tăng khả năng nhớ. Vẫn thêm **phụ đề** (nhiều người xem tắt tiếng nơi công cộng).
- **Giống nội dung tự nhiên** (quay điện thoại, giọng đời thường) thắng bản quảng cáo bóng bẩy. Gắn 3-5 dấu hiệu thương hiệu (logo nhỏ, tên, giọng, màu).
- Một video = một thông điệp + một CTA.

**Khung kịch bản 15-30s cho BĐS nhà phố [UL]:**
1. 0-3s **Hook**: con số/nghịch lý/câu hỏi ("Nhà phố Gò Vấp 4 tỷ còn hẻm xe hơi, có không?"), có người nói trước camera hoặc cảnh rõ nhất của căn nhà.
2. 3-12s **Bằng chứng**: 3 điểm (giá/diện tích/pháp lý, vị trí, tiện ích) - số thật, có chữ trên màn hình.
3. 12-20s **Xử lý phản đối**: pháp lý/giá/lộ trình xem nhà.
4. 20-25s **CTA rõ**: "Để lại SĐT/nhắn Zalo để nhận bảng giá + hẹn xem nhà".
- Dạng hay thắng với đào tạo: demo trước-sau (trước: video quay xấu, sau: bản dựng bằng điện thoại), "3 lỗi khi quay video bán hàng", cảm nhận học viên thật.
- UGC: dùng người thật và lời kể thật; **không bịa lời chứng thực, ảnh hưởng, số liệu** (vi phạm chính sách và niềm tin).

**Quy trình thử creative:** 3 hook khác nhau trên cùng một nội dung (không phải 3 nội dung khác nhau); mỗi video 1-2 phiên bản âm thanh. Làm mới sau 5-10 ngày hoặc khi tần suất tăng.

## 4. Âm thanh/nhạc

Quảng cáo trả phí chỉ được dùng nhạc trong **Commercial Music Library** hoặc nhạc có giấy phép; bài hot dạng organic thường **không** dùng được cho quảng cáo [CH: [commercial music library](https://ads.tiktok.com/help/article/commercial-music-library), cần xác minh]. Spark dùng nhạc của bài gốc nên kiểm tra trước. Bản dựng riêng (nhạc từ thư viện miễn phí hoặc giọng nói) an toàn hơn.

## 5. Lead gen và Instant Form

- Tạo: Ads Manager > Create > **Lead generation** > ở nhóm QC đặt **Optimization location = Instant Form** > ở quảng cáo, mục **Destination** tạo form mới hoặc gắn form có sẵn [CH: [set up lead generation with instant form](https://ads.tiktok.com/resources/help/article/set-up-lead-generation-with-instant-form)]. Form cũng tạo được trong Tools > Instant Page [CH: [build-instant-form](https://ads.tiktok.com/help/article/build-instant-form)].
- **Câu hỏi:** có mẫu hỏi sẵn/thẻ lọc. **Càng ít trường càng nhiều lead nhưng chất lượng thấp**; BĐS nên có 1-2 câu lọc (ngân sách, khu vực, thời gian mua) sau tên + SĐT [UL].
- Cần **chính sách quyền riêng tư** (link) và **lời cảm ơn/đích sau gửi** (Zalo/link/số điện thoại).
- **Nhận lead:** tải thủ công (có nguồn nói TikTok giữ dữ liệu lead ~**90 ngày** và chỉ admin tải được [BL, cần xác minh]); **tích hợp CRM** (trực tiếp, Zapier/LeadsBridge, API webhook, plugin web) [CH: [about CRM integrations](https://ads.tiktok.com/help/article?aid=10001703)]. Với chủ nhỏ: **đẩy về Google Sheets/Zalo** qua webhook/Zapier hoặc tải mỗi sáng.
- **Tin nhắn Zalo:** Lead generation > Optimization location "Instant messaging apps" > goal **Conversations** (khuyến nghị) hoặc **Clicks**; Conversations cần **bộ sự kiện nhắn tin** đã thiết lập trong Events Manager hoặc qua đối tác [CH: help instant messaging]. Cần xác minh trên màn hình thật xem tài khoản VN có hiện Zalo.
- Gọi trong **5-15 phút** đầu; lead BĐS nguội rất nhanh [UL].

## 6. Lỗi hay gặp về target/creative

- Chọn nhiều tầng sở thích + tuổi hẹp + vị trí nhỏ => đối tượng quá hẹp, không tiêu được ngân sách.
- Video ngang, logo mở đầu, nhiều chữ nhỏ che giao diện.
- Quá tin vào "thumb-stop 40%" của blog; hãy so sánh trong chính tài khoản.
- Không gắn đích lead đúng (Instant Form chưa gắn, link Zalo hỏng).
- Dùng ảnh/video nhà không có chủ quyền (ảnh lấy từ web).
