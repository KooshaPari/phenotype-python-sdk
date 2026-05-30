# TestingKit Specification (SPEC.md)

## Version 1.0.0 | Status: Draft

---

## 1. Document Information

### 1.1 Metadata

| Field | Value |
|-------|-------|
| Document ID | SPEC-TESTINGKIT-001 |
| Version | 1.0.0 |
| Status | Draft |
| Author | Phenotype Architecture Team |
| Created | 2026-04-05 |
| Last Updated | 2026-04-05 |
| Target Release | 1.0.0 |

### 1.2 References

- [SOTA.md](./SOTA.md) - State-of-the-art research
- [ADR.md](./ADR.md) - Architecture decision records
- [README.md](./README.md) - Quick start guide

### 1.3 Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-05 | Architecture Team | Initial specification |

---

## 2. Overview

### 2.1 Purpose

TestingKit is a comprehensive, multi-language testing framework designed for the Phenotype ecosystem. It provides:

- **Language-native testing utilities** for Rust, Python, and Go
- **Cross-language testing patterns** for unified developer experience
- **Code quality analysis** integrated with testing workflows
- **Mocking and test doubles** with language-idiomatic APIs
- **Test fixtures and data generation** for reproducible tests
- **Performance and integration testing** infrastructure

### 2.2 Scope

**In Scope:**
- Unit testing utilities and patterns
- Integration testing infrastructure
- Mocking frameworks
- Test fixtures and builders
- Code quality analysis (code smells, patterns)
- Performance testing support
- CI/CD integration
- Cross-language coordination

**Out of Scope:**
- GUI testing (use dedicated tools like Playwright)
- Mobile testing
- Hardware-in-the-loop testing
- Compliance certification frameworks

### 2.3 Target Users

1. **Phenotype Contributors** - Testing their contributions
2. **Ecosystem Developers** - Building on Phenotype
3. **CI/CD Systems** - Automated testing pipelines
4. **Quality Engineers** - Code quality enforcement

### 2.4 Success Criteria

| Metric | Target |
|--------|--------|
| Test execution speed | <10ms per unit test |
| Mock setup time | <5 lines of code |
| Code smell detection | 90%+ accuracy |
| Documentation coverage | 100% public APIs |
| CI integration time | <2 minutes setup |

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     TestingKit Ecosystem                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │    Rust      │  │   Python     │  │     Go       │           │
│  │   Testing    │  │   Testing    │  │   Testing    │           │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘           │
│         │                 │                 │                    │
│         └─────────────────┼─────────────────┘                    │
│                           │                                      │
│              ┌────────────┴────────────┐                         │
│              │   Shared Patterns Layer   │                         │
│              │  • Test Data Formats     │                         │
│              │  • Result Aggregation    │                         │
│              │  • CI/CD Integration     │                         │
│              └──────────────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Component Architecture

#### 3.2.1 Rust Components

| Component | Purpose | Dependencies | Lines of Code |
|-----------|---------|--------------|---------------|
| phenotype-testing | Core utilities | tokio, tracing, rand | ~500 |
| phenotype-mock | Mocking framework | parking_lot | ~400 |
| phenotype-test-fixtures | Test data | chrono, uuid, serde | ~200 |
| phenotype-test-infra | Integration infra | tokio, tempfile | ~300 |
| phenotype-compliance-scanner | Quality checks | syn, quote | ~400 |

#### 3.2.2 Python Components

| Component | Purpose | Dependencies | Lines of Code |
|-----------|---------|--------------|---------------|
| pheno-testing | Core utilities | pytest, anyio | ~800 |
| pheno-quality | Code quality | ast, pylint | ~1000 |

#### 3.2.3 Go Components

| Component | Purpose | Dependencies | Lines of Code |
|-----------|---------|--------------|---------------|
| phenotype-testing | Core utilities | testify | ~200 |

### 3.3 Data Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Test Source   │────▶│  Test Discovery │────▶│  Test Execution │
│   Code Files    │     │  Language-native │     │  Parallel/Serial  │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                              ┌──────────────────────────┼──────────┐
                              │                          │          │
                              ▼                          ▼          ▼
                    ┌─────────────────┐       ┌─────────────────┐  ┌─────────────────┐
                    │  Mock Context   │       │  Fixture Setup  │  │  Quality Check  │
                    │  (if needed)    │       │  (if needed)    │  │  (optional)     │
                    └────────┬────────┘       └────────┬────────┘  └────────┬────────┘
                             │                       │                    │
                             └───────────────────────┴────────────────────┘
                                                         │
                                                         ▼
                                              ┌─────────────────┐
                                              │  Test Result    │
                                              │  Aggregation    │
                                              └────────┬────────┘
                                                       │
                              ┌────────────────────────┼────────────────────────┐
                              │                        │                        │
                              ▼                        ▼                        ▼
                    ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
                    │   JUnit XML     │      │   Coverage      │      │   CI/CD         │
                    │   Report        │      │   Report        │      │   Integration   │
                    └─────────────────┘      └─────────────────┘      └─────────────────┘
```

---

## 4. Detailed Component Specifications

### 4.1 phenotype-testing (Rust)

#### 4.1.1 Module Structure

```rust
//! Phenotype Testing - Core testing utilities

pub mod assertions;    // Assertion helpers
pub mod generators;    // Test data generators
pub mod runtime;       // Test runtime setup

// Core functions
pub async fn timeout<F, T>(future: F, duration: Duration) -> Result<T, Elapsed>;
pub async fn retry_async<F, Fut, T, E>(operation: F, max_attempts: u32, base_delay: Duration) -> Result<T, E>;
pub fn block_on<F, T>(future: F) -> T;
pub fn test_id() -> String;
pub fn random_port() -> u16;
pub async fn wait_for<F, Fut>(condition: F, timeout: Duration) -> bool;
```

#### 4.1.2 Timeout Function

**Signature:**
```rust
pub async fn timeout<F, T>(future: F, duration: Duration) -> Result<T, tokio::time::error::Elapsed>
where
    F: Future<Output = T>,
```

**Behavior:**
- Executes `future` with the specified timeout
- Returns `Ok(result)` if future completes within timeout
- Returns `Err(Elapsed)` if timeout expires
- Uses tokio's timer for accuracy

**Examples:**
```rust
#[tokio::test]
async fn test_with_timeout() {
    let result = timeout(
        async { expensive_operation().await },
        Duration::from_secs(5)
    ).await;
    
    assert!(result.is_ok(), "Operation timed out");
}
```

**Error Handling:**
- Elapsed error contains no additional information
- Caller responsible for interpreting timeout as failure

#### 4.1.3 Retry Function

**Signature:**
```rust
pub async fn retry_async<F, Fut, T, E>(
    mut operation: F,
    max_attempts: u32,
    base_delay: Duration,
) -> Result<T, E>
where
    F: FnMut() -> Fut,
    Fut: Future<Output = Result<T, E>>,
```

**Behavior:**
- Retries operation up to `max_attempts` times
- Uses exponential backoff: `base_delay * 2^attempt`
- Returns first Ok result
- Returns last Err if all attempts fail

**Retry Strategy:**
| Attempt | Delay Formula | Example (base=100ms) |
|---------|---------------|---------------------|
| 1 | base_delay | 100ms |
| 2 | base_delay * 2 | 200ms |
| 3 | base_delay * 4 | 400ms |
| 4 | base_delay * 8 | 800ms |

**Examples:**
```rust
#[tokio::test]
async fn test_with_retry() {
    let result = retry_async(
        || async { flaky_network_call().await },
        5,                    // Max 5 attempts
        Duration::from_millis(100),  // Start with 100ms
    ).await;
    
    assert!(result.is_ok());
}
```

#### 4.1.4 Test Data Generators

**Random String Generator:**
```rust
pub fn random_string(len: usize) -> String
```
- Uses alphanumeric charset: A-Z, a-z, 0-9
- Cryptographically insecure (for testing only)
- Thread-safe

**Random Email Generator:**
```rust
pub fn random_email() -> String
```
- Format: `{random(10)}@example.com`
- Guaranteed valid email format

**Random UUID Generator:**
```rust
pub fn random_uuid() -> String
```
- RFC 4122 version 4 UUID format
- Example: `550e8400-e29b-41d4-a716-446655440000`

#### 4.1.5 Port Allocator

**Signature:**
```rust
pub fn random_port() -> u16
```
- Returns ports from dynamic range: 49152-65535
- Uses thread_rng for distribution
- No guarantee of availability

**Usage Pattern:**
```rust
#[tokio::test]
async fn test_server() {
    let port = random_port();
    let server = TestServer::bind(port).await;
    // Test server...
}
```

### 4.2 phenotype-mock (Rust)

#### 4.2.1 Core Types

**CallRecord:**
```rust
#[derive(Debug, Clone, Default)]
pub struct CallRecord {
    pub method: String,
    pub args: Vec<String>,
    pub return_value: Option<String>,
    pub count: usize,
}
```

**Matcher:**
```rust
#[derive(Debug, Clone, Default)]
pub struct Matcher {
    pub method: String,
    pub expected_args: Option<Vec<String>>,
}
```

**Expectation:**
```rust
#[derive(Debug, Clone, Default)]
pub struct Expectation {
    pub matcher: Matcher,
    pub return_value: Option<String>,
    pub times: Option<usize>,
    pub called_count: usize,
}
```

#### 4.2.2 MockContext API

**Construction:**
```rust
impl MockContext {
    pub fn new() -> Self;
}
```

**Call Recording:**
```rust
pub fn record_call(&self, method: impl Into<String>, args: Vec<String>);
```

**Verification:**
```rust
pub fn verify_called(&self, method: impl AsRef<str>) -> bool;
pub fn verify_called_with(&self, method: impl AsRef<str>, args: &[&str]) -> bool;
pub fn verify_call_count(&self, method: impl AsRef<str>, expected: usize) -> bool;
pub fn call_count(&self, method: impl AsRef<str>) -> usize;
```

**Expectations:**
```rust
pub fn expect(&self, method: impl Into<String>) -> ExpectationBuilder;
pub fn get_return_value(&self, method: impl AsRef<str>, args: &[String]) -> Option<String>;
pub fn verify_all(&self) -> Result<(), Vec<String>>;
```

#### 4.2.3 ExpectationBuilder API

**Fluent Interface:**
```rust
impl ExpectationBuilder {
    pub fn with_args(mut self, args: Vec<impl Into<String>>) -> Self;
    pub fn returns<T: Into<String>>(mut self, value: T) -> Self;
    pub fn times(mut self, count: usize) -> Self;
    pub fn build(self);
}
```

**Usage Example:**
```rust
let ctx = MockContext::new();

ctx.expect("get_user")
    .with_args(vec!["123"])
    .returns(r#"{"id": "123", "name": "Alice"}"#)
    .times(1)
    .build();

// Use mock...

ctx.verify_all().expect("All expectations met");
```

#### 4.2.4 mock_trait! Macro

**Purpose:** Generate mock struct boilerplate

**Syntax:**
```rust
mock_trait!(
    MockName for TraitPath {
        fn method_name(arg1: Type1, arg2: Type2) -> ReturnType;
    }
);
```

**Expansion:**
```rust
// Input:
mock_trait!(MockDatabase for Database {
    fn get(&self, key: &str) -> Option<String>;
});

// Expands to:
pub struct MockDatabase {
    context: phenotype_mock::MockContext,
}

impl MockDatabase {
    pub fn new() -> Self {
        Self {
            context: phenotype_mock::MockContext::new(),
        }
    }
    
    pub fn context(&self) -> &phenotype_mock::MockContext {
        &self.context
    }
}

impl Default for MockDatabase {
    fn default() -> Self {
        Self::new()
    }
}
```

### 4.3 phenotype-test-fixtures (Rust)

#### 4.3.1 TestData Container

**Definition:**
```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TestData<T> {
    pub id: Uuid,
    pub name: String,
    pub value: T,
    pub created_at: DateTime<Utc>,
    pub metadata: HashMap<String, String>,
}
```

**Builder Pattern:**
```rust
impl<T: Default> TestData<T> {
    pub fn new(name: impl Into<String>, value: T) -> Self;
    pub fn with_metadata(mut self, key: impl Into<String>, value: impl Into<String>) -> Self;
}
```

**Usage:**
```rust
let data = TestData::new("test-user", User::default())
    .with_metadata("source", "fixture")
    .with_metadata("version", "1.0");
```

#### 4.3.2 TestScenario

**Definition:**
```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TestScenario {
    pub name: String,
    pub description: String,
    pub setup: Vec<TestStep>,
    pub execution: Vec<TestStep>,
    pub teardown: Vec<TestStep>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TestStep {
    pub name: String,
    pub action: String,
    pub expected_result: String,
}
```

### 4.4 phenotype-test-infra (Rust)

#### 4.4.1 TestServer

**Purpose:** HTTP test server for integration tests

**API:**
```rust
pub struct TestServer {
    pub addr: SocketAddr,
    pub base_url: String,
    _temp_dir: TempDir,
}

impl TestServer {
    pub async fn new() -> std::io::Result<Self>;
    pub fn url(&self, path: &str) -> String;
}
```

**Lifecycle:**
1. Create temp directory for server files
2. Bind to random port on localhost
3. Store address and base URL
4. Clean up temp directory on drop

#### 4.4.2 TestDatabase

**Purpose:** Temporary database for integration tests

**API:**
```rust
pub struct TestDatabase {
    pub connection_string: String,
    _temp_dir: TempDir,
}

impl TestDatabase {
    pub fn new() -> std::io::Result<Self>;
    pub async fn setup(&self) -> Result<(), Box<dyn std::error::Error>>;
    pub async fn teardown(&self) -> Result<(), Box<dyn std::error::Error>>;
}
```

**Default Configuration:**
- SQLite in temp directory
- Connection string: `sqlite:{temp_path}/test.db`
- Auto-cleanup on drop

#### 4.4.3 TestContext

**Purpose:** Aggregate all test resources

**API:**
```rust
pub struct TestContext {
    pub server: Option<TestServer>,
    pub database: Option<TestDatabase>,
    pub temp_dir: TempDir,
}

impl TestContext {
    pub fn new() -> std::io::Result<Self>;
    pub async fn with_server(mut self) -> std::io::Result<Self>;
    pub fn with_database(mut self) -> std::io::Result<Self>;
}
```

**Builder Pattern Usage:**
```rust
let ctx = TestContext::new()?
    .with_server().await?
    .with_database()?;

// Use ctx.server, ctx.database, ctx.temp_dir
// All resources cleaned up when ctx drops
```

### 4.5 pheno-testing (Python)

#### 4.5.1 MCP QA Framework

**MCP (Model Context Protocol) Testing:**

```python
# Process monitoring
from pheno_testing.mcp_qa.process import ProcessMonitor

monitor = ProcessMonitor(pid=1234)
monitor.start_monitoring()
metrics = monitor.get_metrics()
# metrics.cpu_percent, metrics.memory_mb, metrics.status

# Structured logging
from pheno_testing.mcp_qa.logging import MCPFormatter, MCPLogger

logger = MCPLogger(formatter=MCPFormatter(
    include_context=True,
    include_timestamp=True,
))

# Connection management
from pheno_testing.mcp_qa.monitoring import ConnectionManager

manager = ConnectionManager(
    max_connections=10,
    connection_timeout=30.0,
)
```

#### 4.5.2 Performance Testing

**Benchmark Decorator:**
```python
from pheno_testing.performance import Benchmark

@Benchmark(warmup=5, iterations=100, timeout=60.0)
def test_database_query():
    return db.query("SELECT * FROM large_table")
```

**Load Testing:**
```python
from pheno_testing.performance import LoadTester

tester = LoadTester(
    target=test_function,
    concurrent_users=10,
    duration=60.0,
)
results = tester.run()
# results.requests_per_second
# results.average_latency
# results.error_rate
```

#### 4.5.3 Async Fixtures

```python
from pheno_testing.fixtures import async_fixture

@async_fixture
async def async_client():
    client = await Client.connect()
    yield client
    await client.close()
```

### 4.6 pheno-quality (Python)

#### 4.6.1 Code Smell Detection

**Supported Smells:**

| Smell | Description | Detection Method |
|-------|-------------|------------------|
| God Object | Class with too many responsibilities | Method/field count |
| Feature Envy | Method using another class's data | Data flow analysis |
| Data Clump | Related data appearing together | Co-occurrence analysis |
| Shotgun Surgery | Change requires many modifications | Change coupling |
| Divergent Change | Class modified for different reasons | Change history |
| Message Chain | Excessive method chaining | Call chain length |
| Duplicate Code | Similar code blocks | AST comparison |
| Lazy Class | Minimal functionality class | Method complexity |
| Refused Bequest | Unused inheritance | Override analysis |
| Middle Man | Excessive delegation | Call forwarding |

**Detector Interface:**
```python
from pheno_quality.tools import CodeSmellDetector

detector = CodeSmellDetector(
    rules=[
        GodObjectRule(max_methods=20),
        FeatureEnvyRule(threshold=0.7),
    ]
)

issues = detector.analyze_file("src/service.py")
for issue in issues:
    print(f"{issue.location}: {issue.severity} - {issue.message}")
```

#### 4.6.2 Architectural Pattern Detection

**Supported Patterns:**

| Pattern | Validation Approach |
|---------|-------------------|
| Clean Architecture | Dependency direction |
| Domain-Driven Design | Aggregate boundaries |
| SOLID | Interface analysis |
| Hexagonal | Port/adapter matching |
| Layered | Layer dependency rules |
| Microservices | Service boundary detection |

**Validator Interface:**
```python
from pheno_quality.tools import ArchitecturalValidator

validator = ArchitecturalValidator(
    patterns=[CleanArchitecture(), DDD()]
)

report = validator.validate_project("src/")
for violation in report.violations:
    print(f"{violation.rule}: {violation.location}")
```

#### 4.6.3 pytest Integration

```python
# conftest.py
import pytest
from pheno_quality.pytest_plugin import QualityPlugin

def pytest_configure(config):
    config.pluginmanager.register(QualityPlugin(
        rules="pheno_quality.rules.STANDARD",
        fail_on="error",
    ))
```

**CLI Usage:**
```bash
# Run tests with quality checks
pytest --quality

# Quality-only run
pytest --quality-only

# Fail on warnings too
pytest --quality --quality-fail-level=warning
```

---

## 5. API Reference

### 5.1 Rust API Summary

#### phenotype-testing

| Function | Signature | Purpose |
|----------|-----------|---------|
| timeout | `async fn<F,T>(F, Duration) -> Result<T, Elapsed>` | Execute with timeout |
| timeout_default | `async fn<F,T>(F) -> Result<T, Elapsed>` | Execute with 5s timeout |
| block_on | `fn<F,T>(F) -> T` | Block on async in sync context |
| test_id | `fn() -> String` | Generate unique test ID |
| random_port | `fn() -> u16` | Generate random port |
| wait_for | `async fn<F,Fut>(F, Duration) -> bool` | Wait for condition |
| retry_async | `async fn<F,Fut,T,E>(F, u32, Duration) -> Result<T,E>` | Retry with backoff |

#### phenotype-mock

| Type | Purpose |
|------|---------|
| CallRecord | Record of mock invocation |
| Matcher | Argument matching specification |
| Expectation | Expected call specification |
| MockContext | Thread-safe mock state |
| ExpectationBuilder | Fluent expectation construction |

#### phenotype-test-fixtures

| Type | Purpose |
|------|---------|
| TestData<T> | Generic test data container |
| TestScenario | Multi-step test definition |
| TestStep | Single test step |
| TestEnv | Isolated test environment |

#### phenotype-test-infra

| Type | Purpose |
|------|---------|
| TestServer | HTTP server for integration tests |
| TestDatabase | Temporary database |
| TestContext | Aggregated test resources |
| PortAllocator | Sequential port allocation |

### 5.2 Python API Summary

#### pheno-testing

| Module | Purpose |
|--------|---------|
| mcp_qa | MCP testing framework |
| performance | Benchmarking utilities |
| fixtures | Test fixtures |
| markers | Custom pytest markers |

#### pheno-quality

| Class | Purpose |
|-------|---------|
| CodeSmellDetector | Detect code smells |
| ArchitecturalValidator | Validate architecture |
| PatternDetector | Detect patterns |

---

## 6. Integration Points

### 6.1 CI/CD Integration

#### GitHub Actions

```yaml
name: TestingKit CI

on: [push, pull_request]

jobs:
  rust-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Rust
        uses: dtolnay/rust-action@stable
      
      - name: Install Nextest
        run: cargo install cargo-nextest
      
      - name: Run Rust Tests
        run: cargo nextest run --profile ci
      
      - name: Code Quality
        run: cargo run -p phenotype-compliance-scanner

  python-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install Dependencies
        run: |
          pip install -e "python/pheno-testing"
          pip install -e "python/pheno-quality"
      
      - name: Run Python Tests
        run: pytest python/ --cov --cov-report=xml
      
      - name: Code Quality
        run: pytest python/ --quality
```

### 6.2 Test Result Format

#### JUnit XML Schema

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="phenotype-testing" tests="42" failures="0" errors="0" time="1.23">
    <testcase name="test_timeout_success" time="0.01"/>
    <testcase name="test_retry_async" time="0.05">
      <system-out>Attempt 1 failed, retrying...</system-out>
    </testcase>
    <testcase name="test_mock_context" time="0.001"/>
  </testsuite>
</testsuites>
```

### 6.3 Coverage Integration

#### Rust

```bash
# Generate coverage
cargo tarpaulin --out Xml --out Html

# Or with llvm-cov
cargo llvm-cov --html
```

#### Python

```bash
# Generate coverage
pytest --cov=pheno_testing --cov-report=xml --cov-report=html
```

---

## 7. Performance Requirements

### 7.1 Test Execution Performance

| Metric | Requirement | Measurement |
|--------|-------------|-------------|
| Unit test execution | < 10ms/test | Mean across suite |
| Mock setup | < 1ms | From construction to first use |
| Fixture creation | < 5ms | Simple fixture |
| Test discovery | < 1s per 1000 tests | Cold start |

### 7.2 Code Quality Analysis Performance

| Metric | Requirement | Measurement |
|--------|-------------|-------------|
| File analysis | < 100ms per 1000 LOC | Single file |
| Project analysis | < 5s per 10K LOC | Entire project |
| Incremental analysis | < 1s | Changed files only |

### 7.3 Resource Limits

| Resource | Limit | Notes |
|----------|-------|-------|
| Memory per test | 100MB | Soft limit |
| Disk per test | 50MB | Temp files |
| Concurrent tests | CPU cores | Configurable |
| Test timeout | 60s | Default |

---

## 8. Security Considerations

### 8.1 Test Isolation

**Process Isolation:**
- Each test should run in isolation
- No shared mutable state between tests
- Mock contexts are thread-safe but not process-safe

**File System Isolation:**
- Use TempDir for all file operations
- Clean up on test completion
- Unique directories per test

**Network Isolation:**
- Use random ports for test servers
- Prefer loopback (127.0.0.1) only
- Mock external services

### 8.2 Data Handling

**Sensitive Data:**
- Never commit real credentials
- Use fixture generators for test data
- Sanitize logs and reports

**Random Data:**
- Generators are not cryptographically secure
- Not suitable for security-critical code
- Use proper crypto for production

### 8.3 Code Quality Security

**Detection Rules:**
- Flag hardcoded secrets
- Detect unsafe patterns
- Validate input sanitization

---

## 9. Testing Strategy

### 9.1 Test Levels

```
┌─────────────────────────────────────┐
│         E2E Tests (5%)               │
│    Cross-language integration        │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│      Integration Tests (15%)         │
│    Component interactions            │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│        Unit Tests (80%)              │
│    Individual functions/types        │
└─────────────────────────────────────┘
```

### 9.2 Test Categories

| Category | Percentage | Tools |
|----------|------------|-------|
| Unit | 80% | Built-in + Nextest/pytest |
| Integration | 15% | TestServer, TestDatabase |
| E2E | 5% | Full stack scenarios |
| Property-based | 10% | proptest, Hypothesis |
| Mutation | Periodic | cargo-mutants, mutmut |

### 9.3 Testing Requirements

**All Code Must Have:**
- Unit tests for public APIs
- Integration tests for I/O operations
- Documentation tests (Rust)
- Property-based tests for algorithms

**Quality Gates:**
- 80% line coverage minimum
- No flaky tests in CI
- All code smells resolved or documented
- Mutation score > 50%

---

## 10. Deployment and Distribution

### 10.1 Crate/Package Structure

**Rust (crates.io):**
```
phenotype-testing@1.0.0
phenotype-mock@1.0.0
phenotype-test-fixtures@1.0.0
phenotype-test-infra@1.0.0
```

**Python (PyPI):**
```
pheno-testing==1.0.0
pheno-quality==1.0.0
```

**Go (proxy):**
```
github.com/phenotype/testing
```

### 10.2 Versioning

**Semantic Versioning:**
- MAJOR: Breaking API changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes

**Pre-release:**
- `-alpha.X` - Early testing
- `-beta.X` - Feature complete
- `-rc.X` - Release candidate

---

## 11. Monitoring and Observability

### 11.1 Test Metrics

| Metric | Type | Alert Threshold |
|--------|------|-----------------|
| Test duration | Histogram | P99 < 10s |
| Test flakiness | Gauge | > 1% |
| Coverage | Gauge | < 80% |
| Mock usage | Counter | N/A |

### 11.2 Tracing

**Test Execution Trace:**
```rust
use tracing::{info_span, instrument};

#[instrument]
#[test]
fn test_with_tracing() {
    let span = info_span!("test_execution", test_name = "test_with_tracing");
    let _enter = span.enter();
    
    // Test code with automatic tracing
}
```

---

## 12. Future Enhancements

### 12.1 Planned Features

| Feature | Priority | Target |
|---------|----------|--------|
| Visual test diff | Medium | 1.1.0 |
| Snapshot testing | High | 1.1.0 |
| Fuzzing integration | Medium | 1.2.0 |
| WebAssembly testing | Low | 1.3.0 |
| AI test generation | Research | TBD |

### 12.2 Research Areas

1. **AI-Assisted Test Generation**
   - LLM-based test case generation
   - Automated test repair
   - Smart test selection

2. **Distributed Testing**
   - Remote test execution
   - Test result aggregation
   - Cluster-based parallelization

---

## 13. Glossary

| Term | Definition |
|------|------------|
| Fixture | Reusable test setup/teardown |
| Mock | Test double with verification |
| Stub | Test double with canned responses |
| Code Smell | Indicator of deeper problems |
| Property-based | Testing via generated inputs |
| Mutation Testing | Testing by mutating code |
| Flaky Test | Non-deterministic test |

---

## 14. Appendices

### Appendix A: Migration Guide

#### From Existing Frameworks

**From mockall (Rust):**
```rust
// mockall
#[automock]
trait Database { }

// phenotype-mock
mock_trait!(MockDatabase for Database { });
```

**From unittest.mock (Python):**
```python
# unittest.mock
mock = Mock()
mock.method.return_value = 42

# pheno-quality
# Use fixture-based approach with type safety
```

### Appendix B: Troubleshooting

**Issue: Tests timeout unexpectedly**
- Check for blocking operations in async tests
- Verify Tokio runtime configuration
- Use `timeout()` wrapper

**Issue: Mock verification fails**
- Ensure `verify_all()` called
- Check argument matching (exact vs. partial)
- Verify method names match exactly

**Issue: Quality checks too slow**
- Enable incremental analysis
- Exclude generated code
- Tune rule thresholds

### Appendix C: Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Test requirements
- PR process

---

*End of Specification Document*

---

## Appendix D: Detailed Test Patterns

### D.1 Mock Pattern Library

**Pattern 1: Verify Method Called**
```rust
#[test]
fn test_service_calls_repository() {
    let ctx = MockContext::new();
    let mock_repo = MockRepository::with_context(&ctx);
    
    let service = UserService::new(mock_repo);
    service.get_user(1);
    
    assert!(ctx.verify_called("get_user"));
    assert!(ctx.verify_called_with("get_user", &["1"]));
}
```

**Pattern 2: Stub Return Values**
```rust
#[test]
fn test_service_uses_repository_result() {
    let ctx = MockContext::new();
    ctx.expect("get_user")
        .with_args(vec!["1"])
        .returns(r#"{"id":1,"name":"Alice"}"#)
        .build();
    
    let mock_repo = MockRepository::with_context(&ctx);
    let service = UserService::new(mock_repo);
    
    let user = service.get_user(1);
    assert_eq!(user.name, "Alice");
}
```

**Pattern 3: Mock Sequence**
```rust
#[test]
fn test_service_calls_in_order() {
    let ctx = MockContext::new();
    
    // First call
    ctx.expect("begin_transaction").times(1).build();
    // Second call
    ctx.expect("save").times(1).build();
    // Third call
    ctx.expect("commit").times(1).build();
    
    let mock_repo = MockRepository::with_context(&ctx);
    let service = UserService::new(mock_repo);
    
    service.create_user("Alice");
    
    ctx.verify_all().expect("All expectations met");
}
```

### D.2 Async Test Patterns

**Pattern 1: Basic Async Test**
```rust
#[tokio::test]
async fn test_async_operation() {
    let result = async_operation().await;
    assert!(result.is_ok());
}
```

**Pattern 2: Async with Timeout**
```rust
#[tokio::test]
async fn test_async_with_timeout() {
    let result = timeout(
        async_operation(),
        Duration::from_secs(5)
    ).await;
    
    assert!(result.is_ok());
}
```

**Pattern 3: Concurrent Operations**
```rust
#[tokio::test]
async fn test_concurrent_operations() {
    let handles: Vec<_> = (0..10)
        .map(|i| tokio::spawn(async move {
            operation(i).await
        }))
        .collect();
    
    let results = futures::future::join_all(handles).await;
    
    for result in results {
        assert!(result.is_ok());
    }
}
```

### D.3 Fixture Patterns

**Pattern 1: Database Setup**
```rust
struct DatabaseFixture {
    db: TestDatabase,
    connection: Connection,
}

impl DatabaseFixture {
    async fn new() -> Self {
        let db = TestDatabase::new().unwrap();
        let connection = create_connection(&db.connection_string).await;
        run_migrations(&connection).await;
        
        Self { db, connection }
    }
    
    async fn seed_data(&self) {
        // Insert test data
    }
}

#[tokio::test]
async fn test_with_database() {
    let fixture = DatabaseFixture::new().await;
    fixture.seed_data().await;
    
    // Run tests
}
```

**Pattern 2: HTTP Server Fixture**
```rust
struct ServerFixture {
    server: TestServer,
    client: TestClient,
}

impl ServerFixture {
    async fn new() -> Self {
        let server = TestServer::new().await.unwrap();
        let client = TestClient::new(&server.base_url);
        
        Self { server, client }
    }
}

#[tokio::test]
async fn test_api_endpoint() {
    let fixture = ServerFixture::new().await;
    
    let response = fixture.client.get("/api/users").await;
    assert_eq!(response.status, 200);
}
```

---

## Appendix E: Advanced Testing Scenarios

### E.1 Property-Based Testing

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_sort_reverses_reverse(input in prop::collection::vec(1..100i32, 0..100)) {
        let mut sorted = input.clone();
        sorted.sort();
        sorted.reverse();
        
        let mut double_reversed = sorted.clone();
        double_reversed.reverse();
        double_reversed.sort();
        
        prop_assert_eq!(input, double_reversed);
    }
    
    #[test]
    fn test_merge_preserves_elements(
        left in prop::collection::vec(1..100i32, 0..50),
        right in prop::collection::vec(1..100i32, 0..50)
    ) {
        let mut merged = left.clone();
        merged.extend(right.clone());
        merged.sort();
        
        let total_len = left.len() + right.len();
        prop_assert_eq!(merged.len(), total_len);
    }
}
```

### E.2 Fuzz Testing

```rust
#![cfg(fuzzing)]

use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    if let Ok(s) = std::str::from_utf8(data) {
        // Test parser with random input
        let _ = parser::parse(s);
    }
});
```

### E.3 Load Testing Pattern

```rust
#[tokio::test]
async fn test_under_load() {
    let metrics = Arc::new(Mutex::new(LoadMetrics::default()));
    
    let start = Instant::now();
    let handles: Vec<_> = (0..100)
        .map(|_| {
            let metrics = metrics.clone();
            tokio::spawn(async move {
                let req_start = Instant::now();
                let result = make_request().await;
                let duration = req_start.elapsed();
                
                metrics.lock().unwrap().record(duration, result.is_ok());
            })
        })
        .collect();
    
    futures::future::join_all(handles).await;
    
    let total_duration = start.elapsed();
    let final_metrics = metrics.lock().unwrap();
    
    println!("Total time: {:?}", total_duration);
    println!("Success rate: {:.2}%", final_metrics.success_rate() * 100.0);
    println!("Avg latency: {:?}", final_metrics.avg_latency());
}
```

---

## Appendix F: CI/CD Integration Details

### F.1 GitHub Actions Full Configuration

```yaml
name: TestingKit CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  CARGO_TERM_COLOR: always
  RUST_BACKTRACE: 1

jobs:
  rust-tests:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        rust: [stable, nightly]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Install Rust
      uses: dtolnay/rust-action@stable
      with:
        toolchain: ${{ matrix.rust }}
    
    - name: Install cargo-nextest
      uses: taiki-e/install-action@nextest
    
    - name: Cache cargo registry
      uses: actions/cache@v3
      with:
        path: ~/.cargo/registry
        key: ${{ runner.os }}-cargo-registry-${{ hashFiles('**/Cargo.lock') }}
    
    - name: Cache cargo index
      uses: actions/cache@v3
      with:
        path: ~/.cargo/git
        key: ${{ runner.os }}-cargo-index-${{ hashFiles('**/Cargo.lock') }}
    
    - name: Cache cargo build
      uses: actions/cache@v3
      with:
        path: target
        key: ${{ runner.os }}-cargo-build-target-${{ hashFiles('**/Cargo.lock') }}
    
    - name: Check formatting
      run: cargo fmt -- --check
    
    - name: Run clippy
      run: cargo clippy -- -D warnings
    
    - name: Build
      run: cargo build --verbose
    
    - name: Run tests with nextest
      run: cargo nextest run --profile ci
    
    - name: Generate coverage
      run: |
        cargo install cargo-tarpaulin
        cargo tarpaulin --out Xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: ./cobertura.xml
        fail_ci_if_error: true

  python-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -e "python/pheno-testing"
        pip install -e "python/pheno-quality"
        pip install pytest pytest-cov pytest-asyncio hypothesis
    
    - name: Run tests with coverage
      run: |
        pytest python/ --cov=pheno_testing --cov=pheno_quality \
          --cov-report=xml --cov-report=html
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml

  quality-gates:
    runs-on: ubuntu-latest
    needs: [rust-tests, python-tests]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Check code quality
      run: |
        cd python/pheno-quality
        python -m pheno_quality.tools.code_smell_detector --fail-on-error
```

### F.2 GitLab CI Configuration

```yaml
stages:
  - test
  - coverage
  - quality

variables:
  CARGO_HOME: $CI_PROJECT_DIR/.cargo
  RUST_BACKTRACE: 1

cache:
  paths:
    - .cargo/
    - target/

rust:test:
  stage: test
  image: rust:latest
  script:
    - cargo test --verbose
  artifacts:
    reports:
      junit: target/nextest/ci/junit.xml

python:test:
  stage: test
  image: python:3.12
  script:
    - pip install -e "python/pheno-testing"
    - pytest --junitxml=report.xml
  artifacts:
    reports:
      junit: report.xml

coverage:
  stage: coverage
  image: rust:latest
  script:
    - cargo install cargo-tarpaulin
    - cargo tarpaulin --out Xml
  coverage: '/\d+\.?\d*%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: cobertura.xml
```

---

## Appendix G: Troubleshooting Guide

### G.1 Common Issues and Solutions

**Issue 1: Flaky Tests**
- Cause: Timeouts, race conditions, external dependencies
- Solution: Use TestServer, MockContext, deterministic timeouts

**Issue 2: Slow Tests**
- Cause: Database setup, network calls, file I/O
- Solution: Mock external deps, use in-memory databases, parallel execution

**Issue 3: Test Isolation Failures**
- Cause: Global state, shared resources
- Solution: Use TestEnv, clean up in teardown, process-per-test

**Issue 4: Async Test Failures**
- Cause: Runtime not initialized, timing issues
- Solution: Use #[tokio::test], proper timeout handling

### G.2 Debugging Tips

1. **Use RUST_BACKTRACE=1** for Rust test failures
2. **Use pytest -v --tb=long** for detailed Python tracebacks
3. **Run single test** to isolate issues
4. **Add logging** for complex scenarios
5. **Use test profiling** to find slow tests

---

## Appendix H: Migration Guide

### H.1 From Existing Frameworks

**From mockall (Rust):**
```rust
// Before: mockall
#[automock]
trait Database { }

// After: phenotype-mock
mock_trait!(MockDatabase for Database { });
```

**From unittest.mock (Python):**
```python
# Before
from unittest.mock import Mock
mock = Mock()
mock.method.return_value = 42

// After: Use fixture-based patterns with pheno-testing
```

### H.2 Gradual Adoption

1. Start with new tests using TestingKit
2. Migrate critical tests first
3. Maintain legacy tests during transition
4. Use adapter patterns for integration

---

## Appendix I: Glossary

| Term | Definition |
|------|------------|
| Fixture | Reusable test setup/teardown |
| Mock | Test double with verification |
| Stub | Test double with canned responses |
| Spy | Test double that records calls |
| Fake | Working simplified implementation |
| Code Smell | Indicator of deeper problems |
| Property-based | Testing via generated inputs |
| Mutation Testing | Testing by mutating code |
| Flaky Test | Non-deterministic test |
| Coverage | Percentage of code exercised by tests |

---

## Appendix J: Extended References

### J.1 Books

1. "xUnit Test Patterns" - Gerard Meszaros
2. "Test Driven Development" - Kent Beck
3. "Growing Object-Oriented Software" - Freeman & Pryce
4. "The Art of Unit Testing" - Roy Osherove

### J.2 Online Resources

1. [Rust Testing Guide](https://doc.rust-lang.org/book/ch11-00-testing.html)
2. [pytest Documentation](https://docs.pytest.org/)
3. [Testing Strategies](https://testing.googleblog.com/)
4. [Martin Fowler on Testing](https://martinfowler.com/testing/)

### J.3 Courses

1. "Testing with Rust" - Various platforms
2. "Advanced pytest" - Test automation university
3. "Mutation Testing Workshop" - Conference materials

---

## Appendix K: Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-05 | Initial release |

---

---

## Appendix L: Extended API Examples

### L.1 Advanced Mock Scenarios

**Scenario 1: Mocking Async Functions**
```rust
use phenotype_mock::{MockContext, mock_async_trait};
use async_trait::async_trait;

#[async_trait]
trait AsyncDatabase {
    async fn query(&self, sql: &str) -> Result<Vec<Row>, Error>;
    async fn execute(&self, sql: &str) -> Result<u64, Error>;
}

mock_async_trait!(MockAsyncDatabase for AsyncDatabase {
    async fn query(&self, sql: &str) -> Result<Vec<Row>, Error>;
    async fn execute(&self, sql: &str) -> Result<u64, Error>;
});

#[tokio::test]
async fn test_async_mock() {
    let ctx = MockContext::new();
    ctx.expect("query")
        .with_args(vec!["SELECT * FROM users"])
        .returns(r#"[{"id":1,"name":"Alice"}]"#)
        .build();
    
    let db = MockAsyncDatabase::with_context(&ctx);
    let rows = db.query("SELECT * FROM users").await.unwrap();
    
    assert_eq!(rows.len(), 1);
    assert_eq!(rows[0].get("name"), Some(&Value::String("Alice".to_string())));
}
```

**Scenario 2: Mock with Side Effects**
```rust
#[test]
fn test_mock_with_side_effects() {
    let ctx = MockContext::new();
    let call_count = Arc::new(AtomicU32::new(0));
    
    ctx.expect("process")
        .times(3)
        .with_side_effect({
            let count = call_count.clone();
            move || {
                count.fetch_add(1, Ordering::SeqCst);
            }
        })
        .build();
    
    // Execute multiple times
    for _ in 0..3 {
        ctx.trigger("process");
    }
    
    assert_eq!(call_count.load(Ordering::SeqCst), 3);
}
```

**Scenario 3: Conditional Mock Responses**
```rust
#[test]
fn test_conditional_responses() {
    let ctx = MockContext::new();
    
    // Return different values based on input
    ctx.expect("get")
        .with_args(vec!["user:1"])
        .returns(r#"{"id":1,"name":"Alice"}"#)
        .build();
    
    ctx.expect("get")
        .with_args(vec!["user:2"])
        .returns(r#"{"id":2,"name":"Bob"}"#)
        .build();
    
    ctx.expect("get")
        .with_args(vec!["user:999"])
        .returns("")  // Simulate not found
        .build();
    
    // Verify different responses
    assert!(ctx.get_return_value("get", &["user:1".to_string()]).is_some());
    assert!(ctx.get_return_value("get", &["user:2".to_string()]).is_some());
    assert!(ctx.get_return_value("get", &["user:999".to_string()]).is_some());
    assert!(ctx.get_return_value("get", &["user:unknown".to_string()]).is_none());
}
```

### L.2 Complex Test Environment Scenarios

**Scenario 1: Multi-Service Test Environment**
```rust
struct MicroserviceTestEnv {
    api_server: TestServer,
    database: TestDatabase,
    cache: TestCache,
    message_queue: TestMessageQueue,
}

impl MicroserviceTestEnv {
    async fn new() -> Result<Self, Error> {
        Ok(Self {
            api_server: TestServer::new().await?,
            database: TestDatabase::new()?,
            cache: TestCache::new(),
            message_queue: TestMessageQueue::new().await?,
        })
    }
    
    async fn setup_integration(&self) -> Result<(), Error> {
        // Configure services to communicate
        self.api_server.configure_db(&self.database).await;
        self.api_server.configure_cache(&self.cache).await;
        self.api_server.configure_mq(&self.message_queue).await;
        Ok(())
    }
}

#[tokio::test]
async fn test_end_to_end_flow() {
    let env = MicroserviceTestEnv::new().await.unwrap();
    env.setup_integration().await.unwrap();
    
    // Seed test data
    env.database.seed("tests/fixtures/integration_data.sql").await;
    
    // Execute API call
    let response = env.api_server
        .client()
        .post("/api/orders")
        .json(&order_request)
        .send()
        .await;
    
    // Verify response
    assert_eq!(response.status(), 201);
    
    // Verify database state
    let orders = env.database.query("SELECT * FROM orders").await;
    assert_eq!(orders.len(), 1);
    
    // Verify cache
    let cached = env.cache.get("order:latest").await;
    assert!(cached.is_some());
    
    // Verify message published
    let messages = env.message_queue.consume("orders.created").await;
    assert_eq!(messages.len(), 1);
}
```

**Scenario 2: Performance Test Environment**
```rust
struct PerformanceTestEnv {
    server: TestServer,
    load_generator: LoadGenerator,
    metrics_collector: MetricsCollector,
}

impl PerformanceTestEnv {
    async fn run_load_test(&self, config: LoadTestConfig) -> PerformanceReport {
        let start = Instant::now();
        
        // Generate load
        self.load_generator.run(config).await;
        
        // Collect metrics
        let metrics = self.metrics_collector.collect().await;
        
        PerformanceReport {
            duration: start.elapsed(),
            total_requests: metrics.total_requests,
            successful_requests: metrics.successful,
            failed_requests: metrics.failed,
            avg_latency: metrics.avg_latency(),
            p95_latency: metrics.p95_latency(),
            p99_latency: metrics.p99_latency(),
            throughput: metrics.throughput(),
        }
    }
}

#[tokio::test]
async fn test_api_performance() {
    let env = PerformanceTestEnv::new().await.unwrap();
    
    let config = LoadTestConfig {
        concurrent_users: 100,
        duration: Duration::from_secs(60),
        ramp_up: Duration::from_secs(10),
    };
    
    let report = env.run_load_test(config).await;
    
    // Assert performance criteria
    assert!(report.avg_latency < Duration::from_millis(100));
    assert!(report.p95_latency < Duration::from_millis(200));
    assert!(report.p99_latency < Duration::from_millis(500));
    assert_eq!(report.failed_requests, 0);
}
```

### L.3 Advanced Fixture Patterns

**Pattern 1: Parametrized Fixtures**
```rust
use phenotype_test_fixtures::ParameterizedFixture;

struct UserFixture {
    user_type: UserType,
    permissions: Vec<Permission>,
}

#[fixture(param = "admin")]
fn admin_user() -> UserFixture {
    UserFixture {
        user_type: UserType::Admin,
        permissions: vec![Permission::All],
    }
}

#[fixture(param = "regular")]
fn regular_user() -> UserFixture {
    UserFixture {
        user_type: UserType::User,
        permissions: vec![Permission::Read, Permission::Write],
    }
}

#[fixture(param = "guest")]
fn guest_user() -> UserFixture {
    UserFixture {
        user_type: UserType::Guest,
        permissions: vec![Permission::Read],
    }
}

#[test]
#[parametrized_fixture(user_fixture, ["admin", "regular", "guest"])]
fn test_user_permissions(user: UserFixture) {
    match user.user_type {
        UserType::Admin => assert!(user.permissions.contains(&Permission::All)),
        UserType::User => {
            assert!(user.permissions.contains(&Permission::Read));
            assert!(user.permissions.contains(&Permission::Write));
        }
        UserType::Guest => {
            assert!(user.permissions.contains(&Permission::Read));
            assert!(!user.permissions.contains(&Permission::Write));
        }
    }
}
```

**Pattern 2: Hierarchical Fixtures**
```rust
// Base fixture
#[fixture]
fn database() -> TestDatabase {
    TestDatabase::new().unwrap()
}

// Derived fixture
#[fixture]
fn populated_database(database: TestDatabase) -> TestDatabase {
    database.seed(include_str!("fixtures/users.sql"));
    database.seed(include_str!("fixtures/orders.sql"));
    database
}

// Further derived
#[fixture]
fn database_with_orders(populated_database: TestDatabase) -> TestDatabase {
    populated_database.execute("INSERT INTO orders ...");
    populated_database
}

#[test]
fn test_with_populated_db(database_with_orders: TestDatabase) {
    let orders = database_with_orders.query("SELECT * FROM orders");
    assert!(!orders.is_empty());
}
```

**Pattern 3: Scoped Fixtures**
```rust
use phenotype_testing::fixtures::{fixture, Scope};

// Function-scoped: fresh for each test
#[fixture(scope = Scope::Function)]
fn temp_file() -> TempFile {
    TempFile::new()
}

// Module-scoped: shared within module
#[fixture(scope = Scope::Module)]
fn module_cache() -> Cache {
    Cache::new()
}

// Session-scoped: shared across all tests
#[fixture(scope = Scope::Session)]
fn test_config() -> Config {
    Config::load("tests/config.yaml")
}
```

### L.4 Test Data Factory Patterns

**Factory with Builders**
```rust
use phenotype_test_fixtures::{Factory, Builder};

#[derive(Builder)]
struct UserBuilder {
    id: u64,
    name: String,
    email: String,
    role: Role,
    created_at: DateTime<Utc>,
}

impl Factory for UserBuilder {
    type Product = User;
    
    fn default() -> Self {
        Self {
            id: generate_id(),
            name: "Test User".to_string(),
            email: format!("user{}@example.com", generate_id()),
            role: Role::User,
            created_at: Utc::now(),
        }
    }
    
    fn build(self) -> User {
        User {
            id: self.id,
            name: self.name,
            email: self.email,
            role: self.role,
            created_at: self.created_at,
        }
    }
}

#[test]
fn test_user_factory() {
    // Default user
    let user1 = UserBuilder::new().build();
    assert_eq!(user1.role, Role::User);
    
    // Custom user
    let admin = UserBuilder::new()
        .name("Admin User")
        .email("admin@example.com")
        .role(Role::Admin)
        .build();
    assert_eq!(admin.role, Role::Admin);
    
    // Multiple users
    let users: Vec<_> = (0..100)
        .map(|i| UserBuilder::new().name(format!("User {}", i)).build())
        .collect();
    assert_eq!(users.len(), 100);
}
```

### L.5 Advanced Assertion Patterns

**Custom Assertion Macros**
```rust
#[macro_export]
macro_rules! assert_within_range {
    ($value:expr, $min:expr, $max:expr) => {
        assert!(
            $value >= $min && $value <= $max,
            "Expected {} to be within range [{}, {}], but got {}",
            stringify!($value),
            $min,
            $max,
            $value
        );
    };
}

#[macro_export]
macro_rules! assert_matches {
    ($result:expr, $pattern:pat) => {
        match $result {
            $pattern => (),
            _ => panic!(
                "Expected {} to match {}, but got {:?}",
                stringify!($result),
                stringify!($pattern),
                $result
            ),
        }
    };
}

#[test]
fn test_custom_assertions() {
    let score = 85;
    assert_within_range!(score, 0, 100);
    
    let result = process_data();
    assert_matches!(result, Ok(Data { status: Status::Active, .. }));
}
```

---

## Appendix M: Code Quality Detector Details

### M.1 Code Smell Detection Rules

**Rule 1: God Object Detection**
```python
# Detector implementation
class GodObjectDetector(CodeSmellDetector):
    MAX_METHODS = 20
    MAX_FIELDS = 15
    MAX_DEPENDENCIES = 10
    
    def analyze(self, cls: ClassDef) -> List[CodeSmell]:
        smells = []
        
        method_count = len(cls.methods)
        field_count = len(cls.fields)
        dependency_count = len(self.get_dependencies(cls))
        
        if method_count > self.MAX_METHODS:
            smells.append(CodeSmell(
                type=SmellType.GOD_OBJECT,
                message=f"Class has {method_count} methods (max {self.MAX_METHODS})",
                severity=Severity.WARNING,
                location=cls.location
            ))
        
        if field_count > self.MAX_FIELDS:
            smells.append(CodeSmell(
                type=SmellType.GOD_OBJECT,
                message=f"Class has {field_count} fields (max {self.MAX_FIELDS})",
                severity=Severity.WARNING,
                location=cls.location
            ))
        
        return smells
```

**Rule 2: Feature Envy Detection**
```python
class FeatureEnvyDetector(CodeSmellDetector):
    THRESHOLD = 0.7  # 70% of method calls on other class
    
    def analyze(self, method: MethodDef) -> List[CodeSmell]:
        smells = []
        
        # Count method calls on different classes
        external_calls = defaultdict(int)
        total_calls = 0
        
        for call in method.method_calls:
            if call.receiver != "self" and call.receiver != method.class_name:
                external_calls[call.receiver_type] += 1
                total_calls += 1
        
        if total_calls > 0:
            for class_name, count in external_calls.items():
                ratio = count / total_calls
                if ratio > self.THRESHOLD:
                    smells.append(CodeSmell(
                        type=SmellType.FEATURE_ENVY,
                        message=f"Method makes {ratio:.0%} calls on {class_name}",
                        severity=Severity.INFO,
                        location=method.location,
                        suggestion=f"Consider moving method to {class_name}"
                    ))
        
        return smells
```

**Rule 3: Duplicate Code Detection**
```python
class DuplicateCodeDetector(CodeSmellDetector):
    SIMILARITY_THRESHOLD = 0.8
    MIN_LINES = 5
    
    def analyze_module(self, module: Module) -> List[CodeSmell]:
        smells = []
        code_blocks = self.extract_code_blocks(module)
        
        for i, block1 in enumerate(code_blocks):
            for block2 in code_blocks[i+1:]:
                similarity = self.calculate_similarity(block1, block2)
                
                if similarity > self.SIMILARITY_THRESHOLD:
                    smells.append(CodeSmell(
                        type=SmellType.DUPLICATE_CODE,
                        message=f"{similarity:.0%} similar code blocks detected",
                        severity=Severity.WARNING,
                        locations=[block1.location, block2.location],
                        suggestion="Consider extracting common logic to a function"
                    ))
        
        return smells
    
    def calculate_similarity(self, block1: CodeBlock, block2: CodeBlock) -> float:
        # Use AST-based or token-based similarity
        tokens1 = self.tokenize(block1)
        tokens2 = self.tokenize(block2)
        return jaccard_similarity(tokens1, tokens2)
```

---

## Appendix N: Extended Testing Metrics

### N.1 Code Coverage Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Line Coverage | Lines executed / Total lines | > 80% |
| Branch Coverage | Branches taken / Total branches | > 75% |
| Function Coverage | Functions called / Total functions | > 90% |
| Statement Coverage | Statements executed / Total statements | > 80% |
| Condition Coverage | Boolean conditions evaluated / Total conditions | > 70% |
| MC/DC | Modified condition/decision coverage | > 90% (safety-critical) |

### N.2 Quality Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Test Execution Time | Time to run full suite | < 5 minutes |
| Test Maintainability | Ease of test updates | < 10 min per change |
| Flaky Test Rate | % of non-deterministic tests | < 1% |
| Test Documentation | % of tests with docstrings | > 80% |
| Assertion Density | Assertions per test | 3-5 |

---

---

## Appendix O: Release and Deployment

### O.1 Versioning Strategy

TestingKit follows Semantic Versioning (SemVer):
- **MAJOR**: Breaking API changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### O.2 Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in Cargo.toml
- [ ] Git tag created
- [ ] Crates.io published
- [ ] GitHub release notes

### O.3 Deployment Targets

| Target | Platform | Priority |
|--------|----------|----------|
| crates.io | Rust | Primary |
| PyPI | Python | Primary |
| GitHub Releases | All | Secondary |

---

## Appendix P: Community and Support

### P.1 Contributing Guidelines

We welcome contributions! Please see our Contributing Guide for details on:
- Code of Conduct
- Development setup
- Pull request process
- Coding standards

### P.2 Support Channels

- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: Questions and ideas
- Discord: Real-time community chat

### P.3 Acknowledgments

Thanks to all contributors who have helped make TestingKit better!

---

## Appendix Q: Extended Bibliography

### Q.1 Academic Papers

1. Claessen, K., & Hughes, J. (2000). QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs.
2. Meszaros, G. (2007). xUnit Test Patterns: Refactoring Test Code.
3. Beizer, B. (1990). Software Testing Techniques.
4. Myers, G. J. (2011). The Art of Software Testing.

### Q.2 Technical Reports

1. Google Testing Blog - Various articles on testing best practices
2. Martin Fowler's Testing Articles
3. Netflix Tech Blog - Distributed Testing
4. Microsoft Research - Testing at Scale

### Q.3 Standards and Guidelines

1. ISO/IEC/IEEE 29119 - Software Testing Standards
2. ISTQB Testing Certification Materials
3. OWASP Testing Guide

---

*End of Final Specification Document*








































































































































































































