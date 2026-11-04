// api/kiem-tra-thanh-toan.js — Trang tự biết khách đã chuyển khoản chưa (không cần cơ sở dữ liệu).
// Chạy trên Vercel (Node 18+), không cần cài thêm thư viện.
//
// Cách hoạt động: trang thanh toán tạo MÃ ĐƠN ngẫu nhiên (vd DH8F3A2C), in vào nội dung chuyển khoản của mã QR,
// rồi cứ 5 giây gọi:  GET /api/kiem-tra-thanh-toan?ma=DH8F3A2C&so_tien=690000
// Hàm này hỏi SePay danh sách giao dịch gần đây; thấy giao dịch có nội dung chứa mã đơn và số tiền đủ → paid: true.
//
// Biến môi trường (Vercel → Project → Settings → Environment Variables — KHÔNG ghi vào file):
//   SEPAY_API_TOKEN       = token tạo ở my.sepay.vn → Cấu hình Công ty → API Access → + Thêm API
//   SEPAY_ACCOUNT_NUMBER  = (nên có) số tài khoản nhận tiền, để chỉ xét đúng tài khoản này
//
// Tài liệu (đọc lại khi làm thật — có thể thay đổi): https://docs.sepay.vn/api-giao-dich.html
//   GET https://my.sepay.vn/userapi/transactions/list  · header  Authorization: Bearer <token>
//   tham số: account_number, transaction_date_min (yyyy-mm-dd), limit … · trả về: transactions[] gồm
//   id, transaction_date, amount_in, transaction_content, reference_number, code …
// Lưu ý giới hạn gọi API của SePay: trang chỉ nên hỏi 5 giây/lần và dừng sau 15 phút.

function chuanHoa(s) {
  return String(s || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  const ma = chuanHoa(req.query.ma);
  const soTien = parseInt(req.query.so_tien || '0', 10) || 0;

  // Mã đơn quá ngắn dễ trùng/đoán → từ chối
  if (ma.length < 6) {
    res.status(400).json({ paid: false, message: 'Mã đơn không hợp lệ' });
    return;
  }
  const token = process.env.SEPAY_API_TOKEN;
  if (!token) {
    res.status(500).json({ paid: false, message: 'Chưa cài SEPAY_API_TOKEN' });
    return;
  }

  const homQua = new Date(Date.now() - 24 * 3600 * 1000).toISOString().slice(0, 10);
  const params = new URLSearchParams({ transaction_date_min: homQua, limit: '100' });
  if (process.env.SEPAY_ACCOUNT_NUMBER) params.set('account_number', process.env.SEPAY_ACCOUNT_NUMBER);

  let data;
  try {
    const r = await fetch(`https://my.sepay.vn/userapi/transactions/list?${params}`, {
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    });
    if (!r.ok) {
      console.error('SePay trả lỗi', r.status, await r.text());
      res.status(502).json({ paid: false, message: 'Chưa kiểm tra được, thử lại sau' });
      return;
    }
    data = await r.json();
  } catch (err) {
    console.error('Không gọi được SePay:', err.message);
    res.status(502).json({ paid: false, message: 'Chưa kiểm tra được, thử lại sau' });
    return;
  }

  const ds = Array.isArray(data.transactions) ? data.transactions : [];
  const khop = ds.find(
    (t) => Number(t.amount_in) >= soTien && Number(t.amount_in) > 0 &&
      (chuanHoa(t.transaction_content).includes(ma) || chuanHoa(t.code) === ma)
  );

  // Không trả chi tiết giao dịch ra ngoài (bảo vệ thông tin người chuyển)
  res.status(200).json({ paid: Boolean(khop) });
};
