# Known Issues

- `task lint` currently fails on pre-existing Python issues in `python/deploy-kit/src/pheno_deploy_kit/*` and related modules. The Taskfile wiring is working; the repo code still needs separate cleanup for Ruff findings.

- The repository layout includes Go and Python directories, but the current task runner targets the Rust workspace that exists in this checkout.
- The Rust workspace was narrowed to the two crates present in this clone so `cargo`-based tasks can run without missing local path dependencies.
