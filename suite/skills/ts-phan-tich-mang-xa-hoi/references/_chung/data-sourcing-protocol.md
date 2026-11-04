# Data-Sourcing Protocol (Shared Utility)

> Shared framework that teaches the AI **how to fetch real data at runtime** — for any industry — instead of shipping hardcoded numbers that go stale. "Teach fishing, don't hand out fish."

## Core Principle

This kit contains **frameworks and empty templates**, not baked-in market data. Pricing, benchmarks, and industry models change fast and differ per niche. When output needs a concrete number, the AI **researches it live for the specific industry the user is in**, then fills the template — with source + date attached.

## When to Source Data

Trigger a data-sourcing pass whenever the output needs industry-specific concreteness:
- Price points, price ranges, or benchmarks
- Market size / demand figures
- Competitor offers, guarantees, or funnel patterns
- Conversion / channel behavior stats
- Any claim a skeptical reader would ask "says who?" about

If the output is purely structural (a framework, a layout, a checklist), no sourcing needed.

## How to Source (built-in tools only)

Use the web search / web page reading tools available in your environment — no external scrapers needed. For query ideas by industry, the user can also run `/ts-kiem-chung-ngach`.

### Source trust ladder (prefer higher)
1. **Official / primary** — government stats, platform official reports, company's own pricing page
2. **Real marketplace** — Shopee/Tiki/Lazada listings, actual sold counts, live pricing
3. **Community signals** — forums, FB groups, YouTube/marketplace reviews (real users)
4. **Secondary/SEO content** — blogs, listicles (lowest trust; corroborate before using)

### The 3-source rule
For any **important** number (a price you'll anchor on, a market size you'll decide by), confirm with **≥3 independent sources** before treating it as reliable. One source = a lead, not a fact.

## Recording Standard (mandatory)

Every sourced data point is written as:

```
<value> | <source> | <access date> | <trust: high/med/low>
```

Example:
> Mini-course price band 199K–499K VND | Shopee "khóa học online" listings | accessed 2026-07-03 | med

Rules:
- Data older than **12 months** → flag it as potentially stale.
- Always show the source inline or in an evidence note — never a bare number.
- Currency in VND for the Vietnamese market; note FX date if converting.

## When to Use Illustrative Data (fallback only)

If live research genuinely returns nothing usable, you may use an illustrative figure — but:
- Label it clearly: `[Illustrative — assumption, replace with real data]`
- **Never** present it as a fact or cite it as sourced.
- Prefer a **range** over a false-precise single number.
- Note what search was attempted so the user can finish it.

## Integration with the Clarification Gate

The gate captures the **industry / niche** (and market: VN vs global) up front. This protocol then:
1. Takes that industry from the gate's answers.
2. Runs targeted queries for **that** industry (not generic).
3. Fills the empty template (case study, research example, landing copy) with sourced, dated data.

So the flow is: **gate asks industry → protocol fetches that industry's real data → template gets filled**. This is why the kit stays multi-industry and never goes stale.

## Quick Reference (the loop)

```
Need a concrete number?
  → Yes: research (3-source rule) → record (value|source|date|trust) → fill template
       → nothing found? → illustrative with label → note attempted search
  → No (structural only): proceed with framework
```
