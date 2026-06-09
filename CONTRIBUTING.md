# Contributing

Thanks for your interest in the Phenotype Python SDK. This monorepo consolidates
several kits; contributions should follow the conventions of the kit they touch.

## Workflow

1. **Spec first** — open or update a `kitty-spec` under
   `kitty-specs/<feature>/` and get sign-off before substantial changes.
2. **Branch** — create a feature branch in a worktree:
   `git worktree add ../phenotype-python-sdk-wtrees/<topic> origin/main -b feat/<topic>`
3. **Tests** — add or update tests; PRs without tests are not merged for
   logic changes.
4. **Quality** — `just ci` (lint + typecheck + test) must pass locally.
5. **Commit** — Conventional Commits; include kit prefix where relevant
   (`feat(mcp-kit): ...`).
6. **PR** — open against `main`; one logical change per PR.

## Per-kit conventions

- **mcp-kit** — Python + Rust + Go mixed sources. Use the kit's own `justfile`
  when present.
- **testing-kit** — Python `uv` workspace under `python/`.
- **auth-kit / data-kit / observability-kit / resilience-kit** — follow each
  kit's `pyproject.toml`; prefer `uv` when available.

## Style

- Python: `ruff format` + `ruff check`, `mypy --strict` for new modules.
- Rust: `cargo fmt`, `cargo clippy --all-targets --all-features -- -D warnings`.
- Go: `gofmt`, `go vet`, `staticcheck` (where configured).

## Commit hygiene

Split commits by provenance (see global `CLAUDE.md` — Dirty-Tree Commit
Discipline). Don't lump unrelated changes.

## Sign-off

By submitting a contribution, you agree to license your work under the
repository's license (see `LICENSE`).
