<!-- AI-DD-META:START -->
<!-- This repository is planned, maintained, and managed by AI Agents only. -->
<!-- Slop issues are expected and intentionally present as part of an HITL-less -->
<!-- /minimized AI-DD metaproject of learning, refining, and building brute-force -->
<!-- training for both agents and the human operator. -->
![Downloads](https://img.shields.io/github/downloads/KooshaPari/phenotype-python-sdk/total?style=flat-square&label=downloads&color=blue)
![GitHub release](https://img.shields.io/github/v/release/KooshaPari/phenotype-python-sdk?style=flat-square&label=release)
![License](https://img.shields.io/github/license/KooshaPari/phenotype-python-sdk?style=flat-square)
![AI-Slop](https://img.shields.io/badge/AI--DD-Slop%20Expected-orange?style=flat-square)
![AI-Only-Maintained](https://img.shields.io/badge/Planned%20%26%20Maintained%20by-AI%20Agents%20Only-red?style=flat-square)
![HITL-less](https://img.shields.io/badge/HITL--less%20AI--DD-metaproject-yellow?style=flat-square)

> ⚠️ **AI-Agent-Only Repository**
>
> This repo is **planned, maintained, and managed exclusively by AI Agents**.
> Slop issues, rough edges, and AI artifacts are **expected and intentionally
> present** as part of an **HITL-less / minimized AI-DD** metaproject focused
> on learning, refining, and brute-force training both the agents and the
> human operator. Bug reports and contributions are still welcome, but please
> expect AI-generated code, comments, and documentation throughout.
<!-- AI-DD-META:END -->
## Work State

| Field | Value |
|---|---|
| Last commit | 2026-06-02 |
| Open issues | 1 |
| Open PRs | 1 |
| Focus | Python SDK monorepo (ADR-011) |

Progress: ████████░░ 80%

# phenotype-python-sdk

Monorepo of Phenotype org Python (and polyglot) SDK kits, consolidated from standalone kit repositories.

## Workspace kits

| Kit | Path | Role |
|-----|------|------|
| **mcp-kit** | `packages/mcp-kit` | Model Context Protocol tooling (Python, Rust, Go) |
| **testing-kit** | `packages/testing-kit` | QA, quality CLI, analysis, and test harnesses |
| **auth-kit** | `packages/auth-kit` | Authentication and security helpers |
| **resilience-kit** | `packages/resilience-kit` | Deploy, CI/CD, and resilience utilities |

### Python sub-projects (under kits)

- `packages/testing-kit/python/` — `qa-kit`, `pheno-testing-cli`, `pheno-quality-tools`, `pheno-quality-cli`, `pheno-analysis-cli`, `mcp-qa`
- `packages/resilience-kit/python/` — `deploy-kit`, `ci-cd-kit`, `pheno-deploy`

See each package’s `README.md` and `pyproject.toml` for install and usage.

## Development

Root `pyproject.toml` documents the workspace layout. Per-package tooling may use Poetry, setuptools, or Hatch — follow the kit you are changing.

```bash
cd packages/<kit>/python   # when applicable
# use that package's documented install (poetry install, pip install -e ., etc.)
```

## License

MIT — see [LICENSE](LICENSE).