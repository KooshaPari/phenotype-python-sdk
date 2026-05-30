# Pheno Testing CLI

Comprehensive testing toolkit for Python projects - extracted from PhenoSDK and formalized as standalone CLI tools.

## Installation

```bash
pip install pheno-testing-cli
```

Or install from source:

```bash
cd TestingKit/python/pheno-testing-cli
pip install -e .
```

## CLI Commands

### 1. Security Testing

Run comprehensive security tests including DAST (Dynamic Application Security Testing), penetration testing, and compliance checks.

```bash
# Normal security scan
pheno-test security . --scan-depth normal

# Deep security scan (includes penetration testing)
pheno-test security . --scan-depth deep

# Output JSON report
pheno-test security . --scan-depth deep --json --output security-report.json

# Scan specific base URL
pheno-test security . --base-url http://localhost:3000 --scan-depth deep
```

**Features:**
- SQL injection detection
- XSS vulnerability scanning
- Command injection testing
- Path traversal detection
- LDAP injection testing
- Authentication weakness checks
- Session fixation detection
- Brute force protection validation
- SSL/TLS configuration testing
- OWASP Top 10 compliance checks
- GDPR compliance validation
- NIST cybersecurity framework checks

### 2. Performance Testing

Run load tests, stress tests, and performance benchmarks.

```bash
# Comprehensive performance tests
pheno-test performance .

# Run specific load test
pheno-test performance . --load-test heavy_load

# Run stress test
pheno-test performance . --stress-test

# Run memory leak test
pheno-test performance . --memory-test

# Run CPU intensive test
pheno-test performance . --cpu-test

# Output benchmark report
pheno-test performance . --benchmark --json --output perf-report.json
```

**Test Types:**
- Light Load: 10 concurrent users, 60s duration
- Medium Load: 50 concurrent users, 120s duration
- Heavy Load: 100 concurrent users, 180s duration
- Stress Test: Up to 200 workers, resource exhaustion scenarios
- Memory Leak Detection: 50MB threshold monitoring
- CPU Intensive: Mathematical computation benchmarking

**Metrics Captured:**
- Response time (avg, min, max, p50, p95, p99)
- Throughput (requests/second)
- Error rate
- Memory usage (RSS, VMS)
- CPU utilization
- Thread count
- Open file descriptors

### 3. Generate Test Data

Generate comprehensive test scenarios for better coverage.

```bash
# Generate all scenario types (default: 10 scenarios each)
pheno-test generate .

# Generate specific number of scenarios
pheno-test generate . --scenarios 50

# Generate only database scenarios
pheno-test generate . --type database --scenarios 20

# Generate only API scenarios
pheno-test generate . --type api --scenarios 30

# Generate security test scenarios
pheno-test generate . --type security --scenarios 100

# Generate performance test scenarios
pheno-test generate . --type performance --scenarios 25

# Custom output directory
pheno-test generate . --output-dir my_test_data --scenarios 50
```

**Generated Scenarios:**

**Database Scenarios:**
- Connection pool exhaustion
- Connection timeout handling
- Concurrent transaction conflicts
- Long-running transaction recovery
- Large dataset operations (1M+ records)
- Data inconsistency recovery

**API Scenarios:**
- Token lifetime management
- Concurrent token requests (1000+)
- Burst traffic patterns
- Maximum payload validation (10MB)
- Malformed payload handling

**Security Scenarios:**
- SQL injection resistance testing
- XSS vector testing
- Credential stuffing detection
- Privilege escalation prevention
- Input validation testing

**Performance Scenarios:**
- Sustained high load (10K concurrent users)
- Instantaneous traffic spikes (1K to 50K RPS)
- Diurnal traffic patterns
- Burst patterns

**Edge Cases:**
- Null/empty value patterns
- System resource exhaustion
- Leap second handling
- Extreme value validation

### 4. Enhance Test Files

Enhance existing test files with better coverage and infrastructure.

```bash
# Enhance a specific test file
pheno-test enhance tests/test_example.py

# Generate test templates
pheno-test enhance tests/test_example.py --templates

# Enhance testing infrastructure
pheno-test enhance tests/test_example.py --infrastructure

# Full enhancement with output directory
pheno-test enhance tests/test_example.py --templates --infrastructure --output enhanced/
```

**Enhancements Applied:**
- Test suite structure optimization
- Pytest markers and configuration
- Test templates generation (unit, integration, performance)
- Test fixtures and utilities
- Performance testing framework setup
- Test data management
- Test reporting infrastructure
- Test automation scripts

### 5. Parallel Test Execution

Run tests in parallel for faster feedback (up to 4x speedup).

```bash
# Run all tests in parallel with 4 workers (default)
pheno-test parallel .

# Run with specific worker count
pheno-test parallel . --workers 8

# Run specific test tiers
pheno-test parallel . --tiers unit_tier api_tier

# Run benchmark comparison
pheno-test parallel . --benchmark

# Output results to file
pheno-test parallel . --workers 8 --output parallel-results.json
```

**Test Tiers:**
- `database_tier`: Database integration, service layer, data access tests
- `api_tier`: API endpoints, auth service, business logic tests
- `external_tier`: External services, API client, payment gateway tests
- `unit_tier`: Unit tests, utility tests, validation tests
- `e2e_tier`: End-to-end tests, user flows, admin dashboard tests

**Performance Targets:**
- Sequential execution: ~8.5 minutes
- Parallel execution: ~2.1 minutes (4x speedup)
- CPU utilization: 80%+
- Memory efficiency: 70%+

## Python API Usage

You can also use the testing modules programmatically:

```python
from pheno_testing_cli.security_testing import DynamicApplicationSecurityTester

# Create DAST tester
tester = DynamicApplicationSecurityTester(base_url="http://localhost:8000")

# Run DAST scan
endpoints = ["/", "/api/users", "/api/data"]
result = tester.run_dast_scan(endpoints)

print(f"Risk Score: {result.risk_score}")
print(f"Vulnerabilities: {len(result.vulnerabilities)}")
```

```python
from pheno_testing_cli.performance_testing import PerformanceTestingFramework

# Create performance framework
framework = PerformanceTestingFramework("/path/to/project")

# Run comprehensive tests
report = framework.run_comprehensive_tests()

print(f"Score: {report['summary']['score']}/100")
print(f"Tests: {report['summary']['total_tests']}")
```

```python
from pheno_testing_cli.test_data_generator import TestDataEnhancementSystem

# Create test data system
system = TestDataEnhancementSystem("/path/to/project")

# Generate scenarios
scenarios = system.generate_test_data_scenarios()

# Get templates
templates = system.create_test_data_templates()
```

## Configuration

### pyproject.toml Settings

```toml
[tool.pheno-testing]
# Security settings
security_base_url = "http://localhost:8000"
security_scan_depth = "normal"

# Performance settings
performance_load_config = "medium_load"
performance_duration = 120

# Parallel execution settings
parallel_workers = 4
parallel_tiers = ["unit_tier", "api_tier"]

# Test data generation
generate_scenarios = 50
generate_types = ["database", "api", "security"]
```

### Environment Variables

```bash
# Security testing
export PHENO_SECURITY_BASE_URL=http://localhost:8000
export PHENO_SECURITY_SCAN_DEPTH=deep

# Performance testing
export PHENO_PERF_LOAD_CONFIG=heavy_load
export PHENO_PERF_DURATION=180

# Parallel execution
export PHENO_PARALLEL_WORKERS=8
```

## Output Formats

### JSON Output

All commands support `--json` flag for machine-readable output:

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "summary": {
    "total_tests": 10,
    "passed": 8,
    "failed": 1,
    "warnings": 1,
    "score": 85.0
  },
  "results": [...],
  "recommendations": [...]
}
```

### Markdown Reports

Reports are automatically generated in `reports/` directory:
- `security_report_{timestamp}.md`
- `performance_report_{timestamp}.md`
- `test_automation_report_{timestamp}.md`

## CI/CD Integration

### GitHub Actions

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install pheno-testing-cli
      - run: pheno-test security . --scan-depth deep --json --output security.json
      
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install pheno-testing-cli
      - run: pheno-test performance . --benchmark --json --output perf.json
      
  parallel:
    runs-on: ubuntu-latest-8-cores
    steps:
      - uses: actions/checkout@v4
      - run: pip install pheno-testing-cli
      - run: pheno-test parallel . --workers 8
```

## Dependencies

**Required:**
- Python >= 3.10
- requests >= 2.28.0
- numpy >= 1.24.0
- psutil >= 5.9.0

**Optional (for development):**
- pytest >= 7.0.0
- pytest-benchmark >= 4.0.0
- pytest-xdist >= 3.0.0
- ruff >= 0.1.0
- mypy >= 1.5.0
- faker >= 19.0.0

## Project Structure

```
pheno-testing-cli/
├── src/
│   └── pheno_testing_cli/
│       ├── __init__.py
│       ├── cli.py                    # Main CLI entry point
│       ├── security_testing.py       # DAST, penetration, compliance
│       ├── performance_testing.py    # Load, stress, benchmark
│       ├── test_data_generator.py    # Test scenario generation
│       ├── test_enhancer.py          # Test file enhancement
│       ├── parallel_runner.py        # Parallel test execution
│       ├── perf_framework.py         # Performance framework
│       ├── automation_suite.py       # Test automation
│       ├── doc_tester.py             # Documentation testing
│       ├── duration_tracker.py       # Test duration tracking
│       └── package_tester.py         # Package validation
├── pyproject.toml
└── README.md
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please follow the existing code style and add tests for new features.

## Acknowledgments

This package was extracted from the PhenoSDK testing infrastructure to provide standalone testing capabilities for Python projects.
