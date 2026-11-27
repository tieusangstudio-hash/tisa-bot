# Nhật ký cập nhật

***Tiếng Việt** · [English](CHANGELOG.en.md)*

Lịch sử phiên bản TISA BOT. Bản mới nhất ở trên cùng. Xem ngay trong app tại **Cài đặt → Cập nhật**.

Định dạng: mỗi phiên bản là một khối `## [x.y.z] - ngày`, bên dưới nhóm thay đổi theo `### Thêm mới / Sửa lỗi / Cải thiện / Bảo mật`.

## [0.631.26] - 2026-11-28
### Sửa lỗi
- **Bộ TISA V3.75:** (lấy từ bản thử nghiệm V3.77) Mở TISA BOT bằng tên miền mà chậm, báo "Đang kết nối lại máy chủ" rồi "Máy chủ TISA BOT đang tắt" dù máy chủ vẫn chạy: đường hầm Cloudflare mất hết kết nối nhưng tiến trình vẫn sống nên không tự nối lại. Nay cứ 30 giây TISA BOT hỏi đường hầm còn kết nối không, mất khoảng 2 phút liền thì tự khởi động lại đường hầm. Hay gặp sau khi máy ngủ dậy, đổi mạng hoặc tắt mở máy.

## [0.631.25] - 2026-11-28
### Cải thiện
- **Bộ TISA V3.74:** Nhiều máy dễ làm hơn cho người không rành công nghệ. Đầu trang hỏi "Đây là MÁY CHÍNH hay MÁY PHỤ". Máy chính chỉ còn 3 bước, mỗi bước một nút: (1) **Nhờ Đạt Đấu Nối lấy giúp** chìa khóa Cloudflare: Đạt tự mở Cloudflare, tạo token đúng quyền và cất kín vào máy, anh chỉ đăng nhập Cloudflare khi được hỏi; (2) **Tạo giúp mật khẩu dễ nhớ** cho bộ não, có nút Chép và ô xác nhận đã ghi lại; (3) **Dựng Trạm**. Bước nào xong tự hiện dấu ✓, còn thiếu gì trang nói rõ.
- **Bộ TISA V3.74:** Thêm máy phụ theo đúng thứ tự: cài TISA BOT ở máy phụ (hướng dẫn mở Terminal hay PowerShell từng phím, nút tải bộ cài Windows, hoặc **Nhờ Claude cài**: chép một đoạn dán vào Claude Code là Claude tự cài cho cả Mac lẫn Windows), chọn "Đây là MÁY PHỤ", rồi mới tạo dòng ghép. Máy phụ mở được máy chính ngay trên nó bằng tên miền để lấy dòng ghép, bấm "Dán dòng ghép vừa chép" là xong, khỏi chuyển mã giữa hai máy.

## [0.631.24] - 2026-11-27
### Sửa lỗi
- **Bộ TISA V3.73:** Giọng đọc gọi đúng tên "TISA BOT" (đọc là Ti-sa Bót), không còn đọc thành "gia vít" nghe như Javis. Áp dụng cho nút Nghe thử, đọc câu trả lời và ghi chú giọng nói; cuộc gọi ChatGPT Live và Live qua API cũng được dặn đọc tên đúng. Phần nghe vẫn hiểu khi anh gọi nhầm thành Javis.

## [0.631.23] - 2026-11-27
### Thêm mới
- **Bộ TISA V3.72:** **Nhiều máy** có trong bản này (trước chỉ có ở bản thử nghiệm). Một bộ não chạy trên 2 máy trở lên: máy chính nhận khách, chạy lịch; máy phụ làm việc nặng (dựng video) hoặc chờ thay máy chính khi đi xa. Vào **Hệ thống → Nhiều máy**: máy chính chọn "Máy đầu tiên", dán token Cloudflare, đặt mật khẩu bộ não, bấm Dựng; máy phụ cài TISA BOT như bình thường rồi chọn "Máy thêm vào" và dán dòng ghép. Máy phụ nhận đủ bộ não, MCP, API, kết nối. Bộ não được mã hóa ngay trên máy trước khi gửi lên Trạm.
- **Bộ TISA V3.72:** An toàn khi nâng cấp: chưa bật Nhiều máy thì máy chạy y như cũ, không đổi dữ liệu hay kết nối nào. Dựng Trạm trên tài khoản Cloudflare đã có Trạm TISA khác thì tự đặt tên mới (tram-tisa-2...), không ghi đè Trạm đang chạy.

## [0.631.22] - 2026-11-27
### Cải thiện
- **Bộ TISA V3.71:** Tâm Tổng Quản tự đề xuất nhân sự mới. Khi giao việc mà trong đội chưa ai hợp chuyên môn (ví dụ hợp đồng, SEO kỹ thuật, tuyển dụng) và loại việc đó sẽ còn lặp lại, Tâm vẫn làm xong việc hôm nay, đồng thời lên mạng tìm kỹ năng có sẵn (kho công khai trên GitHub, không cần anh nối tài khoản GitHub; chỉ đọc, không chạy mã lạ) và trình một phần **Đề xuất tạo nhân sự mới** ghi rõ tên, việc, kỹ năng, nguồn và vì sao cần. Anh bấm **Duyệt** là Tâm tạo người đó (kỹ năng, hồ sơ, đăng ký lên bảng, chạy thử); bấm Sửa lại để đổi đề xuất; bỏ qua thì không tạo và Tâm không đề xuất lại.

## [0.631.21] - 2026-11-27
### Cải thiện
- **Bộ TISA V3.70:** Trang Giao dự án dễ theo dõi hơn. Tên việc ngắn gọn: việc chỉ là một đường link thì hiện "Việc với trang z4z.poha.vn" (link nằm ở dòng dưới), không còn nguyên link dài; link giữa câu được thay bằng tên trang. Mỗi việc trong "Cần anh" có thanh các bước: bước nào xong, đang làm, chờ anh duyệt, chờ anh làm hay bị kẹt, kèm một câu "đang ở bước mấy, ai làm, chờ gì".
- **Bộ TISA V3.70:** "Cần anh" gọn hơn: việc kẹt và chờ duyệt lên trước, hiện 5 việc đầu (bấm Xem thêm để xem hết). Việc chờ hơn 7 ngày gom vào một khối thu gọn, có nút **Gác lại cả N việc**. Mỗi việc có nút **Gác lại** để cất khỏi danh sách (có cập nhật mới thì tự hiện lại), khối "Đã gác lại" cuối trang để đưa về. Việc nhiều phần chờ duyệt có nút Duyệt hết.
- **Bộ TISA V3.70:** Bố cục trang Giao dự án không còn khoảng trống lớn bên trái: màn hình rộng thì ô Giao việc bên trái (bám theo khi cuộn), Việc của đội bên phải.
- **Bộ TISA V3.70:** Tâm Tổng Quản thông minh hơn: hỏi gom MỘT lần ngay khi nhận việc mọi thứ chỉ anh đưa được (ngân sách, link, ảnh thật, quyền tài khoản...), kèm gợi ý sẵn để anh chỉ cần trả lời "ok", nên việc không còn kẹt giữa chừng. Tâm đọc trang khi việc chỉ là một link, dùng lại kết quả cũ cùng chủ đề, chia đúng người theo bảng phân công, cho các phần độc lập chạy song song, tự soát trước khi trình duyệt, báo cáo 3 dòng Đã xong, Đang làm, Cần anh, và ghi nhớ góp ý "Sửa lại" của anh thành luật cho lần sau.

## [0.631.20] - 2026-11-27
### Sửa lỗi
- **Bộ TISA V3.69:** Nút **Mở như app** luôn có ở chân menu trên máy tính (trước đây chỉ có trên điện thoại, còn nút trên thanh trạng thái chỉ hiện khi Chrome hay Edge tự cho cài, nên hay biến mất). Bấm vào: trình duyệt cho cài thì hiện ngay nút Cài, không thì chỉ đúng cách cài của trình duyệt đang dùng (Chrome, Edge, Safari trên Mac), báo khi địa chỉ không có https nên không cài được, và gợi ý ngồi ở chính máy chạy TISA BOT thì mở http://127.0.0.1 để cài app chạy thẳng trên máy, không đi vòng qua Cloudflare.
### Cải thiện
- **Bộ TISA V3.69:** Truy cập từ xa bằng Cloudflare: thẻ trong Cài đặt cho biết máy này nối vào trạm Cloudflare nào (Singapore, Hong Kong hay Frankfurt...) và trình duyệt đang xem đi qua trạm nào. Trạm ở xa (châu Âu, Mỹ) thì báo rõ là sẽ chậm và chỉ cách khắc phục: bấm Kết nối lại, mở thẳng 127.0.0.1 khi ngồi ở máy đó, hoặc dùng chế độ Tailscale khi ở xa.

## [0.631.19] - 2026-11-27
### Sửa lỗi
- **Bộ TISA V3.68:** Mở khóa máy Mac từ xa: trước khi gõ mật khẩu, TISA BOT xóa sạch ô mật khẩu (ô còn sót ký tự từ lần gõ trước thì mật khẩu đúng vẫn thành sai). Trên macOS 26, TISA BOT giờ đếm được số ký tự đã vào ô bằng cách khác, nên phím bị nuốt thì tự xóa gõ lại thay vì nhấn Enter rồi tính một lần thử sai. Gõ lại thì bấm thẳng vào ô, không bấm ảnh đại diện nữa. Nhật ký ghi rõ khi không đọc được số ký tự.

## [0.631.18] - 2026-11-27
### Cải thiện
- **Bộ TISA V3.67:** Tab Quy trình: nhấn Enter là để TRAO ĐỔI (hỏi, sửa bước, góp ý, kêu lưu ghi nhớ), không còn tự chạy cả quy trình. Muốn chạy từ bước 1 thì bấm nút **Chạy quy trình** (hoặc nhắn "chạy: ..."); "chạy tiếp" và "sửa bước N" vẫn làm ngay như trước. Muốn quay lại kiểu cũ: TISA_QUY_TRINH_ENTER_CHAY=1.
- **Bộ TISA V3.67:** Đang chạy quy trình, cứ 10 giây khung chat báo đang ở bước mấy, cộng sự nào làm, đã chạy bao lâu, vừa dùng công cụ gì, để biết bot không bị treo. Quy trình dừng giữa chừng hoặc chờ anh duyệt thì chuông báo ngay; chạy xong bình thường thì không làm phiền.
- **Bộ TISA V3.67:** Bước quy trình chạy nhanh hơn: trong lúc bước này làm, TISA BOT mở sẵn Claude cho bước kế tiếp (khởi động và nối công cụ trước), tới lượt chỉ việc gửi việc. Mỗi bước vẫn một phiên riêng, không lẫn ngữ cảnh; máy thiếu RAM thì tự bỏ qua. Tắt: TISA_WORKFLOW_MO_SAN=0.
### Thêm mới
- **Bộ TISA V3.67:** Lịch chạy quy trình. Trong tab Quy trình, cột phải có khung **Lịch chạy**: chọn giờ và ngày (mỗi ngày, thứ 2 đến thứ 6, cuối tuần) rồi bấm Đặt lịch. Hoặc nhắn thẳng trong ô quy trình: "chạy mỗi ngày lúc 6h sáng", "tắt lịch". Tới giờ quy trình tự chạy, kết quả về đúng ô chat của quy trình và hòm thư.
### Sửa lỗi
- **Bộ TISA V3.67:** (lấy từ Javis 0.645) Bước quy trình kiểm mãi không đạt, hoặc quy trình chờ duyệt, giờ thành câu hỏi ở trang Nhiệm vụ và trên chuông; trước đây việc bị chạy lại âm thầm hoặc kẹt mà không hỏi gì. Bước chạy bằng model API giữ đúng mức suy nghĩ của trợ lý, không còn bị tắt suy nghĩ.

## [0.631.17] - 2026-11-26
### Sửa lỗi
- **Bộ TISA V3.66:** Thanh "đang làm" (tình hình việc đang chạy) ở trang Trò chuyện không còn nằm lệch sang trái. Nay thẳng hàng với thanh cuộc gọi và khung tin nhắn.

## [0.631.16] - 2026-11-26
### Cải thiện
- **Bộ TISA V3.65:** Khi TISA BOT bấm trên trang web, con trỏ hiện ra là mũi tên chuột màu cam viền trắng (giống con trỏ cam trên máy tính), đầu mũi tên chỉ đúng chỗ bấm và nhấn nhẹ mỗi lần bấm, thay cho chấm tròn cam trước đây. Rõ trên cả nền sáng lẫn nền tối.

## [0.631.15] - 2026-11-26
### Cải thiện
- **Bộ TISA V3.64:** Điều khiển máy tính dùng đúng thế mạnh của agent-desktop (đã đi kèm từ V3.45). Nhật ký trên máy thật cho thấy AI gần như chỉ chụp ảnh rồi bấm theo toạ độ (16 ảnh, 0 lần tìm nút theo tên), vì hướng dẫn điều khiển máy vẫn dạy chụp ảnh trước. Nay AI tìm nút theo tên rồi bấm theo mã trước (khoảng 150 token thay vì 1.200 token mỗi ảnh, không lệch toạ độ, không di chuột thật), chỉ chụp ảnh khi không tìm được.
- **Bộ TISA V3.64:** Thêm lệnh chờ đúng thứ cần chờ: chờ tới khi một dòng chữ, một cửa sổ hoặc một nút xuất hiện (hay bấm được) rồi mới làm tiếp, thay cho chờ cố định rồi chụp ảnh xem lại.
- **Bộ TISA V3.64:** Làm nhiều bước theo mã trong MỘT lệnh (ví dụ điền 3 ô, bấm Gửi, chờ chữ "Đã gửi"), mỗi bước vẫn qua đủ chốt an toàn (duyệt, chống chen, ứng dụng ngân hàng, mật khẩu); lô chỉ gồm bước theo mã thì không kèm ảnh. Ít lượt AI suy nghĩ hơn nên việc trên máy xong nhanh hơn.

## [0.631.14] - 2026-11-26
### Cải thiện
- **Bộ TISA V3.63:** Điều khiển máy tính trên Windows nhanh hơn rõ rệt. Mỗi cú bấm, gõ hay cuộn của AI trước đây mở ít nhất hai cửa sổ PowerShell chỉ để đọc tên ứng dụng đang ở trước (một lần kiểm an toàn trước khi làm, một lần ghi kèm ảnh sau khi làm), tốn khoảng 1 đến 3 giây mỗi thao tác. Nay đọc thẳng bằng API của Windows, dưới 1 mili giây. Xem danh sách ứng dụng và chuyển sang ứng dụng khác cũng không còn mở PowerShell. Nếu cách mới không đọc được thì tự quay về cách cũ.

## [0.631.13] - 2026-11-26
### Sửa lỗi
- **Bộ TISA V3.62:** Máy Windows không còn nháy cửa sổ đen khoảng 1 giây rồi tắt trong lúc dùng. Nguyên nhân: Codex, Claude Code, Grok và các nguồn MCP (npx) được chạy ở chế độ "không có cửa sổ", nên mỗi lệnh mà CHÍNH chúng chạy cho AI (PowerShell, cmd, node) lại bị Windows cấp một cửa sổ đen mới, lặp lại mỗi lần AI dùng công cụ. Nay mọi chương trình con dùng chung cửa sổ ẩn sẵn có của TISA BOT, nên cả con lẫn "cháu" đều không hiện gì. Nút dừng lệnh trong terminal của AI trên Windows cũng gửi được tín hiệu tới đúng lệnh. Muốn quay lại cách cũ: đặt `TISA_AN_CUA_SO_CU=1`.

## [0.631.12] - 2026-11-26
### Sửa lỗi
- **Bộ TISA V3.61:** Bớt đứng cả hệ thống khi nhiều ô chat cùng làm việc. Mỗi lượt chat trước đây soát lại toàn bộ thư mục skill ngay trên luồng chính, kể cả hơn 20.000 tệp thư viện của skill dựng video (`node_modules`, `.venv`): đo trên MacBook mất 0,8 giây mỗi lượt (lần đầu sau khởi động 10 giây), trong lúc đó mọi ô chat khác đứng theo; máy Windows còn lâu hơn. Nay bỏ qua các thư mục thư viện đó khi soát và sao chép (bản sao nối thẳng về bản gốc), còn khoảng 0,1 giây.
- **Bộ TISA V3.61:** Các việc nặng không còn chạy trên luồng chính: dựng lời dặn cho chat với cộng sự, mở video hay ảnh không tìm thấy (quét thư mục tới 4 giây), hỏi trạng thái trình duyệt TISA (khi trình duyệt đang tắt, máy Windows chờ 0,6 giây mỗi lần hỏi), và bước AI đọc tin trong ô chat quy trình (tới 45 giây, trước đây chặn cả tab). Một ô chat đang chạy không còn làm các ô khác khựng theo.
- **Bộ TISA V3.61:** Máy Windows: một kết nối rớt không còn làm máy chủ ngừng nhận kết nối mới (trông như treo hẳn tới khi khởi động lại). Dùng Grok không còn làm cả máy chủ đứng vài giây. Hai bản sửa này lấy từ Javis OS 0.642.3 và 0.645.1.
### Cải thiện
- **Bộ TISA V3.61:** Bảng giao việc (Đội Quân) chạy được tới 3 việc cùng lúc. Trước đây việc thứ hai phải chờ cả đội làm xong việc thứ nhất. Hai lần gửi cho CÙNG một việc (ví dụ gửi sửa khi việc còn đang chạy) vẫn chạy lần lượt. Đổi số việc chạy cùng lúc bằng `TISA_DOI_QUAN_SONG_SONG` (1 đến 4; đặt 1 để như cũ).

## [0.631.11] - 2026-11-25
### Sửa lỗi
- **Bộ TISA V3.60:** Mở khóa máy Mac từ xa không còn "lúc được lúc không". Nguyên nhân: màn hình khóa vừa sáng hay nuốt phím đầu, nên mật khẩu ngắn (ví dụ 4 chữ số) chỉ cần rơi một phím là sai (nhật ký 19/11 ghi ô chỉ có 3 chấm), và chương trình cứ nhấn Enter dù ô chưa đủ ký tự. Nay trước khi nhấn Enter, TISA BOT đếm số chấm trong ô mật khẩu: thiếu hoặc thừa thì xóa gõ lại (tối đa 3 vòng), và vì chưa nhấn Enter nên không bị tính là một lần thử sai (tránh dồn tới 3 lần rồi bị dừng 30 phút). Máy nào macOS không cho đếm chấm thì làm như cũ.
- **Bộ TISA V3.60:** Trước khi gõ, thử tối đa 3 vòng cho ô mật khẩu hiện ra và nhận con trỏ (trước chỉ thử một vòng và bỏ qua kết quả). Đọc ô ở mọi tiến trình màn hình đăng nhập thay vì chỉ cái đầu tiên. Kiểm máy có khóa hay không bằng giá trị thật của cờ khóa, không còn coi "có khóa trong danh sách" là đang khóa.
### Cải thiện
- **Bộ TISA V3.60:** Nhật ký mở khóa (`dieu-khien-may/mo-khoa-nhat-ky.jsonl`) ghi rõ từng giai đoạn: sẵn sàng gõ, ô mật khẩu thấy hay không, số chấm đọc được, gõ lệch phải gõ lại, chưa nhấn Enter. Lần nào còn lỗi, mở nhật ký là thấy lỗi nằm ở bước nào.

## [0.631.10] - 2026-11-25
### Thêm mới
- **Bộ TISA V3.59:** Quy trình đo thời gian từng bước để biết máy chậm ở đâu. Cuối mỗi lần chạy, tin kết quả có thêm một dòng ⏱, ví dụ: "B2 (viet-content) 95s: tới chữ đầu 40s [mở Claude 18s, công cụ 12s], làm 52s". "Tới chữ đầu" là thời gian từ lúc giao việc tới khi bước có chữ hoặc lệnh đầu tiên (gồm mở Claude, nối công cụ, nạp ngữ cảnh, model nghĩ). Số này cũng lưu vào lịch sử chạy và ghi vào `tisa.log` dòng `[workflow timing]`, để gửi cho TISA khi học viên báo chậm. Mở/nối công cụ là số ước lượng; tắt dòng ⏱ bằng `TISA_WORKFLOW_HIEN_THOI_GIAN=0`.

## [0.631.9] - 2026-11-25
### Sửa lỗi
- **Bộ TISA V3.58:** Ở tab Quy trình, nhắn "sửa bước 4" (hoặc "chỉnh bước 3 ảnh đẹp hơn") là TISA BOT sửa luôn đúng bước đó, không còn hỏi tới hỏi lui. Trước đây mỗi góp ý đi ba vòng: nói "em hiểu anh muốn..." chờ ok, làm thử một mẫu chờ ok, rồi mới làm thật. Nay làm trọn bước ngay, kèm vài tin trước của anh trong cuộc làm bối cảnh; góp ý chưa nói rõ đổi gì thì tự rà kết quả và sửa chỗ sai rõ nhất. Muốn xem mẫu trước thì nói "làm thử" hoặc "cho xem mẫu trước". Lần chờ duyệt dang dở từ kiểu cũ cũng được làm luôn khi anh nhắn tiếp.
- **Bộ TISA V3.58:** Sau khi sửa xong một bước, nói "chạy tiếp từ bước 5" là chạy các bước sau bằng kết quả bước vừa sửa (trước đây tin báo dặn vậy nhưng lại chạy lại từ bước 1). Câu "làm thử mẫu khác" ở lúc xem mẫu không còn bị hiểu nhầm là "ok, làm hết".

## [0.631.8] - 2026-11-25
### Sửa lỗi
- **Bộ TISA V3.57:** Quy trình có bước bị lỗi thì nhắn "chạy tiếp", "tiếp tục" hoặc "chạy từ bước 2" là TISA BOT chạy tiếp từ đúng bước hỏng, giữ nguyên kết quả các bước đã xong. Trước đây tin đó bị coi là một lần chạy mới nên quy trình làm lại từ bước 1, rất lâu trên máy Windows. Tin có đề bài khác (ví dụ "tiếp tục viết bài về cà phê") vẫn chạy như một lần chạy mới.
- **Bộ TISA V3.57:** Bước quy trình gặp lỗi tạm thời (máy chủ quá tải, quá nhiều yêu cầu, rớt mạng) tự thử lại tối đa 2 lần, chờ 8 giây rồi 25 giây, thay vì dừng cả quy trình. Chỉ thử lại khi bước chưa làm gì ra ngoài. Hết lượt gói, lỗi đăng nhập hoặc lỗi lạ vẫn dừng như cũ. Đặt `TISA_WORKFLOW_AUTO_RETRIES=0` để tắt.
### Cải thiện
- **Bộ TISA V3.57:** Cột phải và lịch sử chạy chỉ báo lỗi ở bước khi bước đó thật sự hỏng, không còn tô đỏ rồi mới chạy được lúc đang tự thử lại. Khung chat hiện dòng "Bước N gặp lỗi tạm thời, tự thử lại sau X giây".

## [0.631.7] - 2026-11-24
### Sửa lỗi
- **Bộ TISA V3.56:** Ở trang Cộng sự, tab Quy trình: nói "gửi qua đây", "gửi anh xem content", "sao anh không thấy content" không còn bị hiểu thành góp ý sửa rồi hỏi lại mãi mà không gửi gì. Nay TISA BOT gửi ngay nguyên văn kết quả của lần chạy trước (nói "content" thì ra đúng bước viết content).
- **Bộ TISA V3.56:** Quy trình hỏi lại tối đa hai vòng. Anh trả lời câu hỏi của TISA BOT xong là nó làm mẫu luôn, không cần gõ đúng chữ "ok". Nói "thôi" vẫn hủy được.
- **Bộ TISA V3.56:** Kết quả của từng bước quy trình được lưu tối đa 20.000 chữ (trước là 4.000), nên bài content dài không còn bị cắt giữa chừng khi xem lại.

## [0.631.6] - 2026-11-24
### Cải thiện
- **Bộ TISA V3.55:** Form Tạo quy trình dễ điền hơn cho người mới. Mỗi bước tách thành 4 ô có ví dụ mờ: Việc cần làm, Bước này lấy thông tin từ đâu (chọn trong danh sách, không phải gõ ký hiệu), Quy tắc phải tuân thủ, Kết quả mong muốn. Có nút chữ i để xem hướng dẫn, nút Điền ví dụ mẫu vào các ô còn trống và nút Điền quy trình mẫu 2 bước. Quy trình cũ mở ra và lưu lại vẫn giữ nguyên từng chữ.
- **Bộ TISA V3.55:** Thẻ "đang chạy ngầm" hiện tên dễ hiểu thay cho đường dẫn dài, kèm dòng tiến độ mới nhất của việc đó và "ghi X giây trước". Việc quá 20 phút không ghi gì thì đổi màu cảnh báo, để biết việc đang chạy đều hay đã đứng.

## [0.631.5] - 2026-11-24
### Sửa lỗi
- **Bộ TISA V3.54:** Mở TISA BOT nhanh hơn. Trước đây gói chương trình đầu tiên bị báo lỗi mỗi lần mở trang, và trình duyệt còn nhớ lỗi đó rất lâu nên phải tải từng tệp lẻ, chậm hơn. Nay tải đủ các gói như thiết kế.
- **Bộ TISA V3.54:** Nói "ok làm đi", "làm luôn", "triển khai đi" trong lúc có việc đang chạy không còn bị coi là lời xác nhận suông và bỏ qua. Câu đó được làm thật.
### Cải thiện
- **Bộ TISA V3.54:** Cuộc gọi bằng giọng nói chạy song song tối đa 3 việc cùng lúc, giống chế độ gọi nhanh. Máy yếu giao dồn nhiều việc không còn bị nặng hay đơ; vượt 3 việc thì TISA BOT báo rõ để giao lại sau khi xong bớt.
- **Bộ TISA V3.54:** Bỏ mục "Thư mục xem trong chat" khỏi menu Bộ não vì ít dùng.

## [0.631.4] - 2026-11-24
### Cải thiện
- **Bộ TISA V3.53:** Chat mượt hơn khi có công cụ kết nối bị hết hạn đăng nhập (HeyGen, Apify, Meta...). Trước đây mỗi lượt chat mới lại đi gõ cửa công cụ hỏng, có khi chờ tới 20 giây mới ra chữ đầu tiên. Nay công cụ hỏng được nghỉ ít phút; đăng nhập lại là dùng được ngay.
- **Bộ TISA V3.53:** Đồng bộ chat với bảng Đội Quân nhẹ hơn nhiều: không còn kéo cả hồ sơ của mọi cộng sự mỗi 2 giây, hỏi thưa hơn ở phần danh sách model. Máy yếu bớt giật.
- **Bộ TISA V3.53:** Tệp nhật ký `tisa.log` tự cắt khi quá 60 MB (trước đây phình mãi). Thêm tệp `tisa_cham.log` ghi lại đúng chỗ nào làm TISA BOT bị đứng quá 2,5 giây, để gửi cho TISA khi máy bị chậm.
### Sửa lỗi
- **Bộ TISA V3.53:** Khung trình duyệt cạnh chat không còn báo lỗi dài trong nhật ký khi anh đóng khung giữa lúc đang gửi dữ liệu.

## [0.631.3] - 2026-11-24
### Sửa lỗi
- **Bộ TISA V3.52:** Nút **Nói** lại viết lại câu cho đúng như trước. Bản V3.51 bỏ bước này với máy dùng gói thuê bao (Claude Code, Codex), nên nói sai thì chữ hiện sai y vậy.
- **Bộ TISA V3.52:** Chuyển sang một cộng sự khác lúc máy trả lời chậm không còn hiện nhầm cuộc trò chuyện của cộng sự trước, nên giao việc không bị dính vào việc đang làm của bạn kia.

## [0.631.2] - 2026-11-23
### Thêm mới
- **Bộ TISA V3.51:** Việc chạy nền bị ĐỨNG YÊN nay được phát hiện: trong 20 phút liền mà cả nhóm tiến trình không dùng CPU và thư mục làm việc không có tệp nào được ghi thì TISA BOT báo thẳng trong chat, rồi nhờ AI kiểm tra và chạy lại đúng bước kẹt (báo tối đa 2 lần, không tự dừng gì; lệnh chỉ ngồi đợi như `tail -F`, `sleep`, `until` thì bỏ qua). Ca thật: lệnh ghép clip (ffmpeg) kẹt từ 15:04, không báo lỗi, cả chat đứng im gần 2 tiếng tới khi anh hỏi.
- **Bộ TISA V3.51:** Nút **"Dừng việc đang làm, làm tin này ngay"** hiện ngay dưới tin anh nhắn khi AI đang làm dở mà chưa đọc tin đó. Bấm một lần là lượt cũ dừng và AI làm theo tin của anh (trước đây phải bấm Dừng rồi gõ lại). Cảnh video đã dựng được nhớ nên dừng giữa chừng không mất công; sửa riêng một cảnh thì chỉ cảnh đó được dựng lại.
- **Bộ TISA V3.51:** Hỏi tiến độ ("làm tới đâu rồi?", "xong chưa?", "sao im?") mà AI chưa đọc tin thì máy chủ tự trả lời sau khoảng 8 giây: lượt đã chạy bao lâu, bao lâu rồi không có tín hiệu, việc gần nhất AI làm, có việc nào đang tính toán hay đang đứng chờ lệnh gì. Không còn cảnh hỏi mà chat im.
### Cải thiện
- **Bộ TISA V3.51:** Dựng video bằng trình duyệt chuyên dụng của Remotion (chrome-headless-shell) thay cho Chrome thường: tự tải 1 lần (~140MB), không chiếm Chrome của người dùng, nhanh hơn rõ (cảnh 754 khung: 35-43 giây so với 55 giây; cảnh ngắn đạt ~32 khung/giây) và thêm luồng mới có tác dụng (mặc định 4 luồng mỗi cảnh). Các script của AI hay đặt sẵn `CHROME=Chrome thường`: nay bị bỏ qua (muốn ép dùng: `FORCE_CHROME=1`); không tải được thì rơi về Chrome thường. Skill đã cài tự được nâng lên khi khởi động, hướng dẫn skill dặn AI không đặt `CHROME=`.
- **Bộ TISA V3.51:** Câu cảnh báo "lượt đứng im" (V3.53) nay chỉ tới nút Dừng-và-làm-tin-này, không bắt nhắn "làm tiếp" nữa.
- **Bộ TISA V3.51:** Dựng nhiều video cùng lúc không còn tranh nhau làm máy nghẽn: mọi tiến trình dựng trên máy dùng chung một hàng đợi, tối đa 4 cảnh cùng lúc trên máy 12 nhân (đặt bằng `SLOTS`). Đã đo: quá 3-4 cảnh cùng lúc không nhanh thêm mà chỉ nghẽn và dễ treo. Cảnh dư xếp hàng và tự chạy khi tới lượt.
- **Bộ TISA V3.51:** Skill đã cài tự được nâng lên bản dựng mới khi khởi động (theo số bản `RENDER_REV`), bản cũ giữ lại thành `render.mjs.truoc-V3.52`.
### Sửa lỗi
- **Bộ TISA V3.51:** AI báo tiến độ kiểu "Đang ghép bản V2... Xong bước này em sẽ render lại rồi giao" rồi việc chạy nền xong nhưng chat im hàng tiếng, tới khi người dùng nhắn "xong chưa" mới trả lời. Nguyên nhân: câu đó không khớp mẫu lời hứa (mẫu này cố ý hẹp) nên việc nền không được gắn cờ "làm tiếp khi xong". Nay câu báo tiến độ "đang render/ghép/dựng/chạy..." hoặc "xong em sẽ..." cũng mở lượt nối tiếp khi việc nền xong (vẫn có trần 3 lượt nối).
- **Bộ TISA V3.51:** Bấm xem video trong chat không còn ra ô xám/404 khi AI ghi tên tệp rút gọn kiểu `023_BacSiTuan_..._V4.mp4`. Dấu `...` (hoặc `…`, `*`) trong tên tệp nay là ký tự đại diện: máy chủ tìm trong các thư mục anh cho xem và hiện đủ các tệp khớp (bản nhẹ và bản Full HD), bấm là xem được; cùng tên ở hai thư mục (bản chép) chỉ hiện bản mới nhất. Đường dẫn viết tắt kiểu `VIDEO DA DUNG/x.mp4` cũng tìm được.
- **Bộ TISA V3.51:** Ô "Đang soạn câu trả lời..." (và tin cuối cùng) không còn bị cắt mất viền đáy: khung chat nay chừa 14px dưới cùng nên cuộn xuống đáy vẫn thấy trọn phần tử cuối.
- **Bộ TISA V3.51:** Hỏi mà chat im ru nay được báo tình hình thật. Ca thật: AI chờ video dựng xong bằng lệnh `tail -n0 -F <log>` (chỉ báo dòng MỚI) trong khi video đã dựng xong từ trước, nên chờ mãi; tin nhắn của anh nằm trong hộp thư vì lượt chỉ đọc tin sau mỗi bước làm. Nay tin nằm quá 90 giây chưa được đọc thì máy chủ nhìn cây tiến trình rồi tự nhắn một câu: lượt đã chạy bao lâu, đang bận thật (lệnh nào, CPU bao nhiêu) hay đứng chờ lệnh gì, và cách thoát (Dừng rồi nhắn "làm tiếp"). Báo tối đa 2 lần, không tự ngắt lượt (đúng luật của repo: cắt một lượt đang chạy tốt tệ hơn để nó chạy lâu).
- **Bộ TISA V3.51:** Hướng dẫn skill dựng video dặn AI không chờ dựng bằng `tail -F` mà đọc cả file log (`until grep -q 'Xong sau' <log>`) hoặc xem file `.mp4`/`.hash` từng cảnh.
- **Bộ TISA V3.51:** Thẻ video/ảnh trong chat không còn chớp, giật khi AI đang làm việc. Nguyên nhân: khung chat vẽ lại bong bóng liên tục (đồng hồ việc chạy, chữ đổi), mỗi lần vẽ lại thẻ bị xoá rồi mới dựng lại sau gần một giây, ảnh bìa video tải lại từ đầu. Nay thẻ được giữ nguyên và đặt lại ngay trong lượt xử lý, trước khi màn hình kịp vẽ (đo trên trang thử: thẻ có mặt 37/37 lần đo, bản cũ 0/37).
- **Bộ TISA V3.51:** Dựng video không còn treo cả tiếng vì một cảnh kẹt. Đã gặp: Chrome của Remotion kẹt, một cảnh đứng im 30 phút ở 0% CPU trong khi các cảnh khác xong từ lâu nên video không bao giờ xong. `render.mjs` nay tự phát hiện cảnh không tiến thêm khung nào quá 150 giây (đặt bằng `STALL`), tự huỷ và dựng lại cảnh đó (tối đa 3 lần).
- **Bộ TISA V3.51:** Việc chạy nền xong rồi thì TISA BOT tự làm tiếp, không còn đứng im chờ anh nhắc "làm tiếp". Nguyên nhân: khi việc nền (vd dựng video) xong mà khung chat đang bận một lượt khác (vd anh hỏi "em làm tới đâu?" mở thêm một lượt chạy cả chục phút), phần làm tiếp chỉ chờ tối đa 10 phút rồi bỏ cuộc và báo "hội thoại bận quá lâu". Nay chờ ngắn thì tự chạy như cũ; bận quá 45 giây thì lời nhắc làm tiếp được bỏ vào hộp thư của lượt đang chạy (lượt đó đọc ở bước kế tiếp, hoặc chạy ngay sau khi lượt đó xong), không bao giờ rơi mất. Chỉ báo bỏ cuộc sau 6 giờ.
- **Bộ TISA V3.51:** Bấm xem được video, ảnh, âm thanh, PDF mà AI chép ra thư mục ngoài bộ não (vd Desktop/VIDEO DA DUNG): trước đây tên tệp trong chat chỉ là chữ trơ, không bấm được vì khung chat chỉ dò tên tệp trong bộ não. Nay tên tệp (tên trần, đường dẫn đầy đủ hoặc cả thư mục) nằm trong "Thư mục xem trong chat" sẽ hiện thẻ có ảnh/video thật, bấm mở trình xem. Thư mục nào chưa được thêm thì vẫn không xem được (thêm ở Hệ thống → "Thư mục xem trong chat"); sau khi thêm hoặc sau bản cập nhật, tải lại trang (Cmd+R) để tin cũ hiện thẻ.
### Ghi chú
- **Bộ TISA V3.51:** Gói này đưa sang bản 1 các nâng cấp mà bản thử nghiệm đã chạy từ trước (bản thử nghiệm gọi là V3.50 đến V3.57): bấm xem video/ảnh ngoài bộ não, không chớp giật thẻ video, dựng video có chốt chống treo và hàng đợi chung, việc chạy nền xong tự làm tiếp, canh việc nền đứng yên, nút "Dừng việc đang làm, làm tin này ngay", tự trả lời khi hỏi tiến độ. Chức năng dùng nhiều thiết bị (Nhiều máy) chưa đưa sang.

## [0.631.1] - 2026-11-23
### Thêm mới
- **Bộ TISA V3.50:** Quy trình sửa từng bước: gõ góp ý ở tab Quy trình, TISA BOT tự nhận ra đó là việc mới hay là sửa việc đang làm. Nếu là sửa thì chỉ chạy lại đúng bước liên quan, không chạy lại cả 5 bước. AI trả lời ngay cách hiểu của nó, làm MỘT bản mẫu cho anh xem, anh OK rồi mới làm lại cả bước. Nút "Lưu lại quy trình" ghi bài học theo từng bước để lần sau làm đúng ngay.
- **Bộ TISA V3.50:** Trang Giao dự án gộp "Cần anh" và "Đang làm" thành một khung "Việc của đội" có 3 nút lọc (Cần anh, Đang làm, Văn phòng nói). Bảng tiến độ 4 cột vẫn còn qua nút "Bảng tiến độ 4 cột". Menu bỏ hai mục Cần anh và Đang làm trùng lặp, "Thư mục xem trong chat" chuyển sang nhóm Bộ não (sau Kho tư liệu), Team chuyển xuống nhóm Năng lực.
- **Bộ TISA V3.50:** Tiết kiệm token khi chat với cộng sự có hồ sơ rất dài: mục nào quá dài chỉ nạp phần đầu kèm đường dẫn để cộng sự tự mở tệp khi cần chi tiết (hồ sơ dài nhất giảm khoảng 67% lời dặn, tắt được bằng `TISA_GON_HO_SO=0`); khôi phục ngữ cảnh chỉ dán tối đa 120.000 ký tự thay vì 300.000. Bot trả lời khách vẫn nạp đủ như cũ.
### Sửa lỗi
- **Bộ TISA V3.50:** Dòng báo "Em đang hiểu lại góp ý..." phía trên ô chat không còn bị cắt mép.
- **Bộ TISA V3.50:** Sửa bảo mật phần quên mật khẩu; bot Zalo OA và Messenger tự lùi khi nhân viên đang trả lời khách; token dài hạn cho Claude; đăng bài Page hẹn giờ; thông báo điện thoại. Giao diện ô nhập chat giữ nguyên như bản cũ.

## [0.617.13] - 2026-11-23
### Thêm mới
- **Bộ TISA V3.49:** Dựng video nhanh gấp khoảng 3 lần (skill Edit Video Studio): bộ dựng `render.mjs` viết lại. Tự chia nhiều cảnh chạy cùng lúc (đã đo: 1 cảnh dù 2 hay 10 luồng vẫn ~12 khung/giây, nhiều cảnh cùng lúc mới nhanh), nhớ cảnh đã dựng nên sửa một cảnh chỉ dựng lại đúng cảnh đó, kiểm ảnh/video thiếu trước khi mở Chrome (báo ngay thay vì hỏng sau 10 phút), khoá chống hai tiến trình dựng đè cùng một cảnh, ghi file nguyên vẹn (không để lại file dở). Video 10 cảnh trước mất 9 đến 16 phút, nay khoảng 3 phút. Mỗi lần TISA BOT khởi động tự đưa bản mới vào skill đã cài (sao lưu bản cũ thành `render.mjs.truoc-V3.49`), và sửa 2 dòng hướng dẫn cho AI không đặt luồng cao, không mở hai tiến trình.
- **Bộ TISA V3.49:** Thư mục xem trong chat (Hệ thống → "Thư mục xem trong chat"): cho khung chat phát video, hiện ảnh, nghe âm thanh, mở PDF nằm ở thư mục anh chỉ định ngoài bộ não (vd video dựng xong để ở Desktop), trước đây hiện ô xám vì tệp ngoài bộ não bị khoá. Chỉ phục vụ đuôi video/ảnh/âm thanh/PDF trong đúng thư mục đã thêm, vẫn bắt đăng nhập; không cho thêm cả Desktop, cả thư mục người dùng, thư mục ẩn, Library hay nơi cài TISA BOT; không đi qua `../` hay liên kết ra ngoài.

## [0.617.12] - 2026-11-23
### Sửa lỗi
- **Bộ TISA V3.48:** Tên phiên bản hiển thị là V3.48 (trước đó ghi V3.45), cùng một bộ tính năng với bản 0.617.11: khung Trình duyệt hai nút ① Chạy ngầm / ② Chrome ngoài và đấu nối MCP/API chọn hồ sơ Chrome.

## [0.617.11] - 2026-11-23
### Thêm mới
- **Bộ TISA V3.48:** Khung Trình duyệt có hai nút chọn rõ ràng: ① **Chạy ngầm** (trình duyệt riêng, AI làm ngay trong khung bên phải, đăng nhập một lần ngay trong khung) và ② **Chrome ngoài** (chọn một hồ sơ Chrome đã đăng nhập sẵn, AI mở tab ở cửa sổ Chrome bên ngoài). Mỗi ô chat nhớ lựa chọn của nó; dòng chữ dưới thanh giải thích kiểu đang dùng.
- **Bộ TISA V3.48:** Đấu nối MCP/API chọn được trình duyệt: ở hộp ⚙ Cài đặt của Đạt Đấu Nối (trang Kết nối) anh chọn ① Chạy ngầm hoặc ② Chrome ngoài kèm **hồ sơ Chrome đã đăng nhập đúng tài khoản cần nối** (Google, Meta, Cloudflare...). Lần đầu bấm "Nhờ TISA BOT kết nối giúp" mà chưa chọn thì hỏi một lần rồi nhớ; lựa chọn áp đúng cho ô chat của việc nối (cả khi giao việc không qua nút).
### Sửa lỗi
- **Bộ TISA V3.48:** Khung Trình duyệt: AI không còn mở Chrome ở ngoài khi ô chat đang có khung bên phải (lệnh `mo_chrome` chạy thẳng, bỏ qua khung). Ô chat anh đang mở mặc định dùng khung riêng; lệnh mở Chrome ngoài và đổi trình duyệt tự đổi hướng vào khung khi đang ①. Các ô chat cũ đang gắn "Chrome của anh" được trả về mặc định một lần, anh chọn lại ② thì được giữ.
- **Bộ TISA V3.48:** Việc giao bằng giọng nói (ChatGPT Live), việc nền, Kanban: gắn đúng ô chat đang mở (mã `voice:` và `web:` được nhận ra), nên khung đi theo AI thay vì đứng yên.
- **Bộ TISA V3.48:** Khung nhớ sổ tab sau khi khởi động lại; tab của chính bảng TISA BOT không lọt vào danh sách tab của AI; hết chớp khi giao việc kết nối; bỏ nút "Trình duyệt AI" trùng ở ô nhập (giữ nút Trình duyệt ở thanh trên).

## [0.617.10] - 2026-11-22
### Thêm mới
- **Bộ TISA:** Điều khiển máy tiết kiệm token: TISA BOT đọc nút, ô của ứng dụng ra chữ kèm mã (agent-desktop của Vercel Labs, đi kèm cho Mac và Windows), tìm nút theo tên rồi bấm thẳng, không cần ảnh chụp mỗi bước
- **Bộ TISA:** Trình duyệt tiết kiệm token: xem trang bản gọn (ít hơn 31-44% token), tìm nút theo chữ (op=tim, cả phần chưa cuộn tới, không phân biệt dấu), sau mỗi lần bấm tự báo ngắn trang đổi gì thay vì đọc lại cả trang
- **Bộ TISA:** Toàn quyền: TISA BOT tự bấm Cho phép trên hộp 'Cho phép gỡ lỗi từ xa?' của Chrome; chưa Toàn quyền thì thẻ Cho phép hiện ở mọi máy đang mở TISA BOT
- **Bộ TISA:** Hộp chọn tệp / Tải lên: AI tự đi tới thư mục, chọn tệp và bấm Mở, không còn nhờ anh bấm Enter
- **Bộ TISA:** Khung Trình duyệt có thêm Màn hình máy chủ: xem, bấm, gõ trên máy chủ từ máy khác; nút Mở khóa máy khi máy chủ đang khóa màn hình
- **Bộ TISA:** Sửa nút Trình duyệt ở ô nhập cho bằng các nút khác; ô nhập trên điện thoại bám sát bàn phím hơn

## [0.617.9] - 2026-11-22

## [0.617.8] - 2026-11-21
### Thêm mới
- **Bộ TISA:** Sửa lỗi chớp màn hình khi bấm xem hình, video, kết quả (bỏ làm mờ nền khung xem, bảng Trình duyệt không vẽ lại thừa).

## [0.617.7] - 2026-11-21
### Thêm mới
- **Bộ TISA:** báo cáo định kỳ gửi thẳng vào Zalo admin, giảm token chạy ngầm (bot khách nhẹ hơn mà trả lời y như cũ, cầu chì chống vòng lặp), ẩn bớt cộng sự, khung Tình hình công việc gọn hơn.

## [0.617.6] - 2026-11-21
### Thêm mới
- **Bộ TISA:** ô chọn bộ não ghi đúng số ghi chú thật thay vì 5000+, trang Cộng sự cho ẩn bớt cộng sự ít dùng.

## [0.617.5] - 2026-11-21
### Thêm mới
- **Bộ TISA:** nút Bàn giao dưới câu trả lời của cộng sự: phiếu tích chọn việc, giao cho cộng sự khác và nối đuôi nhiều bước.

## [0.617.4] - 2026-11-21
### Thêm mới
- **Bộ TISA:** việc giao qua cuộc gọi hiện Đang làm nền như lệnh gõ chữ, cúp máy vẫn thấy việc đang chạy.

## [0.617.3] - 2026-11-21
### Thêm mới
- **Bộ TISA:** sửa trang Bộ não: thu thanh Hội thoại bên phải hoặc kho ghi chú thì đồ thị tự canh lại, không còn bị lệch và cắt.

## [0.617.2] - 2026-11-21
### Thêm mới
- **Bộ TISA:** V3.36: Chuyển máy mang theo đủ các MCP tự cài (SnapGen, HeyGen, tisa-web...). Trước đây gói bỏ sót thư mục _mcp nên sang máy mới các MCP này không chạy được.

## [0.617.1] - 2026-11-20
### Thêm mới
- **Bộ TISA:** V3.35: nâng cấp lõi mới, sửa lỗi mất danh sách Chatbot, việc giao qua cuộc gọi không còn bị cắt khi cúp máy, sửa chữ khó đọc ở giao diện tối trang Kết nối.
- **Đồng bộ brain 2 chiều nối bằng tài khoản GitHub đã đăng nhập.** Ở trang Tự học, bấm Kết nối GitHub rồi Tạo repo riêng tư hoặc Chọn repo có sẵn. Không còn phải tự tạo token và dán URL.
- **Nối xong là đồng bộ ngay và bật tự động.** Máy thứ hai chọn cùng repo là kéo brain về.
- **Ai đang dùng token riêng vẫn chạy như cũ,** và có nút chuyển sang tài khoản GitHub đã đăng nhập để khỏi lo token hết hạn.
- **Trang Tài khoản có dòng "Quên mật khẩu hiện tại?"** ngay dưới nút Đổi mật khẩu. Trên Windows và Mac, bấm vào là TISA BOT mở thư mục cài đặt và chọn sẵn file reset, chỉ cần bấm đúp. Trên VPS, Docker, Hostinger thì hiện các bước đặt lại.
- **Mac có file `reset-auth.command`** làm đúng việc của `reset-auth.bat` trên Windows: xoá mật khẩu cũ để đặt lại từ đầu.
- **Kết nối Asana.** Trang Kết nối có thẻ Asana dùng MCP chính chủ bản V2: TISA BOT tìm và đọc việc, dự án, hạn chót, tạo và cập nhật việc, thêm bình luận. Đăng nhập ngay trong dashboard, chạy được cả trên VPS.
- Cần tạo một MCP app trong Asana một lần (khoảng 5 phút), thẻ có hướng dẫn từng bước. Mặc định ở mức Chỉ đọc.
- **Rời nhóm Zalo ngay ở menu "..." của trang Hội thoại.** Lịch sử chat vẫn giữ trong TISA BOT, ở bộ lọc Đã ẩn.
- **Nút Chặn có ở mọi kênh.** Messenger và Zalo chặn thật trên nền tảng; kênh khác chặn trong TISA BOT: bot im, chat ẩn đi, tin mới không làm nó hiện lại.
- **Thêm Bỏ chặn** cho cuộc chat đã chặn, trả lại đúng chế độ trả lời trước đó.
- **Tab Thông tin của team gọn lại như Zalo.** Ảnh, File, Link mỗi mục chỉ hiện vài cái mới nhất, kèm nút **Xem tất cả**.
- **Kho lưu trữ:** bấm Xem tất cả là mở ngay trong bảng bên, có ba tab Ảnh, File, Link, ô tìm không cần dấu, xếp theo ngày và phân trang 20 mục một trang.
- Mỗi file có ô màu ghi đuôi file, dung lượng, và báo **File không còn** khi file đã bị xoá hay dời đi. Team có hơn 200 file giờ xem được hết.
- **Link TISA BOT gửi trên Zalo cá nhân hiện thẻ xem trước.** Tin có link giờ hiện tiêu đề, mô tả và ảnh của trang ngay dưới chữ, như khi người thật gõ link trong app Zalo. Trước đây chỉ là link trần. Chủ báo ngày 19/11/2026.
- **Link TISA BOT gửi trên WhatsApp cũng hiện thẻ xem trước.**
- **Link mở thẳng một việc.** Địa chỉ dạng `#task=<mã>` mở trang Nhiệm vụ rồi mở đúng việc đó: việc của bạn (`m:`), nhắc hẹn (`r:`) hoặc việc TISA BOT làm (`k:`). Trang ngoài như bảng điều hành tự làm có thể dẫn thẳng tới một việc thay vì chỉ tới trang Nhiệm vụ.
- **Bot học từ câu bạn xác nhận.** Trên bản nháp ở Hộp thư có ô tick "Bot học câu này", bật sẵn. Gửi một câu có lệnh của bạn, hoặc câu bạn đã tự sửa, thì câu đó được ghi vào tài liệu của Agent (file `tri-thuc-chatbot/<tên-agent>.md`). Lần sau khách khác hỏi chuyện tương tự, bot trả lời theo đúng câu bạn đã xác nhận. Chuyện riêng của một khách thì bỏ tick.
- **Nhờ TISA BOT đặt lịch chạy script ngay trong chat.** Ví dụ "mỗi phút chạy check_shop.py": job chạy thẳng script, không gọi model nên rẻ, và chạy được mỗi phút.
- **Việc "Chờ bạn" của nhóm giờ trả lời được, không chỉ Thử lại.** Bấm **Trả lời** cạnh Thử lại: chọn "Làm tiếp" để thành viên làm lại bước đó kèm câu trả lời của bạn, hoặc "Hỏi lại" để hỏi rõ trước, việc vẫn chờ bạn.
- Câu trả lời và câu hỏi đều hiện trong khung chat của nhóm, có trích lý do việc dừng ở trên, nên đọc lại vẫn biết đang trả lời chuyện gì.
- **TISA BOT nhắn khách được ngay từ khung chat.** Bảo TISA BOT "trả lời chị Lan là còn size M", nó tìm cuộc chat trên trang Hội thoại rồi gửi đúng Page Messenger, Instagram, bot Telegram hay Zalo của cuộc đó, như bạn gõ ở Hộp thư. Trước đây TISA BOT báo thiếu công cụ gửi Messenger và bắt bạn tự dán tin.
- **Tin gửi đi ghi là của bạn, bot của cuộc đó vẫn chạy như cũ.** Chỉ bạn ra lệnh được việc này: khách nhắn bot không đọc hay nhắn được cho khách khác, và TISA BOT chỉ thấy cuộc chat của brain đang dùng.
- **Khung chat vẽ được công thức toán.** Công thức viết dạng `$...$`, `$$...$$`, `\(...\)` hoặc `\[...\]` giờ hiện thành phân số, căn, mũ như trong sách thay vì nguyên mã. Thư viện KaTeX chỉ tải lần đầu có công thức; mất mạng thì vẫn thấy mã gốc. Số tiền kiểu "$5 và $10" không bị nhận nhầm.
- **Đăng video lên Trang có ảnh bìa.** Công cụ đăng video nhận thêm ảnh .jpg/.png làm thumbnail mặc định, và có chế độ đăng dạng Reels. Kết quả ghi rõ ảnh bìa đã gắn hay chưa.
### Sửa lỗi
- **Thẻ cookie Facebook đọc được trang trở lại.** Khi mở trang bằng cookie trên trang Cookies, TISA BOT giờ gửi kèm các header điều hướng như trình duyệt thật (`Sec-Fetch-*`, `Accept`, `Upgrade-Insecure-Requests`). Trước đó Facebook trả lỗi 400 trước cả khi xét tới cookie, nên thẻ còn sống vẫn báo "lần gần nhất không tải được".
- **Mở lại hội thoại không còn lặng lẽ hiện bản cũ.** Máy chủ trả lời chậm hoặc lỗi thì khung chat báo rõ đang hiện bản lưu trên máy, kèm nút Thử lại, thay vì để tin cũ nằm đó như thể đã mới nhất.
- **Hội thoại tải mãi không mở được nay có lời báo.** Sau vài giây chờ, TISA BOT nói cuộc trò chuyện đang tải lâu và cho bấm Thử lại.
- **Một tin hiển thị lỗi không còn làm mất các tin sau nó.** Tin đó hiện dạng chữ thường, các tin còn lại vẫn đủ, và lỗi được ghi vào trang Sức khoẻ để dễ tìm nguyên nhân.
- **File reset không còn mở lại bộ cài đặt lần đầu** (model, kênh, khoá API giữ nguyên), và trên Mac mật khẩu cũ không còn tự quay lại ở lần khởi động sau.
- **Nhờ TISA BOT tự sửa mã nguồn TISA BOT không còn đỏ lỗi "không có quyền ghi vào tieusangstudio-hash/tisa-bot" ở máy người dùng.** Trước đây mọi máy đều tải repo gốc về, sửa cả lượt rồi mới hỏng ở bước đẩy. Giờ máy không có quyền ghi thì TISA BOT không tải, không sửa, mà viết sẵn một báo lỗi kèm hướng sửa và đưa link mở trang tạo Issue cho nhà phát triển. Bạn đọc lại, bấm Submit là gửi, không cần token hay quyền gì thêm.
- **Hội thoại của bot Telegram (và mọi kênh bot khác) hiện lại trong lịch sử của cộng sự nối với bot.** Bot nào được lưu brain theo một cách viết khác của cùng brain đó (đường dẫn đầy đủ từ bản cũ, có dấu `/` ở cuối, hay thư mục brain đã dời chỗ) vẫn trả lời bình thường, nhưng cuộc chat của nó không bao giờ lên cột Lịch sử của cộng sự. Giờ TISA BOT so theo brain mà hội thoại thực sự được lưu, và tên cộng sự có dấu tiếng Việt cũng khớp dù file tạo trên macOS.
- **Hồ sơ tự học không còn ghi "chủ cửa hàng".** Hồ sơ giờ gọi người đang chat là "đối tượng" và lấy họ làm chủ thể, ví dụ "đối tượng được gọi là anh Việt, đối tượng xưng anh", hợp cả khi bot không dùng cho kinh doanh. Hồ sơ cũ đổi theo ở lần cập nhật kế tiếp.
- **Chấm đỏ ở thư mục hội thoại chỉ hiện khi chat đã xong mà chưa đọc.** Chat còn đang chạy hiện vòng xoay chứ không làm sáng chấm đỏ ở thư mục, ở dòng "Chưa xếp nhóm", ở chính dòng chat và ở menu bên trái. Chat đang mở trên màn hình cũng không bị tính. Lượt chạy xong mà chưa được xem thì chấm đỏ mới hiện.
- **Bot Zalo cá nhân đọc được tin dạng thẻ link.** Trước đây một link người khác gửi (Zalo hiện thành thẻ có tiêu đề và ảnh) bị xếp vào loại "khác" nên bot bỏ qua, kể cả khi người gửi tag bot. Giờ thẻ link được đọc như tin chữ, gồm tiêu đề, mô tả và địa chỉ link.
- **Hộp thư và lịch sử giữ lại địa chỉ link.** Tin thẻ link không còn chỉ hiện dòng mô tả của trang mà có cả link để bấm, kể cả tin nhập lại từ lịch sử (tisa-zalo 1.14.0).
- **Kết nối nick Zalo thứ hai không còn làm nick thứ nhất mất kết nối.** Hai người báo ngày 19 và 20/11/2026: mỗi nick một bot ở hai brain, vừa quét QR nick thứ hai thì thẻ bot của nick thứ nhất báo "Một phiên khác của cùng nick đang giành kết nối Zalo" và bot lỡ phần lớn tin, dù không ai mở Zalo Web.
- **Quét QR bằng nick đã kết nối thì TISA BOT báo ngay, không tạo kết nối thứ hai.** Câu báo nêu tên kết nối đang giữ nick đó. Muốn nối nick khác, mở app Zalo bằng nick đó rồi quét lại.
- **Phóng to ảnh trong chat không còn dạt sang trái.** Bấm vào ảnh để xem cỡ thật, ảnh nhỏ hơn màn hình giờ nằm giữa, ảnh lớn hơn thì mở đúng chỗ vừa bấm.
- **Gọi `tisa_team` không còn báo "không tồn tại" khi hub bật chế độ lazy.** Khi có nhiều công cụ, hub giấu bớt sau ô tìm kiếm, nhưng trợ lý quen gọi thẳng tên nên bị báo lỗi. Giờ gọi thẳng tên vẫn chạy đúng công cụ, vẫn qua cùng lớp quyền. Lối tắt huỷ lịch nhắc cũng chạy lại được khi lazy bật.
- **/goal và /plan gõ ở cuối hay giữa câu giờ chạy được.** Trước đây chỉ ăn khi đứng đầu tin, gõ "...làm luôn giúp anh /goal" thì TISA BOT chỉ chat thường. Phần chữ còn lại thành nội dung của mục tiêu.
- **Skill, agent, workflow vừa cài giữa cuộc trò chuyện gọi được ngay bằng "/" ở giữa câu.** Trang nạp lại danh sách trước khi gửi nếu gặp tên lạ, không còn coi là chữ thường.
- **Gõ tên agent hay workflow không cần tiền tố.** "/seo-pro" mở thẳng agent seo-pro, như "/agent-seo-pro".
- **Dấu câu ngay sau lệnh không làm hụt lệnh.** "/viet-email," hay "/goal." vẫn được nhận.
- **Nút soạn trả lời khách làm đúng lệnh của chủ.** Gõ "lịch đã xác nhận 20h ngày 21 và 22" rồi bấm soạn, câu trả lời báo đúng lịch đó, không còn viết "em chưa có lịch xác nhận" chỉ vì tài liệu chưa có hay trước đó bot từng nói "đang kiểm tra". Lệnh của chủ là lời mới nhất, đứng trên tài liệu và lịch sử cuộc chat, không kèm danh sách câu cấm nào. Bấm Viết lại cũng theo lệnh đó.
- **Thẻ bot hiện tên Fanpage thay vì Page ID dạng số.** Trang gắn bằng cách dán token trước đây chỉ lưu ID nên chip kênh hiện một dãy số, khó biết là Trang nào. Nay mỗi lần bot khởi động, TISA BOT lưu tên thật của Trang và chip hiện tên đó. Nhãn bạn tự đặt (tên viết tắt) vẫn được ưu tiên, còn ID xem được khi rê chuột vào chip.
- **Việc chạy quy trình trên trang Nhiệm vụ biết đợi gói mở lại.** Trước đây bước nào vấp gói thuê bao hết lượt là việc thử lại ngay, đốt hết 3 lần thử trong vài giây rồi kẹt. Giờ việc tự hẹn chạy lại đúng giờ gói mở và không tính vào số lần thử.
- **TISA Store không còn trống trơn khi máy chưa đặt mật khẩu.** Cài gói cần đăng nhập thật, nên trước đây Store bị chặn mà không nói vì sao. Giờ trang nói rõ cần đặt mật khẩu và có nút Đặt mật khẩu dẫn thẳng tới trang Tài khoản.
- **Danh sách model Codex nhận đủ bản mới hơn đã cài.** TISA BOT so phiên bản Codex trên `PATH` với bản cài trong thư mục người dùng để không bỏ sót model mới.
- **TISA BOT không còn bị kẹt cảnh mất kết nối vì một bản chạy thừa giữ cổng.** Trên Mac, bản launchd quản lý giờ tự tắt bản TISA BOT chạy lạc rồi tiếp quản; bản thừa khác thì thoát ngay, không chạy phần khởi động.
- **Cập nhật trên Mac luôn đổi ca qua launchd**, kể cả khi lệnh kiểm tra của launchd lỗi, nên không còn sinh ra bản chạy ngoài launchd.
- **Duyệt một mốc của quy trình ở trang Nhiệm vụ thì quy trình chạy tiếp, không hỏi duyệt lại.** Trước đây mỗi lần trả lời, quy trình chạy lại từ bước đầu nên lại dừng đúng mốc cũ. Giờ trả lời "Duyệt", "ok" hay "đồng ý" là chạy tiếp từ mốc đó. Câu yêu cầu sửa vẫn cho quy trình làm lại kèm lời sửa như cũ.
### Cải thiện
- Công tắc Tự động và Đồng bộ cả ảnh có hiệu lực ngay, không cần bấm Lưu.
- **Nhóm Telegram có chủ đề (topic): bot trả lời đúng chủ đề người ta hỏi**, thay vì dồn hết về mục General. Trong nhóm, câu trả lời còn trích đúng tin được hỏi, nên đông người vẫn biết bot đang trả lời ai.
- **Khách gửi nhiều ảnh một lúc thì bot trả lời một lần**, xem đủ cả bộ ảnh, không còn trả lời tách thành hai ba lượt.
- **Bot xem được video khách gửi** (cắt vài khung hình, nghe cả lời nói nếu có key chuyển giọng nói). Vị trí, danh bạ, sticker và bình chọn khách gửi cũng tới được bot, trước đây bị bỏ qua.
- **Telegram giới hạn tần suất thì bot chờ rồi gửi lại**, câu trả lời dài được chia đúng chỗ xuống đoạn, video bot gửi đi xem được ngay trong chat.
- **Bot Messenger biết khách tới từ quảng cáo nào.** Khách bấm quảng cáo "Gửi tin nhắn", link m.me có mã, hay khung chat trên website: bot thấy tên quảng cáo hoặc mã link, kể cả khi khách mở lại một cuộc chat cũ từ quảng cáo rồi mới gõ.
- **Bot xem được video khách gửi** (cắt vài khung hình, nghe cả lời nói nếu có key chuyển giọng nói), thay vì chỉ nhận một đường link không mở được.
- **Sticker và nút thích (👍) được hiểu đúng là cảm xúc**, bot không còn tải về rồi tả lại như một bức ảnh. Trên Instagram, khách trả lời story hay nhắc tài khoản trong story thì bot biết.
- **Messenger giới hạn tần suất hoặc tạm lỗi gửi thì bot chờ rồi gửi lại**, không mất câu trả lời.
- **Bot WhatsApp đọc được đơn đặt hàng từ catalog.** Trước đây khách bấm gửi giỏ hàng thì bot bỏ qua cả đơn. Giờ bot thấy từng sản phẩm, số lượng, tổng tiền và lời nhắn kèm theo. Danh bạ khách gửi, biểu mẫu WhatsApp Flow, tên và địa chỉ của vị trí cũng tới được bot.
- **Bot biết khách tới từ quảng cáo nào** (quảng cáo bấm vào nhắn WhatsApp) và khách đang hỏi sản phẩm nào trong catalog, để trả lời đúng ý.
- **Bot đang tạm dừng hoặc bạn đang tiếp quản thì khách không còn thấy "đang soạn tin..." rồi im luôn.** Dòng đó chỉ hiện khi bot thật sự trả lời.
- **WhatsApp giới hạn tần suất thì bot chờ rồi gửi lại**, video gửi đi xem được ngay trong chat, ảnh quá cỡ tự gửi thành tài liệu thay vì báo lỗi.
- **Bot Slack trả lời đúng thread.** Trước đây, đang trả lời câu hỏi ở thread này mà có người nhắn ở thread khác cùng kênh thì câu trả lời có thể rơi nhầm sang thread kia. Giờ mỗi câu trả lời luôn về đúng thread của câu hỏi.
- **Khách nhắn tiếp trong thread cũ vẫn được trả lời sau khi TISA BOT khởi động lại**, không bị coi là người khác nói chuyện với nhau.
- **Hộp thư hiện tên kênh Slack** (ví dụ #sales), và bot báo ngay khi được thêm vào hoặc bị gỡ khỏi một kênh, giống Telegram. Chữ khách gõ như `a < b`, `@Kim`, đường link giờ tới TISA BOT đúng như khách gõ.
- **Slack đang giới hạn tần suất thì bot chờ rồi gửi lại**, không mất nửa câu trả lời. App tạo theo hướng dẫn cũ vẫn chạy; muốn có tên kênh thì dán lại manifest mới và cài lại app (docs/29-slack-whatsapp.md).
- **Đánh dấu chưa đọc được cả hội thoại đang mở.** Menu "..." của hội thoại đang xem giờ cũng có nút này. Bấm xong chấm đỏ hiện ngay và giữ nguyên, tới khi bạn mở hội thoại khác rồi quay lại, nên dễ đánh dấu những việc chưa xong để quay lại sau.
- **Trang Công cụ (Plugins) làm lại gọn như trang Nhiệm vụ.** Cột trái lọc theo trạng thái và nguồn, mục Tất cả là một danh sách liền xếp theo tên, công cụ của bạn và từ TISA Store có tag riêng.
- **Mỗi dòng chỉ còn tên, một dòng mô tả, mức quyền bằng chữ dễ hiểu và công tắc.** Bấm vào dòng để xem lệnh, phiên bản và nút Gỡ. Gỡ hỏi lại ngay trong trang và có Hoàn tác.
- **Nút "Thêm công cụ" gom ba cách thêm:** TISA Store, nhờ TISA BOT tạo trong chat, cài từ tệp .zip. Nút "Cài từ tệp .zip" vẫn đứng riêng cạnh đó.
- **Trình duyệt và Bộ nghe offline chuyển sang mục "Phần mềm trên máy"**, nút Gỡ không còn tô màu đặc. Trên điện thoại cột trái thành hàng chip, nút + tròn ở góc.
- **"Chưa xếp nhóm" cũng có chấm đỏ.** Cuộc chat chưa thuộc dự án nào mà có câu trả lời chưa đọc thì mục Chưa xếp nhóm trong ô chọn dự án hiện chấm đỏ, giống các dự án. Đọc xong hoặc xếp cuộc đó vào một dự án thì chấm tự tắt.
- **TISA BOT tìm đúng tool hơn hẳn khi có nhiều nguồn.** Câu hỏi đời thường như "doanh thu hôm nay trên POS", "lịch sử tin nhắn Zalo", "chi phí Google Ads" giờ ra đúng tool, kể cả khi mô tả tool viết tiếng Anh. Trên bộ 55 câu thử thật, tỉ lệ tìm trúng từ 20 lên 55.
- **Nêu tên nguồn là ra danh sách tool của nguồn đó**, và nhiều tài khoản cùng loại (ba shop POS, hai Zalo) được gộp một dòng, không còn chiếm chỗ của tool khác.
- **Gọi tool thiếu tiền tố hay gõ sai tên vẫn chạy** nếu chỉ có một tool khớp, nhiều tool khớp thì TISA BOT nêu tên để chọn. Kết quả tìm cũng ngắn hơn để vẫn tiết kiệm token.
- **Hội thoại chưa đọc lên đầu danh sách.** Các cuộc có chấm đỏ giờ gom thành nhóm **Chưa đọc** ngay dưới nhóm Đã ghim, kể cả cuộc cũ nằm tận trang sau. Đọc xong thì cuộc đó về lại đúng chỗ theo ngày.
- **Tab Đã học và Tài liệu chia trang, mỗi trang 20 mục.** Danh sách dài có ô tìm (gõ không dấu vẫn ra) và nút Thêm đứng ngay trên đầu, khỏi phải cuộn hết danh sách.
- **Ghi chú Đã học dễ nhìn hơn.** Lọc nhanh theo Sự thật, Quyết định, Thuật ngữ; mỗi loại một màu; ghi chú của bạn có vạch cam bên trái.
- **Sửa ghi chú, bài học, mô tả tài liệu trong một khung rộng.** Thay cho ô nhập một dòng của trình duyệt: chữ hiện trọn, có đếm ký tự, đổi được loại ghi chú, Ctrl+Enter để lưu. Trên điện thoại khung kéo từ dưới lên.
- **Chuông thông báo gọn hẳn.** Câu trả lời của trò chuyện, cộng sự và team không còn đẩy lên chuông. Thay vào đó là **chấm đỏ** ở mục Trò chuyện, Cộng sự, Team trên menu, như chấm đỏ đang có ở từng cuộc chat.
- **Việc chạy theo lịch không còn kêu mỗi lần chạy.** Kết quả vẫn về đúng khung chat hoặc Telegram, chuông chỉ kêu khi việc lỗi hẳn, hoặc khi chính lần chạy thấy có chuyện anh cần ra tay.
- **Tiêu đề thông báo dễ đọc hơn.** Mỗi lần chạy tự viết một dòng tiêu đề ngắn nói kết quả, không còn kiểu "Em kiểm tra..." và không lặp lại tiêu đề ở dòng dưới.
- **"A.I. soạn" đổi tên thành "TISA BOT soạn"** ở nút trong ô nhập, chế độ trên đầu cuộc chat và các dòng của bản nháp.
- **Kết quả của lịch được lưu đủ, không còn cắt ở 2.000 ký tự.** Lần chạy sau vẫn chỉ đọc phần đầu cho gọn, nhưng giờ biết rõ là đã bị cắt.
- **Lịch lặp bị lỡ lượt thì trang Nhiệm vụ ghi "lỡ N lần".** Trước đây khi một lượt chạy trễ hay chạy lâu, các lượt kế bị bỏ qua mà không ai biết.

## [0.593.0] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Mục Team chuyển vào nhóm Đội Quân AI, nằm trên Cần anh
- **Bot đọc được file nhân viên gửi cho khách trên Zalo OA và Fanpage.** Báo giá PDF, Word, Excel hay ảnh nhân viên gửi từ app OA hoặc hộp thư Trang giờ hiện trong Hộp thư (nhãn Nhân viên), và bot biết nội dung để trả lời khi khách hỏi lại. Ảnh được một bộ não đã kết nối có mắt đọc hộ.
- **Bot đọc được file PDF, Word, Excel khách gửi**, không chỉ biết là "có file" như trước.
### Cải thiện
- **Cần bật thêm một lần:** Zalo OA bật sự kiện `oa_send_text`, `oa_send_image`, `oa_send_file` ở mục Webhook của app. Fanpage bấm **Sửa tự động** ở bảng kiểm tra để TISA BOT bật `message_echoes`.
- **Bấm "A.I. viết" hay "Viết lại" ở Hộp thư giờ thấy ngay A.I. đang làm gì.** Chỗ bản nháp sẽ hiện ra có một khung "A.I. đang viết": biểu tượng nhấp nháy, dòng chữ nói bước hiện tại (đọc cuộc chat, tra tài liệu, xem ảnh khách gửi, viết câu trả lời), số giây đã chờ và ba vạch chạy. Quá 25 giây thì khung nói nhẹ nhàng là A.I. vẫn đang viết, để không ai tưởng bị lỗi.
- **Soạn nháp nhanh hơn một chút:** tra tài liệu, lấy ngữ cảnh plugin và xem ảnh khách gửi giờ chạy cùng lúc thay vì lần lượt.
- **Số tin chưa đọc của cộng sự nằm ở góc dưới trái avatar.** Giờ chat có chỗ riêng ở góc dưới phải, dòng thoáng hơn trên điện thoại, và dải avatar thu gọn trên máy tính giờ cũng thấy ai có tin mới.
- **Team chỉ tải các tin gần nhất, cuộn lên mới tải tiếp tin cũ.** Gần tới đầu khung chat là tự tải thêm một trang, giữ nguyên chỗ đang đọc, giống khung chat chính và trang Chatbot. Lúc đang tải hiện dòng "Đang tải tin cũ...".
- **Việc chạy nền trên bộ não dùng khóa API gửi ít token hơn khoảng 60%.** Việc Kanban, việc lặp và nhắc hẹn có làm việc mang bộ luật việc nền ngắn thay cho toàn bộ bộ luật chat, ở mỗi lần gọi công cụ. Mọi luật về hành động được giữ nguyên: làm đúng việc trong mức quyền, không bịa số, báo kết quả về đúng người giao, không hứa suông, không tự tạo thêm việc, plugin mới luôn tắt. Thử bằng model thật trên 7 loại việc nền mẫu, kết quả ngang bản đầy đủ.
- **Gói thuê bao không đổi.** Claude Code, ChatGPT, Grok, Antigravity vẫn mang bộ luật đầy đủ. Bật thử cho khoảng 10% việc chạy nền, tắt theo mức Tắt.
### Sửa lỗi
- **Nhóm Zalo mới vào cũng có tên.** Bộ Zalo (tisa-zalo 1.12.0) trước chỉ nạp tên nhóm một lần lúc khởi động, nên nhóm nick vào sau đó hiện thành "Nhóm …" kèm đuôi id cho tới lần khởi động lại. Giờ tin đầu tiên từ nhóm lạ sẽ kèm tra tên nhóm, và nhóm đổi tên cũng được cập nhật.
- **Ô chọn nhóm của Chatbot không còn hiện id trần.** Nhóm đã tick mà ô tìm lọc mất, hoặc cũ hơn 80 cuộc chat gần nhất, trước đây hiện thành dãy số dài. Giờ nhóm nào cũng mang tên thật lấy từ Hộp thư, nhóm chưa rõ tên thì hiện "Nhóm …" kèm đuôi id.
- **Biểu tượng chờ ở trang Chatbot giờ quay thật.** Trước đây nút "A.I. đang viết...", nút Gửi bản nháp, mic lúc đang chép lời và thẻ hồ sơ khách đều đứng im.
- **Mở một team không còn kẹt lâu ở "Đang tải tin nhắn của nhóm".** Mỗi lần mở, máy chủ từng cộng lại chi phí model của cả team từ trước tới nay, team càng lâu càng chậm, trong khi màn hình không còn hiện con số đó. Giờ bỏ hẳn bước này khi mở team.
- **Số tiết kiệm ước tính trên trang Mức dùng nay đúng với thứ thật sự được gửi.** Mức Tối ưu trước đây chỉ tính bản luật rút gọn và quên phần nền vẫn gửi kèm (có khối luật kênh chat), nên trang báo bớt 84% cho mọi bộ não. Nay: bộ não dùng API key thấy con số thật, còn gói thuê bao (Claude Code, ChatGPT...) thấy rõ là bộ luật được giữ nguyên, chỉ bộ nhớ và skill nạp phần liên quan.
- **Số token đã tiết kiệm cộng dồn không còn tính mọi lượt ở mức Siêu tiết kiệm như lượt đi đường tắt.** Chỉ câu hỏi đơn giản đi đường tắt, nên phần cộng dồn tính theo giá mức Tối ưu; phần "đo được" của trang vẫn cho thấy đường tắt bớt thật bao nhiêu.
- **Chạy đủ bộ test trên máy không còn tự báo đỏ ở lần sau.** Tệp sổ lượt chat (`turn_ledger.sqlite3`) mà test tạo ra trong `server/` nay được git bỏ qua như các kho dữ liệu chạy khác.

## [0.589.0] - 2026-11-18
### Cải thiện
- **Skill dài nạp có chọn lọc, TISA BOT chọn trước khi nạp.** Với skill kiểu thực đơn như trình tạo agent/loop/plugin, TISA BOT chỉ nạp phần yêu cầu cần cùng mọi mục luật (và phần nó dặn tạo trước, như workflow kéo theo mẫu agent), nhẹ hơn khoảng 47-63%. Đo bằng model thật trên 7 loại yêu cầu, câu trả lời đủ ý như khi nạp cả skill.
- **Mọi ngôn ngữ như nhau.** Cách chọn không dựa vào tiếng Việt hay tiếng Anh: tách chữ được mọi hệ chữ (kể cả Trung, Nhật, Hàn, Thái), nhận cả từ có đuôi biến đổi (tiếng Nga, Đức, Thổ, Hàn), và tự tìm từ thừa ngay trong skill. Người hỏi bằng ngôn ngữ khác skill thì model tóm việc bằng ngôn ngữ của skill để TISA BOT chọn đúng phần. Không chắc là nạp cả skill như cũ, và skill dạng quy trình liền mạch luôn nạp đủ.
- **Học từ cách dùng.** Phần nào model hay phải lấy thêm thì lần sau TISA BOT nạp sẵn. Bật thử cho khoảng 10% phiên chat trước, tắt theo mức Tắt.
- **Nhắn thêm trong team là cộng sự đọc ngay.** Cộng sự đang soạn câu trả lời cho tin trước thì dừng lại và trả lời gộp cả hai tin, tin mới nhất được ưu tiên. Không còn cảnh phải chờ trả lời xong câu trên mới đọc câu dưới.
- **Phó nhóm đang làm một bước việc cũng đọc tin mới ở bước kế tiếp,** nên đổi được cách làm ngay giữa chừng. Dòng trạng thái ghi rõ "Đã đọc giữa chừng".
- **Thẻ xin duyệt đã trả lời thì thông báo tự tắt.** Bấm Duyệt, Sửa, Từ chối, hay Trả lời hỏi lại trên thẻ, thông báo của nó trong chuông chuyển thành đã đọc. Yêu cầu hết hạn hay bị huỷ cũng vậy.
- **Phó nhóm nổi bật trong cài đặt team:** đứng ngay dưới chủ nhóm, có nền màu, viền nhấn và huy hiệu ngôi sao.
- **Lượt dài tốn ít token hơn, với mọi bộ não.** Model gọi lại đúng công cụ với đúng tham số mà kết quả y hệt lần trước thì nhận một dòng tham chiếu thay vì cả khối chữ lần nữa. Công cụ vẫn chạy lại thật, nên dữ liệu đổi là model nhận bản mới đầy đủ. Với Claude Code và Codex, việc này làm ở cổng hub, và TISA BOT quên sổ của lượt đó mỗi khi chúng nén hội thoại.
- **JSON gọn hơn.** Kết quả JSON thụt lề hay có chữ Việt bị mã hoá được viết gọn lại, cùng nội dung. Tệp, terminal, trang web và skill thì giữ nguyên từng ký tự.
- Chọn mức **Tắt** trên trang Mức dùng là tắt luôn hai cách tiết kiệm này. Số ký tự bớt được hiện chung ở dòng kết quả tool trên trang đó.
- **Nút tới tin được tag giờ nằm ở góc trên.** Nút tròn có mũi tên hướng lên, dưới là @ kèm số tin đang chờ, giống Zalo, vì tin được tag thường nằm phía trên. Nút hiện hay ẩn không làm xô lệch tin đang đọc.
- **Thông báo lượt chạy lâu không còn bị nuốt khi bạn đang ở hội thoại khác.** Trước đây cứ mở TISA BOT là im, nay chỉ im khi màn hình đang hiện đúng hội thoại đó.
- **Thẻ Xin duyệt gọn hơn.** Hạn duyệt hiện "còn 5 giờ" ở đầu thẻ cạnh nhãn "Chờ bạn"; bằng chứng và lời gọi thu vào một
- **Lời nhắc "Thêm TISA BOT vào Màn hình chính" không bung ngay lúc vừa đăng nhập nữa.** Trước đây nó hiện 12 giây sau khi
- **Tab cài đặt của team gọn hẳn và tự lưu.** Bỏ mục Nâng cao (nghiệm thu, mức dùng, các con số giới hạn, quyền chi tiết
- **Tin hết lượt không còn nút "Mở giới hạn của team"**, vì không còn con số nào để mở; nút Thử lại vẫn còn.
- **Team không còn giới hạn số lần trả lời mỗi ngày.** Trước đây một team dùng hết 100 lần trả lời trong ngày thì mọi
- **Việc của team chạy song song.** Mọi việc giao cho team bắt đầu ngay, kể cả việc giao chung cho cả team (trước đây việc chung phải chờ nhau vì cùng tính là của phó nhóm).
- **Chỉ chờ khi cần kết quả của người khác:** các phần trong một việc có thứ tự trước sau vẫn chờ nhau, và việc anh viết kiểu "sau khi … xong", "lần lượt" vẫn chờ việc trước nó. Mỗi cộng sự làm lần lượt các phần được giao, đúng thứ tự giao.
- **Bỏ giới hạn số việc mỗi team (trước là 3) và số team làm việc cùng lúc (trước là 4).** Một bước chờ cộng sự đang bận ở việc khác trong cùng team giờ cứ chờ tới lượt, không còn bị báo dừng "bận quá lâu".
- **Việc của team gọn thành một viên thuốc ngay trên khung nhập,** giống việc nền ở chat chính. Bấm vào mới mở chi tiết: lý do dừng, nút xử lý, ai đang làm.
- **Việc chờ bạn tự ẩn khỏi viên thuốc khi bạn đã nhắn trong khung chat sau lúc nó dừng.** Việc vẫn còn ở tab Việc cho tới khi xử lý xong.
- **Đổi tên vai trong team:** bạn, người tạo team, là Trưởng nhóm; cộng sự dẫn team là Phó nhóm (trước là "Điều phối"). Nhãn vai luôn nằm trên một dòng, và "Chia việc", "Làm" ở từng bước thành tag gọn.
- **Tab Việc đứng đầu ngăn bên** (Việc, Thông tin, Team). Mở team đang có việc thì vào thẳng tab Việc, chưa có việc thì vào tab Thông tin.
- **Cập nhật xong, việc đang dở tự chạy tiếp.** Việc team bị cắt giữa chừng tự làm tiếp đúng bước đang dở, câu team đang trả lời tự trả lời lại; không còn phải bấm "Làm tiếp" hay "Thử lại".
- **Câu chat đang trả lời dở cũng được trả lời lại** khi trang mở lại sau khi máy chủ khởi động, cho cả chat chính lẫn chat với cộng sự.
- **Việc nền quay lại hàng đợi ngay** thay vì chờ 90 giây, và lần bị cắt không còn bị tính là một lần thử hỏng.
- **Không làm trùng việc ra ngoài.** Bước nào đã kịp gửi tin, đăng bài hay tạo đơn trước khi máy chủ dừng thì TISA BOT dừng lại báo bạn, không tự làm lại. Lượt workflow bị cắt không còn treo "đang chạy" mãi.
- **Tab Việc của team làm lại theo kiểu trang Nhiệm vụ.** Mỗi việc là một thẻ, ngay dưới là từng thành viên đang làm gì: xong, đang làm hay chờ lượt, kèm lời giao. Việc đang chờ bạn đứng trên cùng.
- **Nút chữ đổi thành icon.** Sửa yêu cầu, nghiệm thu, huỷ, ưu tiên và cất vào Lưu trữ đều là icon; chỉ còn một nút có chữ cho việc đang chờ bạn. Ba tab Thông tin, Việc, Team có icon, tab Việc kèm số việc đang mở.
- **Bấm một việc đã hoàn thành để xem tóm tắt:** xong lúc nào, kết quả, ai đã làm gì. Việc đã hoàn thành và Lưu trữ đều lật trang, 5 việc một trang.
- **Lưu trữ không còn bị cắt ở 30 việc** và có ô tìm khi dài hơn một trang. Nút "Xoá tất cả" đứng riêng ở cuối.
- Thanh chọn dự án và danh sách dự án có chấm đỏ khi dự án khác có câu trả lời chưa đọc. Dự án đang xem chỉ báo trên từng cuộc chat, tránh báo trùng.
- Mở dự án vẫn giữ dấu chưa đọc cho đến khi mở đúng cuộc chat. Dấu báo cập nhật khi có câu trả lời mới hoặc khi đọc ở tab khác.
### Thêm mới
- **Bộ đo trước và sau** cho người phát triển: `tools/token_bench.py` đo số ký tự mỗi lượt gửi cho model, `tools/quality_eval.py` chạy một bộ câu hỏi qua TISA BOT thật rồi so độ đủ ý của câu trả lời giữa hai lần chạy.
- **Nút @ trong khung chat nhóm.** Khi trợ lý tag bạn mà tin đã trôi khỏi màn hình, góc dưới bên phải hiện nút tròn có chữ @ và số tin đang chờ. Bấm là cuộn tới đúng tin đó, bấm tiếp tới tin sau; đọc hết hay bạn đã trả lời thì nút tự ẩn.
- **Tab Team hiện model của từng thành viên.** Dưới tên mỗi trợ lý có dòng engine và model nó đang chạy, ghi rõ "Model chính" khi trợ lý chưa chọn model riêng, để dễ kiểm soát cả nhóm.
- **Giao việc nền kèm điều kiện hoàn thành cố định.** Việc do script hay quy trình giao mỗi ngày giữ nguyên lời giao và được chấm đúng theo các điều kiện đó, không còn hôm đạt hôm kẹt.
- **Báo mỗi câu trả lời khi bạn không xem hội thoại đó.** Bật ô mới trong phần Thông báo đẩy của chuông: TISA BOT trả lời xong là điện thoại kêu, nếu bạn đã chuyển sang app khác hoặc đang mở một hội thoại khác. Đang xem đúng hội thoại đó thì im. Bấm thông báo là mở thẳng hội thoại.
- **Trả lời được thẻ Xin duyệt trong chat team.** Thẻ còn hai nút lớn có icon: Duyệt và Trả lời. Trả lời mở một khung ngay
### Sửa lỗi
- **Tab Thông tin của team không còn "Đang tải..." mãi.** Team mở ở tab Việc rồi bấm sang Thông tin thì giờ hiện ngay ảnh, tài liệu và link của team.
- **Khoá màn hình rồi mở lại vẫn thấy câu trả lời.** Hỏi trên điện thoại, khoá máy, lúc mở lại TISA BOT tự kéo câu trả lời đã xong trong lúc vắng mặt, không phải hỏi lại hay treo màn hình chờ.
- **App trên màn hình chính bị tắt hẳn rồi mở lại cũng đủ câu trả lời.** Trước đây khung chat chỉ hiện bản lưu cũ trên máy, phải vào Lịch sử bấm lại mới thấy.
- **Việc nền trả lời `[SILENT]` thì xong lặng lẽ**, như nhắc hẹn: không còn tin "không có gì" mỗi lần chạy, cũng không bị máy tự kiểm chấm trượt.
- **Sửa lịch đổi được mức quyền, nơi nhận kết quả và giọng đọc.** Trước đây TISA BOT báo "Đã sửa" mà lịch vẫn giữ mức cũ.
- **Wikilink tên ngắn như `[[log]]` mở được** cả khi brain có nhiều file nhắc tới chữ đó. Team cần duyệt chạy ChatGPT trên Docker bị từ chối thì câu báo chỉ luôn cách bật sandbox.
- **Danh sách skill khi gõ / trong Team không còn chồng chữ.** Mỗi skill một dòng tên, một dòng mô tả, tên dài được cắt bằng dấu ba chấm, danh sách cuộn khi dài.
- **Thanh "Đang xem tin của việc" gọn còn một dòng** trên điện thoại: tên việc, một icon mở nghiệm thu và mức dùng, một dấu X để xem lại mọi tin. Trước đây nó chiếm ba dòng và đẩy khung chat xuống.
- **Bấm tên việc hay "Mở tab Việc" trong khung chi tiết của viên thuốc giờ mở đúng thứ đó,** trước đây khung chỉ đóng lại.
- **Việc bạn đã trả lời không hiện lại trên viên thuốc** khi bạn đang xem tin của một việc khác. Việc chưa có tin nào thì khung chat nói đúng như vậy.
- **Câu gợi ý trả lời không còn đè lên dòng "đang gõ"** khi dòng đó hiện ra phía trên ô nhập, ở cả trang Team lẫn chat chính.
- **Playwright không còn báo "chưa cài trình duyệt" sau khi TISA BOT vừa tải xong.** TISA BOT giờ chỉ thẳng cho Playwright file trình duyệt nó đã tải, nên hai bên lệch phiên bản cũng chạy được. Ai đã tự chọn trình duyệt riêng thì TISA BOT giữ nguyên.
- **Ảnh chụp màn hình của Playwright hiện ngay trong khung chat.** Trước đây khi TISA BOT chụp màn hình một trang bằng Playwright, ảnh bị đổi thành một chuỗi ký tự dài gửi cho model, nên bạn không thấy gì trong khung chat. Giờ ảnh được lưu vào bộ não ở `attachments/tool-images/` và TISA BOT nhúng nó vào câu trả lời để bạn xem trước. Ảnh do công cụ khác trả về (biểu đồ, thiết kế) cũng được xử lý giống vậy.

## [0.574.40] - 2026-11-19
### Thêm mới
- **Bộ TISA:** Kho tư liệu nối Google Drive: nối một lần (có nút kết nối tự động), chọn thư mục Drive làm việc để chép tư liệu về kho và thư mục Drive nhận kết quả để đội tải kết quả lên; chạy cả trên Windows. Trang Quản lý web: thẻ web mẫu hiện đúng tên miền, tên web và SEO (tiêu đề, mô tả, ảnh chia sẻ) lấy từ web thật, tự cập nhật khi đổi tên miền; thẻ Web CRM có nút Đổi đăng nhập (email, tên, mật khẩu) cho người quên mật khẩu; mọi nút hỗ trợ giao cho cộng sự Quản Trị WEB.

## [0.574.39] - 2026-11-19
### Thêm mới
- **Bộ TISA:** Thêm cộng sự Quản Trị WEB: quản lý các trang web trong hệ thống, dựng web mới theo nhu cầu (landing page bán hàng, trang lead, web CRM), phân tích web mẫu để làm theo, đưa web lên Cloudflare và gắn tên miền. Kèm sổ tay tra cứu và công cụ kiểm tra web.

## [0.574.38] - 2026-11-19
### Thêm mới
- **Bộ TISA:** Sửa lỗi nối Fanpage ở hộp Kết nối Meta: nút Đăng nhập Facebook không còn bị khóa khi mở TISA BOT bằng http mà máy đã bật Truy cập từ xa; hai ô quyền thêm (Nối cả Instagram, Đọc số liệu bài viết) để trống sẵn để tránh lỗi Invalid Scopes; nút tự mở lại sau 45 giây nếu Facebook báo lỗi. Đạt Đấu Nối được bổ sung kiến thức nối Meta đúng quy trình.

## [0.574.37] - 2026-11-19
### Thêm mới
- **Bộ TISA:** Tắt mặc định việc Chưng cất kiến thức đêm tự chạy lúc 0 giờ mỗi đêm (tốn token, gói 20 đô không đủ). Chỉ chạy khi người dùng yêu cầu; muốn bật lại tự động thì đặt CHUNG_CAT=1.

## [0.574.36] - 2026-11-19
### Thêm mới
- **Bộ TISA:** Nút × ẩn dòng việc đang chạy ngầm trên ô chat: việc vẫn chạy, có việc mới thì dòng hiện lại

## [0.574.35] - 2026-11-19
### Thêm mới
- **Bộ TISA:** Ảnh chụp màn hình xem được trên điện thoại (trước đó báo ảnh hết hạn).
- **Bộ TISA:** Lối vào "Nhập mật khẩu máy tính" ngay ở trang Cài đặt.
- **Bộ TISA:** Sửa bố cục điện thoại: khung Điều khiển của AI hết đè chữ, bảng trong chat thành thẻ, menu +, Quảng Cáo (tab, số, bảng Chiến dịch ghim cột tên), Đội Quân (ô tìm, Cài đặt đội, về đầu trang khi đổi trang).

## [0.574.34] - 2026-11-19
### Thêm mới
- **Bộ TISA:** Mở khóa máy: có ô nhập mật khẩu ở Điều khiển của AI → Máy tính, kiểm đúng mật khẩu với máy, chờ máy mở tới 15 giây, ô chat nào cũng nhắn được "mở khóa máy"; nút Quên mật khẩu ở màn đăng nhập gửi mã 6 số về Zalo admin.

## [0.574.33] - 2026-11-19
### Thêm mới
- **Bộ TISA:** Đại Quảng Cáo thành chuyên gia quảng cáo Facebook, TikTok, Google: đọc bộ não hiểu sản phẩm, chiến lược, content, target, thiết lập đúng chuẩn từng nền tảng; sổ tay quảng cáo; mọi việc quảng cáo giao cho Đại

## [0.574.32] - 2026-11-19
### Thêm mới
- **Bộ TISA:** Giao việc nối công cụ tự bật Toàn quyền 2 giờ, Đạt Đấu Nối dùng mọi cách để thao tác (không xóa tệp, vẫn dừng ở mật khẩu, OTP, CAPTCHA, thanh toán)

## [0.574.31] - 2026-11-19
### Thêm mới
- **Bộ TISA:** Cộng sự Đạt Đấu Nối lo mọi việc nối MCP và API, Cloudflare, đưa web lên mạng; chọn mô hình và mức nỗ lực; cửa sổ hỗ trợ rộng hơn và gửi được hình

## [0.574.30] - 2026-11-19
### Thêm mới
- **Bộ TISA:** Cửa sổ nổi hỗ trợ rộng hơn, gửi được hình (dán, kéo thả, nút 📎), vùng tin nhắn cuộn chung

## [0.574.29] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Mục Team chuyển vào nhóm Đội Quân AI, nằm trên Cần anh

## [0.574.28] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Trang Quảng Cáo, tab Kết nối: khung 'Đang dùng' của thẻ nền tảng gọn lại. Mỗi kết nối một dòng (chấm màu, tên, nguồn, nút nhỏ); cái đang chạy hiện sẵn, cái chưa chạy hoặc đang tắt gộp vào mục 'Cách nối khác chưa chạy' bấm mới mở; các dòng trùng tên gộp thành một dòng ghi số lượng. Thẻ Facebook ngắn đi hơn một nửa.

## [0.574.27] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Sửa lỗi nói 'Khoan' giữa cuộc gọi làm cuộc gọi ChatGPT Live bị ngắt (báo Invalid value: response.cancel): kênh của ChatGPT Live không nhận lệnh huỷ nói, nên TISA BOT chỉ tắt tiếng và xả hàng phát ở phía trình duyệt, không gửi lệnh đó nữa.
- **Bộ TISA:** Chọn Chrome hồ sơ xong là TISA BOT LÀM NGAY, không chỉ ghi nhớ: mở đúng hồ sơ Chrome, chuyển sang 'Chrome của anh' thay vì trình duyệt riêng của TISA, bỏ tab đang làm ở hồ sơ khác và mở tab mới trong đúng hồ sơ. TISA BOT chỉ thao tác tab do nó mở trong hồ sơ đã chọn, tab không rõ hồ sơ bị chặn (SAI_HO_SO). Đã chọn Chrome thật thì không còn nhảy sang trình duyệt riêng của TISA (TK QC FB...).
- **Bộ TISA:** Anh nói 'mở Google Chrome hồ sơ X': một lệnh op=mo_chrome ho_so=X tự tìm đúng hồ sơ (kể cả đúng chữ menu hồ sơ của Chrome như Sang (TIÊU SANG QUẢNG CÁO), không phân biệt hoa thường và dấu), mở, chọn tab, cấp Toàn quyền 2 giờ sau khi anh duyệt.
- **Bộ TISA:** MCP của Claude Code nối vào TISA BOT mặc định: anh đã kết nối Meta Ads (Facebook Ads) hay MCP nào bên Claude Code thì TISA BOT tự dùng luôn để báo cáo, xem số liệu, lên chiến dịch, tắt bật chiến dịch, không phải kết nối lại bằng API hay MCP trong TISA BOT. Trang Kết nối có thẻ báo 'Đã nối MCP của Claude Code vào TISA BOT' kèm từng kết nối (xanh đã nối, cam cần đăng nhập lại, đỏ lỗi), nút Kiểm tra lại và nút thử liệt kê tài khoản quảng cáo. Chỉ engine Claude dùng được; BẬT chiến dịch hay tăng ngân sách vẫn phải hỏi anh trước.
- **Bộ TISA:** Trang Quảng Cáo, tab Kết nối: thẻ Facebook / Meta nhận ra MCP Meta Ads đã nối bên Claude Code, hiện 'Đã nối đầy đủ', có dòng 'MCP của Claude Code: đã nối', Bật tắt đổi tiền và Lên chiến dịch mới đều ✅ qua MCP đó (AI hỏi anh trước khi bật hoặc đổi tiền), kèm nút Kiểm tra lại. Hết cảnh báo 'Có kết nối nhưng chưa chạy' khi MCP của Claude Code đã chạy.

## [0.574.26] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Trang TISA BOT bớt đứng hình: hàm lọc danh sách id nhóm của Chatbot chạy chậm theo bình phương khi một bot có hàng nghìn id bị chặn, làm máy chủ đứng 1 đến 2 giây mỗi lần liệt kê, mọi trang khác phải chờ. Đã sửa, kết quả giữ nguyên.
- **Bộ TISA:** TISA BOT có CON CHUỘT RIÊNG (macOS): nó thao tác thẳng vào cửa sổ cần làm, không kéo con trỏ thật và không giành bàn phím của anh, nên anh vẫn làm việc ở ứng dụng khác. Con trỏ của TISA BOT là mũi tên cam, kèm viền cam nhẹ quanh màn hình khi nó đang thao tác. Nút bấm được bấm bằng Trợ năng nên chạy cả khi cửa sổ nằm sau. Ứng dụng nào chỉ nhận chuột khi ở trước thì bảo AI chuyển chế độ chuột thật.
- **Bộ TISA:** TISA BOT nhìn màn hình và thao tác NHANH hơn: chụp màn hình khoảng 0,1 giây thay vì 0,34 giây, ảnh nhỏ hơn để AI đọc nhanh hơn; mỗi lệnh bấm, gõ, nhấn phím, cuộn, kéo tự kèm ảnh mới (không cần gọi thêm lệnh chụp); nhiều thao tác liền nhau chạy trong MỘT lệnh. Chụp riêng một cửa sổ kể cả khi bị che.
- **Bộ TISA:** Anh mở tab khác lên hoặc cửa sổ khác che mất thì TISA BOT vẫn thao tác đúng tab và cửa sổ của nó: tab trình duyệt của AI luôn được coi là đang xem (bấm, gõ, chụp vẫn chạy khi tab đang ở sau), chuyển tab của AI không còn lật tab anh đang xem (muốn xem mới dùng hien=true), tab mới mở ở nền; cửa sổ ứng dụng bị che vẫn chụp và bấm được bằng ung_dung=<tên hoặc tiêu đề cửa sổ>.
- **Bộ TISA:** Cửa sổ trợ lý nổi không còn tự mất khi anh qua trang khác hoặc tải lại trang lúc đang trao đổi (nhớ trạng thái, chỉ tắt khi anh bấm ✕); ở trang Trò chuyện nó thu thành nút nhỏ ở góc thay vì biến mất.
- **Bộ TISA:** Chọn đúng Chrome để TISA BOT kết nối giúp: hộp chọn hồ sơ Chrome (tên và email tài khoản) hiện trước khi nhờ TISA BOT làm giúp nếu anh chưa chọn, và nút Đổi ngay trong cửa sổ trợ lý nổi. TISA BOT chỉ mở và làm việc trong đúng hồ sơ đã chọn, không mở Chrome mới.
- **Bộ TISA:** Con chuột riêng cũng có trên WINDOWS (không riêng Mac): gửi tin nhắn cửa sổ thẳng vào đúng cửa sổ nên chuột và bàn phím thật của anh không bị động; nút Win32 bấm bằng BM_CLICK, gõ chữ bằng WM_CHAR (tiếng Việt giữ dấu), chụp riêng cửa sổ bị che bằng PrintWindow; mũi tên cam và viền cam nhẹ vẽ bằng PowerShell. Phần Windows chưa kiểm trên máy Windows thật, lỗi thì tự quay về chuột thật.

## [0.574.25] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Khung chat nổi (TISA BOT hỗ trợ) hiện lại đủ: tin anh vừa gõ kèm trạng thái đã gửi, và lời trả lời của AI trong cuộc gọi. Trước đây khung nổi bỏ qua lời trả lời của cuộc gọi nên anh gõ gì cũng thấy không phản hồi dù AI đã trả lời.

## [0.574.24] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Chuyển máy: gói xuất ra không còn làm máy nhận giành tên miền hay bảng giao việc của máy gốc. Trong gói, đường hầm Cloudflare đã tắt sẵn và các dòng nối bảng giao việc Đội Quân trên Cloudflare được chú thích sẵn; máy gốc không bị sửa gì. Chuyển chính thức mới bật lại.
- **Bộ TISA:** Trang Chuyển máy chủ có thanh trên cùng cho biết đang mở đúng máy nào (xanh: local, đỏ: qua tên miền). Nhận file, Áp dụng, Khôi phục qua tên miền bị chặn trừ khi tick xác nhận máy, để không thao tác nhầm lên máy cũ.
- **Bộ TISA:** Hướng dẫn máy mới viết lại rõ từng bước: cài TISA BOT trắng, chạy local, mở bằng localhost trên chính máy mới, nhận file ở đó.
- **Bộ TISA:** Sửa lỗi gõ ở khung chat nổi (TISA BOT hỗ trợ) mà bot không nhận, không phản hồi: đang gọi điện mà có lượt chạy thì tin gõ bị xếp hàng chờ lượt xong và nút Gửi bị khoá. Nay tin gõ luôn đi thẳng vào lượt đang chạy, chỉ lời nói từ mic mới xếp hàng như cũ.

## [0.574.23] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Trang Quảng Cáo gọn lại còn 4 tab: Tổng quan, Chiến dịch, Tạo quảng cáo, Kết nối. Gợi ý tối ưu gộp vào Tổng quan thành mục Việc nên làm (3 việc quan trọng nhất) và Chia lại tiền thu gọn sẵn. Thanh trên chỉ còn giờ cập nhật và một nút Cập nhật số.
- **Bộ TISA:** Tab Kết nối: mỗi nền tảng Facebook, TikTok, Google một thẻ, ghi rõ AI đã xem số, bật tắt, lên chiến dịch được chưa, kèm nút Nhờ AI kết nối và Tôi đã có mã. Ô ROAS đổi thành Mỗi 1đ quảng cáo mong thu về cho dễ hiểu.
- **Bộ TISA:** Bảng Chiến dịch: cột Ngân sách hiện tiền đặt ở cấp nhóm thay vì 0 đ, thêm cột Đánh giá có đèn màu, nút ít dùng gom vào menu ⋯. Hai con số chi mỗi ngày ghi rõ cái nào tính cả chiến dịch đã dừng.
- **Bộ TISA:** Tạo quảng cáo còn 2 cách (Nhờ AI làm, Tự chọn từng bước) và 2 nút lên chiến dịch: ⚡ AI lên tự động (qua API/MCP) và 🌐 AI bấm trên trình duyệt. Phía trên có khung báo API, MCP, trình duyệt đã sẵn sàng chưa, nút Kiểm tra lại. Kết nối chỉ đọc được báo đúng là chỉ xem số, không tưởng là tạo được chiến dịch.

## [0.574.22] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Tên ô chat tự tóm tắt từ nội dung cuộc hội thoại. Trước đây tên chỉ là mấy chữ đầu của tin nhắn đầu nên danh sách có nhiều ô cùng tên kiểu Dùng skill dq-ho-tro-ket-noi hay Alo em ơi, không biết đã trao đổi gì. Giờ sau lượt trả lời đầu AI đặt một tên ngắn (tối đa 7 từ) nói rõ chủ đề, và cập nhật lại khi cuộc trò chuyện dài ra (mốc 8 và 24 tin nhắn) để tên đúng hơn.
- **Bộ TISA:** Tên anh tự đặt không bao giờ bị đè. Lần đầu sau khi cập nhật, 20 ô chat gần nhất đang mang tên máy đặt được đặt lại tên một lần. AI chưa sẵn sàng thì giữ tên cũ và thử lại sau.
- **Bộ TISA:** Bỏ nút Xem bản minh họa dựng sẵn ở khung Giao việc của bảng Đội Quân AI.

## [0.574.21] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Trang Đội ngũ, phần Luồng chuẩn của một chiến dịch: viết lại cho dễ hiểu. Mỗi bước nay ghi việc gì (chức danh), AI nào làm, NHẬN gì từ bước trước, GIAO ra gì và chuyển cho ai; bước có hai người ghi rõ làm cùng lúc, không chờ nhau; nhóm cộng sự thêm vào ghi là Đội mở rộng. Có đoạn giải thích ngắn ngay dưới tiêu đề.
- **Bộ TISA:** Cài đặt đội: mọi nhân sự có cùng một bộ điều khiển: công tắc bật tắt, tên, chức danh, phòng và nút Chi tiết (việc làm và giọng nói). Trước đây nhân sự có sẵn thiếu nút Chi tiết còn cộng sự tự thêm thiếu công tắc. Sửa việc làm của nhân sự có sẵn được lưu và đồng bộ sang hồ sơ cộng sự bên TISA BOT. Nút xóa chỉ có ở cộng sự tự thêm (nhân sự có sẵn tắt bằng công tắc).
- **Bộ TISA:** Thẻ thông báo nổi (AI đang chờ anh, AI xin duyệt) có nút × để tắt cho gọn. Tắt rồi không hiện lại thông báo đó, kể cả sau khi tải lại trang; việc vẫn nằm trong chuông Thông báo.

## [0.574.20] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Cài lần đầu tự bật quyền điều khiển máy: khi TISA BOT mở lần đầu trên macOS, nó tự hiện hộp xin quyền Trợ năng và Ghi màn hình, chạm vào Màn hình nền, Tài liệu, Tải xuống và hỏi Tự động hóa System Events, Chrome để macOS hiện hộp xin quyền đúng lúc, mở sẵn đúng trang Cài đặt, chép sẵn đường dẫn chương trình để dán, rồi đợi người dùng bật xong và báo lại. macOS không cho phần mềm tự bật quyền cho chính nó nên người dùng vẫn phải bấm công tắc. Windows gần như không cần cấp quyền.
- **Bộ TISA:** Khi AI gặp thiếu quyền (không xem được màn hình, không bấm được) nó không còn dừng ở câu em chưa làm được: nó hiện hộp xin quyền, mở trang Cài đặt và hướng dẫn từng bước thật cụ thể (bấm đâu, chữ nào trên màn hình) cho Mac và Windows, đợi người dùng xong rồi làm tiếp việc đã giao. Có thêm lệnh huong_dan_quyen và trang /may-ai/cai-quyen.
- **Bộ TISA:** Giới hạn giữ nguyên dù đã bật hết quyền: không xóa tệp của người dùng; không bấm bước tốn tiền (thanh toán, mua, nạp, nâng gói), nay cả khi bấm bằng chuột trên cửa sổ có tiêu đề thanh toán; không tự vượt mật khẩu, OTP, CAPTCHA, Touch ID.

## [0.574.19] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Mở khóa máy chắc hơn: đánh thức màn hình bằng nhích chuột rồi chờ tới khi thấy ô mật khẩu mới gõ (trước đây gõ vội nên phím có thể bị nuốt), gõ mật khẩu bằng bàn phím ABC để Telex không biến chữ rồi trả lại bộ gõ cũ, phím gõ ra từ nguồn phần cứng và gõ chậm hơn. Nhật ký mỗi lần ghi thêm bàn phím lúc trước và có đổi sang ABC không (không có mật khẩu).
- **Bộ TISA:** Lưu ý: máy ngủ hẳn thì TISA BOT cũng ngừng chạy nên không mở khóa từ xa được. Muốn mở khóa lúc tắt màn hình, bật trong Cài đặt Hệ thống mục Pin hoặc Năng lượng: ngăn máy tự ngủ khi cắm sạc và tắt màn hình.

## [0.574.18] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Chuyển máy chủ: anh tự chọn nội dung của gói. Phần NỀN TẢNG luôn có (bộ não dạng chữ, wiki, kỹ năng, kết nối MCP, khoá API và token, toàn bộ tin nhắn và lịch sử chat, mọi thiết lập, kênh, Đội Quân AI). Phần KHO NẶNG là tùy chọn, mặc định không mang: hình ảnh, video, âm thanh, dữ liệu làm dở để AI làm tiếp, tệp lớn khác. Không tick thì gói chỉ có nền tảng, nhẹ và nhanh (trước đây gói có thể lên hàng chục GB vì video).
- **Bộ TISA:** Trước khi đóng gói, trang báo dung lượng từng phần: nền tảng bao nhiêu GB, từng nhóm kho nặng bao nhiêu GB, chỗ trống trên máy này, gói sẽ nặng bao nhiêu và máy mới cần trống khoảng bao nhiêu GB. Máy không đủ chỗ thì nút Đóng gói tự khoá. Xong gói có báo phần chưa mang theo để anh chép riêng bằng USB hoặc Drive, và máy mới thấy gói này có kèm kho nặng hay không.
- **Bộ TISA:** Điều khiển máy: thêm thao tác mở khóa màn hình đăng nhập khi anh ở xa (tisa_desktop_do op=mo_khoa). Mật khẩu chỉ lấy từ Keychain của máy, không nhận qua tham số, không ghi vào tệp, nhật ký hay chat. Chỉ chạy khi chính anh nhắn từ dashboard (hoặc đúng Zalo anh khai), mỗi lần hỏi duyệt trừ khi Toàn quyền, thất bại 3 lần thì dừng 30 phút, có nhật ký từng lần và chụp màn hình kiểm sau khi vào. Click, gõ và phím thường ở màn hình khóa vẫn bị chặn.
- **Bộ TISA:** Gõ tiếng Việt qua clipboard: chữ có dấu được dán (cmd+v) thay vì gõ từng phím nên bộ gõ Telex của macOS không làm biến chữ; clipboard cũ được khôi phục sau khi dán.
- **Bộ TISA:** Chống chen ngang và khóa hồ sơ Chrome: trước khi gõ vào Chrome, TISA BOT kiểm có tiện ích hay chương trình khác đang điều khiển trình duyệt không và dừng, nói rõ nguyên nhân thay vì gõ mù. Anh chọn hồ sơ Chrome nào thì mọi lần mở trang chỉ vào hồ sơ đó (không còn tự nhảy sang hồ sơ 2, 3 chưa đăng nhập); đổi hồ sơ hay đổi trình duyệt luôn cần anh bấm Duyệt.
- **Bộ TISA:** Việc nền dài: tự giữ máy thức (caffeinate) khi có việc nền chạy và tắt khi xong; có thể cho phép tự mở khóa lại nếu máy khóa giữa chừng. Gặp bước chỉ người thật làm được (Touch ID, mã khóa, CAPTCHA, OTP) TISA BOT gửi anh một tin ngắn, tạm dừng đúng chỗ và tự làm tiếp khi anh xong.
- **Bộ TISA:** Quay và chụp màn hình theo cửa sổ hoặc vùng, lưu vào brain theo thư mục 04-ket-qua/năm-tháng/ngày-mô-tả.
- **Bộ TISA:** Google Drive bằng API (công cụ tisa_drive_do): liệt kê, đổi tên hàng loạt (xem trước, anh duyệt, có tệp hoàn tác), tạo thư mục, tải tệp lớn có tiếp tục sau khi đứt mạng và kiểm dung lượng, chia sẻ, lấy link. Khóa cất trong Keychain, không có thao tác xóa. Kỹ năng kết nối được mở rộng: tự cất khóa API vào Keychain mà giá trị không hiện ra chat.
- **Bộ TISA:** Cuộc gọi bằng giọng bớt phiền: việc nền giao từ vài câu trước xong đúng lúc anh đang nói chuyện khác thì TISA BOT không chen vào nữa. Bot chờ anh nói xong và im một chút mới báo, nêu rõ là việc nào, rút gọn vài câu và nói chi tiết đã ở khung chat. Anh nói liên tục thì bot bỏ lời báo (kết quả vẫn nằm trong khung chat).
- **Bộ TISA:** Thanh gọi có thêm nút Dừng nói (hiện khi bot đang nói): bấm là tắt tiếng ngay, bỏ hàng chờ đọc và huỷ lượt nói. Anh cũng có thể nói thẳng "em ơi dừng lại", "thôi", "đủ rồi" hoặc "stop" (câu ngắn đúng nghĩa dừng), bot dừng và không coi đó là việc giao cho bộ não. Anh nói câu mới thì bot nói lại bình thường.

## [0.574.17] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Chuyển máy làm lại theo hướng AN TOÀN: máy mới chạy CÁCH LY hoàn toàn với máy cũ trong suốt thời gian thử. Mọi thứ tự chạy được tạm dừng: đường hầm tên miền, kênh nhận tin, việc định kỳ và nhắc hẹn, việc Kanban tự chạy, Auto của cộng sự, sao lưu GitHub, nối bảng giao việc trên Cloudflare và Zalo (tránh đá tài khoản máy cũ). Mỗi lần mở lại máy mới vẫn giữ nguyên cách ly. Chỉ khi anh tick xác nhận đã dừng máy cũ và bấm chuyển chính thức, mọi thứ mới được bật lại.
- **Bộ TISA:** Chuyển được cả bốn hướng: Mac sang Windows, Windows sang Mac, Mac sang Mac, Windows sang Windows. Đường dẫn được đổi đúng kiểu cho từng loại tệp (JSON, TOML, cơ sở dữ liệu, văn bản), kể cả phần đuôi dùng dấu gạch xuôi hay ngược; kết nối MCP chạy bằng Python của TISA BOT tự đặt lại đúng chương trình của máy mới; tệp tên không hợp lệ hoặc đường dẫn quá dài trên Windows được báo thay vì làm hỏng cả gói; tập lệnh giữ quyền chạy khi giải nén.
- **Bộ TISA:** Bước kiểm tra tự động báo rõ máy đang cách ly, đã tạm dừng gì, kết nối MCP nào cần cài chương trình và tệp nào không chép được.

## [0.574.16] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Sửa chuyển máy: máy mới không còn tự nối vào đường hầm Cloudflare của máy cũ. Trước đây settings mang theo token đường hầm nên hai máy cùng trả lời một tên miền, anh thấy lúc dữ liệu máy cũ lúc dữ liệu máy mới và tưởng bị đồng bộ, mất chat. Giờ đường hầm tự TẮT ở máy mới cho tới khi anh chủ động bật.
- **Bộ TISA:** Chuyển máy từ Mac sang Windows không còn làm hỏng settings.json và mcp_servers.json: đường dẫn Windows (có dấu gạch ngược) trước đây được chèn thẳng vào tệp JSON nên tệp không đọc được và khóa API, kết nối MCP biến mất; giờ đường dẫn được viết đúng dạng cho từng loại tệp (JSON, TOML, CSDL). Máy Windows cũng tự bọc npx bằng cmd /c cho MCP của Claude Code.
- **Bộ TISA:** Chuyển máy mang thêm các kết nối MCP của Claude Code và Codex (nằm ngoài thư mục TISA BOT); máy mới chỉ thêm cái chưa có, không ghi đè, có bản dự phòng, và báo kết nối nào cần cài lại chương trình.
- **Bộ TISA:** Trang Chuyển máy: nhắc gói là ảnh chụp tại lúc đóng gói, có thêm cách dùng lại đúng đường hầm cũ (tắt ở máy cũ rồi bật ở máy mới) và bước kiểm tra báo đường hầm đang bật hay tắt.
- **Bộ TISA:** Cuộc gọi bằng giọng nói nhớ tên anh chắc hơn: ngoài lời dặn, hồ sơ còn được đưa vào đầu cuộc trò chuyện như chuyện anh vừa tự giới thiệu (tên, cách gọi, tiếng Việt), vì lời dặn đơn thuần đôi khi bị giọng nói bỏ qua.
- **Bộ TISA:** Sửa giao diện điện thoại ở chế độ tối: ngăn danh sách cộng sự, danh sách hội thoại và bảng bên phải trước đây trong suốt nên chữ của khung chat bên dưới lộ xuyên qua, chồng thành một mớ chữ; giờ nền đặc.
- **Bộ TISA:** Trang Tệp tin trên điện thoại: tên thư mục và tệp không còn bị cắt còn 4 ký tự, các nút Đổi tên / Zip / Xoá xuống dòng dưới.

## [0.574.15] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Hồ sơ của anh giờ áp dụng cho MỌI cộng sự: chat riêng, nhóm, việc Kanban và quy trình đều đọc hồ sơ nên cộng sự gọi đúng tên, xưng đúng và nói tiếng Việt ngay từ câu đầu (trước đây cộng sự không đọc hồ sơ).
- **Bộ TISA:** Cuộc gọi bằng giọng nói nói tiếng Việt chắc hơn: quy tắc xưng hô, tiếng Việt, câu chào "Dạ anh…, em nghe ạ" và cách đọc nguyên văn tiếng Việt nằm ngay đầu lời dặn, bỏ các câu cũ cãi lại hồ sơ nên bot không còn chào "bạn, tôi nghe đây" hay chuyển sang tiếng Anh.
- **Bộ TISA:** Hồ sơ đã lưu từ bản cũ tự được dựng lại theo chữ mới khi mở máy, không cần bấm Lưu lại.

## [0.574.14] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Giao diện điện thoại gọn và dễ bấm hơn: cửa sổ trợ lý nổi, trang Quảng Cáo (thanh tab cuộn ngang một hàng), Hồ sơ của anh và Quản lý web có nút đủ lớn cho ngón tay, ô nhập không làm iPhone tự phóng to, thanh Lưu chừa chỗ vạch Home.
- **Bộ TISA:** Sửa lỗi AI gửi đường dẫn video mà bấm không xem được: video, ảnh, tệp AI nhắc trong chữ (kể cả chỉ ghi tên tệp) giờ hiện thẻ xem ngay dưới tin, bấm vào chính tên tệp cũng mở trình xem, và mở đúng bộ não đang dùng (trước đây chỉ tìm ở bộ não mặc định).
- **Bộ TISA:** Rà lại giao diện máy tính: nút Trình duyệt ở ô chat tự thu gọn thành biểu tượng khi hàng nút hẹp (không còn đè lên nút Effort và mic ở Hỏi chuyên gia); thanh bên tự cuộn tới mục đang chọn (mục Quản lý web không còn lấp sau nút Hệ thống).

## [0.574.13] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Sửa lỗi đã cấp Toàn quyền mà AI vẫn báo không làm được vì bị khóa do lần bấm Dừng trước: cấp Toàn quyền thì tự bỏ khóa. Cửa sổ trợ lý hiện thẻ Anh đã bấm Dừng kèm nút Cho AI làm tiếp; anh nhắn tin hay nói làm tiếp thì AI cũng được làm tiếp.

## [0.574.12] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Cửa sổ trợ lý nổi gọn lại: ba nút Gọi, Khung chat, Dừng AI nằm đều trên một hàng.
- **Bộ TISA:** Trang Quản lý web: hai web mẫu (Web CRM, Lead Page & Sale Page) có thêm nút Kết nối tự động. Bấm là TISA BOT tự đưa web lên Cloudflare, có cửa sổ chat và gọi điện hướng dẫn từng bước ở góc màn hình.

## [0.574.11] - 2026-11-18
### Thêm mới
- **Bộ TISA:** Gọi điện với TISA BOT nhanh hơn: máy tự làm nóng đường gọi ChatGPT Live ngay khi mở trang, nên bấm gọi là kết nối luôn, không còn phải đợi khởi động. Mỗi cuộc gọi cũng được ghi lại thời gian từng chặng (không ghi nội dung cuộc nói) để lần sau chậm là biết chậm ở đâu.
- **Bộ TISA:** Sửa lỗi Tắt mic mà vẫn nghe: khi cuộc gọi nghỉ vì im lặng, bộ nghe câu đánh thức không còn tự nghe và nối lại cuộc gọi nếu mic đang tắt; mở lại cuộc gọi vẫn giữ mic tắt. Bật mic lại thì cuộc gọi nối lại ngay.
- **Bộ TISA:** Hết hai giọng chồng nhau: khi đang gọi, kết quả việc chạy nền chỉ do chính giọng của cuộc gọi đọc, không còn giọng đọc khác chen vào. Nút Dừng hiện khi TISA BOT đang nói trong cuộc gọi, bấm là tắt tiếng và bỏ các kết quả đang chờ đọc.
- **Bộ TISA:** Kết nối tự động có giọng hướng dẫn duy nhất: bấm Gọi trong cửa sổ trợ lý thì TISA BOT biết ngay việc đang làm, đọc to lời báo tiến độ, việc anh cần làm và việc xin anh duyệt bằng cùng một giọng, không còn hai giọng khác nhau. Anh nói "xong rồi" thì phần đang làm tiếp tục ngay, không cần bấm nút.

## [0.574.10] - 2026-11-17
### Thêm mới
- **Bộ TISA:** Thẻ Cập nhật chỉ hiện tên V (ví dụ Có bản mới V3.03), không còn hiện số kỹ thuật dài; bản mới vừa phát mà chưa tra được tên thì chỉ ghi Có bản mới.
- **Bộ TISA:** Sửa lỗi AI báo thiếu công cụ dù anh đã cấp Toàn quyền: AI trước đây đi tìm công cụ điều khiển trình duyệt và máy ở chỗ không có (rồi dùng trình duyệt tự động riêng báo bận). Nay lời dặn của TISA BOT chỉ rõ công cụ nằm ở đâu và cấm kết luận thiếu công cụ hay thiếu quyền khi chưa tìm đúng chỗ.
- **Bộ TISA:** Nút ghi âm: trang Quảng Cáo, Hồ sơ, Quản lý web mở được micro (trước đây khung chứa trang thiếu quyền), micro không còn thu ra im lặng khi một cuộc gọi đang giữ micro. Khi không ra chữ, TISA BOT nói đúng lý do: micro không thu được tiếng, hoặc có tiếng nhưng chưa nhận ra chữ.
- **Bộ TISA:** Khi nhờ TISA BOT hỗ trợ cài đặt, kết nối (nút Kết nối tự động, Nhờ TISA BOT làm giúp), có thêm cửa sổ trợ lý nổi ở góc màn hình, hiện trên mọi trang và hộp thoại: báo AI đang làm tới đâu, hiện thẻ Anh cần làm kèm nút Em làm xong rồi khi AI chờ anh đăng nhập hoặc bấm Cho phép, có ô chat nhỏ gọn và nút Gọi: bấm là gọi điện nói chuyện qua lại với AI y như tính năng gọi trong khung chat, nút Dừng AI ngay. Cửa sổ kéo được và thu nhỏ được.

## [0.574.9] - 2026-11-17
### Thêm mới
- **Bộ TISA:** Thêm mục Hồ sơ của anh (menu Bộ não): anh khai tên, cách bot gọi anh, cách bot xưng, ngôn ngữ, nghề và lĩnh vực, công việc, nguyên tắc, và bắt bot nghiên cứu Bộ Não Thứ 2. Mọi ô chat mới, cộng sự và cả cuộc gọi điện với bot đều biết anh là ai ngay từ câu đầu, không còn nói tiếng Anh hay hỏi "chào bạn, bạn cần gì". Có nút Tự động phân tích và điền: TISA BOT đọc Bộ Não Thứ 2 của anh, nhờ AI điền sẵn các ô, anh xem lại rồi bấm Lưu.

## [0.574.8] - 2026-11-17
### Thêm mới
- **Bộ TISA:** Bảng Điều khiển của AI, tab Trình duyệt, được sắp lại thành 3 bước dễ hiểu: 1. Chọn trình duyệt cho AI làm việc (kèm giải thích chấm xanh, nút Đưa lên trước, Đóng cửa sổ và Dừng AI ngay tách riêng cửa sổ với AI), 2. Đăng nhập tài khoản (nút Chép đăng nhập từ Chrome để lộ ra ngay), 3. Quyền của AI trên web. Thêm, đổi tên, xóa trình duyệt gập vào một mục riêng.
- **Bộ TISA:** Không còn dùng Claude để làm giúp. Mọi nút "Nhờ Claude làm giúp" (Quảng Cáo, Cách 2 triển khai quảng cáo, kết nối Meta, đưa web lên Cloudflare, bảng Giao dự án) đổi thành Nhờ TISA BOT: bấm là TISA BOT sang khung chat và tự làm bằng trình duyệt và điều khiển máy của chính nó, tự bật Toàn quyền 2 giờ, riêng xóa tệp luôn bị chặn. Gặp đăng nhập, mật khẩu, mã xác thực thì TISA BOT dừng nhờ anh làm rồi làm tiếp.
- **Bộ TISA:** Cách 2 thiết lập quảng cáo: TISA BOT mở trang quản lý quảng cáo, làm theo phiếu và tải hình, video lên thẳng từ máy anh, không cần tải về hay dán lệnh. Chiến dịch vẫn tạo ở trạng thái tạm dừng.
- **Bộ TISA:** Quảng Cáo, tab Tài khoản và kết nối: sắp lại gọn đẹp thành hai thẻ cạnh nhau, bên trái là cách nhanh để TISA BOT lấy mã giúp (có nút cho Facebook, TikTok, Google), bên phải là ô dán mã nếu anh đã có.
- **Bộ TISA:** Điều khiển máy tính: AI nhìn được màn hình thật. Ảnh chụp màn hình giờ gửi thẳng cho AI xem (trước đây chỉ đưa đường dẫn tệp nên trên Windows AI không đọc được gì). Thêm lệnh phóng to một vùng để đọc chữ nhỏ, tự thu nhỏ ảnh màn hình lớn mà vẫn bấm đúng chỗ, có đường chụp dự phòng trên Windows và báo rõ khi màn hình đang khóa hoặc chụp ra ảnh đen. Trình duyệt TISA cũng gửi ảnh chụp trang thẳng cho AI.
- **Bộ TISA:** Trang Kết nối: mỗi thẻ có thêm nút Kết nối tự động. Bấm là TISA BOT tự làm từ đầu đến cuối: bật Toàn quyền (không xóa tệp), mở trình duyệt, tạo app hoặc khóa, dán kín vào ô và bấm Kết nối; chỗ nào cần anh (đăng nhập, mã xác thực, quét QR, đồng ý quyền) thì báo đúng một việc cần bấm. Có hướng dẫn chi tiết cho Meta Ads, Facebook Trang, Kết nối Meta, Cloudflare, Composio, Google (Gmail, Lịch, Drive, Analytics, Ads, Search Console...), NotebookLM, TikTok, Zalo, Botcake, GitHub, Substack, CRM.
- **Bộ TISA:** Hộp chọn web AI muốn mở: mặc định chọn trình duyệt TISA BOT đang chạy, đánh dấu trang nào đã mở sẵn tab hoặc đã đăng nhập. Trình duyệt đã có tab của đúng trang thì AI chuyển thẳng sang tab đó (khỏi hỏi, khỏi mở Chrome mới, khỏi đăng nhập lại); chưa có thì mở tab mới, không đè lên tab đang dùng.
- **Bộ TISA:** Xem hình, video trên điện thoại chỉ còn MỘT kiểu: ảnh nào trong chat, hộp thư hay kết quả cũng mở cùng khung xem toàn màn hình (trước đây ảnh không nằm trong bộ não mở khung cũ). Thanh nút to ở đáy. Bấm Lưu ảnh / Lưu video hiện bảng chọn: lưu vào thư viện Ảnh (iPhone) hoặc tải về máy (Android), gửi qua Zalo/Messenger, mở ảnh gốc, lưu cả bộ ảnh một lần, hoặc tải tất cả thành .zip.
- **Bộ TISA:** Trình duyệt AI dùng được CHÍNH Chrome anh đang mở TISA BOT (cả Edge, Brave), có sẵn mọi tài khoản anh đã đăng nhập, khỏi chép đăng nhập hay đăng nhập lại. Bật một lần: mở chrome://inspect/#remote-debugging, tích ô cho phép, bấm Nối ngay rồi bấm Allow khi Chrome hỏi. AI luôn mở tab mới để làm, không đụng tab anh đang dùng, không bao giờ đóng hay tắt Chrome của anh; mật khẩu, mã xác thực, thanh toán vẫn do anh tự làm.
- **Bộ TISA:** Bảng Điều khiển của AI gọn chữ hơn: 'AI làm việc trên trình duyệt nào?', 'Hiện cửa sổ lên', 'Chép đăng nhập từ Chrome của anh', 'Chép lại đăng nhập mới nhất', 'Thêm trình duyệt riêng', 'Đổi tên', 'Xóa trình duyệt này'.

## [0.574.7] - 2026-11-17
### Thêm mới
- **Bộ TISA:** Quảng cáo: bật, tắt, đổi ngân sách chỉ cần ra lệnh. Bỏ công tắc Cho phép ở từng tài khoản và bỏ bước gõ câu xác nhận: bấm nút Bật, Tắt trong bảng là làm ngay, hoặc nói trong chat "tắt chiến dịch Nhà Đẹp 3T" thì AI làm luôn, không bắt vào dashboard hay nhập mã.
- **Bộ TISA:** AI có thêm công cụ bật, tắt, đổi ngân sách theo tên hoặc mã chiến dịch, nhóm quảng cáo (Facebook, TikTok, Google). Vẫn đọc trạng thái thật trước, đọc lại sau khi làm, ghi nhật ký, tăng ngân sách tối đa 50% mỗi lần; tên khớp nhiều mục thì hỏi lại đúng mục nào. Chưa nối tài khoản API thì AI làm bằng công cụ ghi của MCP quảng cáo hoặc thao tác trên trang quản lý quảng cáo trong Trình duyệt TISA.
- **Bộ TISA:** Bảng Điều khiển của AI gọn lại và mở nhanh hơn: tab Trình duyệt chỉ còn chọn trình duyệt, chọn quyền một dòng, nút mở hoặc dừng; phần quản lý trình duyệt, trang đã đăng nhập, nhật ký thu vào mục bấm mới mở. Tab Máy tính cũng vậy. Bảng không còn tải danh sách đăng nhập mỗi vài giây nên không còn chậm.
- **Bộ TISA:** AI tự chuẩn bị để điều khiển được: macOS chưa cấp quyền Trợ năng hay Ghi màn hình thì TISA BOT tự mở sẵn đúng chỗ trong Cài đặt rồi chờ anh bật công tắc và tự làm tiếp; việc không tự bấm được (hộp xin quyền, mật khẩu máy, đăng nhập, mã xác thực) thì AI nói rõ một việc anh cần làm. Nút AI hỗ trợ kết nối kiểm tra quyền trước khi bắt đầu.
- **Bộ TISA:** Sửa lỗi Giao dự án: bấm Giao việc cho Tâm Tổng Quản không gửi được (báo "Chưa lưu được. Kiểm tra mạng rồi thử lại"), nhất là trên Windows. Nguyên nhân là bảng giao việc từ chối lệnh lưu vì địa chỉ nguồn không khớp; giờ lưu và giao việc bình thường.

## [0.574.6] - 2026-11-17
### Thêm mới
- **Bộ TISA:** Trình duyệt AI: nút Đưa trình duyệt lên trước nay đưa đúng cửa sổ của trình duyệt đã chọn lên trước (trước đây có thể kích hoạt nhầm Chrome cá nhân của anh nên cửa sổ không hiện), và trình duyệt mới mở cũng tự nổi lên. Trình duyệt mới mở hiện trang chủ có tên trình duyệt, các trang đã đăng nhập và lối vào nhanh.
- **Bộ TISA:** Sửa lỗi trình duyệt nhập từ Chrome mở ra màn hình chọn hồ sơ (Who's using Chrome) thay vì cửa sổ làm việc nên trông như đứng yên; đóng hết cửa sổ rồi bấm mở lại thì tự mở lại cửa sổ.
- **Bộ TISA:** Trình duyệt AI vào đúng trình duyệt anh chọn: bấm vào một trình duyệt trong bảng là AI dùng đúng trình duyệt đó (nhãn AI đang dùng), nút ở khung chat ghi tên trình duyệt AI đang dùng, và AI được dặn không bao giờ tự sang trình duyệt khác.
- **Bộ TISA:** Các nút hỗ trợ dựng web có thêm bộ thiết kế giao diện chuyên nghiệp: nút Làm đẹp giao diện (8 chủ đề màu và chữ theo ngành, hiệu ứng nhẹ, bộ biểu tượng, ảnh, điện thoại) và nút Soát chất lượng trước khi đăng (chữ mẫu còn sót, tốc độ, chia sẻ Zalo, độ dễ đọc). Các nút dựng, sửa, đưa lên mạng cũng tự soát trước khi giao.
- **Bộ TISA:** Nói chuyện bằng giọng: anh bảo dừng hoặc đổi việc giữa chừng thì việc cũ dừng thật và chỉ làm việc mới (trước đây việc cũ vẫn chạy tiếp song song). Hai giọng không còn nói chồng lên nhau khi nhận việc và khi báo kết quả.
- **Bộ TISA:** Trang Kết nối có nút AI hỗ trợ kết nối: anh gõ hoặc nói muốn nối ứng dụng nào, chọn quyền cho AI (trình duyệt web: hỏi mọi bước, hỏi bước quan trọng, toàn quyền; điều khiển máy tính: không cho, hỏi mọi bước, hỏi bước quan trọng, toàn quyền) và chọn trình duyệt ngay trong hộp, có thể thêm trình duyệt mới hoặc lấy đăng nhập từ hồ sơ Chrome tại chỗ. AI đọc hướng dẫn, hỏi anh chọn web để mở, điều khiển thẳng giao diện TISA BOT (mở thẻ kết nối, chọn ô, bấm Kết nối), lấy mã hoặc phiên đăng nhập rồi dán vào ô mà không hiện trong chat, và tự làm tiếp sau khi anh bấm Duyệt.
- **Bộ TISA:** Lưu ý: hồ sơ Chrome nhập vào thường giữ được đăng nhập Facebook, TikTok, Zalo nhưng không giữ được đăng nhập Google (Google tự hủy phiên bị chép), nên với Gmail, YouTube, NotebookLM cần đăng nhập Google một lần trong trình duyệt TISA.
- **Bộ TISA:** Sửa lỗi AI không chụp được màn hình khi TISA BOT chạy ngầm trên macOS (thiếu đường dẫn lệnh chụp màn hình), nay mọi lệnh hệ thống gọi bằng đường dẫn đầy đủ. Điều khiển máy tính có thêm mức Không cho.

## [0.574.5] - 2026-11-17
### Thêm mới
- **Bộ TISA:** Trình duyệt TISA: AI Agent tự điều khiển một cửa sổ trình duyệt riêng như người thật (nhìn trang, di chuột, bấm, gõ, cuộn, chờ, kiểm tra kết quả) cho việc không có MCP hay API như tạo Fanpage, đăng bài, lấy mã, nối công cụ. Người dùng chỉ đăng nhập một lần; mật khẩu và mã xác thực tự gõ, TISA BOT không nhận.
- **Bộ TISA:** Nút Mở trình duyệt cho AI thao tác trong dấu + của khung chat (Hỏi nhanh, Hỏi chuyên gia): mở cửa sổ, đi nhanh tới Facebook, Meta Business Suite, Google, YouTube, TikTok, Zalo OA, Canva, Pancake, xem trang đã đăng nhập, xem AI vừa làm gì, nút Dừng AI ngay.
- **Bộ TISA:** An toàn: AI không nhập mật khẩu, mã xác thực, CAPTCHA, không thanh toán, không thao tác trang ngân hàng hay ví. Đăng bài, gửi, xóa, đổi bảo mật, đăng ký luôn hiện thẻ xin duyệt, anh bấm Duyệt thì AI mới làm, mỗi lần duyệt dùng một lần. Mọi thao tác có nhật ký.
- **Bộ TISA:** Cả đội Đội Quân AI được gắn kỹ năng dùng trình duyệt với kịch bản mẫu đăng bài Fanpage, tạo Fanpage, lấy mã truy cập, tìm kiếm trong trang cần đăng nhập.
- **Bộ TISA:** Mức tự động của AI khi điều khiển trình duyệt: Hỏi mọi bước, Hỏi bước quan trọng (mặc định), Toàn quyền (30 phút, 2 giờ hoặc đến khi tắt). Thẻ xin duyệt có thêm nút Duyệt và đừng hỏi nữa. Mật khẩu, mã xác thực, CAPTCHA, thanh toán, trang ngân hàng luôn do anh làm ở mọi mức.
- **Bộ TISA:** AI tự đấu nối nền tảng vào TISA BOT giúp học viên: mở trang TISA BOT và trang nền tảng, học viên chỉ đăng nhập, AI tạo mã theo quyền tối thiểu rồi chuyển thẳng vào ô của TISA BOT (mã được che, không hiện cho AI, không vào chat), bấm Lưu và kiểm tra kết nối.
- **Bộ TISA:** Điều khiển máy tính: AI dùng chính máy anh như người thật (nhìn màn hình, di chuột, bấm, gõ, mở ứng dụng, thư mục, tệp) trên macOS (Windows đang thử nghiệm). Có 3 mức tự động riêng, nút Dừng AI ngay (hoặc đưa chuột về góc trên trái), thử chụp màn hình trong bảng. AI KHÔNG xóa tệp ở bất kỳ mức nào trừ khi anh bật công tắc Cho phép AI xóa tệp (có hạn giờ), không bấm vào cửa sổ mật khẩu, ví, ngân hàng.
- **Bộ TISA:** Nút Trình duyệt AI có ở mọi khung chat (Hỏi nhanh, từng cộng sự ở Hỏi chuyên gia, Giao dự án). Chỉ có MỘT trình duyệt dùng chung: anh đăng nhập Google, Facebook, TikTok, Facebook Ads... vào đó một lần, đóng mở lại vẫn còn; bấm nút luôn đưa đúng cửa sổ đó lên trước.
- **Bộ TISA:** Nhiều trình duyệt: tạo thêm trình duyệt có tên (Facebook Sang, Fanpage Shop A...), mỗi cái đăng nhập tài khoản riêng nên làm việc cùng lúc với 3 tài khoản Facebook được. Chọn trình duyệt nào là mặc định cho AI, hoặc nói trong chat "dùng Facebook 2". Đổi tên, xóa từng trình duyệt trong bảng.
- **Bộ TISA:** Dùng hồ sơ Chrome anh đã có: bấm Dùng hồ sơ Chrome có sẵn, chọn hồ sơ (Chrome, Edge, Brave), TISA BOT chép phần đăng nhập sang một trình duyệt riêng nên không phải đăng nhập lại Google, Facebook, TikTok. Không chép mật khẩu đã lưu, thẻ, lịch sử; Chrome gốc không bị sửa. Có nút Cập nhật đăng nhập khi anh vừa đăng nhập thêm ở Chrome.
- **Bộ TISA:** Trình duyệt mới mở không còn là trang trắng: hiện trang chủ ghi tên trình duyệt, các trang đã đăng nhập và lối vào nhanh (Facebook, Business Suite, Quảng cáo Facebook, Google, YouTube, TikTok, Zalo OA, Canva).

## [0.574.4] - 2026-11-17
### Thêm mới
- **Bộ TISA:** Kết quả công việc: việc làm tiếp nằm trong việc mở đầu (kết quả 1 → 2 → 3 hiện như mục con), có nút gập, cả chuỗi xếp theo lần làm mới nhất.
- **Bộ TISA:** Báo cáo tự động: mỗi việc báo cáo là một thẻ có nội dung cần báo, tình trạng hôm nay (đã báo lúc mấy giờ, chưa tới giờ hay trễ), nút Sửa nội dung và Tạm dừng; báo cáo gần đây gọn thành danh sách gập, lọc theo loại. Luồng chuẩn của một chiến dịch thành dòng thời gian dễ nhìn. Khung Đồng bộ từ TISA BOT gom thành các mục gập.
- **Bộ TISA:** Kho tư liệu nối vào cả đội: mọi nhân sự Đội Quân AI nay được dặn xem Kho trước khi thiết kế, dựng, đăng bài (kỹ năng mới Dùng Kho tư liệu của chủ), dùng tệp gốc và ghi rõ đã dùng tệp nào.
- **Bộ TISA:** Quảng Cáo: giải thích rõ vì sao dòng Bật, tắt, đổi ngân sách chưa sáng khi mới nối bằng MCP (cần tài khoản API có quyền Quản lý chiến dịch và bật công tắc cho phép), kèm nút mở hướng dẫn.
- **Bộ TISA:** Nạp kiến thức: chọn được mô hình và mức nỗ lực cho phần bóc tách, có gợi ý thông minh theo nguồn đang gửi (video dài, khóa học, nhiều nguồn, văn bản ngắn). Quy trình bóc tách sâu hơn (mổ xẻ bảy góc, thiết kế áp dụng có thử nghiệm và cách đo) và chi tiết bóc tách có hai mục rõ ràng: Đã học được gì và Sẽ áp dụng thế nào.

## [0.574.3] - 2026-11-17
### Thêm mới
- **Bộ TISA:** Cửa sổ xem hình, video và tệp có hai tông sáng và tối, đổi theo giao diện đang dùng. Đã bỏ nút Thư mục và mục Đến nơi chứa tệp vì bấm vào không giải quyết được việc gì.
- **Bộ TISA:** Điện thoại gọn hơn: cột việc Đang làm không còn kéo dài cả màn hình khi trống, bộ lọc ngày gọn một hàng, thanh tab Đội ngũ và Kết quả nằm một hàng cuộn ngang, đầu thẻ thư mục không còn xuống dòng từng chữ, hàng lối tắt trong Lấy dữ liệu từ máy tính ẩn thanh cuộn.

## [0.574.2] - 2026-11-17
### Thêm mới
- **Bộ TISA:** Giao diện mới đẹp và hiện đại hơn, đúng cả tông sáng lẫn tông tối và cả điện thoại: thẻ, tab dạng thanh chọn, ô nhập, bong bóng chat, danh sách hội thoại, danh sách cộng sự và danh sách khách Chatbot cùng một kiểu bo góc, đổ bóng mềm, trạng thái rê chuột và đang chọn rõ ràng. Điện thoại có vùng bấm to hơn và thanh nút Hỏi chuyên gia gọn một hàng.
- **Bộ TISA:** Hỏi chuyên gia: thanh nút trên đầu làm nổi bật hơn. Nút Nhân bản được thay bằng nút Hội thoại cũ (xem lại các cuộc hội thoại cũ của cộng sự để tìm lại, Nhân bản vẫn còn trong menu ba chấm của cộng sự). Nút đóng/mở khung phải luôn thấy dù phóng to chữ, và khung phải luôn có nút X để đóng.
- **Bộ TISA:** Giao việc cho cộng sự (tab Công việc): có ô Giao nhiều việc cùng lúc. Gõ mỗi dòng (hoặc mỗi mục 1. 2. 3.) một việc, xác nhận một lần, các việc vào hàng chờ và chạy lần lượt. Gửi lại sau khi rớt mạng không tạo trùng việc đã giao.
- **Bộ TISA:** Lịch sử hội thoại của cộng sự chỉ hiện hội thoại của chủ với cộng sự, không còn lẫn hội thoại bot với khách (khách vẫn xem ở trang Chatbot).
- **Bộ TISA:** Trang Kết quả: danh sách tệp của việc chỉ hiện thứ dùng được (ảnh, video, tài liệu, trang tính, trình chiếu, văn bản txt, bộ cài, tệp nén, link Drive). Tệp .md và .json do AI ghi chú không còn hiện, chỉ lưu trong thư mục việc và bộ não. Danh sách cũng hết hiện trùng tệp. Việc làm tiếp có nhãn Bước mấy trên tổng bao nhiêu và làm tiếp từ kết quả nào.
- **Bộ TISA:** Trang Kết quả: sản phẩm (video, tài liệu, trang tính, ảnh) hiện ngay trong tab của người làm ra nó để xem và chỉnh tại chỗ, trang Tổng hợp vẫn hiện tất cả. Khung xem video theo đúng tỉ lệ của video: video dọc 9:16 hiện khung dọc, video ngang hiện khung ngang.
- **Bộ TISA:** Sơ đồ đội: mỗi phòng là một thẻ cao tối đa khoảng 6 người, phòng đông người thì cuộn ngay trong thẻ (tên phòng và số người luôn hiện ở đầu thẻ). Tên người xuống tối đa 2 dòng, không còn tràn sang thẻ bên.
- **Bộ TISA:** Xem tệp: bấm vào thẻ tệp trong chat hoặc nút Xem ở trang Kết quả mở cửa sổ popup xem ảnh, video, âm thanh, PDF, văn bản ngay trên trang (không mở tab mới). Có mũi tên và phím mũi tên để chuyển tệp, dải ảnh nhỏ bên dưới, nút Tải về, Hiện trong thư mục, Tải tất cả thành một file .zip.
- **Bộ TISA:** Chuột phải vào tệp: Xem, Tải về, Hiện trong thư mục trên máy, Mở bằng ứng dụng trên máy, Đến nơi chứa tệp (trang Tệp tin, dùng được cả khi truy cập từ xa), Sao chép đường dẫn, Mở tab mới.
- **Bộ TISA:** Cuối câu trả lời của AI có dải Tệp trong tin nhắn: thẻ có ảnh nhỏ, cuộn ngang, nút Tải tất cả. Trang Kết quả có lưới hình ảnh và nút Tải tất cả cho video, hình, tài liệu.
- **Bộ TISA:** Danh sách hội thoại trình bày lại gọn hơn: mỗi hội thoại một dòng ngăn bằng đường kẻ, tiêu đề nhóm có đường kẻ chạy dài.
- **Bộ TISA:** Nút + trong khung chat có mục mới "Lấy dữ liệu từ máy tính": mở cửa sổ chọn ổ đĩa, thư mục và tệp ngay trên máy đang chạy TISA BOT (Màn hình nền, Tài liệu, Tải xuống, ổ ngoài, bộ não...). Tích chọn một hay nhiều tệp, hoặc chọn cả thư mục; AI làm việc tại chỗ, tệp giữ nguyên trên máy, không sao chép hay tải lên. Có lọc theo ảnh, video, tài liệu, tìm nhanh trong thư mục, hiện tệp ẩn, nhớ nơi vừa dùng, dùng được trên điện thoại.
- **Bộ TISA:** Cột Lưu trữ trong danh sách kết quả gọn lại: mỗi việc chỉ hiện nút Ảnh, Video, Tệp kèm số lượng, bấm vào mở cửa sổ xem nhiều tệp.
- **Bộ TISA:** Sơ đồ điều phối và văn phòng 3D gọn hơn khi đội đông người: danh sách người trong phòng cuộn được, người đang làm xếp trước, thẻ tên 3D tự ẩn khi trên 60 nhân sự.
- **Bộ TISA:** Cài đặt đội: sửa lỗi nút Chi tiết và nút xoá đè lên ô chọn phòng ở những cộng sự anh tự thêm.
- **Bộ TISA:** Chatbot, bộ chọn kênh: mỗi nền tảng một màu và một nhãn rõ ràng. Zalo là ô vuông xanh chữ Zalo, Fanpage (Messenger) màu tím gradient; nhóm kênh có dải màu và tên in hoa, tên tài khoản hiện đủ không bị cắt.
- **Bộ TISA:** Menu Giao dự án gọn lại còn 4 mục, mỗi mục trả lời một câu hỏi: Cần anh (việc nào đang chờ anh, có số ngay trên mục), Đang làm (đội làm tới đâu), Kết quả (thành phẩm), Đội ngũ. Văn phòng 3D, Sơ đồ và hồ sơ, Cài đặt đội nay là 3 nút ở đầu trang Đội ngũ. Bỏ hàng 3 ô số cũ vì số đếm cả việc tồn nhiều ngày nên khó hiểu.
- **Bộ TISA:** Số "Cần anh" chỉ đếm việc thật sự chờ anh (duyệt, anh làm, bị kẹt, nộp dữ liệu), tin trả lời của đội tách riêng, và dùng chung một con số ở mọi nơi. Bàn làm việc chỉ hiện 3 việc đầu kèm nút Xem tất cả; trang đầy đủ (gộp theo từng việc, duyệt và sửa ngay tại chỗ) nằm ở mục Cần anh. Khung bên phải đổi tên thành "Đội đang làm", có phần "Vừa làm gần đây".
- **Bộ TISA:** Cần anh và Đang làm tách thành hai trang riêng: Cần anh chỉ có danh sách việc chờ anh quyết; Đang làm chỉ có bảng công việc theo trạng thái. Lịch báo cáo tự động và báo cáo gần đây chuyển sang mục Kết quả, tab Báo cáo tự động.

## [0.574.1] - 2026-11-16
### Thêm mới
- **Bộ TISA:** Kết nối hay bị văng: kết nối Meta Ads MCP tự tạo (mcp.facebook.com/ads) bị Meta từ chối vì chỉ vài ứng dụng được cấp phép, không phải hết phiên. Trang Kết nối giờ nói đúng điều này và chỉ sang kết nối Meta Ads (tự tạo app) hoặc mã API ở trang Quảng Cáo, thay vì bảo bấm Kết nối lại mãi.
- **Bộ TISA:** Kết nối dán mã tay bị từ chối (401, 403) hoặc Zalo báo đã đăng xuất không còn bị thử lại liên tục (trước đó hơn 12.000 lần): nghỉ 10 phút, 30 phút rồi 2 giờ giữa các lần thử. Bấm Kiểm tra hoặc đổi mã thì thử lại ngay.
- **Bộ TISA:** Zalo đã đăng xuất hiện đúng câu Bấm Kết nối lại rồi quét mã QR, trước đó bị báo nhầm là lỗi mạng.
- **Bộ TISA:** Trang Kết quả: việc giao làm tiếp từ một kết quả có tiêu đề rõ hơn. Tiêu đề chỉ nói phần việc mới, kèm tên chuỗi và số bước (ví dụ Mong muốn xây kênh · Bước 2: Đào sâu vấn đề), và có dòng nhỏ Tiếp từ việc trước, bấm vào là mở việc đó.

## [0.574.0] - 2026-11-16
### Cải thiện
- **Gõ thêm lúc đang theo đuổi mục tiêu không còn làm mục tiêu tạm dừng.** Tin bạn gửi được gộp vào mục tiêu: vòng đang chạy đọc nó ở bước kế tiếp, các vòng sau đều mang theo, nên bạn chỉnh hay mở rộng mục tiêu ngay khi TISA BOT đang làm. Mỗi tin như vậy cho thêm một vòng (tối đa 10). Vòng nào báo đạt mà chưa kịp đọc tin của bạn thì TISA BOT vẫn làm thêm một vòng cho tin đó. Nút Dừng vẫn tạm dừng mục tiêu như trước.

## [0.573.0] - 2026-11-16
### Thêm mới
- **Bộ TISA:** Kết quả của Đội Quân AI: video, âm thanh, tài liệu, trang tính giờ bấm Xem và Tải về được ngay trên bảng. Video chạy thẳng trong cửa sổ kết quả, có nút Tải về. Danh sách tệp đọc thẳng từ thư mục của việc trên máy nên hiện ngay cả khi bảng chưa ghi kịp.
- **Bộ TISA:** Việc dựng video, làm hình, soạn tài liệu: thành phẩm lưu ở thư mục kết quả chung (04-ket-qua, output) được tự gom vào thư mục của việc khi báo xong, chỉ gom tệp có tên khớp với việc để không gắn nhầm. Nhân sự có thêm lệnh ban-giao để đưa tệp lên bảng.
- **Bộ TISA:** Tài liệu và trang tính: nhân sự đưa lên Google Drive (khi đã nối Drive) vào thư mục TISA BOT - Kết quả đội AI, chia theo loại, năm, tháng, đặt tên có ngày và tên việc, rồi gắn link Drive vào kết quả. Chưa nối Drive thì ghi rõ chưa lên Drive, tệp vẫn tải được ở bảng.
- **Bộ TISA:** Sửa lỗi bảng báo Xong nhưng phần việc vẫn hiện Đang làm (1/2 phần, 65%, Chưa có nội dung): báo xong thì các phần quên đóng được đóng lại.
- Gói Google Tag Manager trong TISA Store đăng nhập Google ngay trong dashboard, như Analytics và Ads.
- **Trang Cộng sự có tab Đã học cho từng trợ lý.** Nút trên thanh đầu đổi thành "Tài liệu & Đã học". Tab mới liệt kê những bài học trợ lý tự rút ra khi làm việc, đúng những bài nó đang dùng, kèm nơi áp dụng (chat riêng, trong nhóm, mọi nơi). Bạn sửa, xoá hay thêm bài học ngay ở đó, giống tab Đã học của project.
- Bài học bạn thêm dùng ở mọi nơi. Bài học bạn sửa thành của bạn và không bị thay khi danh sách đầy. Xoá thì trợ lý thôi dùng và không tự học lại đúng câu đó.
### Cải thiện
- **Dùng lại key Google cho mọi dịch vụ Google.** Hàng "Dùng lại key này" giờ nằm ngay đầu form, có cả ở Google Ads, Analytics, Merchant Center, Search Console, và mượn được key (kể cả service account) đã lưu ở bất kỳ dịch vụ Google nào. Google chỉ cho xem Client Secret đúng một lần lúc tạo, nên key trong TISA BOT thường là bản duy nhất còn lại.
- **Đổi key ngay trên kết nối.** Mục "Kết nối lại (đăng nhập / đổi key)" của Gmail, Lịch, Analytics, Ads... giờ mở form đổi key: chọn key đã lưu ở dịch vụ khác, hoặc dán key mới, rồi đăng nhập lại.
- **Báo trước khi mất key.** Xoá kết nối cuối cùng còn giữ một key Google thì hộp xác nhận nói rõ, kèm cách giữ lại.
- Trong ngăn tài liệu của trang Cộng sự, tab nằm trên công tắc "Của trợ lý / Chỉ cuộc này", vì công tắc chỉ là lựa chọn của tab Tài liệu.

## [0.571.1] - 2026-11-16
### Sửa lỗi
- **Tab Công việc của cộng sự ghi lại từng lần cộng sự tự làm.** Trước đây phần Auto báo "Hôm nay đã tự làm 1 lần" mà tab Công việc vẫn trống, vì tab chỉ đọc mục tiêu, việc team, việc chat và quy trình. Giờ mỗi lần cộng sự tự nhìn quanh hay tự xem lại là một thẻ ở nguồn Auto, kèm kết quả: đã tự làm gì, đã nhắn bạn, đề xuất việc gì, hay không thấy việc gì cần làm. Số lần hôm nay và số thẻ luôn khớp nhau vì đọc cùng một sổ.

## [0.571.0] - 2026-11-16
### Thêm mới
- **Bộ TISA:** Quảng Cáo, Thiết lập: tách riêng bước Chọn nền tảng và bước Chọn cách làm, các bước sau đánh lại số.
- **Bộ TISA:** Quảng Cáo, Thiết lập: ô nhập ý tưởng ở chế độ Tự động rộng đủ chiều ngang, có công tắc giao luôn cho cộng sự; hai ô tải video và hình cao bằng nhau.
- **Bộ TISA:** Quản lý web: nút Đưa Web CRM lên Cloudflare với 3 cách (TISA BOT đưa lên luôn khi đã nối Cloudflare, Claude làm giúp, tự làm theo hướng dẫn từng bước).
- **Bộ TISA:** Quản lý web: nút Đưa Lead Page và Sale Page lên Cloudflare Pages với 3 cách tương tự, kèm nhắc nối form về CRM.
- **TISA Store có tab Tất cả.** Tab đứng đầu hàng, gom mọi trợ lý, kỹ năng, quy trình, công cụ và kết nối vào một lưới, và kho mở ra ở tab này. Ô tìm ở đây tìm trên cả kho, mỗi thẻ ghi rõ nó thuộc loại nào.
- **Tìm ở một tab mà không thấy thì có nút tìm trong Tất cả.** Nút ghi sẵn số mục khớp ở các tab khác và giữ nguyên chữ bạn đã gõ.

## [0.570.2] - 2026-11-16
### Thêm mới
- **Bộ TISA:** Chi tiết kết quả: phần kiểm duyệt do anh xem lại giờ có nút Đã xem xong để ghi nhận (trước đó phần này treo ở Chờ anh làm, không có nút nào). Tiêu đề đầu cửa sổ chi tiết việc cũng dùng tiêu đề ngắn.
- **Bộ TISA:** Trang Quảng Cáo, nút Hỏi cộng sự: sửa lỗi hỏi liên tiếp nhiều câu thì câu trả lời đã về mà trang vẫn kẹt ở đang đọc câu hỏi (mỗi câu hỏi giờ có bộ đếm riêng). Có hiển thị số giây đã chờ và nút Hỏi lại khi lượt bị gián đoạn hoặc chờ quá lâu.
- **Bộ TISA:** Chi tiết kết quả: khu Việc tiếp theo từ kết quả này hiện ở mọi tab (không chỉ tab Tổng hợp) và có nút Làm tiếp từ kết quả này ở chân cửa sổ.
- **Bộ TISA:** Ô Nhập ý tưởng quảng cáo bố cục lại: ô nhập rộng hết khung, nút mic nằm trong ô (đỏ nhấp nháy khi đang nghe), nút phân tích gọn bên dưới.
- **Bộ TISA:** Thiết lập quảng cáo có hai nút Triển khai: Cách 1 tự động qua API hoặc MCP (cộng sự dựng chiến dịch tạm dừng, có báo trạng thái kết nối), Cách 2 thủ công bằng Claude trên Chrome (tải hình, video về máy, chép lệnh thiết lập kèm hướng dẫn rồi dán vào Claude để Claude điều khiển trình duyệt cài đặt).
- **Bộ TISA:** Khu Làm tiếp từ kết quả này thiết kế lại gọn đẹp hơn: tiêu đề có biểu tượng, hàng gợi ý cuộn ngang, ô nhập rộng có mic, nút Giao việc tiếp nổi bật.

## [0.570.1] - 2026-11-16
### Thêm mới
- **Bộ TISA:** Giao việc bằng giọng nói xong, trên khung chat hiện thanh Tình hình công việc: AI đang làm việc gì, đã chạy bao lâu, đang ở giai đoạn nào (nhận lệnh, tìm hiểu, triển khai, soạn kết quả), bước hiện tại, hoạt động gần nhất và đã thật sự ghi, sửa hay chạy lệnh chưa. Việc xong hoặc lỗi cũng báo ngay.
- **Bộ TISA:** Bảng Quảng Cáo làm lại: hết chữ đè lên nhau, kéo mép tên cột để chỉnh to nhỏ, có đường kẻ dọc giữa các cột và vạch ngang tách từng chiến dịch. Bấm vào chiến dịch để xem các nhóm quảng cáo, bấm vào nhóm để xem từng bài quảng cáo (có ảnh nhỏ và đủ chỉ số, số lấy từ Meta lần đầu rồi lưu lại). Có nút phóng to bảng ra cả màn hình.
- **Bộ TISA:** Gợi ý tối ưu quảng cáo dựa trên số tiền chạy thật: bảng tiền theo từng nền tảng, 3 cách chia lại tiền (An toàn, Cân bằng, Tăng tốc) liệt kê từng chiến dịch giữ, giảm, tăng hay dừng, thêm các gợi ý về tiền chưa ra kết quả, so sánh nền tảng, nhóm đắt hơn hẳn trong cùng chiến dịch, dự báo chi cả tháng, và nút nhờ AI tư vấn sâu.
- **Bộ TISA:** Tab Thiết lập quảng cáo có nút Nhập ý tưởng, AI làm thay: anh bấm mic để nói hoặc gõ ý tưởng, AI phân tích, soạn nội dung và hướng dẫn chi tiết từng bước (bước nào AI làm được, bước nào anh tự làm), rồi dựng chiến dịch tạm dừng theo kế hoạch.
- **Bộ TISA:** Nút Nhờ Claude làm giúp ở phần kết nối nay chép sẵn lệnh để dán vào tiện ích Claude trên Chrome: Claude tự thao tác phần làm được, dừng đúng chỗ anh phải tự làm (đăng nhập, mã xác thực, sao chép và dán mã), có hướng dẫn cụ thể từng việc.
- **Bộ TISA:** Trang Kết quả của Đội Quân AI: tiêu đề việc giao bằng giọng nói giờ do AI tóm tắt thành một dòng ngắn, dễ hiểu (kèm một dòng mô tả), thay cho nguyên văn lời nói dài dòng. Tiêu đề được lưu lại trên máy; chưa tóm tắt kịp thì tự rút gọn bỏ lời chào. Rê chuột vào tiêu đề để xem lời gốc.
- **Bộ TISA:** Bấm Mở file hoặc Hiện trong Finder ở trang Kết quả giờ mở ngay lập tức (trước đây phải chờ vài chục giây vì đi vòng qua máy chủ đám mây). Không mở thẳng được thì tự dùng đường cũ.
- **Bộ TISA:** Chatbot: có nút Chọn page hiển thị (ở tab Kênh và trong bộ chọn kênh) để ẩn bớt Fanpage không dùng khi nối Facebook kéo về quá nhiều. Bật hoặc tắt từng trang, hoặc bấm Chỉ hiện trang đang có A.I. trực. Ẩn chỉ là không hiển thị trong danh sách, không xoá và không tắt bot.
- **Bộ TISA:** Chi tiết kết quả: có khu Việc tiếp theo để giao nối tiếp từ kết quả đã làm xong (nói hoặc gõ), nút Nhờ Claude làm giúp gọn thành một nút kèm Cách thao tác và không hiện ở phần kiểm duyệt; Đội ngũ bố cục lại gọn hơn, hàng cộng sự mới đồng bộ với nhân sự có sẵn.
### Sửa lỗi
- **Bảng chọn repository trong dự án và trong team không còn bị cắt.** Mục "Đã chọn" trước đây chỉ hiện một dải mỏng, và danh sách bên dưới không cuộn được tới các repository ở cuối. Giờ từng dòng hiện đủ và danh sách cuộn bình thường, ở cả tài liệu của dự án, của cộng sự, ô tạo team và khung chat của team.

## [0.570.0] - 2026-11-16
### Thêm mới
- **Bộ TISA:** Lõi hệ thống lên bản mới nhất: cúp máy cuộc gọi vẫn giữ việc đang chạy và đẩy kết quả vào chat, hủy việc nền ngay trong chat, thêm nhiều sửa lỗi ổn định.
- **Bộ TISA:** Báo cáo Quảng Cáo có kho số liệu: quét Facebook một lần, lưu lịch sử từng ngày trên máy, đổi kỳ xem chỉ đọc kho, bảng liệt kê đủ chiến dịch và nhóm quảng cáo; tự đồng bộ nền mỗi giờ.
- **Bộ TISA:** Giọng nói: câu lệnh nói thêm lúc đang có việc chạy không còn bị bỏ qua, khung chat không vẽ lại giữa cuộc gọi nên không mất lời nói.
- **Sửa được webhook sau khi tạo.** Phần Cấu hình của mỗi webhook có nút Sửa: đổi tên, đổi quy trình hoặc việc viết tay, ghi chú và mức quyền ngay trong cửa sổ đó. Link và khoá giữ nguyên, nơi đang gửi sự kiện tới không phải đổi gì.
- **Kết nối API tuỳ chỉnh.** Dịch vụ nào có REST API và API key mà chưa có MCP (POS, CRM, vận chuyển, hoá đơn điện tử...) giờ nối được ở trang Kết nối: dán địa chỉ gốc và key, mọi bộ não gọi được API đó.
- **Key không bao giờ tới tay model.** Key được mã hoá, server tự gắn vào lời gọi và chỉ gửi tới đúng máy chủ đã khai; key có lọt trong kết quả cũng bị che.
- **Mặc định chỉ đọc.** Ở mức Chỉ đọc TISA BOT chỉ gọi GET; muốn tạo, sửa, xoá trên dịch vụ đó thì nâng kết nối lên Toàn quyền.
- **ChatGPT và Claude đổi được model và effort ngay trong câu lệnh gửi qua TISA BOT Gate.** Bảo ChatGPT "bảo TISA BOT làm việc này bằng Opus, effort cao" là xong: model được ghim cho hội thoại đó như khi bạn chọn trên thanh model (chip hiện đúng, đổi lại lúc nào cũng được), còn effort chỉ áp cho đúng tin đó, không đổi cài đặt chung. Công cụ mới `tisa_chat_models` cho AI bên ngoài xem TISA BOT có những model nào.
- **Việc ChatGPT giao xong mà nó đã thôi chờ thì chuông TISA BOT báo về điện thoại**, kèm câu trả lời và câu cần nhắn sang ChatGPT ("xem kết quả TISA BOT"). ChatGPT và Claude chưa cho máy ngoài đánh thức một cuộc chat, nên đây là đường ngắn nhất: nhắn một câu, công cụ mới `tisa_chat_updates` trả mọi kết quả chưa đọc, kể cả ở một cuộc chat mới bên ChatGPT.
- **Gắn repository GitHub vào Project.** Mở khung project, tab Tài liệu, bấm Thêm tài liệu rồi chọn Repository GitHub. Mọi cuộc chat trong project tự có repository đó ngay từ tin đầu, mỗi cuộc làm trên một nhánh riêng.
- **Gắn repository vào tài liệu của Cộng sự.** Mỗi cuộc chat riêng với trợ lý đó cũng tự có repository, TISA BOT vẫn tự commit, đẩy lên GitHub và mở PR như thường.
- **Chọn repository ngay lúc tạo Nhóm.** Trong mục tài liệu của hộp Tạo nhóm có nút Gắn repository GitHub, nhóm tạo xong là repository đã sẵn.
- **Bảo cải tiến là làm được, có hoàn tác.** Nói "cải tiến chính em" hay "sửa lại skill này", trợ lý tự sửa vai trò, hướng dẫn, skill, model của nó, trợ lý khác, skill, workflow, vòng lặp, bộ nhớ. Mỗi lần sửa có mã và sao lưu, nói "hoàn tác #12" là về bản cũ.
- **TISA BOT sửa được chính mã nguồn của nó.** Khi GitHub đã kết nối với repo tisa-os, trợ lý tự gắn repo vào chat, sửa trên nhánh riêng; TISA BOT tự kiểm, mở PR và merge khi CI xanh.
- **Tự cập nhật lên bản vừa phát hành.** Bảo "cập nhật đi", TISA BOT chờ lượt chat xong rồi chạy đúng quy trình của nút Cập nhật, bản mới lỗi thì tự lùi.
- **Bật Auto là trợ lý tự nhìn quanh với toàn quyền.** Ở chat riêng, mỗi lần tự thức trợ lý dùng đủ công cụ đã kết nối (email, lịch, bán hàng, tra web...) và được tự làm việc thật trong vai của mình. Việc nào đã làm cũng luôn được báo lại cho bạn.
- **Trợ lý tự hẹn giờ kiểm lại.** Thấy việc có ngày giờ (giải chạy, cuộc hẹn, hạn nộp) thì nó tự đặt mốc, ví dụ sáng hôm trước hay tối hôm trước. Tới giờ nó tự thức, kiểm lại nguồn rồi mới quyết có nhắn hay không.
- **Gợi ý và nhắc nhở, không phải thông báo.** Trợ lý chỉ nhắn khi điều đó mới, đúng lúc và làm được ngay: tối đa hai đoạn ngắn, một lời khuyên cụ thể, kèm link nguồn thật. Lời nhắc vào nhóm Nhắc lịch, gợi ý vào nhóm mới "Gợi ý của trợ lý" (mặc định vẫn tới tay bạn, hạ hay tắt ở trang Thông báo).
- **Link mở thẳng một trang của dashboard.** Link dạng `#p=tasks` (hay tên trang khác) mở đúng trang đó, kể cả khi tab TISA BOT đang mở sẵn.
- **Huỷ việc nền ngay trong chat.** Bảo TISA BOT huỷ một việc là việc rời hàng đợi, việc đang chạy dừng luôn, lý do được ghi vào nhật ký. Khi trả một việc chưa đạt về làm lại, có thể dặn thêm cách sửa và lần làm lại sẽ theo lời dặn đó.
- **Nối Fanpage có thêm ô "Đọc số liệu bài viết".** Ô tuỳ chọn này xin quyền đọc lượt tiếp cận, lượt lưu của bài. Bảng kiểm tra Messenger báo Trang đã có quyền này chưa.
- **Bấm vào đoạn trích là cuộn về đúng câu gốc.** Trích một câu trong câu trả lời dài để hỏi tiếp, sau này chạm vào đoạn trích đó trong tin của bạn là khung chat tự cuộn lên đúng câu ấy và tô sáng nó vài giây.
- Câu gốc nằm ở phần tin cũ chưa tải thì TISA BOT tự tải thêm để tìm. Chạy ở cả khung chat chính lẫn trang Nhóm.
- **Ô "Ghi nhớ đăng nhập trên máy này" ở màn đăng nhập.** Để tích như cũ thì máy này giữ đăng nhập 30 ngày. Bỏ tích khi dùng máy của người khác: đóng trình duyệt là thoát, để yên 4 giờ hoặc quá 24 giờ TISA BOT cũng tự đăng xuất.
- Trang Bảo mật đánh dấu thiết bị nào đăng nhập kiểu không ghi nhớ.
- **Project tự học ngữ cảnh.** Trong lúc làm việc ở một project, TISA BOT tự ghi lại điều bền và riêng của project (sự thật, quyết định đã chốt, thuật ngữ) và dùng lại ở mọi cuộc sau trong project. Xem, sửa, xoá ở tab mới "Đã học". Ô Hướng dẫn vẫn là của bạn: TISA BOT chỉ sửa khi bạn bảo thẳng.
- **Thả tài liệu vào chat là đủ.** File hay link dùng lâu dài được TISA BOT tự gắn vào project kèm một dòng nói nó chứa gì, nên nó mở đúng tài liệu mà không cần ghim cả file.
- **Cộng sự và nhóm cũng có mô tả tài liệu.** Chat riêng với một cộng sự, nó tự gắn và mô tả tài liệu của mình; tài liệu nhóm có dòng mô tả cho mọi thành viên đọc.
- **Bộ cài Windows báo trước mọi thay đổi trên máy.** Trước khi cài có một trang liệt kê những gì sẽ được tải và cài (TISA BOT, Git, Python, Node.js, các công cụ AI), kèm cam kết quyền riêng tư và cách gỡ.
- **Hai lựa chọn mới khi cài.** Có thể bỏ tích "tự chạy khi đăng nhập Windows" và "cài các công cụ AI dòng lệnh". Để nguyên thì bộ cài làm như trước.
- **Có trang chính sách ký số và chính sách quyền riêng tư.** Nói rõ TISA BOT không theo dõi, không gửi số liệu sử dụng, và tự nó chỉ tải file công khai để kiểm tra cập nhật.
- **Sẵn sàng ký số miễn phí qua SignPath Foundation.** Phần ký trong quy trình dựng bộ cài đã nối xong và đang tắt, sẽ bật khi dự án được SignPath chấp nhận. Bộ cài hiện vẫn chưa ký.
- **Chọn được cả thư mục làm tài liệu.** Ô tìm ở phần Thêm file của dự án, cộng sự, cuộc trò chuyện và nhóm (lúc tạo nhóm lẫn tab Thông tin) giờ hiện cả thư mục khớp tên, có icon thư mục riêng. Bấm Thêm là gắn cả thư mục, không phải chọn từng file.
- **TISA BOT biết trong thư mục có gì.** Thư mục chưa ghim thì TISA BOT thấy đường dẫn và tự mở file bên trong khi cần. Ghim thì danh sách file trong thư mục được nạp sẵn vào mỗi lượt. Thư mục thêm vào nhóm được ghim sẵn.
- **An toàn hơn cho thư mục.** Hàng thư mục không có nút xoá khỏi brain, chỉ có gỡ khỏi danh sách. Bấm vào tên thư mục là mở nó ở trang Tệp tin.
- **Model Claude mới tự hiện trong trình chọn model.** TISA BOT đọc thêm danh mục model mà Claude Code tải về từ Anthropic, nên model vừa ra (bản CLI đang cài chưa ghi sẵn tên) cũng hiện ngay, không phải chờ bản TISA BOT mới ghi thêm tên.
### Sửa lỗi
- **Một gói trong Kho cài được vào nhiều brain.** Trước đây gói đã cài ở brain này thì sang brain khác chỉ hiện "đã cài" kèm nút Tắt và Gỡ, không cách nào đưa trợ lý và skill của gói vào brain đó. Giờ thẻ gói hiện nút "Cài vào brain này". Cập nhật gói thì mọi brain đã cài cùng lên bản mới, phần bạn đã tự sửa vẫn giữ nguyên. Gỡ gói thì gỡ ở mọi brain, và hộp xác nhận nêu tên từng brain.
- **Chữ TISA BOT viết trước và sau mỗi lần gọi công cụ không còn dính liền nhau** (kiểu "cần đăng nhập.Xong mục 3"). Mỗi đoạn mới bắt đầu ở một dòng mới, với Claude Code, Codex, Grok Build và Antigravity.
- **Ghi chú TISA BOT viết trong lúc đang làm cũng theo đúng thứ tiếng bạn dùng**, không còn trôi sang tiếng Anh giữa chừng khi đọc code hay log.
- **Chat với TISA BOT qua Zalo không còn mặc định trả lời tiếng Việt.** Ai nhắn tiếng gì thì TISA BOT trả lời tiếng đó.
- **Nhắc hẹn tạo qua Telegram nói đúng múi giờ bạn đặt trong Cài đặt**, không còn ghi "giờ Việt Nam" cho mọi người.
- **Mức nghĩ (Effort) giờ có tác dụng với Gemini 4.** Chạy Gemini 4 Hydrogen, Argon hay Carbon bằng API key Gemini thì trước đây chọn mức nghĩ nào cũng như không, model luôn chạy theo mức mặc định của nó. Giờ mức bạn chọn được gửi đi, và mọi đời Gemini sau này cũng tự được nhận.
- **Trang Mức dùng tính đúng tiền Gemini mới.** Gemini 4 trước đây bị tính theo giá Gemini cũ nên hiện rẻ hơn thực tế nhiều lần, còn Gemini 3.5 Flash-Lite lại bị tính theo giá bản Pro. Giờ mỗi model có giá riêng.
- **TISA BOT không còn trả lời tiếng Việt khi bạn đang chat tiếng Anh.** Lời dặn ngôn ngữ viết lại bằng tiếng Anh, nói rõ ngôn ngữ bạn đã dặn thắng, và phần tiếng Việt xung quanh không phải gợi ý.
- **Việc chạy nền (Kanban, nhắc hẹn, loop) không còn luôn báo bằng tiếng Việt.** Nó theo ngôn ngữ của chính đầu việc.
- **Câu trả lời tiếng Nhật, Hàn, Trung, Thái được đọc bằng giọng bản xứ**, và tin nhắn tiếng Anh kèm file không còn bị hiểu là tiếng Việt.
- **Chọn nhiều ảnh một lần trong chat Nhóm trên iPhone giờ đính kèm và gửi được.** Trước đây chọn xong vài ảnh thì không ảnh nào hiện lên ô nhập, chỉ một ảnh mới lọt qua. Thêm tài liệu cho nhóm và nhập file nhóm cũng dùng chung cách chọn file đã sửa.
- **Bấm vào file team vừa ghi là mở ra đọc được.** Trước đây bấm link file trong chat nhóm không thấy gì xảy ra. Nay file mở ngay trong khung chat của nhóm, bấm X để quay lại cuộc trò chuyện, chữ đang gõ dở vẫn còn.
- **Trang nào chưa có chỗ cho trình sửa thì file mở dạng bảng nổi**, ví dụ link file ở trang Việc, nên không còn chỗ nào bấm mà không thấy gì.
- **Cúp máy khi TISA BOT còn đang làm việc được giao trong cuộc gọi thì việc không bị bỏ.** TISA BOT làm nốt rồi gửi kết quả vào khung chat của cuộc gọi, kèm thông báo.
- **Đường gọi Tự động không tự chuyển sang ChatGPT Live chỉ vì máy có sẵn phiên Codex.** ChatGPT Live chỉ được chọn khi ChatGPT là model chính hoặc đã kết nối ở trang Models.
- **Việc chạy nền TISA BOT tự bật khi chat bằng API key báo xong đúng lúc.** Trước đây việc kẹt ở trạng thái "đang chạy" tới khi khởi động lại máy chủ.
- **Cuộc chat đã ghim model giữ nguyên model đó.** Khi model ghim tạm hết lượt hoặc mất đăng nhập, lượt chat chạy tạm bằng model chính, rồi tự quay lại model đã ghim khi dùng được lại.
- **Link file kèm số dòng (kiểu `agents/x.md#L66-L75`) mở đúng file.** Câu trả lời không còn bị gắn cảnh báo sai "không tìm thấy file trong brain".
- **Hội thoại Messenger hiện tên khách thay vì một dãy số.** Khi Meta không cho đọc hồ sơ, TISA BOT lấy tên từ cuộc trò chuyện của Trang, và tự thử lại sau 10 phút nếu lần trước không lấy được.
- **Lịch nhắc ở mức chỉ đọc xem được Việc của tôi.** Trước đây lịch nhắc kiểm tra tiến độ báo "không kiểm tra được"; giờ nó đọc được danh sách, còn thêm, sửa, xoá, tích vẫn cần quyền ghi.
- **Bảng chọn model mở ngay trên nút model.** Trước đây khung soạn tin cao (có file đính kèm, gõ nhiều dòng) thì bảng bị đẩy lên xa nút, và danh sách dài còn bị cắt mất mấy dòng đầu. Giờ bảng chọn model, mức suy nghĩ, hạn mức gói và menu "+" đều mở sát hàng nút, và luôn nằm trọn trong màn hình.
- **Menu "+" ở trang Nhóm cũng vậy**, kể cả bảng chọn thư mục và GitHub mở từ menu đó.
- **Kết nối Google Workspace làm được việc thật trên Form, Drive và Sheets.** Trước đây thẻ chỉ bật bộ công cụ rút gọn, nên TISA BOT không sửa được câu hỏi Form, không đọc câu trả lời, không xem thư mục Drive, không đổi tên hay chép file, không thêm tab hay ghi nối dòng vào Sheets. Giờ đủ cả, không phải đăng nhập Google lại.
- Kết nối đã tạo từ trước tự lên bộ công cụ đầy đủ sau khi cập nhật.
- **Sửa compose trong hPanel rồi bấm Deploy không còn bị chặn.** Bản 0.557.1 làm file Hostinger dài 33.167 ký tự, quá trần 32.768 của hPanel. File giờ còn khoảng 28.400 ký tự, phần bảo vệ cập nhật vẫn chạy y như cũ.
- Mở TISA BOT lần đầu trên một trình duyệt mới không còn hiện nhầm dòng đỏ "Phiên đăng nhập đã hết hạn".
- **Nút "Đẩy lại" và dấu chấm than ở thẻ GitHub không còn kẹt mãi.** Việc đã lỡ lưu một tên nhánh bị trùng trên GitHub (từ trước bản sửa trước) vẫn cứ đẩy vào đúng tên đó, nên lần thử lại nào cũng báo "có commit mà máy này không có". Giờ khi chưa đẩy lên được lần nào, TISA BOT chọn lại tên nhánh còn trống (hoặc theo nhánh đang mở ở máy), đẩy lên và mở PR, dấu chấm than tự tắt.
- **Việc GitHub thứ hai trong một khung chat không còn kẹt ở bước đẩy lên.** Tên PR và tên nhánh giờ lấy từ chính câu yêu cầu, bỏ qua các dòng ngữ cảnh như "[NGỮ CẢNH GIAO DIỆN: ...]", nên mỗi việc có tên riêng. Nếu tên đã có người dùng ở máy hay trên GitHub, TISA BOT tự thêm -2, -3 rồi đẩy lên, không còn dừng với câu "có commit mà máy này không có, TISA BOT không ghi đè".
- **TISA BOT không còn biến mất (lỗi 404) sau khi cập nhật.** Trên VPS ổ đĩa chậm, Watchtower hết giờ đúng lúc đang xoá container cũ, bỏ dở mà không dựng bản mới, nên TISA BOT mất hẳn khỏi Docker cho tới khi Redeploy.
- Thêm container canh gác `tisa-guard`: thấy TISA BOT biến mất hay bị dừng giữa chừng quá 2 phút là tự dựng lại (lên đúng bản mới) hoặc bật lại. TISA BOT anh tự bấm dừng thì nó để yên.
- Mỗi lần cập nhật bằng nút bấm có 30 phút thay vì 10. Cần Redeploy một lần để nhận file compose mới.
- **Lấy câu gợi ý rồi xóa bớt thì gợi ý không còn mất.** Trước đây nhấn Tab lấy cả câu (hoặc lấy hết từng chữ) rồi xóa vài chữ là phần gợi ý biến mất luôn. Giờ xóa đến đâu, phần còn lại hiện xám lại đến đó. Xóa hết ô chat thì câu gợi ý hiện lại nguyên vẹn. Gợi ý chỉ mất khi bạn gửi tin.
- **Máy tính cũng có dấu > sau câu gợi ý.** Trước đây dấu này chỉ hiện trên điện thoại. Giờ trên máy tính bấm chuột vào dấu **>** ngay sau chữ cuối là lấy cả câu.
- **Bấm dừng ghi âm phản hồi ngay.** Thanh ghi chuyển sang "Đang viết lại câu cho đúng" ngay khi bấm, và đoạn ghi âm được gửi đi nghe lại luôn chứ không chờ trình duyệt đóng mic xong.
- **Bước viết lại câu nhanh hơn nhiều.** Lớp sửa từ trước đó có lúc tốn vài giây, nay chỉ vài phần trăm giây. Model nhanh không còn "nghĩ" hết lượt rồi trả câu rỗng, máy chạy gói đăng ký thì model chính nghĩ ở mức thấp nhất cho việc này.
- **Đọc dài không còn mất chữ.** Câu dài hơn khoảng 2.000 ký tự trước đây bị cắt cụt sau bước viết lại, nay giữ đủ từng chữ.
- **Bớt đổi nhầm chữ thường thành tên riêng.** "đã viết" không còn thành "TISA", "cần và" không còn thành "Canva".
- **Thẻ OpenAI Compatible và Claude Compatible không còn báo "Chưa lấy được danh sách model" oan.** TISA BOT đọc được danh sách model của nhiều kiểu cổng hơn, và Base URL gõ thiếu `/v1` thì tự tìm đúng địa chỉ. Máy nâng cấp từ bản cũ cũng tự hiện lại model.
- **Tên model bạn tự gõ luôn nằm trong bảng chọn**, kể cả khi cổng có danh sách riêng hoặc tạm thời không trả danh sách.
- **Khi thật sự không có danh sách, bảng chọn nói rõ vì sao** (sai địa chỉ, key bị từ chối, cổng không báo model) và có lối bấm sang trang Models để sửa. Sửa xong mở lại là thấy ngay, không phải chờ vài phút.
- **Key vừa kết nối không còn tự biến mất** nếu đúng lúc đó TISA BOT đang tải danh sách model của một thẻ khác.
- **Nhóm không còn hiện hồ sơ của một người.** Trước đây ô ghi chú của một nhóm Zalo hiện hồ sơ của người nhắn đầu tiên trong nhóm, như thể cả nhóm là một khách. Giờ nhóm có ghi chú riêng của nhóm, sửa ở đó không đụng tới hồ sơ của ai.
- **Bình luận Facebook, Instagram, Threads không được ghi hồ sơ.** Người bình luận không nhắn tin cho shop, nên A.I. không ghi hồ sơ từ các luồng bình luận nữa, và bot trả lời công khai cũng không mang theo hồ sơ học từ chat riêng.
- **TISA BOT không còn đứng hình khi đĩa của máy chủ trả lời chậm.** Trên VPS, mỗi lần đĩa chậm vài giây là mọi trang, bot và kết nối cùng đứng theo, có lúc máy chủ bị coi là sập. Nặng nhất ngay sau khi cập nhật. Giờ các việc chạy liên tục (kiểm tra đăng nhập, hub MCP, bot, link chia sẻ) không còn phải chờ đĩa.
- **Cập nhật bản Docker xong, các nguồn MCP không phải tải và cài lại từ đầu.** Phần đã cài được giữ trên ổ dữ liệu, nên máy chủ không bị dồn việc lúc vừa khởi động lại. Riêng lần cập nhật lên bản này vẫn cài lại một lần cuối.
- **Lúc khởi động, TISA BOT mở các nguồn MCP theo từng nhóm nhỏ** thay vì tất cả cùng lúc, để máy chủ nhỏ không bị quá tải.
- **Đang xem trang Nhiệm vụ không còn bị khựng định kỳ.** Cứ 30 giây (5 giây khi có việc đang chạy) trang lại vẽ lại toàn bộ danh sách dù không có gì mới, làm màn hình đứng một nhịp và mất chỗ đang rê chuột. Giờ không có gì đổi thì không vẽ lại.
- **Dùng Team nhiều không còn làm rớt kết nối tới máy chủ.** Team càng chạy nhiều lượt thì mỗi lần mở team TISA BOT càng lâu mới cộng xong mức dùng của nó: team vài nghìn lượt mất cả phút, trang chờ quá 30 giây thì báo mất kết nối rồi gọi lại, và cả máy chủ đứng theo. Giờ việc này nhanh hơn khoảng 100 lần và không bao giờ chạy chồng lên nhau.
- **Mỗi lần gọi model không còn làm máy chủ khựng.** Sổ mức dùng từng giữ một dòng cho mỗi lần Team gọi model suốt 30 ngày và bị ghi lại toàn bộ sau mỗi lần gọi, nên file phình tới hàng chục MB, chat thường cũng chậm theo. TISA BOT tự dọn file này lúc khởi động, số liệu mức dùng giữ nguyên.
- **Bộ cài Windows không còn bị thay file mới vô cớ.** File `TISA-BOT-Setup.exe` chưa ký số nên trình duyệt và trình diệt virus chỉ nhận ra nó qua mã băm. Trước đây cứ sửa script cài (kể cả script của Linux) là file bị thay, và mỗi lần thay thì Edge lại báo "isn't commonly downloaded" từ đầu. Giờ file chỉ đổi khi chính bộ cài thay đổi.
- **Hướng dẫn cài nhanh có thêm cách gỡ khi bị chặn.** Thêm bước bấm **Keep anyway** khi Edge hoặc Chrome không chịu lưu file, và một dòng lệnh cài không cần file exe cho máy bị trình diệt virus hoặc Smart App Control chặn.
- **Dùng lâu không còn ì dần.** Mỗi lần mở trang Trò chuyện, trình duyệt giữ lại cả trang cũ trong bộ nhớ, đổi trang càng nhiều máy càng nặng. Giờ trang cũ được dọn sạch.
- **Màn Đồ thị hết khựng.** Đồ thị nhớ chỗ các chấm đã nằm nên lần mở sau hiện ngay, không tính lại từ đầu (bộ não 2.600 ghi chú: quãng đứng hình dài nhất từ hơn 1 giây xuống khoảng 0,2 giây). Chấm vừa rê qua cũng không còn sáng mãi và vẽ liên tục sau khi chuột đã rời đi.
- **Vòng sửa xung đột chạy được trên máy chưa khai tên và email cho git.** Trên máy chủ mới hoặc trong Docker, lệnh gộp nhánh của AI dừng ngay với lỗi `empty ident name`. Giờ mỗi repo gắn vào chat có sẵn danh tính, là tài khoản GitHub anh đã kết nối.
- **Commit do AI tự tạo trong repo đó giờ đứng tên giống commit của TISA BOT.** Nếu anh đã tự khai tên và email riêng cho repo thì TISA BOT giữ nguyên.
- **Bộ kiểm tra tự động xanh trở lại.** Hai bản cập nhật GitHub vừa rồi vào cùng lúc làm một bài kiểm tra báo đỏ sai; bài đó đã được viết lại. Cách TISA BOT chạy không đổi gì.
- **PR của repo riêng tư bị xung đột giờ được TISA BOT tự gộp lại.** Trước đây vòng sửa xung đột dừng ngay ở bước tải nhánh chính, vì phần chạy lệnh của AI không có quyền vào GitHub. Giờ TISA BOT tự tải nhánh chính về trước, AI chỉ còn việc gộp và giải quyết xung đột.
- **Mất mạng lúc đó thì TISA BOT chờ rồi thử lại.** Vòng sửa không còn bị tiêu mất vào một lần gộp chắc chắn hỏng; thẻ repo ghi rõ lý do đang chờ.
- **Gắn repo riêng tư vào chat không còn hỏng khi nhánh chính có file mới.** Trước đây repo riêng tư chỉ gắn được lần đầu; hễ nhánh chính có thêm hoặc đổi file là chat mới báo `could not fetch ... from promisor remote`.
- **Đổi nhánh gốc của chat cũng chạy với repo riêng tư.** Cùng lỗi đó làm nút Đổi nhánh và việc tạo lại nhánh sau khi merge thất bại; cả hai đã được sửa.
### Cải thiện
- **Thêm repo mới ngay trong tài liệu của project.** Danh sách chọn repo GitHub ở project, trợ lý và hộp tạo team nay có dòng "+ Thêm repository trên GitHub" như trong hội thoại. Cấp thêm repo trên GitHub xong quay lại là danh sách tự hiện repo mới, không cần tải lại trang.
- **Luật lõi TISA BOT gửi cho model nay viết bằng tiếng Anh, một bản cho mọi ngôn ngữ.** Gồm luật từng kênh chat, chế độ tiết kiệm token, vai TISA Core, đường dẫn agent và skill. Trước đây khoảng một phần tư lời dặn là tiếng Việt và nó kéo câu trả lời về tiếng Việt; nay TISA BOT giữ đúng thứ tiếng bạn viết. Bạn vẫn chat tiếng Việt như cũ, TISA BOT vẫn trả lời tiếng Việt.
- **Lời dặn ngắn hơn về số token**, nên mỗi lượt chat nhẹ hơn một chút.
- **TISA BOT trả lời bằng đúng thứ tiếng bạn viết, với mọi ngôn ngữ, giống Claude hay ChatGPT.** Ô ngôn ngữ ở Cài đặt nay chỉ đổi giao diện, chatbot cũng luôn trả lời khách bằng tiếng của khách. Muốn luôn nhận một thứ tiếng thì dặn TISA BOT một lần; ai đã ghim ngôn ngữ trả lời từ trước được chuyển thành một câu trong hồ sơ, không mất.
- **ChatGPT chờ TISA BOT lâu hơn trong cùng một lượt trả lời** (tới khoảng 10 phút) thay vì bỏ cuộc sau nửa phút, và biết TISA BOT đã làm bao lâu.
- **Chỉ bạn ra lệnh mới sửa được.** Lượt tự thức của Auto và bot nói với khách chỉ được đề xuất. Các câu dặn cũ mâu thuẫn trong prompt đã được thay cho khớp.
- **Bật Auto hỏi lại một lần**, nói rõ là trao toàn quyền. Câu cũ "Auto không phải Toàn quyền" đã thay bằng câu đúng với cách chạy mới.
- **Các dòng hệ thống TISA BOT gắn dưới câu trả lời không còn xưng cứng "mình".** Dòng theo dõi việc chạy nền, đính chính lời hẹn, nhắc trí nhớ, link không thấy file viết không đại từ, nên không lệch với cách xưng hô đã chọn.
- **File, thư mục và link gộp một tab "Tài liệu".** Phân biệt bằng biểu tượng, nút Thêm tài liệu có cả dán link, khung gọn hơn một tab.
- **Bỏ nút chữ "Tab" ở hàng nút dưới ô chat.** Dấu **>** đã làm việc đó, nên hàng nút chỉ còn các nút vốn có (thêm file, model, mức suy nghĩ, mic, gửi). Phím Tab trên bàn phím vẫn lấy câu gợi ý như cũ.
- **Duyệt nhiều nhóm chờ cho bot bằng một lần bấm.** Trong bảng Tình trạng của bot, mỗi nhóm hay người đang chờ là một ô tích, có **Chọn tất cả** và một thanh nút **Cho phép** / **Bỏ qua** chung. Trước đây chín nhóm chờ là chín lần mở bảng rồi bấm.
- **Bảng không tự đóng sau mỗi lần bấm.** Duyệt xong một loạt, bảng ở lại với những dòng còn chờ. Nút ghi sẵn số dòng đang tích, ví dụ "Cho phép (9)".
- **Dễ đọc hơn trên điện thoại.** Tên nhóm chữ to, cả dòng bấm được, thanh nút luôn nằm trong tầm ngón tay dù danh sách dài.
- **Câu gợi ý không còn biến mất khi bạn gõ chữ đầu tiên.** Gõ theo câu gợi ý thì phần còn lại vẫn hiện màu xám ngay sau chữ bạn gõ, kể cả khi gõ không dấu hay đang gõ dở một chữ. Nhấn **Tab** để lấy hết phần còn lại, nhấn **mũi tên phải** để lấy từng chữ. Trên điện thoại không còn nút Tab ở hàng nút: có một dấu **>** nhỏ ngay sau chữ cuối của câu gợi ý, chạm vào là lấy câu đó.
- **Gõ khác đi thì TISA BOT đoán nốt câu.** Dừng gõ một nhịp, TISA BOT viết tiếp phần còn lại của câu bạn đang gõ theo ý mới của bạn, giống gợi ý chữ trên iPhone. Máy có key API (Groq, OpenAI...) thì gần như tức thì. Chỉ dùng gói thuê bao thì chậm vài giây và tối đa 5 lần mỗi lượt, để không ăn vào hạn mức.
- **Câu gợi ý dài hiện đủ.** Ô chat tự cao lên để thấy cả câu, trên điện thoại không còn bị cắt giữa dòng. Áp dụng cho chat chính và trang Nhóm.
- **Trang Nhiệm vụ mở mượt hơn hẳn.** Trước đây mỗi lần mở, trang vẽ lại toàn bộ danh sách hai lần và dựng cả bản máy tính lẫn bản điện thoại. Giờ chỉ vẽ một lần, đúng bản đang hiện. Với 170 việc trên máy chậm: quãng đứng hình từ 0,45 giây xuống khoảng 0,1 giây, trên điện thoại gần như không còn.
- **Trang Cộng sự mở nhanh hơn.** Danh sách trợ lý trước đây bị vẽ lại năm lần mỗi lần mở trang, nay chỉ một lần, nên rê chuột và cuộn không còn bị giật lúc trang vừa hiện.
- **Gõ tìm việc không còn trễ chữ.** Danh sách lọc theo sau khi bạn ngừng gõ một nhịp ngắn, thay vì vẽ lại sau từng chữ.
- **Mở TISA BOT nhanh hơn rõ rệt.** Màn "Đang khởi động TISA BOT…" trước đây luôn đứng đủ 4 giây trên máy có hơn một trang cuộc chat, dù dữ liệu đã về sau khoảng 1 giây. Giờ dữ liệu về là app hiện ngay. Đồ thị bộ não cũng không còn được dựng ngầm khi bạn mở thẳng vào Trò chuyện hay Cộng sự.
- **Để yên thì TISA BOT gần như không tốn máy.** Vành của linh vật, nền sao và đồ thị không còn bắt trình duyệt làm việc 60 lần mỗi giây khi không có gì thay đổi, nên cuộn và gõ mượt hơn, máy đỡ nóng.
### Bảo mật
- **Chia sẻ file hay lịch cho người khác cần Toàn quyền.** Cũng vậy với xoá cả một tab, danh sách việc hay nhóm danh bạ, tạo bộ lọc Gmail và xuất bản Apps Script. Ở mức Chỉ đọc, TISA BOT không chép được file Drive hay ghi dòng vào Sheets.
- **Hook và cấu hình git trong repo không còn đọc được token GitHub.** Trước đây một hook nằm trong bản clone (ví dụ do `npm install` kiểu husky cài, hoặc do model tạo) chạy đúng lúc TISA BOT tải về hay đẩy code và thấy được token. Giờ các lệnh git có mang token của TISA BOT bỏ qua mọi hook của repo.
- **Token chỉ đi tới đúng repo trên GitHub.** Nếu cấu hình git của bản clone bị sửa để lái kết nối sang nơi khác (đổi `origin`, `insteadOf`, proxy), TISA BOT dừng lại và nói rõ dòng nào cần gỡ, thay vì gửi token đi.
- **Thay đổi cần biết:** hook `pre-push` của repo không còn chạy khi TISA BOT đẩy code (bộ kiểm tra của TISA BOT và CI vẫn chạy như cũ). Repo dùng Git LFS: file LFS mới tạo trong chat chưa được tải lên theo lần đẩy.

## [0.551.12] - 2026-11-15
### Thêm mới
- **Bộ TISA:** Giao dự án: khung kết quả của việc nay có danh sách tệp đội đã làm (Excel, Word, PDF, ảnh, báo cáo...) với nút "Mở file" mở thẳng bằng ứng dụng trên máy anh và nút "Hiện trong Finder". Phần nào nhắc tên tệp thì tệp hiện ngay dưới kết quả phần đó; tab Tổng hợp hiện toàn bộ tệp của việc. Danh sách tự cập nhật mỗi khi một phần báo xong.

## [0.551.11] - 2026-11-15
### Thêm mới
- **Bộ TISA:** Gọi AI bằng giọng: ra lệnh xong mà cuộc gọi bị ngắt (đóng tab, mic tự ngủ, mạng chớp) thì việc đang làm không còn bị huỷ giữa chừng nữa. AI tiếp tục làm ở nền, làm xong tự gửi kết quả vào khung chat.

## [0.551.10] - 2026-11-15
### Thêm mới
- **Bộ TISA:** Nói chuyện bằng giọng: nói xong là làm thật. Trước đây AI giọng hay trả lời "để em kiểm tra nhé" rồi dừng ở câu nói, không ai đi làm. Nay hễ anh ra lệnh làm gì hoặc hỏi số liệu thật, hoặc AI vừa hứa làm, TISA BOT tự giao ngay cho bộ não chính chạy thật (có công cụ, có số liệu), kết quả hiện trong khung chat. Việc đăng bài, chạy quảng cáo, gửi tin, tiêu tiền vẫn dừng chờ anh duyệt.

## [0.551.9] - 2026-11-15
### Thêm mới
- **Bộ TISA:** Giao dự án: thêm trang "Cần anh" ngay đầu menu, gom mọi thứ đang chờ anh quyết của mọi việc vào một chỗ: phần chờ duyệt, việc cần anh làm hoặc nộp dữ liệu, việc bị kẹt, tin đội trả lời. Mỗi dòng có thời gian chờ (đổi màu khi chờ quá 4 giờ, quá 1 ngày) và nút xử lý ngay: Duyệt, Sửa lại (gõ góp ý hoặc chọn nhanh "Ngắn gọn hơn", "Thêm số liệu"...), Làm tiếp việc kẹt, Nộp dữ liệu, Trả lời.
- **Bộ TISA:** Việc đứng im quá 30 phút hoặc bị kẹt nay tự hiện trong danh sách Cần anh kèm lý do, bấm Làm tiếp là đội chạy lại, không cần mở từng việc để tìm.

## [0.551.8] - 2026-11-15
### Thêm mới
- **Bộ TISA:** Sửa lỗi bấm vào tên tệp trong chat báo không xem được: AI hay ghi tên tệp trần hoặc thiếu thư mục con, nay TISA BOT tự dò theo tên trong bộ não và mở đúng tệp (tệp mới nhất, ưu tiên đúng thư mục nếu có).
- **Bộ TISA:** Giao dự án: các nút nguy hiểm (Kết thúc việc, Xóa việc) gom vào menu "⋯" ở chân khung việc để khỏi bấm nhầm; nút chính còn Tạm dừng, Duyệt, Yêu cầu sửa lại. Đổi tên "Hướng dẫn từng bước" thành "Chỉ em từng bước" và "Nhờ Claude làm giúp" thành "Nhờ Claude thao tác trên máy" cho dễ hiểu.

## [0.551.7] - 2026-11-15
### Thêm mới
- **Bộ TISA:** Khung trao đổi trong việc đã giao trả lời nhanh hơn nhiều: tin hỏi đi thẳng vào phiên chat của nhân sự (chữ chảy dần), kèm sẵn việc, phần việc và trao đổi gần đây, thay vì đánh thức Tâm chạy cả quy trình. Lệnh của anh thì nhân sự đặt phần về "đang làm" rồi làm ngay.
- **Bộ TISA:** Thanh tiến độ không còn báo "Hoàn thành" khi anh vừa giao thêm việc mà đội chưa làm xong, và ghi rõ "Đã làm xong, chờ anh xem và duyệt" khi việc đang chờ duyệt.
- **Bộ TISA:** Lấy số quảng cáo qua MCP: không còn lỗi "chưa trả số theo mẫu" khi kỳ dài. Số trả về dạng gọn, câu trả lời được giữ tới 60.000 ký tự, và nếu vẫn bị cắt thì lấy phần còn nguyên và báo rõ.

## [0.551.6] - 2026-11-15
### Thêm mới
- **Bộ TISA:** Sửa lỗi khung chat trong việc đã giao và Chat nội bộ luôn báo "Chưa có tin nào": trang chỉ tải 500 tin cũ nhất nên tin mới không hiện. Nay tải 1.500 tin mới nhất, tin gửi và câu trả lời hiện đầy đủ.

## [0.551.5] - 2026-11-15
### Thêm mới
- **Bộ TISA:** Khung nhắn tin trong việc đã giao: tin chủ nhắn mà không ai trả lời (lượt xử lý chết vì khởi động lại hay lỗi) nay tự được gửi lại tối đa 2 lần; trạng thái tin hiện rõ "đang chuyển", "đang xử lý", "chưa gửi được".
- **Bộ TISA:** Việc đứng im hơn 20 phút mà lượt làm việc đã chết hoặc bỏ dở: cầu nối tự cho làm tiếp tối đa 2 lần rồi mới để chủ quyết định.
- **Bộ TISA:** Nhân sự phân biệt câu hỏi và LỆNH trong khung trao đổi: lệnh thì cập nhật kế hoạch và làm ngay, không chỉ trả lời. Thêm quy trình triển khai sau khi chủ duyệt: giao phần tới lượt, ghi người làm và hạn, tóm tắt 3 dòng (đã xong, đang làm, cần anh).
- **Bộ TISA:** Văn phòng: không còn tự nhảy từ 2D sang 3D. Chỉ đổi khi anh bấm chọn; thư viện 3D được nạp ngầm để bấm là vào ngay.
- **Bộ TISA:** Quản lý web: Web CRM có nút đặt link công khai (ví dụ tên miền riêng trỏ về CRM) để chạy demo trên mạng.

## [0.551.4] - 2026-11-14
### Thêm mới
- **Bộ TISA:** Trang Quảng Cáo, chế độ Tự động: thêm ô "Ý tưởng anh muốn chạy". Anh gõ ý tưởng, bấm một nút, trợ lý tự chọn cấu trúc và đối tượng, AI viết nội dung bài, rồi giao cho cộng sự dựng cả chiến dịch ở trạng thái tạm dừng để anh duyệt.
- **Bộ TISA:** Web CRM mặc định tự chạy và tự nối với TISA BOT khi mở máy (Hỏi nhanh, Đội Quân AI, chatbot ghi khách vào CRM). Anh bấm Tắt thì máy không tự bật lại, bấm Chạy thì bật lại.
- **Bộ TISA:** Bảng Đội Quân AI: bỏ hẳn chữ cũ còn sót ở thông báo nhận việc, tên công cụ và dữ liệu đã lưu, thay bằng TISA BOT.
- **Bộ TISA:** Khung nhắn tin trao đổi với nhân sự trong việc đã giao: khi đường nối bị ngắt giữa chừng lúc máy đang bận, trợ lý tự lấy lại câu trả lời từ phiên chat thay vì báo "chưa trả lời được".
- **Bộ TISA:** Lấy số quảng cáo qua MCP: lệnh nay dặn cộng sự lấy đủ mọi chiến dịch và nhóm (đọc hết các trang, gộp đủ), tự thử lại khi máy chủ báo lỗi tạm thời, và trang cảnh báo khi số MCP chỉ phủ ngắn hơn kỳ đang xem.

## [0.551.3] - 2026-11-13
### Thêm mới
- **Bộ TISA:** Sửa lỗi đồng bộ cộng sự với Đội Quân AI: hồ sơ trợ lý hệ thống không còn bị đưa lên bảng, và một cộng sự mà lõi chưa nhận không còn chặn việc thêm các cộng sự khác vào nhóm. Bộ cài Mac và Windows dựng lại đạt kiểm tra.
### Sửa lỗi
- **Mục Bộ phán xử luôn có trong menu "..." của thẻ bot.** Trước đây nó chỉ hiện khi bot ở chế độ Tự đánh giá, nên nhiều người tìm không thấy.
- **Bot chưa bật Tự đánh giá thì bảng nói rõ bộ phán xử đang nghỉ**, kèm nút Sửa để bật, thay vì một danh sách trống.

## [0.551.2] - 2026-11-13
### Thêm mới
- **Bộ TISA:** Quảng Cáo: nút "Lấy số thật qua MCP" cho người đã nối MCP quảng cáo (ví dụ Meta Ads) mà chưa nhập mã API. Bấm nút, cộng sự phụ trách quảng cáo đọc số qua MCP (chỉ đọc, không bịa số) rồi trang hiện lên Tổng quan, Chiến dịch và bảng chi tiết, ghi rõ lấy lúc nào và kỳ nào. Không đọc được (ví dụ chưa đăng nhập) thì trang báo lại lý do, không hiện số giả. Có mã API thì API được dùng trước.
### Sửa lỗi
- **Quy ước ở trang Hồ sơ giờ có tác dụng cả với câu trả lời đi đường tắt.** Bản 0.546.2 đã đưa hồ sơ vào các mức tiết kiệm, nhưng còn sót: lời chào, lời cảm ơn (ở mọi mức) và câu hỏi đơn giản ở mức Siêu tiết kiệm vẫn được trả lời mà không có hồ sơ, nên TISA BOT có thể xưng hô sai ngay ở câu chào đầu tiên.
- Câu trả lời tổng hợp từ dữ liệu vừa đọc (trên bộ não dùng API key) cũng theo hồ sơ.
- Hồ sơ trống thì không có gì thay đổi. Hồ sơ dài nhất (4.000 ký tự) làm một lượt đi đường tắt nặng thêm khoảng 1.400 token.

## [0.551.1] - 2026-11-12
### Thêm mới
- **Bộ TISA:** Nâng cấp lõi mới nhất: việc nền tự chọn model vừa đủ để tiết kiệm token; Zalo cá nhân đọc tin ngay, bot Zalo nhận được file PDF, Word, Excel; Chatbot thêm kênh WeChat; hồ sơ khách hàng tự ghi sau mỗi cuộc chat; một team chạy được nhiều việc cùng lúc, tạo team kèm tài liệu ngay từ đầu; ô chat tự nhảy số thứ tự; ghim thư mục trong cây bộ não; khung chat điện thoại gọn hơn; công cụ Facebook và Meta Ads không còn đưa token cho AI; cài trên Windows hiện tiến trình ngay trong cửa sổ Setup. Kết nối máy chủ MCP tự thêm bằng đăng nhập trình duyệt (ví dụ HeyGen) theo đúng chuẩn MCP nên hết lỗi Invalid redirect_uri. Chuyển máy chủ an toàn hơn: gói tạo từ chính máy này thì cảnh báo đỏ, phải tick xác nhận, có nút Khôi phục bản trước khi chuyển.
- **Bộ TISA:** Icon ứng dụng (Dock, màn hình chính, cài như app) đổi theo logo bạn tải lên. Menu thu gọn trên điện thoại và iPad chỉ còn nền và logo, hết chữ chồng lên nhau. Cộng sự tạo ở trang Cộng sự hiện đồng bộ ở Cài đặt đội, Văn phòng, Đội ngũ, và Tâm Tổng Quản tự xếp vào phòng hợp với công việc. Kết quả của từng nhân sự đúng phần việc của họ, hết báo cáo lặp lại nhau.
- **Bộ TISA:** Thẻ Quảng Cáo mới ở cột trái, dưới Chatbot: quản lý tài khoản Facebook, TikTok, Google Ads, bảng số liệu gộp (chi phí, kết quả, giá mỗi kết quả, doanh thu, ROAS) xem theo ngày, tuần, tháng, kiểm tra kết nối qua API hoặc MCP, gợi ý tối ưu, phiếu thiết lập quảng cáo (trợ lý tạo ở trạng thái tạm dừng, chờ bạn duyệt) và hỏi trợ lý bằng tiếng Việt. Trang chỉ đọc số liệu, không tự bật hay tiêu tiền. Nút Giao dự án khi thu gọn gọn hơn. Phần Thiết lập quảng cáo đi từng bước theo từng nền tảng: chọn mẫu chiến dịch (1 nhóm 1 bài, 1 nhóm 3 bài, 3 nhóm 3 bài), tải nhiều hình và video (mỗi video là một bài), dán nhiều nội dung, chọn nút kêu gọi, gợi ý đối tượng theo ngành, đối tượng tuỳ chỉnh và tương tự, bật tắt AI tự tối ưu, chế độ Tự động cho người chưa rành quảng cáo, tự quét kết nối API và MCP, và lịch chọn ngày.
- **Bộ TISA:** Màn đăng nhập mới: hai cột, khẩu hiệu "Tự động hoá doanh nghiệp của bạn với AI Agent", ô nhập có biểu tượng, nút Đăng nhập nổi bật, khu Quên mật khẩu gọn đẹp, dùng tốt trên điện thoại. Trang Quảng Cáo có bảng chỉ số chi tiết theo nhóm quảng cáo hoặc chiến dịch với 19 cột như Trình quản lý quảng cáo Meta (phân phối, ngân sách, chi tiêu, người tiếp cận, hiển thị, tần suất, chia sẻ, bình luận, tin nhắn, kết quả, CPM, CTR, lượt phát video 25 đến 100%), chọn bộ cột và tải CSV.
- **Bộ TISA:** Quảng Cáo thêm: chọn Fanpage hoặc kênh để quảng cáo (nhập một lần, lần sau chỉ chọn), chạy đúng bài đã đăng bằng cách dán link (có hướng dẫn lấy link), và bộ tạo bài quảng cáo bằng AI ngay trong trang: chọn tầng phễu 1 đến 5, loại bài (chữ, ảnh 1 tấm, nhiều tấm, video), AI viết nội dung theo công thức, tạo ảnh, dựng video từ ảnh cảnh, sửa lại từng phần ngay tại chỗ. Chế độ Tự động giờ vẫn chọn được mẫu 1-1-1, 1-1-3, 1-3-1, 1-3-3 và bật tắt từng chức năng AI. Tab Tài khoản và kết nối chuyển xuống cuối.
- **Bộ TISA:** Quảng Cáo thêm thao tác ngay trong trang: bật, tắt, đổi ngân sách từng chiến dịch hoặc nhóm quảng cáo (mặc định tắt, phải bật công tắc cho từng tài khoản; mỗi lần gõ đúng câu xác nhận, tăng ngân sách tối đa 50%, có nhật ký). Tab Tài khoản và kết nối có bảng tính năng cần gì, soạn báo cáo bằng chữ, cài báo cáo tự động, hướng dẫn kết nối từng bước cho Facebook, TikTok, Google và nút dán lệnh nhờ Claude làm cùng.
- **Bộ TISA:** Nút Giao cho cộng sự làm luôn trong Thiết lập quảng cáo: trang tự tìm cộng sự phụ trách quảng cáo (anh đổi người được), giao việc lên Bảng giao việc, theo dõi tiến độ ngay trong trang. Chiến dịch luôn tạo ở trạng thái tạm dừng, chờ anh duyệt.
- **Bộ TISA:** Mọi nút Hỏi trợ lý trong trang Quảng Cáo (gợi ý tối ưu, câu hỏi nhanh, hỏi tự do, hỏi về báo cáo) gửi thẳng cho cộng sự phụ trách quảng cáo, câu trả lời hiện ngay trong khung bên cạnh, hỏi tiếp được.
- **Bộ TISA:** Quảng Cáo, tạo bài bằng AI: viết bài, ảnh, video đều đọc bộ não của doanh nghiệp trước để đúng sản phẩm, giọng và quy tắc. Thêm tải ảnh tham chiếu (nhân vật, logo, hình sản phẩm) để ảnh ra đúng người, đúng logo, đúng sản phẩm. Cộng sự thiết kế đọc bộ não rồi viết chỉ đạo cho từng ảnh; có nút giao cộng sự thiết kế làm ảnh và giao cộng sự dựng video làm video, tiến độ hiện trong trang, ảnh và video cộng sự lưu xong được nhận về. Tạo ảnh chưa được thì báo rõ lý do và gợi ý giao việc thay vì báo lỗi chung.
- **Bộ TISA:** Quảng Cáo: độ dài video chọn nhiều mức hoặc tự nhập số giây (5 đến 180), số cảnh tự chia theo độ dài. Các lựa chọn AI tự tối ưu mặc định tắt hết. Phần Tài khoản và kết nối có nút Nhờ Claude làm giúp và nút Xem hướng dẫn thao tác từng bước (đọc mà tự làm được) cho API và MCP.
- **Bộ TISA:** Sửa lỗi Chuyển máy chủ: gói chuyển máy chỉ chứa DỮ LIỆU (bộ não, kết nối MCP, API, plugin, kỹ năng, Đội Quân AI, cài đặt), không còn mang chương trình TISA BOT của máy cũ sang. Trước đây máy cài từ bộ cài (không có git) bị gói cả chương trình, áp dụng xong chương trình máy mới bị thay bằng bản cũ. Máy mới giữ đúng bản đang cài, trang đối chiếu bản hai máy và dừng khi máy mới thấp bản hơn máy cũ. Gói cũ lỡ có kèm chương trình thì tự bỏ phần chương trình khi nhận.
- **Bộ TISA:** Chuyển máy chủ: máy mới nhận dữ liệu xong chạy THỬ ở local trước, máy cũ vẫn chạy bình thường, các kênh nhận tin trên máy mới tạm tắt để không trả lời trùng. Có bảng kiểm tra tự động và danh sách việc cần thử, thanh nhắc ở giao diện chính. Thử ổn mới hiện hướng dẫn trỏ Cloudflare (Tunnel hoặc VPS) về máy mới, rồi bấm Chính thức chuyển để bật lại các kênh. Chưa ổn thì máy cũ vẫn là máy chính.
- **Bộ TISA:** Cộng sự tạo ở ô Cộng sự tự hiện ở Văn phòng, Đội ngũ, Cài đặt đội của Đội Quân AI kể cả khi bảng đặt ngoài (Cloudflare); Tâm Tổng Quản tự xếp phòng. Hồ sơ có sẵn lúc bật lần đầu giữ nguyên, chỉ cộng sự tạo từ lúc đó mới lên bảng.
- **Team mới chạy việc tới khi xong.** Team tạo từ bản này không còn trần số lần trả lời và số bước của mỗi việc, nên việc không dừng giữa chừng để chờ bấm "Cho thêm lượt". Đổi lại một việc khó có thể tốn nhiều token hơn. Trần số lần trả lời mỗi ngày của team vẫn giữ nguyên, và việc vẫn tự dừng khi ra hai kết quả giống hệt nhau.
- Team đã có từ trước giữ nguyên giới hạn cũ. Muốn đổi thì vào Nâng cao, mục Giới hạn của team, tích "Không giới hạn" hoặc nhập lại con số.
- **Một team chạy được nhiều việc cùng lúc.** Trước đây mỗi team chỉ chạy một việc tại một thời điểm, nên việc của cộng sự này phải chờ việc của cộng sự kia xong. Giờ tối đa 3 việc chạy song song khi chúng thuộc các cộng sự khác nhau.
- **Việc của cùng một cộng sự vẫn chạy lần lượt** theo đúng thứ tự trong hàng chờ. Các việc do người điều phối lên kế hoạch cũng vậy.
- **Muốn việc sau chờ kết quả việc trước thì nói rõ trong yêu cầu.** Việc có câu như "sau khi ... xong", "lần lượt" hay "theo thứ tự" sẽ chờ mọi việc đứng trước nó xong rồi mới chạy, và không việc nào phía sau chen lên trước.
- **Tạo team kèm tài liệu ngay từ đầu.** Hộp Tạo team có thêm mục "Thêm tài liệu cho team (file, link)": tìm file có sẵn trong brain theo tên, tải file từ máy, hoặc dán link. Cộng sự trong team đọc được các tài liệu này từ tin đầu tiên.
- **Không phải tải lại file đã có trong brain.** Tab Thông tin của mỗi team có ô tìm file trong brain, bấm Thêm là xong. File vẫn nằm nguyên chỗ cũ, không tạo bản sao.
- **Agent chọn ChatGPT giờ chạy đúng bằng ChatGPT trong workflow nền giới hạn công cụ.** Trước đây các bước đó luôn chạy bằng Claude Code dù anh chị chọn ChatGPT. Bước chỉ được gọi đúng danh sách công cụ của nó, giữ mức quyền của việc, không có lệnh máy, web hay tác tử con.
- Máy chưa cài Codex thì bước đó vẫn chạy bằng Claude Code như trước, không báo lỗi.
- **Gửi tin Zalo dạng trả lời có trích dẫn.** Khi anh chị bảo TISA BOT trả lời đúng một tin cụ thể, tin gửi đi hiện kèm khung trích tin gốc, giống bấm "Trả lời" trong Zalo. Chỉ trích được tin chữ. Kết nối Zalo tự chuyển sang tisa-zalo 1.11.0 ở lần chạy tới.
- **Hồ sơ khách hàng.** Sau khi một cuộc chat riêng im khoảng 15 phút, model chạy nền tự ghi lại những gì cần nhớ về khách: tên, cách xưng hô, liên hệ, đang quan tâm gì, đã chốt gì, việc còn dang dở. Lần sau bot đọc hồ sơ này cùng 30 tin gần nhất nên không phải hỏi lại, kể cả khi khách quay lại sau vài tháng.
- **Ô ghi chú về khách thành mục Hồ sơ khách hàng** trong khung Thông tin của trang Hội thoại, dài tới 4.000 ký tự. Bạn vẫn sửa, ghi thêm hay xoá trắng được, phần bạn viết được giữ lại ở lần cập nhật sau.
- **Chatbot trả lời được trên WeChat.** Ở Chatbot, Thêm kênh có thêm **WeChat**: bot chuyên trách trả lời người theo dõi WeChat Official Account của bạn, mọi cuộc chat vào chung Hộp thư và bạn tiếp quản được như các kênh khác.
- **Cài đặt gọn.** Form hiện sẵn địa chỉ webhook và Token để dán sang WeChat; bên TISA BOT chỉ cần dán AppID và AppSecret. Bấm Kiểm tra là biết ngay IP nào cần thêm vào whitelist.
- **Cần biết:** WeChat chỉ cho tài khoản đã xác minh (hoặc tài khoản thử nghiệm) trả lời qua API, chỉ trong 48 giờ sau tin cuối của khách, gửi được chữ và ảnh. Hướng dẫn từng bước ở tài liệu 36.
- **Bot Zalo chính thức nhận được file.** Khi Zalo chuyển file cho bot, TISA BOT tải về và đọc luôn PDF, Word, Excel và file chữ, gửi kèm câu hỏi là trả lời theo file.
- **Không còn im lặng.** Zalo chưa có loại tin file riêng cho bot, nên khi Zalo không kèm nội dung thì bot nói thẳng là chưa nhận được và nhờ gửi ảnh chụp hoặc dán chữ. Trước đây bot im.
- **Ghim thư mục lên đầu cây Vault.** Bấm nút ba chấm của thư mục rồi chọn "Ghim lên đầu". Thư mục nằm sâu bên trong cũng ghim được, không phải mở từng tầng để tới nó nữa.
- **Thư mục luôn mở sẵn.** Cũng trong menu đó, chọn "Luôn mở sẵn" thì mỗi lần mở TISA BOT thư mục ấy đã xổ ra, ví dụ thư mục wiki.
- **Lưu theo từng brain, trên máy chủ.** Điện thoại và máy tính thấy cùng một cây, bản chạy trên VPS cũng dùng được. Đổi tên thư mục trong TISA BOT thì ghim vẫn đi theo.
- **Ô chat tự nhảy số thứ tự.** Dòng trên là `1. ...` thì xuống dòng sẽ có sẵn `2. `, giống trong Claude. Xuống dòng là Enter trên điện thoại, Shift+Enter trên máy tính (Enter trên máy tính vẫn là gửi). Có ở chat chính, Nhóm, Hội thoại và ô chạy thử chatbot.
- Xuống dòng lần nữa ở mục còn trống thì số tự mất để kết thúc danh sách. Chèn một dòng vào giữa thì các số bên dưới tự tăng theo.
- **Nút "Đúng trợ lý cũ, xác nhận tất cả" theo gói** trên trang Cộng sự. Khi TISA BOT vẫn phải hỏi về nhiều trợ lý của cùng một gói, bấm một lần là xong, không phải mở từng thẻ.
- **Bấm tên file TISA BOT tạo ngoài brain để mở ngay.** Ví dụ một bài giảng nằm trong ~/Documents. Trước đây khung chat chỉ hiện tên file như chữ thường. Giờ đường dẫn đầy đủ thành link, bấm vào là file mở bằng ứng dụng mặc định trên máy, như khi nhấp đúp trong Finder.
- Link chỉ hiện khi bạn dùng TISA BOT ngay trên máy đang chạy nó. Trên VPS, qua tên miền hoặc trong Docker, đường dẫn vẫn là chữ như cũ để bạn sao chép. Link chỉ mở file trong thư mục người dùng. Chương trình và script không được chạy, TISA BOT chỉ mở thư mục chứa chúng. Cảm ơn mminhthu0304-gif đã đóng góp phần này.
- **Hộp thư báo khi câu bot trả lời chưa tới khách trên Zalo cá nhân.** Trước đây câu bot soạn xong là hiện trong Hộp thư như đã gửi, dù Zalo từ chối hay gửi hết giờ. Giờ tin gửi được thì không hiện gì thêm. Tin chưa gửi được, tin chưa rõ kết quả hoặc tin bị bỏ vì khách nhắn thêm sẽ có một dòng nhỏ ngay dưới, kèm lý do. Tin kẹt ở trạng thái đang gửi quá 5 phút tự chuyển thành chưa rõ kết quả. Cảm ơn hwangrin đã đóng góp phần này.
- **Kết quả tool lớn không còn bị cắt mất phần giữa.** TISA BOT cất bản đầy đủ, đưa cho model phần gọn kèm mã tham chiếu, và model đọc lại đúng phần nó cần. Báo cáo hết thiếu đơn, lại tốn ít token hơn trên mọi bộ não.
- **Tính bằng code, không nhẩm.** Tool `tisa_query` tự lật hết các trang rồi cộng, đếm, xếp hạng bằng SQL chỉ đọc. Model lớn hay nhỏ đều ra cùng một con số.
- **Trinh sát bằng model nền.** Việc đọc nhiều nguồn có thể giao cho model việc nền (`tisa_scout`), chỉ kết luận quay về khung chat. Trinh sát chỉ đọc, không gửi hay tạo gì.
- **Việc định kỳ nhớ cách lấy số.** Sau hai lần chạy giống nhau ở hai ngày khác nhau, TISA BOT tự lấy sẵn dữ liệu cho lần sau. Chưa chắc về ngày tháng thì chạy như cũ.
- **Lịch nhắc chạy việc nay gửi kèm ảnh nó vừa tạo.** Báo cáo định kỳ dạng ảnh (quảng cáo, doanh số theo mẫu cố định) trước đây chỉ tới Zalo Bot và Telegram phần chữ, còn ảnh nằm lại trong brain. Giờ ảnh có trong câu trả lời và được tạo trong đúng lượt chạy đó sẽ đi cùng, tối đa 4 ảnh mỗi lượt.
- Zalo Bot chỉ nhận ảnh, nên PDF hay bảng tính vẫn như cũ. Ảnh gửi lỗi không làm hỏng lượt nhắc: phần chữ vẫn tới.
- **Công cụ hay dùng được ghim sẵn theo từng brain.** Khi brain đấu nhiều nguồn, công cụ phải "tìm rồi mới gọi", tốn thêm một vòng mỗi lần dùng. Giờ TISA BOT tự đếm công cụ nào mỗi brain gọi nhiều nhất và ghim sẵn vài cái (mặc định tối đa 4, TISA Core tự nới tới 8 khi cần): công cụ đã ghim được gọi thẳng. Việc nền như loop được lợi nhiều nhất vì trước đây lần nào cũng phải tìm lại. Không phải cài gì, có thông báo ở chuông khi ghim.
- **Xem và tắt bằng lời.** Hỏi TISA BOT "đang ghim công cụ nào" để xem danh sách kèm số lượt gọi thẳng và số lượt còn phải tìm. Nói "đừng ghim công cụ nữa" để tắt.
- **TISA Core giữ một vòng cải tiến chung.** Phần nào của TISA BOT muốn tự điều chỉnh thì đăng ký một "núm chỉnh" với TISA Core. Vòng dời núm theo cùng một cách: mỗi lần một bước, trong khoảng cho phép, nhiều nhất một lần mỗi ngày, có ghi lý do, có thông báo ở chuông và hoàn lại được bằng lời. Vòng này chỉ là mã, không gọi model và không chạm vào lượt chat.
- **Tự học tự chỉnh ngưỡng mở mẻ.** Khi phần lớn các mẻ học gần đây không rút ra được gì (thường gặp khi bạn hay hỏi nhanh một hai câu), TISA Core tự nâng số lượt cần có trước khi mở một mẻ; các mẻ có ích trở lại thì tự hạ xuống. Lượt chưa đủ ngưỡng vẫn nằm chờ và được học cùng các lượt sau.
- **Dặn TISA BOT nên học thế nào, bằng lời.** Nói "đừng ghi doanh thu từng ngày thành ghi nhớ" hay "chỉ ghi nhớ quyết định đã chốt": TISA Core giữ thành một bài học và mọi mẻ tự học đọc nó trước. Xem và thu hồi như bài học của mọi trợ lý.
- **Model việc nền có chế độ Tự động, và là mặc định.** Trước đây việc nền chạy bằng model mặc định của nhà cung cấp, trên gói thuê bao thường là model mạnh và tốn nhất. Giờ TISA BOT dùng nhà cung cấp của MAIN và chọn sẵn hai model từ danh sách của chính nhà đó: model nhẹ cho việc TISA BOT tự làm (tự học, gợi ý câu tiếp theo, chấm điểm), model bậc giữa cho việc bạn giao chạy nền (nhắc hẹn, loop, Kanban). Trang Models ghi rõ hai model đang dùng. TISA BOT chỉ chọn lại khi danh sách model của nhà đó thay đổi, và báo ở chuông mỗi lần chọn.
- **Mỗi việc nền tự tìm model vừa đủ cho nó.** Hai model trên chỉ là điểm xuất phát. Từng nhắc hẹn, từng loop, từng loại việc Kanban và tự học có một bậc riêng: hỏng vì model yếu thì lần chạy sau leo một bậc, chạy tốt nhiều lần liền thì thử xuống một bậc, không được thì quay lại. Lỗi do hết hạn mức, mất đăng nhập hay đứt kết nối không làm đổi model. Mỗi lần đổi có thông báo ở chuông kèm lý do.
- **Chỉnh việc nền bằng lời, không có ô cài đặt.** Nói "tiết kiệm token giúp anh", "việc gửi báo cáo phải thật chắc", "báo cáo sáng nay sai rồi" hay "việc nền đang chạy model gì": TISA BOT ghi ý định của bạn cho mọi việc hoặc riêng một việc, điều chỉnh theo, và hoàn lại được một lần đổi model khi bạn bảo.
- **Model bạn tự chọn thì TISA BOT không bao giờ đổi.** Bấm Đổi model ở khối Model việc nền và chọn một model: nó giữ nguyên. Muốn về Tự động thì chọn dòng "Tự động (khuyên dùng)" ở đầu danh sách. Máy đã cài: model nền còn nguyên cấu hình mặc định thì chuyển sang Tự động, bạn từng chọn model khác thì giữ nguyên.
- **Việc TISA BOT tự làm tự nghỉ khi gói sắp hết hạn mức.** Cửa sổ 5 giờ của gói đã dùng từ 80% thì tự học và gợi ý câu tiếp theo chờ tới lúc hạn mức mở lại, phần còn lại để dành cho chat của bạn.
- **Claude Agent SDK tự cập nhật.** Cùng công tắc "Tự cập nhật Claude Code mỗi ngày" ở trang Models nay giữ luôn gói Claude Agent SDK ở bản mới nhất trong dòng của nó. TISA BOT chỉ lấy bản đã ra ít nhất ba ngày, chạy thử trước khi giữ, lỗi thì tự lùi về bản cũ. Bản mới dùng từ lần khởi động lại kế tiếp. Bản Docker vẫn nhận theo ảnh TISA BOT mới.
### Sửa lỗi
- **ChatGPT (hay Claude, Grok) mất đăng nhập thì TISA BOT tự chuyển sang model khác đã kết nối.** Trước đây chỉ khi hết lượt mới chuyển, còn mất đăng nhập thì lượt nào cũng báo lỗi cho tới khi anh đăng nhập lại.
- **Áp dụng cho cả bot trả lời khách và trợ lý có model riêng.** Bot hay trợ lý đặt model ChatGPT sẽ trả lời bằng model chính trong lúc ChatGPT chưa đăng nhập lại, khách không còn gặp lượt hỏng.
- **Có báo rõ để anh biết.** Khung chat hiện dòng "Đang dùng ... vì ChatGPT mất đăng nhập", ô chọn model gắn nhãn "Mất đăng nhập", và chuông có một thông báo nhắc đăng nhập lại ở trang Models. Đăng nhập xong là dùng lại model cũ ngay.
- **Team không còn chặn gửi ảnh sau một thời gian dùng.** Mỗi team giữ tối đa 50 tài liệu, và mỗi ảnh gửi vào team chiếm hai chỗ (ảnh và bản mô tả ảnh cho cộng sự đọc). Sau khoảng 25 lần gửi ảnh là đầy, và từ đó file gửi thêm bị bỏ đi mà không báo gì. Giờ khi đầy, ảnh cũ nhất và bản mô tả của nó rời danh sách tài liệu để nhường chỗ cho ảnh mới. File vẫn còn trên máy và tin nhắn vẫn còn trong chat.
- **Tài liệu bạn tự gắn không bao giờ tự rời danh sách.** Bảng giá, hợp đồng, file PDF và bản chữ của nó vẫn giữ nguyên.
- **File không vào được team thì có báo.** Khi danh sách đã đầy toàn tài liệu bạn tự gắn, TISA BOT nói rõ lý do và chỉ chỗ gỡ bớt, thay vì im lặng bỏ file.
- **Việc nền chạy dự phòng bằng đúng model anh chị chọn trên thẻ.** Trước đây lựa chọn đó bị bỏ qua: khi model việc nền hết lượt và việc rơi sang Claude Code, nó chạy model mặc định của CLI, thường là model tốn hạn mức nhất. Thẻ chưa chọn model thì vẫn chạy như cũ.
- **Cài bằng root trên Linux không còn làm Claude lỗi "exit code 1".** Bản cài mới tự tạo tài khoản thường `tisa` và chạy TISA BOT dưới tài khoản đó, vì Claude Code từ chối mức Toàn quyền dưới root.
- **Bản clone nằm trong `/root` được chuyển sang `/opt`**, vì tài khoản khác không vào được `/root`. Trình cài báo rõ nơi mới.
- **Máy đã cài từ trước giữ nguyên tài khoản cũ.** `./update.sh` chạy bằng root vẫn dùng như thường.
- **Lỗi "SDK engine: ProcessError... Check stderr output for details" giờ nói rõ lý do.** Khi Claude Code thoát trước khi trả lời, khung chat hiện đúng câu nó in ra thay vì một dòng không biết làm gì tiếp.
- **Ba ca hay gặp có luôn cách xử lý:** TISA BOT chạy bằng tài khoản root, cấu hình nguồn dữ liệu (MCP) hỏng, và Claude Code trên máy quá cũ.
- **Vòng hạn mức hết đỏ ngay khi gói dùng lại được.** Trước đây anh chị đặt lại gói trên trang nhà cung cấp rồi mà vòng vẫn đỏ 100% và việc TISA BOT tự làm vẫn nghỉ, cho tới giờ làm mới cũ.
- **Đọc được giờ mở lại có ghi cả năm.** Câu báo kiểu "try again at Nov 13th, 2026 3:32 PM" trước đây bị coi là không rõ lúc nào mở lại, nay hiện đúng giờ.
- **Việc nền bị từ chối vì hết lượt cũng làm vòng hạn mức đỏ.** Trước đây chỉ lượt chat mới ghi nhận, nên việc nền dùng cạn gói mà vòng vẫn xanh.
- **Kiểm tra Messenger phát hiện được webhook không truy cập được.** Trước đây mọi dòng đều báo ổn trong khi đường HTTPS đã chết, nên bot không trả lời mà không rõ vì sao.
- **Link nhanh đổi địa chỉ thì Sửa tự động trỏ lại đúng địa chỉ đang chạy**, giữ nguyên đường dẫn nhận tin, và chỉ lưu sau khi Meta xác minh thành công.
- **Quy ước ghi ở trang Hồ sơ giờ tới được model cả khi bật tiết kiệm token.** Trước đây ở các mức tiết kiệm (kể cả mức mặc định) hồ sơ bị bỏ cùng với mục lục ký ức, nên cách xưng hô hay cách trình bày anh chị đặt một lần cho mọi brain chỉ có tác dụng khi tắt tiết kiệm.
- **Mở phiên chat mới với Claude Code không còn ghi lại toàn bộ cache khi bật tiết kiệm token.** Trước đây một dòng giờ đổi theo từng phút, cùng phần ký ức chọn theo câu hỏi, nằm trong phần prompt được cache, nên mỗi phiên mới phải ghi lại khoảng 25 nghìn token. Nay phần đó đi kèm tin nhắn đầu của phiên, còn prompt giữ nguyên giữa các phiên.
- **Mở một Team đã chat nhiều giờ không còn làm cả app chậm lại.** Từ bản 0.518.0, mỗi lần mở Team trên màn hình rộng là tab Thông tin tự mở, và máy chủ đọc lại toàn bộ tin nhắn của nhóm để dò file và link. Nhóm càng dài càng chậm, và trong lúc đó tải tin nhắn, chuyển nhóm, gửi tin đều phải chờ. Giờ máy chủ nhớ kết quả, lần sau chỉ đọc tin mới. Đo với nhóm 3.000 tin: từ 1,5 giây mỗi lần mở còn 0,003 giây.
- Mục Tài liệu của một cuộc trò chuyện dài cũng nhanh theo, vì dùng chung cách đọc này.
- **Tạo ảnh ChatGPT không báo "không có tài khoản" khi mọi tài khoản đang nghỉ vì hết lượt chat.** TISA BOT vẫn thử tài khoản đang bật đầu tiên, như trước khi có xoay tài khoản. Tài khoản đã tắt thì vẫn không được dùng.
- **Tạo ảnh ChatGPT không mắc kẹt ở tài khoản hết lượt.** Khi tài khoản đang dùng báo lỗi hạn mức, TISA BOT thử tài khoản ChatGPT đã đăng nhập tiếp theo theo thứ tự trong Models. Lỗi khác không tự gửi lại yêu cầu tạo ảnh và tài khoản bị tắt không được sử dụng.
- **Tag bot Zalo trong nhóm không còn bị nhầm là tag người khác sau khi TISA BOT khởi động lại.** Lưu Zalo ID đã xác minh từ tin do chính tài khoản gửi, dùng lại khi khởi động lại và từ chối ID không khớp.
- **Tắt riêng bản tổng hợp Việc của tôi lúc 07:30 khi đã có Morning Brief.** Đặt `agenda_enabled: false` trong `TISA/my-tasks.json` của brain cần tắt. Không thay đổi task, nhắc deadline, lịch hẹn hay thông báo thói quen của brain đó. Mặc định các brain khác vẫn có bản tổng hợp như cũ.
- **Đăng nhập được MCP có thông tin OAuth đặt ở máy chủ khác (impact.com).** Trước đây thẻ kết nối báo máy chủ không khai OAuth chuẩn MCP. Nay TISA BOT đọc thông tin đó khi nó nằm trên https công khai, do chính địa chỉ MCP đã khai trả về, và đúng là của địa chỉ đó.
- **Bot không còn quên khách sau mỗi lần cập nhật.** Trước đây lịch sử chat riêng của bot chỉ nằm trong bộ nhớ tạm, nên TISA BOT khởi động lại là bot gặp khách cũ như người lạ. Giờ bot đọc lại cuộc chat từ Hộp thư, gồm cả câu bạn tự trả lời tay.
- **Đọc tiếng Anh vào mic không còn bị tự dịch sang tiếng Việt.** Sau khi bấm dừng, TISA BOT nhờ mô hình viết lại câu cho đúng chính tả, và mô hình đôi khi trả về bản dịch tiếng Việt thay vì câu tiếng Anh đã nói (hay gặp ở câu dài, lần đọc thứ hai). Giờ câu nói bằng tiếng nào thì giữ đúng tiếng đó. Nếu mô hình vẫn dịch, TISA BOT bỏ bản dịch và giữ nguyên lời đã nghe. Áp dụng cho mic ở chat chính, Nhóm, Hội thoại và trình sửa ghi chú.
- **Bộ cài Windows hết đứng im.** Trước đây lỗi nằm chờ bấm Enter trong cửa sổ đen bị che, hoặc một trình cài phụ (winget, npm, Grok, Antigravity) không chịu kết thúc là cả bộ cài treo. Giờ mỗi bước có giới hạn thời gian, quá giờ thì bỏ qua và đi tiếp.
- **Tải Git, Python, Node nhanh hơn nhiều** trên máy không có winget.
- **TISA Store hiện gói "Trọn bộ".** Gói gồm nhiều loại trong một, như Quản lý khách hàng (CRM), trước đây không nằm ở tab nào nên không tìm và không cài được từ trang Store. Giờ có tab "Trọn bộ" ở cuối hàng tab.
- **Cài lại gói Store không còn bắt xác nhận Auto từng trợ lý.** Gỡ rồi cài lại một gói (ví dụ ECC: Đội lập trình), TISA BOT tự nhận các trợ lý của gói là trợ lý cũ: công tắc Auto, mục tiêu và cuộc trò chuyện giữ nguyên. File bạn tự tạo trùng tên một trợ lý cũ thì vẫn được hỏi như trước.
- **Trợ lý chưa bật Auto và không có mục tiêu đang mở không còn báo "Cần xác nhận"** khi file của nó mất rồi có lại.
- **Trình kết nối không khởi động được không còn bị báo nhầm là "hết phiên đăng nhập".** TISA BOT nhận lỗi đăng nhập bằng cách tìm số 401 trong câu lỗi, nên khi đường dẫn cài đặt tình cờ có chứa 401, lỗi "không tìm thấy file" hiện thành lời mời bấm Kết nối lại. Giờ 401 (và 502, 503, 504) chỉ được tính khi đứng riêng như một mã lỗi.
- **Gỡ gói ở Store nay nói rõ đồ của gói nằm ở brain nào.** Cộng sự và skill của một gói chỉ được đặt vào brain đang mở lúc cài. Trước đây đứng ở brain khác bấm gỡ là mất đồ ở brain kia mà màn xác nhận không nói đó là brain nào.
- Thẻ gói cũng ghi rõ khi đồ của gói nằm ở một brain khác với brain đang mở, thay vì chỉ ghi "Đã cài".
- **Bot nhóm tự gỡ các nhãn "bỏ lỡ" sai đã học trước bản 0.530.7.** Bản đó chặn nhãn sai mới, còn nhãn cũ vẫn nằm trong kho và tiếp tục đẩy bot nói nhiều. Lần mở kho đầu tiên sau khi cập nhật, TISA BOT gỡ nhãn "bỏ lỡ" gắn trên lượt thả cảm xúc, trả lại ngưỡng cho các nhóm bị kéo lệch, và thôi coi nhãn tự suy ra từ tin của chủ là lời chủ dạy.
- Lời chủ dạy thật (bấm 👍/👎, bảo bot im, dạy trong chat) giữ nguyên.
- Hiện lại mục Sửa cấu hình cho MCP tự thêm đã đăng nhập OAuth. Khi sửa URL, biểu mẫu giữ đăng nhập và chặn chuyển thông tin OAuth sang máy chủ khác.
- **Codex chạy đúng mức suy luận đã chọn ngay sau khi TISA BOT khởi động lại.** Trước đây, cho tới khi có người mở trang Models, bot và việc nền chạy bằng Codex rơi về mức mặc định của Codex (thường là cao) dù đã chọn thấp hay trung bình, nên chậm và tốn lượt hơn.
- **Bot nhóm không còn tự học sai rằng phải trả lời lượt thả cảm xúc.** Chủ thả tim vào tin của khách, hay một người thả hai cảm xúc liền nhau, từng bị tính là bot "bỏ lỡ" tin trước đó, khiến bot nói nhiều dần lên ở đúng những nhóm nó im là đúng.
- Chữ "up" trong câu thường như "up ảnh giúp em" và "hỏi lại" trong một câu dặn dài không còn bị hiểu là khách hỏi lại vì không ai trả lời.
- Nhãn bot tự suy ra từ tin của chủ không còn được tính nặng như lời chủ dạy trực tiếp.
- **Bước quy trình nay chạy đúng mức suy luận của trợ lý.** Trước đây mức suy luận đặt cho một trợ lý chỉ có tác dụng khi chat và trong nhóm; bước quy trình, kể cả việc Kanban giao theo quy trình, luôn chạy ở mức mặc định của model. Trợ lý chưa đặt mức thì bước vẫn chạy như cũ.
- **Việc nền chạy bằng Codex không còn bị bỏ cả lượt vì cổng công cụ lên chậm.** Trước đây cổng trả lời chậm hơn 20 giây là lượt nhắc hẹn hay lịch định kỳ đó hỏng luôn, phải chờ tới lần chạy kế tiếp. Giờ TISA BOT chờ cổng tới 45 giây và tự thử lại một lần sau 30 giây. Lỗi này xảy ra trước khi gọi model nên thử lại không tốn lượt và không lặp hành động nào.
- **Chatbot dùng gói ChatGPT nay tự chuyển tài khoản khi hết lượt.** Trước đây bot riêng luôn gọi bằng tài khoản 1, bỏ qua thứ tự tài khoản ở trang Models, nên tài khoản 1 hết lượt là bot báo lỗi 429 dù tài khoản khác còn dùng được.
- Bot chỉ đổi tài khoản khi chưa nói chữ nào và chưa gọi công cụ nào, nên khách không nhận tin trùng.
- Công cụ được tìm qua Hub có thêm cách nhận tham số bằng chuỗi JSON, tránh mất các trường dữ liệu trên một số cổng tương thích. Tham số sai định dạng bị từ chối trước khi gọi công cụ; quyền truy cập vẫn giữ nguyên.
- **Ảnh trong chat không còn tự thành ô trống sau 30 ngày.** Trước đây phiên đăng nhập hết hạn đúng 30 ngày sau lần đăng nhập dù ngày nào cũng dùng, chat vẫn chạy nhưng ảnh và danh sách tải không được mà không báo gì. Giờ còn dùng là phiên tự gia hạn.
- **Phiên hết hạn giữa chừng thì hiện ngay màn đăng nhập** thay vì để trang hỏng lặng lẽ.
- **Trợ lý tạo lại đúng tên cũ đã xác nhận được Auto.** Thẻ báo "Auto: Cần xác nhận" nhưng bấm vào thì cột phải không có hai nút "Đúng trợ lý cũ" và "Đây là trợ lý mới", nên không cách nào bật lại Auto. Nay hai nút hiện ra ngay dưới phần cài đặt của trợ lý.
- **Claude trả lời lại trên máy Windows cài bằng npm.** Sau khi cập nhật, mọi lượt chat Claude báo "Refusing to execute batch script ...claude.CMD". TISA BOT giờ tự tìm `claude.exe` thật nằm cạnh file đó (hoặc bản cài native, hoặc bản đi kèm SDK) nên không cần cài lại gì. Codex không dính lỗi này.
- **Kết nối Google Ads không còn đòi developer token.** Ô này giờ là tuỳ chọn và hướng dẫn đi theo đường Google Cloud: bật Google Ads API, bấm xin mức Explorer ngay trong project, rồi tạo OAuth client. Người mới không còn kẹt ở bước xin một token mà Google không còn yêu cầu.
- **Trang Models không còn làm app ì dần.** Mỗi lần mở trang để lại một lớp theo dõi thao tác kéo thả không bao giờ gỡ. Nay chỉ còn một lớp dùng chung.
- **Nhóm (Team) không còn kẹt ở tài khoản đã hết lượt.** Thẻ Claude Code, ChatGPT hay Grok Build có nhiều tài khoản thì lượt của cộng sự trong nhóm giờ chạy trên tài khoản còn hạn mức, giống chat và việc nền. Trước đây nhóm luôn chạy tài khoản 1, nên tài khoản 1 hết lượt tuần là cả nhóm báo "You've hit your weekly limit" dù tài khoản kia vẫn còn.
- **Hết lượt giữa lượt nhóm thì tự chạy lại bằng tài khoản kế.** Tài khoản báo hết lượt trước khi gọi công cụ nào: TISA BOT cho nó nghỉ và chạy lại ngay, tin trả lời ghi rõ đang dùng tài khoản nào. Bước đã gọi công cụ thì không chạy lại, để không gửi hay đăng hai lần.
- **Câu báo hết lượt không còn bị đăng thành câu trả lời của cộng sự.** Claude Code đôi khi in câu đó như một câu trả lời thường, nhóm giờ nhận ra và xử lý như lỗi hết lượt.
- **Workflow cũng xoay tài khoản.** Bước workflow chạy bằng Claude Code hay ChatGPT bắt đầu trên tài khoản còn lượt; tài khoản hết lượt khi bước chưa làm gì thì bước đó tự chạy lại bằng tài khoản kế và lần chạy đi tiếp. Trước đây cả lần chạy dừng với câu "gói hết lượt" dù tài khoản kia vẫn còn.
- **Thẻ ở trang Models ghi đúng tài khoản đang dùng.** Dòng đầu thẻ hiện tên, email và gói của tài khoản đang chạy. Trước đây nó luôn ghi tài khoản 1, nên thẻ đang chạy tài khoản Max vẫn đề "Pro".
### Cải thiện
- **Tab cài đặt của Team gọn hơn.** Phần hiện sẵn chỉ còn những gì bạn cần quyết cho một team: thành viên, mục tiêu, người điều phối tự quyết đến đâu, hành động ra ngoài có cần duyệt không, tên và trạng thái team.
- **Nghiệm thu và mức dùng chuyển vào mục Nâng cao**, cùng chỗ với các con số giới hạn và quyền chi tiết. Không có gì bị bỏ đi, mở Nâng cao là thấy đủ như trước.
- **Mục tiêu của team được đưa lên ngay dưới danh sách thành viên.**
- **Dải việc đầu khung chat hiện đủ các việc đang chạy**, không chỉ một việc.
- Cần quay về kiểu từng việc một thì đặt biến môi trường `TISA_TEAM_JOBS=1`.
- **Lần mở đầu tiên của một team dài sau khi TISA BOT khởi động lại không còn làm các thao tác khác chờ.** Trong lúc TISA BOT đọc lại lịch sử để dựng mục Tài liệu, tải tin nhắn vẫn nhanh như thường.
- **Theo dõi Facebook (Apify) không còn nằm sẵn trong TISA BOT, nó đi cùng gói trong Kho cài đặt.** Công cụ quét qua Apify là phần cài thêm, không phải ai cũng dùng. Anh chị đang dùng thì vào Kho cài đặt, bấm cập nhật gói "Theo dõi Facebook (Apify)" là có lại tool `fb_monitor`; token Apify đã dán vẫn giữ nguyên.
- **Tìm file theo tên dễ trúng hơn.** Gõ nhiều từ như "bảng giá" sẽ ra cả `bang-gia-dich-vu.md`: tên file chỉ cần chứa đủ các từ, không cần đúng dấu gạch hay thứ tự. Áp dụng cho mọi ô tìm file theo tên, gồm ngăn Tài liệu của cuộc trò chuyện.
- **Màn "Đang khởi động TISA BOT…" nhường chỗ cho app nhanh hơn.** Dữ liệu trang đầu về xong là màn này tắt gần như ngay.
- **Máy tải dữ liệu chậm không còn bị che tới 12 giây.** Trang đầu đã mở mà danh sách còn tải thì sau 4 giây app hiện ra, phần nào chưa xong tự hiện dòng "Đang tải" của nó như mọi trang khác.
- **Chỉ chat riêng mà bot đã trả lời mới có hồ sơ.** Nhóm và các cuộc chat của bạn bè, người nhà trên nick Zalo cá nhân thì không. Mỗi 5 phút TISA BOT làm tối đa 5 hồ sơ nên không tốn hạn mức dồn dập.
- **Bot xem lại 30 tin gần nhất của chat riêng thay vì 20.** Áp cho mọi kênh bot (Zalo Bot, Zalo cá nhân, Telegram, Messenger...). Cuộc chat có tin rất dài thì bot bớt từ tin cũ nhất. Nhóm vẫn xem 30 tin trước tin đang hỏi như cũ.
- **Cài trên Windows không còn cửa sổ đen riêng.** Tiến trình cài hiện ngay trong cửa sổ Setup: dòng "Bước 2/5", thanh chạy liên tục và một khung ghi từng việc đang làm.
- **Lỗi hiện ngay trong Setup.** Bước nào hỏng thì Setup nói rõ thiếu gì kèm đường dẫn nhật ký, trang cuối không còn báo "đã cài xong" khi chưa xong.
- **Mỗi dòng trong cây Vault chỉ còn một nút ba chấm.** Tạo file, tạo thư mục, ghim, tải về, đổi tên, xoá đều nằm trong menu bấm ra, nên tên file không còn bị các nút che mất, nhất là trên điện thoại.
- **Màn chào mừng: nhập mật khẩu hai lần.** Hai ô không giống nhau thì TISA BOT báo ngay và đưa anh chị tới đúng ô cần sửa, chưa tạo tài khoản. Gõ nhầm một ký tự không còn làm mất quyền vào máy mới cài.
- **Có nút con mắt để xem mật khẩu.** Bấm là hiện cả hai ô cùng lúc để so cho dễ, bấm lần nữa là ẩn lại.
- **Khung chat trên điện thoại gọn hơn.** Vòng hạn mức, tên model và mức suy nghĩ gộp thành một viên duy nhất (ví dụ "Opus 5.5 Medium"), tên model không còn bị cắt thành "Op...".
- **Bấm vào viên đó là mở một bảng từ dưới lên**, có đủ ba thứ: hạn mức gói (mỗi khung một dòng), thanh mức suy nghĩ kèm Fast mode, và danh sách model có ô tìm. Chọn model xong bảng tự đóng; bấm X, bấm vùng mờ hoặc kéo xuống cũng đóng.
- Bản máy tính giữ nguyên ba nút và ba bảng nhỏ như trước.
- **Tìm tool gọn hơn**, và mục Đề xuất ở trang Mức dùng cho biết kết quả tool đã giữ được bao nhiêu ngoài hội thoại.
- **Zalo cá nhân: có tin là TISA BOT đọc ngay, không còn quét 20 giây một lần.** Trước đây TISA BOT hỏi Zalo đều đặn cả ngày kể cả khi không có tin nào, và tin trong nhóm phải chờ tới 20 giây bot mới thấy. Giờ tin tới lúc nào TISA BOT đọc lúc đó; ngày không có tin thì không đọc lần nào.
- Không có tin thì TISA BOT không chạy nhịp nào cho Zalo. Tiến trình Zalo bị tắt thì TISA BOT dựng lại ngay và đọc bù. Máy chưa lên bản Zalo mới vẫn chạy theo nhịp cũ, không mất tin.
- **Danh sách ghim tự theo thói quen.** Công cụ lâu không dùng tự rời danh sách, công cụ mới dùng nhiều tự vào. Danh sách của một brain đổi nhiều nhất một lần mỗi ngày và có giới hạn kích thước, nên prompt không phình và phần lưu đệm của nhà cung cấp ít bị làm mới.
- **Điều bạn dặn TISA Core được giữ nguyên.** Một giá trị bạn đặt bằng lời cho bất kỳ núm tự chỉnh nào thì TISA Core không tự đổi lại trong 30 ngày, kể cả sau khi khởi động lại.
- **Ghi nhớ học sai được tính vào kết quả.** Một ghi nhớ TISA BOT tự học mà bạn bảo xoá được tính là một lần học sai, nên mẻ học sau tự dùng model mạnh hơn một bậc. Ghi nhớ do bạn tự viết bị xoá thì không ảnh hưởng gì.
- **Một chỗ để xem và hoàn lại.** Hỏi TISA BOT "việc nền và tự học đang chỉnh gì": một câu trả lời gồm model của từng việc nền, các núm đang tự chỉnh, các thay đổi gần đây và bài học về cách học.
- **Tự học mặc định chỉ học ký ức và wiki.** Học skill mở thêm một lượt phản biện mỗi mẻ và kéo theo cả phần chấm điểm skill chạy ngầm, là chỗ tốn hạn mức nhất khi bạn không gõ gì. Máy đã cài cũng được tắt một lần; cần thì bật lại công tắc Kỹ năng ở trang Tự học.
- **Tự học chạy 15 phút sau sự kiện cuối cùng, một lần cho cả cuộc trò chuyện.** Trước đây cứ 3 lượt chat là một mẻ học, nên một cuộc 12 lượt mở 4 mẻ đọc lại gần như cùng một đoạn. Giờ TISA BOT chờ brain yên 15 phút (bạn hỏi thêm, việc nền chạy xong hay khách đang nhắn với chatbot đều tính lại từ đầu) rồi học một mẻ, mỗi tin nhắn chỉ đọc một lần. Cả ngày không có sự kiện nào thì không học và không tốn gì. Câu "ghi nhớ giúp" vẫn được học sau 30 giây, và brain bận liên tục (chatbot có khách suốt ngày) thì vẫn học sau tối đa 2 giờ.
- **Bỏ trần ngày của tự học.** Trần 40 mẻ và 15 triệu token mỗi ngày không hợp cho cả người dùng nhiều lẫn người dùng ít, và chạm trần thì TISA BOT vẫn chạy mẻ học rồi chỉ không ghi file. Nhịp mới đã giữ số mẻ theo đúng số cuộc trò chuyện.
- **Gợi ý câu tiếp theo và các lượt chỉ cần chữ nhẹ đi nhiều.** Những lượt này (gợi ý câu tiếp theo sau mỗi lượt chat, bộ phán xử, phân loại sự cố, câu nhắc thói quen) không dùng công cụ nào nhưng vẫn gửi kèm cả bộ luật và mô tả công cụ của Claude Code. Phép đo sẵn có trong mã cho cùng một câu: 27.665 token khi gửi kèm, 183 token khi không. Giờ chúng không gửi kèm nữa.
- **Câu trả lời dài chảy ra không còn khựng.** Trong lúc chữ đang về, TISA BOT chỉ vẽ lại đoạn đang viết dở, các đoạn đã xong giữ nguyên. Đo với một câu trả lời 20.000 ký tự trên điện thoại yếu: thời gian vẽ từ 5,4 giây xuống 1 giây, hết hẳn các lần đứng hình.
- **Màn chính lúc rảnh nhẹ máy hơn.** Nền sao sau quả cầu vẽ thưa lại khi không ai nói và TISA BOT không nghĩ, nhìn vẫn như cũ. Điện thoại đỡ nóng và đỡ hao pin khi để mở.
- **Chat nhẹ đĩa hơn, và một kết nối hỏng không còn kéo chậm mọi lượt.** Mỗi lượt chat bớt hàng chục lần ép ghi đĩa (đỡ rõ trên VPS). Nguồn dữ liệu đứng hình hai lần liền thì TISA BOT trả lời ngay bằng danh sách công cụ đang có và dò lại ở nền.
### Bảo mật
- **Công cụ Facebook và Meta Ads không còn đưa token cho AI.** Link "trang sau" và thông báo lỗi của Facebook có kèm token truy cập; nay TISA BOT gỡ token trước khi trả kết quả cho model. Dữ liệu bài viết, bình luận và con trỏ phân trang giữ nguyên.
- **Kết nối Chỉ đọc không còn xin phạm vi dạng `mcp:write`.** Khi đăng nhập theo kiểu TISA BOT tự dò và máy chủ có sẵn phạm vi đọc (vd `mcp:read`), kết nối đặt Chỉ đọc bỏ các phạm vi có tên kết thúc bằng `write`. Kiểm tra tên tool của hub vẫn là lớp chặn chính. Nâng mức quyền sau đó thì phải đăng nhập lại.
- **Tin WeChat giả bị chặn từ cửa.** TISA BOT kiểm chữ ký từng tin, từ chối yêu cầu cũ quá 15 phút, và tài khoản bật Chế độ an toàn thì chỉ nhận tin đã mã hoá.
- **Bot của chủ không tải gì của người lạ.** Ảnh, tin thoại và file chỉ được tải về khi chat đã được bấm Cho phép.
- **Tool sửa nhãn của Google Ads không còn chạy được ở mức Chỉ đọc.** Bản MCP mới của Google có thêm tool tạo, sửa, xoá nhãn và tải video lên YouTube; hai tool nhãn từng bị xếp nhầm vào nhóm đọc. Giờ chúng chỉ chạy ở mức Toàn quyền, tạo asset ở mức Ghi nháp, và thẻ kết nối nói rõ mỗi mức sửa được gì.
- **Siết khung chat, trung tâm công cụ và việc chạy nền.** Chữ trong tin nhắn không còn chen được mã vào trang điều khiển. Trung tâm công cụ chỉ trả lời chính máy đang chạy TISA BOT. Việc chạy ở mức Ghi nháp chỉ ghi được file thường trong bộ não.
- **Chatbot trả lời khách dưới mức Toàn quyền không còn giao được việc cho AI chạy sau.** Nó vẫn tạo được lời nhắc chỉ nhắc bằng chữ. Cần bot tự giao việc thì nâng bot lên Toàn quyền.
- **Bộ não nhập từ tệp về luôn ở trạng thái nghỉ.** Vòng lặp, plugin và nhắc việc đều tắt dù tệp viết kiểu nào; cấu hình chạy lệnh của các engine không được nhập theo. Thư viện đọc PDF lên bản đã vá.

## [0.526.6] - 2026-11-10
### Thêm mới
- **Bộ TISA:** Thẻ Kết quả của Đội Quân AI: xem ảnh, video và tải tệp kết quả không còn báo lỗi. Thông báo có bản mới ghi tên bản (V2.77) thay cho số nội bộ.

## [0.526.5] - 2026-11-10
### Thêm mới
- **Bộ TISA:** Chuyển máy chủ: Hệ thống → Chuyển máy chủ đóng gói toàn bộ TISA BOT (mọi bộ não, khoá API, kết nối MCP, Fanpage, Zalo, Chatbot, lịch sử chat, việc định kỳ, Đội Quân AI) thành một file khoá bằng mật khẩu; máy mới hoặc VPS chỉ cần tải file lên là dùng tiếp, không phải cài đặt lại.

## [0.526.4] - 2026-11-10
### Thêm mới
- **Bộ TISA:** Giao dự án và Đội Quân AI chung một khung trên thanh menu: dòng Giao dự án là nút tím, bấm vào mở Bàn làm việc; 3 ô số Đang làm / Chờ duyệt / Đã xong; thanh Đội Quân AI thu gọn / mở 5 mục; Chatbot nằm dưới. Hộp Kết nối Meta có nút Tạo prompt cho Claude làm giúp. Menu linh vật theo thanh menu, biểu tượng có màu. Trang Mô hình: bảng Độ sâu suy nghĩ và các bảng chọn hiện giữa màn hình; bỏ dòng cảnh báo gói Claude dễ gây hiểu lầm. Cuối menu điện thoại gọn một hàng. Trợ lý không tự khởi động lại TISA BOT giữa lượt trả lời nữa. Điện thoại có lại nút thu gọn menu cạnh Hệ thống.

## [0.526.3] - 2026-11-10
### Thêm mới
- **Bộ TISA:** Điện thoại: khu cuối menu xếp lại (ô bộ não rộng hết, 3 nút Âm thanh · Thư mục · Sáng/tối bằng nhau có chữ); hàng nút Hỏi chuyên gia cân hơn; trang Nhân sự, phòng ban: công tắc ngang tên bên phải, chức danh và ô phòng rộng hết dòng.

## [0.526.2] - 2026-11-10
### Thêm mới
- **Bộ TISA:** Cài đặt đội > Nhân sự, phòng ban gọn và dễ dùng hơn: thanh tổng quan có ô tìm nhanh, thẻ phòng hai cột, mỗi người một dòng có hình mang màu phòng, công tắc bật tắt, tên và chức danh xếp gọn.
### Sửa lỗi
- **Claude Fable 5.2 đã có trong ô chọn model.** Trước đây danh sách model Claude chỉ lấy từ bản Claude Code đang cài, nên máy nào Claude Code chưa lên bản mới thì không thấy model mới dù đã cập nhật TISA BOT. Nay danh sách gộp cả model mà bản TISA BOT biết, bản mới nhất đứng trên.
- **Thêm Claude Haiku 5.5 vào danh sách dự phòng và sửa giá quy đổi** của Fable 5.2, Opus 5.5, Sonnet 5.5, Haiku 5.5 trên trang Mức dùng.

## [0.526.1] - 2026-11-10
### Thêm mới
- **Bộ TISA:** Sửa cộng sự mang hình đại diện kiểu TISA (bong bóng, bo góc, lục giác, khiên, giọt nước) không còn báo Hình đại diện không hợp lệ. Đội Quân AI là một phần của TISA BOT: mở ngay trong cùng tên miền, không hỏi đăng nhập lần hai; gõ /doiquanai là vào thẳng.
### Cải thiện
- **Số Node và Link nằm gọn trong đồ thị.** Dòng số cạnh nút chọn bộ não đã bỏ, giờ hiện ở góc trên bên trái của đồ thị, nút con mắt ẩn nó cùng các nhãn khác.
- **Danh sách bộ não gọn hơn.** Mỗi bộ não ghi "1920 Node · 2480 Link" trên đúng một dòng, chữ nhỏ hơn một chút, không còn gãy làm hai.

## [0.526.0] - 2026-11-10
### Thêm mới
- **Bộ TISA:** Chặn bot AI và máy quét đọc trang quản trị, không cho Google đưa link quản trị lên tìm kiếm, gõ lại mật khẩu mới hai lần, lưu trữ hội thoại bằng nút ⋯, chọn bộ não mặc định, xuất và tải lên bộ não bằng file .zip, app bớt khựng, giờ thông báo theo múi giờ đã chọn. Đăng nhập Zalo bằng QR tự làm mới mã khi hết hạn hoặc bị từ chối, không còn đứng. Đội Quân AI đặt trên Cloudflare cũng mở ngay trong TISA BOT, cùng một tên miền. Bấm Cập nhật: kéo bản mới lỗi thì tự trả bản đang dùng về, máy cài từ nguồn khác thì dừng trước khi đụng vào. Web CRM: bảng Data Zalo / FB có cột STT, Ngày đăng ký rồi Khách. Zalo MCP trên Mac: hai bản cùng một tài khoản không còn đá nhau làm bot chỉ nghe tin vài giây.
- **Mỗi hội thoại trong cột lịch sử có một nút ⋯** thay cho bốn icon rời (ghim, chuyển project, đổi tên, xoá). Menu có: Ghim lên đầu, Chuyển vào project, Đổi tên (sửa ngay tại dòng), Chia sẻ link, Xuất ra file .md, Đánh dấu chưa đọc, Lưu trữ và Xoá. Bấm chuột phải hoặc nhấn giữ trên điện thoại cũng mở menu này; trên điện thoại menu trượt lên từ dưới, chữ to.
- **Lưu trữ hội thoại:** hội thoại lưu trữ rời khỏi danh sách nhưng giữ nguyên nội dung, TISA BOT vẫn nhớ và ô tìm kiếm vẫn tìm thấy. Mục "Đã lưu trữ" ở đáy cột mở danh sách này; mở một hội thoại đã lưu trữ thì thanh tiêu đề có nút "Đưa trở lại danh sách". Nhắn tiếp vào hội thoại đã lưu trữ thì nó tự trở lại danh sách.
- **Chọn bộ não nào làm mặc định.** Trong bảng chọn bộ não, bấm ngôi sao ở một bộ não để đặt nó làm mặc định. Việc chưa chọn bộ não riêng sẽ chạy ở đó, và mọi máy đồng bộ cũng đổi theo.
- **Xoá được Brain Default cũ.** Đổi mặc định sang bộ não khác xong, Brain Default thành bộ não thường và xoá được như mọi bộ não khác (vẫn vào thùng rác 30 ngày). Nó không tự sống lại nữa.
- **Biết trước khi xoá.** Ô xoá bộ não giờ nói rõ bao nhiêu vòng lặp, nhắc việc sẽ dừng theo, và bot nào đang trả lời từ bộ não đó để chuyển đi trước.
- **Bấm Kết nối GitHub, TISA BOT kiểm tra máy có git chưa, thiếu thì tự cài rồi mới mở bước đăng nhập.** Windows cài bằng winget hoặc bộ cài chính thức của Git (không cần quyền quản trị), Mac dùng Homebrew hoặc công cụ của Apple, Linux dùng trình quản lý gói khi TISA BOT có quyền.
- **Thẻ GitHub đã kết nối mà máy thiếu git có thêm nút Cài git.** Cài không được thì TISA BOT hiện đúng lệnh để cài tay, nút Thử lại và nút Bỏ qua.
- **Xuất và tải lên cả bộ não bằng một file .zip:** mỗi dòng trong hộp chọn bộ não có nút Xuất. File mang theo ghi chú, ảnh, agent, skill, workflow và bộ nhớ, không mang theo token, chat thô hay lịch sử git. Nút "Tải lên bộ não (.zip)" luôn tạo một bộ não mới, không đè bộ não đang có. Plugin, vòng lặp và nhắc việc đi kèm file đều được tắt sẵn, bật lại ở trang tương ứng nếu cần. Không có trần dung lượng cố định: máy chủ còn đủ chỗ trống là nhận, tới một triệu file. Nén và giải nén chạy nền có hiện tiến độ, file tải lên được gửi từng phần 32MB, nên bộ não lớn vẫn đi qua được Cloudflare Tunnel.
- **Đổi tên và xoá ngay trên từng dòng của hộp chọn bộ não**, cuối hộp có ba nút Tạo bộ não, Tải lên bộ não và Mở thư mục ngoài. Bốn nút rời cạnh hộp chọn trên thanh trên cùng đã bỏ.
### Cải thiện
- **Xoá hỏi lại ngay trong menu**, kèm gợi ý chọn Lưu trữ nếu chỉ muốn cho gọn, thay cho hộp thoại của trình duyệt.
- **Bỏ nút "Xem thêm":** cuộn tới cuối danh sách là tự tải thêm.
- **Dòng hội thoại gọn hơn:** tin ghim có dấu ghim nhỏ trước tiêu đề, tên project có icon thư mục và chữ thường, tên bộ não AI chữ xám nhạt.
- **Mở lại màn mạng nơ-ron, mở thêm tab hay điện thoại vừa kết nối lại không còn làm cả app khựng.** Cả app dùng chung một bộ theo dõi file cho mỗi thư mục, dựng một lần rồi giữ thêm 15 phút sau khi đóng màn đồ thị. Trước đây mỗi lần mở là dựng lại từ đầu, có lần làm mọi thao tác khác chờ gần 3 giây.
- **Danh sách công cụ của các kết nối MCP được nhớ 10 phút** thay vì hỏi lại mọi máy chủ mỗi phút, nên app bớt hẳn những lần khựng một hai giây khi đang chat. Nút Kiểm tra và vòng kiểm tra sức khoẻ vẫn hỏi thẳng máy chủ, và kết nối nào báo đổi công cụ thì được hỏi lại ngay.
- **Điện thoại: nút chọn model về khung nhập, đứng ngay cạnh nút mức suy nghĩ** y như bản máy tính. Bấm vào thì bảng chọn model mở ngay phía trên khung nhập, vừa khít bề ngang màn hình.
- **Thanh trên cùng gọn hơn:** chỉ còn nút menu, chuông thông báo và nút + hội thoại mới.
- **Đổi mật khẩu giờ có thêm ô "Nhập lại mật khẩu mới".** Hai lần gõ phải khớp nhau thì TISA BOT mới lưu, nên lỡ gõ sai một ký tự không còn tự khoá mình ngoài cửa. Áp dụng ở cả trang Tài khoản lẫn khối Tài khoản đăng nhập trong Cài đặt.
- **Mở màn mạng nơ-ron không còn làm cả app đứng.** Bộ theo dõi file của đồ thị được dựng trên luồng riêng, nên bộ não nhiều thư mục không còn khiến mọi thao tác khác chờ tới 2 giây mỗi lần mở.
- **Mọi kết nối ra ngoài dùng chung một bộ chứng chỉ bảo mật**, được nạp một lần trên luồng nền lúc khởi động. Trước đây mỗi lần gọi ra ngoài (tin cộng đồng, Telegram, Zalo, model...) đều nạp lại cả bộ, có lần làm app đứng gần 2 giây.
- **Đọc lịch sử Zalo cá nhân chạy nền.** Sau mỗi lượt đọc tin, phần dò lại tin bị sót trong file lịch sử không còn chặn các thao tác khác.
- **Câu trả lời trải rộng hết khung chat, không chừa khoảng trống lớn bên phải:** ở trang Cộng sự, câu trả lời giờ rộng tới đúng mép tin bạn nhắn (trên iPad từ khoảng 780px lên hơn 1.000px), bớt cuộn hẳn. Màn máy tính rất rộng thì khung dừng ở khoảng 120 chữ mỗi dòng để mắt khỏi mỏi.
- **Trang Trò chuyện và trang Team đổi theo cùng một kiểu:** câu trả lời rộng bằng cột chat, câu trả lời của trợ lý trong Team không còn bị chặn ở 680px.
- **Màn hình khởi động:** mở TISA BOT là thấy logo cùng dòng "Đang khởi động TISA BOT…" cho tới khi trang đầu tiên đã có đủ dữ liệu. TISA BOT vừa cập nhật hay khởi động lại thì màn này báo thêm lần mở đầu có thể lâu hơn một chút.
- **Mọi màn đang chờ tải dùng chung một hiệu ứng** như trang Cộng sự: vòng xoay nhỏ kèm chữ "Đang tải", trang lớn thì vòng xoay ở giữa. Trang đang nạp không còn hiện nhầm câu "đang phát triển".
- **Số node và liên kết trên thanh trên cùng chỉ hiện ở màn mạng nơ-ron**, các trang khác gọn hơn.
- **Hộp chọn bộ não ghi số node và số liên kết của từng bộ não**, đúng như đồ thị đếm. Số chỉ được đếm khi mở hộp, nên không làm chậm lúc tải trang.
- **Trang Cộng sự và Team hiện dòng "Đang tải…"** ở chỗ danh sách và cuộc trò chuyện chưa về, thay vì để trống như bị treo.
- **Mở một team là thấy ngay tab Thông tin** ở khung bên phải trên màn rộng. Đóng khung đó thì lần sau TISA BOT nhớ và để đóng.
- **Nút tìm kiếm, cài đặt và nút đóng của Team gọn đẹp hơn:** nút vuông, không viền, cùng kiểu với các tab bên cạnh.
- **Danh sách team tải nhanh hơn khoảng 2,5 lần**, và tốc độ mở team không đổi dù team có hàng chục nghìn tin nhắn.
### Sửa lỗi
- **Giờ trong thông báo đã khớp múi giờ trong Cài đặt.** Trên VPS, cảnh báo bảo mật và thẻ "Thông báo hệ thống" trong TISA Core từng in giờ máy chủ (UTC), lệch 7 tiếng với giờ Việt Nam. Nay chúng theo múi giờ anh chị đã chọn.
- Cùng lỗi đó được sửa ở dòng "mở lại lúc" khi ChatGPT Live hết lượt, giờ đồng bộ sao lưu, lần cuối Threads gửi bình luận, và giờ sự kiện webhook TISA BOT đọc được.
- **Quy trình chạy bằng agent Claude dùng được mọi kết nối của TISA BOT.** Việc giao theo quy trình (kể cả mức Toàn quyền) và quy trình chạy từ chat không còn báo "thiếu công cụ" khi cần Gmail, Sheet, Zalo hay MCP khác.
- **Chatbot, mục Hội thoại chỉ hiện hội thoại của brain đang mở.** Fanpage và bot đã chuyển sang brain khác không còn hiện ở brain cũ, kể cả số đếm. Bật "mọi brain" ở mục Kênh để xem tất cả.
- **Kiểm tra tự động xanh lại.** Hai bản cập nhật cùng thêm đường dẫn mới cho máy chủ nên bảng đối chiếu bị lệch số thứ tự. Người dùng không thấy gì khác.
- **Git vừa cài xong được nhận ngay, không phải khởi động lại TISA BOT.** Trước đây máy chủ chạy từ trước khi có git vẫn báo "chưa cài git".
- **Nút cài app ở chân menu trái không còn tràn ra ngoài** trên máy tính bảng và laptop cảm ứng: nút gọn bằng nút Tặng sao, ghi "Cài app", thu gọn menu thì chỉ còn biểu tượng.
### Bảo mật
- **Lỡ lộ link quản trị thì Google không đưa lên kết quả tìm kiếm.** Mọi trang của TISA BOT giờ mang lệnh `noindex`, kể cả màn hình đăng nhập và link chia sẻ.
- **Bot AI không đọc được TISA BOT.** GPTBot, ClaudeBot, PerplexityBot, công cụ SEO và máy quét như Shodan, Censys nhận lỗi 403, không thấy chữ nào. TISA BOT cũng có `/robots.txt` cấm chúng.
- Trình duyệt thật, khung xem trước link khi dán vào Zalo hay Telegram, webhook và TISA BOT Gate vẫn chạy như cũ. Cần tắt lớp chặn thì đặt `TISA_BLOCK_BOTS=0`.
- **Các file bảo mật tài khoản không còn lọt vào git hay image Docker.** Dấu vân tay tài khoản, nhật ký bảo mật, danh sách mạng đã đăng nhập và thông tin phiên giờ nằm trong danh sách bỏ qua, nên `git add -A` hay `docker build` trên máy không mang chúng theo nữa.

## [0.517.4] - 2026-11-10
### Thêm mới
- **Bộ TISA:** Quản lý web có sẵn 2 web mẫu nối sẵn với TISA BOT: Web CRM (khách, đơn, sale, KPI, hoa hồng, báo cáo) và Lead Page + Sale Page, nhân bản thêm bao nhiêu trang cũng được. Mọi chatbot (Fanpage, Zalo, Zalo OA) hễ khách để lại số điện thoại là tự vào CRM kèm hội thoại gốc; CRM lấy số để kết bạn Zalo và nhắn chăm sóc khi anh chị đã duyệt mẫu tin. Giao diện điện thoại: nút thu/mở khung và các nút nhỏ to hơn, thanh công cụ một hàng cân đối.

## [0.517.3] - 2026-11-09
### Thêm mới
- **Bộ TISA:** Trang Quản lý web: mọi web đã đưa lên mạng nằm một chỗ, kiểm tra kết nối và tên miền, lấy nội dung về bộ não để tư vấn, nhận khách để lại thông tin, nhờ AI sửa web. Văn phòng 3D: nhân sự có hình riêng, đứng dậy đi tới Tâm nhận việc và nộp lại khi xong. Tài khoản nhân viên: mỗi ô chat có nhãn màu cho biết hỏi ai, lọc theo người được hỏi, lưu trữ thay cho xoá. Tên thương hiệu dài tự xuống hàng (Shift + Enter để tự ngắt dòng). Menu Hệ thống có màu. Dòng phiên bản TiSaBot dưới thanh menu, có bản mới thì hiện nút Cập nhật. Nhật ký cập nhật gom theo từng lần phát và đặt tên V.

## [0.517.2] - 2026-11-09
### Thêm mới
- **Bộ TISA:** Thanh menu mới: Hỏi nhanh, Hỏi chuyên gia, Giao dự án, Chatbot; Đội Quân AI thành nhóm trên thanh menu, dùng chung đăng nhập ở /doiquanagent. Tự đặt tên, chọn màu giao diện. Tài khoản nhân viên có phân quyền, chọn mô hình, nhiều cuộc hỏi và giới hạn câu hỏi mỗi ngày. Cài đặt đội gom theo phòng ban. Trang Tự học: tích ô Học cái gì là lưu ngay. Kết quả lưu theo tháng và ngày trong 04-ket-qua, có lối tắt ngoài Desktop; ảnh, video, PDF bấm là xem, trên máy chủ mở thẳng slide, Word, Excel. Giao diện tối áp đúng cho Đội Quân AI và trang nhân viên.

## [0.517.1] - 2026-11-09
### Thêm mới
- **Bộ TISA:** Bật lại nút Cập nhật trong app: có bản mới thì TISA BOT báo, bấm là tự lên bản mới, giữ nguyên dữ liệu và kết nối.
- **Trình sửa file tự lưu như Google Docs.** Ngừng gõ khoảng một giây là file được lưu, nút Lưu báo "Đang lưu…" rồi "Đã lưu". Đóng file, chuyển file, tải lại hay lỡ vuốt lùi trang cũng không mất chữ đã gõ.
- **Mất mạng giữa chừng vẫn giữ chữ.** Phần chưa lưu được giữ trong trình duyệt và tự khôi phục ở lần mở file sau.
- **Nút mic đọc chữ trong trình sửa file .md và .txt.** Bấm, nói, chữ hiện đúng chỗ con trỏ và được viết lại cho đúng ngữ cảnh, giống mic ở khung chat.
- **Bot Zalo cá nhân hiện "đang soạn tin..." trong nhóm.** Chỉ bật sau khi bot đã quyết định trả lời (được gọi tên, hoặc bộ phán xử chọn lên tiếng) và giữ tới lúc gửi xong, nên nhóm không còn im 20-30 giây rồi mới thấy bot nói. Tin bot đọc rồi im thì không hiện gì.
- **Nút bật/tắt trên trang Chatbot** cho từng bot, mặc định bật.
- **Mỗi hội thoại ở cột trái có nhãn thư mục nhỏ ghi tên project.** Liếc là biết cuộc đó thuộc nhóm nào, không cần mở ra. Đang lọc đúng một project thì nhãn tự ẩn cho đỡ lặp.
- **Nhãn bộ não ghi tên dễ hiểu:** "Claude" thay cho "cli", "Codex", "Grok", "OpenRouter"... thay cho mã nội bộ.
- **Bảy bộ não chạy bằng API key cũng có thẻ "Kế hoạch" trong khung chat.** OpenRouter, OpenAI, Anthropic API, Gemini, Groq, DeepSeek và Ollama giờ có công cụ `tisa_plan`: gặp việc từ 3 bước trở lên, model lập danh sách việc và đánh dấu từng mục khi xong, giống Claude Code, Codex và Grok Build. Câu hỏi thường không dùng tới nó.
- Tốn thêm khoảng 200 token mỗi lượt cho phần mô tả công cụ (đa số hãng có cache), cộng một vòng công cụ ngắn mỗi lần cập nhật danh sách. Muốn tắt thì vào menu "+" ở ô nhập, mục "Kế hoạch việc dài (bộ não API)". Chỉ khung chat của chủ có công cụ này, bot trả lời khách và việc nền thì không.
- **Khung trò chuyện hiện kế hoạch của bộ não như một danh sách việc.** Khi Claude Code, ChatGPT (Codex) hay Grok Build tự lập kế hoạch cho một việc nhiều bước, thẻ "Kế hoạch 2/5" hiện ngay trên câu trả lời: việc xong có dấu tích và gạch ngang, việc đang làm in đậm, việc còn lại để trống. Dòng trạng thái dưới khung chat cũng ghi đang ở bước nào. Thẻ được giữ lại khi tải lại trang.
- Không tốn thêm token: TISA BOT chỉ vẽ danh sách mà bộ não vốn đã lập, không gọi thêm model.
- **Tab Công việc ở trang Cộng sự hiện việc cộng sự đang làm trong chat.** Trước đây tab chỉ có việc đã xếp hàng, nên lúc cộng sự đang trả lời nhiều bước ngay trong khung chat bên cạnh thì tab vẫn trống. Nay có thẻ "Đang làm trong chat" kèm số bước và kế hoạch, xong lượt là thẻ tự tắt.
- **Tab Công việc hiện các lần chạy Quy trình mà cộng sự có tham gia.** Mỗi lần chạy là một thẻ: đang chạy thì ghi bước nào và của ai, chờ duyệt thì nằm ở Cần bạn, hỏng thì đánh dấu hỏng, bấm Mở là tới đúng quy trình. Bộ lọc nguồn có thêm "Quy trình". Lần chạy bị cắt giữa chừng (máy chủ tắt khi đang chạy) không còn nằm mãi ở Đang làm.
- **Zalo OA cấp quyền theo OAuth v4.** Ở form Thêm kênh Zalo OA, dán App ID, App secret key, OA secret key rồi bấm Cấp quyền bằng Zalo: chọn OA, bấm Cho phép là TISA BOT tự lưu kênh. Không cần lấy refresh token tay ở API Explorer nữa. Form hiện sẵn Callback URL để dán vào app Zalo một lần.
- **Cấp quyền lại một nút.** Refresh token chết thì mở Sửa kênh, bấm Cấp quyền lại bằng Zalo, TISA BOT dùng khoá đã lưu và bot đang trực tự chạy lại.
- **Gói ChatGPT nghe giọng luôn, không cần key.** Đã nối ChatGPT ở trang Models là mic đọc chữ, cuộc gọi đường Cơ bản và tin thoại Telegram, Zalo được chính gói ChatGPT nghe, câu Việt xen tiếng Anh giữ đúng cả hai thứ tiếng.
- **Tai nghe tự theo model đang dùng.** Bộ não chính là ChatGPT thì gói ChatGPT nghe trước, là Groq hay OpenAI thì tai của hãng đó. Claude, Antigravity và Grok không mở cổng nghe cho gói của họ, nên TISA BOT dùng tai tốt nhất đang có.
- **Bot Zalo ở Kênh Admin gọi được cộng sự như Telegram.** Gõ `@<tên> <câu hỏi>` để hỏi một câu, hoặc `/agent <tên>` để cộng sự đó trả lời cả chat.
- **Thẻ trợ lý ở trang Cộng sự hiện tag ngay dưới tên**, cạnh avatar. Chữ "Hệ thống" của TISA Core cũng xuống dòng này. Cột hẹp thì tag dư gộp thành "+n".
- **Gọi TISA BOT qua API không cần giữ kết nối chờ.** Gửi `POST /chat/jobs` là nhận ngay mã job, lượt chat chạy nền, lát sau hỏi `GET /chat/jobs/{mã}` để lấy câu trả lời. Hợp cho backend chạy trên serverless, và rớt mạng giữa chừng cũng không mất kết quả.
- **Job nào của token nấy.** Token khác không đọc được, mỗi token chạy tối đa 4 job cùng lúc, mỗi phiên một job. Kết quả giữ 24 giờ.
- **Linh vật có ảnh riêng.** Vào Cài đặt > Linh vật, bấm Tải ảnh lên: ảnh được cắt theo hình dáng đang chọn và hiện ở con pet, logo thanh bên lẫn ô chọn hình. Bấm Dùng lại hình TISA BOT là về khuôn mặt cũ.
- **Ảnh đó làm luôn icon trên tab trình duyệt**, nên mở nhiều TISA BOT cùng lúc vẫn phân biệt được ngay. Có công tắc để tắt nếu muốn giữ logo trên tab.
- **Đặt tên tài khoản ngay lần đăng nhập đầu.** Thẻ ChatGPT, Claude Code, Grok, Antigravity và key API đầu tiên đều hỏi tên trước khi đăng nhập, tên hiện ngay trên dòng trạng thái của thẻ nên không còn lẫn tài khoản nào với tài khoản nào.
- **Đổi tên tài khoản bất cứ lúc nào.** Nút ⋯ của thẻ có "Đặt tên tài khoản", mỗi tài khoản trong danh sách cũng có "Đổi tên". Thêm tài khoản mới thì bắt buộc đặt tên.
- **Gợi ý câu tiếp theo ngay trong ô chat.** TISA BOT trả lời xong, ô nhập trống hiện mờ câu anh nhiều khả năng sẽ gõ tiếp (ví dụ "ok làm theo đề xuất cho cả 2 PR đi"). Bấm **Tab** để điền vào, sửa thêm hoặc Enter gửi luôn; trên điện thoại bấm nút **Tab** cạnh ô nhập.
- Có cả ở chat chính lẫn trang Nhóm. Gợi ý chạy bằng model việc nền, không tốn bộ não chính. Tắt hoặc bật lại ở menu **+** của khung chat, mục "Gợi ý câu tiếp theo".
- **Mỗi cộng sự có thể chọn giọng ChatGPT Live riêng.** Trong trình sửa trợ lý, chọn một trong các giọng mà Codex realtime v3 hỗ trợ. Để Mặc định thì dùng giọng chung ở trang Cài đặt. Giọng được lưu trong file cộng sự và đi cùng Brain Sync.
- **Không ảnh hưởng cuộc gọi khác.** Giọng được chọn theo phiên cộng sự; cuộc gọi TISA Core và Live API khác tiếp tục theo cài đặt hiện tại.
- **Cuộc trò chuyện chưa đọc có chấm đỏ.** TISA BOT trả lời xong mà chưa mở xem thì hàng đó trong lịch sử trò chuyện hiện chấm đỏ và tiêu đề in đậm hơn, ở cả trang Trò chuyện lẫn cột lịch sử của trang Cộng sự.
- **Mở cuộc nào là hết chấm cuộc đó.** Đang xem đúng cuộc nào thì tin mới về cũng không hiện chấm, và đã đọc ở tab này thì tab khác cũng tự tắt chấm.
- **Số tin chưa đọc ở danh sách Nhóm và Cộng sự đổi sang màu đỏ.** Nhóm hoặc cộng sự đã tắt thông báo vẫn giữ màu xám.
- Cuộc trò chuyện cũ có từ trước bản này tính là đã đọc, nên lịch sử không sáng đỏ cùng lúc.
- **Tắt lịch tự động trên riêng một máy.** Dùng TISA BOT trên nhiều máy chung một brain thì trước đây mỗi lịch chạy một lần trên mỗi máy đang bật. Nay ở mục Lặp lại của trang Nhiệm vụ có nút tắt lịch cho máy đang dùng, các máy khác vẫn chạy bình thường.
- **Nút Đẩy lại** trong bảng GitHub của cuộc chat, cho lần đẩy đang chờ thử lại.
- **Mã QR cho từng link chia sẻ.** Bấm icon QR trên mỗi hàng ở trang Link chia sẻ để hiện mã, quét bằng điện thoại là mở đúng link. Có nút tải ảnh PNG để in hoặc gửi đi.
- **Đổi được đường dẫn của link chia sẻ.** Bấm bút chì để sửa cả tên lẫn phần sau `/s/`, ví dụ `/s/vibecode-tisa`. Link mã ngẫu nhiên đã gửi đi vẫn mở được.
- **Đếm lượt xem từng link.** Mỗi hàng hiện số lượt xem, số người, 7 ngày gần nhất, lần xem cuối và biểu đồ 14 ngày. Bot xem trước link và chính chủ khi đang đăng nhập không bị tính.
- **Bong bóng chép lời sửa chữ ngay khi bạn đang nói (máy tính), ở chat chính, trang Nhóm và trang Chatbot.** Bong bóng mờ hiện chữ nghe được, rồi đổi sang bản đã sửa vài khoảnh khắc sau: TISA BOT dùng Groq nếu bạn đã gắn khoá, không thì dùng model nền. Dừng ghi là ô chat nhận đúng bản đã sửa. Server không trả lời thì chữ giữ nguyên như nghe được.
- **Tích việc có tiếng "tách, ting" nghe đã tai.** Việc ưu tiên có thêm chuỗi tiếng lấp lánh. Tích thói quen nghe tiếng lửa bùng lên, có tia lửa cam bay ra. Phá băng thì nghe tiếng băng nứt rồi chuông pha lê, mảnh băng xanh văng ra trước khi lửa cháy lại. Ngày sạch việc có đoạn nhạc mừng ngắn. Âm thanh tạo ngay trong trình duyệt, không tải file nào, tab ẩn thì im lặng.
- **Nút bật/tắt âm thanh cạnh nút sáng/tối.** Loa có sóng là đang bật, loa gạch chéo là đang tắt. Chỉ bật hoặc tắt, không có chỉnh âm lượng. Bật lên nghe ngay một tiếng "ting". Trên điện thoại nút nằm ở chân menu, ngay trước nút sáng/tối.
- **Việc của tôi giờ được nhắc qua chuông thông báo (và Telegram, thông báo điện thoại).** Việc có giờ được nhắc đúng giờ. Việc lặp lại được nhắc vào mỗi ngày của nó, trừ ngày đã xong hoặc đã bỏ qua.
- **Mỗi sáng 07:30 có một tin tóm tắt:** mọi việc và lịch hẹn hôm nay theo thứ tự giờ, kèm số việc còn quá hạn.
- **Khung chat bị chuyển model thì khung đó chuyển theo luôn.** Khi model đã chọn hết lượt và TISA BOT chuyển sang thẻ dự phòng, chip đổi sang tên model dự phòng với chấm cam, dấu tick trong bảng chọn, chip Effort, vòng hạn mức gói và lệnh `/model` cũng theo model đang chạy. Kéo thanh Effort lúc đó là chỉnh mức của chính model dự phòng. Rê chuột (hoặc giữ) vào chip để xem model đã chọn, hết lượt tới mấy giờ, và model đang chạy.
- **Một dòng ngắn trong chat khi đổi đường**, ví dụ "Antigravity hết lượt → đang dùng Claude Code". Dòng chỉ hiện ở lượt đầu tiên đổi, không lặp lại mỗi câu. Khi model đã chọn có lượt lại, chat báo một dòng "đã quay về" và chip tự xanh lại.
- **Bảng chọn model có nhãn "Hết lượt" và "Đang chạy"** cạnh tên từng nhà, để biết ngay nhà nào đang nghỉ và nhà nào đang làm thay.
- **Cloudflare có sẵn trong TISA BOT, không phải cài từ Kho nữa.** Trang Kết nối, tab Sẵn có, có thẻ Cloudflare với hai cách: dán API token, hoặc bấm Kết nối rồi đăng nhập Cloudflare và tick quyền ngay trên trang của Cloudflare. Mặc định Chỉ đọc, công cụ `execute` vẫn ở nhóm nguy hiểm.
- **Máy đã cài gói Cloudflare từ Kho vẫn chạy như cũ.** Kết nối đang có chuyển sang bản dựng sẵn, không báo lỗi trùng.
- **OpenAI Compatible thêm được nhiều key.** Đây là đường API key nâng cao: mỗi key một địa chỉ (NVIDIA Build, Kimi, OpenRouter, LiteLLM...), TISA BOT tự lấy danh sách model của từng cổng, key đang dùng hết lượt thì tự sang key kế. Cổng nào không báo danh sách model thì mở thêm ô gõ tên model.
- **Skill hệ thống mới `security-audit`.** TISA BOT giờ có sẵn quy trình rà soát bảo mật của Cloudflare trong mọi brain: hỏi nhanh về bảo mật thì chỉ dùng phần liên quan, còn bảo "audit bảo mật repo này" thì chạy đủ 6 bước (dò kiến trúc, săn lỗi theo vùng, kiểm chứng độc lập từng lỗi, xuất báo cáo kèm cách sửa). Giấy phép MIT, ghi nguồn đầy đủ.
- **Việc nền Toàn quyền chạy bằng API key có terminal thật.** Task, nhắc hẹn hay workflow ở mức Toàn quyền giờ chạy được lệnh máy trong brain (ffmpeg, python, script dựng video...) và vẫn tìm, đọc được web, đúng như khi chạy bằng Claude Code. Việc chạy lâu thì để chạy nền, xong TISA BOT báo về khung chat đã giao việc hoặc TISA Core. Mức Tự động, Gợi ý và loop bị cô lập vẫn không có lệnh máy.
- **Trang Model làm mới theo kiểu trang Nhiệm vụ.** Mỗi thẻ có logo thật của nhà cung cấp, hàng nút có icon (Dùng cho việc nền, Kiểm tra, Thêm tài khoản hay key, Ngắt) và nút ⋯ mở bảng kéo từ dưới lên với đủ thao tác. Thẻ chạy việc nền mang nhãn VIỆC NỀN.
- **API key nâng cao.** Cắm nhiều key của các nhà bán khác nhau (Kimi, MiniMax, bên bán lại Claude...), mỗi key một địa chỉ. Key đang dùng hết lượt thì TISA BOT tự sang key kế.
- **Antigravity có nút Ngắt, và thêm được tài khoản Google** trên máy Linux hoặc VPS để xoay vòng khi một tài khoản hết lượt.
- **Menu linh vật tự sắp xếp được.** Vào Cài đặt, tab Linh vật, thẻ Menu linh vật: bấm "Thêm chức năng" để đưa các trang khác của TISA BOT (Nhiệm vụ, Tệp tin, Kết nối, Models...) vào menu, rồi kéo thả hoặc bấm mũi tên để đổi thứ tự.
- Bấm **Lưu thay đổi** là menu dùng ngay ở lần mở sau, không cần khởi động lại, và giữ nguyên sau khi tải lại trang. Rời trang khi chưa lưu thì TISA BOT hỏi lại trước.
- Chưa từng chỉnh thì menu vẫn là sáu mục như cũ. Mục nào tạm chưa dùng được (ví dụ trình duyệt chặn mic) vẫn nằm đúng chỗ, mờ đi và ghi rõ lý do.
- **TISA BOT sửa được mọi thứ trong Việc của tôi ngay từ chat:** đổi việc lặp thành lịch hẹn (và ngược lại), đổi ngày giờ, giờ kết thúc, lặp, địa điểm, nhắc trước, tag, ghi chú, bật tắt thói quen, gắn sao, xoá và bỏ qua một lần.
- **Lịch hẹn có icon thao tác như việc:** Dời và Xoá, lịch hẹn lặp có thêm Bỏ qua lần này (Dời và Bỏ qua chỉ đụng lần đó). Sự kiện từ Google Calendar có icon mở trong lịch.
- **Ô trả lời khách ở trang Chatbot có nút micro chép lời.** Bấm micro rồi nói, chữ hiện thẳng vào ô. Bấm lại để dừng, sửa chữ nếu cần rồi bấm Gửi, hoặc bấm A.I. soạn để chữ vừa nói thành lệnh cho A.I. Không có gì tự gửi đi. Bấm Gửi lúc đang nghe thì TISA BOT dừng nghe rồi gửi luôn.
- **Đặt tên riêng cho TISA Core.** Bấm bút chì cạnh tên trên thẻ TISA Core ở trang Cộng sự, hoặc nói trong chat ("từ giờ tên em là Mây"). Mỗi brain một tên, để trống là về lại TISA Core.
- **TISA Core tự xin tên ở lần chat đầu** và nhớ phong cách nói chuyện bạn thích, chỉ hỏi một lần.
- **Lượt chat chạy lâu xong thì rung chuông và báo lên điện thoại.** Lượt từ 3 phút trở lên, hoặc lượt TISA BOT tự làm tiếp sau việc nền, để câu trả lời vào hòm thư và đẩy thông báo. Máy đang mở TISA BOT ngay trước mặt thì không hiện thông báo. Đổi mốc bằng `TISA_LONG_TURN_NOTIFY_S` (0 là tắt).
- **Dải "Nhịp hôm nay" trên mọi danh sách Việc của tôi:** 4 ô Ngày sạch, Ưu tiên, Hôm nay, Thói quen (bấm được), kèm câu của ngôi sao theo từng mục.
- **Chuỗi Ngày sạch:** ngày nào mọi việc đều được làm, dời, bỏ qua hoặc xoá và xong ít nhất 1 việc thì thêm lửa. Sót việc thì đóng băng, sót 2 ngày liền mới mất chuỗi.
- **Gắn sao tối đa 3 việc ưu tiên mỗi ngày.** Việc lặp có Bỏ qua lần này (nhảy sang lần sau, không tính lửa). Mọi việc có sẵn icon Dời và Xoá, bỏ nút "Dời tất cả".
- **Phần thưởng khi xong việc:** dấu tích nảy, sao vàng cho việc ưu tiên, lời khen bất ngờ, màn ăn mừng Sạch bảng, Sạch quá hạn và mốc số việc. Trang trống thì TISA BOT gợi ý việc để thêm.
- **Tên gói ChatGPT và Grok tự cập nhật.** CLI của OpenAI chỉ gửi mã gói, và mã không khớp tên đang bán (mã "prolite" là gói 100 đô). Nay TISA BOT tra tên trong danh bạ tên gói đặt ở kho tisa-store, tải về 6 giờ một lần, chạy ngầm, không làm chậm trang nào. Nhà cung cấp đổi tên thì chỉ cần sửa danh bạ, mọi máy thấy tên mới mà không cần bản cập nhật. Claude vẫn ưu tiên tên lấy thẳng từ Anthropic; mã chưa có trong danh bạ thì TISA BOT viết gọn mã như trước.
### Sửa lỗi
- **Mở hội thoại ở trang Cộng sự hết báo nhầm "mở quá lâu".** Lúc trang đang tự kết nối lại thì không báo lỗi nữa. Mở TISA Core bị treo thì báo lỗi kèm nút Thử lại, và bấm Thử lại là tải lại thật thay vì chờ tiếp lượt đang treo.
- **Việc nền chạy bằng ChatGPT (Codex) bị chặn ghi file giờ báo đúng là lỗi môi trường**, kèm cách sửa, thay vì nằm ở "chờ bạn trả lời".
- **Ký ức do việc nền ghi không còn bị gắn nhầm nguồn** là cuộc chat đang mở cùng lúc.
- **ChatGPT (Codex) không còn mất công cụ khi chat nghỉ vài phút rồi nhắn tiếp.** Lịch, Zalo, Drive dùng được ngay ở lượt sau. Trên Windows, việc nền Codex mức "Được ghi" ghi được file trở lại.
- **Ký ức không còn bị hỏng hay mất thông tin sau lượt chat.** Ký ức có dấu hai chấm trong mô tả giữ nguyên loại, mô tả và thẻ. Ký ức đã hỏng từ trước tự lành khi sửa trong app.
- **Ollama Local chạy được việc nhóm và việc nền.** Hết báo "engine chưa sẵn sàng" khi Ollama ở máy nhà không đặt khoá.
- **Kết nối ổn hơn:** chạy sau Caddy (VPS Hostinger) thì nút Đăng nhập Facebook không còn bị khoá, thẻ CapCut đăng nhập được, GitHub trong chat dùng đúng Lệnh kiểm tra đã lưu và hiểu repo đặt app trong thư mục con.
- **Chatbot tra tài liệu, lượt học tự động và nhắc việc không còn làm cả app đứng vài giây.** Các việc này giờ chạy ở luồng phụ và không còn quét cả brain.
- **Trang Cộng sự không còn chờ khoá dữ liệu Cộng hưởng**, và danh mục kết nối không còn kiểm tra lại ổ đĩa ở mọi lần gọi.
- **Khối chữ (như khối TEXT của email nháp) tự xuống dòng** thay vì kéo dài sang phải. Lúc đang sửa, vuốt ngang bàn di chuột không còn làm trình duyệt lùi trang.
- **"Đang soạn tin" ở chat riêng không còn tắt cả tiếng.** Trước đây chỉ một cuộc chat bị Zalo từ chối, hoặc MCP khởi động lại, là dấu này tắt ở mọi cuộc chat của nick suốt một giờ. Giờ chỉ tắt cho đúng lượt đó, và dấu được giữ tới khi tin đã gửi đi.
- **Nút "Nhập tin cũ" của Zalo nhập được thật.** Trước đây cuộc chat nào đã có dù chỉ một tin trong Hộp thư đều bị bỏ qua, nên tài khoản đã bật Ghi hội thoại bấm nhập gần như không được gì. Giờ cuộc chat đã có tin nhận thêm các tin cũ hơn tin đầu tiên của nó, xếp lên trên đúng thứ tự thời gian.
- Tin cũ vừa nhập không nhảy xuống cuối khung chat đang mở, không làm bot hiểu nhầm là tin mới, và nhóm vẫn chỉ giữ các tin gần nhất như cũ.
- **Chấm trạng thái trên thẻ cộng sự khớp với tab Công việc.** Việc anh đã bấm Xong (cất vào lưu trữ) hay đã xoá không còn làm chấm xanh "vừa xong" (hay chấm đỏ khi việc đó hỏng) sáng lên nữa.
- **Ô chat ở trang Cộng sự không còn bị khoá.** Từ bản 0.503, bấm vào một cộng sự (hay vừa trả lời xong) đôi khi làm ô chat không nhận con trỏ nữa, Ctrl+Shift+R cũng không đỡ. Nay mở hội thoại lại ngay như cũ.
- **Mở hội thoại quá lâu thì có báo lỗi kèm nút Thử lại**, thay vì một ô chat khoá im lặng.
- **Lên bản mới là trình duyệt tự làm mới bộ nhớ đệm của TISA BOT**, không phải bấm Ctrl+Shift+R.
- **Review chéo trên GitHub chạy bằng đúng model bạn đã chọn.** Trước đây nó gửi model rỗng, nên thẻ Groq rơi về `llama-3.3-70b-versatile`, model Groq đã tắt từ 16/08/2026, và lần review nào cũng báo 404 rồi bỏ qua. Giờ model việc nền review trước (nếu khác hãng với engine đã viết), các thẻ khác dùng model và mức suy nghĩ chọn trên thẻ. Khung chat ghi rõ tên model đã review.
- **Model mặc định của Groq đổi sang `openai/gpt-oss-120b`**, model Groq khuyên dùng thay cho `llama-3.3-70b-versatile`.
- **Chép lời không còn dừng khi chuyển tab.** Đang ghi âm thành chữ mà Alt Tab hay chuyển sang trang khác, máy tính vẫn nghe tiếp, quay lại là chữ vẫn đủ.
- **Trên điện thoại, quay lại là ghi tiếp.** Điện thoại tắt mic khi trình duyệt chạy nền, nên đoạn nói lúc ở app khác không nghe được. Nhưng đoạn đã ghi không bị mất, và mic tự mở lại khi quay về TISA BOT, không cần bấm lại.
- **Cập nhật xong không còn "mất" nhóm.** Trang mở lại đúng lúc máy chủ đang khởi động thì TISA BOT lặng lẽ chuyển sang Brain Default, nên trang Nhóm hiện nhóm của brain khác và nhóm mới tạo cũng rơi vào đó. Nay TISA BOT luôn mở đúng brain anh chị đã chọn, và tự thử lại tới khi lấy được danh sách brain.
- Dữ liệu nhóm chưa từng bị xoá: nhóm nào "biến mất" trước đây vẫn nằm ở brain còn lại, chọn brain đó ở ô chọn brain là thấy.
- **Việc nền trượt lượt tự kiểm không còn hiện ô "Gõ câu trả lời" trống.** Trước đây việc chạy xong mà máy tự kiểm thấy chưa đạt thì chuyển sang "cần bạn trả lời" dù chẳng có câu hỏi nào.
- **Trượt lần đầu, việc tự quay lại cho người làm sửa** theo đúng lý do máy chấm, bạn không bị làm phiền.
- **Trượt lần hai mới tới bạn**, thẻ ghi rõ "Máy tự kiểm chưa qua" kèm hai nút: **Sửa rồi chạy lại** hoặc **Chấp nhận như vậy**. Bấm kiểm lại một việc đã xong mà trượt thì cũng hiện hai nút này.
- **Tin Zalo không còn lọt khỏi Hộp thư sau mỗi lần rớt mạng ngắn.** TISA BOT dùng tisa-zalo 1.9.1. Trước đây khi kết nối Zalo rớt dưới 5 giây rồi tự nối lại, tin nhắn trong lúc đó chỉ vào kho lịch sử, không tới Hộp thư và bot. Giờ chúng tới ngay như tin thường. Một tin lỗi cũng không còn kéo mất các tin đi cùng lô với nó.
- **Bot không còn gửi câu "You've hit your monthly spend limit" cho khách.** Khi gói Claude hết cả hạn mức chi thêm theo tháng, Claude Code in ra một câu mới mà TISA BOT chưa nhận ra, nên bot Zalo dán nguyên câu tiếng Anh đó vào tin trả lời khách. Nay câu này được coi là lượt hỏng như mọi câu báo hết lượt khác: khách không nhận gì, chủ được báo ở chuông thông báo. Khung chat, việc Kanban và workflow cũng nhận ra nó là hết lượt gói, kèm giờ mở lại.
- **Câu báo hết lượt có dấu nháy cong (You’ve) cũng được nhận ra** như dấu nháy thường.
- **Chat từ Zalo và Telegram (Kênh Admin) nay hiện trong lịch sử của TISA Core**, còn chat gọi một cộng sự thì hiện trong lịch sử của cộng sự đó, có nhãn TG hoặc zalo.
- **Lệnh `/brain`, `/reset`, `/stop`, `/model` trên bot Zalo admin tác động đúng cuộc chat đang nói.** Trước đây chúng đổi nhầm một phiên khác nên chat có thể rơi sang brain mặc định.
- **Bot chuyên trách không được dùng chung token với bot Zalo admin nữa.** Dùng chung khiến tin nhắn bị chia đôi và một nửa chui vào hộp thư khách, mất khỏi chat của bạn.
- **App TISA BOT trên màn hình chính iPhone (iOS 26/27) hết vệt mờ ở trên cùng.** Thanh trạng thái giờ là nền đặc, trang bắt đầu ngay bên dưới nên iOS không còn gì để làm mờ.
- **Cần làm một lần:** xoá icon TISA BOT khỏi màn hình chính rồi mở Safari, bấm Chia sẻ, Thêm vào MH chính lại. iOS chỉ đọc kiểu thanh trạng thái lúc thêm icon.
- **Bot nghe được tin thoại Zalo.** Tin thoại Zalo là AAC thô, Groq và OpenAI từ chối nên bot báo "chưa nghe được". Giờ TISA BOT nhận dạng định dạng theo nội dung file và tự đổi sang mp3 trước khi gửi, áp dụng cho mọi kênh.
- **Mở trang và đổi hội thoại không còn khựng vài giây khi TISA BOT đang làm việc nền.** Bộ điều phối Kanban (chạy 5 giây một lần) ghi kho việc ngay trên luồng chính của máy chủ, nên mỗi khi kho đang bận là mọi cú bấm phải đứng chờ theo, có lúc hơn 1 giây. Giờ phần đó chạy ở luồng phụ.
- **Lần tự cập nhật Claude Code không còn làm máy chủ đứng 3 giây.** Việc đọc danh sách model từ chương trình `claude` cũng chuyển sang luồng phụ.
- **Tin Zalo cá nhân không còn bị hụt trong Hộp thư.** Có lúc một cuộc chat riêng dừng ở một tin, trong khi điện thoại vẫn nhắn tiếp cả hai chiều. Cứ khoảng 1,5 phút TISA BOT tự so Hộp thư với kho lịch sử Zalo, thiếu tin nào thì bù tin đó, kể cả tin anh chị tự gõ trên điện thoại. Tin bù hiện chưa đọc, không giao cho bot trả lời muộn, không trùng với câu bot đã gửi, và không đè dòng tin cuối của cuộc chat.
- **Antigravity CLI không còn tự dừng ở phút thứ 15.** Việc nặng, nhiều bước giờ chạy tới khi xong, giống Claude Code và Codex. Nút Dừng vẫn cắt được bất cứ lúc nào.
- Muốn đặt lại trần thì dùng biến môi trường `TISA_AGY_TIMEOUT` (giây). Mức chỉ đọc vẫn giữ lưới 15 phút vì nó không tự duyệt tool.
- **Tự chuyển sang tài khoản Claude thứ hai giờ chạy được thật.** Trước đây tài khoản 1 hết lượt thì TISA BOT có chọn tài khoản 2, nhưng vẫn cố mở lại mạch hội thoại cũ vốn nằm trong thư mục của tài khoản 1. Claude Code không tìm thấy mạch đó nên thoát ngay, và mọi tin nhắn sau đều báo "SDK engine: ProcessError: Command failed with exit code 1". Nay TISA BOT nhận ra mạch thuộc tài khoản khác, mở mạch mới trên tài khoản đang chạy và mồi lại ngữ cảnh từ lịch sử đã lưu, nên hội thoại chạy tiếp như bình thường.
- **Mạch cũ bị mất cũng được khôi phục dù Claude Code báo bằng lỗi thoát.** Bản Claude Code mới báo "No conversation found" bằng cách thoát mã 1 thay vì trả kết quả lỗi, nên đường khôi phục ngữ cảnh trước đây không chạy. Nay cả hai cách báo đều được nhận ra.
- **PR đã merge không còn kẹt biểu tượng "đang chờ CI".** Khi PR được merge lúc TISA BOT mất kết nối GitHub, khung chat từng giữ mãi biểu tượng nhánh đang làm. Giờ nó đổi sang biểu tượng đã merge, và `tisa_github` không còn báo "chờ CI" cho PR đã merge.
- **CI không còn đỏ oan vì phép đo tốc độ khởi động.** Test cũ bấm giờ lúc nạp server và đỏ ngẫu nhiên khi máy chạy chậm. Nay nó liệt kê các thư viện được nạp lúc khởi động: không còn phụ thuộc tốc độ máy, và khi có thư viện nặng lọt vào thì nó gọi đúng tên.
- **Khung chat không còn kẹt ở "Mất kết nối tới máy chủ" hàng giờ.** Trước đây một tin máy chủ xử lý lỗi làm đứt kết nối, trang nối lại rồi gửi lại đúng tin đó, lại đứt, lặp mãi, khởi động lại máy chủ cũng không hết. Nay máy chủ báo lỗi ngay dưới tin đó và kết nối vẫn chạy.
- **Một tin gửi 3 lần không được nhận thì trả về ô nhập**, không gửi lại vô hạn nữa.
- **Phiên đăng nhập hết hạn thì hiện màn đăng nhập**, thay vì báo mất kết nối mãi và mọi danh sách về 0.
- **Brain đặt trên Google Drive, OneDrive đỡ làm đứng máy chủ:** phần quét thư mục đầu và cuối mỗi lượt chat chạy riêng, không chặn kết nối nữa.
- **Gọi thoại với cộng sự không còn tự nhận là ChatGPT.** Danh tính của cộng sự giờ đứng đầu lời dặn của cuộc gọi, nên hỏi "bạn là ai" (cả bằng tiếng Anh) là cộng sự trả lời đúng tên mình.
- **Cuộc gọi với cộng sự không còn kéo theo bộ nhớ chung của brain chính,** chỉ dùng hướng dẫn và trí nhớ riêng của cộng sự đó, nên không lạc sang chuyện không thuộc vai của nó.
- **Agent trong quy trình chưa chọn model riêng giờ chạy bằng model chính.** Trước đây bước đó luôn chạy bằng Claude, dù trang Models đang chọn não khác. Agent đã chọn model riêng vẫn giữ nguyên lựa chọn đó.
- **Đẩy code lên GitHub hỏng một lần không còn kẹt luôn.** Trước đây sau một lần đẩy lỗi, các lượt chat sau coi như "không có gì đổi" nên không bao giờ đẩy lại, kể cả khi đã đăng nhập GitHub lại. Giờ TISA BOT tự đẩy lại ở lượt chat kế tiếp, định kỳ vài phút một lần, và ngay khi GitHub được kết nối lại, rồi mở PR, chờ CI và tự merge như thường.
- **Lỗi đẩy nói bằng lời dễ hiểu.** Thay cho câu git `could not read Username`, TISA BOT nói rõ là thiếu đăng nhập hay thiếu quyền ghi vào repo, và cần làm gì ở trang Kết nối.
- **Bấm Merge rồi đóng bảng, PR vẫn được merge.** Trước đây đóng bảng chi tiết GitHub (hay đóng tab) ngay sau khi bấm Merge là lệnh merge bị huỷ giữa chừng. Giờ TISA BOT merge tiếp ở nền và báo kết quả vào khung chat.
- Mở lại bảng khi đang merge sẽ thấy "Đang merge...", không hiện nút Merge lần nữa nên không merge trùng.
- **Nút ở trang 2 trở đi của danh sách link bấm lại được.** Trước đây chỉ trang đầu bấm ăn.
- **Gõ xong bấm Enter rồi vuốt sang app khác trên điện thoại, câu hỏi không còn biến mất.** Trước đây điện thoại có lúc để kết nối chết ngầm, câu hỏi không tới máy chủ nên quay lại thì cả đoạn mất sạch, Lịch sử cũng không có. Nay máy chủ xác nhận từng câu đã nhận, câu nào chưa được xác nhận thì TISA BOT tự gửi lại khi nối lại, và không bao giờ chạy trùng hai lần.
- **Biểu tượng GitHub trong danh sách chat không còn kẹt màu cam sau khi đã merge.** Khung chat có hai repo mà chỉ một repo có việc thì giờ hiện đúng màu "đã merge". Repo kia nếu chưa đụng tới thì không kéo trạng thái lệch đi nữa.
- **Repo bị chặn ở bước kiểm tra trước khi đẩy giờ hiện màu đỏ "cần người xem"**, kèm lý do. Trước đây nó cứ nhấp nháy cam như đang làm, nhất là sau khi khởi động lại TISA BOT, trông như TISA BOT bỏ quên repo đó.
- **TISA BOT đẩy nhánh lên GitHub được ngay cả khi repo có bài kiểm tra dành cho máy Mac hay Windows.** Trước đây máy Linux cũng chạy thử bài cài đặt của Mac, bài đó treo rồi báo đỏ nên TISA BOT dừng đẩy, dù thay đổi chẳng liên quan. Giờ bài của hệ điều hành khác để CI trên GitHub chạy, rồi CI xanh là TISA BOT tự merge như thường.
- **TISA BOT nghe đúng tên các sản phẩm AI hơn.** "Groq", "Grok", "Claude", "ChatGPT", "Gemini", "OpenRouter"... ra đúng chính tả, và nói "Groq" không còn bị đổi thành "Grok".
- **"Jarvis OS" giờ ra đúng "TISA BOT".**
- **Chép lời trên Android không còn mất chữ.** Bản trước bỏ mất câu ngắn nói sau một câu dài (nói "tôi về rồi" rồi "tôi" thì mất chữ "tôi"). Giờ chữ được dựng lại từ toàn bộ những gì máy nghe, mà vẫn không lặp kiểu "tôi tôi bị".
- **Menu trên iPhone không còn chồng chữ.** Ở cuối menu, nhóm "Hệ thống" từng đè lên ô chọn ngôn ngữ (thấy rõ trên Safari). Giờ mỗi thứ nằm một hàng riêng, menu dài thì cuộn xuống như thường.
- **App thêm vào màn hình chính bớt cảnh "đơ".** Có lúc mở lên, iPhone đẩy lệch cả trang nên chạm đâu cũng trượt khỏi nút. Giờ TISA BOT tự kéo trang về đúng chỗ khi mở app, khi quay lại từ nền và ngay lúc bạn chạm.
- **Gọi giọng không còn kẹt ở ChatGPT Live khi gói ChatGPT hết lượt.** Trước đây cuộc gọi cứ mở lại đúng tài khoản đã cạn và báo lỗi "You've hit your usage limit" mãi, dù đã đổi model chính sang gói khác. Giờ tài khoản đó được cho nghỉ tới giờ mở lại, cuộc gọi tự chuyển ngay sang tài khoản ChatGPT thứ hai, hết nữa thì sang Live qua API key, rồi đường Cơ bản (trả lời bằng model chính).
- **ChatGPT Live dùng được tài khoản ChatGPT thứ hai.** Trước đây gọi giọng chỉ chạy trên tài khoản 1.
- **Đường Cơ bản không chọn lại ChatGPT đã hết lượt** làm bộ não trả lời nhanh: chờ tới giờ mở lại, lượt nói đi bộ não khác.
- **Lỗi hết lượt chỉ hiện một lần**, kèm giờ mở lại đọc từ câu "try again at 8:42 AM" (đường chat cũng đọc được giờ này).
- **Thói quen bị quá hạn có nút Bỏ qua và Xoá.** Trước đây một lần lỡ của thói quen (ví dụ "Chạy bộ 3 buổi / tuần") nằm trong ô Quá hạn mà không có nút nào. Giờ có Bỏ qua lần này và Xoá, như mọi việc lặp quá hạn khác.
- **Nút + không còn che việc cuối danh sách.** Trang Nhiệm vụ chừa khoảng trống ở dưới cùng, nên các nút Dời, Xoá, sao của việc cuối luôn bấm được.
- **Nút + thêm việc trên điện thoại hạ xuống sát góc, không còn đè lên công tắc "Đang bật" của loop.** Cuối trang Nhiệm vụ có thêm khoảng trống, nên dòng cuối cùng luôn cuộn lên được phía trên nút.
- **Lịch hẹn để trống ô nhắc giờ được nhắc trước 15 phút**, đúng như trang vẫn hiển thị. Trước đây lịch hẹn TISA BOT tạo từ chat không bao giờ được nhắc. Chọn "Không nhắc" thì vẫn không nhắc.
- **Review chéo khi TISA BOT làm việc trên GitHub không còn báo "không chạy được" mỗi lần.** TISA BOT từng chọn gói ChatGPT để review code do Claude viết, nhưng bước review chỉ cho chạy engine không có công cụ đọc ghi file, nên gói ChatGPT (cũng như Grok Build, Antigravity) luôn bị chặn. Giờ TISA BOT chỉ chọn Claude hoặc một nhà dùng API key khác họ, bỏ qua thẻ đang hết lượt, và một reviewer hỏng thì thử reviewer kế tiếp.
- **Bỏ qua review thì nói rõ vì sao**, kèm lý do lỗi, và khi không có engine nào review được thì chat chỉ cách bật: thêm API key của một nhà khác họ (OpenAI, Gemini, DeepSeek, OpenRouter...).
- **Quay lại khung chat đang chạy không còn bong bóng rỗng.** TISA BOT đang làm mà bạn sang khung chat khác rồi quay lại, trước đây phía trên dòng tiến trình mọc ra một bong bóng trả lời trống. Giờ chỉ còn các bước đã chạy và dòng tiến trình, bong bóng hiện ra khi TISA BOT bắt đầu viết.
- **Mục Trò chuyện trên đầu thanh bên không còn hiện `page.chat.label`.** Ngay sau khi cập nhật, lúc máy chủ còn đang khởi động, từ điển về chậm và mục này giữ nguyên khoá thô. Giờ mọi mục trên thanh bên tự đổi chữ khi từ điển về.
- **Ô chọn ngôn ngữ ở chân thanh bên trái hết dính vào hàng phiên bản.** Ô và hàng phiên bản giờ chung một đường kẻ, cách nhau đều, ô cao bằng nút thu/mở và chữ to hơn chút cho dễ đọc. Khi chỉ có một ngôn ngữ, ô trống không còn hiện ra.
- **Thẻ Claude Compatible quay lại.** Bản 0.477.0 đổi tên nó thành "API key nâng cao" nên đường Claude Compatible biến mất. Giờ nó là thẻ riêng như cũ, vẫn thêm được nhiều key, key đã lưu giữ nguyên.
- **Đọc chữ trên Android không còn lặp kiểu "tôi tôi bị tôi bị học".** Một số máy Android gửi lại cả câu mỗi lần nghe thêm một chữ, TISA BOT từng ghép hết các bản nháp đó vào ô chat. Giờ chỉ giữ câu cuối cùng.
- **Đang bật mic ghi âm thành chữ, ấn Enter là gửi luôn.** Không cần ấn nút dừng trước: TISA BOT dừng ghi, chờ nốt chữ cuối rồi gửi. Áp dụng cho ô chat chính, ô trả lời khách ở trang Hội thoại và chat Nhóm.
- Trên điện thoại Enter vẫn là xuống dòng như cũ, bấm nút gửi để gửi.
- **Gắn sao trước cho việc ngày mai được rồi.** Sao ưu tiên giờ tính theo ngày của chính việc đó: mỗi ngày tối đa 3 sao riêng, sao của hôm nay không còn chặn việc gắn sao cho ngày mai, và gắn sao việc ngày mai thì việc vẫn nằm ở ngày mai (trước đây bị kéo về hôm nay). Chỉ việc chưa có ngày hoặc đã quá hạn mới được đưa về hôm nay khi gắn sao.
- **Việc nền chạy bằng API key không còn dừng ở vòng 30.** Task, loop, workflow, team dùng OpenRouter, OpenAI, Anthropic API, Gemini, Groq, DeepSeek hay Ollama giờ có 500 vòng công cụ mỗi lượt như khung chat, nên điền cả trăm dòng Google Sheet hay dựng video chạy được tới hết thay vì báo "đã chạy hết 30 vòng" rồi bỏ dở.
- **Gói Google hết lượt thì chat chuyển sang thẻ khác thật.** Trước đây TISA BOT không đánh dấu Antigravity hết lượt, nên cứ chạy lại nó và báo "chưa có bộ não nào khác" dù ChatGPT đang đăng nhập.
- **Chọn ChatGPT là ChatGPT chạy.** Một dấu "hết lượt" cũ không còn kéo chat về Google: chọn thẻ nào thì thẻ đó được thử, và thẻ đang tạm nghỉ hiện rõ tới mấy giờ kèm nút Dùng lại ngay.
- **Mở file PDF trên iPhone, iPad không còn bị kẹt.** Trước đây bấm link PDF trong chat ở app cài ra màn hình chính thì PDF đè lên cả TISA BOT, không có nút quay lại, không có nút tải về, phải tắt app mở lại. Giờ PDF mở trong khung xem ngay trong TISA BOT: có nút đóng, vuốt hay bấm quay lại cũng đóng được, và nút Tải về mở bảng chia sẻ để lưu vào Tệp hoặc gửi đi.
- **Chữ in đậm trong link hiện đúng.** Link kiểu `[**Tải file**](...)` không còn lộ hai dấu sao.
- **Codex không còn đếm trùng token.** Codex có lúc báo số dùng lặp lại cho cùng một request, TISA BOT từng cộng cả lần lặp nên số token của lượt bị thổi lên. Nay chỉ tính phần tăng thật. Ý tưởng và bản đầu của kubintran (#999).
- **Xoay mạch Codex nhìn đúng độ dài mạch.** Trước đây TISA BOT lấy tổng token của cả lượt, nên một lượt chạy nhiều vòng tool trông như mạch rất dài. Nay lấy input của request cuối mà Codex đo được; không đo được thì dùng số cũ như trước. Xoay mạch vẫn bật như cũ.
- **Gọi thoại với cộng sự nay đúng là cộng sự đó.** Trước đây bấm gọi trong khung chat của một cộng sự thì giọng nói vẫn là TISA BOT chung, không biết tên, vai hay hướng dẫn của cộng sự, hỏi "em là ai" còn đáp "em là ChatGPT". Nay cuộc gọi mang tên, vai, file hướng dẫn và bộ nhớ của cộng sự.
- **Việc giao trong cuộc gọi do chính cộng sự làm.** Câu cần tra dữ liệu hay hành động chạy bằng prompt và model của cộng sự, kết quả về đúng khung chat của cộng sự.
- **Chat gõ chữ với cộng sự cũng biết mình là ai.** Cộng sự hiểu mình là cộng sự trong TISA BOT của chủ, không tự nhận là ChatGPT hay Claude, chỉ nói tên model khi được hỏi rõ.
- **Chip model trong chat TISA Core không còn báo ghim giả.** Chat TISA Core chưa ghim mà gửi một tin là chip hiện dấu ghim, trông như đã ghim nhưng thật ra vẫn theo model chính, nên đổi model ở khung chat chính thì TISA Core đổi theo. Giờ chip nói đúng: chưa ghim là theo model chính, chọn một model ở đây mới là ghim riêng.
- **Chọn quá giới hạn không còn mất Trang âm thầm.** Trước đây tích hơn 20 tài khoản thì bot chỉ giữ 20, số còn lại bị bỏ mà không báo. Giờ TISA BOT từ chối và nói rõ kênh nào đang quá, bot giữ nguyên như cũ.
- **Cài lại trợ lý từ Kho nay hiện lại ở trang Cộng sự.** Trước đây đổi tên hay sửa trợ lý của gói, gỡ rồi cài lại thì TISA BOT lặng lẽ bỏ qua. Nay bản của bạn giữ nguyên, bản của gói được cài thêm dưới tên mới (ví dụ `tisa-vu-2`) và màn hình nói rõ tên đó.
- **Xoá trợ lý, quy trình, kỹ năng của gói trong app thì Kho thôi báo "Đã cài".** Thẻ hiện lại nút Cài để lấy lại.
- **Gỡ gói dọn sạch kỹ năng:** kể cả kỹ năng đang tắt và bản sao cho Claude Code, nên kỹ năng đã gỡ không còn được nạp ngầm.
- **Brain còn dùng thư mục cũ `TISA/agents`** cài trợ lý từ Kho không còn làm mất các trợ lý đang có.
- **Lịch nền chạy bằng ChatGPT (Codex) giao được việc cho Nhóm.** Trước đây một nhắc hẹn hay việc Kanban có bộ não nền là Codex gọi `tisa_team` mà không mang danh tính lượt, nên bị chặn với câu "lượt không có danh tính" và nhóm không bao giờ dậy làm việc. Giờ lượt nền mang khoá lượt tới hub như lúc chat, nên nhóm nhận việc đúng giờ.
- **Lệnh dài chạy ngầm (render, dựng video) giờ tự báo về khi xong, với mọi bộ não.** Trước đây TISA BOT không thấy lệnh ngầm của Claude Code, và có thể sót lệnh ngầm của Codex, Grok, Antigravity, nên không báo gì và lời dặn "xong thì làm tiếp" bị bỏ. Giờ mọi lệnh ngầm của khung chat đều được theo dõi: xong là báo vào đúng khung chat, kèm file mới, rồi tự làm tiếp phần đã hẹn.
- **Việc nền chạy quá 30 phút không còn bị dừng giữa chừng.** Hết giờ chờ thì lượt chat nhả ra, còn việc vẫn chạy tiếp và được theo dõi tới khi xong.
### Cải thiện
- **Trang Tài khoản gọn hơn.** Bỏ thanh tiêu đề trang, hai tab Tài khoản và Bảo mật nằm ngay trên cùng.
- **Token API cho CLI chuyển sang trang Tích hợp** (nhóm Việc, trước là Webhook), tab Token API. Cả hai đều là cửa để chương trình khác gọi vào TISA BOT nên giờ nằm chung một chỗ. Token đã tạo vẫn dùng như cũ.
- **Mở app nhanh hơn rõ rệt.** Khoảng 110 file giao diện lúc khởi động giờ đi chung một gói. Trên đường mạng có độ trễ 150ms, danh sách Cộng sự hiện sau khoảng 2 giây thay vì gần 5 giây.
- **Khởi động lại hay cập nhật xong không còn bị khựng ở lần mở đầu.** Bản nén gọn được lưu lại trên đĩa nên máy chủ không phải làm lại từ đầu, chỉ file nào vừa đổi mới phải nén lại.
- **Trang Cộng sự không còn đứng chờ cả loạt.** Các lệnh đọc danh sách, trạng thái Cộng hưởng và việc nền giờ chạy ở luồng phụ, không chặn các lệnh khác.
- **Review chéo trên GitHub giờ do bạn quyết, mặc định tắt.** CI xanh là TISA BOT merge, không tự gọi thêm model nào để review. Muốn review thì bật cho từng repo (thẻ GitHub, dấu ba chấm, Review chéo), bấm **Review ngay** ở biểu tượng GitHub của cuộc trò chuyện, hoặc nhắn "review PR này".
- **Mặc định review bằng chính model đang chat**, không bắt buộc phải là model khác hãng. Chọn model khác được, theo repo hay mỗi lần review.
- **Phát hiện chờ bạn chọn.** TISA BOT không tự gửi đi sửa nữa: dừng merge, hiện danh sách lỗi kèm hai nút **Sửa các lỗi này** và **Bỏ qua, merge**.
- **Chọn "chấp nhận" hay "sửa lại" ngay trong chat.** Việc nền trượt lượt tự kiểm hai lần thì tin báo về Telegram, Zalo hay khung chat web giờ cho bạn nhắn thẳng "chấp nhận" hoặc "sửa lại", không cần mở trang Nhiệm vụ. Nhiều việc cùng chờ thì TISA BOT hỏi lại là việc nào.
- **Agent nghe bằng tai của chính nó.** Agent chọn model hãng nào thì tin thoại gửi bot chuyên trách và lời đọc trong khung chat của agent đó được hãng ấy nghe, không mượn tai của bộ não chính.
- **Model nghe tự lên đời theo hãng, có chấm điểm trước.** Mỗi ngày TISA BOT hỏi Groq, OpenAI và Google danh sách model. Gặp bản mới, TISA BOT cho bản mới và bản đang dùng cùng nghe một bộ câu Việt xen Anh, bản mới không tệ hơn mới được dùng. Một tai hỏng thì tai kế tiếp nghe thay, câu nói không bị mất.
- **Giọng đọc tự theo thứ tiếng của câu trả lời.** Câu trả lời tiếng Anh do giọng nói được tiếng Anh đọc chuẩn, không còn "Vinglish". Câu trả lời tiếng Việt do Hoài My hoặc Nam Minh đọc, từ tiếng Anh xen trong câu vẫn đọc kiểu người Việt nói.
- Giọng anh chọn trong Cài đặt quyết định nam hay nữ: chọn Hoài My thì câu tiếng Anh do Emma đọc, chọn Andrew thì câu tiếng Việt do Nam Minh đọc. Tin nhắn thoại gửi qua Telegram cũng theo luật này.
- **Giao diện giờ chỉ còn tiếng Anh và tiếng Việt.** Bản dịch tiếng Đức đã được gỡ khỏi ô chọn ngôn ngữ. Máy nào đang để tiếng Đức sẽ tự về tiếng Anh.
- **Lúc TISA BOT đang trả lời hay đang chạy việc Kanban, các cú bấm khác không còn phải xếp hàng chờ.** Việc đọc ghi lịch sử hội thoại trong mỗi lượt chat (kể cả đọc lại cả cuộc dài để gửi cho model) và mọi lần ghi của việc Kanban giờ chạy ở luồng phụ, không chiếm luồng phục vụ giao diện nữa.
- **Các trang đọc nhiều (Tệp tin, bộ nhớ, sao lưu, tự học, nhắc hẹn, vòng lặp, nhóm hội thoại, tài sản trong chat...) không còn làm cả máy chủ khựng khi brain lớn.** Số chỗ làm việc nặng trên luồng chính giảm từ 347 xuống 218, Kanban về 0.
- Một test mới chặn không cho con số đó tăng trở lại.
- **Mở app, vào trang, đổi hội thoại giờ hỏi máy chủ một chuyến thay vì nhiều đợt nối tiếp.** TISA BOT học xem mỗi lúc như vậy cần đọc những gì, lần sau gửi gộp tất cả trong một lượt, máy chủ trả từng phần ngay khi xong. Đo qua mạng chậm: mở app từ 3,5 giây còn 2,6 giây, số lượt hỏi từ 47 còn 22; đổi hội thoại từ 5 lượt hỏi còn 1.
- Phần nào máy chủ không gộp được thì trang tự hỏi riêng như cũ, nên không có gì bị thiếu.
- **Mở lại hội thoại hiện ngay, kể cả sau khi tải lại trang.** TISA BOT giữ phần cuối của 50 cuộc gần nhất ngay trong trình duyệt, vẽ ngay từ đó rồi mới hỏi máy chủ bản mới. Đo qua mạng chậm: từ khoảng 0,3 giây xuống còn 0,03-0,04 giây.
- **Cuộc vừa dạy TISA BOT không còn phải tải lại từ đầu.** Rời một cuộc đang có tin mới thì TISA BOT lấy sẵn bản mới ở nền, TISA BOT trả lời xong ở cuộc khác cũng vậy. Các cuộc đầu danh sách được tải trước khi máy rảnh, kể cả trên điện thoại.
- **Quay lại các trang Kỹ năng, Kết nối, Kênh, Cài đặt, Models, Tự học, Plugin, Webhook hiện ngay.** Trang vẽ ngay dữ liệu lần trước rồi tự cập nhật nếu có gì đổi, trừ khi đã có thao tác bấm hay gõ trên trang. Đo qua mạng chậm: từ 0,3-0,7 giây xuống 0,02-0,1 giây.
- Đăng xuất là xoá các hội thoại đã giữ trong trình duyệt.
- **Bù tin Zalo cá nhân không còn chạy theo lịch.** TISA BOT chỉ để ý khi file lịch sử Zalo thật sự có tin mới, rồi chỉ xét đúng những tin đó. Ngày không có tin nào thì gần như không tốn gì (một lần xem kích thước file sau mỗi lượt đọc), không gọi Zalo, không quét các cuộc chat đã im.
- **Trang `/health/loop` ghi cả những lần khựng ngắn (từ 0,3 giây).** Mỗi lần được tính vào đúng chỗ code gây ra, xếp theo tổng thời gian mất, để lần sau thấy chậm là biết ngay vì đâu.
- **Bỏ hết trần thời gian của các model.** Grok không còn tự dừng ở phút 15, một lệnh của Claude Code hay ChatGPT không còn bị cắt ở 1 tiếng, việc nền và Nhóm cũng chạy tới khi xong. Nút Dừng vẫn cắt được bất cứ lúc nào.
- Muốn có trần lại thì đặt biến môi trường tương ứng (giây), ví dụ `TISA_GROK_TIMEOUT` hay `TISA_BG_MAX_WALL_S`. Bản Grok cũ không tự duyệt được tool vẫn giữ lưới 15 phút để không treo mãi.
- **Trang Nhóm gọn hơn.** Mô tả của nhóm nằm trong nút (i) cạnh tên nhóm thay vì một dòng bên dưới. Các dòng giải thích còn sót (mục Nâng cao, sổ lần trả lời, quyền của người điều phối, cách ghi nguồn cho mục tiêu, mục File và Link) cũng gập vào (i).
- **Mục File và Link không còn bị cắt chữ.** Khi chưa có gì chỉ hiện một câu ngắn, phần giải thích nằm trong (i) cạnh tiêu đề.
- **Thẻ trợ lý gọn hơn.** Dòng mô tả xám bị cắt dưới tên trợ lý đã bỏ. Mô tả đầy đủ nằm trong nút (i) ở góc trên phải thẻ, ngay trên nút Auto, bấm là đọc được hết.
- **Gọi thoại với cộng sự giữ được hướng dẫn dài hơn.** Phần hướng dẫn trong file cộng sự đưa vào cuộc gọi tăng từ 4.000 lên 12.000 ký tự, bộ nhớ từ 2.000 lên 6.000, chỉnh được qua `TISA_VOICE_AGENT_BODY_CHARS` và `TISA_VOICE_AGENT_MEMORY_CHARS`. Đặt luật quan trọng giữa `<!-- TISA_VOICE_RULES_START -->` và `<!-- TISA_VOICE_RULES_END -->` trong file cộng sự thì luật đó luôn được đưa lên đầu, không bị cắt.
- **Cộng sự không bịa số liệu khi gọi thoại.** Mọi cuộc gọi với cộng sự luôn kèm một luật không bị cắt: thông tin hay thay đổi phải lấy từ công cụ, và chỉ báo việc đã xong khi công cụ trả kết quả thành công.
- **Kết nối thêm nhà cung cấp không còn popup.** Bấm một cái là xổ ra hết các thẻ kết nối ngay bên dưới, bấm lần nữa để gập lại.
- **Trang Chatbot mở nhanh hơn hẳn khi hòm thư đã nhiều tin.** Các con số "tin hôm nay" ở Hội thoại và trên thẻ bot trước đây phải đọc lại toàn bộ tin nhắn mỗi 5 giây, nay chỉ đọc đúng khoảng thời gian cần.
- **Tab Thống kê tính nhanh hơn và nhớ kết quả.** Kỳ trước để so sánh được giữ 10 phút, chuyển tab qua lại không phải tính lại từ đầu.
- **Hội thoại tải danh sách cùng lúc với danh sách kênh**, không còn đợi xong cái này mới hỏi cái kia. Lúc trang đang tính, các trang khác của TISA BOT không bị đứng theo.
- **Model biết trạng thái thật của repo** (đã lên GitHub chưa, PR, CI, lý do kẹt), nên không còn trả lời "em không được đẩy" hay đề nghị sửa code chỉ để kích hoạt việc đẩy.
- **Hộp "Repo đã tải về brain này" mang dáng trang Nhiệm vụ.** Mỗi repo là một thẻ gọn: tên repo, số cuộc trò chuyện và trạng thái tự merge, công tắc gạt để bật tắt tự merge.
- **Lệnh kiểm tra, Số đo, Gỡ khỏi brain gom vào nút ⋯.** Bấm là mở menu như trang Nhiệm vụ, trên điện thoại trượt lên từ dưới, nút Gỡ tô đỏ cho khỏi bấm nhầm.
- **Ghi âm thành chữ lại hiện chữ ngay trong ô chat** khi đang nói trên máy tính, như bản cũ, không còn bong bóng mờ phía trên. Điện thoại vẫn hiện chữ khi ghi xong.
- **Nói xong là câu được viết lại cho đúng ngữ cảnh.** Bấm dừng, Enter hay Gửi thì một mô hình đọc vài tin nhắn gần nhất rồi viết lại cả câu, sửa mọi chỗ máy nghe nhầm, không chỉ vài từ như "Travis OS" thành "TISA BOT". Gửi ngay thì câu đã viết lại mới là câu được gửi.
- **Đi đường nhanh trước.** Mô hình chính là API key thì dùng chính nó. Mô hình chính là Claude Code hay Codex thì dùng khoá API có sẵn trên máy (Groq trước), chỉ khi không có khoá nào mới gọi CLI, nên thường chỉ chờ khoảng một giây.
- Lỗi mạng hay mô hình chậm quá 25 giây thì giữ câu nghe được, không mất chữ. Tai Groq hay OpenAI giờ luôn giữ tên TISA BOT trong từ mồi dù có nhiều kết nối.
- **Trang Link chia sẻ gọn và dễ dùng hơn.** Nút thành icon như trang Nhiệm vụ, có lọc (File, Hội thoại, Chưa ai xem) và sắp xếp (Mới tạo, Xem nhiều, Xem gần đây), thu hồi thì hỏi lại trước.
- **Repo GitHub ở trang Nhóm có logo GitHub như ở phần Trò chuyện**, trên chip repo, trong menu "+" và trong bảng thông tin nhóm.
- **Kiểm tra trước khi phát hành nhanh hơn thêm.** Bộ test lưu công thức được tách thành ba file, nên các máy kiểm tra cân bằng hơn.
- **Kiểm tra trước khi phát hành chạy nhanh hơn.** Test Python chia cho 4 máy thay vì 2, nên một lượt kiểm tra xong sớm hơn. Người dùng không thấy thay đổi nào khác.
- **Nút mic chép lời trên máy tính có lại bong bóng chữ mờ.** Lúc bạn nói, câu đang nhận ra hiện trong một bong bóng nháp mờ ở cuối khung chat, để biết TISA BOT đang nghe. Ô chat vẫn đứng yên, đến khi bấm dừng hoặc gửi thì cả đoạn chữ mới vào ô.
- Điện thoại không có bong bóng này: trên Android, trình nhận giọng hay gửi lại cả câu mỗi lần nghe thêm chữ nên bong bóng bị lặp. Điện thoại vẫn chỉ nhận chữ khi bấm dừng.
- **Thanh trên cùng gọn hơn: bỏ nút Lịch sử và nút làm mới hội thoại.** Danh sách hội thoại vẫn ở trang Trò chuyện (mục đầu menu). Nút "+" hội thoại mới trên điện thoại vẫn chạy như cũ.
- **Mỗi ngày chỉ 1 ngôi sao ưu tiên.** Chọn đúng một việc quan trọng nhất trong ngày. Bấm sao ở việc khác cùng ngày thì sao tự chuyển sang việc đó (có nút Hoàn tác), không còn bị chặn bằng câu "đã đủ".
- Lựa chọn model của bạn không bị đổi khi dự phòng: TISA BOT tự quay về model đã chọn khi nó hồi lượt, chọn tay một model thì TISA BOT thử model đó ngay. Chip cập nhật tại chỗ, không cần tải lại trang hay khởi động lại.
- **Nút mic chép lời giờ chạy như máy ghi âm**, ở chat chính, trang Nhóm và trang Hội thoại. Lúc nói, ô chat đứng yên. Bấm dừng hoặc gửi thì cả đoạn chữ hiện ra một lần.
- **Bấm vào một hội thoại cũ hiện ra nhanh hơn, máy đỡ khựng.** Các tin dựng lại từ lịch sử không còn chạy hiệu ứng trồi lên cùng một lúc, việc này từng chiếm phần lớn thời gian vẽ trên điện thoại. Tin mới tới vẫn có hiệu ứng như cũ.
- **Mở hội thoại tải ít dữ liệu hơn.** Khung chat không còn tải phần chi tiết công cụ mà nó không hiển thị, có cuộc nhẹ đi tới 70%.
- **Trang Team gửi yêu cầu tải tin ngay khi bấm,** không chờ vẽ xong cả trang rồi mới hỏi máy chủ.
- **Bấm "Hội thoại mới" ở trang Cộng sự là khung chat trống ngay.** Trước đây phải chờ hai chuyến mạng nối nhau và cột phải dựng lại từ đầu; nay còn một chuyến, số lượt gọi máy chủ giảm từ 18 xuống 7.
- **Chuyển giữa các hội thoại trong Lịch sử nhẹ hơn hẳn.** Danh sách chỉ đổi dòng đang chọn, không tải lại cả danh sách, tin chưa đọc, việc nền và hòm thư mỗi lần bấm (từ khoảng 14 lượt gọi xuống 5).
- **Mọi mục trong menu linh vật giờ đều có nút ✕**, kể cả sáu mục mặc định. Bỏ hẳn nút con mắt.
- **Xóa hết sạch cũng được.** Menu trống thì bấm linh vật nó vẫn trượt ra nhưng không mở khung nào. Muốn lấy lại mục nào thì bấm "Thêm chức năng".
- **Mục tự thêm vào menu linh vật giờ có nút ✕ để xóa hẳn.** Sáu mục mặc định vẫn giữ nút con mắt để ẩn hiện, không xóa được, nên lúc nào cũng đưa menu về như cũ được.
- **"Trợ lý" trong menu linh vật đổi thành "Cộng sự"**, đúng tên trang nó mở.
- **Trò chuyện đứng riêng ở dòng đầu thanh bên**, luôn hiện sẵn, không phải mở nhóm Bộ não mới thấy.
- **Đồ thị đổi tên thành Mạng nơ-ron**, kèm biểu tượng mạng nơ-ron mới vẽ riêng cho TISA BOT (ba lớp nút nối nhau). Nói "mở mạng nơ-ron" với TISA BOT cũng mở đúng trang này.
- **Tự học có biểu tượng riêng** (bộ não có bánh răng), không còn trùng hình với nhóm Bộ não.
- **Ẩn bớt mục trên menu linh vật.** Mỗi hàng trong Cài đặt > Linh vật > Menu linh vật có nút con mắt: bấm để ẩn, bấm lại để hiện. Mục bị ẩn vẫn nằm đúng chỗ trong danh sách, chỉ không hiện trên menu. Luôn giữ ít nhất một mục hiện.
- **Kéo lên kéo xuống để sắp xếp, bỏ hai nút mũi tên.** Máy tính nắm tay cầm để kéo. Điện thoại nhấn giữ vào hàng khoảng nửa giây rồi kéo, còn vuốt nhanh vẫn là cuộn trang.
- Trần vòng việc của bạn lên 500 (trước là 150 ở khung chat, 30 ở việc nền), đặt `TISA_MAX_TOOL_ROUNDS_CODING=0` là không giới hạn. Bot nói chuyện với khách vẫn giữ 30.
- Phanh chống kẹt thông minh hơn: chờ một việc đang chạy (hỏi tiến độ dựng video) không còn bị cắt ở lần thứ 5 khi kết quả vẫn đổi, còn model xoay vòng A-B-A-B mà không tiến triển thì bị dừng sớm.
- Lượt dài không còn tràn ngữ cảnh của model: kết quả công cụ cũ được rút gọn khi vượt ngân sách, kết quả mới nhất giữ nguyên. Chỉnh bằng `TISA_TOOL_LOOP_BUDGET_CHARS`.
- **Không còn menu xổ xuống.** Chọn model, độ sâu suy nghĩ (giữ nguyên thanh trượt, có nút tia sét), menu từng key, form thêm và câu hỏi trước khi Ngắt đều là bảng kéo lên. Gói Claude ghi đúng tên Pro và Ultra.
- **Giao diện sáng giờ là mặc định của TISA BOT.** Máy chưa từng chọn tông sẽ mở ra nền sáng cả ngày lẫn đêm, không còn tự chuyển sang nền tối sau 18:00.
- Ai đã tự chọn Tối hoặc Tự động theo giờ thì vẫn giữ nguyên lựa chọn đó. Đổi lại lúc nào cũng được bằng nút mặt trời trên thanh trên cùng hoặc trong Cài đặt.
- **Chuyển qua lại giữa các cuộc chat hiện ngay.** Cuộc đã mở gần đây vẽ lại tức thì rồi tự cập nhật ngầm; rê chuột hay chạm vào một cuộc trong danh sách là nó bắt đầu tải trước khi bấm. Dựng một cuộc chat (kể cả lúc F5) cũng nhanh hơn nhiều lần vì không còn cuộn theo từng tin. Ở trang Cộng sự, bấm một trợ lý mở luôn cuộc gần nhất thay vì chờ hai lượt hỏi máy chủ nối đuôi.
- **Trang Nhiệm vụ và trang Nhóm quay lại là thấy ngay** nội dung lần trước, không còn màn "Đang tải" trống. Nhóm đã mở gần đây cũng hiện tin ngay khi chuyển qua lại.
- **Hết cảnh lúc nhanh lúc chậm 1-2 giây khi TISA BOT đang bận.** Đọc lịch sử chat không còn xếp hàng sau các lượt ghi, các lượt đọc nặng của trang Nhiệm vụ không còn chặn máy chủ, và mở một nhóm không phải tính lại thống kê mỗi lần.
- Code của từng trang tải song song và ưu tiên Nhiệm vụ, Nhóm; rê chuột vào mục menu là trang đó bắt đầu tải.
- **TISA Core giờ chỉnh y hệt các agent khác.** Ở trang Cộng sự, bấm TISA Core là mở đúng khung cài đặt quen thuộc: đổi ảnh, tên, vai trò, hướng dẫn, gắn tài liệu, chọn skill và model. Hướng dẫn ban đầu là system prompt gốc của TISA Core.
- **Auto của TISA Core luôn bật, không tắt được**, và nó vẫn là trợ lý hệ thống không xoá được. Thẻ đổi tên riêng của bản trước được bỏ, tên mới lưu ngay trong khung cài đặt hoặc khi bạn nói trong chat.
- **Kết quả JSON lớn từ `tisa_run_tool` lấy được từng phần.** Model chỉ định đường dẫn, trường và trang cần lấy, đỡ tốn ngữ cảnh. Tool vẫn chạy đúng một lần qua gateway; có lỗi hay dữ liệu lạ thì trả nguyên kết quả gốc.
- **Một bot trực được tới 100 Fanpage.** Messenger và Instagram nhận tin qua webhook nên mỗi Trang gần như không tốn gì thêm. Shop nhiều Fanpage giờ dùng một bot, dạy một lần. Các kênh khác (Zalo, Telegram...) vẫn tối đa 20 tài khoản mỗi bot.
- **Danh sách gọn và thẳng hàng hơn:** mỗi việc một thẻ, chỉ việc ưu tiên và quá hạn in đậm, trên điện thoại giờ và hạn nằm chung hàng tag.
### Bảo mật
- **Chatbot chỉ đọc tài liệu ghim ở mục Tài liệu của Agent nó dùng**, cộng thư mục `rieng-theo-nhom/` và Google Docs gắn từ Agent. Trước đây bot coi mọi ghi chú trong brain là tài liệu, nên có thể trích ghi chú riêng của chủ cho khách.
- **Cần làm sau khi cập nhật:** mở Agent của từng bot và ghim các file bảng giá, chính sách, hướng dẫn mà bot cần đọc. Bot chưa ghim file nào chỉ trả lời theo vai trò của Agent.
- **Tab Bảo mật mới trong trang Tài khoản.** Xem 2FA, thiết bị đang đăng nhập (IP, trình duyệt, lần hoạt động cuối) và lịch sử đăng nhập đúng, sai, mọi lần đổi tài khoản. Đăng xuất từng thiết bị hoặc mọi thiết bị khác mà không cần đổi mật khẩu.
- **Báo ngay khi tài khoản có biến.** Đổi tên, đổi mật khẩu, bật tắt 2FA, đăng nhập từ mạng lạ: chuông và Telegram của chủ báo liền. File cài đặt bị sửa từ ngoài TISA BOT thì mọi thiết bị bị đăng xuất và có cảnh báo đỏ.
- **Trợ lý AI không còn đụng được file bí mật** (cài đặt, khoá mã hoá, phiên đăng nhập), ở mọi mức quyền. Gỡ 2FA khi bị khoá chỉ cần thêm `TISA_RESET_2FA=1` rồi Redeploy.
- **Hostinger: cổng 7777 tự đóng ra ngoài khi đã có tên miền HTTPS**, chỉ còn đường vào có mã hoá.
- **Trang /health/loop giờ cần đăng nhập.** Trang này có thông tin lỗi và đường dẫn trên máy chủ. Riêng /health vẫn mở để kiểm tra máy còn sống.
- **Token API loại "chat" chỉ vào được phần trò chuyện**, không còn tạo, sửa hay xoá chatbot được nữa.
- **Khách gửi hai file trùng tên qua WhatsApp thì cả hai đều được giữ**, file sau không còn ghi đè file trước.
- **Đọc web và theo dõi trang kết nối đúng vào địa chỉ đã kiểm**, nên một tên miền đổi DNS giữa chừng không dẫn được vào mạng nội bộ.
- **Gói khai "thay thế" gói khác không còn tự bật.** Chỉ bản phát hành của kho chính thức mới giữ trạng thái bật của gói cũ. Màn hình cài ghi rõ gói nào sẽ bị gỡ và nhận dữ liệu plugin.
- **Trang chạy ở cổng localhost khác không gửi lệnh được vào TISA BOT.** Dev server hay app khác trên cùng máy không còn mở được terminal hay gọi API. Cửa đọc API cho mọi cổng localhost chỉ mở khi đặt `TISA_DEV_CORS=1`.
- **Link chia sẻ một ghi chú không còn mở ảnh trong inbox/, memory/ hay thư mục ẩn của brain.**
- **Tool của kết nối MCP tự thêm có tên forward, share, trash, transfer... được tính là thao tác ghi**, nên không chạy ở mức Chỉ đọc.
- **Chạy tay workflow Docker chỉ xuất bản image từ nhánh main.**
- **Chatbot và việc nền dưới mức Toàn quyền không còn ghi được chỗ chứa mã chạy.** Thư mục plugins/, TISA/ (loop, script), .git, .claude và cấu hình engine chỉ chủ ở mức Toàn quyền mới ghi được. Chatbot trả lời khách thì không ghi được ở mọi mức.
- **Việc hẹn giờ không vượt mức của người tạo.** Nhắc hẹn hay việc Kanban do một lượt chạy mức "auto" hoặc "suggest" tạo ra giờ chạy đúng mức đó, không còn mặc định Toàn quyền. Lượt dưới Toàn quyền cũng không sửa được việc đã lên lịch.
- **File HTML, SVG, XML mở từ brain chạy trong hộp cách ly.** Giống link chia sẻ, script trong file đó không còn dùng được phiên đăng nhập của chủ. PDF và ảnh vẫn hiện như cũ.
- **Thêm kết nối MCP cần Toàn quyền và chatbot khách không thấy tool này.**
- **Đường miễn đăng nhập cho công cụ trên máy (/reminders) từ chối request từ trang web**, kể cả trang đổi tên miền về 127.0.0.1.
- **Thư mục .grok/ (chứa mã hub) không còn vào git và bản sao lưu GitHub.** Brain đã lỡ commit thì được gỡ khỏi git ở lần sao lưu sau. Nếu bạn từng dùng Grok Build và có sao lưu, nên đổi mã hub: xoá file `.hub_token` trong thư mục dữ liệu TISA BOT rồi khởi động lại.

## [0.465.17] - 2026-11-06
### Thêm mới
- **Bộ TISA:** Sơ đồ 2D trên điện thoại: vuốt được trang, có tia sáng.

## [0.465.16] - 2026-11-06
### Thêm mới
- **Bộ TISA:** Mặc định tiếng Việt, sửa ô chọn ngôn ngữ bị trắng chữ.

## [0.465.15] - 2026-11-05
### Thêm mới
- **Bộ TISA:** Cài bằng một câu trong Claude Code, sửa lỗi nhỏ khi cài.

## [0.465.14] - 2026-11-05
### Thêm mới
- **Bộ TISA:** Cài bằng một câu trong Claude Code

## [0.465.13] - 2026-11-05
### Thêm mới
- **Bộ TISA:** Sửa sơ đồ 2D bị cắt phần dưới

## [0.465.12] - 2026-11-05
### Thêm mới
- **Bộ TISA:** Thêm cộng sự Hà Hồ Sơ dẫn người dùng xây bộ não; nhật ký che mật khẩu lỡ gửi

## [0.465.11] - 2026-11-05
### Thêm mới
- **Bộ TISA:** Sơ đồ 2D điều phối có tia sáng; nút Nhân bản cộng sự; đủ nút Duyệt; siết quyền công cụ quảng cáo; điền chữ mẫu trong bộ não

## [0.465.10] - 2026-11-05
### Thêm mới
- **Bộ TISA:** Giao diện TISA BOT cùng tông màu với Đội Quân AI; một bộ não chung; khung chat Đội Quân AI không còn hiện mã máy; xoá cộng sự không còn bị tạo lại.

## [0.465.9] - 2026-11-04
### Thêm mới
- **Bộ TISA:** Trang Kết nối có sẵn đầy đủ kết nối, TISA Store đủ gói.

## [0.465.8] - 2026-11-04
### Thêm mới
- **Bộ TISA:** Ổn định quy trình tạo bộ cài.

## [0.465.7] - 2026-11-04
### Thêm mới
- **Bộ TISA:** Thêm Nhân Viên Tư Vấn, đổi model trong khung chat trên bảng, TISA Store có lại kho gói, bỏ cập nhật trong app.

## [0.465.6] - 2026-11-04
### Thêm mới
- **Bộ TISA:** Nhân sự, phòng ban, kỹ năng và khung chat đồng bộ hai bên giữa Đội Quân AI và TISA BOT. Đổi toàn bộ tên kỹ thuật sang TISA.

## [0.465.5] - 2026-11-04
### Thêm mới
- **Bộ TISA:** Ổn định quy trình phát hành.

## [0.465.4] - 2026-11-04
### Thêm mới
- **Bộ TISA:** Sửa lỗi bảng Đội Quân AI hiện khung đăng nhập khi trình duyệt còn phiên cũ.

## [0.465.3] - 2026-11-04
### Thêm mới
- **Bộ TISA:** Bổ sung bài kiểm tra hai chiều giữa TISA BOT và Đội Quân AI sau khi cài.
### Sửa lỗi
- **Tên gói hiện đúng như nhà cung cấp đặt.** Anthropic đổi gói Max 20x thành Ultra ngày 30/10/2026 nhưng TISA BOT vẫn ghi "Max", vì trước giờ tên gói lấy từ một bảng điền tay. Nay thẻ Claude Code ở trang Models, vòng tròn hạn mức cạnh ô chat và câu báo hết lượt trên trang Việc đọc đúng tên mà máy chủ Anthropic trả về (Claude Code tự lưu tên này trong file cấu hình của nó, không đụng tới token). Nhà cung cấp đổi tên lần sau thì TISA BOT tự hiện tên mới, không cần ra bản cập nhật. Claude Code bản cũ chưa lưu tên thì TISA BOT chỉ làm gọn mã gói như trước.

## [0.465.2] - 2026-11-04
### Thêm mới
- **Bộ TISA:** Cập nhật lên lõi mới nhất, đặt tài khoản mặc định admin cho Windows và Mac, gỡ các luật riêng khỏi khung chung.
### Cải thiện
- **Bấm sang một hội thoại là thấy ngay.** Hộp thư Chatbot không còn khựng khi chuyển giữa các cuộc chat dài. Cuộc đã mở trước đó hiện lại tức thì rồi chỉ tải phần tin mới; cuộc mới mở hiện dòng Đang tải ngay lúc bấm.
- Mở một cuộc chat giờ chỉ cần một lần hỏi máy chủ thay vì hai, và danh sách bên trái chỉ vẽ lại đúng những dòng có thay đổi. Trên máy yếu, thời gian từ lúc bấm tới lúc khung chat phản hồi giảm từ khoảng nửa giây xuống dưới 0,05 giây.
- Vẫn chỉ tải 40 tin gần nhất, kéo lên mới tải thêm tin cũ như trước.
- **Số phiên bản giờ do máy tự đánh sau khi merge.** Mỗi bản sửa chỉ ghi nhật ký vào một file riêng, nên làm nhiều bản sửa cùng lúc không còn giành số của nhau và không phải đánh số lại.
- Mỗi lần merge vẫn ra một số phiên bản mới như cũ, kèm nhật ký tiếng Việt và tiếng Anh, rồi bản cập nhật được phát hành ngay sau đó.
### Sửa lỗi
- **Việc hẹn giờ tạo trong chat Cộng sự báo về đúng chat đó.** Trước đây nhắc hẹn và việc định kỳ giao từ chat với một trợ lý không biết mình đến từ đâu, nên cả kết quả lẫn lỗi đều rơi về TISA Core. Giờ TISA BOT tự gắn khung chat đang hỏi.
- **Tới giờ, việc chạy bằng đúng vai trợ lý đã nhận nó.** Việc đăng bài hẹn từ chat với trợ lý Đăng bài giờ dùng vai trò, quy trình, bộ nhớ và luật chủ dặn của trợ lý đó, không chạy như TISA BOT chung nữa. Trang Nhiệm vụ cũng xếp việc đó dưới tên trợ lý.
- **Sự cố báo về nơi đã giao việc.** Việc nền hỏng thì TISA Core vẫn xét và thử lại như cũ, nhưng tin "Sự cố cần bạn" giờ hiện ở khung chat đã giao việc. Việc không gắn khung chat nào thì vẫn về TISA Core.
- Việc đã tạo trước bản này vẫn chạy như cũ. Muốn có cách mới thì nhờ trợ lý tạo lại việc đó.

## [0.463.0] - 2026-11-04
### Thêm mới
- **Bộ TISA:** Bản TISA BOT đầu tiên cho học viên: TISA BOT, Bảng giao việc Đội Quân AI và bộ kỹ năng /ts-.
- **Việc của tôi đổi Dự án thành Tags.** Một việc gắn được nhiều tag, hiện thành nhãn màu ngay dưới tên việc với nút **+ Tags**. Bấm vào một tag ở cột bên để xem mọi việc gắn tag đó. Dự án cũ tự thành tag, không mất gì.
- **Việc con cho từng việc của anh.** Mở một việc là thấy danh sách việc con kèm thanh tiến độ: tích vòng tròn, sửa tên ngay tại chỗ, xoá bằng dấu x. Việc con xong thì gạch ngang và tự chìm xuống cuối. Ngoài danh sách, việc nào có việc con hiện số `1/3`, bấm vào là xổ ra tích luôn. Việc lặp lại thì mỗi lần mới bắt đầu với việc con chưa tích. Việc của TISA BOT vẫn giữ phẳng như cũ.
- **Sắp xếp thứ tự Tags.** Kéo thả tag ở cột bên trên máy tính, hoặc chọn **Chuyển lên trên / xuống dưới** trong menu của tag trên điện thoại.
- **Ghi chú gắn được link, note và file.** Dán link web hoặc gõ `[[tên note]]`, bên dưới hiện nút bấm mở thẳng. **Nối note** tìm note, file trong brain để chèn. **Tải file lên** (hoặc dán, kéo file vào ô ghi chú như khung chat) lưu file vào thư mục `task-files` của brain, giữ lâu dài.

