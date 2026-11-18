# 41. Chiến lược: phễu, chọn nền tảng, ngân sách, thử nghiệm 2 tuần, đọc số, báo cáo

Dùng sau bước phân tích (tệp 40) và brief (tệp 44). Nguồn chính: skill `ads`, `ad-creative`, `ab-testing` và các tệp `meta-decision-system`, `meta-andromeda-playbook`, `audience-targeting`, `google-search-playbook` trong https://github.com/coreyhaines31/marketingskills ; mốc chi phí VND của https://github.com/minhnv0807/ai-business-skills ; quan điểm Andromeda (đa dạng sáng tạo) từ https://www.chatterbuzzmedia.com/blog/meta-andromeda-creative-targeting/ . Ngày: 19/11/2026.

Cảnh báo chung: phần lớn mốc số (tần suất, vòng đời mẫu, ngưỡng thắng) lấy từ thực hành B2B/SaaS Mỹ. Đây là điểm khởi đầu, chưa kiểm cho nhà phố/khóa học Việt Nam; sau 2 tuần phải thay bằng số thật của chủ. Chỗ nào chưa chắc ghi "cần xác minh".

## 1. Phễu TOFU / MOFU / BOFU theo mức nhận thức

| Tầng | Mức nhận thức (tệp 01) | Mục tiêu | Định dạng nên dùng | Nền tảng | Chỉ số chính |
|---|---|---|---|---|---|
| TOFU (lạnh) | 1-2 chưa biết, biết vấn đề | Chặn lướt, làm khách nhận ra nỗi đau, đưa người mới vào | Video 15-45 giây, câu chuyện, mẹo, "câu hỏi khách hay gặp" | TikTok, Facebook/Instagram Reels | Tỉ lệ xem 3 giây, tỉ lệ giữ xem, CPM, tiếp cận |
| MOFU (ấm) | 3-4 biết giải pháp, biết sản phẩm | Giải phản đối, cho thấy bằng chứng | Lời chứng thật, so sánh, quy trình, buổi học thử, tham quan căn nhà | Facebook (nhắm lại người xem video, người tương tác), YouTube | CTR, giá mỗi lượt nhấp, thời gian xem |
| BOFU (nóng) | 5 sẵn sàng mua | Chốt: nhắn tin, đặt lịch, đăng ký | Offer rõ + hạn thật + nút hành động; trả lời tin nhắn nhanh | Google Search (người tự tìm), Facebook nhắm lại, Zalo/inbox | Giá mỗi tin nhắn/lead đủ điều kiện, tỉ lệ chốt |

Nguyên tắc: khách đã nhắn tin hoặc xem 50% video không nên thấy lại quảng cáo mức 1-2; loại họ khỏi nhóm lạnh (marketingskills khuyên loại khách hiện có và người vừa chuyển đổi 7-14 ngày).

Phân bổ ngân sách theo tầng khi mới bắt đầu (gợi ý, không phải nghiên cứu): TOFU 55-65%, MOFU 15-25%, BOFU 15-25%. Ngân sách nhỏ thì bỏ MOFU riêng; đưa quảng cáo bằng chứng vào cùng bộ với quảng cáo hook.

## 2. Chọn nền tảng theo sản phẩm và ngân sách

| Sản phẩm | Ưu tiên 1 | Ưu tiên 2 | Ghi chú |
|---|---|---|---|
| Nhà phố (BĐS) | Facebook: video thật căn nhà, kéo tin nhắn/biểu mẫu | Google Search "nhà phố + khu vực" (khách tự tìm); TikTok để tăng nhận diện bằng video tham quan | Giao dịch ít, giá trị lớn: đo bằng lead đủ điều kiện và lượt xem nhà, không chỉ số tin nhắn. Phải tuân pháp lý nhà đất (tệp 42) |
| Khóa học/đào tạo | Facebook: video + học thử, kéo tin nhắn | TikTok: demo, kết quả học viên (Spark Ads từ video thật); Google/YouTube nếu có người tìm "học ..." | Mức 1-3 là chính; offer học thử là bước vào rẻ nhất |
| Dịch vụ địa phương | Google Search + Maps (nhu cầu gấp, tự tìm) | Facebook nhắm bán kính nhỏ | Nếu lượng tìm kiếm gần 0 thì dồn sang Facebook (google-search-playbook cũng nói vậy) |
| Bán hàng online | TikTok: video demo, Spark Ads, có thể TikTok Shop | Facebook nhắm lại người xem/giỏ hàng; Google Shopping khi có nguồn cấp (cần xác minh tại Việt Nam) | Sản phẩm bốc đồng hợp video bằng chứng/tình huống |

Theo ngân sách (VND mỗi ngày; điểm khởi đầu, cần xác minh). Gợi ý mặc định của lệnh /ts-len-camp-facebook là 200.000 đến 500.000 đồng/ngày:

| Ngân sách/ngày | Cách làm |
|---|---|
| Dưới 150.000 | MỘT kênh. Dịch vụ có người tìm: Google Search (1 chiến dịch). Còn lại: Facebook 1 chiến dịch, 1 nhóm, 3 mẫu |
| 150.000 - 500.000 | Facebook là chính: 1 chiến dịch, 1-2 nhóm, 3-5 mẫu khác ý tưởng. Thêm Google khi có từ khóa rõ |
| 500.000 - 1.500.000 | Facebook (80% chạy/20% thử) + Google Search + nhắm lại |
| Trên 1.500.000 | Thêm TikTok (cần có kho video đủ nhiều) |

Tách chạy/thử (từ meta-decision-system): khi đã có mẫu thắng, đặt hai chiến dịch trùng đối tượng: Chạy (~80%, chỉ mẫu đã thắng) và Thử (~20%, ý tưởng mới). Hai tuần đầu chưa có mẫu thắng thì dồn 100% vào thử.

## 3. Đặt giá mục tiêu trước khi chạy (rất quan trọng)

Mọi quyết định tắt/giữ/tăng đều so với một con số G = giá tối đa chấp nhận được cho một khách đủ điều kiện (hoặc cho một tin nhắn). Cách tính ngược từ lợi nhuận, ví dụ MINH HỌA (thay bằng số thật của chủ):

Nhà phố: lợi nhuận một giao dịch giả định 60 triệu; chủ chấp nhận chi quảng cáo tối đa 15% = 9 triệu cho một giao dịch. Nếu 20 lượt xem nhà mới ra 1 giao dịch (5%) thì mỗi lượt xem nhà tối đa 450.000. Nếu 40% khách đủ điều kiện đi xem thì mỗi khách đủ điều kiện tối đa 180.000. Nếu 30% tin nhắn là khách đủ điều kiện thì mỗi tin nhắn tối đa khoảng 54.000.

Khóa học: học phí giả định 3.000.000; chấp nhận chi tối đa 30% = 900.000 cho một học viên. Nếu 5% tin nhắn thành học viên thì mỗi tin nhắn tối đa 45.000.

Nếu chủ chưa có tỉ lệ thật, dùng giả định rồi ghi `[GIẢ ĐỊNH]` và thay sau 2 tuần. Mốc tham khảo thô (cần xác minh, không phân theo ngành): chi phí mỗi tin nhắn Meta "tốt" 18.000-25.000, TikTok 20.000-28.000, ROAS trung bình 2-4 lần (https://github.com/minhnv0807/ai-business-skills). Nhà phố thường cao hơn nhiều vì tin nhắn kém đủ điều kiện hơn.

## 4. Cấu trúc tài khoản gọn (tránh trộn nhóm)

Facebook (theo Andromeda, ý kiến thực hành, cần xác minh):
- 1 chiến dịch mục tiêu tin nhắn hoặc khách hàng tiềm năng. 1 nhóm quảng cáo đối tượng rộng (tệp 43). 3-5 mẫu quảng cáo KHÁC Ý TƯỞNG (angle, mức nhận thức, định dạng khác nhau), không phải 5 bản chỉ đổi màu.
- Meta có thể gộp các mẫu quá giống nhau (ước chừng trên 60% giống nhau, theo thực hành); các bản sao của mẫu thắng không thêm tiếp cận mới.
- Đặt tên: `[Kênh]_[Mục tiêu]_[Đối tượng]_[Offer]_[Ngày]`, ví dụ `FB_Tin-nhan_Rong-GoVap_XemNha_1124`.
- Mỗi mẫu có một ý tưởng, một angle, một mức nhận thức (ghi vào tên).

Google Search (rút từ google-search-playbook):
- Bắt đầu 1 chiến dịch Search; nhóm theo ý định chung (5-15 từ khóa cùng ý, cùng trang đích); 2-3 quảng cáo thích ứng mỗi nhóm.
- Tắt Search Partners và mạng hiển thị cho chiến dịch mới; định vị "đang ở khu vực" thay cho mặc định.
- Giá thầu: dưới 15 chuyển đổi/tháng dùng CPC thủ công hoặc "tối đa hóa chuyển đổi" không mục tiêu; từ 30 chuyển đổi/30 ngày ổn định mới đặt giá mục tiêu mỗi chuyển đổi.
- Hằng tuần xem báo cáo cụm từ tìm kiếm: loại từ phủ định (3 nhấp không chuyển đổi), thêm cụm hiệu quả thành khớp cụm/chính xác.

TikTok: dùng Spark Ads từ video hữu cơ đã có tương tác (cần xác minh quy trình); đối tượng rộng; sáng tạo quyết định nhiều hơn nhắm đối tượng (tỉ lệ sáng tạo 70/nhắm 30 theo marketingskills, đây là quan điểm).

## 5. Đo lường tối thiểu trước khi bật tiền

1. Mỗi quảng cáo có dấu vết: từ khóa nhắn tin riêng (ví dụ "XEM NHÀ"), UTM, hoặc mã ưu đãi.
2. Cài Pixel/Conversions API (Meta), thẻ TikTok, thẻ chuyển đổi Google nếu có trang web.
3. Một bảng lead (Google Sheet) có cột: ngày, nguồn quảng cáo, mẫu, lead đủ điều kiện (Có/Không/Chưa rõ), đi xem/đăng ký, chốt, doanh thu.
4. Quy ước "đủ điều kiện": ví dụ BĐS = đúng khu vực, ngân sách phù hợp, sẵn sàng xem trong 30 ngày. Khóa học = đúng đối tượng, hỏi lịch/học phí. Ghi trong brief.
5. Cam kết thời gian trả lời tin nhắn (chỉ tiêu đề xuất: trong 15 phút giờ làm việc; cần xác minh). Phản hồi chậm làm CPA thật cao dù quảng cáo tốt.

## 6. Kế hoạch thử nghiệm 2 tuần

| Ngày | Việc | Quyết định cần ra |
|---|---|---|
| T-3 đến T-1 | Phân tích (40), brief (44), đặt G, viết 3-5 mẫu (42), kiểm lỗi, chủ duyệt, cài đo lường | Chủ ký duyệt bản nháp |
| 1 | Tạo chiến dịch ở trạng thái TẠM DỪNG, xem trước, chủ duyệt rồi mới bật | Bật khi chủ duyệt |
| 1-3 | KHÔNG sửa gì (sửa mẫu đang chạy làm hệ thống học lại). Chỉ xem giao hàng | Mẫu nào chi ~0 sau ngày 3: thay hook/hình |
| 4-6 | Đọc theo mẫu: 3 giây xem, giữ xem, CTR, số tin nhắn. Chưa kết luận khi chi nhỏ hơn 3G | Tắt mẫu có chi từ 3G mà 0 tin nhắn |
| 7 | Họp tuần 1: gọi lại ít nhất 10 lead để chấm chất lượng; báo cáo (mục 9) | Giữ/tắt/thay; chọn 1 angle thắng |
| 8-10 | Viết vòng 2: 2-3 biến thể của angle thắng (đổi hook/hình, giữ ý) + 1 angle mới | Chủ duyệt mẫu mới; chạy song song, không sửa mẫu cũ |
| 11-13 | Chạy vòng 2; nếu đã có đủ người xem/nhắn tin, tạo nhóm nhắm lại (BOFU) | Tắt mẫu yếu |
| 14 | Báo cáo tổng 2 tuần; thay mốc mẫu bằng số thật | Quyết định tuần 3-4: tăng 20% mẫu thắng, tiếp tục thử |

Mỗi lần thử chỉ đổi MỘT biến (hook, hình, offer, nút hành động). Mỗi giả thuyết ghi đủ: chỉ số, mẫu đối chứng, hướng kỳ vọng ("hook A có tỉ lệ xem 3 giây cao hơn hook B ít nhất 20%"). Không kết luận theo cảm giác khi mẫu nhỏ; không dừng sớm chỉ vì số đang đẹp (ab-testing).

## 7. Bộ chỉ số theo mục tiêu

| Mục tiêu | Chỉ số chính | Chỉ số phụ để chẩn đoán |
|---|---|---|
| Nhận diện | Tiếp cận, CPM, xem 3 giây, thời gian xem | Tần suất |
| Tin nhắn/lead (nhà phố, khóa học, dịch vụ) | Giá mỗi tin nhắn, giá mỗi lead đủ điều kiện, tỉ lệ đủ điều kiện | CTR, CPC, tỉ lệ phản hồi trong 15 phút, tỉ lệ đi xem/đăng ký |
| Bán hàng online | ROAS, giá mỗi đơn, tỉ lệ chốt | Tỉ lệ thêm giỏ, thời gian trả lời |
| Lưu lượng web/Google | CTR, CPC, tỉ lệ chuyển đổi trang đích, giá mỗi chuyển đổi | Thị phần hiển thị bị mất do ngân sách hay do thứ hạng, từ khóa lãng phí |

Chẩn đoán theo chặng (hook-system):
- Thumbstop thấp: sửa 3 giây đầu (hình hoặc chữ phủ).
- Giữ xem thấp: sửa đoạn giây 3-15 (lời dẫn).
- CTR thấp: lời hứa hoặc offer chưa rõ.
- Nhắn tin/đăng ký thấp dù CTR tốt: trang đích/tin nhắn chào chưa nối tiếp quảng cáo.
- Thumbstop cao nhưng giữ xem và chuyển đổi sụp: hook "câu view", không phải hook thắng.

Thứ tự kiểm tra tuần: chi tiêu -> lưu lượng -> chuyển đổi -> sáng tạo -> trang đích -> theo dõi. Kết luận mỗi vấn đề bằng một nhãn: GIỮ (biến động bình thường/đang học), SỬA (lỗi đã biết, cách sửa đã biết), THỬ (giả thuyết, có chỉ số và điều kiện dừng), ĐIỀU TRA (số liệu không đáng tin, ưu tiên trước mọi nhãn khác).

## 8. Luật tắt / giữ / tăng (rút từ meta-decision-system, hiệu chỉnh cho ngân sách nhỏ)

G là giá mục tiêu mỗi khách đủ điều kiện hoặc mỗi tin nhắn (mục 3). Xét dữ liệu 7-14 ngày gần nhất, dừng ở điều kiện đầu tiên đúng:

1. Chi của mẫu dưới 3G: chờ.
2. Chi từ 3G mà 0 tin nhắn/lead: tắt, bỏ ý tưởng.
3. Có tin nhắn nhưng không có lead đủ điều kiện: đổi angle, giữ định dạng. Số tin nhắn tối thiểu trước khi kết luận là mốc đề xuất 5 tin (cần xác minh).
4. Tỉ lệ đủ điều kiện dưới 40%: thêm câu lọc vào quảng cáo (giá, khu vực, đối tượng). 40-60%: theo dõi thêm 1 tuần. Từ 60%: tốt.
5. Giá mỗi lead đủ điều kiện hơn 1,5G: thay mẫu. Từ G đến 1,5G: theo dõi. Dưới hoặc bằng G: ứng viên thắng.

Chuyển mẫu từ Thử sang Chạy khi đủ: từ 5 lead đủ điều kiện, tỉ lệ đủ điều kiện từ 60%, giá không quá G, chạy từ 14 ngày, có lead trong 7 ngày cuối. Ngân sách nhỏ có thể hạ còn 3 lead nhưng rủi ro nhiễu cao: ghi rõ trong báo cáo.

Tăng ngân sách: mỗi lần +20%, cách nhau ít nhất 5 ngày, không bao giờ +30% trở lên một lần. Điều kiện: giá mỗi lead không quá G hai tuần liên tiếp, tần suất chung dưới 3,0, đã có 3 mẫu thay thế sẵn. Nếu sau khi tăng giá vượt 1,5G: giảm 20-30%, ổn định 2 tuần rồi tăng lại 10%.

Mệt mỏi quảng cáo: nhắm người lạnh tần suất an toàn 1,0-2,5, cảnh báo 2,5-4,0, nguy hiểm trên 4,0; nhắm lại an toàn 2,0-4,0, nguy hiểm trên 6,0 (mốc B2B, cần xác minh). Dấu hiệu khác: CTR giảm từ 20% trong 7 ngày, CPM tăng từ 30% trong 2 tuần. Vòng đời mẫu ước tính: ảnh tĩnh 14-28 ngày, video ngắn 21-35 ngày, video người thật/lời chứng 28-42 ngày (cần xác minh ở Việt Nam).

Quy tắc vận hành:
- Không sửa mẫu đang chạy tốt (làm học lại); tạo bản mới chạy cạnh. Tạm dừng không làm học lại.
- Không tắt mẫu khi chưa có mẫu thay thế; giữ 2-3 bản biến thể chờ sẵn.
- Ưu tiên sửa theo thứ tự: hook, hình, định dạng, thân bài/nút hành động.
- Tỉ lệ thắng thực tế thấp (mẫu mới khoảng 1 trên 10 theo nguồn B2B): lập kế hoạch cho nhiều lần thử, đừng kỳ vọng mẫu đầu thắng.
- Mốc 50 chuyển đổi mỗi tuần để thoát giai đoạn học: ngân sách nhỏ khó đạt; tối ưu theo tin nhắn (sự kiện gần đỉnh phễu hơn) thay vì chốt đơn.
- Google: bấm "AI Max"/khớp rộng chỉ sau khi có từ 30 chuyển đổi/tháng và danh sách từ phủ định chặt.

## 9. Báo cáo hằng tuần (một trang, gửi chủ mỗi tuần)

1. Tóm tắt 3 dòng: tuần này tốt/xấu, vì sao, làm gì tiếp.
2. Bảng số (so với tuần trước): chi tiêu, tiếp cận, tần suất, CTR, CPC, số tin nhắn/lead, lead đủ điều kiện, giá mỗi lead và giá mỗi lead đủ điều kiện (so với G), số đi xem/đăng ký, số chốt, doanh thu nếu có.
3. Top 3 mẫu thắng và lý do (hook, angle, mức nhận thức).
4. Mẫu đã tắt và lý do (theo luật mục 8).
5. Điều học được (khách phản ứng với nỗi đau nào, phản đối mới).
6. Quyết định tuần tới: giữ/tắt/tăng/thử gì, mẫu mới nào cần chủ duyệt.
7. Việc cần chủ: trả lời tin nhắn chậm, bằng chứng còn thiếu, cập nhật giá/lịch.
8. Cảnh báo: chính sách bị từ chối, tần suất cao, số liệu nghi ngờ (nhãn ĐIỀU TRA).
Đối chiếu số trong nền tảng với bảng lead thật của chủ, không chỉ tin báo cáo nền tảng. Một lần mỗi tháng rà lại toàn bộ số thô và gọi lại khách không chuyển đổi để lấy phản đối mới đưa vào quảng cáo.
