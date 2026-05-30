# Pheno Quality CLI

A comprehensive code quality analysis CLI tool extracted from phenoSDK.

## Installation

```bash
pip install pheno-quality-cli
```

Or install from source:

```bash
cd TestingKit/python/pheno-quality-cli
pip install -e .
```

## CLI Commands

### pheno-quality-check

Run quality analysis on a path.

```bash
# Basic usage
pheno-quality-check .

# With specific format
pheno-quality-check ./src --format html --output report.html

# With specific tools
pheno-quality-check . --tools pattern_detector,security_scanner

# With configuration preset
pheno-quality-check . --config strict --severity high

# Summary only
pheno-quality-check . --summary
```

### pheno-quality-report

Generate a quality report for a path.

```bash
# Basic usage
pheno-quality-report . --output report.json

# With strict configuration
pheno-quality-report ./src --config strict --output report.html
```

### pheno-quality-export

Export a quality report in different formats.

```bash
# Convert existing report
pheno-quality-export html --input report.json --output report.html

# Direct export
pheno-quality-export csv --output report.csv
```

### pheno-quality-import

Import a quality report from various formats.

```bash
# Import JSON report
pheno-quality-import report.json

# Import CSV report
pheno-quality-import report.csv --format csv

# Import XML report
pheno-quality-import report.xml --format xml
```

## Available Tools

- **pattern_detector**: Detects anti-patterns and design issues
- **architectural_validator**: Validates architectural patterns
- **performance_detector**: Detects performance issues
- **security_scanner**: Scans for security vulnerabilities
- **code_smell_detector**: Detects code smells
- **integration_gates**: Validates integration quality
- **atlas_health**: Analyzes overall code health

## Configuration Presets

- **default**: Default configuration
- **pheno-sdk**: Configuration for pheno-sdk projects
- **zen-mcp**: Configuration for zen-mcp-server projects
- **atoms-mcp**: Configuration for atoms-mcp-old projects
- **strict**: Strict quality thresholds
- **lenient**: Lenient quality thresholds for legacy codebases

## Python API Usage

```python
from pheno_quality import quality_manager, get_config

# Get configuration
config = get_config("pheno-sdk")
quality_manager.config = config

# Analyze a project
report = quality_manager.analyze_project(
    project_path="./src",
    enabled_tools=["pattern_detector", "security_scanner"],
    output_path="./reports/quality_report.json"
)

# Generate summary
summary = quality_manager.generate_summary(report)
print(f"Quality Score: {summary['quality_score']:.1f}/100")
print(f"Total Issues: {summary['total_issues']}")

# Export in different formats
quality_manager.export_report(report, "./reports/quality_report.html")
quality_manager.export_report(report, "./reports/quality_report.csv")
```

## Output Formats

- **JSON**: Machine-readable format
- **HTML**: Human-readable report with styling
- **Markdown**: Documentation-friendly format
- **CSV**: Spreadsheet-compatible format
- **XML**: CI/CD integration format

## Exit Codes

- **0**: Success (quality score >= 70)
- **1**: Quality issues found (quality score < 70)

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src/

# Run type checking
mypy src/
```

## License

MIT
