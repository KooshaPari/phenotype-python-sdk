# Architecture Decision Records: TestingKit

## ADR-001: Multi-Language Testing Framework Architecture

### Status
**Accepted** | 2026-04-05

### Context

The Phenotype ecosystem spans multiple programming languages:
- Rust (core systems, CLI tools)
- Python (data processing, ML pipelines)
- Go (infrastructure, cloud services)

Each language has its own testing idioms, frameworks, and best practices. The challenge is providing a unified testing experience while respecting language-specific conventions and leveraging each language's strengths.

**Forces:**
1. Need consistent testing patterns across the ecosystem
2. Must respect language-specific conventions
3. Cross-language integration testing requirements
4. CI/CD unification needs
5. Developer experience consistency
6. Maintenance burden of multiple frameworks

### Decision

Implement a **layered testing architecture** with:

1. **Language-Native Core** - Each language uses its idiomatic testing framework
   - Rust: Built-in test harness + Nextest runner
   - Python: pytest with custom plugins
   - Go: Standard testing package + testify

2. **Shared Patterns Layer** - Common testing patterns abstracted
   - Test fixtures and builders (language-specific implementations)
   - Mocking patterns (trait-based in Rust, duck-typing in Python)
   - Assertion helpers (idiomatic per language)

3. **Integration Layer** - Cross-language coordination
   - Unified test result formats (JUnit XML)
   - Shared test data schemas
   - CI/CD integration helpers

4. **Tooling Layer** - Shared developer tools
   - Test discovery across languages
   - Coverage aggregation
   - Performance benchmarking

### Consequences

**Positive:**
- Developers use familiar, language-idiomatic testing
- No impedance mismatch from forcing one paradigm on all languages
- Each language can evolve its testing independently
- Shared infrastructure reduces duplication

**Negative:**
- More complex overall architecture
- Need expertise in multiple testing frameworks
- Cross-language integration requires careful coordination
- Documentation must cover multiple approaches

**Mitigations:**
- Comprehensive documentation with examples per language
- Shared CI/CD templates abstract language differences
- Regular architecture reviews ensure alignment

### Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| Single framework (Rust-based) | Uniformity | Poor DX for non-Rust devs | Rejected |
| Bazel with rules_* | Unified build/test | Steep learning curve, heavy | Rejected |
| Language-native + conventions | Best DX | Harder to enforce | **Accepted** |
| Wrapper around single runner | Simple architecture | Least common denominator | Rejected |

### Implementation

```
TestingKit/
├── rust/                          # Rust-specific testing
│   ├── phenotype-testing/         # Core utilities
│   ├── phenotype-mock/           # Mocking framework
│   ├── phenotype-test-fixtures/  # Test data
│   └── phenotype-test-infra/     # Integration infra
├── python/                        # Python-specific testing
│   ├── pheno-testing/            # Testing utilities
│   └── pheno-quality/            # Code quality
└── go/                           # Go-specific testing
    └── phenotype-testing/        # Testing utilities
```

### References

- [SOTA.md](./SOTA.md) - State-of-the-art research
- [SPEC.md](./SPEC.md) - Detailed specification
- [RFC-42: Cross-Language Testing](./rfcs/rfc-042-cross-lang-testing.md)

---

## ADR-002: Trait-Based Mocking for Rust Components

### Status
**Accepted** | 2026-04-05

### Context

Rust's ownership model and lack of reflection make traditional mocking approaches (dynamic proxy generation) impossible. Mocking in Rust requires compile-time code generation or manual trait implementations.

**Challenges:**
1. Mockall's `#[automock]` requires proc-macro expansion complexity
2. Mock verification is verbose
3. Async mocking adds complexity
4. Mock setup often duplicates test logic

**Forces:**
- Need for reliable, testable Rust code
- Developer experience of mocking setup
- Performance requirements (no runtime reflection)
- Type safety guarantees

### Decision

Implement **custom trait-based mocking** with the following design principles:

1. **Explicit Mock Context**
   ```rust
   pub struct MockContext {
       calls: Arc<Mutex<Vec<CallRecord>>>,
       expectations: Arc<Mutex<HashMap<String, Vec<Expectation>>>>,
   }
   ```

2. **Fluent Expectation API**
   ```rust
   ctx.expect("get_user")
       .with_args(vec!["123"])
       .returns(user_json)
       .times(1)
       .build();
   ```

3. **Automatic Call Recording**
   All mock methods automatically record calls for later verification

4. **Thread-Safe by Default**
   All mocks use Arc<Mutex<>> for thread-safe test execution

5. **Async Compatibility**
   Mocks work with async/await patterns

### Consequences

**Positive:**
- No proc-macro complexity
- Explicit control over mock behavior
- Thread-safe by design
- Minimal dependencies

**Negative:**
- More verbose than mockall
- Requires manual trait implementation
- No automatic mock generation

**Mitigations:**
- `mock_trait!` macro reduces boilerplate
- Documentation with common patterns
- IDE snippets for mock creation

### Implementation Example

```rust
// Define trait
pub trait UserRepository {
    async fn find_by_id(&self, id: UserId) -> Result<Option<User>, Error>;
    async fn save(&self, user: &User) -> Result<(), Error>;
}

// Create mock
mock_trait!(MockUserRepository for UserRepository {
    fn find_by_id(&self, id: UserId) -> Result<Option<User>, Error>;
    fn save(&self, user: &User) -> Result<(), Error>;
});

// Use in test
#[tokio::test]
async fn test_user_service() {
    let mut mock = MockUserRepository::new();
    
    mock.context()
        .expect("find_by_id")
        .with_args(vec!["123"])
        .returns(r#"{"id": "123", "name": "Alice"}"#)
        .build();
    
    let service = UserService::new(mock);
    let user = service.get_user("123").await.unwrap();
    
    assert_eq!(user.name, "Alice");
    mock.context().verify_called("find_by_id");
}
```

### References

- [phenotype-mock/src/lib.rs](./rust/phenotype-mock/src/lib.rs)
- Mockall documentation (comparison)
- [Rust Testing Guide](./docs/rust-testing-guide.md)

---

## ADR-003: Code Quality Analysis Integration

### Status
**Accepted** | 2026-04-05

### Context

Code quality analysis (detecting code smells, anti-patterns) is typically performed by separate tools (Pylint, Clippy, SonarQube) that run outside the test suite. This creates:

1. Delayed feedback (run in CI, not locally)
2. Different toolchains for testing vs. quality
3. Hard to enforce quality gates
4. Difficult to track quality trends

**Forces:**
- Need fast feedback on code quality
- Consistent quality standards across projects
- Integration with existing testing workflows
- Minimal developer friction

### Decision

Integrate **code quality analysis as a first-class testing concern** with:

1. **Quality as Tests**
   Code quality checks run as part of the test suite, not separate tools

2. **Configurable Rules Engine**
   ```python
   detector = CodeSmellDetector(rules=[
       GodObjectRule(max_methods=20),
       FeatureEnvyRule(threshold=0.7),
   ])
   ```

3. **Multiple Detection Strategies**
   - AST-based pattern detection
   - Semantic analysis
   - Architectural constraint validation
   - Custom rule support

4. **Integration Points**
   - pytest plugin for Python
   - Custom test harness for Rust
   - CI/CD reporting integration

### Quality Categories

| Category | Rules | Severity |
|----------|-------|----------|
| Code Smells | 10+ | Warning/Error |
| Architectural | 6 | Error |
| Security | TBD | Error |
| Performance | TBD | Warning |

### Consequences

**Positive:**
- Immediate quality feedback during development
- Quality gates enforced in CI
- Unified toolchain (test + quality)
- Trend tracking over time

**Negative:**
- Slower test execution
- Potential false positives
- Requires rule tuning per project

**Mitigations:**
- Caching of analysis results
- Configurable rule severity
- Baseline establishment for existing code
- Automatic exemption for legacy code

### Implementation

```python
# pytest.ini
[pytest]
quality_rules = pheno_quality.rules.STANDARD
quality_fail_on = error
quality_warn_on = warning

# Test with quality checks
pytest --quality

# Quality-only run
pytest --quality-only
```

### References

- [pheno-quality documentation](./python/pheno-quality/README.md)
- [SonarQube Quality Profiles](https://docs.sonarqube.org/latest/)
- [Martin Fowler: Code Smells](https://martinfowler.com/bliki/CodeSmell.html)

---

## ADR Index

| ID | Title | Status | Date |
|----|-------|--------|------|
| 001 | Multi-Language Testing Framework Architecture | Accepted | 2026-04-05 |
| 002 | Trait-Based Mocking for Rust Components | Accepted | 2026-04-05 |
| 003 | Code Quality Analysis Integration | Accepted | 2026-04-05 |

---

## ADR Process

### Creating New ADRs

1. Create file: `ADR-XXX-{short-title}.md`
2. Use template below
3. Submit PR for review
4. Update index

### ADR Template

```markdown
## ADR-XXX: Title

### Status
Proposed | Accepted | Deprecated | Superseded by ADR-YYY

### Context
Problem statement and forces

### Decision
What was decided

### Consequences
Positive, negative, mitigations

### Alternatives Considered
Table or list of alternatives

### Implementation
How to implement

### References
Related docs, issues, PRs
```

---

*End of Architecture Decision Records*
