# Functional Requirements — TestingKit

Traces to: PRD.md epics E1–E7.
ID format: FR-TESTINGKIT-{NNN}.

---

## Test Framework & Assertions

**FR-TESTINGKIT-001**: The system SHALL provide assertion macros with helpful failure messages that include diffs for complex types.
Traces to: E1.1

**FR-TESTINGKIT-002**: The system SHALL support snapshot testing with diff-on-change for verifying large outputs (API responses, generated code).
Traces to: E1.2

**FR-TESTINGKIT-003**: The system SHALL provide table-driven test helpers to reduce boilerplate for parametrized tests.
Traces to: E1.3

---

## Mocking & Doubles

**FR-TESTINGKIT-004**: The system SHALL provide mock object builders and spy helpers for testing interactions without external dependencies.
Traces to: E2.1

**FR-TESTINGKIT-005**: The system SHALL support property-based testing via generative test case generation.
Traces to: E2.2

---

## Test Data Builders

**FR-TESTINGKIT-006**: The system SHALL provide fluent builders for constructing complex test data with sensible defaults.
Traces to: E3.1

**FR-TESTINGKIT-007**: The system SHALL support fake implementations of services for testing in isolation.
Traces to: E3.2

---

## Trace & Test Guidance

All tests MUST reference a Functional Requirement (FR):

```rust
// Traces to: FR-TESTINGKIT-NNN
#[test]
fn test_assertion_macros() { ... }
```
