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