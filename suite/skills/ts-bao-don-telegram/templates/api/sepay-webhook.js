// api/sepay-webhook.js — Nhận webhook "có tiền vào" từ SePay rồi báo về Telegram.
// Chạy trên Vercel (Node 18+), KHÔNG cần cài thêm thư viện.
//
// Cách dùng (AI làm giúp học viên):
// 1. Đặt file này vào thư mục trang, đúng đường dẫn: api/sepay-webhook.js (cạnh index.html).
// 2. Trên Vercel: Project → Settings → Environment Variables, thêm 3 biến (KHÔNG ghi vào file này):
//      SEPAY_WEBHOOK_APIKEY  = chuỗi bí mật tự đặt, dán giống hệt vào ô API Key khi tạo webhook trên SePay
//      TELEGRAM_BOT_TOKEN    = token BotFather cấp
//      TELEGRAM_CHAT_ID      = ID người nhận hoặc ID nhóm (nhóm thường là số âm, bắt đầu -100)
//    rồi đưa trang lên lại (redeploy) để biến có hiệu lực.
// 3. Trên my.sepay.vn → Webhooks → + Thêm webhook: sự kiện "Có tiền vào",
//    URL = https://<ten-trang>.vercel.app/api/sepay-webhook, chứng thực = API Key (dán SEPAY_WEBHOOK_APIKEY).
//    SePay sẽ gửi header:  Authorization: Apikey <SEPAY_WEBHOOK_APIKEY>
// 4. Thử: chuyển khoản 2.000đ vào tài khoản đã liên kết → Telegram báo trong vài giây.
//
// SePay coi là thành công khi nhận HTTP 200/201 + JSON {"success": true} trong 30 giây; nếu không sẽ gửi lại
// (tối đa 7 lần). Vì vậy file luôn trả {"success": true} nhanh sau khi đã kiểm tra hợp lệ.
// Tài liệu (đọc lại khi làm thật, có thể thay đổi): https://docs.sepay.vn/tich-hop-webhooks.html

const MIN_AMOUNT = 0; // chỉ báo khi số tiền >= mức này (vd 10000) — tùy chỉnh nếu muốn lọc giao dịch nhỏ

function escapeHtml(text) {
  return String(text ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function formatVnd(amount) {
  const n = Number(amount) || 0;
  return n.toLocaleString('vi-VN') + 'đ';
}

async function sendTelegram(text) {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chatId) throw new Error('Thiếu TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID');
  const r = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: chatId, text, parse_mode: 'HTML', disable_web_page_preview: true }),
  });
  if (!r.ok) throw new Error(`Telegram lỗi ${r.status}: ${await r.text()}`);
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ success: false, message: 'Chỉ nhận POST' });
    return;
  }

  // 1) Kiểm tra khóa bí mật — chặn người lạ gửi báo đơn giả
  const expected = process.env.SEPAY_WEBHOOK_APIKEY;
  const auth = req.headers['authorization'] || '';
  if (!expected || auth !== `Apikey ${expected}`) {
    res.status(401).json({ success: false, message: 'Sai khóa' });
    return;
  }

  const t = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});

  // 2) Chỉ báo tiền VÀO
  if (t.transferType !== 'in' || Number(t.transferAmount) < MIN_AMOUNT) {
    res.status(200).json({ success: true, skipped: true });
    return;
  }

  // 3) Soạn tin nhắn (mẫu khác: references/notification-message-templates.md)
  const lines = [
    '💰 <b>CÓ TIỀN VÀO</b>',
    `Số tiền: <b>${formatVnd(t.transferAmount)}</b>`,
    `Nội dung CK: <code>${escapeHtml(t.content)}</code>`,
    t.code ? `Mã đơn nhận diện: <code>${escapeHtml(t.code)}</code>` : null,
    `Ngân hàng: ${escapeHtml(t.gateway)} · TK ${escapeHtml(t.accountNumber)}`,
    `Thời gian: ${escapeHtml(t.transactionDate)}`,
    `Mã giao dịch SePay: ${escapeHtml(t.id)} · Tham chiếu: ${escapeHtml(t.referenceCode)}`,
  ].filter(Boolean);

  try {
    await sendTelegram(lines.join('\n'));
  } catch (err) {
    // Ghi lỗi để xem trong Vercel → Project → Logs; vẫn trả lỗi 500 để SePay gửi lại sau
    console.error('Gửi Telegram thất bại:', err.message);
    res.status(500).json({ success: false, message: 'Gửi Telegram thất bại' });
    return;
  }

  res.status(200).json({ success: true });
};
