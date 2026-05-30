# Pheno Quality CLI Tests

## Running Tests

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=pheno_quality

# Run specific test file
pytest tests/test_quality.py

# Run with verbose output
pytest -v
```

## Test Structure

- `test_quality.py`: Core quality framework tests
- `test_cli.py`: CLI-specific tests (to be added)

## Test Categories

1. **Core Classes**: Test QualityIssue, QualityMetrics, QualityConfig, QualityReport
2. **Configuration**: Test config presets and custom configs
3. **Manager**: Test QualityAnalysisManager functionality
4. **CLI**: Test CLI entry points
5. **Exporters**: Test export functionality
6. **Importers**: Test import functionality
