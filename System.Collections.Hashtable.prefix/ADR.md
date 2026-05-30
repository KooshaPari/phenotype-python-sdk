# Architecture Decision Records (ADR)

> **Project:** ResilienceKit  
> **Status:** Active  
> **Last Updated:** 2024

---

## 1. Introduction

### What are ADRs?

Architecture Decision Records (ADRs) capture important architectural decisions made during the development of ResilienceKit. Each ADR describes:

- **Context**: The situation that requires a decision
- **Problem**: The specific challenge or question to address
- **Decision**: The chosen approach
- **Consequences**: The outcomes, both positive and negative
- **Status**: Current state (proposed, accepted, deprecated, superseded)

### Why ADRs Matter

1. **Knowledge Preservation**: Document reasoning that might otherwise be lost
2. **Onboarding**: Help new team members understand system design
3. **Transparency**: Make decision-making visible to stakeholders
4. **Consistency**: Guide future decisions with historical context
5. **Accountability**: Track who made decisions and when

### ADR Lifecycle

```
Proposed → Accepted → [Deprecated] → Superseded
              ↓
           Rejected
```

- **Proposed**: ADR is submitted for review
- **Accepted**: Decision is ratified by team consensus
- **Rejected**: Decision is declined
- **Deprecated**: Decision is no longer relevant
- **Superseded**: Decision has been replaced by a newer ADR

---

## 2. ADR Index

### Active Decisions

| ID | Title | Status | Date | Author | Tags |
|----|-------|--------|------|--------|------|
| 001 | [Monorepo Structure](adrs/001-monorepo-structure.md) | ✅ Accepted | 2024-Q1 | Team | #organization |
| 002 | [Rust as Primary Language](adrs/002-rust-primary-language.md) | ✅ Accepted | 2024-Q1 | Core Team | #language #performance |
| 003 | [Async Runtime Selection](adrs/003-async-runtime.md) | ✅ Accepted | 2024-Q1 | Core Team | #async #runtime |
| 004 | [Error Handling Strategy](adrs/004-error-handling.md) | ✅ Accepted | 2024-Q1 | Core Team | #errors #thiserror |
| 005 | [Circuit Breaker Pattern](adrs/005-circuit-breaker.md) | ✅ Accepted | 2024-Q2 | Architecture | #resilience #patterns |
| 006 | [Retry Policy Configuration](adrs/006-retry-policy.md) | ✅ Accepted | 2024-Q2 | Core Team | #resilience #config |
| 007 | [Bulkhead Isolation](adrs/007-bulkhead-isolation.md) | ✅ Accepted | 2024-Q2 | Architecture | #resilience #concurrency |
| 008 | [Timeout Management](adrs/008-timeout-management.md) | ✅ Accepted | 2024-Q2 | Core Team | #resilience #performance |
| 009 | [Metrics and Observability](adrs/009-metrics-observability.md) | ✅ Accepted | 2024-Q3 | Observability | #metrics #tracing |
| 010 | [Plugin Architecture](adrs/010-plugin-architecture.md) | 📝 Proposed | 2024-Q4 | Architecture | #extensibility |

### Deprecated/Superseded

| ID | Title | Status | Superseded By |
|----|-------|--------|---------------|
| - | *No deprecated ADRs yet* | - | - |

---

## 3. Decision Drivers Summary

### Performance & Scalability
- Low latency requirements (< 1ms overhead)
- High throughput support (100K+ req/s)
- Minimal memory footprint

### Reliability & Resilience
- Fault tolerance mechanisms
- Graceful degradation strategies
- Self-healing capabilities

### Maintainability
- Clear, readable code
- Comprehensive test coverage
- Well-documented APIs

### Ecosystem Compatibility
- Integration with existing Phenotype systems
- Support for multiple async runtimes
- Language interoperability (FFI)

### Operational Excellence
- Observable behavior
- Configurable without redeployment
- Zero-downtime updates

---

## 4. ADR Categories

### 🏗️ Architecture (ADR-001 to ADR-010)
High-level structural decisions affecting the entire codebase.

**Key Topics:**
- Code organization
- Module boundaries
- API design
- Data flow

### 🔧 Implementation (ADR-011 to ADR-020)
Specific implementation choices and technical approaches.

**Key Topics:**
- Algorithm selection
- Data structures
- Library choices
- Performance optimizations

### 🔌 Integration (ADR-021 to ADR-030)
Decisions about external dependencies and system integration.

**Key Topics:**
- Third-party libraries
- Service communication
- Protocol selection
- Compatibility layers

### 📊 Observability (ADR-031 to ADR-040)
Decisions related to monitoring, logging, and debugging.

**Key Topics:**
- Metrics collection
- Tracing strategies
- Alert thresholds
- Dashboard design

### 🔒 Security (ADR-041 to ADR-050)
Security-related architectural decisions.

**Key Topics:**
- Authentication mechanisms
- Authorization patterns
- Data protection
- Audit logging

### 🚀 Operations (ADR-051 to ADR-060)
Deployment, configuration, and operational decisions.

**Key Topics:**
- CI/CD pipelines
- Configuration management
- Feature flags
- Rollout strategies

---

## 5. How to Contribute New ADRs

### Before Writing an ADR

1. **Discuss First**: Open a GitHub issue or discussion to gauge interest
2. **Check Existing**: Ensure no existing ADR covers the same decision
3. **Gather Context**: Collect requirements, constraints, and options

### Writing Process

1. **Use the Template**: Copy from [templates/adr-template.md](templates/adr-template.md)
2. **Be Concise**: Focus on the decision and its context
3. **Include Options**: Document alternatives considered
4. **Be Honest**: Acknowledge trade-offs and negative consequences

### Submission Checklist

- [ ] Uses the standard ADR template
- [ ] Assigned a sequential ID
- [ ] Status set to "Proposed"
- [ ] All sections completed
- [ ] Linked in the index above
- [ ] PR submitted with clear description

### Review Process

```
1. Author submits PR with ADR in "Proposed" status
2. Maintainers review within 5 business days
3. Community feedback period (3 days minimum)
4. Decision: Accept, Request Changes, or Reject
5. If accepted, merge and update index
```

### ADR Format Requirements

**File Naming**: `XXX-descriptive-title.md`
- Three-digit sequential number (001, 002, etc.)
- Lowercase words separated by hyphens
- Place in `adrs/` directory

**Required Sections**:
1. Title and metadata
2. Context
3. Decision
4. Consequences
5. Status
6. References (optional)

---

## 6. Templates

### Standard ADR Template

```markdown
# ADR-XXX: [Title]

- **Status**: Proposed | Accepted | Rejected | Deprecated | Superseded by ADR-YYY
- **Date**: YYYY-MM-DD
- **Author**: [Name](mailto:email@example.com)
- **Tags**: #tag1 #tag2

## Context

What is the issue that we're seeing that is motivating this decision or change?

## Decision

What is the change that we're proposing or have agreed to implement?

## Consequences

What becomes easier or more difficult to do and any risks introduced by the change?

### Positive

- Benefit 1
- Benefit 2

### Negative

- Drawback 1
- Drawback 2

## Alternatives Considered

### Alternative A: [Name]

Description and why it was rejected.

### Alternative B: [Name]

Description and why it was rejected.

## References

- Link 1
- Link 2
```

### Lightweight ADR Template (for minor decisions)

```markdown
# ADR-XXX: [Title]

- **Status**: Accepted
- **Date**: YYYY-MM-DD
- **Author**: [Name]
- **Impact**: Low

## Decision

Brief description of the decision.

## Rationale

Why this decision was made.

## Consequences

- Impact 1
- Impact 2
```

### RFC-Style ADR Template (for major decisions)

```markdown
# ADR-XXX: [Title]

- **Status**: Proposed
- **Date**: YYYY-MM-DD
- **Author**: [Name]
- **Stakeholders**: @person1, @person2

## Summary

One paragraph explanation of the proposal.

## Motivation

Why are we doing this? What use cases does it support? What is the expected outcome?

## Detailed Design

Technical details of the proposed solution.

## Drawbacks

Why might this be a bad idea?

## Alternatives

What other approaches were considered?

## Adoption Plan

How will this be rolled out?

## Unresolved Questions

What needs to be resolved before acceptance?
```

---

## 7. Best Practices

### Do's

✅ **Focus on decisions, not just documentation**  
ADRs record why we chose a particular approach, not just what the approach is.

✅ **Write them when the decision is fresh**  
Capture context while it's still in recent memory.

✅ **Include the "why"**  
Explain the reasoning behind the decision, not just the outcome.

✅ **Be honest about trade-offs**  
Every decision has downsides. Acknowledge them.

✅ **Keep them immutable once accepted**  
Don't edit accepted ADRs; supersede them with new ones instead.

✅ **Make them discoverable**  
Link from README, index, and relevant code comments.

### Don'ts

❌ **Don't use ADRs for trivial decisions**  
Not every code change needs an ADR. Reserve them for significant architectural choices.

❌ **Don't let them become outdated**  
Update the status when decisions change.

❌ **Don't write them in isolation**  
Discuss significant decisions with the team before documenting.

❌ **Don't make them overly long**  
Aim for 1-2 pages. Longer ADRs may indicate scope creep.

---

## 8. Glossary

| Term | Definition |
|------|------------|
| **ADR** | Architecture Decision Record |
| **RFC** | Request for Comments |
| **Circuit Breaker** | Pattern to prevent cascade failures |
| **Bulkhead** | Pattern to isolate failures |
| **FFI** | Foreign Function Interface |
| **WASM** | WebAssembly |

---

## 9. Related Resources

- [Architecture Decision Records (ADR)](https://adr.github.io/)
- [Documenting Architecture Decisions](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions)
- [ResilienceKit SPEC.md](./SPEC.md)
- [ResilienceKit README.md](./README.md)

---

## 10. Maintenance

**ADR Shepherd**: Core Team  
**Review Schedule**: Monthly  
**Last Full Review**: 2024-Q4

---

*This index is automatically updated. Please submit a PR to add new ADRs or update existing ones.*
