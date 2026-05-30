# Architecture Decision Records (ADR)

> **Project:** McpKit  
> **Status:** Active  
> **Last Updated:** 2024

---

## 1. Introduction

### What are ADRs?

Architecture Decision Records (ADRs) capture important architectural decisions made during the development of McpKit. Each ADR describes:

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
| 001 | [MCP Protocol Implementation](adrs/001-mcp-protocol.md) | ✅ Accepted | 2024-Q1 | Team | #mcp #protocol |
| 002 | [JSON-RPC Transport](adrs/002-json-rpc.md) | ✅ Accepted | 2024-Q1 | Core Team | #transport #jsonrpc |
| 003 | [Server Architecture](adrs/003-server-arch.md) | ✅ Accepted | 2024-Q1 | Core Team | #server #architecture |
| 004 | [Tool Registration](adrs/004-tool-registration.md) | ✅ Accepted | 2024-Q2 | Architecture | #tools #registration |
| 005 | [Capability Negotiation](adrs/005-capabilities.md) | ✅ Accepted | 2024-Q2 | Core Team | #capabilities #negotiation |
| 006 | [Resource Management](adrs/006-resources.md) | ✅ Accepted | 2024-Q2 | Core Team | #resources #templates |
| 007 | [Prompt Handling](adrs/007-prompts.md) | ✅ Accepted | 2024-Q2 | Core Team | #prompts #llm |
| 008 | [Type-Safe Bindings](adrs/008-type-bindings.md) | ✅ Accepted | 2024-Q3 | Core Team | #types #safety |
| 009 | [Multi-Language Support](adrs/009-multilang.md) | ✅ Accepted | 2024-Q3 | Architecture | #languages #sdk |
| 010 | [Authentication Model](adrs/010-auth-model.md) | 📝 Proposed | 2024-Q4 | Security | #auth #security |

### Deprecated/Superseded

| ID | Title | Status | Superseded By |
|----|-------|--------|---------------|
| - | *No deprecated ADRs yet* | - | - |

---

## 3. Decision Drivers Summary

### Protocol Compliance
- Model Context Protocol specification
- Anthropic compatibility
- Standard method support
- Version negotiation

### Developer Experience
- Easy server creation
- Type-safe APIs
- Good documentation
- Clear error messages

### Performance
- Efficient JSON-RPC handling
- Streaming support
- Connection pooling
- Minimal overhead

### Extensibility
- Pluggable transports
- Middleware support
- Custom tool types
- Hook system

### Interoperability
- Multiple language SDKs
- Framework integration
- Tool marketplace
- Standard schemas

---

## 4. ADR Categories

### 🌐 Protocol (ADR-001 to ADR-010)
MCP protocol implementation decisions.

**Key Topics:**
- JSON-RPC methods
- Message formats
- Protocol versions
- Error handling

### 🛠️ Tools (ADR-011 to ADR-020)
Tool definition and registration.

**Key Topics:**
- Tool schemas
- Input validation
- Output formatting
- Tool discovery

### 📄 Resources (ADR-021 to ADR-030)
Resource management and templates.

**Key Topics:**
- Resource URIs
- Template parameters
- MIME types
- Content encoding

### 💬 Prompts (ADR-031 to ADR-040)
Prompt handling and management.

**Key Topics:**
- Prompt templates
- Arguments
- Descriptions
- Examples

### 🔌 Transport (ADR-041 to ADR-050)
Transport layer implementations.

**Key Topics:**
- stdio transport
- HTTP transport
- WebSocket support
- SSE streaming

### 🔒 Security (ADR-051 to ADR-060)
Security and authentication.

**Key Topics:**
- Authentication
- Authorization
- Token handling
- Rate limiting

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

### MCP ADR Template (for protocol decisions)

```markdown
# ADR-XXX: [Title]

- **Status**: Proposed
- **Date**: YYYY-MM-DD
- **Author**: [Name]
- **MCP Impact**: Protocol | Tool | Resource | Prompt

## Protocol Context

Relevant MCP specification section.

## Current Implementation

How McpKit currently handles this.

## Proposed Change

What will change in the implementation.

## Compatibility

MCP spec compliance and breaking changes.

## Example

```json
{
  "jsonrpc": "2.0",
  "method": "...",
  "params": {}
}
```

## Migration Guide

How users should update their code.
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
| **MCP** | Model Context Protocol |
| **JSON-RPC** | Remote Procedure Call using JSON |
| **stdio** | Standard input/output transport |
| **SSE** | Server-Sent Events |
| **Tool** | Callable function exposed via MCP |
| **Resource** | URI-addressable data |
| **Prompt** | Template for LLM interaction |
| **Capability** | Feature set negotiation |
| **Transport** | Communication channel |

---

## 9. Related Resources

- [Architecture Decision Records (ADR)](https://adr.github.io/)
- [Documenting Architecture Decisions](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [McpKit SPEC.md](./docs/SPEC.md)
- [McpKit README.md](./README.md)

---

## 10. Maintenance

**ADR Shepherd**: Core Team  
**Review Schedule**: Monthly  
**Last Full Review**: 2024-Q4

---

*This index is automatically updated. Please submit a PR to add new ADRs or update existing ones.*
