# 00. Danh sách repo, skill và tài liệu chất lượng nhất cho chuyên viên quảng cáo

Ngày tra cứu: 19/11/2026. Số sao lấy từ trang GitHub khi đọc trực tiếp; nếu chỉ thấy qua trang tổng hợp thì ghi "ước lượng". Số sao đổi từng ngày, chỉ dùng để so độ phổ biến, không phải độ đúng.

Quy tắc dùng: lấy PHƯƠNG PHÁP và KHUNG, viết lại bằng lời của mình cho thị trường Việt Nam. Không cài nguyên skill cộng đồng vào máy học viên khi chưa đọc hết nội dung (skill cũng là chỉ dẫn cho AI, có thể chứa lệnh không mong muốn). Số liệu mẫu trong các repo thường là B2B/SaaS Mỹ: phải hiệu chỉnh lại cho nhà phố, khóa học, dịch vụ địa phương ở Việt Nam.

Thang độ tin cậy: Cao = có cấu trúc rõ, đọc được nội dung gốc, nhiều người dùng; Vừa = ý hay nhưng cần kiểm lại; Thấp = ít người dùng hoặc không đọc được nội dung.

## A. Nhóm nên lấy ý nhiều nhất (đã đọc trực tiếp nội dung)

| # | Nguồn | URL | Sao | Tin cậy | Nên lấy gì |
|---|---|---|---|---|---|
| 1 | coreyhaines31/marketingskills (53 skill, nền là `product-marketing`) | https://github.com/coreyhaines31/marketingskills | 61,2k | Cao | Mọi skill đọc chung một tệp "bối cảnh sản phẩm" trước rồi mới viết: đúng ý tưởng "đọc bộ não trước". Có sẵn `ads`, `ad-creative`, `copywriting`, `customer-research`, `offers`, `ab-testing`, `marketing-psychology` |
| 2 | `ad-creative` + thư mục `references/` (hook-system, awareness-headlines, platform-specs, short-form-video-specs, static-ad-templates) | https://github.com/coreyhaines31/marketingskills/tree/main/skills/ad-creative | (thuộc #1) | Cao | 3-5 angle khác nhau; 13 kiểu hook; hook gồm hình + lời + chữ trên màn hình; bảng giới hạn ký tự; làm bản thấp công trước, chỉ đầu tư quay đẹp khi bản thấp có tín hiệu; không bịa số liệu/lời chứng thực |
| 3 | `ads` + `references/` (meta-decision-system, meta-andromeda-playbook, audience-targeting, google-search-playbook, payback-period) | https://github.com/coreyhaines31/marketingskills/tree/main/skills/ads | (thuộc #1) | Cao | Luật tắt/giữ/tăng theo bội số của giá mục tiêu; tăng ngân sách +20% mỗi 5 ngày; dải tần suất; cấu trúc 2 chiến dịch (80% chạy, 20% thử); Google bắt đầu bằng khớp cụm/chính xác, danh sách từ khóa phủ định |
| 4 | `copywriting` | https://github.com/coreyhaines31/marketingskills/tree/main/skills/copywriting | (thuộc #1) | Cao | "Bài kiểm 3 câu hỏi" cho mỗi dòng (hình dung được, kiểm chứng được, đối thủ không dùng y nguyên được); danh sách "dấu hiệu viết bằng AI" cần tránh; đánh dấu `[NEED: ...]` thay vì bịa |
| 5 | `customer-research` | https://github.com/coreyhaines31/marketingskills/tree/main/skills/customer-research | (thuộc #1) | Cao | 3 chế độ (phân tích tài liệu có sẵn, khai thác lời khách trên mạng, phỏng vấn); 6 trường trích xuất (JTBD, nỗi đau, sự kiện kích hoạt, kết quả mong muốn, từ vựng, phương án thay thế); nhãn tin cậy Cao/Vừa/Thấp; không lập persona khi dưới 5 điểm dữ liệu |
| 6 | `offers`, `ab-testing`, `marketing-psychology` | https://github.com/coreyhaines31/marketingskills/tree/main/skills/offers | (thuộc #1) | Cao | Chấm 4 đòn bẩy của công thức giá trị 1-10, sửa đòn bẩy thấp nhất; 6 thành phần của một offer; chỉ dùng khan hiếm thật; kỷ luật thử nghiệm (không nhìn lén rồi dừng sớm) |
| 7 | realkimbarrett/advertising-skills | https://github.com/realkimbarrett/advertising-skills | 790 | Vừa | Thứ tự chạy: chân dung -> offer -> mức nhận thức -> cơ chế -> nhân bội angle -> sáng tạo -> đường chuyển đổi -> xử lý phản đối -> diệt câu chung chung. Nhóm QA (claim-checker, generic-language-killer). README không mô tả sâu cách làm: chỉ lấy khung thứ tự |
| 8 | minhnv0807/ai-business-skills (bản tiếng Việt, 147 skill, MIT) | https://github.com/minhnv0807/ai-business-skills | 695 | Vừa | Duy nhất có mốc chi phí theo VND 2025-2026 (chi phí mỗi tin nhắn Meta, TikTok, ROAS, tỉ lệ lead->hẹn); có skill ad copy, audience research, ads audit, "two-layer copy". Số mốc không rõ nguồn: cần xác minh trước khi coi là chuẩn |
| 9 | wondelai/skills (65 skill từ sách kinh điển) | https://github.com/wondelai/skills | 2,7k | Vừa | `hundred-million-offers` (Hormozi), `influence-psychology` (Cialdini), `made-to-stick`, `storybrand-messaging`, `one-page-marketing`: khung thuật lại sách, dùng để đối chiếu |
| 10 | Anthropic: knowledge-work-plugins, thư mục `marketing` | https://github.com/anthropics/knowledge-work-plugins/tree/main/marketing | không thấy | Cao (nguồn gốc) | 7 lệnh + 5 skill (campaign-planning, content-creation, brand-voice, competitive-analysis, performance-analytics): khuôn đầu ra cho kế hoạch chiến dịch và báo cáo hiệu quả |

## B. Nhóm tham khảo thêm (đọc trang giới thiệu, chưa đọc từng skill)

| # | Nguồn | URL | Sao | Tin cậy | Nên lấy gì |
|---|---|---|---|---|---|
| 11 | AgriciDaniel/claude-ads | https://github.com/AgriciDaniel/claude-ads | 11,1k | Vừa | Triết lý kiểm tra: mỗi mục ra "đạt / không đạt / chưa biết / không áp dụng", dữ liệu thiếu thì ghi "chưa biết", không đoán. Mặc định chỉ đọc, thay đổi tài khoản chỉ ở dạng bản nháp. Rất hợp nguyên tắc "chủ duyệt" của TISA BOT |
| 12 | alirezarezvani/claude-skills | https://github.com/alirezarezvani/claude-skills | 30,1k | Vừa | Tách `paid-ads` (chiến lược chiến dịch) khỏi `ad-creative` (chỉ viết nội dung): cách chia việc cho chuyên viên |
| 13 | openclaudia/openclaudia-skills | https://github.com/openclaudia/openclaudia-skills | 746 | Vừa | Có `facebook-ads`, `google-ads`, `video-ad-analysis`, `google-ads-report`: tham khảo cấu trúc báo cáo |
| 14 | kostja94/marketing-skills | https://github.com/kostja94/marketing-skills | 1,1k | Vừa | Nhánh `meta-ads` (Pixel, Conversions API, lookalike): checklist thiết lập đo lường |
| 15 | whawkinsiv/claude-code-superpowers (skill `customer-research`, tệp MY-ICP.md) | https://github.com/whawkinsiv/claude-code-superpowers | 264 | Vừa | Ý tưởng lưu chân dung khách vào một tệp để mọi skill sau dùng lại giọng khách. Repo không có skill quảng cáo |
| 16 | guia-matthieu/clawfu-skills (`grand-slam-offers`, MIT) | https://github.com/guia-matthieu/clawfu-skills | ~143 (ước lượng) | Thấp-Vừa | Khung dựng offer theo Hormozi: chồng bonus, bảo đảm, khan hiếm |
| 17 | ericosiu/ai-marketing-skills | https://github.com/ericosiu/ai-marketing-skills | ~1,7k-3k (các trang báo khác nhau) | Thấp-Vừa | Không có skill quảng cáo trả phí; chỉ tham khảo "expert-panel" (nhiều góc nhìn chuyên gia cho một quyết định) |
| 18 | mfwarren/entrepreneur-claude-skills (skill `copywriting`: PAS, AIDA, BAB) | https://skills.cat/skills/mfwarren/entrepreneur-claude-skills/copywriting | không rõ | Thấp-Vừa | Bản gọn các công thức viết quen thuộc cho người mới |
| 19 | adkit/ads-skills (`meta-ads-strategy`, cây quyết định Facebook hay Google khi ngân sách thấp) | https://skillselion.com/skills/adkit/ads-skills/meta-ads-strategy | 17 | Thấp | Chỉ tham khảo cách hỏi "ngân sách thấp thì chọn nền tảng nào" |
| 20 | getagentseal/founder-playbook (`100m-offers`) và các bản `alex-hormozi-pitch` | https://claudeskills.info/skills/getagentseal/founder-playbook/100m-offers/ | không rõ | Thấp | Chỉ đối chiếu; nội dung gốc là sách của tác giả |

## C. Tài liệu chính thức và playbook ngoài GitHub (nên đọc bản gốc trước khi chốt luật)

| Nguồn | URL | Dùng để |
|---|---|---|
| Meta, Tiêu chuẩn quảng cáo: "Đặc điểm cá nhân và hành vi vi phạm quyền riêng tư" (tiếng Việt) | https://transparency.meta.com/vi-vn/policies/ad-standards/objectionable-content/privacy-violations-personal-attributes/ | Quy tắc cấm khẳng định/ám chỉ tuổi, tài chính khó khăn, sức khỏe... của người xem (đã đọc trực tiếp) |
| Meta, Tiêu chuẩn quảng cáo (trang chung) | https://transparency.meta.com/vi-vn/policies/ad-standards/ | Danh mục chính sách; mục "kết quả phi thực tế" (unrealistic outcomes) cần đọc bản gốc: trang tôi thử mở lỗi 404 |
| Google Ads: About responsive search ads | https://support.google.com/google-ads/answer/7684791 | Tối đa 15 tiêu đề, 4 mô tả; tiêu đề phải ghép lẫn vẫn có nghĩa; hạn chế ghim |
| TikTok Business Help: Creative best practices for performance ads | https://ads.tiktok.com/help/article/creative-best-practices | Nêu giá trị trong 3 giây đầu, ưu tiên hook trong 6 giây (qua trang thứ cấp; cần đọc bản tiếng Anh gốc) |
| Meta Andromeda và đa dạng sáng tạo (tổng hợp thực hành) | https://www.chatterbuzzmedia.com/blog/meta-andromeda-creative-targeting/ ; https://pubcast.jonloomer.com/stack-creative-diversity-in-phases/ | Quan điểm: sáng tạo khác nhau về ý tưởng mới là "đòn bẩy nhắm đối tượng". Đây là ý kiến người làm nghề, không phải thử nghiệm đối chứng |
| TripleDart: Meta Ads prompt playbook (12 prompt) | https://www.tripledart.com/ai-ppc/prompt-playbook-meta-ads | Mẫu prompt kiểm thử sáng tạo, nghiên cứu đối tượng, theo dõi hiệu quả |
| Jon Loomer (chuyên gia Meta Ads) | https://www.jonloomer.com/facebook-ad-rules/ | Giải thích luật Meta bằng ngôn ngữ thực hành |

## D. Điều rút ra cho thiết kế chuyên viên Đại Quảng Cáo

1. Luôn có một tệp "bối cảnh sản phẩm" làm đầu vào chung (mẫu: tệp 44). Chưa đủ thì hỏi chủ một lần, không đoán.
2. Chia bước: phân tích -> chiến lược -> ý tưởng/angle -> viết -> kiểm lỗi -> kế hoạch thử -> báo cáo. Mỗi bước có tệp đầu ra riêng.
3. Mỗi dữ kiện trong quảng cáo phải có nguồn (từ bộ não hoặc chủ xác nhận). Thiếu thì ghi `[THIẾU: ...]`, không điền.
4. Mọi thay đổi trên tài khoản quảng cáo ở dạng nháp/tạm dừng, chỉ bật khi chủ duyệt (cùng tinh thần `claude-ads`).
5. Kiểm lỗi (tệp 42) chạy trước khi đưa chủ xem: chính sách Meta/Google/TikTok, pháp lý nhà đất, lời hứa thu nhập.
6. Số mốc (CPM, CTR, chi phí mỗi tin nhắn) chỉ dùng làm điểm khởi đầu; sau 2 tuần chạy phải thay bằng số thật của chủ.

## E. Chỗ chưa chắc (cần xác minh)

- Số sao của #11, #12, #16, #17 lấy từ trang tổng hợp, có thể lệch.
- Mốc chi phí VND của #8 chưa thấy nguồn đo; chỉ dùng làm tham chiếu thô.
- Chưa tìm được repo GitHub nào vừa tiếng Việt vừa chuyên sâu về TikTok Ads/Google Ads cho nhà phố hay khóa học; #8 là gần nhất.
- Chưa đọc được trang chính sách "kết quả phi thực tế" của Meta (lỗi 404); nội dung lời hứa thu nhập lấy từ các bài thứ cấp và phải đối chiếu lại.
