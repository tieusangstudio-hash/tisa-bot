# 30 - Google Ads: chọn loại chiến dịch, nghiên cứu từ khóa, so khớp, từ phủ định

Tra cứu ngày 19/11/2026. Nhãn nguồn: **[CH]** Google chính thức; **[BL]** bài bên thứ ba; **[UL]** ước lượng/kinh nghiệm. Google Ads thay đổi nhanh (AI Max, Smart campaigns, Demand Gen); mọi tên menu ghi "cần xác minh trên màn hình thật".

## 1. Google bắt người đang **tìm kiếm** - khác TikTok

Search chỉ **gom nhu cầu đã có**, không tạo nhu cầu [BL: coreyhaines31/marketingskills `skills/ads/references/google-search-playbook.md`]. Nếu ngách có rất ít lượt tìm tại VN (ví dụ khóa "dựng video bằng điện thoại"), kiểm tra Keyword Planner trước; thiếu cầu thì chuyển ngân sách sang TikTok/YouTube/Demand Gen. BĐS nhà phố theo khu vực (Gò Vấp, Quận 12, Tân Bình) thường có lượt tìm thật => Search hợp.

## 2. Chọn loại chiến dịch theo ngữ cảnh người bán VN

| Loại | Dùng khi | Không dùng khi | Ghi chú 2026 |
|---|---|---|---|
| **Search (có thể bật AI Max)** | Có từ khóa mua/thuê/tìm dịch vụ; muốn lead có ý định cao | Cầu tìm kiếm gần 0 | **Điểm xuất phát cho hầu hết chủ nhỏ.** Chiến dịch cho cả BĐS lẫn dịch vụ địa phương |
| **Performance Max (PMax)** | Đã có chuyển đổi ổn, nhiều creative, muốn phủ Search+YouTube+Maps+Display | Chưa có tracking chuyển đổi tốt, ngân sách rất nhỏ, mới bắt đầu | Hộp đen; xem file 33 |
| **Demand Gen** (thay Discovery + Video action) | Muốn tạo cầu trên YouTube/Shorts/Discover/Gmail bằng video, retarget | Cần lead nóng ngay | **Ngân sách tối thiểu 5 USD/ngày** (hiệu lực 1/4/2026) [CH: [dev blog](https://developers.google.com/ads/blog/posts/2026/02/minimum-budget-requirement-for-demand)]; Video Action Campaign đã nâng cấp thành Demand Gen [CH: [help](https://support.google.com/google-ads/answer/15110871)] |
| **YouTube video (Video)** | Muốn tăng nhận diện, đã có video | Bán trực tiếp | Nhiều mục tiêu video nay đi qua Demand Gen; cần xác minh trên màn hình thật |
| **Display** | Remarketing rẻ | Làm mồi mới | Hạn chế; dễ click rác |
| **Local/Maps** | Có cửa hàng/văn phòng | Chỉ bán online | Chiến dịch "Local" cũ nay thuộc PMax có mục tiêu cửa hàng/địa điểm; Local Services Ads đang chuyển sang PMax (chủ yếu Mỹ) [BL, chưa áp dụng VN; cần xác minh] |
| **Call** | Muốn khách gọi | - | **Quảng cáo chỉ gọi (call-only ads) đã bị gỡ tùy chọn tạo từ 2/2026 và ngừng hiển thị 2/2027**; thay bằng **RSA + call asset** [CH: [help 16619010](https://support.google.com/google-ads/answer/16619010)] |
| **Smart campaign** | - | - | API **ngừng tạo Smart Campaign từ 23/9/2026**; chiến dịch cũ vẫn chạy; chuyển sang PMax [CH: Google Ads API release notes v25.2] |

**Khuyến nghị quy trình cho TISA BOT:** (1) Search theo từ khóa có ý định cao; (2) thêm **remarketing/Demand Gen** sau khi có >= vài trăm lượt truy cập; (3) PMax chỉ khi >= ~30 chuyển đổi/tháng và có tracking sạch [UL từ playbook trên]. Không bao giờ chạy PMax làm chiến dịch đầu tiên.

## 3. Nghiên cứu từ khóa (Keyword Planner + sổ tay)

**Quy trình [UL, theo thực chiến]:**
1. Chủ liệt kê: sản phẩm, khu vực, loại khách, câu khách hay hỏi.
2. **Keyword Planner** (Tools > Planning): "Discover new keywords" > nhập chủ đề + **trang web** > đặt **địa điểm Việt Nam/TP.HCM** (nhắm vị trí chính xác hơn khi xem lượt tìm), **ngôn ngữ Tiếng Việt**, **tiền tệ VND** (nếu có). Xem: lượt tìm hàng tháng, mức cạnh tranh, **giá thầu đề xuất (thấp/cao)**. Không dùng số của Mỹ.
3. Tách theo **mức ý định:**
   - Mua: "mua nhà phố Gò Vấp", "bán nhà phố Gò Vấp 4 tỷ", "nhà phố hẻm xe hơi quận 12".
   - So sánh/tìm hiểu: "giá nhà phố Gò Vấp 2026", "kinh nghiệm mua nhà phố".
   - Thương hiệu: tên công ty/thương hiệu (luôn bật, rẻ).
   - Đào tạo: "khóa học dựng video điện thoại", "học quảng cáo facebook ở đâu tphcm".
4. Nhóm theo **chủ đề**: mỗi nhóm quảng cáo 5-15 từ khóa cùng ý, cùng một lời hứa, cùng một trang đích [BL: coreyhaines31]. Không dùng SKAG.
5. Ưu tiên từ có **địa danh + hành động**; từ khóa 50 lượt/tháng nhưng đúng ý > từ 5.000 lượt lẫn lộn.
6. Mỗi từ khóa gắn nhãn ý định để khỏi tiêu tiền vào "tìm hiểu" khi ngân sách còn nhỏ.

**Lỗi hay gặp:** dùng số liệu giá thầu/lượt tìm nước ngoài; quên loại khách tìm "thuê/cho thuê" khi bạn bán; gom nhiều quận khác nhau vào cùng nhóm (cần trang đích riêng).

## 4. Kiểu so khớp từ khóa năm 2026

- **Exact [từ khóa]:** khớp cùng ý định (biến thể gần). **Phrase "từ khóa":** khớp theo ý nghĩa cụm. **Broad:** khớp rộng theo ý; cần **Smart Bidding theo chuyển đổi**.
- **Ưu tiên khi cùng khớp:** (1) **Exact** đúng y từ khóa tìm kiếm; (2) phrase/broad hoặc search theme PMax giống truy vấn; (3) độ liên quan do AI chọn; (4) Ad Rank phá hòa [CH: [help 13389795](https://support.google.com/google-ads/answer/13389795)].
- **Cài đặt "broad match ở cấp chiến dịch" đang bị chuyển thành AI Max** (tự động từ tháng 9/2026). Khi đó từ khóa broad không còn được coi như exact trong xếp ưu tiên; muốn giữ, thêm **bản exact** của từ khóa đó [CH: help 13389795]. Dynamic Search Ads nâng lên AI Max từ **2/2027** (hoãn từ 9/2026) [CH: blog.google, trích trong claude-ads audit 12/10/2026].
- **AI Max** (lớp tối ưu bật trong chiến dịch Search): gồm Search term matching (mở rộng truy vấn theo broad + trang đích), Text customization (tự viết lại tiêu đề/mô tả), Final URL expansion (đổi trang đích). Có thể tắt từng phần; chiến dịch **bị giới hạn ngân sách thì ít lợi**; với **final URL expansion bật, các asset ghim có thể không dùng**; cần kiểm tra link theo dõi (tracking template) tránh 404 [CH: [help AI Max](https://support.google.com/google-ads/answer/15910187)]. Google nêu +14% chuyển đổi cùng CPA (số của Google, chưa kiểm chứng độc lập) [BL: ppc.land, techwyse].
- **Cách dùng cho chủ nhỏ [UL]:**
  1. Khởi động bằng **Phrase + Exact** theo nhóm chủ đề, giá thầu thủ công hoặc Maximize conversions khi dữ liệu thấp.
  2. Mỗi tuần đọc **báo cáo cụm từ tìm kiếm**: thêm từ thắng thành Exact/Phrase; thêm từ rác thành từ phủ định.
  3. Chỉ bật **Broad/AI Max** khi: >= ~30 chuyển đổi/tháng, Smart Bidding đã chạy, và danh sách từ phủ định chặt [BL: coreyhaines31]. Nếu bật: loại trừ URL không muốn nhận lưu lượng (trang tuyển dụng, blog), loại trừ thương hiệu không liên quan, so sánh với chiến dịch không bật AI Max.

## 5. Từ khóa phủ định

- **Cấp chiến dịch** (hoặc danh sách dùng chung) cho từ rác chung; **cấp nhóm** để điều hướng truy vấn về đúng nhóm.
- Danh sách khởi điểm cho BĐS/đào tạo VN [UL]: *thuê, cho thuê, tuyển dụng, việc làm, lương, miễn phí, free, crack, torrent, pdf, mẫu, tải, youtube (nếu không muốn), đồ chơi, game, mô hình, tranh, ảnh, hình ảnh, wiki, là gì, ý nghĩa, sinh viên, thực tập, quận (khu bạn không bán), tỉnh (tỉnh bạn không phục vụ)*. Với nhà phố: phủ định *chung cư, đất nền, căn hộ, biệt thự* nếu không bán loại đó; với đào tạo: *miễn phí, học bổng, đại học, cao đẳng, thạc sĩ*.
- **Phủ định theo kiểu so khớp:** phủ định broad cần **đủ mọi từ** (mọi thứ tự) trong truy vấn; phủ định phrase chặn theo thứ tự; exact chỉ chặn đúng truy vấn đó. Hầu hết lỗi chặn nhầm/hụt từ đến từ chỗ này [BL: coreyhaines31].
- **Đừng phủ định quá tay**; chỉ chặn cái chắc chắn sai; thêm >= ~8-10 phủ định ngay lúc dựng.
- **Phủ định thương hiệu của bạn** trong chiến dịch non-brand để truy vấn thương hiệu về chiến dịch thương hiệu.
- Quy tắc chi tiêu: từ có >= 3 click, chi tiêu lớn mà không có chuyển đổi và không liên quan => phủ định [UL].

## 6. Cấu trúc tài khoản khởi điểm

```
Chiến dịch 1: Thương hiệu (ngân sách riêng, rất nhỏ)
Chiến dịch 2: Search ý định cao (mua/bán) theo khu vực → nhóm: Gò Vấp / Quận 12 / Tân Bình (mỗi nhóm trang đích riêng)
(Sau 3-4 tuần) Chiến dịch 3: Remarketing / Demand Gen
```
- Ngân sách **riêng từng chiến dịch**; không dùng chung để thương hiệu không "ăn" hết.
- Mặc định cần chỉnh khi dựng Search: **tắt Search Partners và Display Network** cho tới khi có bằng chứng; vị trí chọn **"Presence" (đang ở)**; xem file 31 [BL: coreyhaines31 playbook].
- Gộp chiến dịch nếu không đạt ~15-30 chuyển đổi/tháng: Smart Bidding cần dữ liệu.

## 7. Lỗi hay gặp

- Bật Broad/AI Max khi chưa có chuyển đổi và phủ định => tiền chạy vào truy vấn không liên quan.
- Cùng từ khóa, cùng so khớp ở nhiều nhóm (cạnh tranh nội bộ).
- Để mặc định "Presence or interest" và Search Partners/Display.
- Một nhóm quảng cáo chứa mọi khu vực nhưng chỉ một trang đích chung.
- Không dùng số điện thoại/Zalo thật => không đo được cuộc gọi.

## Nguồn chính

- Match types/ưu tiên: https://support.google.com/google-ads/answer/13389795 (tra 19/11/2026)
- AI Max: https://support.google.com/google-ads/answer/15910187
- Demand Gen budget: https://developers.google.com/ads/blog/posts/2026/02/minimum-budget-requirement-for-demand
- Call ads → call assets: https://support.google.com/google-ads/answer/16619010
- Skill GitHub: https://github.com/coreyhaines31/marketingskills/tree/main/skills/ads ; https://github.com/AgriciDaniel/claude-ads/tree/main/skills/ads-google
- Quy tắc đối chiếu API: https://developers.google.com/google-ads/api/docs/release-notes
