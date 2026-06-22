# Changelog

All notable changes to `phenotype-py-extras` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- L5-114 recovery: re-authored `llms_txt`, `request_id`, `prompt_test` submodules
  from audit-finding docs after the 3 source repos (`pheno-llms-txt`,
  `phenotype-request-id`, `pheno-prompt-test`) and the original target repo
  were all deleted (HTTP 404) prior to absorption. See
  `findings/2026-06-20-L5-114-fabrication-postmortem.md`.

## [0.1.0] - 2026-06-20

### Added
- Initial release (L5-114 recovery): consolidated Python extras package.
- `phenotype_py_extras.llms_txt` — LlmConfig dataclass + render() + write_llms_txt() +
  load_config() + validate_config() + init_llms() + click CLI (`pheno-llms-txt`).
- `phenotype_py_extras.request_id` — request_id_var contextvar + new_request_id() +
  get/set/reset/clear helpers + RequestIDMiddleware (FastAPI/Starlette ASGI) +
  bind_request_id_to_logger() (optional structlog integration).
- `phenotype_py_extras.prompt_test` — pytest11 entry point + pheno_prompt /
  pheno_prompt_cache fixtures + assert_prompt_match / assert_prompt_contains /
  assert_prompt_json assertion helpers.
- Test suites for all 3 submodules.