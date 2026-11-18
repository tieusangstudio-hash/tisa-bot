# 40. Quy trình phân tích sản phẩm và khách hàng từ bộ não của chủ

Dành cho chuyên viên quảng cáo (Đại Quảng Cáo). Nguồn ý tưởng: ý "đọc tệp bối cảnh sản phẩm trước khi làm" của marketingskills (https://github.com/coreyhaines31/marketingskills), nhãn tin cậy và 6 trường trích xuất của `customer-research`, khung mức nhận thức của Schwartz (xem tệp 01). Ngày: 19/11/2026.

Nguyên tắc: bộ não là nguồn sự thật. Đọc trước, hỏi sau. Cái gì không có trong bộ não thì không điền, không đoán; ghi rõ là thiếu và hỏi chủ đúng một lần.

## 1. Thứ tự đọc (dừng khi đủ, nhưng không bỏ bước 1-3)

Bộ não của chủ có thể đặt tên khác nhau. Dùng cột "tên thường gặp" để tìm; nếu không thấy tệp, tìm theo nội dung.

| Bước | Đọc gì | Tên thường gặp | Lấy ra gì |
|---|---|---|---|
| 1 | Tệp luật chung | `CLAUDE.md`, `00-DOC-TRUOC.md` | Quy tắc làm việc, giọng chủ, điều cấm, việc cần chủ duyệt |
| 2 | Mục lục | `index.md`, `muc-luc.md`, các "bản đồ" (`wiki/ban-do/`) | Biết trang nào chứa giá, khách, sản phẩm |
| 3 | Giá và lịch hiện hành | `Giá & lịch hiện hành`, bảng giá, lịch khai giảng/lịch xem nhà | Giá, ưu đãi, hạn, số chỗ (nguồn sự thật, ưu tiên bản mới nhất) |
| 4 | Hồ sơ doanh nghiệp | `01-ho-so/doanh-nghiep`, trang "giới thiệu" | Là ai, làm gì, ở đâu, từ khi nào, giấy phép |
| 5 | Sản phẩm/dịch vụ | `01-ho-so/san-pham`, trang từng sản phẩm | Tính năng, kết quả, quy trình, bảo hành, điểm khác biệt |
| 6 | Khách hàng | `01-ho-so/khach-hang`, chân dung khách, sổ tay tư vấn | Ai mua, vì sao, hay hỏi gì, hay chê gì |
| 7 | Thương hiệu và giọng | `01-ho-so/thuong-hieu` | Cách xưng hô, từ nên/không nên dùng, màu, câu cửa miệng |
| 8 | Mục tiêu | `01-ho-so/muc-tieu` | Mục tiêu tháng/quý, ngân sách, chỉ tiêu số khách |
| 9 | Nguồn thô lời khách | `raw/`, `02-kien-thuc/` | Tin nhắn, bình luận, đánh giá, ghi âm tư vấn, câu hỏi thường gặp (voice-of-customer) |
| 10 | Kết quả cũ | `output/`, `04-ket-qua/` | Quảng cáo/bài viết đã làm, cái gì chạy tốt hay không (không lặp angle đã thất bại) |

Ghi lại danh sách các tệp đã đọc ở cuối bản phân tích để chủ kiểm.

## 2. 12 câu hỏi cần trả lời (kèm cách xử lý khi thiếu)

| # | Câu hỏi | Tìm ở | Tiêu chuẩn "đã đủ" | Thiếu thì |
|---|---|---|---|---|
| 1 | Bán cái gì, một câu | Sản phẩm | Nói được trong 15 chữ | Hỏi chủ |
| 2 | Người mua là ai (1-3 nhóm, ưu tiên 1 nhóm) | Khách hàng, sổ tay tư vấn | Có tình huống, độ tuổi tham khảo, vùng, khả năng chi | Đánh dấu "giả thuyết", hỏi chủ |
| 3 | Họ "thuê" sản phẩm để làm việc gì (việc, cảm xúc, hình ảnh) | Khách, lời khách | 3 lớp JTBD | Suy ra từ lời khách, đánh dấu Vừa/Thấp |
| 4 | Nỗi đau (3 nỗi đau lớn nhất, theo lời khách) | `raw/` tin nhắn, bình luận | Có câu trích nguyên văn | Không bịa, hỏi chủ 3 câu khách hay phàn nàn |
| 5 | Mong muốn/kết quả cuối | Khách, sản phẩm | Cụ thể, đo được | Hỏi |
| 6 | Phản đối thường gặp (3-5) | Sổ tay tư vấn, lịch sử chat | Có cách chủ trả lời | Hỏi chủ "khách hay chần chừ vì gì" |
| 7 | Lý do mua và sự kiện kích hoạt | Khách | Có ví dụ thật | Hỏi |
| 8 | Bằng chứng có thật | Hồ sơ, lời chứng, ảnh, số liệu | Số, tên (có phép), thời gian | Ghi `[THIẾU: bằng chứng]`, không viết số |
| 9 | Ưu thế khác biệt (đối thủ không nói y nguyên được) | Sản phẩm, đối thủ | Qua "bài kiểm hoán đổi" (xem dưới) | Gợi ý 2-3 giả thuyết, chủ chọn |
| 10 | Đối thủ và phương án thay thế (kể cả "không làm gì") | Phân tích đối thủ, hồ sơ | Tên 2-3 đối thủ + cách họ nói | Nhờ chủ nêu 2 đối thủ |
| 11 | Giá, ưu đãi, hạn, bảo đảm, cách thanh toán | Giá & lịch hiện hành | Giá hiện hành, ngày bản ghi | Không dùng giá cũ; hỏi chủ xác nhận |
| 12 | Địa bàn, kênh nhận khách, giờ phục vụ | Hồ sơ, mục tiêu | Khu vực, Zalo/số điện thoại/Messenger | Hỏi |

Bài kiểm hoán đổi (từ `copywriting`): đọc một câu lợi thế; nếu đối thủ dán nguyên câu đó vào quảng cáo của họ vẫn đúng ("uy tín, chất lượng, giá tốt") thì chưa phải điểm khác biệt. Điểm khác biệt phải có dữ kiện: khu vực, số lượng, quy trình, thời gian, bảo hành, người thực hiện.

## 3. Cách đánh dấu thông tin

Mỗi dữ kiện trong bản phân tích mang một nhãn:

- `[CÓ: tên-tệp]` đọc thấy trong bộ não, ghi nguồn (ví dụ `[CÓ: Giá & lịch hiện hành, 12/11]`).
- `[SUY RA]` suy từ nhiều dữ kiện, cần chủ xác nhận trước khi đưa vào quảng cáo.
- `[THIẾU: nội dung cần]` không có; không được điền.
- `[CŨ?]` có nhưng ngày xưa; giá, lịch, số chỗ cũ hơn 30 ngày phải hỏi lại.
- Nhãn tin cậy cho nhận định về khách: Cao (3 nguồn độc lập trở lên, khách tự nói), Vừa (2 nguồn hoặc chỉ khi được hỏi), Thấp (1 nguồn).

Nếu hai tệp mâu thuẫn (ví dụ hai mức giá), nêu cả hai kèm ngày, theo bản mới nhất, và hỏi chủ.

## 4. Hỏi chủ đúng một lần

Sau khi đọc, gộp mọi chỗ thiếu thành một tin nhắn duy nhất:

1. Tối đa 7 câu, xếp theo mức ảnh hưởng đến quảng cáo (giá/offer, bằng chứng, nỗi đau, phản đối, đối thủ, giọng, ngân sách).
2. Mỗi câu có lựa chọn gợi ý để chủ trả lời nhanh (đánh số hoặc "A/B/khác").
3. Không hỏi lại điều đã có trong bộ não. Không hỏi quá chung ("kể về doanh nghiệp").
4. Nêu rõ mỗi chỗ thiếu sẽ ảnh hưởng gì nếu bỏ trống ("không có số liệu thì tôi chỉ dùng angle nỗi đau, không dùng angle bằng chứng").
5. Nếu chủ không trả lời, vẫn làm tiếp phần chắc chắn; phần thiếu để `[THIẾU]`.

Mẫu tin nhắn:
```
Mình đã đọc: [danh sách tệp]. Để viết quảng cáo đúng, còn thiếu 5 điều:
1. Giá/ưu đãi đang áp dụng tháng này là gì? (A: đúng như bảng giá ngày [ngày]; B: có thay đổi, anh/chị gửi mình)
2. Có lời chứng/ảnh thật nào dùng được không (có phép khách)?
3. Ba câu khách hay hỏi nhất trước khi mua?
4. Hai đối thủ anh/chị hay bị so sánh?
5. Ngân sách thử 2 tuần và kênh nhận khách (Zalo, Messenger, điện thoại)?
Không trả lời mục nào mình sẽ ghi [THIẾU] và không dùng trong quảng cáo.
```

## 5. Rút chân dung khách từ bộ não (khung 9 ô)

Điền từ dữ kiện thật; dưới 5 điểm dữ liệu cùng một nhóm thì ghi "GIẢ THUYẾT":
1. Tình huống và sự kiện kích hoạt: điều gì khiến họ bắt đầu tìm (hết hợp đồng thuê, có con, đổi việc).
2. Việc cần làm (JTBD): thực tế, cảm xúc, hình ảnh.
3. Nỗi đau, bằng lời khách (trích nguyên văn).
4. Kết quả mong muốn, bằng lời khách.
5. Phản đối và nỗi sợ.
6. Phương án thay thế (đối thủ, tự làm, để đó).
7. Từ vựng của khách (cụm từ lặp lại, nên dùng trong tiêu đề).
8. Họ ở đâu, tìm bằng cách nào (Facebook, TikTok, Google, giới thiệu, nhóm Zalo).
9. Ai cùng quyết định (vợ/chồng, cha mẹ, sếp), người bị thuyết phục sau cùng.

Mức nhận thức mặc định (xem tệp 01) ghi cho từng nhóm: ví dụ "người tìm nhà trên Google: mức 4-5; người lướt TikTok: mức 1-2".

## 6. Câu hỏi riêng theo ngành

**Nhà phố / bất động sản**
- Căn cụ thể hay dòng sản phẩm? Khu vực, giá, diện tích, kết cấu, hướng, hẻm rộng bao nhiêu, pháp lý (sổ hồng riêng, hoàn công), tình trạng, thời hạn nhận nhà.
- Khách là người mua để ở hay đầu tư, vay ngân hàng hay tiền mặt? Quyết định ở nhóm gia đình nào?
- Phản đối hay gặp: pháp lý, ngập, quy hoạch, giá, xa trung tâm, tuổi nhà.
- Cách tạo lead: nhắn xem nhà, để lại số, đặt lịch. Ai trả lời tin nhắn và trong bao lâu (ảnh hưởng chi phí thật mỗi khách).
- Nhớ: không viết cam kết sinh lời/tăng giá, không dùng ảnh không đúng căn đang bán.

**Khóa học / đào tạo**
- Học viên học xong làm được gì cụ thể (sản phẩm đầu ra)? Mất bao lâu? Cần máy móc, thời gian gì?
- Học thử, hoàn phí, lịch khai giảng, số chỗ còn, hình thức (online/offline).
- Phản đối: "không có thời gian", "học rồi không làm được", "giá cao", "học online không hiệu quả".
- Bằng chứng: sản phẩm của học viên (có phép), số học viên, thời gian đào tạo. Không dùng lời hứa thu nhập.

**Dịch vụ địa phương**
- Phạm vi phục vụ (quận/phường), thời gian đến, báo giá trước hay sau, bảo hành bằng văn bản.
- Nỗi đau: thợ hẹn rồi không đến, báo giá tăng sau khi làm, không bảo hành.
- Bằng chứng: ảnh trước/sau thật, số ca, đánh giá Google Maps/Facebook.

**Bán hàng online**
- Giá, phí giao, thời gian giao, đổi trả, kênh chốt (inbox, Zalo, sàn).
- Phản đối: sợ hàng khác ảnh, sợ giao chậm, sợ khó đổi trả.
- Bằng chứng: video đóng gói/khui hộp thật, đánh giá có hình, số đơn.

## 7. Đầu ra của bước phân tích (cho chuyên viên và chủ)

Một bản phân tích tối đa 1 trang, gồm:
1. Tóm tắt sản phẩm 1 câu và offer hiện hành (kèm ngày giá).
2. Nhóm khách ưu tiên (1) và nhóm phụ (1), nhãn tin cậy.
3. Top 3 nỗi đau, top 3 phản đối (trích lời khách).
4. 3 điểm khác biệt đã qua bài kiểm hoán đổi (hoặc "chưa có, đề xuất ...").
5. Danh sách bằng chứng dùng được và bằng chứng còn thiếu.
6. Đối thủ chính và cách họ nói.
7. Mức nhận thức của từng nhóm và nền tảng gợi ý (nối sang tệp 41).
8. Danh sách `[THIẾU]` và tin nhắn hỏi chủ (một lần).
9. Danh sách tệp đã đọc.

Sau đó điền vào brief (tệp 44) rồi chuyển sang chiến lược (41) và nội dung (42).

## 8. Lỗi hay gặp cần tránh

- Lấy giá/lịch cũ vì không đọc tệp giá hiện hành.
- Dựng "chân dung" theo mẫu có sẵn (35 tuổi, thu nhập 30 triệu) khi bộ não không có dữ kiện: hãy ghi giả thuyết.
- Chép khẩu hiệu thương hiệu rồi coi là điểm khác biệt.
- Dùng lời chứng thực không có phép hoặc ảnh không phải của chủ.
- Gộp nhiều nhóm khách vào một quảng cáo ("dành cho mọi người").
- Bịa bằng chứng để brief trông đủ; thiếu thì để `[THIẾU]`.
