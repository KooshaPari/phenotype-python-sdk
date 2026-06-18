# Origin — `agentmcp-hex`

This package was extracted from a now-archived source repository to preserve
clean, in-domain code that would otherwise have been lost during fleet
consolidation.

## Source

| Field | Value |
|-------|-------|
| Source repo | [`KooshaPari/McpKit`](https://github.com/KooshaPari/McpKit) |
| Source path | `python/agentmcp/` |
| Source license | MIT |
| Original `pyproject.toml` `name` | `agentmcp` |
| Original version | `0.1.0` (2026-06-08) |
| Merged-into repo (intermediate) | `KooshaPari/McpKit` (itself archived 2026-06-17) |
| Source status | **ARCHIVED** — read-only marker on GitHub |
| Upstream-of-source | `AgentMCP` (independently archived prior to merge) |

## Extraction

| Field | Value |
|-------|-------|
| Extracted to | [`KooshaPari/phenotype-python-sdk`](https://github.com/KooshaPari/phenotype-python-sdk) |
| Target path | `packages/agentmcp-hex/` |
| New Python import | `agentmcp_hex` (was `agentmcp`) |
| New package `name` | `agentmcp-hex` (was `agentmcp`) |
| New version | `0.3.0` (bumped from `0.1.0`) |
| Extraction date | 2026-06-18 |
| Extraction rationale | McpKit absorption audit (L5-099): `agentmcp` was "the cleanest code in the repo" and a textbook hexagonal-DDD layout. Source repo archived 2026-06-17 — extract before code is lost. |

## Provenance trail

1. **2026-06-08** — `KooshaPari/AgentMCP` merged into `KooshaPari/McpKit`
   at `python/agentmcp/`. See `McpKit/python/agentmcp/docs/SSOT.md`.
2. **2026-06-17** — `KooshaPari/McpKit` archived per the McpKit absorption
   audit (ADR-003). All public-facing McpKit capabilities were either
   migrated to substrate (`pheno-mcp-router`, `PhenoFastMCP`) or
   deprecated. The `python/agentmcp/` sub-package was identified in the
   audit as clean code that should be preserved as a fleet lib rather
   than lost during archival.
3. **2026-06-17** — `PhenoFastMCP/FORK-NOTES.md:121` documented the
   intended supersession path: `AgentMCP hex adapters → python/pheno/
   layer`. That target layer was never built.
4. **2026-06-18** — This extraction realizes that intent. The package is
   placed at `packages/agentmcp-hex/` in the `phenotype-python-sdk`
   monorepo (the workspace that already holds the rest of the Phenotype
   Python SDK).

## Audit cross-reference

- McpKit absorption audit: `findings/2026-06-17-L5-099-mcpkit-absorption.md`
- ADR-003 (McpKit merge into PhenoMCP): `docs/adr/2026-06-14/ADR-003-mcpkit.md`
- ADR-023 (app-substrate placement): `docs/adr/2026-06-15/ADR-023-agent-effort-governance.md`
- ADR-018 (Polyglot Reuse via Canonical Ports): `docs/adr/2026-06-15/ADR-018-prcp-pattern.md`

## License

MIT — original code from `KooshaPari/McpKit` (archived) preserved under
the same MIT license. See `LICENSE-MIT` in the source repo.