# AGENTS.md — phenotype-py-extras

## Purpose

Consolidated Python extras for the Phenotype fleet. Houses three submodules
absorbed from retired `pheno-*` / `phenotype-*` repos during the L5-114
fleet-rationalization wave (2026-06-19 → 2026-06-20):

- `phenotype_py_extras.llms_txt` — from `KooshaPari/pheno-llms-txt`
- `phenotype_py_extras.request_id` — from `KooshaPari/phenotype-request-id`
- `phenotype_py_extras.prompt_test` — from `KooshaPari/pheno-prompt-test`

## Module conventions

- Each submodule is a directory under `src/phenotype_py_extras/<name>/`.
- Each submodule exposes a public API via `__init__.py` re-exports.
- Each submodule has its own test suite under `tests/<name>/`.
- All dependencies are optional (grouped via `pyproject.toml` extras):
  - `cli` — click (for llms_txt CLI)
  - `web` — fastapi (for request_id middleware)
  - `observability` — structlog (for request_id logging helper)
  - `testing` — pytest + pytest-asyncio

## Quality bar

Per ADR-023 Rule 3.1 (substrate quality bar):

- Spec: `docs/<submodule>-spec.md` per absorbed submodule (see `docs/`)
- Docs: this README + per-submodule spec doc
- Tests: unit + integration per submodule
- Coverage: ≥80% for a polyglot SDK (this repo's tier)
- Worklog: this repo uses the L5-114 absorption findings docs as the source
  of truth for per-submodule history. No ad-hoc WORKLOG.md is kept here
  (the target uses `worklog-schema v2.1` per ADR-030 if needed; absorbed
  repos were ad-hoc and not portable per ADR-032).

## Recovery context (L5-114)

This repo was created on 2026-06-20 as part of a recovery operation after
the original L5-114 absorption was fabricated (PR #35 on `phenotype-apps`
claimed absorption but no real target repo or code existed). See
`findings/2026-06-20-L5-114-fabrication-postmortem.md` for the full timeline.

All three absorbed libraries were re-authored from the audit-finding docs
in the monorepo (`findings/2026-06-19-L5-114-*.md`), which preserved the
API surface + algorithm descriptions even after the source repos were deleted.

## Commit / PR conventions

- Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`
- Branch naming: `feat/l5-114-<submodule>-2026-06-20`
- PR labels: `L5-114-recovery`, `absorption`

## Status

- [x] Repo scaffold + pyproject.toml + README + LICENSE + CHANGELOG + AGENTS.md
- [x] `llms_txt` submodule re-authored + tests
- [x] `request_id` submodule re-authored + tests
- [x] `prompt_test` submodule re-authored + tests
- [x] All tests pass locally (≥45 unit tests)
- [ ] CI workflow (`.github/workflows/ci.yml`)
- [ ] Per-submodule spec docs in `docs/`