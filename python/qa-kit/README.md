# QA Kit

Comprehensive QA testing and reporting framework for standalone use. Originally extracted from phenoSDK, now maintained as an independent package.

## Features

- **Multi-Framework Test Ingestion**: Import results from pytest, Jest, Vitest, Playwright, and more
- **SQLite-Based Storage**: Local, fast, and portable database for test results
- **Accessibility Testing**: Ingest Axe accessibility audit results
- **Performance Testing**: Ingest Lighthouse CI performance reports
- **Database Merging**: Consolidate multiple test runs from CI artifacts
- **E2E Testing**: Automated Playwright-based testing for QA dashboards

## Installation

```bash
# Basic installation ( SQLite only )
pip install -e .

# With optional dependencies
pip install -e ".[core]"        # pytest and testing tools
pip install -e ".[e2e]"         # Playwright for E2E testing
pip install -e ".[api]"         # FastAPI/HTTP client tools
pip install -e ".[all]"         # All dependencies
```

## Quick Start

### 1. Ingest Test Results

The primary workflow is ingesting test results from various frameworks into a local SQLite database:

```bash
# Pytest (JUnit XML format)
pytest --junitxml=reports/pytest-junit.xml
qa-ingest \
  --project my-project \
  --framework pytest \
  --input reports/pytest-junit.xml \
  --format junit \
  --commit $(git rev-parse HEAD) \
  --branch $(git branch --show-current) \
  --ci github

# Jest (JUnit format)
jest --reporters=default --reporters=jest-junit
qa-ingest \
  --project frontend-app \
  --framework jest \
  --input reports/junit.xml \
  --format junit

# Jest (JSON format)
jest --json --outputFile=reports/jest.json
qa-ingest \
  --project frontend-app \
  --framework jest \
  --input reports/jest.json \
  --format jest-json

# Vitest
vitest --reporter=junit --outputFile=reports/vitest-junit.xml
qa-ingest \
  --project frontend-admin \
  --framework vitest \
  --input reports/vitest-junit.xml \
  --format junit

# Playwright
qa-ingest \
  --project e2e-tests \
  --framework playwright \
  --input reports/playwright-results.json \
  --format playwright-json
```

### 2. Ingest Accessibility Results (Axe)

```bash
# Run axe-core and ingest results
axe --reporter json https://example.com > reports/axe.json
qa-ingest-axe \
  --project my-project \
  --db qa_data/qa.db \
  --input reports/axe.json
```

### 3. Ingest Lighthouse CI Results

```bash
# After running LHCI
qa-ingest-lhci \
  --project my-project \
  --db qa_data/qa.db \
  --input .lighthouseci/*.json
```

### 4. Merge Multiple Databases

When running tests in parallel CI jobs, merge results into a single database:

```bash
# Merge all CI artifact DBs
qa-merge-db \
  --output merged-qa.db \
  --inputs artifacts/*.db

# Or seed from a directory
qa-seed-from-dir \
  --seed-dir /mnt/qa-artifacts \
  --dest-db qa_data/qa.db
```

## CLI Reference

### `qa-ingest`

Ingest test results from multiple frameworks into the QA database.

```bash
qa-ingest \
  --project <name> \              # Required: Project identifier
  --framework <name> \             # Required: Framework name (pytest, jest, vitest, etc.)
  --input <path> [path...] \       # Required: Input file(s)
  --format <format> \              # Input format (auto, junit, jest-json, vitest-json, playwright-json)
  [--db <path>] \                  # Database path (default: qa_data/qa.db)
  [--commit <sha>] \               # Git commit SHA
  [--branch <name>] \              # Git branch name
  [--ci <provider>] \              # CI provider (github, gitlab, jenkins, local)
  [--triggered-by <user>] \        # Who triggered the test run
  [--coverage-json <path>] \       # Path to coverage summary JSON
  [--coverage-xml <path>] \        # Path to Cobertura XML coverage
  [--meta <json>]                  # Additional metadata as JSON string
```

**Environment Variables:**
- `QA_DB_PATH`: Default database path
- `QA_PROJECT_ALIASES`: JSON mapping to canonicalize project names

### `qa-ingest-axe`

Ingest Axe accessibility audit results.

```bash
qa-ingest-axe \
  --project <name> \               # Required: Project name
  --db <path> \                    # Required: Database path
  --input <path> [path...]         # Required: Axe JSON files
```

### `qa-ingest-lhci`

Ingest Lighthouse CI performance reports.

```bash
qa-ingest-lhci \
  --project <name> \               # Required: Project name
  --db <path> \                    # Required: Database path
  --input <path> [path...]         # Required: LHCI JSON files
```

### `qa-merge-db`

Merge multiple QA databases into one.

```bash
qa-merge-db \
  --output <path> \                # Required: Output database path
  --inputs <path> [path...]        # Required: Input database paths
```

### `qa-seed-from-dir`

Seed a QA database by merging all `.db` files from a directory.

```bash
qa-seed-from-dir \
  --seed-dir <path> \              # Required: Directory with .db files
  [--dest-db <path>]               # Destination DB (default: qa_data/qa.db or $QA_DB_PATH)
```

### `qa-dashboard-e2e`

Run E2E tests against the QA dashboard using Playwright.

```bash
qa-dashboard-e2e
```

**Note:** Requires Playwright to be installed (`pip install playwright`).

## Database Schema

The SQLite database uses the following schema:

### Tables

#### `projects`
- `id`: INTEGER PRIMARY KEY
- `name`: TEXT UNIQUE NOT NULL

#### `runs`
- `id`: INTEGER PRIMARY KEY
- `project_id`: INTEGER (FK to projects)
- `framework`: TEXT NOT NULL
- `commit_sha`: TEXT
- `branch`: TEXT
- `ci_provider`: TEXT
- `triggered_by`: TEXT
- `created_at`: TEXT NOT NULL
- `started_at`: TEXT
- `duration_ms`: INTEGER
- `total`, `passed`, `failed`, `skipped`, `errors`: INTEGER counts
- `coverage_lines`, `coverage_branches`: REAL percentages
- `meta_json`: TEXT (JSON metadata)

#### `test_cases`
- `id`: INTEGER PRIMARY KEY
- `run_id`: INTEGER (FK to runs)
- `file`: TEXT (test file path)
- `suite`: TEXT (test suite name)
- `name`: TEXT (test case name)
- `status`: TEXT (passed, failed, skipped, error)
- `duration_ms`: INTEGER
- `error_message`: TEXT
- `retry_count`: INTEGER
- `extra_json`: TEXT (additional metadata)

#### `axe_runs` (accessibility)
- `id`: INTEGER PRIMARY KEY
- `project_id`: INTEGER (FK to projects)
- `created_at`: TEXT
- `url`: TEXT
- `critical`, `serious`, `moderate`, `minor`: INTEGER counts
- `raw_json`: TEXT

#### `lh_runs` (Lighthouse CI)
- `id`: INTEGER PRIMARY KEY
- `project_id`: INTEGER (FK to projects)
- `url`: TEXT
- `created_at`: TEXT
- `perf`, `a11y`, `bp`, `seo`, `pwa`: REAL scores (0-100)
- `raw_json`: TEXT

## Usage Examples

### CI/CD Integration (GitHub Actions)

```yaml
# .github/workflows/test.yml
name: Test and Report

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install qa-kit
        run: pip install "git+https://github.com/yourorg/TestingKit.git#subdirectory=python/qa-kit"
      
      - name: Run tests
        run: pytest --junitxml=reports/pytest.xml
      
      - name: Ingest results
        run: |
          qa-ingest \
            --project ${{ github.repository }} \
            --framework pytest \
            --input reports/pytest.xml \
            --format junit \
            --commit ${{ github.sha }} \
            --branch ${{ github.ref_name }} \
            --ci github \
            --triggered-by ${{ github.actor }}
      
      - name: Upload QA database
        uses: actions/upload-artifact@v4
        with:
          name: qa-db
          path: qa_data/qa.db
```

### Merge CI Artifacts

```yaml
# .github/workflows/merge-reports.yml
name: Merge QA Reports

on:
  workflow_run:
    workflows: ["Test and Report"]
    types: [completed]

jobs:
  merge:
    runs-on: ubuntu-latest
    steps:
      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts
          pattern: qa-db-*
          merge-multiple: true
      
      - name: Install qa-kit
        run: pip install "git+https://github.com/yourorg/TestingKit.git#subdirectory=python/qa-kit"
      
      - name: Merge databases
        run: |
          qa-seed-from-dir \
            --seed-dir artifacts \
            --dest-db qa_data/qa.db
      
      - name: Upload merged database
        uses: actions/upload-artifact@v4
        with:
          name: qa-db-merged
          path: qa_data/qa.db
```

### Querying Results (Python)

```python
import sqlite3

# Connect to the QA database
conn = sqlite3.connect("qa_data/qa.db")
conn.row_factory = sqlite3.Row

# Get recent test runs
cursor = conn.execute("""
    SELECT r.*, p.name as project_name
    FROM runs r
    JOIN projects p ON r.project_id = p.id
    WHERE p.name = 'my-project'
    ORDER BY r.created_at DESC
    LIMIT 10
""")
runs = cursor.fetchall()

# Get failure summary
cursor = conn.execute("""
    SELECT tc.file, tc.name, tc.error_message
    FROM test_cases tc
    JOIN runs r ON tc.run_id = r.id
    WHERE tc.status = 'failed'
    AND r.created_at > date('now', '-7 days')
    ORDER BY r.created_at DESC
""")
failures = cursor.fetchall()

# Get accessibility trends
cursor = conn.execute("""
    SELECT created_at, critical, serious, moderate, minor
    FROM axe_runs
    ORDER BY created_at DESC
    LIMIT 30
""")
a11y_trends = cursor.fetchall()

conn.close()
```

## Project Structure

```
qa-kit/
├── pyproject.toml           # Package configuration
├── README.md                # This file
├── qa_kit_logging.py        # Standalone logging utility
└── scripts/
    ├── ingest.py            # Main test result ingestion
    ├── ingest_axe.py        # Axe accessibility ingestion
    ├── ingest_lhci.py       # Lighthouse CI ingestion
    ├── merge_db.py          # Database merging utility
    ├── seed_from_dir.py     # Directory-based seeding
    └── dashboard_e2e.py     # E2E testing with Playwright
```

## Migration from phenoSDK

If you were previously using qa-kit from phenoSDK:

1. **Update imports**: The logging module is now standalone (`qa_kit_logging.py`)
2. **CLI commands**: All scripts are now registered as console scripts:
   - `qa-ingest` (was `scripts/qa_ingest.py`)
   - `qa-ingest-axe` (was `scripts/qa_ingest_axe.py`)
   - `qa-ingest-lhci` (was `scripts/qa_ingest_lhci.py`)
   - `qa-merge-db` (was `scripts/qa_merge_db.py`)
   - `qa-seed-from-dir` (was `scripts/qa_seed_from_dir.py`)
   - `qa-dashboard-e2e` (was `scripts/qa_dashboard_e2e.py`)

3. **Database path**: Default location is still `qa_data/qa.db`

## Development

```bash
# Clone the repository
git clone https://github.com/yourorg/TestingKit.git
cd TestingKit/python/qa-kit

# Install in editable mode
pip install -e ".[all]"

# Run linting
ruff check scripts/

# Format code
ruff format scripts/

# Type checking
mypy scripts/
```

## License

Proprietary - PHENO-SDK Team

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and questions:
- Open an issue on GitHub
- Contact the PHENO-SDK Team
