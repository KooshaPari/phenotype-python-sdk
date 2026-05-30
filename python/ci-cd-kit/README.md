# CI/CD Kit

Reusable GitHub Actions workflow templates for Python projects. Provides coverage reporting, quality gates, import linting, file size guards, and more.

## Overview

CI/CD Kit is a collection of composable, reusable GitHub Actions workflows designed to enforce quality standards across Python projects. These workflows support both `pip` and `uv` package managers and are designed to be called via `workflow_call` from your project's CI configuration.

## Workflows

### Coverage Workflows

| Workflow | Description | File |
|----------|-------------|------|
| **Coverage Gate** | General coverage analysis with threshold enforcement | `coverage.yml` |
| **Python Coverage** | Python-specific coverage with pytest and Codecov upload | `coverage_python.yml` |

**Features:**
- Configurable coverage threshold (default: 80%)
- Support for both `uv` and `pip` package managers
- XML and HTML report generation
- Codecov integration
- Artifact upload for coverage reports

### Quality Gate Workflows

| Workflow | Description | File |
|----------|-------------|------|
| **Import Linter Gate** | Validates import boundaries using import-linter | `import_linter.yml` |
| **Legacy Imports Guard** | Prevents legacy/disallowed imports from being added | `legacy_imports.yml` |
| **File Size Guard** | Blocks files exceeding size limit (default: 50MB) | `file_size_guard.yml` |

**Features:**
- Import boundary enforcement
- Legacy dependency detection
- PR-scoped file size checking
- Configurable limits and thresholds

### QA Workflows

| Workflow | Description | File |
|----------|-------------|------|
| **QA Aegis** | Test ingestion with JUnit XML support | `qa_aegis.yml` |
| **QA E2E** | End-to-end testing with Playwright | `qa_e2e.yml` |

**Features:**
- JUnit XML test result ingestion
- Playwright-based E2E testing
- QA database artifact generation
- Multi-requirements file support

## Usage

### Calling a Workflow

In your project's `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  coverage:
    uses: your-org/ci-cd-kit/.github/workflows/coverage.yml@main
    with:
      python_version: '3.13'
      coverage_threshold: '85'
      use_uv: true

  import-linter:
    uses: your-org/ci-cd-kit/.github/workflows/import_linter.yml@main
    with:
      python_version: '3.13'
      use_uv: true

  file-size-guard:
    uses: your-org/ci-cd-kit/.github/workflows/file_size_guard.yml@main
    with:
      file_size_limit_mb: '50'
```

### Workflow Inputs Reference

#### coverage.yml

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `python_version` | string | `3.13` | Python version to use |
| `coverage_threshold` | string | `80` | Minimum coverage percentage |
| `use_uv` | boolean | `true` | Use uv package manager |

#### coverage_python.yml

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `python_version` | string | `3.11` | Python version to use |
| `test_path` | string | `tests` | Path to test files |
| `test_markers` | string | `not integration` | Test markers to run |
| `coverage_threshold` | string | `80` | Minimum coverage percentage |
| `requirements_files` | string | `requirements.txt,requirements-dev.txt` | Comma-separated requirements files |

#### import_linter.yml

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `python_version` | string | `3.13` | Python version to use |
| `use_uv` | boolean | `true` | Use uv package manager |
| `lint_command` | string | `lint-imports --verbose` | Import linting command |

#### legacy_imports.yml

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `python_version` | string | `3.12` | Python version to use |
| `legacy_script_path` | string | `scripts/ci_check_legacy_imports.py` | Path to legacy check script |
| `requirements_files` | string | `requirements.txt,requirements-dev.txt` | Comma-separated requirements files |

#### file_size_guard.yml

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `file_size_limit_mb` | string | `50` | Maximum file size in MB |
| `check_draft_prs` | boolean | `false` | Whether to check draft PRs |

#### qa_aegis.yml

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `project_name` | string | `Aegis` | Project name for QA reporting |
| `python_version` | string | `3.11` | Python version to use |
| `test_path` | string | `tests/aegis_langgraph` | Path to test files |
| `requirements_files` | string | `requirements.txt,requirements-dev.txt,requirements-langgraph.txt` | Comma-separated requirements files |

#### qa_e2e.yml

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `project_name` | string | `Dashboard` | Project name for QA reporting |
| `python_version` | string | `3.11` | Python version to use |
| `requirements_files` | string | `requirements.txt,requirements-dev.txt` | Comma-separated requirements files |
| `e2e_script_path` | string | `scripts/qa_dashboard_e2e.py` | Path to E2E test script |

## Requirements

- Python 3.11+
- GitHub Actions runner (ubuntu-latest recommended)
- For `uv` workflows: Astral uv setup action

## Project Structure

```
ci-cd-kit/
├── pyproject.toml          # Package configuration
├── README.md               # This documentation
└── workflows/              # GitHub Actions workflows
    ├── coverage.yml        # General coverage gate
    ├── coverage_python.yml # Python-specific coverage
    ├── file_size_guard.yml # File size enforcement
    ├── import_linter.yml   # Import boundary checking
    ├── legacy_imports.yml  # Legacy import detection
    ├── qa_aegis.yml        # QA test ingestion
    └── qa_e2e.yml          # E2E testing
```

## License

MIT License - See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test workflows in a fork
5. Submit a pull request

## Related Projects

- [ResilienceKit](https://github.com/KooshaPari/ResilienceKit) - Python resilience patterns and utilities
