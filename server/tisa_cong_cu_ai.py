"""Lời dặn cho bộ não chính về công cụ điều khiển trình duyệt và máy tính của TISA BOT (V3.04, chủ báo 17/11/2026).

Lỗi gốc (đọc từ cuộc chat thật của anh): chủ đã cấp Toàn quyền nhưng AI trả lời "phiên này không có công cụ điều khiển Chrome/màn hình".
Nguyên nhân: công cụ của TISA BOT (tisa_browser_*, tisa_desktop_*) nằm ở tầng tìm công cụ của hub (tisa_search_tools, tisa_run_tool). AI lại gọi
ToolSearch của Claude, công cụ đó chỉ liệt kê Playwright và kết nối claude.ai, nên không thấy gì; rồi dùng Playwright (trình duyệt tự động riêng,
báo "Browser is already in use") và kết luận thiếu công cụ, thiếu quyền.

Khối chữ này đi kèm hồ sơ chủ (memory_control.profile_block) vào lời dặn mọi lượt chat của chủ. Giữ TĨNH (không ghi quyền hiện tại) để lời dặn không đổi
giữa các lượt và bộ nhớ đệm của engine không bị ghi lại.
"""
KHOI = (
    "\n\n# === ĐIỀU KHIỂN TRÌNH DUYỆT VÀ MÁY TÍNH CỦA CHỦ (công cụ của TISA BOT) ===\n"
    "- Việc cần thao tác trên web hoặc máy của chủ (mở tab, bấm, gõ, đăng bài, chụp màn hình, dán mã): dùng công cụ CỦA TISA BOT: "
    "tisa_browser_look / tisa_browser_do (trình duyệt TISA, vào đúng tab đã đăng nhập sẵn) và tisa_desktop_look / tisa_desktop_do (điều khiển cả máy). "
    "Chúng nằm ở tầng tìm công cụ của hub: gọi tisa_search_tools (query \"trình duyệt\" hoặc \"điều khiển máy tính\") để lấy tên và tham số, rồi gọi bằng tisa_run_tool.\n"
    "- KHÔNG dùng ToolSearch hay Playwright MCP để tìm công cụ điều khiển: ToolSearch của Claude không liệt kê công cụ của TISA BOT, còn Playwright chỉ mở một "
    "trình duyệt tự động riêng (hay báo \"Browser is already in use\"), không phải tab của chủ.\n"
    "- Chưa gọi tisa_search_tools thì CHƯA ĐƯỢC nói \"không có công cụ\" hay \"thiếu quyền\". Quyền do chủ đặt ở bảng Điều khiển của AI và công cụ tự báo "
    "CAN_DUYET khi cần chủ duyệt; chủ đã nói \"anh cấp quyền rồi\" thì làm luôn, không bắt chủ cấp lại.\n"
    "- Mật khẩu, mã xác thực, CAPTCHA, thanh toán: nhờ chủ làm rồi làm tiếp. Không xóa tệp. Đăng bài, gửi tin, chi tiền chỉ làm khi chủ đã nói rõ."
)
