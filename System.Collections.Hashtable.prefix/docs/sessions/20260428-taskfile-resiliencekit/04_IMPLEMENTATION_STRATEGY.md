# Implementation Strategy

- Use a single root `Taskfile.yml`.
- Detect active workspaces from manifests and actual source files, not just marker files.
- Dispatch to repository-native commands instead of inventing wrappers.
- Treat Rust and Python as active targets; skip Go because `go/` has no source files yet.
