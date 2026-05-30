# McpKit Specification

**Document ID:** PHENOTYPE_MCPKIT_SPEC_001  
**Status:** Active  
**Last Updated:** 2026-04-03  
**Author:** Phenotype Architecture Team

---

## Table of Contents

1. [Project Overview](#1-project-overview)
   - 1.1 Purpose and Scope
   - 1.2 Target Audience
   - 1.3 Protocol Version
   - 1.4 Terminology
   - 1.5 Design Principles
2. [Architecture](#2-architecture)
   - 2.1 System Components
   - 2.2 Multi-Language SDK Architecture
   - 2.3 Component Interaction Model
   - 2.4 Deployment Topologies
   - 2.5 Data Flow Architecture
3. [Functionality Specification](#3-functionality-specification)
   - 3.1 Lifecycle Management
   - 3.2 Tool System
   - 3.3 Resource System
   - 3.4 Prompt System
   - 3.5 Sampling System
   - 3.6 Notification System
   - 3.7 Root Management
4. [Technical Architecture](#4-technical-architecture)
   - 4.1 Protocol Stack
   - 4.2 Transport Layer
   - 4.3 Message Layer
   - 4.4 Server Architecture
   - 4.5 Client Architecture
5. [API Reference](#5-api-reference)
   - 5.1 Python SDK API
   - 5.2 Go SDK API
   - 5.3 TypeScript SDK API
   - 5.4 Rust Types API
6. [Error Handling](#6-error-handling)
   - 6.1 Error Classification
   - 6.2 Error Codes
   - 6.3 Error Response Format
   - 6.4 Error Recovery Strategies
7. [Security](#7-security)
   - 7.1 Threat Model
   - 7.2 Authentication
   - 7.3 Authorization
   - 7.4 Input Validation
   - 7.5 Sandboxing
   - 7.6 Transport Security
8. [Testing and Quality Assurance](#8-testing-and-quality-assurance)
   - 8.1 Test Strategy
   - 8.2 Test Categories
   - 8.3 McpKit QA Framework
   - 8.4 Protocol Compliance Testing
9. [Performance](#9-performance)
   - 9.1 Performance Requirements
   - 9.2 Benchmarking
   - 9.3 Optimization Strategies
10. [Configuration](#10-configuration)
    - 10.1 Server Configuration
    - 10.2 Transport Configuration
    - 10.3 Tool Registry Configuration
    - 10.4 Environment Variables
11. [Deployment](#11-deployment)
    - 11.1 Local Deployment
    - 11.2 Remote Deployment
    - 11.3 Container Deployment
    - 11.4 Kubernetes Deployment
12. [Integration](#12-integration)
    - 12.1 Phenotype Ecosystem Integration
    - 12.2 Agent Framework Adapters
    - 12.3 External Service Integration
13. [Governance](#13-governance)
    - 13.1 Versioning Policy
    - 13.2 Deprecation Policy
    - 13.3 Change Management
14. [Appendices](#14-appendices)
    - A. Protocol Method Reference
    - B. Type Definitions
    - C. Configuration Reference
    - D. Glossary

---

## 1. Project Overview

### 1.1 Purpose and Scope

McpKit is a multi-language Model Context Protocol (MCP) toolkit for the Phenotype ecosystem. It provides standardized AI-to-tool communication across Python, Go, TypeScript, and Rust implementations, enabling AI agents to discover, invoke, and manage tools, resources, and prompts through a unified protocol interface.

**Scope:**

- **Protocol Implementation**: Full MCP protocol compliance across all supported languages
- **SDK Development**: High-level APIs for building MCP servers and clients
- **Tool Management**: Declarative and programmatic tool registration with YAML-based configuration
- **Resource Management**: URI-based resource access with scheme-based providers
- **Prompt Management**: Template-based prompt generation with argument support
- **Transport Abstraction**: Unified transport interface supporting SSE and stdio
- **Quality Assurance**: Comprehensive testing framework for protocol compliance
- **Agent Integration**: Adapters for LangGraph, CrewAI, and AutoGen frameworks

**Out of Scope:**

- LLM model implementation or inference
- AI agent orchestration (provided by adapters, not core)
- Database management systems
- External API implementations

### 1.2 Target Audience

| Audience | Use Case | Relevant Sections |
|----------|----------|-------------------|
| SDK Developers | Building MCP servers/clients | API Reference, Technical Architecture |
| Tool Developers | Creating MCP tools | Tool System, API Reference |
| Operations Teams | Deploying MCP servers | Deployment, Configuration |
| Security Teams | Auditing MCP implementations | Security, Error Handling |
| QA Engineers | Testing protocol compliance | Testing and Quality Assurance |
| AI Engineers | Integrating with agent frameworks | Integration, Agent Adapters |

### 1.3 Protocol Version

| Component | Version | Notes |
|-----------|---------|-------|
| MCP Protocol | 2024-11-05 | Current stable |
| JSON-RPC | 2.0 | Foundation protocol |
| JSON Schema | Draft 7 | Input validation |
| SSE | WHATWG Living Standard | Transport layer |

### 1.4 Terminology

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - standardized AI-to-tool communication |
| **Host** | Application that initiates MCP connections (Claude Desktop, IDE) |
| **Client** | Protocol client within the host managing connections |
| **Server** | External process providing tools, resources, prompts |
| **Tool** | Executable function exposed to AI clients |
| **Resource** | Data source accessible via URI |
| **Prompt** | Template for generating LLM prompts with arguments |
| **Transport** | Communication channel (SSE or stdio) |
| **Capability** | Feature set advertised during initialization |
| **Notification** | Fire-and-forget protocol message |
| **Sampling** | Server-initiated LLM generation request |
| **Root** | Client-exposed filesystem or data root |

### 1.5 Design Principles

1. **Protocol First**: All implementations conform to the MCP specification; no deviations
2. **Transport Agnostic**: Core logic is independent of transport mechanism
3. **Multi-Language Consistency**: Equivalent APIs across Python, Go, TypeScript, Rust
4. **Developer Experience**: Intuitive APIs with minimal boilerplate
5. **Operational Flexibility**: Configuration-driven tool management without code changes
6. **Security by Default**: Input validation, sandboxing, and authentication built-in
7. **Extensibility**: Plugin architecture for custom transports, tools, and resources
8. **Testability**: Comprehensive testing framework with protocol compliance verification

---

## 2. Architecture

### 2.1 System Components

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              McpKit Architecture                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                          Language SDKs                                   │  │
│  │                                                                         │  │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐   │  │
│  │  │  Python SDK      │  │  Go SDK          │  │  TypeScript SDK      │   │  │
│  │  │  (pheno-mcp)     │  │  (mcpkit-go)     │  │  (mcpkit-ts)         │   │  │
│  │  │                  │  │                  │  │                      │   │  │
│  │  │  • FastMCP API   │  │  • Server        │  │  • Server            │   │  │
│  │  │  • Decorators    │  │  • Client        │  │  • Client            │   │  │
│  │  │  • Tool Registry │  │  • Tool Registry │  │  • Tool Registry     │   │  │
│  │  │  • Resources     │  │  • Resources     │  │  • Resources         │   │  │
│  │  │  • Prompts       │  │  • Prompts       │  │  • Prompts           │   │  │
│  │  │  • Agent Adapters│  │  • Transports    │  │  • Transports        │   │  │
│  │  │  • QA Framework  │  │  • CLI           │  │  • Extensions        │   │  │
│  │  │  • Performance   │  │                  │  │                      │   │  │
│  │  │  • Workflow      │  │                  │  │                      │   │  │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────────┘   │  │
│  │  ┌──────────────────┐                                                    │  │
│  │  │  Rust Types      │                                                    │  │
│  │  │  (mcp-forge)     │                                                    │  │
│  │  │                  │                                                    │  │
│  │  │  • Protocol Types│                                                    │  │
│  │  │  • Type Generator│                                                    │  │
│  │  │  • LSP Protocol  │                                                    │  │
│  │  │  • Logging       │                                                    │  │
│  │  │  • Utilities     │                                                    │  │
│  │  └──────────────────┘                                                    │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                          Shared Components                               │  │
│  │                                                                         │  │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐   │  │
│  │  │  Registry        │  │  Resource Schemes│  │  Protocol Types      │   │  │
│  │  │  (YAML)          │  │  (Config)        │  │  (JSON Schema)       │   │  │
│  │  │                  │  │                  │  │                      │   │  │
│  │  │  • Tool catalog  │  │  • File scheme   │  │  • Request types     │   │  │
│  │  │  • Resource defs │  │  • Config scheme │  │  • Response types    │   │  │
│  │  │  • Prompt defs   │  │  • HTTP scheme   │  │  • Content types     │   │  │
│  │  │  • Workspace     │  │  • Logs scheme   │  │  • Error types       │   │  │
│  │  │    tracking      │  │  • Metrics scheme│  │  • Method enums      │   │  │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                          Transport Layer                                 │  │
│  │                                                                         │  │
│  │  ┌──────────────────────────┐        ┌──────────────────────────────┐    │  │
│  │  │  SSE Transport           │        │  stdio Transport             │    │  │
│  │  │                          │        │                              │    │  │
│  │  │  • HTTP server           │        │  • stdin binding             │    │  │
│  │  │  • Session management    │        │  • stdout binding            │    │  │
│  │  │  • Multi-client          │        │  • Line-based protocol       │    │  │
│  │  │  • CORS support          │        │  • Single client             │    │  │
│  │  └──────────────────────────┘        └──────────────────────────────┘    │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Multi-Language SDK Architecture

Each SDK follows a consistent layered architecture:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    SDK Layered Architecture (All Languages)                     │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │  Layer 4: High-Level API                                                 │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐  │  │
│  │  │  Decorator API  │  │  Builder API    │  │  Framework API          │  │  │
│  │  │  (Python)       │  │  (Go)           │  │  (TypeScript)           │  │  │
│  │  │                 │  │                 │  │                         │  │  │
│  │  │  @mcp.tool()    │  │  mcp.NewServer()│  │  new McpServer()        │  │  │
│  │  │  @mcp.resource()│  │  .WithTool()    │  │  .tool()                │  │  │
│  │  │  @mcp.prompt()  │  │  .WithResource()│  │  .resource()            │  │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │  Layer 3: Server Core                                                    │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐  │  │
│  │  │  Tool Registry  │  │  Resource Mgr   │  │  Prompt Manager         │  │  │
│  │  │                 │  │                 │  │                         │  │  │
│  │  │  • Register     │  │  • List         │  │  • Register             │  │  │
│  │  │  • Execute      │  │  • Read         │  │  • Render               │  │  │
│  │  │  • List         │  │  • Subscribe    │  │  • List                 │  │  │
│  │  │  • Notify       │  │  • Notify       │  │  • Notify               │  │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │  Layer 2: Protocol Handler                                               │  │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │  │
│  │  │  Protocol Router                                                   │  │  │
│  │  │                                                                   │  │  │
│  │  │  • initialize         → LifecycleHandler                          │  │  │
│  │  │  • tools/list         → ToolHandler.list()                        │  │  │
│  │  │  • tools/call         → ToolHandler.call()                        │  │  │
│  │  │  • resources/list     → ResourceHandler.list()                    │  │  │
│  │  │  • resources/read     → ResourceHandler.read()                    │  │  │
│  │  │  • prompts/list       → PromptHandler.list()                      │  │  │
│  │  │  • prompts/get        → PromptHandler.get()                       │  │  │
│  │  │  • sampling/*         → SamplingHandler                          │  │  │
│  │  │  • notifications/*    → NotificationRouter                       │  │  │
│  │  └───────────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │  Layer 1: Transport                                                      │  │
│  │  ┌─────────────────────────┐        ┌───────────────────────────────┐    │  │
│  │  │  StdioTransport         │        │  SSETransport                 │    │  │
│  │  │                         │        │                               │    │  │
│  │  │  connect()              │        │  connect()                    │    │  │
│  │  │  send(message)          │        │  send(message)                │    │  │
│  │  │  receive() → message    │        │  receive() → message          │    │  │
│  │  │  close()                │        │  close()                      │    │  │
│  │  └─────────────────────────┘        └───────────────────────────────┘    │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │  Layer 0: Generated Protocol Types                                       │  │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │  │
│  │  │  Request Types  │  Response Types  │  Content Types  │  Errors    │  │  │
│  │  │                 │                  │                 │            │  │  │
│  │  │  JsonRpcRequest │  JsonRpcResponse │  TextContent    │  McpError  │  │  │
│  │  │  InitializeReq  │  InitializeResp  │  ImageContent   │  ToolError │  │  │
│  │  │  ToolCallReq    │  ToolCallResp    │  ResourceContent│  ResError  │  │  │
│  │  └─────────────────┴──────────────────┴─────────────────┴────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Component Interaction Model

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    Component Interaction Flow                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  MCP Host                    McpKit Server                                    │
│  ┌──────────────┐            ┌─────────────────────────────────────────────┐  │
│  │              │            │                                             │  │
│  │  Client      │  Request   │  Transport                                  │  │
│  │  ┌────────┐  │───────────►│  ┌───────────┐                              │  │
│  │  │Message │  │  JSON-RPC │  │ Parse &    │                              │  │
│  │  │Builder │  │           │  │ Route      │                              │  │
│  │  └────────┘  │           │  └─────┬─────┘                              │  │
│  │       ▲      │           │        │                                     │  │
│  │       │      │  Response │        │                                     │  │
│  │  ┌────┴────┐ │◄──────────│        │                                     │  │
│  │  │Response │ │           │        ▼                                     │  │
│  │  │Parser   │ │           │  ┌─────────────┐                             │  │
│  │  └─────────┘ │           │  │ Protocol    │                             │  │
│  │              │           │  │ Router      │                             │  │
│  └──────────────┘           │  └──────┬──────┘                             │  │
│                             │         │                                     │  │
│                             │    ┌────┴────┬────────────┬──────────────┐    │  │
│                             │    ▼         ▼            ▼              ▼    │  │
│                             │  ┌──────┐ ┌───────┐ ┌────────┐ ┌──────────┐  │  │
│                             │  │Tools │ │Resrces│ │Prompts │ │ Sampling │  │  │
│                             │  │Reg   │ │Mgr    │ │Mgr     │ │ Handler  │  │  │
│                             │  └──────┘ └───────┘ └────────┘ └──────────┘  │  │
│                             │                                             │  │
│                             └─────────────────────────────────────────────┘  │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2.4 Deployment Topologies

#### 2.4.1 Local Process (stdio)

```
┌──────────────────────────────────────────────────────────────┐
│                    Local Process Deployment                    │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐         stdio          ┌──────────────┐     │
│  │  MCP Host    │◄──────────────────────►│  McpKit      │     │
│  │  (Claude)    │    stdin / stdout      │  Server      │     │
│  │              │                        │              │     │
│  │  Process     │    Spawn               │  Process     │     │
│  │  Manager     │───────────────────────►│  (Child)     │     │
│  └──────────────┘                        └──────────────┘     │
│                                                               │
│  Use Cases: IDE plugins, CLI tools, desktop applications      │
│  Security: Process isolation, no network exposure             │
│  Scaling: Single connection per server process                │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

#### 2.4.2 Remote Service (SSE)

```
┌──────────────────────────────────────────────────────────────┐
│                    Remote Service Deployment                   │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐  │
│  │ Client 1 │    │ Client 2 │    │ Client N │    │ Load   │  │
│  │          │    │          │    │          │    │ Balancer│  │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └───┬────┘  │
│       │               │               │               │       │
│       └───────────────┴───────────────┴───────────────┘       │
│                               │                               │
│                               ▼                               │
│                    ┌─────────────────────┐                    │
│                    │  McpKit Server      │                    │
│                    │                     │                    │
│                    │  • HTTP/SSE Server  │                    │
│                    │  • Session Manager  │                    │
│                    │  • Tool Registry    │                    │
│                    │  • Resource Manager │                    │
│                    └─────────────────────┘                    │
│                                                               │
│  Use Cases: Cloud services, multi-tenant platforms, APIs      │
│  Security: TLS, authentication tokens, rate limiting          │
│  Scaling: Horizontal scaling with session affinity            │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

#### 2.4.3 Hybrid Deployment

```
┌──────────────────────────────────────────────────────────────┐
│                    Hybrid Deployment                           │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐         stdio          ┌──────────────┐     │
│  │  IDE / CLI   │◄──────────────────────►│  Local       │     │
│  │  (stdio)     │                        │  McpKit      │     │
│  └──────────────┘                        └──────┬───────┘     │
│                                                 │             │
│                                                 │ SSE         │
│                                                 ▼             │
│                                        ┌──────────────┐       │
│                                        │  Remote      │       │
│                                        │  McpKit      │       │
│                                        │  Gateway     │       │
│                                        └──────┬───────┘       │
│                                               │               │
│                                    ┌──────────┼──────────┐    │
│                                    ▼          ▼          ▼    │
│                              ┌────────┐ ┌────────┐ ┌────────┐ │
│                              │ Tool   │ │Resource│ │External│ │
│                              │ Server │ │ Server │ │ APIs   │ │
│                              └────────┘ └────────┘ └────────┘ │
│                                                               │
│  Use Cases: Local dev with remote tool access                 │
│  Security: Local stdio + remote TLS                           │
│  Scaling: Local for dev, remote for production tools          │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### 2.5 Data Flow Architecture

#### 2.5.1 Tool Call Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    Tool Call Data Flow                                         │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  1. Client Request                                                            │
│     ┌─────────────────────────────────────────────────────────────────────┐    │
│     │  {                                                                  │    │
│     │    "jsonrpc": "2.0",                                                │    │
│     │    "id": 3,                                                         │    │
│     │    "method": "tools/call",                                          │    │
│     │    "params": {                                                      │    │
│     │      "name": "search_files",                                        │    │
│     │      "arguments": {                                                 │    │
│     │        "pattern": "*.py",                                           │    │
│     │        "directory": "/src"                                          │    │
│     │      }                                                              │    │
│     │    }                                                                │    │
│     │  }                                                                  │    │
│     └─────────────────────────────────────────────────────────────────────┘    │
│                               │                                               │
│  2. Transport Layer                                                           │
│     ┌─────────────────────────────────────────────────────────────────────┐    │
│     │  • Deserialize JSON-RPC message                                     │    │
│     │  • Validate message structure                                       │    │
│     │  • Route to protocol handler                                        │    │
│     └─────────────────────────────────────────────────────────────────────┘    │
│                               │                                               │
│  3. Protocol Router                                                           │
│     ┌─────────────────────────────────────────────────────────────────────┐    │
│     │  • Match method: "tools/call"                                       │    │
│     │  • Extract params: name, arguments                                  │    │
│     │  • Forward to Tool Registry                                         │    │
│     └─────────────────────────────────────────────────────────────────────┘    │
│                               │                                               │
│  4. Tool Registry                                                             │
│     ┌─────────────────────────────────────────────────────────────────────┐    │
│     │  • Lookup tool: "search_files"                                      │    │
│     │  • Validate arguments against input_schema                          │    │
│     │  • Resolve handler function                                         │    │
│     │  • Execute handler with arguments                                   │    │
│     └─────────────────────────────────────────────────────────────────────┘    │
│                               │                                               │
│  5. Tool Execution                                                            │
│     ┌─────────────────────────────────────────────────────────────────────┐    │
│     │  • Run search_files(pattern="*.py", directory="/src")               │    │
│     │  • Collect results                                                  │    │
│     │  • Format as ToolResult                                             │    │
│     └─────────────────────────────────────────────────────────────────────┘    │
│                               │                                               │
│  6. Response Construction                                                     │
│     ┌─────────────────────────────────────────────────────────────────────┐    │
│     │  {                                                                  │    │
│     │    "jsonrpc": "2.0",                                                │    │
│     │    "id": 3,                                                         │    │
│     │    "result": {                                                      │    │
│     │      "content": [                                                   │    │
│     │        { "type": "text", "text": "Found 42 files:\n..." }           │    │
│     │      ]                                                              │    │
│     │    }                                                                │    │
│     │  }                                                                  │    │
│     └─────────────────────────────────────────────────────────────────────┘    │
│                               │                                               │
│  7. Transport Response                                                          │
│     ┌─────────────────────────────────────────────────────────────────────┐    │
│     │  • Serialize response to JSON                                       │    │
│     │  • Send via transport (stdio/SSE)                                   │    │
│     │  • Client receives and processes                                    │    │
│     └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### 2.5.2 Resource Read Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    Resource Read Data Flow                                     │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Client Request                              Server Processing                │
│  ┌────────────────────────┐                  ┌────────────────────────────┐    │
│  │  method: resources/read│                  │  1. Parse URI              │    │
│  │  params:               │                  │  2. Match scheme           │    │
│  │    uri: "file:///src/  │─────────────────►│  3. Resolve provider       │    │
│  │    main.py"            │                  │  4. Read resource          │    │
│  │                        │◄─────────────────│  5. Determine MIME type    │    │
│  │  Response:             │                  │  6. Return content         │    │
│  │    contents: [{        │                  │                            │    │
│  │      uri: "...",       │                  │  Scheme Resolution:        │    │
│  │      mimeType:         │                  │  ┌──────────────────────┐  │    │
│  │        "text/x-python",│                  │  │ file:// → FileScheme │  │    │
│  │      text: "..."       │                  │  │ config:// → Config   │  │    │
│  │    }]                  │                  │  │ http:// → HttpScheme │  │    │
│  └────────────────────────┘                  │  │ log:// → LogsScheme  │  │    │
│                                              │  └──────────────────────┘  │    │
│                                              └────────────────────────────┘    │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Functionality Specification

### 3.1 Lifecycle Management

#### 3.1.1 Initialization Sequence

The MCP initialization sequence establishes the connection and negotiates capabilities:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    MCP Initialization Sequence                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Client                                      Server                           │
│    │                                          │                              │
│    │  1. initialize request                   │                              │
│    │  ──────────────────────────────────────► │                              │
│    │  {                                       │                              │
│    │    "jsonrpc": "2.0",                     │                              │
│    │    "id": 1,                              │                              │
│    │    "method": "initialize",               │                              │
│    │    "params": {                           │                              │
│    │      "protocolVersion": "2024-11-05",    │                              │
│    │      "capabilities": {                   │                              │
│    │        "roots": { "listChanged": true }  │                              │
│    │      },                                  │                              │
│    │      "clientInfo": {                     │                              │
│    │        "name": "phenotype-host",         │                              │
│    │        "version": "1.0.0"               │                              │
│    │      }                                   │                              │
│    │    }                                     │                              │
│    │  }                                       │                              │
│    │                                          │                              │
│    │                                          │  Validate protocol version   │
│    │                                          │  Check capabilities          │
│    │                                          │  Store client info           │
│    │                                          │                              │
│    │  2. initialize response                  │                              │
│    │  ◄────────────────────────────────────── │                              │
│    │  {                                       │                              │
│    │    "jsonrpc": "2.0",                     │                              │
│    │    "id": 1,                              │                              │
│    │    "result": {                           │                              │
│    │      "protocolVersion": "2024-11-05",    │                              │
│    │      "capabilities": {                   │                              │
│    │        "tools": { "listChanged": true }, │                              │
│    │        "resources": {                    │                              │
│    │          "subscribe": true,              │                              │
│    │          "listChanged": true             │                              │
│    │        },                                │                              │
│    │        "prompts": { "listChanged": false}│                              │
│    │      },                                  │                              │
│    │      "serverInfo": {                     │                              │
│    │        "name": "mcpkit-server",          │                              │
│    │        "version": "0.1.0"               │                              │
│    │      }                                   │                              │
│    │    }                                     │                              │
│    │  }                                       │                              │
│    │                                          │                              │
│    │  3. notifications/initialized            │                              │
│    │  ──────────────────────────────────────► │                              │
│    │  {                                       │                              │
│    │    "jsonrpc": "2.0",                     │                              │
│    │    "method": "notifications/initialized" │                              │
│    │  }                                       │                              │
│    │                                          │                              │
│    │  ←── Connection Established ──→          │                              │
│    │                                          │                              │
│    │  4. tools/list, resources/list, etc.     │                              │
│    │  ──────────────────────────────────────► │                              │
│    │                                          │                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### 3.1.2 Capability Negotiation

| Capability | Client Support | Server Support | Negotiated |
|------------|---------------|----------------|------------|
| `roots.listChanged` | true | N/A | Client notifies on root changes |
| `tools` | N/A | `{ listChanged: true }` | Server supports tool listing |
| `resources` | N/A | `{ subscribe: true, listChanged: true }` | Full resource support |
| `prompts` | N/A | `{ listChanged: false }` | Static prompt list |
| `sampling` | N/A | Not advertised | Not supported |
| `logging` | N/A | Not advertised | Not supported |

#### 3.1.3 Ping / Keepalive

```json
// Ping request (either direction)
{
  "jsonrpc": "2.0",
  "id": 100,
  "method": "ping"
}

// Ping response
{
  "jsonrpc": "2.0",
  "id": 100,
  "result": {}
}
```

### 3.2 Tool System

#### 3.2.1 Tool Definition

Every tool in McpKit conforms to the following definition:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    Tool Definition Schema                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  {                                                                           │
│    "name": "string",              // Unique tool identifier (required)        │
│    "description": "string",       // Human-readable description (required)    │
│    "inputSchema": {               // JSON Schema for input validation         │
│      "type": "object",            // Always "object"                          │
│      "properties": {              // Parameter definitions                    │
│        "<param_name>": {          │
│          "type": "string|integer|number|boolean|array|object",               │
│          "description": "string", │
│          "default": <any>,        // Optional default value                   │
│          "enum": [<values>],      // Optional enumeration                    │
│          "minimum": <number>,     // Optional numeric minimum                │
│          "maximum": <number>,     // Optional numeric maximum                │
│          "pattern": "regex"       // Optional string pattern                 │
│        }                                                                   │
│      },                                                                   │
│      "required": ["string"]       // List of required parameter names         │
│    }                                                                      │
│  }                                                                        │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### 3.2.2 Tool Registration Methods

McpKit supports three tool registration methods:

**Method 1: YAML Declarative**

```yaml
# registry.yaml
tools:
  - name: search_files
    description: Search for files matching a glob pattern
    handler: pheno_mcp.tools.search:search_files
    tags: [filesystem, search]
    category: file-operations
    timeout: 30
    input_schema:
      type: object
      properties:
        pattern:
          type: string
          description: Glob pattern to match
        directory:
          type: string
          description: Directory to search in
          default: "."
      required:
        - pattern
```

**Method 2: Decorator (Python)**

```python
from pheno_mcp import McpKit

mcp = McpKit("my-server", "0.1.0")

@mcp.tool()
def search_files(pattern: str, directory: str = ".") -> str:
    """Search for files matching a glob pattern."""
    # Implementation
    pass
```

**Method 3: Programmatic (Go)**

```go
server := mcpkit.NewServer("my-server", "0.1.0")
server.RegisterTool(&SearchFilesTool{})
```

#### 3.2.3 Tool Execution Protocol

```json
// Tool call request
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "search_files",
    "arguments": {
      "pattern": "*.py",
      "directory": "/src"
    }
  }
}

// Success response
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Found 42 files:\n/src/main.py\n/src/utils.py\n..."
      }
    ],
    "isError": false
  }
}

// Error response
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Permission denied: /src/secret.py"
      }
    ],
    "isError": true
  }
}
```

#### 3.2.4 Tool Result Content Types

| Content Type | Schema | Use Case |
|-------------|--------|----------|
| Text | `{ "type": "text", "text": "..." }` | Text output, messages |
| Image | `{ "type": "image", "data": "<base64>", "mimeType": "..." }` | Generated images, screenshots |
| Resource | `{ "type": "resource", "resource": { ... } }` | Embedded resource content |

#### 3.2.5 Tool Change Notifications

When the tool registry changes, the server sends a notification:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/list_changed"
}
```

The client should re-fetch the tool list via `tools/list`.

### 3.3 Resource System

#### 3.3.1 Resource URI Scheme

McpKit uses URI-based resource addressing with pluggable scheme handlers:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    Resource URI Schemes                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Scheme          Example                          Description                │
│  ──────────────  ───────────────────────────────  ─────────────────────────  │
│  file://         file:///path/to/file.txt         Local file access          │
│  config://       config://app/settings            Application configuration  │
│  http://         http://api.example.com/data      HTTP resource              │
│  log://          log://app/2024-01-01             Log file access            │
│  metric://       metric://cpu/usage               System metrics             │
│  env://          env://DATABASE_URL               Environment variables      │
│  prompt://       prompt://code-review             Prompt templates           │
│  tool://         tool://search_files/schema       Tool schema access         │
│  system://       system://info                    System information         │
│  zen://          zen://project/overview           Zen mode project data      │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### 3.3.2 Resource Definition

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    Resource Definition Schema                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Static Resource:                                                             │
│  {                                                                           │
│    "uri": "config://app/settings",        // Unique resource URI            │
│    "name": "Application Settings",          // Human-readable name           │
│    "description": "App configuration",     // Optional description           │
│    "mimeType": "application/json"           // Optional MIME type            │
│  }                                                                           │
│                                                                               │
│  Resource Template (dynamic):                                                  │
│  {                                                                           │
│    "uriTemplate": "file://{path}",          // URI with parameters           │
│    "name": "Project File",                  // Human-readable name           │
│    "description": "Access project files",   // Optional description           │
│    "mimeType": "text/plain"                 // Optional MIME type            │
│  }                                                                           │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### 3.3.3 Resource Content Types

```json
// Text resource
{
  "uri": "file:///src/main.py",
  "mimeType": "text/x-python",
  "text": "def main():\n    print('Hello')\n"
}

// Binary resource (base64 encoded)
{
  "uri": "file:///images/logo.png",
  "mimeType": "image/png",
  "blob": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

#### 3.3.4 Resource Subscription

```json
// Subscribe to resource changes
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "resources/subscribe",
  "params": {
    "uri": "config://app/settings"
  }
}

// Resource updated notification
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/updated",
  "params": {
    "uri": "config://app/settings"
  }
}
```

### 3.4 Prompt System

#### 3.4.1 Prompt Definition

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    Prompt Definition Schema                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  {                                                                           │
│    "name": "code_review",                 // Unique prompt identifier         │
│    "description": "Generate code review",  // Human-readable description      │
│    "arguments": [                         // Optional arguments              │
│      {                                  │
│        "name": "code",                  // Argument name                     │
│        "description": "Code to review", // Argument description              │
│        "required": true                 // Whether required                  │
│      },                               │
│      {                                  │
│        "name": "language",              // Argument name                     │
│        "description": "Programming language",                                │
│        "required": false                // Optional argument                 │
│      }                                │
│    ]                                  │
│  }                                                                           │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### 3.4.2 Prompt Retrieval

```json
// Get prompt request
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "code": "def foo():\n    return 1 + 1",
      "language": "python"
    }
  }
}

// Get prompt response
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Please review the following python code:\n\n```python\ndef foo():\n    return 1 + 1\n```\n\nProvide feedback on code quality, potential bugs, and improvements."
        }
      }
    ]
  }
}
```

### 3.5 Sampling System

#### 3.5.1 Sampling Request (Server → Client)

```json
{
  "jsonrpc": "2.0",
  "id": 10,
  "method": "sampling/createMessage",
  "params": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Summarize the following search results..."
        }
      }
    ],
    "maxTokens": 1000,
    "temperature": 0.7,
    "metadata": {
      "tool_name": "search_files"
    }
  }
}
```

### 3.6 Notification System

#### 3.6.1 Notification Types

| Notification | Direction | Trigger |
|-------------|-----------|---------|
| `notifications/initialized` | Client → Server | After initialization complete |
| `notifications/tools/list_changed` | Server → Client | Tool registry modified |
| `notifications/resources/list_changed` | Server → Client | Resource list modified |
| `notifications/resources/updated` | Server → Client | Specific resource changed |
| `notifications/prompts/list_changed` | Server → Client | Prompt list modified |
| `notifications/roots/list_changed` | Client → Server | Client roots changed |
| `notifications/cancelled` | Either → Either | Request cancellation |
| `notifications/progress` | Either → Either | Long-running operation progress |

#### 3.6.2 Progress Notifications

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "abc123",
    "progress": 50,
    "total": 100
  }
}
```

### 3.7 Root Management

#### 3.7.1 Root Definition

Roots define the filesystem or data boundaries visible to the MCP server:

```json
// Server requests roots list
{
  "jsonrpc": "2.0",
  "id": 8,
  "method": "roots/list"
}

// Client responds with roots
{
  "jsonrpc": "2.0",
  "id": 8,
  "result": {
    "roots": [
      {
        "uri": "file:///home/user/project",
        "name": "Project Root"
      },
      {
        "uri": "file:///home/user/docs",
        "name": "Documentation"
      }
    ]
  }
}
```

---

## 4. Technical Architecture

### 4.1 Protocol Stack

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    MCP Protocol Stack                                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Layer 5: Application                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Tools     │  │ Resources   │  │  Prompts    │  │    Sampling         │  │
│  │             │  │             │  │             │  │                     │  │
│  │ • list      │  │ • list      │  │ • list      │  │ • createMessage     │  │
│  │ • call      │  │ • read      │  │ • get       │  │                     │  │
│  │             │  │ • subscribe │  │             │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                                                                               │
│  Layer 4: Protocol                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────────────┐    │
│  │ Initialize   │  │ Capabilities │  │  Notifications                    │    │
│  │              │  │              │  │                                   │    │
│  │ • Handshake  │  │ • Negotiate  │  │ • tools/list_changed             │    │
│  │ • Version    │  │ • Detect     │  │ • resources/updated              │    │
│  │ • ClientInfo │  │ • Features   │  │ • progress                       │    │
│  └──────────────┘  └──────────────┘  └──────────────────────────────────┘    │
│                                                                               │
│  Layer 3: Transport                                                           │
│  ┌──────────────────────────┐  ┌──────────────────────────────────────────┐  │
│  │  SSE                     │  │  stdio                                   │  │
│  │                          │  │                                          │  │
│  │  • GET /sse (stream)     │  │  • stdin (read)                          │  │
│  │  • POST /message (send)  │  │  • stdout (write)                        │  │
│  │  • Session management    │  │  • Line-delimited JSON                   │  │
│  │  • CORS headers          │  │  • Process lifecycle                     │  │
│  └──────────────────────────┘  └──────────────────────────────────────────┘  │
│                                                                               │
│  Layer 2: Message                                                             │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  JSON-RPC 2.0                                                           │    │
│  │                                                                        │    │
│  │  Request:    { jsonrpc, id, method, params? }                          │    │
│  │  Response:   { jsonrpc, id, result?, error? }                          │    │
│  │  Error:      { code, message, data? }                                  │    │
│  │  Notification: { jsonrpc, method, params? }                            │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  Layer 1: Wire Format                                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  UTF-8 encoded JSON                                                     │    │
│  │  • stdio: newline-delimited JSON lines                                  │    │
│  │  • SSE: text/event-stream with data: prefix                             │    │
│  │  • HTTP POST: application/json body                                     │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Transport Layer

#### 4.2.1 Transport Trait/Interface

All transports implement a common interface:

**Python:**
```python
class Transport(ABC):
    @abstractmethod
    async def connect(self) -> None: ...
    @abstractmethod
    async def send(self, message: dict) -> None: ...
    @abstractmethod
    async def receive(self) -> dict: ...
    @abstractmethod
    async def close(self) -> None: ...
    @abstractmethod
    def is_connected(self) -> bool: ...
```

**Go:**
```go
type Transport interface {
    Connect(ctx context.Context) error
    Send(ctx context.Context, message json.RawMessage) error
    Receive(ctx context.Context) (json.RawMessage, error)
    Close() error
    IsConnected() bool
}
```

**TypeScript:**
```typescript
interface Transport {
    connect(): Promise<void>;
    send(message: JsonRpcMessage): Promise<void>;
    receive(): Promise<JsonRpcMessage>;
    close(): Promise<void>;
    isConnected(): boolean;
}
```

#### 4.2.2 stdio Transport Specification

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    stdio Transport Specification                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Protocol: Line-delimited JSON                                                │
│  Direction: Bidirectional                                                     │
│  Encoding: UTF-8                                                              │
│  Line Ending: \n (LF)                                                         │
│                                                                               │
│  Write (stdout):                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  {"jsonrpc":"2.0","id":1,"result":{...}}\n                             │    │
│  │  {"jsonrpc":"2.0","id":2,"result":{...}}\n                             │    │
│  │  {"jsonrpc":"2.0","method":"notifications/tools/list_changed"}\n       │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  Read (stdin):                                                                │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  {"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}\n       │    │
│  │  {"jsonrpc":"2.0","id":2,"method":"tools/list"}\n                      │    │
│  │  {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{...}}\n       │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  Error Handling:                                                              │
│  • Invalid JSON: log to stderr, continue reading                              │
│  • EOF: graceful shutdown                                                     │
│  • Write error: log to stderr, attempt recovery                               │
│                                                                               │
│  Process Lifecycle:                                                           │
│  • Parent spawns child process                                                │
│  • Child binds stdin/stdout                                                   │
│  • Child writes errors to stderr                                              │
│  • Parent terminates child on disconnect                                      │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### 4.2.3 SSE Transport Specification

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    SSE Transport Specification                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Endpoints:                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  GET  /sse          → Establish SSE connection (server → client)       │    │
│  │  POST /message      → Send message (client → server)                   │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  SSE Connection Flow:                                                         │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  1. Client: GET /sse                                                   │    │
│  │  2. Server: 200 OK with text/event-stream                              │    │
│  │  3. Server: event: endpoint\ndata: /message?sessionId=abc123\n\n       │    │
│  │  4. Client: POST /message?sessionId=abc123 with JSON body              │    │
│  │  5. Server: 202 Accepted                                               │    │
│  │  6. Server: event: message\ndata: {json-rpc}\n\n (to SSE stream)       │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  Session Management:                                                          │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  • Session ID: UUID v4                                                 │    │
│  │  • Timeout: 300 seconds (configurable)                                 │    │
│  │  • Max Sessions: 100 (configurable)                                    │    │
│  │  • Cleanup: on disconnect or timeout                                   │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  HTTP Headers (SSE endpoint):                                                 │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  Content-Type: text/event-stream                                       │    │
│  │  Cache-Control: no-cache                                               │    │
│  │  Connection: keep-alive                                                │    │
│  │  Access-Control-Allow-Origin: * (configurable)                         │    │
│  │  Access-Control-Allow-Methods: POST, OPTIONS                           │    │
│  │  Access-Control-Allow-Headers: Content-Type                            │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  Error Handling:                                                              │
│  • Invalid session: 404 Not Found                                            │    │
│  • Invalid JSON: 400 Bad Request                                             │    │
│  • Session full: 503 Service Unavailable                                     │    │
│  • Server error: 500 Internal Server Error                                   │    │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Message Layer

#### 4.3.1 JSON-RPC Message Types

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    JSON-RPC 2.0 Message Types                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Request:                                                                     │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  {                                                                    │    │
│  │    "jsonrpc": "2.0",              // Always "2.0"                     │    │
│  │    "id": <string|number>,         // Unique request ID                │    │
│  │    "method": "<method-name>",     // Method to invoke                 │    │
│  │    "params": { ... }              // Optional parameters              │    │
│  │  }                                                                    │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  Success Response:                                                            │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  {                                                                    │    │
│  │    "jsonrpc": "2.0",              // Always "2.0"                     │    │
│  │    "id": <matching-request-id>,   // Must match request ID            │    │
│  │    "result": { ... }              // Method result                    │    │
│  │  }                                                                    │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  Error Response:                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  {                                                                    │    │
│  │    "jsonrpc": "2.0",              // Always "2.0"                     │    │
│  │    "id": <matching-request-id>,   // Must match request ID            │    │
│  │    "error": {                     // Error object                     │    │
│  │      "code": <number>,            // Error code                       │    │
│  │      "message": "<string>",       // Error message                    │    │
│  │      "data": <any>                // Optional error data              │    │
│  │    }                                                                  │    │
│  │  }                                                                    │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  Notification:                                                                │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  {                                                                    │    │
│  │    "jsonrpc": "2.0",              // Always "2.0"                     │    │
│  │    "method": "<method-name>",     // Notification method              │    │
│  │    "params": { ... }              // Optional parameters              │    │
│  │  }                                                                    │    │
│  │                                                                       │    │
│  │  Note: Notifications have NO "id" field and receive NO response       │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### 4.3.2 Message ID Rules

| ID Type | Format | Example |
|---------|--------|---------|
| String | Any non-empty string | `"req-001"` |
| Number | Integer (positive or negative) | `1`, `-1`, `42` |
| Null | `null` (for notifications) | `null` |

**Rules:**
- IDs must be unique within a connection
- Response IDs must exactly match request IDs
- Notifications MUST NOT have an ID field
- Servers should use incrementing integers for simplicity

### 4.4 Server Architecture

#### 4.4.1 Server State Machine

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    MCP Server State Machine                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────┐    initialize     ┌──────────────┐    initialized     ┌────────┐│
│  │          │ ────────────────► │              │ ────────────────► │        ││
│  │  IDLE    │                   │  INITIALIZING│                   │  READY ││
│  │          │◄───────────────── │              │                   │        ││
│  └──────────┘   error/close    └──────────────┘                   └───┬────┘│
│       ▲                                                               │      │
│       │                                                               │      │
│       │  close/close                                                  │      │
│       │◄──────────────────────────────────────────────────────────────┘      │
│       │                                                               │      │
│       │  error                                                        │      │
│       │◄──────────────────────────────────────────────────────────────┘      │
│       │                                                               │      │
│  ┌────┴────┐                                                    ┌───────┴───┐│
│  │         │                                                    │           ││
│  │ CLOSED  │                                                    │ RUNNING   ││
│  │         │                                                    │           ││
│  └─────────┘                                                    └───────────┘│
│                                                                               │
│  State Transitions:                                                           │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  IDLE → INITIALIZING:   Client sends "initialize" request              │    │
│  │  INITIALIZING → READY:  Client sends "notifications/initialized"       │    │
│  │  READY → RUNNING:       Server accepts method requests                 │    │
│  │  Any → CLOSED:          Connection closed or error                     │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  Method Availability by State:                                                │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │  State        │ Allowed Methods                                       │    │
│  │  ──────────── │ ───────────────────────────────────────────────────── │    │
│  │  IDLE         │ initialize                                            │    │
│  │  INITIALIZING │ (waiting for initialized notification)                │    │
│  │  READY/RUNNING│ All methods: tools/*, resources/*, prompts/*, etc.    │    │
│  │  CLOSED       │ None                                                  │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### 4.4.2 Server Request Router

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    Server Request Router                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Incoming Request                                                             │
│       │                                                                       │
│       ▼                                                                       │
│  ┌─────────────────┐                                                         │
│  │ Validate JSON   │ ── Invalid ──► Return Parse Error (-32700)              │
│  │ Structure       │                                                         │
│  └────────┬────────┘                                                         │
│           │ Valid                                                             │
│           ▼                                                                   │
│  ┌─────────────────┐                                                         │
│  │ Check State     │ ── Not Ready ──► Return Invalid Request (-32600)        │
│  └────────┬────────┘                                                         │
│           │ Ready                                                             │
│           ▼                                                                   │
│  ┌─────────────────┐                                                         │
│  │ Route by Method │                                                         │
│  │                 │                                                         │
│  │ "initialize"    ──► LifecycleHandler.handleInitialize()                   │
│  │ "ping"          ──► LifecycleHandler.handlePing()                         │
│  │ "tools/list"    ──► ToolHandler.list()                                    │
│  │ "tools/call"    ──► ToolHandler.call()                                    │
│  │ "resources/list"──► ResourceHandler.list()                                │
│  │ "resources/read"──► ResourceHandler.read()                                │
│  │ "resources/sub" ──► ResourceHandler.subscribe()                           │
│  │ "prompts/list"  ──► PromptHandler.list()                                  │
│  │ "prompts/get"   ──► PromptHandler.get()                                   │
│  │ "roots/list"    ──► RootHandler.list()                                    │
│  │ "sampling/*"    ──► SamplingHandler.*()                                   │
│  │ *               ──► Return Method Not Found (-32601)                      │
│  └─────────────────┘                                                         │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 4.5 Client Architecture

#### 4.5.1 Client Connection Manager

```python
class ClientConnectionManager:
    """Manages MCP client connections to multiple servers."""

    def __init__(self):
        self._connections: dict[str, McpConnection] = {}
        self._message_router = MessageRouter()

    async def connect(self, server_id: str, transport: Transport) -> None:
        """Connect to an MCP server."""
        connection = McpConnection(server_id, transport)
        await connection.initialize()
        self._connections[server_id] = connection

    async def disconnect(self, server_id: str) -> None:
        """Disconnect from an MCP server."""
        if server_id in self._connections:
            await self._connections[server_id].close()
            del self._connections[server_id]

    async def call_tool(self, server_id: str, tool_name: str, args: dict) -> dict:
        """Call a tool on a specific server."""
        connection = self._connections[server_id]
        return await connection.call_tool(tool_name, args)

    async def read_resource(self, server_id: str, uri: str) -> dict:
        """Read a resource from a specific server."""
        connection = self._connections[server_id]
        return await connection.read_resource(uri)
```

---

## 5. API Reference

### 5.1 Python SDK API

#### 5.1.1 McpKit Server (FastMCP API)

```python
from pheno_mcp import McpKit

# Create server instance
mcp = McpKit(
    name: str,                    # Server name
    version: str = "0.1.0",       # Server version
    instructions: str = None,     # Server instructions for clients
)

# Tool decorator
@mcp.tool(
    name: str = None,             # Override function name
    description: str = None,      # Override docstring
    tags: list[str] = None,       # Categorization tags
    category: str = None,         # Tool category
    timeout: int = None,          # Execution timeout (seconds)
)
def tool_function(param: type, ...) -> str:
    """Tool description from docstring."""
    ...

# Resource decorator
@mcp.resource(
    uri: str,                     # Resource URI
    name: str = None,             # Resource name
    mime_type: str = None,        # MIME type
)
def resource_function() -> str:
    """Resource description."""
    ...

# Resource template decorator
@mcp.resource_template(
    uri_template: str,            # URI with {parameters}
    name: str = None,
    mime_type: str = None,
)
def template_function(param: str) -> str:
    """Template description."""
    ...

# Prompt decorator
@mcp.prompt(
    name: str = None,
    description: str = None,
)
def prompt_function(arg: str, ...) -> str | list[dict]:
    """Prompt description."""
    ...

# Run server
mcp.run(
    transport: str = "stdio",     # "stdio" or "sse"
    host: str = "0.0.0.0",        # SSE host
    port: int = 8000,             # SSE port
)
```

#### 5.1.2 Tool Registry API

```python
from pheno_mcp.registry import ToolRegistry

registry = ToolRegistry()

# Register tool
registry.register(
    name: str,
    description: str,
    input_schema: dict,
    handler: Callable,
    source: str = "programmatic",
    tags: list[str] = None,
    category: str = None,
    version: str = None,
    timeout: int = None,
    enabled: bool = True,
) -> ToolEntry

# Unregister tool
registry.unregister(name: str) -> None

# Get tool
registry.get(name: str) -> ToolEntry | None

# List tools
registry.list_tools() -> list[dict]

# Execute tool
await registry.execute(name: str, arguments: dict) -> Any

# Load from YAML
registry.load_from_yaml(path: str) -> list[ToolEntry]

# Change listener
registry.on_change(callback: Callable) -> None
```

#### 5.1.3 Resource Scheme API

```python
from pheno_mcp.resources.schemes.base import ResourceScheme

class CustomScheme(ResourceScheme):
    scheme = "custom"

    async def list_resources(self) -> list[Resource]:
        ...

    async def read_resource(self, uri: str) -> ResourceContent:
        ...

# Register scheme
from pheno_mcp.resources.schemes.registry import SchemeRegistry
SchemeRegistry.register(CustomScheme)
```

### 5.2 Go SDK API

#### 5.2.1 Server API

```go
import "github.com/phenotype/mcpkit-go"

// Create server
server := mcpkit.NewServer(
    "my-server",    // name
    "0.1.0",        // version
)

// Register tool
server.RegisterTool(handler ToolHandler)

// Register resource
server.RegisterResource(provider ResourceProvider)

// Run with transport
server.RunStdio()           // stdio transport
server.RunSSE(":8000")      // SSE transport
```

#### 5.2.2 Tool Handler Interface

```go
type ToolHandler interface {
    Definition() Tool
    Execute(ctx context.Context, args map[string]interface{}) (*ToolResult, error)
}

// Tool definition
type Tool struct {
    Name        string                 `json:"name"`
    Description string                 `json:"description,omitempty"`
    InputSchema map[string]interface{} `json:"inputSchema"`
}

// Tool result
type ToolResult struct {
    Content []Content `json:"content"`
    IsError *bool     `json:"isError,omitempty"`
}
```

### 5.3 TypeScript SDK API

#### 5.3.1 Server API

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-server",
  version: "0.1.0",
});

// Register tool
server.tool(
  "tool_name",
  "Tool description",
  {
    param1: z.string().describe("Parameter description"),
    param2: z.number().optional(),
  },
  async ({ param1, param2 }) => {
    return {
      content: [{ type: "text", text: "Result" }],
    };
  }
);

// Register resource
server.resource(
  "resource_name",
  "resource://uri",
  async (uri) => ({
    contents: [{
      uri: uri.href,
      mimeType: "text/plain",
      text: "Content",
    }],
  })
);

// Register prompt
server.prompt(
  "prompt_name",
  "Prompt description",
  {
    arg: z.string().describe("Argument description"),
  },
  ({ arg }) => ({
    messages: [{
      role: "user",
      content: { type: "text", text: `Prompt with ${arg}` },
    }],
  })
);
```

### 5.4 Rust Types API

#### 5.4.1 Generated Protocol Types

```rust
use mcp_forge::protocol::*;

// JSON-RPC types
let request = JsonRpcRequest {
    jsonrpc: "2.0".into(),
    id: JsonRpcId::Number(1),
    method: "tools/list".into(),
    params: None,
};

// Tool types
let tool = Tool {
    name: "search".into(),
    description: Some("Search files".into()),
    input_schema: serde_json::json!({
        "type": "object",
        "properties": {
            "pattern": { "type": "string" }
        },
        "required": ["pattern"]
    }),
};

// Content types
let content = Content::text("Hello, world!");
let image = Content::image(base64_data, "image/png");
```

---

## 6. Error Handling

### 6.1 Error Classification

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    Error Classification Hierarchy                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  McpError (Base)                                                              │
│  ├── ProtocolError                                                            │
│  │   ├── ParseError (-32700)                    Invalid JSON                  │
│  │   ├── InvalidRequestError (-32600)           Malformed request             │
│  │   ├── MethodNotFoundError (-32601)           Unknown method                │
│  │   ├── InvalidParamsError (-32602)            Parameter validation failed   │
│  │   └── InternalError (-32603)                 Server internal error         │
│  │                                                                              │
│  ├── McpApplicationError                                                        │
│  │   ├── ResourceNotFoundError (-32001)         Resource URI not found        │
│  │   ├── ToolExecutionError (-32002)            Tool execution failed         │
│  │   ├── CapabilityNotSupportedError (-32003)   Feature not available         │
│  │   ├── PromptNotFoundError (-32004)           Prompt not found              │
│  │   └── SubscriptionError (-32005)             Subscription failed           │
│  │                                                                              │
│  ├── SecurityError                                                              │
│  │   ├── AuthenticationError (-32100)           Invalid credentials           │
│  │   ├── AuthorizationError (-32101)            Insufficient permissions      │
│  │   └── RateLimitError (-32102)              Too many requests               │
│  │                                                                              │
│  └── TransportError                                                             │
│      ├── ConnectionError                  Connection failed                   │
│      ├── TimeoutError                     Operation timed out                 │
│      └── DisconnectedError                Connection lost                     │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Error Codes Reference

| Code | Name | Category | Description |
|------|------|----------|-------------|
| -32700 | ParseError | Protocol | Invalid JSON was received by the server |
| -32600 | InvalidRequest | Protocol | The JSON sent is not a valid Request object |
| -32601 | MethodNotFound | Protocol | The method does not exist or is not available |
| -32602 | InvalidParams | Protocol | Invalid method parameter(s) |
| -32603 | InternalError | Protocol | Internal JSON-RPC error |
| -32001 | ResourceNotFound | MCP | The requested resource was not found |
| -32002 | ToolExecutionError | MCP | Tool execution failed |
| -32003 | CapabilityNotSupported | MCP | Requested capability is not supported |
| -32004 | PromptNotFound | MCP | The requested prompt was not found |
| -32005 | SubscriptionError | MCP | Resource subscription failed |
| -32100 | AuthenticationError | Security | Authentication failed |
| -32101 | AuthorizationError | Security | Insufficient permissions |
| -32102 | RateLimitError | Security | Rate limit exceeded |
| -32103 | TimeoutError | Transport | Request timed out |

### 6.3 Error Response Format

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "error": {
    "code": -32002,
    "message": "Tool execution error: search_files",
    "data": {
      "tool_name": "search_files",
      "error_type": "PermissionError",
      "error_detail": "Permission denied: /src/secret.py",
      "timestamp": "2026-04-03T12:00:00Z"
    }
  }
}
```

### 6.4 Error Recovery Strategies

| Error Type | Recovery Strategy |
|------------|------------------|
| ParseError | Log error, continue reading next message |
| InvalidRequest | Return error response, continue processing |
| MethodNotFound | Return error, suggest similar methods |
| InvalidParams | Return error with validation details |
| InternalError | Log full stack trace, return generic error |
| ToolExecutionError | Return error with tool output, continue |
| ConnectionError | Attempt reconnection with exponential backoff |
| TimeoutError | Cancel operation, return timeout error |
| RateLimitError | Wait and retry after specified delay |

---

## 7. Security

### 7.1 Threat Model

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    McpKit Threat Model                                         │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Attack Vectors:                                                              │
│                                                                               │
│  1. Tool Execution                                                             │
│     ┌─────────────────────────────────────────────────────────────────────┐    │
│     │  • Arbitrary code execution via tool arguments                      │    │
│     │  • Command injection through parameter values                       │    │
│     │  • Resource exhaustion (CPU, memory, disk)                          │    │
│     │  • Privilege escalation through tool chaining                       │    │
│     │  • Path traversal in file operations                                │    │
│     └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  2. Data Access                                                               │
│     ┌─────────────────────────────────────────────────────────────────────┐    │
│     │  • Unauthorized resource access                                     │    │
│     │  • Data exfiltration through tool outputs                           │    │
│     │  • Sensitive data exposure in prompts                               │    │
│     │  • Information leakage in error messages                            │    │
│     └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  3. Transport                                                                 │
│     ┌─────────────────────────────────────────────────────────────────────┐    │
│     │  • Man-in-the-middle (SSE without TLS)                              │    │
│     │  • Session hijacking                                                │    │
│     │  • Replay attacks                                                   │    │
│     │  • Denial of service                                                │    │
│     └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  4. Protocol                                                                  │
│     ┌─────────────────────────────────────────────────────────────────────┐    │
│     │  • Malformed JSON-RPC messages                                      │    │
│     │  • Protocol version mismatch                                        │    │
│     │  • Capability spoofing                                              │    │
│     │  • Notification flooding                                            │    │
│     └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Authentication

#### 7.2.1 API Key Authentication

```python
class ApiKeyAuthenticator:
    """API key authentication for MCP servers."""

    def __init__(self, keys: dict[str, list[str]]):
        """Initialize with key-to-scopes mapping."""
        self._keys = keys

    def authenticate(self, api_key: str) -> list[str]:
        """Authenticate and return granted scopes."""
        if api_key not in self._keys:
            raise AuthenticationError("Invalid API key")
        return self._keys[api_key]
```

#### 7.2.2 OAuth 2.0 Integration

```python
from authlib.integrations.starlette_client import OAuth

class McpOAuthAuthenticator:
    """OAuth 2.0 authentication for MCP servers."""

    def __init__(self, config: dict):
        self.oauth = OAuth()
        self.oauth.register(
            name=config["provider"],
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            server_metadata_url=config["metadata_url"],
        )

    async def authenticate(self, request) -> dict:
        """Authenticate via OAuth 2.0."""
        token = await self.oauth.provider.authorize_access_token(request)
        return token
```

### 7.3 Authorization

#### 7.3.1 Permission Levels

| Level | Permissions | Use Case |
|-------|------------|----------|
| Read | List tools, read resources, get prompts | Information retrieval |
| Execute | Call read-only tools | Data analysis |
| Write | Call write tools, modify resources | Content modification |
| Admin | Register tools, configure server | Server management |

#### 7.3.2 Scope-Based Access Control

```python
class ScopeAuthorizer:
    """Scope-based authorization."""

    SCOPES = {
        "tools:read": ["tools/list"],
        "tools:execute": ["tools/call"],
        "resources:read": ["resources/list", "resources/read"],
        "resources:write": ["resources/write"],
        "prompts:read": ["prompts/list", "prompts/get"],
        "admin": ["*"],
    }

    def authorize(self, scopes: list[str], method: str) -> bool:
        """Check if scopes authorize the method."""
        allowed = set()
        for scope in scopes:
            allowed.update(self.SCOPES.get(scope, set()))
        return method in allowed or "*" in allowed
```

### 7.4 Input Validation

#### 7.4.1 JSON Schema Validation

All tool inputs are validated against their declared JSON Schema:

```python
from jsonschema import validate, ValidationError

def validate_tool_input(schema: dict, arguments: dict) -> None:
    """Validate tool arguments against input schema."""
    try:
        validate(instance=arguments, schema=schema)
    except ValidationError as e:
        raise InvalidParamsError(f"Invalid tool arguments: {e.message}")
```

#### 7.4.2 Path Validation

```python
import os

def validate_path(path: str, allowed_root: str) -> str:
    """Validate file path to prevent directory traversal."""
    resolved = os.path.realpath(os.path.join(allowed_root, path))
    allowed = os.path.realpath(allowed_root)
    if not resolved.startswith(allowed):
        raise SecurityError("Path traversal detected")
    return resolved
```

### 7.5 Sandboxing

#### 7.5.1 Process Sandboxing

```python
import asyncio
import tempfile

class ToolSandbox:
    """Execute tools in isolated environment."""

    def __init__(
        self,
        timeout: int = 30,
        memory_limit: str = "256m",
        network_enabled: bool = False,
    ):
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.network_enabled = network_enabled

    async def execute(self, command: list[str]) -> str:
        """Execute command in sandbox."""
        with tempfile.TemporaryDirectory() as tmpdir:
            env = {
                "HOME": tmpdir,
                "TMPDIR": tmpdir,
                "PATH": "/usr/bin:/bin",
            }

            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
                cwd=tmpdir,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.timeout,
                )
            except asyncio.TimeoutError:
                process.kill()
                raise TimeoutError(f"Execution exceeded {self.timeout}s")

            if process.returncode != 0:
                raise RuntimeError(stderr.decode())

            return stdout.decode()
```

### 7.6 Transport Security

#### 7.6.1 TLS Configuration (SSE)

```python
import ssl

def create_ssl_context(
    cert_file: str,
    key_file: str,
    ca_file: str = None,
) -> ssl.SSLContext:
    """Create SSL context for SSE transport."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_file, key_file)
    if ca_file:
        context.load_verify_locations(ca_file)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    return context
```

#### 7.6.2 CORS Configuration

```python
CORS_CONFIG = {
    "allow_origins": ["https://trusted-domain.com"],
    "allow_methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "allow_credentials": True,
    "max_age": 3600,
}
```

---

## 8. Testing and Quality Assurance

### 8.1 Test Strategy

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    McpKit Test Strategy                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Test Pyramid:                                                                │
│                                                                               │
│                         ┌─────────┐                                           │
│                        │  E2E    │   Integration tests across components     │
│                       │ Tests   │   • Full protocol flows                   │
│                      └───────────┘  • Multi-server scenarios                │
│                     ┌─────────────┐                                          │
│                    │ Integration │   Cross-component tests                   │
│                   │   Tests     │   • Transport + Protocol                  │
│                  └─────────────┘  • Registry + Server                       │
│                 ┌─────────────────┐                                          │
│                │    Unit Tests   │   Individual component tests              │
│               │                 │   • Tool handlers                         │
│              └───────────────────┘  • Schema validation                     │
│             ┌─────────────────────┐                                         │
│            │   Protocol Compliance │   MCP spec verification                │
│           │      Tests           │   • Method responses                    │
│          └───────────────────────┘  • Error codes                         │
│         ┌─────────────────────────┐                                        │
│        │    Performance Tests    │   Benchmark and load tests              │
│       └─────────────────────────┘  • Latency measurement                  │
│                                    • Throughput testing                   │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Test Categories

| Category | Scope | Tools | Coverage Target |
|----------|-------|-------|-----------------|
| Unit | Individual functions/classes | pytest, go test | >90% |
| Integration | Component interactions | pytest-asyncio | >80% |
| Protocol | MCP spec compliance | Custom test harness | 100% |
| E2E | Full server-client flows | Playwright, httpx | Key flows |
| Performance | Latency, throughput | pytest-benchmark | Baseline |
| Security | Vulnerability scanning | bandit, gosec | Critical only |

### 8.3 McpKit QA Framework

The McpKit Python package includes a comprehensive QA framework:

```
pheno_mcp/qa/
├── core/
│   ├── base/
│   │   ├── client_adapter.py    # MCP client for testing
│   │   └── test_runner.py       # Test execution engine
│   ├── cache.py                 # Test result caching
│   └── test_registry.py         # Test case registry
├── config/
│   └── endpoints.py             # Test endpoint configuration
├── logging/
│   └── structured_events.py     # Structured test event logging
├── oauth/
│   └── credential_broker.py     # Test credential management
├── pytest_plugins/
│   └── auth.py                  # Pytest authentication plugin
├── reporters/
│   ├── console.py               # Console output reporter
│   ├── error_detail.py          # Detailed error reporting
│   ├── json_reporter.py         # JSON output reporter
│   ├── markdown.py              # Markdown report generator
│   └── matrix.py                # Test matrix reporter
├── testing/
│   └── logging_config.py        # Test logging configuration
└── tui/
    └── widgets_compat.py        # Terminal UI widgets
```

### 8.4 Protocol Compliance Testing

```python
class ProtocolComplianceTest:
    """Test MCP protocol compliance."""

    async def test_initialize_flow(self, server):
        """Test initialization sequence."""
        response = await server.handle_request({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test", "version": "1.0.0"},
            },
        })

        assert response["result"]["protocolVersion"] == "2024-11-05"
        assert "serverInfo" in response["result"]
        assert "capabilities" in response["result"]

    async def test_tools_list_response(self, server):
        """Test tools/list response format."""
        response = await server.handle_request({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
        })

        assert "tools" in response["result"]
        for tool in response["result"]["tools"]:
            assert "name" in tool
            assert "inputSchema" in tool

    async def test_tools_call_success(self, server):
        """Test successful tool execution."""
        response = await server.handle_request({
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "echo",
                "arguments": {"message": "hello"},
            },
        })

        assert "content" in response["result"]
        assert response["result"].get("isError") != True

    async def test_tools_call_not_found(self, server):
        """Test tool not found error."""
        response = await server.handle_request({
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "nonexistent",
                "arguments": {},
            },
        })

        assert response["result"].get("isError") == True
```

---

## 9. Performance

### 9.1 Performance Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| Tool call latency (p50) | < 10ms | Time from request to response |
| Tool call latency (p99) | < 100ms | Time from request to response |
| Protocol message throughput | > 1000 msg/s | Messages processed per second |
| Server startup time | < 500ms | Time to first request |
| Memory usage (idle) | < 50MB | RSS at rest |
| Memory usage (under load) | < 200MB | RSS at 100 concurrent requests |
| SSE session capacity | > 100 sessions | Concurrent SSE connections |

### 9.2 Benchmarking

```python
import asyncio
import time
from dataclasses import dataclass

@dataclass
class BenchmarkResult:
    operation: str
    iterations: int
    total_time: float
    avg_latency_ms: float
    p50_latency_ms: float
    p99_latency_ms: float
    throughput_ops: float

async def benchmark_tool_calls(
    server,
    tool_name: str,
    arguments: dict,
    iterations: int = 1000,
) -> BenchmarkResult:
    """Benchmark tool call performance."""
    latencies = []

    # Warmup
    for _ in range(10):
        await server.handle_request({
            "jsonrpc": "2.0",
            "id": 0,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        })

    # Measure
    start = time.perf_counter()
    for i in range(iterations):
        req_start = time.perf_counter()
        await server.handle_request({
            "jsonrpc": "2.0",
            "id": i,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        })
        latencies.append((time.perf_counter() - req_start) * 1000)

    total = time.perf_counter() - start
    latencies.sort()

    return BenchmarkResult(
        operation=f"tools/call:{tool_name}",
        iterations=iterations,
        total_time=total,
        avg_latency_ms=sum(latencies) / len(latencies),
        p50_latency_ms=latencies[len(latencies) // 2],
        p99_latency_ms=latencies[int(len(latencies) * 0.99)],
        throughput_ops=iterations / total,
    )
```

### 9.3 Optimization Strategies

| Strategy | Description | Impact |
|----------|-------------|--------|
| Connection pooling | Reuse HTTP connections for SSE | Reduces latency 30% |
| Message batching | Batch multiple tool calls | Increases throughput 2x |
| Schema caching | Cache compiled JSON Schemas | Reduces validation time 50% |
| Lazy loading | Load tools on first use | Reduces startup time |
| Async I/O | Non-blocking I/O operations | Increases concurrency |
| Memory pooling | Reuse message buffers | Reduces GC pressure |

---

## 10. Configuration

### 10.1 Server Configuration

```yaml
# mcpkit.yaml
server:
  name: "mcpkit-server"
  version: "0.1.0"
  instructions: "McpKit MCP Server for the Phenotype ecosystem"

transport:
  type: "sse"              # stdio | sse
  sse:
    host: "0.0.0.0"
    port: 8000
    cors_origins:
      - "https://example.com"
    session_timeout: 300
    max_sessions: 100

tools:
  registry_path: "registry.yaml"
  auto_discover: true
  discovery_paths:
    - "pheno_mcp.tools"

resources:
  schemes:
    - "file"
    - "config"
    - "http"
    - "log"
    - "metric"
    - "env"

security:
  authentication: "api_key"
  api_keys_path: ".mcpkit-keys"
  rate_limit:
    requests_per_minute: 100
    burst: 20

logging:
  level: "INFO"
  format: "json"
  output: "stdout"
```

### 10.2 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MCPKIT_SERVER_NAME` | Server name | `mcpkit-server` |
| `MCPKIT_TRANSPORT` | Transport type | `stdio` |
| `MCPKIT_PORT` | SSE port | `8000` |
| `MCPKIT_HOST` | SSE host | `0.0.0.0` |
| `MCPKIT_REGISTRY` | Registry YAML path | `registry.yaml` |
| `MCPKIT_LOG_LEVEL` | Log level | `INFO` |
| `MCPKIT_API_KEY` | API key for auth | _(none)_ |
| `MCPKIT_CORS_ORIGINS` | CORS allowed origins | `*` |
| `MCPKIT_SESSION_TIMEOUT` | SSE session timeout (s) | `300` |
| `MCPKIT_MAX_SESSIONS` | Max SSE sessions | `100` |

---

## 11. Deployment

### 11.1 Local Deployment (stdio)

```json
{
  "mcpServers": {
    "mcpkit": {
      "command": "python",
      "args": ["-m", "pheno_mcp"],
      "env": {
        "MCPKIT_TRANSPORT": "stdio",
        "MCPKIT_REGISTRY": "/path/to/registry.yaml"
      }
    }
  }
}
```

### 11.2 Remote Deployment (SSE)

```bash
# Start MCP server with SSE transport
MCPKIT_TRANSPORT=sse \
MCPKIT_PORT=8000 \
MCPKIT_REGISTRY=registry.yaml \
python -m pheno_mcp
```

### 11.3 Container Deployment

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev

COPY . .

EXPOSE 8000

ENV MCPKIT_TRANSPORT=sse
ENV MCPKIT_HOST=0.0.0.0
ENV MCPKIT_PORT=8000

CMD ["poetry", "run", "python", "-m", "pheno_mcp"]
```

### 11.4 Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcpkit-server
  labels:
    app: mcpkit-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcpkit-server
  template:
    metadata:
      labels:
        app: mcpkit-server
    spec:
      containers:
      - name: mcpkit
        image: mcpkit/server:latest
        ports:
        - containerPort: 8000
        env:
        - name: MCPKIT_TRANSPORT
          value: "sse"
        - name: MCPKIT_REGISTRY
          value: "/config/registry.yaml"
        - name: MCPKIT_LOG_LEVEL
          value: "INFO"
        volumeMounts:
        - name: config
          mountPath: /config
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
      volumes:
      - name: config
        configMap:
          name: mcpkit-config
---
apiVersion: v1
kind: Service
metadata:
  name: mcpkit-service
spec:
  selector:
    app: mcpkit-server
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

---

## 12. Integration

### 12.1 Phenotype Ecosystem Integration

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    Phenotype Ecosystem Integration                             │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  AgilePlus   │  │  HeliosCLI   │  │   TheGent    │  │   PhenoSpecs     │  │
│  │              │  │              │  │              │  │                  │  │
│  │  Project     │  │  CLI         │  │  Dotfiles    │  │  Specifications  │  │
│  │  Management  │  │  Framework   │  │  Manager     │  │  & ADRs          │  │
│  │  & Tracking  │  │  & Commands  │  │  & Config    │  │  & Patterns      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                 │                 │                   │             │
│         └─────────────────┼─────────────────┼───────────────────┘             │
│                           │                 │                                 │
│                    ┌──────▼─────────────────▼──────┐                          │
│                    │                               │                          │
│                    │        McpKit                 │                          │
│                    │                               │                          │
│                    │  AI Agent Tool Integration    │                          │
│                    │                               │                          │
│                    │  • AgilePlus project queries  │                          │
│                    │  • HeliosCLI command execution│                          │
│                    │  • TheGent config management  │                          │
│                    │  • PhenoSpecs pattern lookup  │                          │
│                    │                               │                          │
│                    └───────────────────────────────┘                          │
│                           │                                                   │
│                    ┌──────▼──────┐                                            │
│                    │  AI Agents  │                                            │
│                    │  (Claude,   │                                            │
│                    │   custom)   │                                            │
│                    └─────────────┘                                            │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 12.2 Agent Framework Adapters

#### 12.2.1 LangGraph Adapter

```python
from pheno_mcp.agents.adapters.langgraph_adapter import LangGraphAdapter

adapter = LangGraphAdapter(mcp_server)

# Convert MCP tools to LangGraph tools
langgraph_tools = adapter.to_langgraph_tools()

# Use in LangGraph workflow
from langgraph.graph import StateGraph

workflow = StateGraph(State)
for tool in langgraph_tools:
    workflow.add_node(tool.name, tool)
```

#### 12.2.2 CrewAI Adapter

```python
from pheno_mcp.agents.adapters.crewai_adapter import CrewAIAdapter

adapter = CrewAIAdapter(mcp_server)

# Convert MCP tools to CrewAI tools
crewai_tools = adapter.to_crewai_tools()

# Use in Crew
from crewai import Agent, Crew

agent = Agent(
    role="Researcher",
    goal="Research topics",
    tools=crewai_tools,
)
```

#### 12.2.3 AutoGen Adapter

```python
from pheno_mcp.agents.adapters.autogen_adapter import AutoGenAdapter

adapter = AutoGenAdapter(mcp_server)

# Convert MCP tools to AutoGen functions
autogen_functions = adapter.to_autogen_functions()

# Use in AutoGen assistant
from autogen import AssistantAgent

assistant = AssistantAgent(
    name="assistant",
    function_map=autogen_functions,
)
```

### 12.3 External Service Integration

McpKit tools can integrate with external services:

```python
@mcp.tool()
def query_database(query: str, database: str = "default") -> str:
    """Execute a database query."""
    import httpx
    response = httpx.post(
        f"https://db-api.example.com/{database}/query",
        json={"query": query},
    )
    return response.text

@mcp.tool()
def search_web(query: str, max_results: int = 10) -> str:
    """Search the web for information."""
    import httpx
    response = httpx.get(
        "https://search-api.example.com/search",
        params={"q": query, "limit": max_results},
    )
    results = response.json()
    return "\n".join(f"{r['title']}: {r['url']}" for r in results)
```

---

## 13. Governance

### 13.1 Versioning Policy

McpKit follows Semantic Versioning (SemVer 2.0.0):

| Version Component | Increment When |
|------------------|----------------|
| MAJOR | Breaking protocol changes, API incompatibilities |
| MINOR | New tools, features, backward-compatible additions |
| PATCH | Bug fixes, performance improvements, documentation |

### 13.2 Deprecation Policy

| Phase | Duration | Description |
|-------|----------|-------------|
| Announcement | 1 release cycle | Deprecation warning in logs and docs |
| Grace Period | 2 release cycles | Feature works but with warnings |
| Removal | After grace period | Feature removed in next major version |

### 13.3 Change Management

All changes to McpKit must follow the AgilePlus workflow:

1. **Spec Creation**: `agileplus specify --title "<feature>" --description "<desc>"`
2. **ADR**: Document architectural decisions
3. **Implementation**: Code with tests
4. **Review**: Pull request with spec reference
5. **Validation**: `agileplus validate --feature <slug>`
6. **Integration**: Merge to main branch

---

## 14. Appendices

### A. Protocol Method Reference

| Method | Direction | Params | Result | Description |
|--------|-----------|--------|--------|-------------|
| `initialize` | C → S | `protocolVersion`, `capabilities`, `clientInfo` | `protocolVersion`, `capabilities`, `serverInfo` | Initialize connection |
| `notifications/initialized` | C → S | _(none)_ | _(none)_ | Signal init complete |
| `ping` | Either | _(none)_ | _(empty)_ | Health check |
| `tools/list` | C → S | `cursor?` | `tools[]`, `nextCursor?` | List available tools |
| `tools/call` | C → S | `name`, `arguments` | `content[]`, `isError?` | Execute a tool |
| `resources/list` | C → S | `cursor?` | `resources[]`, `nextCursor?` | List available resources |
| `resources/read` | C → S | `uri` | `contents[]` | Read resource content |
| `resources/subscribe` | C → S | `uri` | _(empty)_ | Subscribe to resource |
| `resources/unsubscribe` | C → S | `uri` | _(empty)_ | Unsubscribe from resource |
| `prompts/list` | C → S | `cursor?` | `prompts[]`, `nextCursor?` | List available prompts |
| `prompts/get` | C → S | `name`, `arguments?` | `messages[]` | Get prompt with args |
| `roots/list` | S → C | _(none)_ | `roots[]` | List client roots |
| `sampling/createMessage` | S → C | `messages`, `maxTokens?`, `temperature?` | `role`, `content`, `model` | Request LLM sampling |

### B. Type Definitions

#### B.1 JSON-RPC Types

```
JsonRpcRequest:
  jsonrpc: "2.0"
  id: string | number
  method: string
  params?: object

JsonRpcResponse:
  jsonrpc: "2.0"
  id: string | number
  result?: object
  error?: JsonRpcError

JsonRpcError:
  code: number
  message: string
  data?: any

JsonRpcNotification:
  jsonrpc: "2.0"
  method: string
  params?: object
```

#### B.2 Content Types

```
TextContent:
  type: "text"
  text: string

ImageContent:
  type: "image"
  data: string (base64)
  mimeType: string

ResourceContent:
  type: "resource"
  resource:
    uri: string
    mimeType?: string
    text?: string
    blob?: string (base64)
```

### C. Configuration Reference

See Section 10 for full configuration documentation.

### D. Glossary

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - standardized communication between AI models and tools |
| **JSON-RPC** | JSON-based remote procedure call protocol (version 2.0) |
| **SSE** | Server-Sent Events - HTTP-based server-to-client streaming |
| **stdio** | Standard I/O - process-based communication via stdin/stdout |
| **Tool** | An executable function exposed to AI clients through MCP |
| **Resource** | A data source accessible via URI through MCP |
| **Prompt** | A template for generating LLM prompts with arguments |
| **Capability** | A feature set advertised during MCP initialization |
| **Schema** | JSON Schema definition for tool input validation |
| **Handler** | The function that executes a tool's logic |
| **Registry** | Central store of tool/resource/prompt definitions |
| **Transport** | Communication layer (SSE or stdio) |
| **Host** | Application that initiates MCP connections |
| **Sampling** | Server-initiated request for LLM generation |
| **Root** | Client-exposed filesystem or data boundary |
| **Notification** | Fire-and-forget protocol message (no response expected) |
| **mcp-forge** | McpKit's type generator for Rust protocol types |
| **pheno-mcp** | McpKit's Python SDK package |

---

*Specification Version: 1.0*  
*Total Lines: 2000+*  
*Last Updated: 2026-04-03*
