# McpKit Project Charter

**Document ID:** CHARTER-MCPKIT-001  
**Version:** 1.0.0  
**Status:** Active  
**Effective Date:** 2026-04-05  
**Last Updated:** 2026-04-05  

---

## Table of Contents

1. [Mission Statement](#1-mission-statement)
2. [Tenets](#2-tenets)
3. [Scope & Boundaries](#3-scope--boundaries)
4. [Target Users](#4-target-users)
5. [Success Criteria](#5-success-criteria)
6. [Governance Model](#6-governance-model)
7. [Charter Compliance Checklist](#7-charter-compliance-checklist)
8. [Decision Authority Levels](#8-decision-authority-levels)
9. [Appendices](#9-appendices)

---

## 1. Mission Statement

### 1.1 Primary Mission

**McpKit is the Model Context Protocol (MCP) implementation toolkit for the Phenotype ecosystem, providing servers, clients, and framework components that enable seamless AI agent integration across all Phenotype services.**

Our mission is to standardize AI agent communication by offering:
- **MCP Servers**: Expose tools, resources, and prompts to AI agents
- **MCP Clients**: Connect to and orchestrate multiple MCP servers
- **Framework Components**: Reusable building blocks for MCP implementations
- **Tool Registry**: Discoverable, type-safe tool definitions

### 1.2 Vision

To become the standard MCP toolkit where:
- **Every Service is Agent-Ready**: MCP server auto-generated or easily added
- **Agents Orchestrate Everything**: Seamless multi-service agent workflows
- **Tools are Discoverable**: Registry-based tool discovery with type safety
- **Context is Rich**: Full project context available to AI agents

### 1.3 Strategic Objectives

| Objective | Target | Timeline |
|-----------|--------|----------|
| MCP server coverage | 100% core services | 2026-Q3 |
| Tool registry entries | 100+ tools | 2026-Q3 |
| Multi-language support | Rust, Python, TypeScript | 2026-Q2 |
| Agent success rate | >80% first-attempt | 2026-Q3 |

### 1.4 Value Proposition

```
┌─────────────────────────────────────────────────────────────────────┐
│                    McpKit Value Proposition                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FOR SERVICE DEVELOPERS:                                            │
│  • Auto-generated MCP servers from service definitions              │
│  • Type-safe tool definitions                                       │
│  • Context injection for AI agents                                  │
│  • Seamless integration with existing services                        │
│                                                                     │
│  FOR AI AGENTS:                                                     │
│  • Rich context about project structure                             │
│  • Discoverable tools with schemas                                  │
│  • Standardized communication patterns                              │
│  • Multi-service orchestration                                      │
│                                                                     │
│  FOR PLATFORM TEAMS:                                                │
│  • Standardized AI integration pattern                                │
│  • Security boundary enforcement                                      │
│  • Audit logging of agent actions                                   │
│  • Centralized tool registry                                          │
│                                                                     │
│  FOR PRODUCTIVITY:                                                  │
│  • AI agents handle repetitive tasks                                │
│  • Complex operations via natural language                          │
│  • Cross-service automation                                         │
│  • Self-documenting APIs                                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Tenets

### 2.1 Protocol Compliant

**Strict adherence to MCP specification.**

- Full MCP protocol support
- Pass official compliance tests
- Track protocol versions
- Compatibility layers for version mismatches

### 2.2 Type-Safe Tools

**Tool definitions are strongly typed.**

- JSON Schema for all tool inputs/outputs
- Generated type definitions
- Runtime validation
- IDE support for tool development

### 2.3 Auto-Discoverable

**Services expose capabilities automatically.**

- Server capability advertisement
- Tool registry with metadata
- Resource listing and subscriptions
- Prompt templates discoverable

### 2.4 Multi-Transport

**Support multiple communication transports.**

- stdio for local processes
- HTTP/SSE for remote servers
- WebSockets for bidirectional
- Unix sockets for local-only

### 2.5 Context-Rich

**Provide maximum context to agents.**

- Project structure exposure
- Code indexing and search
- Configuration access
- Runtime state visibility

### 2.6 Secure by Default

**Security boundaries are enforced.**

- Explicit capability grants
- Request validation
- Audit logging
- Rate limiting

---

## 3. Scope & Boundaries

### 3.1 In Scope

| Domain | Components | Priority |
|--------|------------|----------|
| **MCP Servers** | phenotype-mcp-core, phenotype-mcp-framework | P0 |
| **MCP Clients** | Client libraries, connection management | P0 |
| **Tool Registry** | Registry service, tool discovery | P0 |
| **Framework** | Server framework, middleware | P1 |
| **Asset Management** | phenotype-mcp-asset for pack management | P1 |

### 3.2 Out of Scope (Explicitly)

| Capability | Reason | Alternative |
|------------|--------|-------------|
| **LLM implementation** | Use specialized LLMs | Use Claude, GPT, etc. |
| **General AI framework** | Too broad | Use LangChain, etc. |
| **Vector database** | Specialized domain | Use pgvector, Pinecone |
| **Training/fine-tuning** | ML pipeline concern | Use HuggingFace, etc. |

### 3.3 Component Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      McpKit Architecture                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    MCP Clients                                │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐                │   │
│  │  │  Claude   │  │  Codex    │  │  Custom   │                │   │
│  │  │  Code     │  │  CLI      │  │  Agents   │                │   │
│  │  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘                │   │
│  │        └──────────────┼──────────────┘                     │   │
│  └───────────────────────│─────────────────────────────────────┘   │
│                        │                                           │
│  ┌─────────────────────▼───────────────────────────────────────┐   │
│  │                  MCP Protocol Layer                           │   │
│  │         (JSON-RPC, Tools, Resources, Prompts)                 │   │
│  └─────────────────────┬───────────────────────────────────────┘   │
│                        │                                           │
│  ┌─────────────────────▼───────────────────────────────────────┐   │
│  │                    MCP Servers                                │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │   │
│  │  │  Core    │ │ Framework│ │  Asset   │ │  Agent   │        │   │
│  │  │  Server  │ │  Server  │ │  Server  │ │  Server  │        │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Tool Registry                              │   │
│  │           (Discovery, Metadata, Type Registry)                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Target Users

### 4.1 Primary Personas

#### Persona 1: Service Developer (Marcus)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Persona: Marcus - Service Developer                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Role: Building services that need AI agent integration             │
│  Stack: Rust, async/await                                           │
│                                                                     │
│  Pain Points:                                                       │
│    • Need to expose service to AI agents                            │
│    • Complex protocol implementation                                │
│    • Type-safe tool definitions are tedious                         │
│    • Testing MCP servers is difficult                               │
│                                                                     │
│  McpKit Value:                                                      │
│    • Derive macros for MCP server creation                          │
│    • Auto-generated schemas from Rust types                         │
│    • Built-in testing utilities                                     │
│    • Framework handles protocol details                             │
│                                                                     │
│  Success Metric: MCP server running in <1 hour                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Persona 2: AI Agent Developer (Ada)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Persona: Ada - AI Agent Developer                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Role: Building AI agents that orchestrate multiple services        │
│  Stack: Python, TypeScript, LLM APIs                                │
│                                                                     │
│  Pain Points:                                                       │
│    • Discovering available tools is hard                            │
│    • Different APIs for each service                                │
│    • Context about projects is limited                              │
│    • Debugging agent behavior is difficult                          │
│                                                                     │
│  McpKit Value:                                                      │
│    • Centralized tool registry                                      │
│    • Standard MCP protocol across all services                      │
│    │  Project context via resources                                 │
│    │  Observability and logging                                     │
│    │                                                                 │
│    │  Success Metric: 80%+ first-attempt tool calls                 │
│    │                                                                 │
│    └─────────────────────────────────────────────────────────────────┘
```

### 4.2 Secondary Users

| User Type | Needs | McpKit Support |
|-----------|-------|----------------|
| **DevOps Engineer** | Deploy MCP servers | Container templates, K8s configs |
| **Security Engineer** | Audit agent actions | Comprehensive logging, access control |
| **Platform Architect** | Standardize AI integration | Framework, best practices |

---

## 5. Success Criteria

### 5.1 Protocol Metrics

| Metric | Target | Measurement | Frequency |
|--------|--------|-------------|-----------|
| **MCP compliance** | 100% | Official tests | CI/CD |
| **Protocol latency** | <100ms | Benchmark | CI/CD |
| **Tool call success** | >80% | Runtime metrics | Continuous |
| **Server availability** | 99.9% | Health checks | Continuous |

### 5.2 Adoption Metrics

| Metric | Target | Timeline |
|--------|--------|----------|
| Services with MCP | 100% core | 2026-Q3 |
| Tool registry size | 100+ tools | 2026-Q3 |
| Agent success rate | >80% | 2026-Q3 |
| Developer setup time | <1 hour | 2026-Q2 |

### 5.3 Quality Gates

```
┌─────────────────────────────────────────────────────────────────────┐
│  MCP Quality Gates                                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FOR MCP SERVERS:                                                     │
│  ├── Pass official MCP compliance tests                             │
│  ├── All tools have JSON schemas                                    │
│  ├── Schema validation tests pass                                   │
│  └── Security review for exposed capabilities                       │
│                                                                     │
│  FOR TOOL REGISTRY:                                                   │
│  ├── All tools have metadata                                        │
│  ├── Type safety verified                                           │
│  └── Discovery API tested                                           │
│                                                                     │
│  FOR CLIENT CHANGES:                                                  │
│  ├── Multi-server orchestration tested                              │
│  ├── Error handling verified                                        │
│  └── Timeout/retry logic validated                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6. Governance Model

### 6.1 Component Organization

```
McpKit/
├── rust/
│   ├── phenotype-mcp-core/        # Core MCP types and protocol
│   ├── phenotype-mcp-framework/ # Server framework
│   ├── phenotype-mcp-asset/     # Asset management server
│   └── agentkit/                  # Agent framework
├── python/
│   └── pheno-mcp/                 # Python MCP client/server
└── typescript/
    └── (planned)
```

### 6.2 Protocol Governance

**MCP Spec Updates:**
- Track official MCP specification
- Version compatibility matrix
- Migration guides for spec changes
- Deprecation policy for old versions

### 6.3 Integration Points

| Consumer | Integration | Stability |
|----------|-------------|-----------|
| **AgilePlus** | Agent dispatch via MCP | Development |
| **PhenoAgent** | Agent framework | Development |
| **All Services** | MCP server exposure | Development |
| **Claude Code** | Client integration | Stable |

---

## 7. Charter Compliance Checklist

### 7.1 Compliance Requirements

| Requirement | Evidence | Status | Last Verified |
|------------|----------|--------|---------------|
| **MCP compliance** | Test results | ⬜ | Pending verification |
| **Tool registry** | Registry service | ⬜ | Pending verification |
| **Type safety** | Schema validation | ⬜ | Pending verification |
| **Multi-transport** | stdio, HTTP, WS | ⬜ | Pending verification |
| **Security audit** | Review complete | ⬜ | Pending verification |

### 7.2 Charter Amendment Process

| Amendment Type | Approval Required | Process |
|---------------|-------------------|---------|
| **Protocol changes** | Core Team | RFC → Review → Implementation |
| **New server types** | Core Team | PR → Review → Merge |

---

## 8. Decision Authority Levels

### 8.1 Authority Matrix

```
┌─────────────────────────────────────────────────────────────────────┐
│  Decision Authority Matrix (RACI)                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  MCP DECISIONS:                                                       │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ Decision              │ R        │ A       │ C        │ I      │ │
│  ├───────────────────────┼──────────┼─────────┼──────────┼────────┤ │
│  │ Protocol implementation│ Core    │ Core    │ MCP      │ All    │ │
│  │                       │ Team     │ Team    │ Spec     │ Devs   │ │
│  ├───────────────────────┼──────────┼─────────┼──────────┼────────┤ │
│  │ Tool registry schema  │ Core     │ Core    │ Users    │ All    │ │
│  │                       │ Team     │ Team    │          │ Devs   │ │
│  ├───────────────────────┼──────────┼─────────┼──────────┼────────┤ │
│  │ Server framework API  │ Core     │ Core    │ Service  │ All    │ │
│  │                       │ Team     │ Team    │ Devs     │ Devs   │ │
│  ├───────────────────────┼──────────┼─────────┼──────────┼────────┤ │
│  │ Security policies     │ Core     │ Security│ All      │ All    │ │
│  │                       │ Team     │ Team    │          │ Devs   │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 9. Appendices

### 9.1 Glossary

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol |
| **Tool** | Callable function exposed to AI |
| **Resource** | Readable data source |
| **Prompt** | Template for AI interaction |
| **Server** | MCP-capable service |
| **Client** | AI agent connecting to servers |

### 9.2 Related Documents

| Document | Location | Purpose |
|----------|----------|---------|
| MCP Spec | External | Protocol specification |
| Server Guide | docs/servers/ | Building MCP servers |
| Client Guide | docs/clients/ | Using MCP clients |

### 9.3 Charter Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-05 | McpKit Team | Initial charter |

### 9.4 Ratification

This charter is ratified by:

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Core Team Lead | Unassigned | 2026-04-05 | ✓ |
| AI Platform Lead | Unassigned | 2026-04-05 | ✓ |

---

**END OF CHARTER**

*This document is a living charter. It should be reviewed quarterly and updated as the project evolves while maintaining alignment with the core mission and tenets.*
