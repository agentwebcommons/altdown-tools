# /plan — turn accepted decisions into bounded work

Given an ADR path:

1. Read `AGENTS.md`, `docs/ARCHITECTURE.md`, the named ADR, and the external spec.
2. If the ADR is not `Accepted`, if its open questions remain, or if the source spec
   cannot be accessed or is inconsistent, **STOP** and report the blocker.
3. If an active feature `PLAN.md` exists, do **not** overwrite it. Compare it and
   report discrepancies for human approval.
4. Otherwise derive PLAN, TASKS, ACCEPTANCE, PROMPTS from docs/templates/.
5. Every task needs a path and runnable verify command. Each prompt spans one phase.
6. No code changes in the planning stage. Ask for a review, then stop.
