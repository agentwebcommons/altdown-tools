# v0.1 tasks — ordered, checkable, one phase at a time

Status: **Not started; ADR is Proposed.** Do not check a box before its verification passes.
Each task contains a verification command that must run offline once its code exists.

## Phase 0 — human gate and packaging

- [ ] **T001** Human reviews the tool policy in the ADR and sets status to `Accepted` in
  `docs/adr/2026-10-31-separate-fetch-and-validation.md` — **verify:**
  `python scripts/verify_scaffold.py --require-accepted`
- [ ] **T002** Confirm build metadata, dependencies, and the console entry point
  `altdown` — `pyproject.toml`, `src/altdown_tools/cli.py` — **verify:**
  `uv sync && uv run python -c 'import altdown_tools'`
- [ ] **T003** CLI `--help` and a usage error, plus a test that opens no socket. No
  `fetch` or `check` behavior in this task — `tests/test_cli.py`, `tests/fixtures/` — **verify:**
  `uv run pytest tests/test_cli.py`

## Phase 1 — protocol core

- [ ] **T004** Typed, serializable results: `fallback_reason`, `warnings`, issue
  `severity` of `error` or `warning`, and `fidelity` left null until phase 3 —
  `src/altdown_tools/models.py`, `tests/test_models.py` — **verify:**
  `uv run pytest tests/test_models.py`
- [ ] **T005** Final-URL and same-origin checks, RFC 3986 normalization, fragments,
  default ports, scheme and host casing; never guess a copy path —
  `src/altdown_tools/urls.py`, `tests/test_urls.py` — **verify:**
  `uv run pytest tests/test_urls.py`
- [ ] **T006** `<head>` alternate discovery, exact `text/markdown` type with no
  parameters, `hreflang` selection by the page's `html lang`, duplicate detection,
  and `<link rel=canonical>` —
  `src/altdown_tools/discovery.py`, `tests/test_discovery.py` — **verify:**
  `uv run pytest tests/test_discovery.py`
- [ ] **T007** Minimal front matter parser. Duplicate keys keep the first value and
  are reported. Unknown unprefixed fields are retained for `check` and do not by
  themselves reject a reader parse. Handle LF/CRLF, BOM, and UTF-8 —
  `src/altdown_tools/frontmatter.py`, `tests/test_frontmatter.py` — **verify:**
  `uv run pytest tests/test_frontmatter.py`

## Phase 2 — reference consumer

- [ ] **T008** Bounded injectable HTTP transport: 10-second timeout, 1 MiB streamed
  body, at most 5 redirects, no environment proxies, cookies, credentials, or retries —
  `src/altdown_tools/http.py`, `tests/test_http.py` — **verify:**
  `uv run pytest tests/test_http.py`
- [ ] **T009** Public-URL policy and refusal of private/loopback/unsafe target and
  redirect schemes; explicitly document DNS rebinding boundary —
  `src/altdown_tools/http.py`, `tests/test_security.py` — **verify:**
  `uv run pytest tests/test_security.py`
- [ ] **T010** `robots.txt` applies to the copy only. An unreachable or missing
  `robots.txt` allows the copy. `Altdown:` is not permission. Record the User-Agent —
  `src/altdown_tools/robots.py`, `tests/test_robots.py` — **verify:**
  `uv run pytest tests/test_robots.py`
- [ ] **T011** Implement `fetch(url)` on `load_page`, including negotiation that still
  fetches HTML to confirm the link, HTML fallback, and explicit provenance. No
  guessed `.md` path and no fidelity check —
  `src/altdown_tools/load.py`, `src/altdown_tools/reader.py`, `tests/test_reader.py` — **verify:**
  `uv run pytest tests/test_reader.py`
- [ ] **T012** Implement `altdown fetch URL [--json]`; match stdout, stderr and
  exit codes, without catching fatal errors as valid HTML —
  `src/altdown_tools/cli.py`, `src/altdown_tools/__main__.py`,
  `pyproject.toml`, `tests/test_cli.py` — **verify:**
  `uv run pytest tests/test_cli.py -k fetch`

## Phase 3 — publisher validator

- [ ] **T013** Implement A09, A18, A19, and A21–A24 severities, plus stable issue
  codes. `script`, `style`, and HTML comments are errors. Do not add a rule named
  unsafe HTML —
  `src/altdown_tools/validator.py`, `tests/test_validator.py` — **verify:**
  `uv run pytest tests/test_validator.py`
- [ ] **T014** Implement draft five-word overlap on whole-page visible text, including
  nav and footer, with `indeterminate` below five normalized words and diagnostic
  snippets —
  `src/altdown_tools/fidelity.py`, `tests/test_fidelity.py` — **verify:**
  `uv run pytest tests/test_fidelity.py`
- [ ] **T015** Wire `check(url)` through the same `load_page`. `FIDELITY_LOW` and
  `ROBOTS_DISALLOW` exit 1. Operational failures stay exit 3.
  `altdown check URL [--json]` — `src/altdown_tools/cli.py`,
  `tests/test_cli.py` — **verify:**
  `uv run pytest tests/test_cli.py -k check`

## Phase 4 — release gate

- [ ] **T016** Cover A01–A24, or record a named human waiver for any missing row.
  Tests cannot use a live website — `tests/` — **verify:**
  `uv run pytest`
- [ ] **T017** README states that v0.1 reads one URL and does not crawl an index or
  run the multi-page spot check. A human reads that diff. The scaffold script does
  not prove the prose — `README.md`, `docs/` — **verify:**
  `python scripts/verify_scaffold.py --require-accepted`
- [ ] **T018** Update `docs/ARCHITECTURE.md` from actual code only, including
  `load_page`. Keep plan and ADR history separate. A human reads that diff. The
  scaffold script does not prove the prose — `docs/ARCHITECTURE.md` — **verify:**
  `python scripts/verify_scaffold.py --require-accepted`
- [ ] **T019** Keep `crawl`, `diff`, index, build tools and MCP entirely out of v0.1;
  reviewers inspect the diff — `src/`, `tests/` — **verify:**
  `uv run pytest && uv run ruff check . && uv run ruff format --check .`
- [ ] **T020** Run packaging/entry point smoke; release v0.1 only after human
  accepts actual behavior — `pyproject.toml`, `.github/workflows/ci.yml` — **verify:**
  `uv build && uv run python -m altdown_tools --help && uv run altdown --help`

## On any failure

Do not tick the task. Diagnose within its scoped files and rerun only its verify command.
If a protocol decision is missing, add the question to the plan and **stop**.
Report the last passing task and files changed before continuing to another phase.
