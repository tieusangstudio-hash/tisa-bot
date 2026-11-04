# Anti-AI-Slop Checklist

> A mandatory gate. Before exporting any landing page HTML, run this checklist and fix every hit. "AI smell" is what makes a page feel machine-made and untrustworthy — this file kills it.

## How to Use

After drafting the page, scan against the three categories below. Each item: **❌ the tell → ✅ the fix**. Do not export until the top-10 red flags are clear.

## Top 10 Red Flags (must-fix before export)

1. Blue/purple gradient hero (the default AI palette)
2. Exactly 3 symmetric feature cards with generic icons
3. Empty-phrase copy ("Empower", "Unlock", "Seamless", "Elevate")
4. Every section identical padding + same grid
5. Placeholder testimonials with no names/photos
6. Generic CTA ("Learn more", "Get started") with no context
7. Emoji used as UI icons
8. Vague headline that could belong to any business
9. Stock-photo-shaped placeholders described generically
10. Perfect symmetry everywhere, zero visual hierarchy

## A. Copy Slop

| ❌ Tell | ✅ Fix |
|---------|--------|
| "Empower your business", "Unlock your potential", "Take it to the next level", "In today's fast-paced world", "Seamless/Revolutionize/Elevate/Cutting-edge" | Delete the phrase. Say the specific thing: what changes, by how much, for whom. |
| Vague headline: "The best solution for your needs" | Concrete: name the outcome + audience + number. "Get 30 qualified leads/month for your Da Nang spa" |
| Feature-dump ("Powerful. Flexible. Scalable.") | Benefit tied to outcome, in the customer's words (pull from VoC if available). |
| Generic CTA: "Learn more", "Submit", "Get started" | Contextual CTA: "Book my free spa trial", "Send me the price list", "Claim the launch price" |
| Every sentence same length/rhythm | Vary sentence length. Short punch. Then a longer explanatory line. |

## B. Visual Slop

| ❌ Tell | ✅ Fix |
|---------|--------|
| Blue→purple gradient hero | Use the industry palette (design-data.md); limit gradients; consider solid + one accent |
| 3 perfectly symmetric icon cards | Vary count (2, 4, 5), break symmetry, use real detail not generic icons |
| Same padding + same 3-col grid every section | Alternate layouts (see Layout Variation Matrix); vary density and height |
| Generic placeholder images | Describe specific, real-feeling imagery; use the user's real photos where possible |
| Emoji as UI icons | SVG icons (Heroicons/Lucide) |
| Centered everything | Mix alignment — left-aligned editorial blocks read more human |

## C. Structure Slop

| ❌ Tell | ✅ Fix |
|---------|--------|
| Rigid symmetric sections top to bottom | Editorial/asymmetric rhythm; one focal element per section |
| Everything weighted equally | Clear visual hierarchy — one hero message, one primary CTA |
| Proof dumped only at the bottom | Place proof next to the claim it supports |
| Uniform, machine-even spacing | Intentional spacing rhythm; whitespace as emphasis |
| No local specificity | Add real VN detail: names, districts, VND prices, hotline, business registration |

## Export Gate

Before producing the final HTML, confirm in one line:
> Anti-AI check: no default gradient, no empty-phrase copy, varied layout, concrete CTA, proof placed with claims, real local detail. ✅

If any red flag remains, fix it first. Ties into `humanize-design-patterns.md` (add human detail) and `conversion-structure-principles.md` (structure for conversion, not decoration).
