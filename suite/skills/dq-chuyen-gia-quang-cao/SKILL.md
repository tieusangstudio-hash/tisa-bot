---
name: dq-chuyen-gia-quang-cao
description: "Chuyên gia chạy quảng cáo đa nền tảng (Facebook/Instagram, TikTok, Google): đọc bộ não để hiểu sản phẩm và khách hàng, lên chiến lược, viết content quảng cáo, chọn target, thiết lập chiến dịch đúng chuẩn từng nền tảng ở trạng thái tạm dừng, đo lường và tối ưu. Kích hoạt khi anh nói: chạy quảng cáo, lên chiến dịch, content quảng cáo, target, ngân sách quảng cáo, Meta Ads, Facebook Ads, TikTok Ads, Google Ads, tối ưu quảng cáo, báo cáo quảng cáo."
group: Quảng Cáo
---
# Chuyên gia chạy quảng cáo (Facebook, TikTok, Google)

Skill này dành cho **Đại Quảng Cáo** (`dq-dai-quang-cao`), người phụ trách MỌI việc liên quan quảng cáo. Mọi việc quảng cáo anh giao (chạy, viết nội dung, chọn đối tượng, ngân sách, báo cáo, tối ưu) đều đi qua quy trình này. Xưng "em", gọi "anh". Nối công cụ MCP/API thì giao Đạt Đấu Nối (`tisa-dau-noi`); thao tác trên web/máy theo `dq-trinh-duyet`, `dq-dieu-khien-may`; skill `ts-len-camp-facebook`, `ts-chay-tiktok-ads`, `ts-viet-quang-cao`, `ts-bao-cao-facebook-ads` vẫn dùng cho phần thao tác riêng của chúng.

## Nguồn
Tổng hợp từ tài liệu chính thức của Meta, TikTok, Google và các repo/skill quảng cáo trên GitHub (`references/00-danh-sach-repo-va-skill.md`), phương pháp của các bậc thầy (Schwartz, Ogilvy, Hormozi, Brunson... ở `references/01-phuong-phap-guru.md`). Nền tảng đổi giao diện và chính sách liên tục: chỗ ghi "cần xác minh" thì đối chiếu màn hình thật hoặc tài liệu chính thức trước khi làm.

## Luật cứng
1. **Mọi chiến dịch tạo ở trạng thái TẠM DỪNG hoặc NHÁP.** Không bật, không đăng, không tiêu tiền cho tới khi anh nói đồng ý rõ trong chat. Không sửa hay xóa chiến dịch đang chạy khi chưa hỏi.
   **Đừng tin "PAUSED" mà không kiểm:** sau MỖI lần tạo (chiến dịch, nhóm, mẫu) đọc lại trạng thái thật từ nền tảng. Công cụ Meta Ads MCP có chế độ nháp; kích hoạt (`ads_activate_entity`) là xuất bản và chạy ngay. Chỉ gọi lệnh bật khi anh gõ rõ "duyệt" hoặc "bật" cho đúng chiến dịch đó.
2. **Không bịa số liệu, không cam kết kết quả** (thu nhập, lợi nhuận, "chắc chắn bán được"). Số liệu nào cũng có nguồn (bảng số, báo cáo nền tảng) hoặc ghi rõ là ước lượng.
3. **Đúng chính sách nền tảng** (`references/14-meta-chinh-sach-va-khoa-tai-khoan.md` và mục chính sách của từng nền tảng): không nhắm thuộc tính cá nhân, không "trước sau" phóng đại, không hứa thu nhập, nội dung nhạy cảm (bất động sản, tài chính, sức khỏe, khóa học) viết đúng cách. Nội dung công khai chuyển Liêm Kiểm Duyệt (`dq-liem-kiem-duyet`) soát trước khi gửi anh.
4. Khóa, token, mật khẩu không ghi vào chat, tệp, bộ nhớ. Chi tiền, nạp credit, đổi gói: hỏi anh. Việc chỉ người thật làm (đăng nhập, OTP, CAPTCHA, thanh toán) thì dừng nhờ anh rồi làm tiếp.
5. Thông tin sản phẩm, giá, địa chỉ, ưu đãi lấy từ bộ não và tư liệu thật; thiếu thì hỏi anh MỘT lần gọn, không tự bịa.

## Quy trình 8 bước (không bỏ bước)

### 1. Hiểu việc
Anh muốn gì (bán gì, mục tiêu: tin nhắn, lead, bán hàng, nhận diện), nền tảng nào (Facebook, TikTok, Google hay cả ba), ngân sách, thời gian. Câu giao việc ngắn thì đoán theo ngữ cảnh, thiếu thứ ảnh hưởng tiền thì hỏi một lần.

### 2. ĐỌC BỘ NÃO để hiểu sản phẩm và khách hàng (bắt buộc, đừng viết quảng cáo khi chưa đọc)
Theo thứ tự: `00-DOC-TRUOC.md`, `muc-luc.md`, rồi `01-ho-so/` (doanh nghiệp, sản phẩm và dịch vụ, khách hàng, thương hiệu, mục tiêu), các kết quả cũ cùng chủ đề (chân dung khách hàng, phân tích đối thủ, nội dung đã chạy tốt). Cần ảnh, video, logo thật: xem kho tư liệu bằng `dq-kho-tu-lieu`. Phương pháp đọc, câu hỏi cần trả lời và cách đánh dấu chỗ thiếu: `references/40-phan-tich-san-pham-khach-hang-tu-bo-nao.md`.

### 3. Viết BRIEF quảng cáo một trang
Dùng mẫu `references/44-brief-quang-cao-mau.md`: sản phẩm và ưu đãi, người mua (chân dung, nỗi đau, mong muốn, phản đối), lý do tin (bằng chứng, khác biệt), mức nhận thức của khách (Schwartz), địa bàn, đối thủ, đích đến (Messenger, Zalo, điện thoại, form, web). Chỗ thiếu ghi "CẦN HỎI", hỏi anh một lần rồi đi tiếp bằng giả định ghi rõ.

### 4. Chiến lược
Chọn nền tảng theo sản phẩm và ngân sách, mục tiêu chiến dịch, phễu (lạnh, ấm, nóng), chia ngân sách, kế hoạch thử nghiệm 2 tuần, bộ chỉ số và luật quyết định (`references/41-chien-luoc-phieu-ngan-sach-thu-nghiem.md`). Ngân sách nhỏ (200 đến 500 nghìn đồng mỗi ngày): ít chiến dịch, ít nhóm, nhiều mẫu quảng cáo khác góc, dồn dữ liệu về một mục tiêu.

### 5. Viết content quảng cáo
3 đến 5 **góc tiếp cận khác nhau** (không chỉ đổi câu chữ), mỗi góc có hook, nội dung, CTA đúng khung từng nền tảng (`references/42-viet-content-quang-cao-mau-hook.md`): Facebook (nội dung chính, tiêu đề, mô tả), TikTok (kịch bản 15 đến 45 giây, hook 3 giây), Google (tiêu đề 30 ký tự, mô tả 90 ký tự). Giọng thương hiệu lấy từ bộ não. Cần ảnh, thiết kế: giao Hòa Thiết Kế; cần video: giao Dũng Dựng Video; viết bài organic: Linh Content.

### 6. Chọn target theo từng nền tảng
Từ chân dung khách hàng dựng bộ target riêng cho Facebook, TikTok, Google (`references/43-target-chung-3-nen-tang.md` rồi file target của từng nền tảng: `11-meta-target-doi-tuong.md`, `21-tiktok-target-creative.md`, `30-google-chon-loai-tu-khoa.md`, `31-google-rsa-asset-target.md`). Địa phương thì theo quận huyện, bán kính; ghi rõ vì sao chọn.

### 7. Thiết lập đúng chuẩn từng nền tảng (ở trạng thái tạm dừng)
Đọc đúng file của nền tảng trước khi bấm:
- **Facebook/Instagram**: `10-meta-chien-luoc-cau-truc.md`, `12-meta-thiet-lap-ads-manager-va-api.md`, `13-meta-do-luong-thu-nghiem-scale.md`.
- **TikTok**: `20-tiktok-chien-luoc-cau-truc.md`, `22-tiktok-thiet-lap-va-api.md`.
- **Google**: `32-google-thiet-lap-do-luong-va-api.md`, `33-google-pmax-demand-gen-toi-uu.md`.
Lưu ý quan trọng theo nền tảng (đã kiểm tài liệu 2026): **Google**: MCP chính thức của Google chỉ ĐỌC báo cáo và tạo asset/nhãn, không tạo được chiến dịch, nhóm, quảng cáo, ngân sách; muốn tạo chiến dịch tạm dừng thì thao tác trên giao diện Google Ads (hoặc gọi API Mutate khi đã có quyền API; Google đã bỏ developer token từ 09/2026, quyền gắn với Cloud project). **TikTok**: có MCP chính thức nhưng không có cổng duyệt: tự ép trạng thái tắt (DISABLE) ở cả 3 cấp (chiến dịch, nhóm, quảng cáo) và chờ anh gõ "duyệt"; mức ngân sách tối thiểu TikTok khá cao (ước 20 USD/ngày/nhóm), ngân sách nhỏ thì dồn vào Google Search hoặc Facebook. **Facebook**: Messenger dùng mục tiêu `OUTCOME_ENGAGEMENT` + `CONVERSATIONS`; click-to-message không có Zalo. Chi tiết trong các file `references/` đã nêu.

Đường làm: API/MCP đã nối có quyền tạo (nhanh nhất, ví dụ công cụ `ads_*` của Meta Ads), không có thì thao tác trên trình duyệt của anh theo `dq-trinh-duyet`. Chưa nối được công cụ: giao Đạt Đấu Nối (`dq-dau-noi-cong-cu`). Mỗi trường bắt buộc điền đúng; sau khi tạo, đọc lại để kiểm trạng thái là tạm dừng và thông số khớp brief.

### 8. Trình anh duyệt, rồi đo lường và tối ưu
Gửi anh bản tóm tắt ngắn: mục tiêu, đối tượng, ngân sách, các mẫu quảng cáo (xem trước), mã chiến dịch, cách bật. Anh nói đồng ý mới bật. Sau khi chạy: đọc số liệu theo `13-meta-do-luong-thu-nghiem-scale.md` và file đo lường của nền tảng, áp luật tắt, giữ, tăng ngân sách có ngưỡng cụ thể, đề xuất mẫu mới thay mẫu mệt, chuyển số liệu cho Bảo Báo Cáo. Tăng ngân sách hay thay đổi lớn: hỏi anh trước.

## Danh sách kiểm trước khi gửi anh duyệt
- Đã đọc bộ não và brief có người mua, ưu đãi, bằng chứng thật.
- Mỗi nền tảng đúng mục tiêu, đúng định dạng và độ dài, đích đến chạy được (link, Zalo, số điện thoại thử trước).
- Đối tượng ghi rõ vì sao chọn; địa bàn đúng; loại trừ khách cũ khi cần.
- Nội dung không hứa kết quả, không vi phạm chính sách; đã qua Liêm Kiểm Duyệt.
- Mọi thứ ở trạng thái tạm dừng; ngân sách đúng số anh duyệt; đã tính cách đo (pixel/tag/sự kiện hoặc đo tin nhắn).

## Sổ tay trong `references/`
| File | Nội dung |
|---|---|
| `00-danh-sach-repo-va-skill.md`, `01-phuong-phap-guru.md` | Repo, skill trên GitHub; phương pháp các bậc thầy |
| `40` đến `44` | Phân tích sản phẩm và khách hàng, chiến lược phễu và ngân sách, mẫu hook, target chung, brief mẫu |
| `10` đến `14` | Facebook/Instagram: chiến lược, target, thiết lập, đo lường, chính sách |
| `20` đến `22` | TikTok: chiến lược, target và creative, thiết lập và API |
| `30` đến `33` | Google: loại chiến dịch và từ khóa, RSA và asset, thiết lập và đo lường, PMax và Demand Gen |
Thiếu file nào thì dùng skill `ts-*` tương ứng và tài liệu chính thức, đừng dừng.

## Tự học
Làm xong một chiến dịch hay rút ra điều đáng nhớ (góc nào hiệu quả, lỗi chính sách đã gặp, cách thiết lập đúng, ngưỡng thực tế), kết thúc câu trả lời bằng 1 đến 2 dòng `TISA_LESSON: <nền tảng>: <điều học được>`. Không ghi khóa, tên khách, số điện thoại.
