# Architecture Decision Records

ADRs capture hard-to-reverse decisions (contracts, trust boundaries, subsystem ownership,
lifecycles), not every implementation detail.

- `Proposed`: review in a docs-only PR; implementation blocked.
- `Accepted`: human-reviewed; implementation may proceed.
- `Rejected`: retained for history; do not implement.
- `Superseded`: replaced by a later ADR.

Use date-slug names: `YYYY-MM-DD-brief-decision.md`.
Accepted ADRs are immutable: write a new ADR rather than editing history.

## Index

- [2026-10-31 — Separate retrieval and validation](2026-10-31-separate-fetch-and-validation.md) — **Proposed**.

## Workflow

1. Identify the decision and alternatives.
2. Write ADR `Proposed`; do not add implementation code in the same PR.
3. A human resolves open questions and changes `Status:` to `Accepted` or `Rejected`.
4. Draft/confirm the feature plan and implement one phase at a time.

Template: [ADR.md](../templates/ADR.md).
