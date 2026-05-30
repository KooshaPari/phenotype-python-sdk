# Pheno Analysis CLI

A unified code analysis suite for Python projects, extracted from phenoSDK and formalized as standalone CLI tools.

## Installation

```bash
# Install from source
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Usage

```bash
# Get help
pheno-analyze --help

# Analyze code complexity
pheno-analyze complexity src/
pheno-analyze complexity src/ --report
pheno-analyze complexity src/ --json

# Analyze git churn
pheno-analyze churn .
pheno-analyze churn . --days 30
pheno-analyze churn . --days 7 --json

# Analyze code duplication
pheno-analyze duplication src/
pheno-analyze duplication src/ --report

# Analyze dependencies
pheno-analyze dependencies .
pheno-analyze dependencies . --report

# Run coverage analysis
pheno-analyze coverage .
pheno-analyze coverage . --report
pheno-analyze coverage . --gaps  # Analyze coverage gaps (mock)

# Detect patterns and anti-patterns
pheno-analyze patterns src/
pheno-analyze patterns src/ --json
pheno-analyze patterns src/ --severity high
pheno-analyze patterns src/ --category architectural

# Detect code smells
pheno-analyze smells src/
pheno-analyze smells src/ --json
pheno-analyze smells src/ --severity high
```

## Commands

### `complexity`

Analyzes code complexity using multiple metrics:
- **Cyclomatic Complexity**: Measures the number of linearly independent paths
- **Maintainability Index**: Assesses how maintainable the code is
- **Halstead Complexity**: Measures computational difficulty

Requires: `radon`

```bash
pip install radon
```

### `churn`

Analyzes git commit history to identify:
- Files with frequent changes
- Top contributors
- Lines added/deleted statistics

No external dependencies required.

### `duplication`

Detects code duplication using:
- Pylint duplicate code detection
- Similar block analysis
- Refactoring recommendations

Requires: `pylint`

```bash
pip install pylint
```

### `dependencies`

Analyzes project dependencies:
- Total package count
- Direct vs transitive dependencies
- Outdated packages
- Dependency conflicts
- Circular dependencies

Requires: `pipdeptree`, optionally `pydeps`

```bash
pip install pipdeptree pydeps
```

### `coverage`

Runs test coverage analysis:
- pytest with coverage reporting
- HTML/XML/JSON report generation
- Coverage gap analysis (optional mock mode)

Requires: `pytest`, `pytest-cov`

```bash
pip install pytest pytest-cov
```

### `patterns`

Detects architectural patterns and anti-patterns:
- Anti-patterns (long functions, too many parameters)
- Vibe-patterns (import style, magic strings)
- Code smells (feature envy, god classes)
- Architectural violations (layer violations, SOLID principles)

No external dependencies required.

### `smells`

Comprehensive code smell detection:
- Long methods/classes
- Duplicate code
- Dead code
- Magic numbers
- Deep nesting
- God objects
- Feature envy
- And many more...

No external dependencies required.

## Programmatic Usage

All analysis modules can be imported and used programmatically:

```python
from pheno_analysis_cli import analyze_complexity, code_smell_detector

# Complexity analysis
results = analyze_complexity.run_complexity_analysis()
print(f"Overall Score: {results['overall_complexity_score']['score']}/100")

# Code smell detection
detector = code_smell_detector.CodeSmellDetector()
detector.analyze_file(Path("src/myfile.py"))
report = detector.generate_report()
print(f"Total smells: {report['summary']['total_smells']}")
```

## Analysis Modules

The following analysis modules are included:

| Module | Purpose | Standalone |
|--------|---------|------------|
| `analyze_complexity.py` | Cyclomatic, maintainability, Halstead metrics | Yes |
| `analyze_churn.py` | Git churn analysis | Yes |
| `analyze_duplication.py` | Code duplication detection | Yes |
| `analyze_dependencies.py` | Dependency analysis | Yes |
| `coverage_analysis.py` | pytest coverage runner | Yes |
| `analyze_test_coverage.py` | Test coverage gap analysis (mock) | Yes |
| `analyze_quality_coverage.py` | Quality tooling coverage | Yes |
| `analyze_response_times.py` | API response time measurement | Yes |
| `code_smell_detector.py` | Code smell detection | Yes |
| `advanced_pattern_detector.py` | Advanced pattern detection | Yes |
| `architectural_pattern_validator.py` | Architectural pattern validation | Yes |
| `detect_dead_code.py` | Dead code detection | Yes |

## Requirements

- Python 3.10+
- Optional: radon, pylint, pipdeptree, pydeps, pytest, pytest-cov, vulture

## License

MIT License - See LICENSE file for details.

## Source

Extracted from: `/Users/kooshapari/CodeProjects/Phenotype/repos/phenoSDK/tools/analysis/`
Target: `/Users/kooshapari/CodeProjects/Phenotype/repos/TestingKit/python/pheno-analysis-cli/`
