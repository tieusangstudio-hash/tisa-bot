---
name: "Bóc tách, chưng cất kiến thức"
description: "Bóc tách sâu video, ghi âm, PDF, bài viết để nạp bộ não; chọn mô hình và nỗ lực; ra mục Đã học được gì và Sẽ áp dụng thế nào. Dùng khi nạp kiến thức."
group: Điều hành
---
# Bóc tách, chưng cất kiến thức (bản sâu)

Mục tiêu: biến một nguồn (video, ghi âm, YouTube, PDF, bài viết, văn bản chủ gửi) thành kiến thức **đúng nguồn, mổ xẻ tới tận gốc, dùng được ngay** cho doanh nghiệp, và nói rõ cho chủ hai điều: **đã học được gì** và **sẽ áp dụng thế nào**. Kỹ năng này là bước "Bóc tách" của việc `nap-kien-thuc` và bước "Chưng cất" của việc `chung-cat-dem` (skill `dq-nhan-viec-tu-bang`). Các bước lấy nội dung, ghi Obsidian, ghi TISA BOT, gửi bản bóc tách lên bảng vẫn làm theo skill đó.

## 1. Chọn mô hình và mức nỗ lực (theo chủ chọn)

Sự kiện có `nap_kien_thuc.mo_hinh` (mã mô hình, ví dụ `claude-opus-5-5`) và `nap_kien_thuc.nang_luc` (`low`, `medium`, `high`, `xhigh`). Chủ đã chọn, làm đúng như vậy. Không có thì mặc định `claude-opus-5-5` và `high`. Việc `chung-cat-dem` luôn dùng `opus` và `high`.

- Phần bóc tách và soát lỗi giao cho nhân viên phụ (công cụ Agent / Task) với đúng mô hình chủ chọn: đặt `model` bằng mã mô hình; công cụ không nhận mã đầy đủ thì dùng tên ngắn `haiku`, `sonnet`, `opus`, `fable`. Công cụ có tham số `effort` thì đặt đúng mức chủ chọn.
- Mức nỗ lực quyết định dòng đầu của lời giao việc và số lượt:

| Mức chủ chọn | Dòng đầu lời giao việc | Số lượt | Dùng khi |
|---|---|---|---|
| `low` (Thấp) | (bỏ trống) | 2: chưng cất + áp dụng ngắn, không soát lỗi | gom nhanh nhiều nguồn, nguồn ngắn |
| `medium` (Vừa) | `think` | 4: bản đồ, chưng cất, áp dụng, soát nhanh | nguồn thường, cần nhanh |
| `high` (Cao) | `think hard` | 6 lượt đầy đủ (mục 2) | nguồn có giá trị, mặc định |
| `xhigh` (Rất sâu) | `ultrathink` | 6 lượt + chưng cất độc lập lần hai + soát phản biện | khung lớn, khóa học, quy trình cả hệ thống |

- Lời giao việc cho nhân viên phụ viết bằng **tiếng Anh** (mẫu ở mục 4). Kết quả viết bằng **tiếng Việt có dấu**.
- Chép lời video, ghi âm vẫn dùng `nghe_tep`, `nghe_youtube` (Whisper). Chỉ dùng mô hình mạnh cho phần suy luận.
- Chủ chọn Fable hoặc mức Rất sâu thì tốn lượt hơn nhiều: vẫn làm đúng ý chủ, nhưng nói trong bản tóm tắt gửi lên bảng.
- Ghi vào trang nguồn dòng `mo_hinh: <tên mô hình> (<mức nỗ lực>), <số lượt>, soát lỗi <điểm>` để biết bản nào bóc bằng gì.

## 2. Sáu lượt

| Lượt | Ai làm | Làm gì |
|---|---|---|
| 0. Chuẩn bị | Người chạy việc | Lấy nội dung thật (bản chép lời có mốc giờ, chữ PDF có số trang). Đọc `index.md` và bản đồ chủ đề liên quan trong Obsidian, tìm (`grep -ril`) các trang đã có về chủ đề này. Đọc hồ sơ doanh nghiệp trên bảng (`"{{PY}}" "$B" doi`) và bảng giá, lịch, quy tắc tư vấn hiện hành. Gom thành gói ngữ cảnh. |
| 1. Bản đồ nguồn | Mô hình đã chọn | Mục lục trung thực theo mốc giờ hoặc số trang. Chưa diễn giải. |
| 2. Chưng cất trung thực | Mô hình đã chọn | Bóc theo khung ở mục 3 (phần 3 đến 11). Nguồn dài (trên khoảng 40 phút hoặc 30 trang): chia khúc 15 đến 20 phút (hoặc 10 trang), bóc từng khúc song song rồi gộp, bỏ trùng, giữ mốc giờ. |
| 3. Mổ xẻ | Mô hình đã chọn | Soi nguồn bằng 7 góc ở mục 3A: giả định ngầm, nguyên lý gốc, điều kiện đúng, phản biện, mô hình tư duy, kiểu lỗi, điều không nói. Viết phần **Đã học được gì**. |
| 4. Nối bộ não, thiết kế áp dụng | Mô hình đã chọn | Gắn nhãn mỗi ý: MỚI, CỦNG CỐ `[[trang]]`, MÂU THUẪN `[[trang]]`. Thiết kế phần **Sẽ áp dụng thế nào** (mục 3B), có thử nghiệm nhỏ và cách đo. |
| 5. Soát lỗi | Mô hình đã chọn, phiên mới | Nhân viên phụ khác đóng vai biên tập viên khó tính: đối chiếu từng ý với bản chép lời, bỏ ý chung chung, bỏ điều nguồn không nói, sửa số, kiểm tra từng dòng áp dụng có làm được ngay không. Trả danh sách sửa; người chạy việc sửa xong mới ghi bộ não. |

Mức `xhigh` thêm: lượt 2 làm hai lần độc lập (hai nhân viên phụ không thấy bài nhau), người chạy việc gộp phần giống, tra phần khác nhau với nguồn; lượt 5 soát theo lối phản biện (cố tìm chỗ sai).

## 3. Khung trang nguồn (thứ tự cố định)

Hai mục **Đã học được gì** và **Sẽ áp dụng thế nào** luôn đứng ngay sau Thẻ nguồn, vì bảng giao việc đọc đúng hai mục này để chủ thấy ngay. Tiêu đề phải viết đúng như vậy (`## Đã học được gì`, `## Sẽ áp dụng thế nào`).

0. **Thẻ nguồn**: tên, tác giả hoặc kênh, ngày đăng, loại, độ dài, link hoặc đường dẫn, lượt xem nếu có, mục đích của nguồn (dạy, bán hàng, quảng bá), độ tin cậy và lý do, mô hình bóc tách.
1. **`## Đã học được gì`** (kiến thức tiếp thu, viết cho người không xem nguồn vẫn hiểu):
   - **Luận điểm cốt lõi**: 1 đến 2 câu, nguồn muốn người xem tin hoặc làm điều gì.
   - **5 điều quan trọng nhất học được** (thêm tới 8 nếu nguồn xứng đáng). Mỗi điều gồm: *Điều học được* (một câu khẳng định rõ, không nhãn chủ đề); *Vì sao đúng* (bằng chứng hoặc ví dụ trong nguồn, mốc giờ hoặc số trang); *Khác gì cách đang làm* (MỚI / CỦNG CỐ `[[trang]]` / MÂU THUẪN `[[trang]]`); *Hiểu sâu* (nguyên lý đằng sau, vì sao nó hiệu quả, điều kiện để đúng).
   - **Quy tắc ra quyết định** rút được: dạng "nếu X thì làm Y, trừ khi Z". Tối đa 6 quy tắc.
   - **Khung, công thức, quy trình làm được ngay**: tên khung, các bước theo thứ tự, điều kiện dùng, đầu vào, đầu ra, lỗi hay gặp. Chỉ ghi điều nguồn nói; điều AI tự thêm phải ghi rõ "(AI suy luận)".
   - **Điều chưa chắc hoặc nguồn bán hàng**: chỗ người nói đang quảng bá, số tự kể chưa kiểm chứng.
2. **`## Sẽ áp dụng thế nào`** (một kế hoạch làm được, không phải lời khuyên chung):
   - **Làm ngay trong 24 giờ** (tối đa 3 việc): việc, ai làm, xong khi nào thì coi là đạt.
   - **Bảng áp dụng** (3 đến 8 dòng). Cột: Việc cụ thể; Nhân sự AI làm (Linh content, Thảo tư vấn, Đại quảng cáo, Hiền sản phẩm, Họa thiết kế...); Dùng ở đâu (khóa nào, kênh nào, kịch bản nào, trang nào, bộ não trang nào cập nhật); Làm thế nào (3 đến 5 bước); **Bản mẫu viết sẵn** (một câu hook, một câu tư vấn, một đoạn quy trình, một mẫu tin nhắn); Đo bằng gì và mức thế nào là đạt; Khi nào; Ưu tiên (cao, vừa, thấp); Rủi ro hoặc điều kiện.
   - **Thử nghiệm nhỏ** đề xuất (một thử nghiệm, cách chia nhóm, thời gian, số cần đo) trước khi áp dụng rộng.
   - **Bộ não và kỹ năng sẽ cập nhật**: liệt kê trang wiki, kỹ năng, mẫu tư vấn nào bị đổi và đổi gì.
   - **Cần chủ xác nhận**: điều chạm giá, ưu đãi, cam kết, chi tiền, đăng công khai.
3. **Ý chính chi tiết** (5 đến 12): mỗi ý một câu khẳng định rõ, kèm vì sao quan trọng, bằng chứng, mốc giờ hoặc số trang, nhãn MỚI / CỦNG CỐ / MÂU THUẪN.
4. **Số liệu**: tách ba loại: số đo thật (kèm nguồn, ngày đo), số người nói tự kể chưa kiểm chứng, số ví dụ minh họa. Không biến ví dụ thành số liệu.
5. **Câu đáng giữ**: tối đa 5 câu, mỗi câu dưới 25 chữ, ghi rõ nguyên văn hay viết gọn, kèm mốc giờ. Dùng làm hook, câu chốt.
6. **Ví dụ, tình huống** đáng nhớ trong nguồn.
7. **Điều bất ngờ, ngược số đông**.
8. **Giới hạn**: khi nào không nên áp dụng, nguồn thiếu gì.
9. **Câu hỏi còn mở**.
10. **Nhật ký bóc tách**: mô hình, mức nỗ lực, số lượt, các sửa lúc soát, điểm tự chấm.

### 3A. Bảy góc mổ xẻ (lượt 3)
1. **Giả định ngầm**: nguồn đang coi điều gì là hiển nhiên mà chưa chứng minh?
2. **Nguyên lý gốc**: bỏ lớp kỹ thuật, điều cốt lõi hoạt động theo cơ chế gì (hành vi khách, tâm lý, kinh tế, thuật toán)?
3. **Điều kiện đúng**: đúng với ai, quy mô nào, ngành nào, giai đoạn nào? Với doanh nghiệp này đúng hay không, vì sao?
4. **Phản biện mạnh nhất**: người giỏi phản đối sẽ nói gì? Nguồn trả lời được không?
5. **Mô hình tư duy**: có thể gọi tên thành khung dùng lại (ví dụ phễu, đòn bẩy, chi phí cơ hội)?
6. **Kiểu thất bại**: áp dụng sai thì hỏng ở đâu, dấu hiệu sớm là gì?
7. **Điều nguồn không nói**: câu hỏi hiển nhiên mà nguồn né, dữ liệu còn thiếu.

Trang khái niệm (`wiki/concepts/`): mỗi trang **một ý**, tên trang là chính ý đó, mở đầu 1 đến 2 câu định vị (là gì, từ nguồn nào, dùng khi nào), có `aliases`, có `[[...]]` về trang nguồn và bản đồ chủ đề.

Trang TISA BOT (`wiki/Van-phong-AI/kien-thuc/`): bản ngắn cho đội làm việc và cho bảng giao việc đọc. **Bắt buộc có đủ hai mục `## Đã học được gì` và `## Sẽ áp dụng thế nào`, đứng đầu trang ngay sau Thẻ nguồn**, kèm link trang Obsidian ở cuối.

## 4. Mẫu lời giao việc cho nhân viên phụ (tiếng Anh)

Dòng đầu: theo bảng ở mục 1 (`think`, `think hard`, `ultrathink`, hoặc bỏ trống).

### Lượt 1 đến 4 (giao một lần, hoặc mỗi khúc một lần với nguồn dài)

```
<think | think hard | ultrathink, per the effort level>

You are a senior knowledge distiller and strategy analyst for the owner's business (read the business profile in the brain first). Your reader is the owner, who has NOT watched the source and will decide what to change in the business from your page alone.

INPUTS
- SOURCE (transcript with timestamps, or text with page numbers): <path>
- SOURCE CARD facts already known: <title, author/channel, date, url, length, views>
- OWNER FOCUS (what the owner wants extracted, may be empty): <chu_y>
- BRAIN CONTEXT: existing wiki pages on this topic and their key claims: <list of paths + 1-line summaries>
- BUSINESS CONTEXT: products or courses, channels, customers, team roles, current prices and rules: <short profile>

TASK
Pass 1, MAP: a faithful outline of the source by timestamp or page. No interpretation.
Pass 2, DISTILL (faithful): source card and credibility (is the speaker selling something? measured data or opinion?); core thesis in 1-2 sentences; 5-12 key ideas, each a precise claim with why it matters, the evidence the source gives, timestamp/page; frameworks, formulas and step-by-step processes (name, ordered steps, when to use, inputs, outputs, common mistakes; anything you add is marked "(AI suy luan)"); numbers split into measured data, self-reported claims, illustrative examples (never promote an example to data); up to 5 keeper lines under 25 words each, marked "nguyen van" or "viet gon", with timestamp; memorable cases; surprising or contrarian points; limits.
Pass 3, DISSECT through seven lenses, and write what you find in plain language:
 (1) hidden assumptions; (2) first principles, the mechanism underneath; (3) conditions where it is true (who, what scale, what stage) and whether this business meets them; (4) the strongest counter-argument and whether the source answers it; (5) the reusable mental model, named; (6) failure modes and early warning signs; (7) what the source avoids saying.
 Then write "Da hoc duoc gi": the core thesis, the 5-8 most important things learned (each: the lesson in one clear sentence, why it is true with evidence and timestamp, how it differs from what the business does now, the deeper principle and its conditions), up to 6 decision rules in the form "if X then Y unless Z", and the ready-to-use frameworks.
Pass 4, CONNECT AND DESIGN THE APPLICATION:
 - Tag every key idea MOI (new), CUNG CO [[page]] (reinforces), or MAU THUAN [[page]] (contradicts) against BRAIN CONTEXT. Never silently overwrite an older view.
 - Write "Se ap dung the nao": up to 3 actions to do within 24 hours (each with who does it and what counts as done); an application table of 3-8 rows with columns: concrete action; which AI staff role does it; where it is used (course, channel, script, ad, page, which brain page changes); how, in 3-5 steps; ONE ready-to-use sample written in Vietnamese (a hook, a sales line, a process step or a message template); how to measure and the pass threshold; when; priority (cao/vua/thap); risk or precondition. Then one small experiment (design, split, duration, metric) to run before rolling out wide; the list of brain pages and skills to update and what changes in each; the items that need the owner's confirmation (prices, offers, promises, spending, public posting). Prioritise OWNER FOCUS.
 - Open questions for the owner.

RULES
- Fidelity first: every claim must be traceable to a timestamp or page. If the source does not say it, do not write it, or mark it "(AI suy luan)".
- Specific over generic: delete any sentence that would fit any source ("content is important", "understand your customer"). Keep the speaker's own terms.
- Business rules: never state tuition, discounts, seats left, refund promises; student results always carry "tuy san pham va muc do ap dung". No customer phone numbers, addresses, bank details.
- Output in Vietnamese with full diacritics, Markdown. Use exactly these two level-2 headings right after the source card: "## Đã học được gì" and "## Sẽ áp dụng thế nào". Do not use the em dash character; use a colon or comma instead.
- Test before finishing: could a team member act on this tomorrow without watching the source? If not, make it more concrete.
```

### Lượt 5: soát lỗi (phiên mới, chưa thấy lời giao việc ở trên)

```
<think | think hard | ultrathink, per the effort level>

You are a strict fact-checking editor. Compare the DRAFT against the SOURCE line by line.
SOURCE: <path>   DRAFT: <path>
Return a numbered list of fixes, each with the exact draft text, the problem, and the corrected Vietnamese text:
- claims the source does not support, or wrong timestamps/pages
- numbers that are wrong or mislabelled (example presented as data)
- generic sentences with no actionable content
- important ideas, steps or numbers in the source that the draft missed (include timestamp)
- "Da hoc duoc gi" items that merely repeat a topic label instead of stating a lesson
- "Se ap dung the nao" rows that are vague, break business rules, have no ready-to-use sample, no measure, or cannot be done by the named AI role
- the two required headings missing or in the wrong place
- Vietnamese spelling or diacritics errors, and any em dash characters
End with a score 1-10 for fidelity, specificity, depth of insight and usefulness. If any score is below 8, list what would raise it.
```

Mức `xhigh`: thêm lượt phản biện: "Attack the draft: list the three most likely ways the application plan fails in this business and fix the plan."

## 5. Chốt trước khi ghi bộ não

- Đã sửa hết danh sách soát lỗi; điểm cả bốn mục từ 8 trở lên (nếu chưa, chạy lại lượt 2 đến 4 cho phần yếu).
- Mỗi ý có mốc giờ hoặc số trang; mỗi số có loại (đo thật, tự kể, ví dụ).
- Mục **Đã học được gì** nêu bài học bằng câu khẳng định, không chỉ tên chủ đề. Mục **Sẽ áp dụng thế nào** mỗi dòng có bản mẫu viết sẵn và cách đo.
- Mâu thuẫn với trang cũ: giữ cả hai, ghi mục `## Mâu thuẫn`, thêm vào `wiki/_open-questions.md`.
- Phần tóm tắt gửi lên bảng (`boc-tach --tom-tat`) nêu: nguồn nói gì, đã học được gì, sẽ áp dụng vào đâu, bóc bằng mô hình nào và mức nỗ lực nào.
- Nguồn không đọc được, hoặc chưa đủ (thiếu phụ đề, video chỉ có hình): nói rõ trong trang và trên bảng, không giả là đã nạp đủ.

## 6. Chưng cất đêm (`chung-cat-dem`)

Dùng `opus`, nỗ lực `high` và lượt 5 soát lỗi. Khác ở chỗ nguồn là hội thoại khách, việc và hướng dẫn của chủ trong ngày: chỉ giữ tối đa 10 điều **mới và có ích lâu dài**, mỗi điều có nguồn (cuộc chat, việc, ngày), nhãn MỚI / CỦNG CỐ / MÂU THUẪN, và một dòng "dùng thế nào". Điều chưa được chủ xác nhận thì ghi "chờ chủ xác nhận", không đưa cho bot trả lời khách. Trang TISA BOT vẫn có hai mục `## Đã học được gì` (các điều mới) và `## Sẽ áp dụng thế nào` (mỗi điều dùng ở đâu).
