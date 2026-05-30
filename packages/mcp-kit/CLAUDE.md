# McpKit

Model Context Protocol kit — multi-language MCP implementation across Rust, Python, Go, and TypeScript.

## Stack
| Layer | Technology |
|-------|------------|
| Core | Rust + Python + Go + TypeScript |
| Python | fastmcp, Pydantic, httpx |
| Rust | rust/, workspace crates |
| Go | go/ |
| TypeScript | typescript/ |
| MCP | Model Context Protocol 2.13+ |
| Docs | VitePress |

## Key Commands
```bash
# Rust
cd rust && cargo build --workspace
cargo test --workspace

# Python
cd python && pip install -e .
python -m mcpkit_python

# TypeScript
cd typescript && npm install
npm run build

# Go
cd go && go build ./...

# Docs
cd docs && npm install
npm run docs:dev
```

## Key Files
- `rust/` — Rust workspace crates
- `python/` — Python packages
- `go/` — Go modules
- `typescript/` — TypeScript packages
- `docs/` — VitePress documentation
- `shaders/` — GLSL/shader assets
- `tests/` — Integration tests

## Reference
Global Phenotype rules: see `~/.claude/CLAUDE.md` or `/Users/kooshapari/CodeProjects/Phenotype/repos/CLAUDE.md`
