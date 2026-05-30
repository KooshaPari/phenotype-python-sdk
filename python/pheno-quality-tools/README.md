# Pheno Quality Tools

Comprehensive quality analysis framework for Python projects, extracted from phenoSDK.

## Overview

Pheno Quality Tools provides a comprehensive suite of quality analysis tools for Python projects:

- **Pattern Detection**: Detect code patterns and anti-patterns (God Object, Feature Envy, Data Clump, etc.)
- **Architectural Validation**: Validate architectural patterns (Hexagonal, Clean Architecture, SOLID)
- **Performance Detection**: Find performance issues (N+1 queries, memory leaks, blocking calls)
- **Security Scanning**: Scan for security vulnerabilities
- **Code Smell Detection**: Detect code smells (long methods, large classes, duplicate code)
- **Integration Gates**: Validate integration quality
- **Atlas Health**: Project health analysis

## Installation

```bash
# From source
pip install -e /path/to/TestingKit/python/pheno-quality-tools

# Or with development dependencies
pip install -e ".[dev]"
```

## Quick Start

### CLI Usage

```bash
# Check current directory
pheno-quality-gates check .

# Check with specific tools
pheno-quality-gates check src/ --tools pattern_detector security_scanner

# Validate quality gates
pheno-quality-gates validate --run-analysis

# Atlas health check
pheno-quality-gates atlas .

# Export report to different format
pheno-quality-gates export --input report.json --format html --output report.html

# List available tools
pheno-quality-gates list tools
```

### Python API

```python
from pheno_quality_tools import quality_manager

# Analyze a project
report = quality_manager.analyze_project("./src")
print(f"Quality Score: {report.metrics.quality_score:.1f}/100")
print(f"Total Issues: {report.metrics.total_issues}")

# Generate summary
summary = quality_manager.generate_summary(report)
print(f"Status: {summary['quality_status']}")

# Export report
quality_manager.export_report(report, "report.html", "html")
```

## Configuration Presets

Available configuration presets:

- `default`: General purpose configuration
- `strict`: High quality standards (90+ score threshold)
- `lenient`: Relaxed standards for legacy codebases
- `pheno-sdk`: Configuration optimized for SDK projects
- `zen-mcp`: Configuration for MCP servers
- `atoms-mcp`: Configuration for Atoms MCP

```python
from pheno_quality_tools import get_config

config = get_config("strict")
quality_manager.config = config
```

## Available Tools

| Tool | Description |
|------|-------------|
| `pattern_detector` | Detect code patterns and anti-patterns |
| `architectural_validator` | Validate architectural patterns |
| `performance_detector` | Detect performance issues |
| `security_scanner` | Scan for security vulnerabilities |
| `code_smell_detector` | Detect code smells |
| `integration_gates` | Validate integration quality |
| `atlas_health` | Project health analysis |

## Architecture

```
pheno_quality_tools/
├── core.py              # Base classes and data structures
├── manager.py           # QualityManager - main entry point
├── cli.py               # CLI implementation
├── config.py            # Configuration presets
├── registry.py          # Tool registry
├── plugins.py           # Plugin system
├── utils.py             # Utility functions
├── exporters.py         # Report exporters (JSON, HTML, CSV, etc.)
├── importers.py         # Report importers
├── integration.py       # Framework integration utilities
├── export_import.py     # Export/import functionality
├── pattern_detector.py  # Pattern detection tool
├── architectural_validator.py
├── performance_detector.py
├── security_scanner.py
├── code_smell_detector.py
├── integration_gates.py
└── atlas_health.py
```

## Report Formats

Export reports to multiple formats:

- **JSON**: Full structured data
- **HTML**: Rich visual report
- **Markdown**: GitHub-friendly format
- **CSV**: Spreadsheet compatible
- **XML**: CI/CD integration

## Integration

### Makefile Integration

```makefile
.PHONY: quality quality-report

quality:
    pheno-quality-gates check . --summary

quality-report:
    pheno-quality-gates check . --output reports/quality.json
```

### CI/CD Integration

```yaml
# .github/workflows/quality.yml
- name: Run Quality Checks
  run: |
    pip install pheno-quality-tools
    pheno-quality-gates validate --run-analysis --quality-threshold 80
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .

# Run type checking
mypy src/pheno_quality_tools
```

## License

MIT License - See repository for details.

## Attribution

Extracted from phenoSDK/tools/quality/ and formalized as standalone CLI tools.
