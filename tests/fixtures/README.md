# Synthetic Altdown fixtures

All fixtures are original, deliberately minimal and **offline**. They are not
snapshots of any real site or replacements for the external Altdown specification.

- `valid/` has a complete page and companion copy.
- Other directories vary one feature at a time, for error and warning tests.
- `manifest.json` names the intended outcomes. Its descriptions are **test design**,
  not implemented passing tests.
- Map `https://example.org/garden/` to `page.html` and
  `https://example.org/garden/page.md` to `page.md` with `respx` in tests.
- `robots-disallow/` should be combined with the valid pair.
- Add every acceptance scenario in `ACCEPTANCE.md`; the current fixture set is just
  the starting pool.

Keep malformed copies as text files; do not import them as Python source.
