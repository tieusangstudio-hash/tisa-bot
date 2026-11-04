# Resend — Customer Order Confirmation Email

> Telegram notifies **you** (the owner); Resend emails the **customer** an order confirmation. Together: owner alerted + customer reassured. Transactional email via Resend.

## Why Also Email the Customer
- Builds trust — customer gets an instant, professional confirmation.
- Reduces "did my order go through?" support messages.
- Standard for any real business.

## MCP-First
If the **Resend MCP** is connected, the AI sends/tests confirmation emails directly. Otherwise it uses the API key (fetch `official-docs-index.md` for the endpoint).

## Setup Flow
1. **Resend account + API key** (resend.com).
2. **Verify sending domain** — so email comes from your brand and lands in inbox. DNS steps in `resend-deliverability.md` (shared).
3. **Wire the trigger** — payment confirmed → AI sends the confirmation email to the customer's address (captured at checkout).
4. **Compose the confirmation** (template below).
5. **Test** with a real small order.

## Confirmation Email Template (fill in)
```
Subject: Đơn hàng của bạn đã được xác nhận ✓

Chào [tên khách],

Cảm ơn bạn đã đặt [sản phẩm]!
- Mã đơn: [order id]
- Số tiền: [amount] VND
- Trạng thái: Đã thanh toán ✓

[Nếu sản phẩm số: link/hướng dẫn truy cập]
[Nếu giao sau: dự kiến khi nào]

Cần hỗ trợ? Nhắn [Zalo/hotline].
— [Tên shop]
```
> The AI localizes/translates to the brand's tone; keep it specific, not generic.

## If It Fails
| Problem | Fix |
|---------|-----|
| No email to customer | Customer email not captured at checkout — add the field |
| In spam | Domain not verified — `resend-deliverability.md` |
| Wrong details | Order data mapping — AI fixes |

## Cross-References
- Owner alert (Telegram): `no-tech-walkthrough.md`
- Deliverability + DNS: `resend-deliverability.md`
- Official docs: `official-docs-index.md`
