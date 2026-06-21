# prompt_test specification

pytest plugin + assertion helpers for LLM prompt regression testing.

## 1. Scope

`prompt_test` provides:

1. A pytest plugin that auto-collects prompt fixtures (`prompts/*.txt` or
   `prompts/*.json`) and registers the `pheno_prompt` / `pheno_prompt_cache`
   fixtures.
2. Standalone assertion helpers (`assert_prompt_match`, `assert_prompt_contains`,
   `assert_prompt_json`) usable outside pytest.

## 2. Public API

```python
from phenotype_py_extras.prompt_test import (
    assert_prompt_match,        # (actual, expected, *, strip=True, ignore_case=False)
    assert_prompt_contains,     # (actual, needle, *, ignore_case=False, as_regex=False)
    assert_prompt_json,         # (actual, expected, *, ignore_case_keys=False)
)

# pytest plugin (auto-loaded via the `pheno_prompt_test` pytest11 entry point):
#   - pheno_prompt(request) -> str | dict | None
#   - pheno_prompt_cache(request, pheno_prompt) -> tuple[Path, Callable[[str|dict], None]]
#   - @pytest.mark.prompt  (recognized by name)
```

## 3. CLI

```bash
pytest --prompt-cache-dir=.pheno_prompts
```

## 4. Fixture discovery

For a test named `test_foo` in `tests/test_bar.py`, the plugin looks for:

1. `prompts/test_bar/test_foo.json`
2. `prompts/test_bar/test_foo.txt`
3. `prompts/test_foo.json`
4. `prompts/test_foo.txt`

JSON fixtures are parsed and returned as dicts; text fixtures are returned
as strings.

## 5. Cache format

`pheno_prompt_cache` writes JSON like:

```json
{
  "test": "test_foo",
  "prompt_sha256": "<sha256 of the prompt fixture>",
  "actual": "<string or JSON-encoded dict>"
}
```

## 6. See also

- `pheno-prompt-test` (deleted 2026-06-20) — original source repo.
- `findings/2026-06-19-L5-114-pheno-prompt-test-absorption.md` — L5-114 audit.