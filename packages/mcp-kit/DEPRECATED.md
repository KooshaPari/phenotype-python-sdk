# DEPRECATED — `mcp-kit` is being retired

> **Status:** DEPRECATED (effective **2026-06-22**)
> **Notice posted:** 2026-06-18
> **Source archived:** 2026-06-17 (`KooshaPari/McpKit`)
> **Authority:** [ADR-017 — MCP polyrepo boundaries](https://github.com/KooshaPari/PhenoSpecs/blob/main/adrs/017-mcp-polyrepo-boundaries.md)
> **Registry row:** [`phenotype-registry/registry/disposition-index.json`](https://github.com/KooshaPari/phenotype-registry) — `id: 28` (`crates/phenotype-mcp`, wave D, `fsm: done`, note: "McpKit retired per registry #100; HexaKit#255 stub")
> **Full retirement:** TBD (tracked in [KooshaPari/phenotype-python-sdk#TODO](https://github.com/KooshaPari/phenotype-python-sdk/issues))

---

## Why

The upstream source `KooshaPari/McpKit` is **archived** on GitHub (push returned *"This repository was archived so it is read-only"*). The mirror at `phenotype-python-sdk/packages/mcp-kit/` is **incomplete and orphaned**:

- 4 of 5+ Rust crates present (`mcp-forge`, `phenotype-mcp-asset`, `phenotype-mcp-core`, `phenotype-mcp-framework`).
- **Missing** Rust crates: `phenotype-mcp-fast`, `phenotype-mcp-fast-macros`, `agentora`.
- **Missing** `python/` subdirectory entirely (the Python half advertised in the SDK's root `README.md` table never landed in this mirror).
- **No** Go modules wired (`go/go.work` is a stub).
- **No** TypeScript package published.

The mirror is therefore neither buildable as Rust (incomplete workspace) nor installable as Python (no package surface), nor runnable as Go/TS. ADR-017 retires the polyrepo structure; this mirror is a casualty.

---

## Migration targets

| Language | Use this instead | Source |
|----------|------------------|--------|
| **Python** | [`PhenoFastMCP`](https://github.com/KooshaPari/PhenoFastMCP) | Vendored from `PrefectHQ/fastmcp` |
| **Rust**   | [`PhenoFastMCP-rust`](https://github.com/KooshaPari/PhenoFastMCP-rust) | Vendored from `Dicklesworthstone/fastmcp_rust` |
| **Go**     | [`PhenoFastMCP-go`](https://github.com/KooshaPari/PhenoFastMCP-go) | Vendored from `mark3labs/mcp-go` |
| **Catalog** | [`PhenoMCPServers`](https://github.com/KooshaPari/PhenoMCPServers) — `catalog/registry.yaml` | Canonical registry of MCP servers / tools / resources / prompts |

Do **not** start new development against `packages/mcp-kit/`. The 1-week deprecation window (2026-06-18 → 2026-06-22) is for consumers to finish reading existing code, copy snippets if needed, and move import paths to the targets above.

---

## Source provenance

- **Upstream:** `KooshaPari/McpKit` (archived 2026-06-17, GitHub read-only tombstone).
- **Mirror:** `phenotype-python-sdk/packages/mcp-kit/` (this directory).
- **Absorption audit:** see `findings/2026-06-15-mcpkit-absorption-audit.md` in the monorepo root (Block-C disposition, sdk-canonical reconcile).
- **Cross-repo signal:** `phenotype-registry/registry/disposition-index.json` row `id: 28` (`crates/phenotype-mcp`, wave D, `fsm: done`).
- **Sister deprecations (polyrepo collapse):** [`settly-*`](https://github.com/KooshaPari), [`pheno-vessel-*`](https://github.com/KooshaPari), [`pheno-types-*`](https://github.com/KooshaPari), [`pheno-profiling`](https://github.com/KooshaPari/Profila) — all under the same ADR-017 / ADR-021 wave.

---

## What stays

Until full retirement (TBD), this directory is **read-only**:

- The Rust `Cargo.toml` and partial workspace remain for historical reference.
- `registry.yaml` is kept as a frozen snapshot (status was `planning` at mirror time; do not update).
- `pyproject.toml` is dev-tooling only (`packages = []`); it never installed a Python package.
- All binding docs in `README.md` are preserved verbatim for archaeology.

**Do not:**
- Add new tools, resources, prompts to `registry.yaml`.
- Wire `go.work` to a real module.
- Publish a `typescript/package.json` (the placeholder `package.json` is a stub).
- Open PRs against this directory other than to update this deprecation notice.
- Reference `phenotype-python-sdk/packages/mcp-kit/` in new code, new docs, or new READMEs.

---

## What to do if you arrived here from a `git clone`

You are looking at a deprecated, incomplete, archived mirror. Close this tab and go to the migration targets above. There is no support path for this directory after 2026-06-22.

---

*Posted by the Phenotype substrate circle per ADR-017 / ADR-023. Questions: open an issue on `phenotype-registry` referencing `disposition-index.json#id=28`.*
