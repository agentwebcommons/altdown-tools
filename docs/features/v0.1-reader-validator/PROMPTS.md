# Cursor prompts — paste exactly one phase per session

The initial ADR is **Proposed**. These prompts implement an approved plan, **not**
permission to bypass its human review gate. Cursor should read `AGENTS.md` first.

## Prompt 0 — review and human approval

> Read `AGENTS.md`, `docs/ARCHITECTURE.md`, and the Proposed ADR for the
> v0.1 reader and validator. Summarize the decision, the tool policy, alternatives,
> consequences, and any conflict with the current Altdown 1.0 draft.
> Do not write implementation code or change the ADR status. Stop and ask me to
> explicitly accept or reject the ADR. Once I change status to Accepted,
> implement **only T002–T003**. Run each verify command.
> Update only completed checkboxes. Stop.

## Prompt 1 — parsing and URL rules

> Read `AGENTS.md`, current architecture, the Accepted ADR, `PLAN.md`,
> `ACCEPTANCE.md`, and `TASKS.md`. Implement only **T004–T007**. Build
> typed result structures, URL/canonical checks, HTML `<head>` discovery,
> and front matter parsing from the Altdown 1.0 draft. Use offline fixtures.
> Do not add network retrieval, reader orchestration, validation CLI, crawl,
> diff, or new standards. Run each task's verify command and Ruff.
> Update only completed checkboxes and `docs/ARCHITECTURE.md` for new
> implemented boundaries. Summarize changes and uncertainties. Stop.

## Prompt 2 — reference consumer

> Read `AGENTS.md`, architecture, the Accepted ADR, `PLAN.md`,
> `ACCEPTANCE.md`, and unfinished Phase 2 tasks. Implement only **T008–T012**.
> The reader must verify discovered copies, respect robots for copies, enforce
> bounded HTTP/URL policies, return HTML explicitly on Altdown rejection, and
> never probe a guessed Markdown path. Include negotiated Markdown cases.
> Network tests must be fully mocked. Do not add `check`, crawl, diff,
> persistence, caching, or MCP. Run all verify commands and Ruff, update
> architecture and completed checkboxes. Stop.

## Prompt 3 — publisher validation

> Read `AGENTS.md`, architecture, the Accepted ADR, `PLAN.md`,
> `ACCEPTANCE.md`, and unfinished Phase 3 tasks. Implement **T013–T015** only.
> The validator must give precise mandatory failures vs `should` warnings,
> five-word fidelity overlap with explicit limitations, and documented CLI
> exit codes. Keep reader and validator implementations separate over shared
> primitives. Add mocked tests. Run verify commands and Ruff; update
> architecture and completed checkboxes. Stop.

## Prompt 4 — hardening and release review

> Read all project artifacts and evaluate **T016–T020** against actual code.
> Fill missing adversarial/acceptance tests, run the full offline suite and
> packaging smoke, update README/examples and `docs/ARCHITECTURE.md`.
> Do not add deferred features, change the Altdown spec, or mark a release
> without my explicit approval. Report any unsupported conformance rules and
> residual risks; update only verified checkboxes. Stop.

## Session handoff

At the end of every prompt, report these four facts, not a general progress narrative:

1. Tasks completed (IDs) and corresponding verification output.
2. Files changed.
3. Open spec/design questions, if any.
4. Next **single** unfinished phase (do not implement it yet).
