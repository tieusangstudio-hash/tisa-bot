---
name: "Bóc tách, chưng cất kiến thức"
description: "Quy trình 5 lượt bóc tách và chưng cất kiến thức từ video, ghi âm, YouTube, PDF, bài viết, văn bản để nạp bộ não thứ 2 (Obsidian và TISA BOT). Dùng Claude Opus 5.5, nỗ lực cao (high). Kích hoạt khi: nạp kiến thức, bóc tách, chưng cất, tiêu hoá nguồn, ingest, loai_viec nap-kien-thuc hoặc chung-cat-dem."
group: Điều hành
---
# Bóc tách, chưng cất kiến thức 

Mục tiêu: biến một nguồn (video, ghi âm, YouTube, PDF, bài viết, văn bản chủ gửi) thành kiến thức **đúng nguồn, cụ thể, dùng được ngay** cho công việc của doanh nghiệp. Kỹ năng này là bước "Bóc tách" của việc `nap-kien-thuc` và bước "Chưng cất" của việc `chung-cat-dem` (skill `dq-nhan-viec-tu-bang`). Các bước lấy nội dung, ghi Obsidian, ghi TISA BOT, gửi bản bóc tách lên bảng vẫn làm theo skill đó.

## 1. Chọn mô hình (bắt buộc)

- Phần bóc tách và phần soát lỗi giao cho nhân viên phụ (công cụ Agent / Task) với `model: "opus"` (Claude Opus 5.5) và **nỗ lực cao**: nếu công cụ có tham số `effort` thì đặt `"high"`. **Không dùng `fable`, `mythos`** (chi phí cao, chủ không duyệt). Không dùng `sonnet`, `haiku` cho bóc tách.
- Lời giao việc cho nhân viên phụ viết bằng **tiếng Anh** (mẫu ở mục 4), có dòng `think hard` ở đầu để mô hình suy nghĩ kỹ (mức cao). Kết quả viết bằng **tiếng Việt có dấu**.
- Chép lời video, ghi âm vẫn dùng `nghe_tep`, `nghe_youtube` (Whisper). Chỉ dùng mô hình mạnh cho phần suy luận.
- Ghi vào trang nguồn dòng `mo_hinh: opus-5.5 (high)` để biết bản nào bóc bằng mô hình nào.

## 2. Năm lượt

| Lượt | Ai làm | Làm gì |
|---|---|---|
| 0. Chuẩn bị | Người chạy việc | Lấy nội dung thật (bản chép lời có mốc giờ, chữ PDF có số trang). Đọc `index.md` và bản đồ chủ đề liên quan trong Obsidian, tìm (`grep -ril`) các trang đã có về chủ đề này. Đọc hồ sơ doanh nghiệp trên bảng (`"{{PY}}" "$B" doi`). Gom thành gói ngữ cảnh. |
| 1. Bản đồ nguồn | Opus | Mục lục trung thực theo mốc giờ hoặc số trang. Chưa diễn giải. |
| 2. Chưng cất | Opus | Bóc theo khung ở mục 3. Nguồn dài (trên khoảng 40 phút hoặc 30 trang): chia khúc 15 đến 20 phút (hoặc 10 trang), bóc từng khúc song song rồi gộp, bỏ trùng, giữ mốc giờ. |
| 3. So với bộ não, áp dụng | Opus | Gắn nhãn mỗi ý: MỚI, CỦNG CỐ `[[trang]]`, MÂU THUẪN `[[trang]]`. Viết phần Áp dụng cho doanh nghiệp. |
| 4. Soát lỗi | Opus, phiên mới | Một nhân viên phụ khác đóng vai biên tập viên khó tính: đối chiếu từng ý với bản chép lời, bỏ ý chung chung, bỏ điều nguồn không nói, sửa số, chính tả. Trả danh sách sửa; người chạy việc sửa xong mới ghi bộ não. |

## 3. Khung bóc tách (thứ tự trong trang nguồn)

1. **Thẻ nguồn**: tên, tác giả hoặc kênh, ngày đăng, loại, độ dài, link hoặc đường dẫn, lượt xem nếu có, mục đích của nguồn (dạy, bán hàng, quảng bá), độ tin cậy và lý do.
2. **Luận điểm cốt lõi**: 1 đến 2 câu, nguồn muốn người xem tin hoặc làm điều gì.
3. **Ý chính** (5 đến 12): mỗi ý một câu khẳng định rõ, kèm vì sao quan trọng, bằng chứng hoặc ví dụ trong nguồn, mốc giờ hoặc số trang, nhãn MỚI / CỦNG CỐ / MÂU THUẪN.
4. **Khung, công thức, quy trình làm được ngay**: tên khung, các bước theo thứ tự, điều kiện dùng, đầu vào, đầu ra, lỗi hay gặp. Chỉ ghi điều nguồn nói; điều AI tự thêm phải ghi rõ "(AI suy luận)".
5. **Số liệu**: tách ba loại: số đo thật (kèm nguồn, ngày đo), số người nói tự kể chưa kiểm chứng, số ví dụ minh họa. Không biến ví dụ thành số liệu.
6. **Câu đáng giữ**: tối đa 5 câu, mỗi câu dưới 25 chữ, ghi rõ nguyên văn hay viết gọn, kèm mốc giờ. Dùng làm hook, câu chốt.
7. **Ví dụ, tình huống** đáng nhớ trong nguồn.
8. **Điều bất ngờ, ngược số đông**: chỗ nguồn nói khác thói quen thường gặp.
9. **Giới hạn**: khi nào không nên áp dụng, nguồn thiếu gì, chỗ người nói đang bán hàng.
10. **Áp dụng cho doanh nghiệp** (bảng): việc cụ thể, nhân sự AI làm (ví dụ Linh content, Thảo tư vấn, Đại quảng cáo, Hiền sản phẩm), dùng ở đâu (khóa nào, kênh nào, kịch bản nào), **một bản mẫu viết sẵn** (một câu hook, một câu tư vấn, một bước quy trình), mức ưu tiên.
11. **Câu hỏi còn mở**: điều cần chủ xác nhận hoặc cần kiểm chứng thêm.

Trang khái niệm (`wiki/concepts/`): mỗi trang **một ý**, tên trang là chính ý đó, mở đầu 1 đến 2 câu định vị (là gì, từ nguồn nào, dùng khi nào), có `aliases`, có `[[...]]` về trang nguồn và bản đồ chủ đề.

Trang TISA BOT (`wiki/Van-phong-AI/kien-thuc/`): bản ngắn cho đội làm việc: luận điểm cốt lõi, ý chính, khung làm ngay, bảng áp dụng, link trang Obsidian.

## 4. Mẫu lời giao việc cho nhân viên phụ (tiếng Anh)

### Lượt 1 đến 3 (giao một lần, hoặc mỗi khúc một lần với nguồn dài)

```
think hard

You are a senior knowledge distiller for the owner's business (read the business profile in the brain first).

INPUTS
- SOURCE (transcript with timestamps, or text with page numbers): <path>
- SOURCE CARD facts already known: <title, author/channel, date, url, length, views>
- OWNER FOCUS (what the owner wants extracted, may be empty): <chu_y>
- BRAIN CONTEXT: existing wiki pages on this topic and their key claims: <list of paths + 1-line summaries>
- BUSINESS CONTEXT: Products or courses, channels, customers, team roles: <short profile>

TASK
Pass 1, MAP: build a faithful outline of the source by timestamp or page. No interpretation.
Pass 2, DISTILL, in this order:
 1. Source card + credibility (is the speaker selling something? is this measured data or opinion?).
 2. Core thesis in 1-2 sentences.
 3. 5-12 key ideas. Each: a precise claim (not a topic label), why it matters, the evidence or example the source gives, timestamp/page.
 4. Frameworks, formulas, step-by-step processes: name, ordered steps, when to use, inputs, outputs, common mistakes. Only what the source says; anything you add must be marked "(AI suy luận)".
 5. Numbers, split into: measured data (with source and date), self-reported claims, illustrative examples. Never promote an example to data.
 6. Up to 5 keeper lines, each under 25 words, marked "nguyên văn" or "viết gọn", with timestamp.
 7. Memorable examples or cases.
 8. Surprising or contrarian points.
 9. Limits: when not to apply, what the source leaves out, where the speaker is pitching.
Pass 3, CONNECT AND APPLY:
 - Tag every key idea MOI (new), CUNG CO [[page]] (reinforces), or MAU THUAN [[page]] (contradicts) against BRAIN CONTEXT. Never silently overwrite an older view.
 - "Ap dung cho doanh nghiep": 3-8 concrete actions. Each: what to do, which AI staff role does it, where it is used (course, channel, script, ad), one ready-to-use sample written in Vietnamese (a hook, a sales line, or a process step), priority (cao/vua/thap). Prioritise OWNER FOCUS.
 - Open questions for the owner.

RULES
- Fidelity first: every claim must be traceable to a timestamp or page. If the source does not say it, do not write it.
- Specific over generic: delete any sentence that would fit any source ("content is important", "understand your customer"). Keep the speaker's own terms.
- Business rules: never state tuition, discounts, seats left, refund promises; student results always carry "tuy san pham va muc do ap dung". No customer phone numbers, addresses, bank details.
- Output in Vietnamese with full diacritics, Markdown, using the section order above. Do not use the em dash character; use a colon or comma instead.
- Test before finishing: could a team member act on this tomorrow without watching the source? If not, make it more concrete.
```

### Lượt 4: soát lỗi (phiên mới, chưa thấy lời giao việc ở trên)

```
think hard

You are a strict fact-checking editor. Compare the DRAFT against the SOURCE line by line.
SOURCE: <path>   DRAFT: <path>
Return a numbered list of fixes, each with the exact draft text, the problem, and the corrected Vietnamese text:
- claims the source does not support, or wrong timestamps/pages
- numbers that are wrong or mislabelled (example presented as data)
- generic sentences with no actionable content
- important ideas, steps or numbers in the source that the draft missed (include timestamp)
- "Ap dung cho doanh nghiep" items that are vague, break business rules, or have no ready-to-use sample
- Vietnamese spelling or diacritics errors, and any em dash characters
End with a score 1-10 for fidelity, specificity and usefulness. If any score is below 8, list what would raise it.
```

## 5. Chốt trước khi ghi bộ não

- Đã sửa hết danh sách soát lỗi; điểm cả ba mục từ 8 trở lên (nếu chưa, chạy lại lượt 2 hoặc 3 cho phần yếu).
- Mỗi ý có mốc giờ hoặc số trang; mỗi số có loại (đo thật, tự kể, ví dụ).
- Bảng Áp dụng cho doanh nghiệp có bản mẫu viết sẵn cho từng dòng.
- Mâu thuẫn với trang cũ: giữ cả hai, ghi mục `## Mâu thuẫn`, thêm vào `wiki/_open-questions.md`.
- Phần tóm tắt gửi lên bảng (`boc-tach --tom-tat`) nêu: nguồn nói gì, rút được gì, áp dụng vào đâu, bóc bằng mô hình nào.
- Nguồn không đọc được, hoặc chưa đủ (thiếu phụ đề, video chỉ có hình): nói rõ trong trang và trên bảng, không giả là đã nạp đủ.

## 6. Chưng cất đêm (`chung-cat-dem`)

Dùng cùng mô hình (`opus`, nỗ lực cao) và lượt 4 soát lỗi. Khác ở chỗ nguồn là hội thoại khách, việc và hướng dẫn của chủ trong ngày: chỉ giữ tối đa 10 điều **mới và có ích lâu dài**, mỗi điều có nguồn (cuộc chat, việc, ngày), nhãn MỚI / CỦNG CỐ / MÂU THUẪN, và một dòng "dùng thế nào". Điều chưa được chủ xác nhận thì ghi "chờ chủ xác nhận", không đưa cho bot trả lời khách.
