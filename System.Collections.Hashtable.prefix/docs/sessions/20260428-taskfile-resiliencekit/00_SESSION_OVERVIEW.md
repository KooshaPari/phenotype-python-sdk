# Session Overview

- Goal: add a root `Taskfile.yml` that detects the repo language and exposes common tasks.
- Scope: `build`, `test`, `lint`, and `clean`.
- Active languages detected in this repo: Rust workspace under `rust/` and Python package roots under `python/`.
- `go/` contains a `go.work` file but no `.go` sources, so it is not treated as an active target.
- Success criteria: `task detect`, `task build`, `task test`, `task lint`, and `task clean` operate on the detected Rust and Python workspaces without manual path selection.
