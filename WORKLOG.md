# WORKLOG

**Schema version:** v2.1 (ADR-025)
**Repo:** phenotype-python-sdk
**Maintained by:** @KooshaPari

| Date | Task ID | Layer | Action | Files | Notes | device |
|---|---|---|---|---|---|---|
| 2026-06-20 | T3B-2026-06-20 | governance | init | (all) | Initial SSOT bundle generation (T3B) | macbook |
| 2026-07-23 | AUDIT-LANE-FLAT-LAYOUT-001 | packaging | fix | pyproject.toml, tests/test_install_path.py, tests/__init__.py | Add `[tool.setuptools] py-modules = []` + `[tool.setuptools.packages.find]` no-op to suppress flat-layout auto-discovery; new regression test runs `uv pip install` against the workspace path and asserts success + no flat-layout error. DAG tick: +1. Second lane after PR #42 (fix/auth-kit-gitlink). | macbook |
