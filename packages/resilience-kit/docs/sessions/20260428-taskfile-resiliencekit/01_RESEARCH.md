# Research

- Root repo has a Rust workspace manifest at `rust/Cargo.toml`.
- Root README describes Rust as the primary implementation language.
- A root `Taskfile.yml` already existed, but it only detected a single primary language and treated `go/` as active despite the absence of `.go` sources.
- Python package manifests exist at `python/ci-cd-kit/pyproject.toml` and `python/deploy-kit/pyproject.toml`.
- `go/` currently contains `go/go.work` only; there are no `.go` files or `go.mod` manifests.
- Existing Rust workspace commands are `cargo build --workspace`, `cargo test --workspace`, and `cargo clippy --workspace --all-targets --all-features -- -D warnings`.
