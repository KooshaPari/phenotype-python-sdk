"""phenotype_py_extras: consolidated Python extras absorbed from retired Phenotype fleet repos.

Submodules (populated incrementally by per-submodule PRs during L5-114 recovery):
    - llms_txt:    LlmConfig + render + load_config + write_llms_txt + init_llms + CLI
                   (absorbed from KooshaPari/pheno-llms-txt, L5-114)
    - request_id:  contextvars-based request-ID propagation + FastAPI middleware + structlog binding
                   (absorbed from KooshaPari/phenotype-request-id, L5-114)
    - prompt_test: pytest plugin + assertions for LLM prompt regression testing
                   (absorbed from KooshaPari/pheno-prompt-test, L5-114)

See:
    - findings/2026-06-19-L5-114-pheno-llms-txt-absorption.md
    - findings/2026-06-19-L5-114-phenotype-request-id-absorption.md
    - findings/2026-06-19-L5-114-pheno-prompt-test-absorption.md
"""

__version__ = "0.1.0"
__all__ = ["llms_txt", "request_id", "prompt_test"]  # L5-114 recovery: PR #1 (llms_txt) + PR #4 (request_id) + PR #5 (prompt_test)
