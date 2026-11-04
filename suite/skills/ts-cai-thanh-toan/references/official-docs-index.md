# Official Docs Index — SePay

> Authoritative documentation links for the payment toolstack. **Fetch these before giving setup/API instructions** so guidance matches the current version — do not rely on memory for API details.

## When to Fetch (token-aware)
- **Fetch** when: user is actually setting up, needs a specific endpoint/field, webhook payload shape, or something isn't working.
- **Don't fetch** when: user only asks a general "what is / should I" question.
- **Rule:** live docs override prior knowledge on any conflict — payment APIs change.

## SePay (VietQR payment gateway)
| Topic | URL |
|-------|-----|
| Docs home | https://docs.sepay.vn |
| API reference | https://docs.sepay.vn/api |
| Webhook (payment notification) | https://docs.sepay.vn/tich-hop-webhooks.html |
| VietQR / QR generation | https://docs.sepay.vn/lay-ma-qr-dong.html |
| Dashboard | https://my.sepay.vn |

## What to Extract When Fetched
- Exact webhook payload fields (to match transaction → order).
- Auth header format + how to verify webhook authenticity.
- Rate limits and retry behavior.
- QR generation URL/params (for dynamic amounts).

## Cross-References
- No-tech step-by-step: `no-tech-walkthrough.md`
- Checkout UX: `checkout-flow-design-patterns.md`
- Full integration: `payment-gateway-integration-guide.md`
