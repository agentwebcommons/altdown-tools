## Scope

- Feature / phase:
- ADR (if any), and status:
- Task IDs closed:
- Spec version checked:

## Verification (paste actual output)

- [ ] `python scripts/verify_scaffold.py`
- [ ] `uv run pytest`
- [ ] `uv run ruff check .`
- [ ] `uv run ruff format --check .`

## Review gates

- [ ] ADR human-accepted before implementation (if applicable)
- [ ] `docs/ARCHITECTURE.md` updated for actual boundary changes, or no boundary changed
- [ ] No deferred feature (`crawl`, `diff`, index sync, MCP) added accidentally
- [ ] Tests are offline, deterministic; HTTP and redirection failures covered
- [ ] Protocol behavior reflects external Altdown spec and docs/acceptance
- [ ] Security limitations and fallback semantics accurately documented
- [ ] Apache-2.0 license headers/notices respected; no CC-BY-SA spec copied
