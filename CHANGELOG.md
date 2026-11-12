# Nhật ký cập nhật

***Tiếng Việt** · [English](CHANGELOG.en.md)*

Lịch sử phiên bản TISA BOT. Bản mới nhất ở trên cùng. Xem ngay trong app tại **Cài đặt → Cập nhật**.

Định dạng: mỗi phiên bản là một khối `## [x.y.z] - ngày`, bên dưới nhóm thay đổi theo `### Thêm mới / Sửa lỗi / Cải thiện / Bảo mật`.

## [0.551.3] - 2026-11-13
### Thêm mới
- **Bộ TISA:** Sửa lỗi đồng bộ cộng sự với Đội Quân AI: hồ sơ trợ lý hệ thống không còn bị đưa lên bảng, và một cộng sự mà lõi chưa nhận không còn chặn việc thêm các cộng sự khác vào nhóm. Bộ cài Mac và Windows dựng lại đạt kiểm tra.

## [0.551.2] - 2026-11-13
### Thêm mới
- **Bộ TISA:** Quảng Cáo: nút "Lấy số thật qua MCP" cho người đã nối MCP quảng cáo (ví dụ Meta Ads) mà chưa nhập mã API. Bấm nút, cộng sự phụ trách quảng cáo đọc số qua MCP (chỉ đọc, không bịa số) rồi trang hiện lên Tổng quan, Chiến dịch và bảng chi tiết, ghi rõ lấy lúc nào và kỳ nào. Không đọc được (ví dụ chưa đăng nhập) thì trang báo lại lý do, không hiện số giả. Có mã API thì API được dùng trước.

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

