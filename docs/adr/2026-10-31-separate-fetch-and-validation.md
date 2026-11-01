# Separate the Altdown reader and publisher validator

- Date: 2026-10-31
- Status: **Proposed**
- Decision owner: Agent Web Commons maintainers
- Spec: https://altdown.org/1.0/

## Context

Altdown has two different consumers. An **agent** needs to retrieve useful content
reliably and fall back to HTML when a copy is absent or invalid. A **publisher** needs
strict, explainable conformance failures. The reader must not turn an approximate
fidelity score into a false claim of trust. Fetching arbitrary URLs also introduces
network and redirect risks that must be bounded.

## Decision

**Implement one shared HTTP/discovery/front-matter core with separate fail-open-to-HTML
`fetch` and strict diagnostic `check` surfaces, returning typed results with explicit
source, warnings, and failure reasons.**

The library is synchronous in v0.1; CLI functions are thin wrappers. The HTTP transport
is injectable for tests. A copy is never elevated to trusted instructions. Public-network
CLI use is the intended v0.1 operating context; do not advertise it as safe for
multi-tenant server-side fetching of arbitrary untrusted URLs.

Status stays **Proposed** until a human sets **Accepted**. The tool policy below is
the text to accept. It is repository policy for this local CLI and library. It does
not amend the Altdown draft.

### v0.1 tool policy

`fetch` and `check` both call one `load_page` function for HTTP, redirects, robots,
discovery, and front matter.

**`fetch` returns Markdown** only when every item below holds:

- The page has a usable same-origin `link rel="alternate" type="text/markdown"` in
  `head`, with no parameters on `type`. When several Markdown alternates exist, each
  `hreflang` is distinct, and `fetch` selects the alternate whose `hreflang` equals
  the page's `html lang`. If none matches, `fetch` returns HTML.
- A negotiated `text/markdown` response still requires a follow-up HTML fetch that
  finds that link. This is narrower than the draft sentence that skips discovery.
- The copy is HTTP 200, UTF-8, and has no BOM. Front matter is present, `altdown`
  is `1`, and `canonical` matches the final page URL after RFC 3986 normalization.
  `fetch` compares that final URL only. It does not also require a match to
  `link rel=canonical`.
- `robots.txt` allows the copy. The URL the user named is fetched even when
  `robots.txt` disallows that page. An unreachable or missing `robots.txt` allows
  the copy. The `Altdown:` line is not permission.

On that path, `fetch` still returns Markdown when `title` is missing, `title` differs
from the `h1`, the copy uses CRLF, a key is duplicated (the first value wins), or a
field is unknown. Unknown fields, including unprefixed ones, are ignored. `fetch`
does not compute fidelity.

**`fetch` returns raw HTML** (`format=html`, `source=html-fallback`, exit 0) with a
reason when any accept condition fails, including copy non-200, a copy timeout, or a
copy body over the byte cap. Failure or refusal of the URL the user named is an
operational error (exit 3): timeout, redirect loop, body over the byte cap, or a
private, loopback, link-local, reserved, or credential-bearing target.

**`check` errors (exit 1)** for every condition that makes `fetch` fall back, except
copy timeout and copy oversize, and also for:

- missing `title`, duplicate keys, an unprefixed unknown field
- `description` longer than 300 characters
- a link `type` that carries parameters
- a `script`, `style` block, or HTML comment in the body
- `lang` / `hreflang` mismatch, or duplicate `hreflang` values
- `canonical` disagreeing with `link rel=canonical` when that element is present
- copy HTTP status other than 200 (`COPY_NOT_OK`)
- a robots disallow of the copy (`ROBOTS_DISALLOW`); the copy is not fetched
- five-word overlap below 0.90 (`FIDELITY_LOW`), labeled as a heuristic

**`check` warnings stay on exit 0:** CRLF, and a `title` that differs from the
level-one heading. Absent optional fields produce no issue. A present `updated` or
`published` value that is not RFC 3339 UTC is an error. A `lang` that differs from
the page's `html lang` is a warning. Malformed `signals` syntax is an error.
Unspecified signals stay unspecified. Fewer than five normalized words sets fidelity
to `indeterminate` and does not fail the check by itself.

Copy timeout or a copy body over 1 MiB is exit 3 for `check`. The same events on
the URL the user named are exit 3 for both commands.

**Fidelity** runs only in `check`, on the one requested URL. Extraction follows the
draft: remove `script`, `style`, `noscript`, `template`, comments, and hidden
content (`hidden`, `aria-hidden="true"`, inline `display: none`), then use the
remaining visible text of the whole page, including navigation and footer. The score
is the share of the copy's five-word sequences found in that text. Overlap does not
measure omitted main content, and v0.1 does not add a separate omission score.

**Budgets,** as tool policy: at most 5 redirects, a 10-second timeout, and 1 MiB
read per response body regardless of `Content-Length`. Use a stable product
User-Agent. No cookies, credentials, environment proxies, retries, or cache. DNS
rebinding is unsolved. v0.1 is a local CLI and library, not a hosted fetch service.

## Alternatives considered

1. **One `fetch` function that always validates everything.** Rejected: turns a
   heuristic fidelity check into a mandatory read-time network round trip.
2. **Independent implementations for CLI and library.** Rejected: conformance drift.
3. **Only a publisher validator.** Rejected: no reference agent-side consumer, the
   principal adoption gap.
4. **Headless-browser extraction.** Rejected: high complexity, active script risk and
   different trust boundaries. HTML fallback is explicit, not silently re-rendered.
5. **Automatic private-network access.** Rejected: URL processing must have a bounded,
   conservative default; local testing may need an explicit exception later.

## Consequences

- Typed `FetchResult`, `CheckReport`, and structured diagnostics are public API contracts.
  Check issues carry `severity` of `error` or `warning`. `FIDELITY_LOW` is an error
  and is labeled as a heuristic.
- `fetch` returns raw HTML on fallback, never masquerading it as Markdown, and does
  not compute fidelity.
- `fetch` and `check` share `load_page`. A second HTTP or discovery path is a drift bug.
- Negotiation is in v0.1 and always re-fetches HTML to confirm the link element.
- An HTTP transport abstraction, robots policy, and redirect tests are required.
  DNS rebinding is documented as out of scope for hosted use.
- The implementation stays small: no plugins, caching, retry engine, web server or browser.
- The trust-boundary rules require a future ADR before embedding in hosted services.

## Confirmation

After implementation, all should pass:

```bash
uv run pytest tests/test_reader.py tests/test_validator.py tests/test_security.py
uv run pytest tests/test_cli.py
uv run ruff check .
```

Review that no CLI path silently bypasses `load_page` or treats page content as an
instruction. Also verify `fetch` does not promise fidelity verification.
