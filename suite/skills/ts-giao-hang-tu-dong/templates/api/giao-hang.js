// api/giao-hang.js — Khách trả tiền xong là tự nhận sản phẩm số (link + email), không cần cơ sở dữ liệu.
// Chạy trên Vercel (Node 18+), không cần cài thêm thư viện.
//
// Luồng: trang thanh toán (mẫu ở /ts-cai-thanh-toan) có thêm ô Email + Tên. Khi trang đã thấy "đã thanh toán",
// nó gọi  POST /api/giao-hang  { ma, goi, email, ten }.
// Hàm này: (1) hỏi SePay xem mã đơn đã trả ĐỦ tiền của gói chưa, (2) gửi email giao hàng qua Resend,
// (3) báo Telegram cho chủ shop (nếu có cài), (4) trả link sản phẩm để trang cảm ơn hiện luôn.
//
// Biến môi trường (Vercel → Project → Settings → Environment Variables — KHÔNG ghi vào file):
//   SEPAY_API_TOKEN        token SePay (Cấu hình Công ty → API Access)
//   SEPAY_ACCOUNT_NUMBER   (nên có) số tài khoản nhận tiền
//   RESEND_API_KEY         khóa API Resend (resend.com → API Keys)
//   EMAIL_GUI              địa chỉ gửi trên tên miền ĐÃ XÁC MINH ở Resend, vd "Tiệm bánh Mây <don@tiembanhmay.vn>"
//   TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID   (tùy chọn) báo chủ shop — xem /ts-bao-don-telegram
//
// Tài liệu (đọc lại khi làm thật — có thể thay đổi):
//   SePay API giao dịch: https://docs.sepay.vn/api-giao-dich.html
//   Resend gửi email:    https://resend.com/docs/api-reference/emails/send-email  (POST https://api.resend.com/emails,
//                        header Authorization: Bearer <RESEND_API_KEY>, body { from, to, subject, html })
//
// Giới hạn cần biết: không có cơ sở dữ liệu nên nếu trang gọi lại cùng mã đơn, email có thể gửi lại lần nữa.
// Mã đơn phải NGẪU NHIÊN ≥ 8 ký tự để người khác không đoán được. Sản phẩm giá trị cao → dùng nền tảng có
// tài khoản học viên / link có hạn (xem references/digital-product-delivery-methods.md).

// ====== DANH MỤC SẢN PHẨM — AI điền từ 01-ho-so/02-san-pham-dich-vu.md ======
const SAN_PHAM = {
  // mã gói: { ten, gia (số nguyên VND), link (link tải/link truy cập ổn định), huongDan }
  KHOABANH: {
    ten: 'Khóa học Bánh mì tại nhà',
    gia: 690000,
    link: 'https://drive.google.com/…',   // [CẦN BỔ SUNG: link thật]
    huongDan: 'Mở link, đăng nhập Gmail bạn đã điền để xem video. Bắt đầu từ Bài 1.',
  },
};
const LIEN_HE_HO_TRO = 'Zalo {{SO_ZALO}}';     // lấy từ 05-muc-tieu-quy-tac-lien-he.md
// ===========================================================================

const chuanHoa = (s) => String(s || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const emailHopLe = (e) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(e || ''));

async function daThanhToan(ma, soTien) {
  const homQua = new Date(Date.now() - 24 * 3600 * 1000).toISOString().slice(0, 10);
  const p = new URLSearchParams({ transaction_date_min: homQua, limit: '100' });
  if (process.env.SEPAY_ACCOUNT_NUMBER) p.set('account_number', process.env.SEPAY_ACCOUNT_NUMBER);
  const r = await fetch(`https://my.sepay.vn/userapi/transactions/list?${p}`, {
    headers: { Authorization: `Bearer ${process.env.SEPAY_API_TOKEN}`, 'Content-Type': 'application/json' },
  });
  if (!r.ok) throw new Error(`SePay ${r.status}`);
  const d = await r.json();
  return (d.transactions || []).some(
    (t) => Number(t.amount_in) >= soTien &&
      (chuanHoa(t.transaction_content).includes(ma) || chuanHoa(t.code) === ma)
  );
}

async function guiEmail({ email, ten, sp, ma }) {
  const html = `
    <p>Chào ${esc(ten) || 'bạn'},</p>
    <p>Cảm ơn bạn đã mua <b>${esc(sp.ten)}</b>. Đơn <b>${esc(ma)}</b> đã thanh toán thành công.</p>
    <p><a href="${esc(sp.link)}" style="display:inline-block;padding:12px 20px;background:#C2410C;color:#fff;border-radius:8px;text-decoration:none">Mở sản phẩm của bạn</a></p>
    <p>${esc(sp.huongDan)}</p>
    <p>Cần hỗ trợ? Nhắn ${esc(LIEN_HE_HO_TRO)}.</p>`;
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: process.env.EMAIL_GUI,
      to: [email],
      subject: `Sản phẩm của bạn đã sẵn sàng: ${sp.ten}`,
      html,
    }),
  });
  if (!r.ok) throw new Error(`Resend ${r.status}: ${await r.text()}`);
}

async function baoTelegram(text) {
  const { TELEGRAM_BOT_TOKEN: tk, TELEGRAM_CHAT_ID: id } = process.env;
  if (!tk || !id) return;
  await fetch(`https://api.telegram.org/bot${tk}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: id, text, parse_mode: 'HTML' }),
  }).catch(() => {});
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') { res.status(405).json({ ok: false }); return; }
  const b = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  const ma = chuanHoa(b.ma);
  const sp = SAN_PHAM[chuanHoa(b.goi)];

  if (ma.length < 8 || !sp) { res.status(400).json({ ok: false, message: 'Mã đơn hoặc gói không hợp lệ' }); return; }
  if (b.email && !emailHopLe(b.email)) { res.status(400).json({ ok: false, message: 'Email không hợp lệ' }); return; }

  let paid = false;
  try { paid = await daThanhToan(ma, sp.gia); } catch (e) {
    console.error('Không kiểm tra được SePay:', e.message);
    res.status(502).json({ ok: false, message: 'Chưa kiểm tra được thanh toán, thử lại sau ít phút' });
    return;
  }
  if (!paid) { res.status(200).json({ ok: true, paid: false }); return; }

  let daGuiEmail = false;
  if (b.email && process.env.RESEND_API_KEY && process.env.EMAIL_GUI) {
    try { await guiEmail({ email: b.email, ten: b.ten, sp, ma }); daGuiEmail = true; }
    catch (e) { console.error('Gửi email lỗi:', e.message); }
  }
  await baoTelegram(
    `📦 <b>ĐÃ GIAO TỰ ĐỘNG</b>\nĐơn: <code>${esc(ma)}</code>\nGói: ${esc(sp.ten)} · ${sp.gia.toLocaleString('vi-VN')}đ\n` +
    `Email: ${daGuiEmail ? '✅ đã gửi' : '⚠️ chưa gửi — kiểm tra'} ${esc(b.email || '')}`
  );
  res.status(200).json({ ok: true, paid: true, link: sp.link, huongDan: sp.huongDan, daGuiEmail });
};
