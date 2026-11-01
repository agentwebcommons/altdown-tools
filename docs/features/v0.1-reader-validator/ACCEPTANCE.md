# v0.1 acceptance criteria (draft)

The normative requirements are in the [Altdown 1.0 draft](https://altdown.org/1.0/).
These examples define **tool behavior** and are not changes to that specification.

## Public contract

Python API (names can be refined **before** implementation via plan review):

```python
from altdown_tools import fetch, check

f = fetch('https://example.org/page/')
assert f.format in ('markdown', 'html')
assert f.source in ('altdown', 'html-fallback')
assert isinstance(f.content, str)

c = check('https://example.org/page/')
assert isinstance(c.passed, bool)
assert isinstance(c.issues, list)
assert all(issue.severity in ('error', 'warning') for issue in c.issues)
```

`passed` is true only when every issue is a warning and fidelity is `ok`,
`indeterminate`, or `null`. `FIDELITY_LOW` sets `passed` false.

Proposed JSON structure (stable shape, fields may be added but not silently removed):

```json
{"url":"https://example.org/page/","final_url":"https://example.org/page/","format":"markdown","source":"altdown","content":"# Hello","copy_url":"https://example.org/page/index.md","fallback_reason":null,"warnings":[]}
```

```json
{"url":"https://example.org/page/","passed":false,"copy_url":null,"issues":[{"code":"MISSING_ALTERNATE","severity":"error","message":"No Altdown link found","spec_section":"Discovery"}],"fidelity":null}
```

```json
{"url":"https://example.org/page/","passed":true,"copy_url":"https://example.org/page/index.md","issues":[{"code":"CRLF","severity":"warning","message":"Copy uses CRLF line endings","spec_section":"File rules"}],"fidelity":{"status":"ok","score":1.0}}
```

```json
{"url":"https://example.org/page/","passed":false,"copy_url":"https://example.org/page/index.md","issues":[{"code":"FIDELITY_LOW","severity":"error","message":"Overlap 0.40 is below 0.90","spec_section":"The spot check"}],"fidelity":{"status":"low","score":0.40}}
```

`fidelity.status` is `ok`, `low`, or `indeterminate`. `indeterminate` uses
`score: null` and does not add an issue. `fidelity` is `null` when no copy was
checked. Every issue has `severity` of `error` or `warning`.

CLI output:

| Command | Exit 0 | Exit 1 | Exit 2 | Exit 3 |
| --- | --- | --- | --- | --- |
| `fetch` | Markdown or HTML fallback returned | — | CLI usage error | Named URL timed out, looped, exceeded 1 MiB, or was refused by URL policy |
| `check` | No errors. Warnings allowed. Fidelity `ok` or `indeterminate` | Any error, including nonconformance, `FIDELITY_LOW`, `ROBOTS_DISALLOW`, and `COPY_NOT_OK` | CLI usage error | Named URL failed as in `fetch`, or the copy timed out or exceeded 1 MiB |

- `--json` emits exactly one valid JSON object to stdout. Non-JSON diagnostics go to stderr.
- Plain `fetch` prints only content to stdout and logs the `html-fallback` reason to stderr.
- Plain `check` prints PASS/FAIL and named issues. Fidelity failures are labeled as a
  heuristic. Warnings are listed and leave the exit code at 0. No Python traceback for
  routine failures.
- `check` missing alternate = nonconformant (`exit 1`); `fetch` missing alternate = HTML
  fallback (`exit 0`).

## Core scenarios

| ID | Scenario | Required result | Fixture/test |
| --- | --- | --- | --- |
| A01 | Same-origin, correct link and canonical, valid front matter | `fetch` returns Markdown only | `tests/test_reader.py` |
| A02 | No announced alternate | Return raw HTML, never guess `.md` | `tests/test_reader.py` |
| A03 | Copy missing, 404, bad UTF-8, BOM, or malformed front matter | `fetch` HTML fallback with reason. `check` errors (`COPY_NOT_OK` for non-200) | `tests/test_reader.py` |
| A04 | Cross-origin alternate or copy canonical mismatch | HTML fallback; `check` fails | `tests/test_urls.py`, `tests/test_validator.py` |
| A05 | Final page URL differs after redirect | Normalize against final URL, not requested alias | `tests/test_urls.py` |
| A06 | Accepts CRLF from agent read, flags publisher's CRLF as `should` warning | Correct parsing without false error | `tests/test_frontmatter.py` |
| A07 | Duplicate metadata keys | Reader first-wins, publisher checker errors | `tests/test_frontmatter.py` |
| A08 | Unknown `x-` field | Accepted and ignored | `tests/test_frontmatter.py` |
| A09 | Unknown unprefixed field | `fetch` returns Markdown and ignores the field. `check` errors | `tests/test_validator.py` |
| A10 | Alternate with `hreflang` | `fetch` selects the `hreflang` that equals `html lang`. No match returns HTML. `check` errors on a mismatch or on duplicate `hreflang` | `tests/test_discovery.py` |
| A11 | Copy text is not in the page's visible text | `fetch` returns Markdown. `check` errors with `FIDELITY_LOW` | `tests/test_fidelity.py` |
| A12 | Description/usage signals | Never used as instructions, and unspecified signals remain unspecified | `tests/test_frontmatter.py` |
| A13 | `robots.txt` disallows the copy URL | Copy is not fetched. `fetch` returns HTML, exit 0. `check` errors with `ROBOTS_DISALLOW` | `tests/test_robots.py` |
| A14 | HTTP timeout, redirect loop, oversized response | Failure of the named URL exits 3. Copy non-200 is `fetch` fallback and `check` exit 1. Copy timeout or copy over 1 MiB is `fetch` fallback and `check` exit 3 | `tests/test_security.py` |
| A15 | localhost, private address, or unsafe redirect target | Refused by default before content fetch, exit 3 | `tests/test_security.py` |
| A16 | Negotiated Markdown response | Accepted only after the HTML link and canonical checks succeed. A malformed copy is not accepted from the content type alone | `tests/test_reader.py` |
| A17 | `text/plain` Markdown copy | Do not reject only for media type | `tests/test_reader.py` |
| A18 | Missing `title`, `title` differing from the `h1`, or `altdown` other than `1` | Missing `title`: `fetch` returns Markdown, `check` errors. Title differing from the `h1`: warning, exit 0. `altdown` other than `1`: `fetch` falls back, `check` errors | `tests/test_validator.py` |
| A19 | Optional timestamps, `lang`, and `signals` | Absent optional fields produce no issue. A non-RFC 3339 timestamp is an error. `lang` differing from `html lang` is a warning. Malformed `signals` syntax is an error | `tests/test_validator.py` |
| A20 | CLI text/JSON and exit code contracts | Verified with Typer CliRunner | `tests/test_cli.py` |
| A21 | Link `type` carries parameters | Treated as no alternate. `fetch` falls back. `check` errors | `tests/test_discovery.py` |
| A22 | `description` longer than 300 characters | `fetch` returns Markdown. `check` errors | `tests/test_validator.py` |
| A23 | Body contains a `script`, `style` block, or HTML comment | `fetch` returns Markdown. `check` errors. The body stays data | `tests/test_validator.py` |
| A24 | `rel=canonical` disagrees with the final page URL | `fetch` compares the final URL only and can return Markdown. `check` errors | `tests/test_urls.py`, `tests/test_validator.py` |

## Fidelity limitations

The specification's five-word overlap is an **approximate positive coverage signal**.
It measures how much of the copy appears in the page's visible text. It does not
measure omitted main content, and v0.1 does not add an omission score. Do not label
a copy `trusted` from its overlap. `fetch` does not compute fidelity. For copies
containing fewer than five normalized words, report `fidelity.status=indeterminate`
and `score: null`. That result does not fail `check`.

Visible text is the whole page after removing `script`, `style`, `noscript`,
`template`, comments, and hidden content (`hidden`, `aria-hidden="true"`, inline
`display: none`). Navigation and footer text stay in the page side of the comparison.

## Security and test constraints

- Every HTTP call in the test suite is mocked; network disabled or deliberately failed.
- No credentials, tokens, cookies, or environment proxy settings used implicitly.
- Honor at most 5 redirects. Bound every response at 1 MiB read and a 10-second
  timeout, not only by a `Content-Length` header.
- DNS pre-resolution alone is not a rebinding defense. If secure address binding is
  not implemented, document limitation and do not claim server-side SSRF safety.
- Avoid following `file:`, `ftp:`, `data:`, localhost or RFC 1918 URLs without an
  explicit documented test-mode override.

## Definition of done

1. ADR is human-marked `Accepted`.
2. v0.1 `fetch` and `check` work as documented in a local offline smoke test.
3. All A01–A24 scenarios have tests, or a named, documented waiver reviewed by a human.
4. `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .` succeed.
5. `docs/ARCHITECTURE.md` describes implemented components and no longer says absent.
6. Public README examples are accurate, license is Apache-2.0, CI is green.
7. No unfinished v0.2 feature is silently bundled into v0.1.
