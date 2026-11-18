# 20 - TikTok Ads: chiến lược, mục tiêu, cấu trúc, ngân sách, luật tối ưu

Tra cứu ngày 19/11/2026. Dành cho chuyên viên quảng cáo của TISA BOT (chủ doanh nghiệp nhỏ VN: BĐS nhà phố, đào tạo, dịch vụ, bán hàng). Quy ước: **[CH]** = nguồn chính thức của TikTok; **[BL]** = blog/bên thứ ba; **[UL]** = ước lượng/kinh nghiệm thực chiến, không phải ngưỡng bắt buộc. Chỗ nào ghi "cần xác minh trên màn hình thật" thì giao diện/tên gọi có thể đã đổi.

## 1. Nguyên tắc nền (đọc trước khi lên chiến dịch)

- TikTok là nền tảng **tạo nhu cầu** (người ta lướt, không chủ động tìm). Với nhà phố/khóa học giá trị lớn, TikTok thường kéo **lead rẻ nhưng chất lượng dao động**; cần quy trình gọi/nhắn lại nhanh trong vài giờ. [UL]
- Mọi chiến dịch AI dựng đều tạo ở trạng thái **TẠM DỪNG (DISABLE)**, chủ duyệt rồi mới bật. Ghi rõ trong bản duyệt: mục tiêu, ngân sách/ngày, đối tượng, video, link, đích nhận lead, ngày chạy thử.
- Ưu tiên **1 mục tiêu / 1 chiến dịch**, 1 câu hỏi cần kiểm chứng / 1 nhóm quảng cáo (ví dụ: "video có mặt chủ nhà" vs "video quay căn nhà").
- Trước khi chạy: có nơi nhận lead và người trả lời (Zalo OA, số điện thoại, CRM, bảng tính). Không có nơi nhận thì không bật.

## 2. Chọn mục tiêu theo ngữ cảnh người bán VN

| Tình huống | Mục tiêu nên chọn | Tối ưu theo / đích | Ghi chú |
|---|---|---|---|
| BĐS nhà phố, muốn khách để lại SĐT | **Lead Generation** | Instant Form (trong app) hoặc form web/landing | Hợp nhất cho bắt đầu. Form ngắn: tên, SĐT, quận quan tâm, ngân sách |
| BĐS/dịch vụ, khách quen Zalo | **Lead Generation → Instant messaging apps (Zalo)** | Goal "Conversations" (khuyến nghị) hoặc "Clicks" | Cần **Zalo Official Account** liên kết; Clicks dùng Instant Messaging URL, **không có dữ liệu form**, phải theo dõi lead ngay trong Zalo [CH: help "set up lead generation with instant form" + tài liệu messaging, cần xác minh trên màn hình thật] |
| Đào tạo/khóa học, bán trên landing page | **Website conversions** (tên mới có thể là **Sales/Product sales** trong Smart+) | Tối ưu theo sự kiện Lead/Đăng ký/Thanh toán qua Pixel | Cần Pixel + đủ sự kiện; xem mục 5 |
| Chỉ muốn kéo người vào web/landing, chưa có Pixel ổn | **Traffic** | Click / Landing page view | Rẻ nhưng nhiều click rác; chỉ dùng thử creative hoặc khi chưa có Pixel |
| Xây kênh, tăng follow, video organic đã hiệu quả | **Video views / Community interaction (Engagement)** + Spark Ads | Xem 6s / theo dõi | Dùng để mồi uy tín, không dùng đo bán hàng |
| Muốn phủ nhận diện khu vực | **Reach** | Tiếp cận + tần suất | Hiếm cần với ngân sách nhỏ |
| Shop TikTok | **Shop / GMV Max** | Tự động theo Shop | Chỉ khi có TikTok Shop; ngoài phạm vi BĐS/đào tạo |

Ghi chú mục tiêu:
- Các blog 2026 nói Website Conversions đang được gộp vào "Product/Sales" [BL: megadigital.ai, hawky.ai], blog khác vẫn liệt kê riêng; **không xác nhận được trên tài liệu TikTok**. Chuyên viên phải đọc danh sách mục tiêu hiện hữu trên màn hình thật rồi mới gọi API.
- **Smart+** (tự động hóa theo module) hỗ trợ: Traffic, Sales, Lead generation, App [CH: [ads.tiktok.com/business/en/blog/smart-plus-ai-performance-solution](https://ads.tiktok.com/business/en/blog/smart-plus-ai-performance-solution), [help: upgraded Smart+](https://ads.tiktok.com/resources/help/article/how-to-create-a-campaign-in-the-upgraded-smart-experience?lang=en)]. Có thể bật/tắt từng module (đối tượng, ngân sách, vị trí, creative). Giới hạn: tối đa 30 nhóm QC/chiến dịch, 30 nhóm asset/nhóm QC, 50 creative/nhóm asset.

## 3. Cấu trúc chiến dịch

Ba tầng của TikTok: **Campaign** (mục tiêu, có thể giữ ngân sách chung) > **Ad group** (đối tượng, vị trí, ngân sách, lịch, tối ưu, bid) > **Ad** (video, chữ, nút CTA, link, form).

Cấu trúc khởi điểm cho ngân sách nhỏ (khuyến nghị [UL]):

```
Chiến dịch 1 mục tiêu (vd. Lead Generation - Nhà phố Gò Vấp)
 └ Nhóm 1: Rộng (vị trí Gò Vấp+Q12+Tân Bình, 25-55 tuổi, không chọn sở thích) - 1 nhóm chính
    ├ Quảng cáo A: video hook "giá/vị trí"
    ├ Quảng cáo B: video hook "câu chuyện khách"
    └ Quảng cáo C: video Spark (video organic đã tốt)
 └ (Sau 5-7 ngày) Nhóm 2: Sở thích/hành vi hoặc Custom Audience để so sánh
```

- Vì mỗi nhóm cần đủ dữ liệu để thoát giai đoạn học, **ít nhóm hơn là tốt hơn** khi ngân sách nhỏ. Tránh 5 nhóm x 100.000đ/ngày.
- 3-5 creative/nhóm để thử; TikTok chạy theo kết quả, không chia đều.
- **Manual vs Smart+ (automated)**: manual cho phép mỗi nhóm có mục tiêu tối ưu/bid riêng; Smart+ "ngân sách chiến dịch tự động" yêu cầu **mọi nhóm cùng vị trí tối ưu, goal, event, target CPA** [CH: help Smart+]. Chủ mới: dùng manual 1 nhóm hoặc Smart+ lead gen; xem "cần xác minh trên màn hình thật".
- Quảng cáo Smart+ Web hiện không trộn Spark và non-Spark trong cùng chiến dịch [BL: megadigital.ai/en/blog/tiktok-campaign, cần xác minh].

## 4. Ngân sách tối thiểu, giai đoạn học, bid

**Ngân sách tối thiểu [CH: [help: budget](https://ads.tiktok.com/help/article/budget?lang=en), trang ghi đơn vị "$", không nêu VND; cần xác minh với tài khoản VND]:**
- Ngân sách ngày cấp **chiến dịch**: phải vượt **50 USD**; cấp **nhóm quảng cáo**: phải vượt **20 USD/ngày**. Lifetime cấp nhóm = số ngày x mức tối thiểu/ngày (31 ngày => 620 USD).
- Quy đổi tạm (tỷ giá ~25.000-26.000đ/USD, [UL]): nhóm QC >= ~500.000-520.000đ/ngày; chiến dịch có ngân sách chung >= ~1,25 triệu đ/ngày. Nghĩa là **TikTok không hợp với ngân sách 100-200k/ngày**; nếu chủ chỉ có 200k/ngày thì ưu tiên Google Search/Meta hoặc chỉ đẩy Spark/Promote vài ngày. Phải **hiển thị cho chủ** giới hạn này trước khi lên chiến dịch.
- Không đổi giữa daily và lifetime sau khi đã chạy. Ngân sách chiến dịch không nên nhỏ hơn ngân sách nhóm.
- Hướng dẫn ngân sách conversions web: APAC khuyến nghị nhóm QC tối thiểu 20 USD/ngày [CH: [trang lập ngân sách](https://ads.tiktok.com/business/vi/how-it-works/budgeting)].

**Giai đoạn học (learning phase):**
- TikTok: biến động giảm sau khoảng **25 kết quả hoặc 7 ngày**; không tạm dừng khi đang học; tránh sửa làm học lại [CH: [help: learning-phase](https://ads.tiktok.com/help/article/learning-phase?lang=en)]. Hướng dẫn bid/budget gợi ý ~**50 chuyển đổi** là chỉ báo thoát học rõ nhất với oCPM; ngân sách nhóm ~ **CPA mục tiêu x 10** để đủ 50 chuyển đổi (cần xác minh nguyên văn) [CH: [bidding-budget-solutions](https://ads.tiktok.com/help/article/bidding-budget-solutions-drive-tiktok-auction-ad-performance)]. Bài blog thường nói 50 chuyển đổi/7 ngày [BL].
- Đổi ngân sách: tăng tối đa **40%/lần khi đang học, 30%/lần sau khi thoát**, không đổi thường xuyên hơn **mỗi 2 ngày** [CH: help budget].
- Với lead BĐS, CPL có thể cao nên khó đủ 50 lead/tuần: chấp nhận "học chậm", tối ưu theo sự kiện **gần phễu hơn** (ví dụ gửi form) thay vì sự kiện hiếm.

**Bid** (tên có thể khác trên màn hình thật): **Maximum Delivery** (tiêu hết ngân sách, CPA dao động; hợp khi mới) và **Cost Cap** (giữ CPA trung bình <= mức đặt; chỉ khả dụng với một số goal) [CH: [bidding-strategies](https://ads.tiktok.com/help/article/bidding-strategies)]. Tên cũ "Lowest Cost/Bid Cap" còn gặp trong blog [BL]. Khởi điểm: Maximum Delivery hoặc Lowest Cost; sau khi có ~20+ lead, thử Cost Cap bằng ~CPA thực tế +10-20% [UL].

## 5. Chỉ số cần theo dõi (và cách đọc)

| Chỉ số | Ý nghĩa | Tham chiếu |
|---|---|---|
| CPM | Giá 1.000 lần hiển thị | Trung vị toàn cầu ~**4,08 USD** (Triple Whale, 5.900 thương hiệu, 8/2025-7/2026) [BL: [triplewhale.com/blog/tiktok-benchmarks](https://www.triplewhale.com/blog/tiktok-benchmarks)]; Q4 đắt hơn 22-30%. Đây là **benchmark Mỹ/toàn cầu, không phải VN** |
| CTR (đích) | Nhấp/hiển thị | Trung vị ~**0,61%**; dịch vụ/lead ~0,7% (cùng nguồn) |
| CPC | Giá mỗi click | Phổ biến 0,10-1,00 USD [BL] |
| Thumb-stop / hook rate | % xem >= 2-3s trên lượt hiển thị | **Không có nguồn chính thức**; thực chiến: >25-30% là ổn [UL] |
| 6s view rate / completion | Giữ chân | TikTok nhấn mạnh 6 giây đầu quyết định nhớ quảng cáo [CH: [creative best practices](https://ads.tiktok.com/business/en/blog/creative-best-practices-top-performing-ads)] |
| CVR (form/landing) | Khách làm gì sau click | Instant form thường cao hơn web; theo dõi riêng theo đích [UL] |
| CPL / CPA | Giá mỗi lead/chuyển đổi | Lấy **chi phí chấp nhận được** từ chủ (giá trị khách), không dùng benchmark |
| Chất lượng lead | % nghe máy, % hẹn xem nhà | Chỉ số quyết định thực sự với BĐS/đào tạo |

## 6. Luật tắt / giữ / scale (khởi điểm [UL], chủ điều chỉnh theo CPL chấp nhận được = X)

1. **Ngày 1-3:** không sửa gì (trừ sai link/duyệt). Không tạm dừng nhóm đang học.
2. **Sau ~3 ngày hoặc ~1.000-2.000 lượt hiển thị/creative:** tắt creative có CTR < ~0,3% và hook rate thấp nhất; giữ 1-2 creative tốt nhất.
3. **Sau 7 ngày:** nếu chi >= 2-3 x X mà **0 lead** => dừng nhóm/creative, đổi hook hoặc đích, không tăng ngân sách.
4. CPL <= X và ổn >= 3 ngày: **tăng 20-30% ngân sách** mỗi 2-3 ngày (<= giới hạn TikTok). Hoặc nhân bản nhóm thắng với đối tượng mới thay vì đập ngân sách.
5. CPL > 1,5 x X nhưng CTR tốt: lỗi nằm ở đích (form dài, landing chậm, không trả lời). Sửa đích trước, không đổi video.
6. Mệt mỏi creative: tần suất tăng, CTR giảm >30% trong 3-5 ngày => làm hook mới (cùng nội dung, mở đầu khác).
7. Mỗi tuần: ghi lại lead thật (đã gọi, đã hẹn) để so với số lead trong Ads Manager; **CRM thắng số của nền tảng**.

## 7. Lỗi hay gặp

- Chạy Traffic rồi trách "không có đơn": Traffic tối ưu click, không tối ưu người mua.
- Ngân sách chia nhỏ nhiều nhóm, không nhóm nào thoát học.
- Sửa mục tiêu/đối tượng/creative liên tục (reset học).
- Tắt quảng cáo sau 1 ngày vì CPL cao trong lúc đang học.
- Dùng video ngang, nhiều chữ, mở đầu bằng logo (xem file 21).
- Không có người trả lời lead trong 1 giờ.
- Bật Spark mà không kiểm tra mã/cho phép hết hạn (ads ngưng khi mã hết hạn).

## Nguồn chính

- Ngân sách: https://ads.tiktok.com/help/article/budget?lang=en (tra 19/11/2026)
- Learning phase: https://ads.tiktok.com/help/article/learning-phase?lang=en
- Bid: https://ads.tiktok.com/help/article/bidding-strategies
- Smart+: https://ads.tiktok.com/business/en/blog/smart-plus-ai-performance-solution
- Hướng dẫn BĐS lead gen: https://ads.tiktok.com/business/vi/guides/real-estate-lead-generation
- Benchmark: https://www.triplewhale.com/blog/tiktok-benchmarks ; https://lebesgue.io/tiktok-ads/tiktok-ads-benchmarks
- Skill tham khảo GitHub: https://github.com/AgriciDaniel/claude-ads (skills/ads-tiktok), https://github.com/coreyhaines31/marketingskills (skills/ads)
