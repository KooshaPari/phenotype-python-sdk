# phenotype-py-extras

Consolidated Python extras absorbed from retired Phenotype fleet repos (L5-114).

| Submodule     | Absorbed from                                | Purpose                                                       |
| ------------- | -------------------------------------------- | ------------------------------------------------------------- |
| `llms_txt`    | `KooshaPari/pheno-llms-txt`                  | Generate `llms.txt` files for repos (config + render + CLI).  |
| `request_id`  | `KooshaPari/phenotype-request-id`            | Contextvars-based request-ID propagation + FastAPI middleware.|
| `prompt_test` | `KooshaPari/pheno-prompt-test`               | Pytest plugin + assertions for LLM prompt regression testing. |

## Install

```bash
pip install phenotype-py-extras
# or with all extras:
pip install "phenotype-py-extras[all]"
```

## Quickstart — llms_txt

```python
from phenotype_py_extras.llms_txt import init_llms, render, write_llms_txt

# Scaffold a starter YAML + render llms.txt (idempotent)
result = init_llms(".", repo_name="my-project", tagline="My project.")
print(result)  # {"config_path": "...", "llms_path": "...", "created_config": True}
```

CLI:

```bash
pheno-llms-txt --config pheno-llms-txt.yaml --out llms.txt
```

## Quickstart — request_id

```python
from fastapi import FastAPI
from phenotype_py_extras.request_id import RequestIDMiddleware

app = FastAPI()
app.add_middleware(RequestIDMiddleware)
```

```python
# Anywhere in the call stack (handlers, log statements, downstream libs):
from phenotype_py_extras.request_id import get_request_id
print(get_request_id())  # current request's ID, or None
```

## Quickstart — prompt_test

```toml
# pyproject.toml
[project.optional-dependencies]
test = ["phenotype-py-extras[testing]"]
```

```python
# tests/test_prompts.py
def test_greeting(pheno_prompt, pheno_prompt_cache):
    from phenotype_py_extras.prompt_test import assert_prompt_match
    actual = "Hello, world!"
    assert_prompt_match(actual, pheno_prompt)
    _, write_fn = pheno_prompt_cache
    write_fn(actual)
```

Fixtures are auto-loaded from `prompts/test_<name>.{txt,json}`.

## Origin (L5-114)

These three libraries were originally independent repos:

- `KooshaPari/pheno-llms-txt` — deleted 2026-06-20 (404)
- `KooshaPari/phenotype-request-id` — deleted 2026-06-20 (404)
- `KooshaPari/pheno-prompt-test` — deleted 2026-06-20 (404)

Their content was re-authored into this single package on 2026-06-20 from the
audit-finding docs (which preserved the API surface + algorithm descriptions
even after the source repos were deleted). See:

- `findings/2026-06-19-L5-114-pheno-llms-txt-absorption.md`
- `findings/2026-06-19-L5-114-phenotype-request-id-absorption.md`
- `findings/2026-06-19-L5-114-pheno-prompt-test-absorption.md`
- `findings/2026-06-20-L5-114-fabrication-postmortem.md`

## License

MIT — see `LICENSE`.