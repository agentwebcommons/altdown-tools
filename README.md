# Altdown Tools

**Reference reader, validator, and conformance tools for [Altdown](https://altdown.org/spec/).**

A public, Apache-2.0-licensed project from [Agent Web Commons](https://github.com/agentwebcommons).

> **Status: planning scaffold, not an implemented CLI.** This repository is designed to
> hand to Cursor. The feature documents define the v0.1 implementation and its tests;
> do not advertise `altdown fetch` or `altdown check` as working until they are built.

## Goal

Two consumers of the same small library:

- **Agent developers:** retrieve a publisher-authored Altdown Markdown copy when verified,
  otherwise return the original HTML for the caller to handle.
- **Publishers:** validate published pages and report actionable failures against the
  Altdown 1.0 **draft**, including a heuristic fidelity comparison.

The specification lives in [agentwebcommons/altdown](https://github.com/agentwebcommons/altdown)
under **CC BY-SA 4.0**; this repository implements it under **Apache-2.0**.
This repository does not relicense the specification or claim the draft is final.

## v0.1 proposed interface (not yet implemented)

```bash
altdown fetch https://example.org/article/            # Markdown or raw HTML fallback
altdown fetch https://example.org/article/ --json
altdown check https://example.org/article/            # publisher report
altdown check https://example.org/article/ --json
```

Python API (target contract, not yet implemented):

```python
from altdown_tools import fetch, check

result = fetch('https://example.org/article/')
report = check('https://example.org/article/')
```

The stable proposed outputs and exit codes live in
[ACCEPTANCE.md](docs/features/v0.1-reader-validator/ACCEPTANCE.md).

## Give this repository to Cursor

1. Open the folder in Cursor and ask it to **read `AGENTS.md` first**.
2. Review [the proposed ADR](docs/adr/2026-10-31-separate-fetch-and-validation.md).
   Set `Status: Accepted` **yourself** only after approving its decision.
3. Then run prompts **one phase at a time**, in
   [PROMPTS.md](docs/features/v0.1-reader-validator/PROMPTS.md).
4. At each phase boundary, inspect the diff and run the listed verification commands.
   Do not ask Cursor to implement every phase in one prompt.

For the scaffold before dependencies are installed:

```bash
python scripts/verify_scaffold.py
```

After implementation begins:

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Roadmap and boundaries

| Version | In scope | Explicitly out of scope |
| --- | --- | --- |
| v0.1 | `fetch`, `check`, importable Python API, deterministic fixtures | `diff`, `crawl`, site-index sync, publishing/building copies, MCP integration |
| Later, after v0.1 | `diff` fidelity diagnostics, `crawl`/JSON Feed index, agent integration | Not authorized by the current feature plan |

## References

- [Altdown 1.0 draft (normative)](https://altdown.org/1.0/)
- [Latest draft](https://altdown.org/spec/)
- [Plan before you prompt](https://www.vivekchopra.com/posts/plan-before-you-prompt)

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
