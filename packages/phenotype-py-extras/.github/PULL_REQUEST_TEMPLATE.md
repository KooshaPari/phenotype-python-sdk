name: PULL_REQUEST_TEMPLATE

## Summary

<!-- 1-3 sentences describing the change. -->

## Submodule touched

<!-- Pick one or leave blank if multi-submodule -->

- [ ] `phenotype_py_extras.llms_txt`
- [ ] `phenotype_py_extras.request_id`
- [ ] `phenotype_py_extras.prompt_test`
- [ ] meta (README, pyproject, CI, AGENTS.md, docs/)

## L5 tracking

<!-- If related to a fleet wave, e.g. L5-114 -->

- [ ] L5-114 recovery
- [ ] other: ____

## Checklist

- [ ] `pytest -ra` passes locally
- [ ] New code has tests
- [ ] Public API re-exports added to the submodule's `__init__.py`
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] If touching docs/spec, the `docs/<submodule>-spec.md` is updated