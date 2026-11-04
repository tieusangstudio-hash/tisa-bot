# Clarification Checklists (Shared Utility)

> Per-command context checklists used by `clarification-gate.md`. Each command lists the slots to fill before producing output. **Blocker** = cannot proceed without it. **Optimizer** = improves quality, ask only if rounds remain.

## How to Use

1. Pick the checklist for the active command.
2. In Round 1, ask the **blocker** slots (2-4 at a time).
3. If blockers are filled but rounds remain and quality would benefit, ask **optimizer** slots.
4. Stop per the gate's stop-conditions. Record skipped slots as assumptions.

---

## `/ts-dinh-gia-offer` — Offer Packaging

| Slot | Type | Why it matters |
|------|------|----------------|
| Product/service | Blocker | Nothing to package without it |
| Buyer: B2C or B2B | Blocker | Selects the B2C/B2B modifier |
| Channel: online / offline / hybrid | Blocker | Selects the online/offline modifier |
| Price range (VND) | Blocker | Selects low/high-ticket modifier + QA intensity |
| Existing proof (testimonials, results, numbers) | Blocker | Drives likelihood + guarantee design |
| Goal (launch / scale / reposition) | Optimizer | Shapes urgency + ladder |
| Target audience specifics | Optimizer | Sharpens dream outcome |

## `/ts-landing-page` — Landing Page (+ đọc màu/logo/giọng từ `01-ho-so/04-thuong-hieu-noi-dung.md`, copy từ `/ts-trang-ban-hang` nếu có)

| Slot | Type | Why it matters |
|------|------|----------------|
| Industry / niche | Blocker | Palette, tone, structure |
| ONE action the visitor should take | Blocker | CTA hierarchy is built around it |
| Traffic source | Blocker | Message-match (ad promise → page promise) |
| Real proof available (names, numbers, photos) | Blocker | Anti-AI: concrete proof beats placeholders |
| Brand colors / tone (if any) | Optimizer | Randomization respects existing brand |
| Offer details (price, guarantee) | Optimizer | Above-fold clarity |

## `/ts-kiem-chung-ngach` — Market Research

| Slot | Type | Why it matters |
|------|------|----------------|
| Niche / topic | Blocker | Scope of research |
| Market: Vietnam / global / both | Blocker | Sources + language of queries |
| Goal: validate / size / entry strategy | Blocker | Which phase to emphasize |
| Reference competitors (if any) | Optimizer | Faster teardown |
| Target customer guess | Optimizer | VoC mining focus |

## `/ts-trang-ban-hang` — Sales Page

| Slot | Type | Why it matters |
|------|------|----------------|
| Is the offer already finalized? | Blocker | Sales page needs a locked offer |
| Buyer + main pain | Blocker | Lead + emotional hook |
| Desired length (short / long-form) | Blocker | Structure |
| Proof assets available | Optimizer | Placement of social proof |

## `/ts-phan-tich-doi-thu` — Competitor Analysis

| Slot | Type | Why it matters |
|------|------|----------------|
| Competitor name(s) or niche | Blocker | Target of analysis |
| Your angle / what you're comparing | Blocker | Gap direction |
| Market (VN / global) | Optimizer | Source selection |

## `/ts-thiet-ke-pheu` — Funnel Architecture

| Slot | Type | Why it matters |
|------|------|----------------|
| Product + price tier | Blocker | Funnel depth (low-ticket ≠ high-ticket) |
| Traffic source(s) | Blocker | Top-of-funnel design |
| Goal (leads / sales / launch) | Blocker | Funnel type |
| Existing assets (list, content, ads) | Optimizer | Reuse vs build |

## `/ts-pheu-qua-tang` — Lead Magnet

| Slot | Type | Why it matters |
|------|------|----------------|
| Audience + their #1 problem | Blocker | Magnet relevance |
| Format preference (checklist, guide, template, quiz) | Blocker | Deliverable type |
| What paid offer it leads to | Blocker | Bridge to the offer |

## `/ts-viet-quang-cao` — Copywriting

| Slot | Type | Why it matters |
|------|------|----------------|
| Asset to write (headline, email, ad, page section) | Blocker | Format + length |
| Audience + main pain/desire | Blocker | Angle |
| Framework preference (or let AI pick) | Optimizer | Structure |
| Voice-of-customer language available | Optimizer | Anti-AI: use real customer words |

---

## Fallback for Unlisted Commands

If a command has no checklist here, ask the universal minimum before producing output:
1. **What exactly** is the deliverable?
2. **Who** is it for (audience)?
3. **What** is the single goal / desired action?
4. **What** context/assets already exist?
