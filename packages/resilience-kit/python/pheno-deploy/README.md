# Pheno-Deploy

Unified deployment CLI for Phenotype projects. Extracted from phenoSDK as a standalone tool.

## Overview

Pheno-Deploy provides a comprehensive set of deployment automation commands for building, releasing, and managing Phenotype projects. It consolidates functionality from multiple deployment scripts into a unified, easy-to-use CLI.

## Installation

```bash
pip install pheno-deploy
```

Or install from source:

```bash
cd /Users/kooshapari/CodeProjects/Phenotype/repos/ResilienceKit/python/pheno-deploy
pip install -e .
```

## Quick Start

```bash
# Check deployment readiness
pheno-deploy check --format text

# Build the project
pheno-deploy build --target local

# Create a release
pheno-deploy release patch --dry-run

# Validate a package
pheno-deploy validate ./dist/my-package.whl
```

## Commands

### `build` - Build Package

Build package and optionally publish.

```bash
pheno-deploy build [config] --target [local|staging|prod]
```

Options:
- `--target, -t`: Deployment target (default: local)
- `--skip-tests`: Skip running tests
- `--skip-install-test`: Skip fresh venv install test
- `--dry-run`: Build without publishing
- `--verbose, -v`: Enable verbose output

### `release` - Create Release

Create a new release with semantic versioning.

```bash
pheno-deploy release [version] --notes [file] --dry-run
```

Arguments:
- `version`: Version to release (major, minor, patch, or custom version like "1.2.3")

Options:
- `--notes, -n`: Path to release notes file
- `--dry-run`: Simulate release without making changes
- `--prerelease`: Mark as prerelease
- `--project, -p`: Project root directory

Examples:
```bash
pheno-deploy release patch              # Bump patch version
pheno-deploy release minor --dry-run    # Simulate minor release
pheno-deploy release 1.5.0 --prerelease # Create 1.5.0-rc.1
```

### `check` - Run Deployment Checks

Run deployment readiness checks.

```bash
pheno-deploy check [environment] --health --schema --config
```

Arguments:
- `environment`: Environment to check (default: local)

Options:
- `--health/--no-health`: Run health checks (default: True)
- `--schema`: Check schema consistency
- `--config`: Validate configuration files
- `--format, -f`: Output format (text, json, markdown)
- `--output, -o`: Write report to file
- `--project, -p`: Project directory

### `schema-drift` - Check Schema Drift

Check for schema drift between environments.

```bash
pheno-deploy schema-drift [db-url] --baseline [file] --report
```

Options:
- `--baseline, -b`: Path to baseline schema file
- `--report, -r`: Write drift report to file
- `--offline`: Skip remote connection, use local only
- `--json`: Output in JSON format

### `rollback` - Rollback Version

Rollback to a previous version.

```bash
pheno-deploy rollback [version] --confirm
```

Arguments:
- `version`: Version to rollback to

Options:
- `--confirm, -y`: Skip confirmation prompt
- `--dry-run`: Show what would be done without executing
- `--project, -p`: Project root directory

### `validate` - Validate Package

Validate a package before deployment.

```bash
pheno-deploy validate [package] --requirements --security
```

Arguments:
- `package`: Package to validate (wheel or source directory)

Options:
- `--requirements/--no-requirements`: Validate requirements (default: True)
- `--security`: Run security scans
- `--metadata/--no-metadata`: Validate package metadata (default: True)

### `promote` - Promote Deployment

Promote deployment from one environment to another.

```bash
pheno-deploy promote [from] [to] --tests
```

Arguments:
- `from`: Source environment (e.g., staging)
- `to`: Target environment (e.g., prod)

Options:
- `--tests/--no-tests`: Run tests before promotion (default: True)
- `--dry-run`: Simulate promotion without deploying

### `artifacts` - Manage Artifacts

Manage build artifacts.

```bash
pheno-deploy artifacts [action] --older-than [days]
```

Arguments:
- `action`: Action to perform (list, clean, archive)

Options:
- `--older-than`: Filter artifacts older than N days
- `--keep-minimum`: Minimum artifacts to keep when cleaning (default: 5)
- `--dry-run`: Show what would be done without executing

Examples:
```bash
pheno-deploy artifacts list                    # List all artifacts
pheno-deploy artifacts clean --older-than 7    # Clean artifacts older than 7 days
pheno-deploy artifacts clean --keep-minimum 3  # Keep only 3 most recent artifacts
```

## Deployment Checks

The `check` command runs the following checks:

| Check | Priority | Description |
|-------|----------|-------------|
| git_clean | CRITICAL | Git working directory is clean |
| pyproject_valid | CRITICAL | pyproject.toml has required fields |
| tests_exist | HIGH | Tests directory exists |
| readme_exists | MEDIUM | README file exists |
| changelog_exists | MEDIUM | CHANGELOG.md exists |
| license_exists | LOW | LICENSE file exists |
| no_large_files | MEDIUM | No files larger than 10MB |
| python_version | HIGH | Python version is supported |

## Release Process

The `release` command performs the following steps:

1. **Validate environment**: Check git status, branch, and clean working directory
2. **Get current version**: Read from pyproject.toml
3. **Calculate new version**: Based on release type (major/minor/patch)
4. **Update version files**: Update pyproject.toml and __init__.py
5. **Generate changelog**: Categorize commits since last tag
6. **Generate release notes**: Create formatted release notes
7. **Run tests**: Execute pytest suite
8. **Build artifacts**: Create wheel distribution
9. **Create git tag**: Tag the release
10. **Push changes**: Push to remote repository

## Configuration

Pheno-Deploy uses sensible defaults but can be configured through:

1. Command-line options
2. Environment variables
3. Project structure (pyproject.toml, CHANGELOG.md, etc.)

### Environment Variables

- `PHENO_DEPLOY_DRY_RUN`: Set to `1` or `true` to enable dry-run mode by default
- `PHENO_DEPLOY_TARGET`: Default deployment target

## Integration with CI/CD

### GitHub Actions

```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pheno-deploy
      - run: pheno-deploy check --format json
      - run: pheno-deploy build --target staging
```

### GitLab CI

```yaml
deploy:
  stage: deploy
  image: python:3.11
  script:
    - pip install pheno-deploy
    - pheno-deploy check
    - pheno-deploy build --target production
```

## Source Files

This tool was extracted from:
- `phenoSDK/tools/deployment/` - Original Typer-based CLI scripts
- `phenoSDK/scripts/` - Original argparse-based scripts

Original files preserved for reference:
- `build_and_release.py` (tools and scripts versions)
- `check_deployment.py` (tools and scripts versions)
- `check_schema_drift.py` (tools and scripts versions)
- `release_automation.py` (tools and scripts versions)

## Differences from Original

1. **Standalone**: No dependency on `pheno.*` internal modules
2. **Unified CLI**: Single entry point with subcommands
3. **Rich output**: Uses Rich for beautiful terminal output
4. **Type hints**: Full type annotation coverage
5. **Simplified**: Removed phenoSDK-specific dependencies

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
mypy src/pheno_deploy

# Format code
ruff format .
```

## License

MIT License - See LICENSE file for details.

## See Also

- [ResilienceKit](../../README.md) - Parent project
- [phenoSDK](../../../phenoSDK/README.md) - Source project
