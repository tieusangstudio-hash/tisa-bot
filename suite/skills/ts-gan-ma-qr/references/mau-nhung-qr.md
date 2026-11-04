# 4 mẫu nhúng mã QR & xử lý webhook — /ts-gan-ma-qr

> Chuyển từ SKILL.md gốc (phần code mẫu dài). Khi dùng:
> - Đổi đường dẫn ảnh QR sang `https://vietqr.app/img` (đường dẫn trong tài liệu SePay hiện tại). Mẫu cũ
>   `https://vietqr.app/img` dùng cùng tham số — nếu ảnh không hiện thì đổi sang đường dẫn còn lại.
> - Dịch chữ hiển thị sang tiếng Việt, số tiền định dạng `789.000đ`, thay `YOUR_ACCOUNT`, `YOUR_BANK`.
> - Nội dung chuyển khoản (`des`): chữ và số không dấu, không khoảng trắng, ngắn (≤ 25 ký tự là an toàn).
> - Webhook: SePay coi là thành công khi trả HTTP 200/201 + JSON `{"success": true}` trong 30 giây; bảo mật API Key
>   gửi header `Authorization: Apikey <khóa>`. Mẫu webhook đầy đủ, đã kiểm tra: dùng `/ts-bao-don-telegram`.

## HTML Embed Patterns

### Pattern 1: Simple QR Code

Clean, centered payment section with QR code and bank details.

```html
<div class="payment-section text-center p-8 bg-gray-50 rounded-lg">
  <h3 class="text-2xl font-bold mb-4 text-gray-800">Pay via Bank Transfer</h3>

  <img
    src="https://vietqr.app/img?acc=YOUR_ACCOUNT&bank=YOUR_BANK&amount=789000&des=YOUR_PRODUCT"
    alt="Payment QR Code"
    class="mx-auto w-64 h-64 rounded-lg shadow-lg"
  />

  <div class="mt-6 text-left max-w-sm mx-auto bg-white rounded-lg p-4 shadow">
    <p class="mb-2"><strong>Bank:</strong> YOUR_BANK</p>
    <p class="mb-2"><strong>Account:</strong> YOUR_ACCOUNT</p>
    <p class="mb-2"><strong>Amount:</strong> 789,000 VND</p>
    <p class="mb-2"><strong>Content:</strong> YOUR_PRODUCT</p>
  </div>

  <p class="mt-4 text-sm text-gray-600">
    Scan with any banking app • 44+ banks supported
  </p>
</div>
```

### Pattern 2: Dynamic QR with JavaScript

Generate QR codes dynamically with JavaScript for multiple products or dynamic pricing.

```html
<div id="payment-container">
  <img id="qr-code" alt="Payment QR Code" class="w-64 h-64 mx-auto" />
  <div id="payment-details"></div>
</div>

<script>
function generatePaymentQR(options) {
  const params = new URLSearchParams({
    acc: options.account,
    bank: options.bank,
  });

  if (options.amount) params.set('amount', options.amount);
  if (options.description) params.set('des', options.description);
  if (options.template) params.set('template', options.template);

  return `https://vietqr.app/img?${params}`;
}

// Usage example
const qrUrl = generatePaymentQR({
  account: 'YOUR_ACCOUNT',
  bank: 'Vietcombank',
  amount: 789000,
  description: 'Order_Product_Name'
});

document.getElementById('qr-code').src = qrUrl;

// Update payment details
document.getElementById('payment-details').innerHTML = `
  <div class="mt-4 text-center">
    <p><strong>Amount:</strong> 789,000 VND</p>
    <p><strong>Description:</strong> Order_Product_Name</p>
  </div>
`;
</script>
```

### Pattern 3: Pricing Card with QR Payment

Embed QR code directly into pricing cards for product/service packages.

```html
<div class="bg-white rounded-2xl shadow-xl p-8 border-2 border-blue-500 max-w-sm">
  <!-- Pricing Header -->
  <div class="text-center">
    <h3 class="text-xl font-bold text-gray-800">Pro Plan</h3>
    <div class="mt-4">
      <span class="text-4xl font-bold text-blue-600">789,000</span>
      <span class="text-gray-500 ml-1">VND</span>
    </div>
    <p class="text-sm text-gray-500 mt-1">per month</p>
  </div>

  <!-- Features List -->
  <ul class="mt-6 space-y-3">
    <li class="flex items-center text-gray-700">
      <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
      </svg>
      Premium Feature Access
    </li>
    <li class="flex items-center text-gray-700">
      <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
      </svg>
      Priority Support
    </li>
    <li class="flex items-center text-gray-700">
      <svg class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
      </svg>
      Advanced Analytics
    </li>
  </ul>

  <!-- Payment QR -->
  <div class="mt-8 text-center">
    <img
      src="https://vietqr.app/img?acc=YOUR_ACCOUNT&bank=YOUR_BANK&amount=789000&des=PRO_PLAN&template=compact"
      alt="Scan to pay"
      class="mx-auto w-48 h-48 rounded-lg shadow-md"
    />
    <p class="mt-3 text-sm text-gray-600">Scan QR code to pay instantly</p>
    <p class="text-xs text-gray-500 mt-1">Payment confirmed automatically</p>
  </div>
</div>
```

### Pattern 4: Payment Modal (Click to Show QR)

Show QR code in modal when user clicks "Buy Now" button.

```html
<!-- Trigger Button -->
<button
  onclick="showPaymentModal()"
  class="bg-blue-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-700 transition-colors">
  Buy Now - 789,000 VND
</button>

<!-- Modal Overlay -->
<div id="payment-modal" class="hidden fixed inset-0 bg-black/50 flex items-center justify-center z-50">
  <div class="bg-white rounded-2xl p-8 max-w-md mx-4 relative">
    <!-- Close Button -->
    <button
      onclick="hidePaymentModal()"
      class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 text-2xl font-bold">
      &times;
    </button>

    <!-- Modal Header -->
    <div class="mb-6">
      <h3 class="text-xl font-bold text-gray-800">Complete Payment</h3>
      <p class="text-sm text-gray-600 mt-1">Scan QR code with your banking app</p>
    </div>

    <!-- QR Code -->
    <div class="text-center">
      <img
        src="https://vietqr.app/img?acc=YOUR_ACCOUNT&bank=YOUR_BANK&amount=789000&des=ORDER_ID"
        alt="Payment QR"
        class="mx-auto w-56 h-56 rounded-lg shadow-lg"
      />

      <!-- Payment Details -->
      <div class="mt-4 bg-gray-50 rounded-lg p-4 text-sm text-left">
        <p class="mb-2"><strong>Bank:</strong> YOUR_BANK</p>
        <p class="mb-2"><strong>Account:</strong> YOUR_ACCOUNT</p>
        <p class="mb-2"><strong>Amount:</strong> 789,000 VND</p>
        <p class="mb-2"><strong>Content:</strong> ORDER_ID</p>
      </div>

      <!-- Instructions -->
      <div class="mt-4 bg-blue-50 rounded-lg p-3 text-sm text-blue-800">
        <p class="font-medium">After payment:</p>
        <p class="mt-1">Confirmation is sent automatically via Telegram</p>
      </div>
    </div>
  </div>
</div>

<script>
function showPaymentModal() {
  document.getElementById('payment-modal').classList.remove('hidden');
}

function hidePaymentModal() {
  document.getElementById('payment-modal').classList.add('hidden');
}

// Close modal when clicking outside
document.getElementById('payment-modal').addEventListener('click', function(e) {
  if (e.target === this) {
    hidePaymentModal();
  }
});
</script>
```

## Webhook Setup (Advanced)

For automatic payment confirmation, set up webhook endpoint to receive transaction notifications.

### Requirements
- Backend server to receive POST requests
- SePay account with webhook configured
- Endpoint URL (must be HTTPS)

### Webhook Payload Structure

```json
{
  "id": 92704,
  "gateway": "Vietcombank",
  "transactionDate": "2023-03-25 14:02:37",
  "accountNumber": "0123456789",
  "content": "payment content",
  "transferType": "in",
  "transferAmount": 789000,
  "referenceCode": "FT23084123456",
  "description": "Transfer details"
}
```

### Webhook Processing Steps

1. **Verify Signature** - Validate request authenticity using HMAC
2. **Match Payment** - Match by content, amount, or reference code
3. **Update Order Status** - Mark order as paid in database
4. **Trigger Delivery** - Send email, Telegram notification, or unlock access
5. **Return 200 OK** - Acknowledge receipt to SePay

### Example Webhook Handler (Node.js)

```javascript
app.post('/webhook/sepay', async (req, res) => {
  const transaction = req.body;

  // Verify transaction
  if (transaction.transferType === 'in' && transaction.transferAmount > 0) {
    // Match payment by content
    const orderId = transaction.content.match(/ORDER_(\d+)/)?.[1];

    if (orderId) {
      // Update order status
      await updateOrderStatus(orderId, 'paid');

      // Send notification
      await sendTelegramNotification({
        orderId,
        amount: transaction.transferAmount,
        transactionDate: transaction.transactionDate
      });
    }
  }

  // SePay requires HTTP 200 + JSON {"success": true} within 30s
  res.status(200).json({ success: true });
});
```
