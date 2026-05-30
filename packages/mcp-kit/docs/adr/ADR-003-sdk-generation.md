# ADR-003: SDK Generation Strategy

**Document ID:** PHENOTYPE_MCPKIT_ADR_003  
**Status:** Proposed  
**Last Updated:** 2026-04-03  
**Author:** Phenotype Architecture Team

---

## Table of Contents

1. [Title](#title)
2. [Status](#status)
3. [Context](#context)
4. [Decision](#decision)
5. [Consequences](#consequences)
6. [Architecture](#architecture)
7. [Implementation Details](#implementation-details)
8. [Code Examples](#code-examples)
9. [Cross-References](#cross-references)

---

## Title

**SDK Generation Strategy: Schema-Driven Code Generation from MCP Protocol Definitions**

## Status

**Proposed** — This strategy is under evaluation and has not yet been approved for implementation.

## Context

### Problem Statement

McpKit targets four programming languages (Python, Go, TypeScript, Rust), each requiring SDK implementations that conform to the MCP protocol specification. Maintaining protocol-compliant types, message structures, and error codes across multiple languages presents significant challenges:

1. **Protocol Drift**: Manual implementations inevitably diverge from the protocol specification as the spec evolves. Changes to MCP types, methods, or error codes must be propagated to all SDKs simultaneously.

2. **Type Inconsistency**: Different language implementations may interpret protocol types differently. For example, a JSON-RPC ID that can be either string or number requires different union types in each language.

3. **Maintenance Overhead**: Every protocol update requires changes across four codebases. A single field addition to a protocol type requires updates in Python dataclasses, Go structs, TypeScript interfaces, and Rust structs.

4. **Documentation Synchronization**: SDK documentation, API references, and code examples must be updated alongside implementation changes, multiplying the documentation burden.

5. **Testing Burden**: Each SDK requires its own test suite covering protocol compliance, type serialization/deserialization, and error handling. Test cases must be equivalent across languages.

### Generation Options Evaluated

#### Option A: Manual Implementation

Each SDK is hand-written and maintained independently:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Manual Implementation Model                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  MCP Protocol Spec                                                    │
│  (TypeScript types)                                                   │
│       │                                                               │
│       ├──► Python SDK (hand-written)                                  │
│       │                                                               │
│       ├──► Go SDK (hand-written)                                      │
│       │                                                               │
│       ├──► TypeScript SDK (hand-written)                              │
│       │                                                               │
│       └──► Rust SDK (hand-written)                                    │
│                                                                       │
│  Problems:                                                            │
│  • Protocol drift between implementations                             │
│  • Inconsistent type mappings                                         │
│  • High maintenance burden                                            │
│  • Difficult to verify compliance                                     │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

**Pros:**
- Full control over implementation details
- Idiomatic code for each language
- No build-time generation dependency
- Easier to debug (no generated code layer)

**Cons:**
- Protocol drift inevitable over time
- High maintenance cost for spec updates
- Inconsistent behavior across SDKs
- Difficult to verify protocol compliance

#### Option B: Single Source of Truth (TypeScript → All Languages)

Use the official MCP TypeScript types as the source of truth and generate other language SDKs:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    TypeScript-First Generation Model                   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  MCP TypeScript Types (Official)                                      │
│  (types.ts, protocol.ts)                                              │
│       │                                                               │
│       ├──► mcp-forge (Go-based generator)                             │
│       │       │                                                       │
│       │       ├──► Python types (dataclasses)                         │
│       │       ├──► Go types (structs)                                 │
│       │       └──► Rust types (structs)                               │
│       │                                                               │
│       └──► TypeScript SDK (uses source directly)                      │
│                                                                       │
│  Existing: mcp-forge already generates Rust types from TS schema      │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

**Pros:**
- TypeScript is the official reference implementation
- Single source of truth for protocol types
- mcp-forge already exists for Rust generation
- TypeScript types are well-structured for generation

**Cons:**
- TypeScript types may not map cleanly to all languages
- Generator complexity for type system differences
- Loss of language-specific optimizations
- Generator bugs affect all target languages

#### Option C: JSON Schema as Source of Truth

Define the MCP protocol in JSON Schema and generate all SDKs from it:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    JSON Schema-First Generation Model                   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  MCP Protocol JSON Schema                                             │
│  (mcp-schema.json)                                                    │
│       │                                                               │
│       └──► Multi-language Generator                                   │
│               │                                                       │
│               ├──► Python SDK (pydantic models)                       │
│               ├──► Go SDK (structs + validation)                      │
│               ├──► TypeScript SDK (interfaces + Zod)                  │
│               └──► Rust SDK (serde structs)                           │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

**Pros:**
- Language-agnostic source format
- Built-in validation through JSON Schema
- Many existing code generators available
- Easy to version and diff

**Cons:**
- JSON Schema cannot express all TypeScript type patterns
- Loss of TypeScript-specific features (generics, unions)
- Requires maintaining separate schema file
- May not capture protocol semantics fully

#### Option D: Hybrid Generation (mcp-forge Extended)

Extend the existing `mcp-forge` tool to generate types for all target languages from the TypeScript source, while allowing hand-written SDK logic around the generated types:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Hybrid Generation Model (Proposed)                   │
├──────────────────────────────────────────────────────────────────────┘
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    Source Layer                                  │  │
│  │                                                                 │  │
│  │  MCP TypeScript Types (Official SDK)                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │  │
│  │  │ types.ts     │  │ protocol.ts  │  │  server/index.ts     │   │  │
│  │  │              │  │              │  │                      │   │  │
│  │  │ • Request    │  │ • Methods    │  │  • Server class      │   │  │
│  │  │ • Response   │  │ • Lifecycle  │  │  • Tool registration │   │  │
│  │  │ • Content    │  │ • Capabilities│ │  • Transport connect │   │  │
│  │  │ • Error      │  │ • Notifications│ │                      │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                               │                                       │
│                  ┌────────────▼────────────┐                          │
│                  │    mcp-forge            │                          │
│                  │    (Go-based generator) │                          │
│                  │                         │                          │
│                  │  • Parse TypeScript AST │                          │
│                  │  • Map type systems     │                          │
│                  │  • Generate target code │                          │
│                  │  • Apply templates      │                          │
│                  └────────────┬────────────┘                          │
│                               │                                       │
│  ┌────────────────────────────┼────────────────────────────────────┐  │
│  │                    Generated Types Layer                         │  │
│  │                                                                 │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │  │
│  │  │ Python       │  │ Go           │  │ Rust                 │   │  │
│  │  │              │  │              │  │                      │   │  │
│  │  │ dataclasses  │  │ structs      │  │ structs              │   │  │
│  │  │ type hints   │  │ json tags    │  │ serde derives        │   │  │
│  │  │ docstrings   │  │ comments     │  │ doc comments         │   │  │
│  │  │              │  │              │  │                      │   │  │
│  │  │ pheno_mcp/   │  │ mcpkit-go/   │  │ mcp-forge/           │   │  │
│  │  │ types.py     │  │ protocol/    │  │ protocol/            │   │  │
│  │  │ (generated)  │  │ (generated)  │  │ (generated)          │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                               │                                       │
│  ┌────────────────────────────┼────────────────────────────────────┐  │
│  │                    Hand-Written SDK Layer                        │  │
│  │                                                                 │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │  │
│  │  │ Python SDK   │  │ Go SDK       │  │ TypeScript SDK       │   │  │
│  │  │              │  │              │  │ (Official + Custom)  │   │  │
│  │  │ • Server     │  │ • Server     │  │ • Server (official)  │   │  │
│  │  │ • Transports │  │ • Transports │  │ • Transports         │   │  │
│  │  │ • Registry   │  │ • Registry   │  │ • Custom extensions  │   │  │
│  │  │ • Decorators │  │ • CLI        │  │                      │   │  │
│  │  │ • QA         │  │              │  │                      │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

**Pros:**
- Leverages existing mcp-forge infrastructure
- Generated types stay in sync with protocol
- Hand-written SDK logic remains idiomatic
- Clear separation between types and behavior
- TypeScript remains the source of truth

**Cons:**
- Generator maintenance required
- Type mapping complexity across languages
- Generated code may not be perfectly idiomatic
- Build pipeline dependency

### Requirements

| Requirement | Priority | Description |
|-------------|----------|-------------|
| R1 | Must | Generate protocol types from TypeScript source |
| R2 | Must | Support Python, Go, Rust generation |
| R3 | Must | Generated types must be protocol-compliant |
| R4 | Must | Generation must be reproducible (deterministic) |
| R5 | Should | Generated code passes language linters |
| R6 | Should | Support incremental generation (only changed types) |
| R7 | Should | Generate documentation comments from TypeScript JSDoc |
| R8 | Could | Generate TypeScript SDK extensions |
| R9 | Could | Generate test fixtures from protocol types |
| R10 | Could | Generate OpenAPI/Swagger docs from protocol types |

### Existing mcp-forge Capabilities

The existing `mcp-forge` tool in `rust/mcp-forge/` already generates Rust protocol types from MCP TypeScript definitions:

```
rust/mcp-forge/
├── cmd/generate/
│   ├── main.go              # Entry point
│   ├── generate.go          # Generation logic
│   ├── types.go             # Type mapping
│   ├── methods.go           # Method generation
│   ├── tables.go            # Type tables
│   ├── typenames.go         # Name mapping
│   └── output.go            # Output formatting
├── internal/
│   ├── protocol/
│   │   ├── interfaces.go    # Protocol interfaces
│   │   ├── tsprotocol.go    # TypeScript protocol types
│   │   ├── tsdocument-changes.go
│   │   ├── tsjson.go
│   │   ├── uri.go
│   │   ├── pattern_interfaces.go
│   │   └── tables.go
│   ├── lsp/
│   │   ├── client.go
│   │   ├── protocol.go
│   │   ├── transport.go
│   │   ├── methods.go
│   │   ├── detect-language.go
│   │   ├── server-request-handlers.go
│   │   └── typescript.go
│   ├── logging/
│   │   ├── logger.go
│   │   └── logger_test.go
│   ├── utilities/
│   │   ├── edit.go
│   │   ├── edit_test.go
│   │   └── logging.go
│   └── watcher/
│       ├── watcher.go
│       └── gitignore.go
├── go.mod
├── go.sum
└── justfile
```

## Decision

**Extend mcp-forge to generate protocol types for Python and Go, in addition to the existing Rust generation.**

The generation strategy follows a layered approach:

1. **Source**: Official MCP TypeScript types serve as the single source of truth
2. **Generator**: mcp-forge parses TypeScript AST and generates target language types
3. **Generated Layer**: Protocol types (requests, responses, content, errors) are generated
4. **SDK Layer**: Hand-written SDK code (server, transport, registry) wraps generated types

### Generation Pipeline

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Generation Pipeline                                 │
├──────────────────────────────────────────────────────────────────────┘
│                                                                       │
│  Step 1: Parse TypeScript Source                                      │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                                                                 │  │
│  │  Input: @modelcontextprotocol/sdk/src/types.ts                  │  │
│  │                                                                 │  │
│  │  ┌───────────────────────────────────────────────────────────┐  │  │
│  │  │ TypeScript AST Parser                                     │  │  │
│  │  │                                                           │  │  │
│  │  │ • Extract interface definitions                           │  │  │
│  │  │ • Extract type aliases                                    │  │  │
│  │  │ • Extract enum definitions                                │  │  │
│  │  │ • Extract JSDoc comments                                  │  │  │
│  │  │ • Resolve type references                                 │  │  │
│  │  │ • Handle union/intersection types                         │  │  │
│  │  │ • Handle generic types                                    │  │  │
│  │  └───────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                               │                                       │
│                               ▼                                       │
│  Step 2: Type Mapping                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                                                                 │  │
│  │  TypeScript          →  Python          →  Go          →  Rust  │  │
│  │  ──────────────────     ──────────────     ──────────     ─────  │  │
│  │  interface Foo        →  class Foo      →  type Foo    →  struct│  │
│  │  type Foo = ...       →  type Foo       →  type Foo    →  enum  │  │
│  │  enum Foo             →  Enum Foo       →  const iota  →  enum  │  │
│  │  string               →  str            →  string      →  String│  │
│  │  number               →  int|float      →  float64     →  f64   │  │
│  │  boolean              →  bool           →  bool        →  bool  │  │
│  │  T[]                  →  list[T]        →  []T         →  Vec<T>│  │
│  │  Record<K,V>          →  dict[K,V]      →  map[K]V     →  HashMap│  │
│  │  T | null             →  Optional[T]    →  *T          →  Option│  │
│  │  A | B (union)        →  Union[A,B]     →  interface{} →  enum  │  │
│  │  { [key: string]: T } →  dict[str, T]   →  map[string]T→  HashMap│  │
│  │                                                                 │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                               │                                       │
│                               ▼                                       │
│  Step 3: Template Rendering                                           │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                                                                 │  │
│  │  Language Templates:                                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │  │
│  │  │ Python       │  │ Go           │  │ Rust                 │   │  │
│  │  │ templates/   │  │ templates/   │  │ templates/           │   │  │
│  │  │              │  │              │  │                      │   │  │
│  │  │ dataclass.go │  │ struct.go    │  │ struct.go            │   │  │
│  │  │ module.go    │  │ package.go   │  │ mod.go               │   │  │
│  │  │ imports.go   │  │ imports.go   │  │ imports.go           │   │  │
│  │  │ docstring.go │  │ comment.go   │  │ doc_comment.go       │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                               │                                       │
│                               ▼                                       │
│  Step 4: Output                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                                                                 │  │
│  │  python/pheno_mcp/types.py          # Generated Python types    │  │
│  │  go/mcpkit-go/protocol/types.go     # Generated Go types        │  │
│  │  rust/mcp-forge/protocol/           # Generated Rust types      │  │
│  │  typescript/                          # Generated TS extensions │  │
│  │                                                                 │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### Type Mapping Strategy

The core challenge is mapping TypeScript's type system to target languages:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Type Mapping Strategy                               │
├──────────────────────────────────────────────────────────────────────┘
│                                                                       │
│  Complex Type Patterns:                                               │
│                                                                       │
│  1. Tagged Unions (Discriminated Unions)                              │
│     ┌─────────────────────────────────────────────────────────────┐   │
│     │  TypeScript:                                                │   │
│     │  type Content =                                             │   │
│     │    | { type: "text"; text: string }                         │   │
│     │    | { type: "image"; data: string; mimeType: string }      │   │
│     │                                                             │   │
│     │  Python:                                                    │   │
│     │  @dataclass                                                 │   │
│     │  class TextContent:                                         │   │
│     │      type: Literal["text"] = "text"                         │   │
│     │      text: str                                              │   │
│     │                                                             │   │
│     │  Go:                                                        │   │
│     │  type Content interface { isContent() }                     │   │
│     │  type TextContent struct { Type string; Text string }       │   │
│     │  func (TextContent) isContent() {}                          │   │
│     │                                                             │   │
│     │  Rust:                                                      │   │
│     │  #[serde(tag = "type")]                                     │   │
│     │  enum Content {                                             │   │
│     │      #[serde(rename = "text")]                              │   │
│     │      Text { text: String },                                 │   │
│     │      #[serde(rename = "image")]                             │   │
│     │      Image { data: String, mime_type: String },             │   │
│     │  }                                                          │   │
│     └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  2. Optional Fields                                                   │
│     ┌─────────────────────────────────────────────────────────────┐   │
│     │  TypeScript:                                                │   │
│     │  interface Tool {                                           │   │
│     │    name: string;                                            │   │
│     │    description?: string;                                    │   │
│     │  }                                                          │   │
│     │                                                             │   │
│     │  Python:                                                    │   │
│     │  @dataclass                                                 │   │
│     │  class Tool:                                                │   │
│     │      name: str                                              │   │
│     │      description: str | None = None                         │   │
│     │                                                             │   │
│     │  Go:                                                        │   │
│     │  type Tool struct {                                         │   │
│     │      Name        string  `json:"name"`                      │   │
│     │      Description *string `json:"description,omitempty"`     │   │
│     │  }                                                          │   │
│     │                                                             │   │
│     │  Rust:                                                      │   │
│     │  struct Tool {                                              │   │
│     │      name: String,                                          │   │
│     │      #[serde(skip_serializing_if = "Option::is_none")]      │   │
│     │      description: Option<String>,                           │   │
│     │  }                                                          │   │
│     └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  3. JSON-RPC ID (String | Number | Null)                              │
│     ┌─────────────────────────────────────────────────────────────┐   │
│     │  TypeScript:                                                │   │
│     │  type RequestId = string | number | null;                   │   │
│     │                                                             │   │
│     │  Python:                                                    │   │
│     │  RequestId = str | int | None                               │   │
│     │                                                             │   │
│     │  Go:                                                        │   │
│     │  type RequestID any  // with custom JSON marshaler          │   │
│     │                                                             │   │
│     │  Rust:                                                      │   │
│     │  #[serde(untagged)]                                         │   │
│     │  enum RequestId {                                           │   │
│     │      String(String),                                        │   │
│     │      Number(i64),                                           │   │
│     │      Null,                                                  │   │
│     │  }                                                          │   │
│     └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Consequences

### Positive Consequences

1. **Protocol Compliance Guarantee**: Generated types are derived directly from the official MCP TypeScript types, ensuring 100% protocol compliance. Any change to the protocol specification is automatically reflected in all generated SDKs when the generator is re-run. This eliminates the risk of protocol drift that plagues manual implementations.

2. **Single Update Point**: When the MCP protocol specification changes, only the TypeScript source and generator templates need updating. Running the generator propagates changes to all target languages simultaneously. A single field addition to a protocol type requires one TypeScript change and one generator template update, rather than four separate SDK changes.

3. **Consistent Type Mappings**: The generator enforces consistent type mappings across all languages. A TypeScript `string` always maps to Python `str`, Go `string`, and Rust `String`. A TypeScript optional field always maps to Python `Optional[T]`, Go `*T` with `omitempty`, and Rust `Option<T>`. This consistency reduces cognitive load for developers working across multiple SDKs.

4. **Leverages Existing Infrastructure**: mcp-forge already implements TypeScript-to-Rust generation with a well-structured pipeline (parsing, type mapping, template rendering, output). Extending it for Python and Go reuses this infrastructure rather than building new generators from scratch. The existing `internal/protocol/` package provides the type mapping foundation.

5. **Documentation Generation**: JSDoc comments from TypeScript types can be automatically converted to language-appropriate documentation (Python docstrings, Go comments, Rust doc comments). This ensures documentation stays synchronized with type definitions and reduces the documentation maintenance burden.

6. **Reproducible Builds**: The generation process is deterministic — running the generator with the same TypeScript source always produces identical output. This enables CI/CD verification that generated types match the committed code, catching any manual modifications that would cause drift.

7. **Test Fixture Generation**: Protocol types can be used to generate test fixtures (valid and invalid JSON-RPC messages) automatically. This ensures test coverage for all protocol types and reduces the manual effort of creating test data.

### Negative Consequences

1. **Generator Complexity**: The type mapping logic must handle all TypeScript type patterns (unions, intersections, generics, conditional types, mapped types) and produce correct output for each target language. This is a complex undertaking, particularly for advanced TypeScript patterns that don't have direct equivalents in other languages. The generator itself becomes a significant codebase requiring maintenance.

2. **Generated Code Quality**: Generated code may not be perfectly idiomatic for each target language. Python developers expect dataclasses with type hints, Go developers expect idiomatic structs with json tags, and Rust developers expect serde derives with proper error handling. The generator must produce code that meets each language's conventions, which may require complex template logic and post-processing.

3. **Build Pipeline Dependency**: SDK development now depends on the generator being available and functional. If the generator breaks, all SDK type generation is blocked. This adds a critical dependency to the build pipeline and requires the generator to be maintained alongside the SDKs. CI/CD must run the generator and verify output on every protocol change.

4. **Debugging Generated Code**: When issues arise in generated types, developers must debug code they didn't write and may not fully understand. Stack traces point to generated files, and the relationship between TypeScript source and generated output may not be immediately obvious. Source maps or generation annotations can help but add complexity.

5. **Type Mapping Limitations**: Some TypeScript patterns cannot be cleanly mapped to all target languages. For example, TypeScript's structural typing, template literal types, and conditional types have no direct equivalents in Go or Rust. These patterns require manual intervention, special-case handling in the generator, or acceptance of imperfect mappings.

6. **Template Maintenance**: Each target language requires its own set of templates for different type patterns (interfaces, type aliases, enums, unions). As the MCP protocol evolves, templates must be updated to handle new type patterns. Template bugs affect all generated code and can be difficult to diagnose.

7. **Version Coupling**: Generated SDKs are coupled to the specific version of the TypeScript source they were generated from. If a project needs to support multiple MCP protocol versions simultaneously, the generator must support version-aware generation, producing different types for different protocol versions. This adds significant complexity to the generation pipeline.

## Architecture

### mcp-forge Extended Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Extended mcp-forge Architecture                     │
├──────────────────────────────────────────────────────────────────────┘
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    mcp-forge CLI                                 │  │
│  │                                                                 │  │
│  │  Usage: mcp-forge generate [options]                            │  │
│  │                                                                 │  │
│  │  Options:                                                       │  │
│  │    --source <path>     TypeScript source directory              │  │
│  │    --target <lang>     Target language (python|go|rust|ts)      │  │
│  │    --output <path>     Output directory                         │  │
│  │    --template <path>   Custom template directory                │  │
│  │    --watch             Watch for source changes                 │  │
│  │    --dry-run           Show what would be generated             │  │
│  │    --validate          Validate generated code                  │  │
│  │                                                                 │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                               │                                       │
│  ┌────────────────────────────┼────────────────────────────────────┐  │
│  │                    Generation Pipeline                            │  │
│  │                                                                 │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │  │
│  │  │   Parser    │  │  Resolver   │  │  Intermediate           │  │  │
│  │  │             │  │             │  │  Representation         │  │  │
│  │  │ • TypeScript│  │ • Type      │  │                         │  │  │
│  │  │   AST walk  │  │   resolution│  │  ┌───────────────────┐  │  │  │
│  │  │ • Extract   │  │ • Reference │  │  │  IR Schema        │  │  │  │
│  │  │   types     │  │   tracking  │  │  │                   │  │  │  │
│  │  │ • Parse     │  │ • Cycle     │  │  │  types: [...]     │  │  │  │
│  │  │   JSDoc     │  │   detection │  │  │  methods: [...]   │  │  │  │
│  │  │ • Build AST │  │ • Import    │  │  │  enums: [...]     │  │  │  │
│  │  └─────────────┘  └─────────────┘  │  │  interfaces: [...]│  │  │  │
│  │                                    │  └───────────────────┘  │  │  │
│  │                                    └─────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                               │                                       │
│  ┌────────────────────────────┼────────────────────────────────────┐  │
│  │                    Language Backends                             │  │
│  │                                                                 │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │  │
│  │  │ Python       │  │ Go           │  │ Rust                 │   │  │
│  │  │ Backend      │  │ Backend      │  │ Backend              │   │  │
│  │  │              │  │              │  │                      │   │  │
│  │  │ • dataclass  │  │ • struct     │  │ • struct             │   │  │
│  │  │ • type hints │  │ • json tags  │  │ • serde              │   │  │
│  │  │ • docstrings │  │ • comments   │  │ • doc comments       │   │  │
│  │  │ • pydantic   │  │ • interfaces │  │ • enums              │   │  │
│  │  │   (optional) │  │ • methods    │  │ • traits             │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                               │                                       │
│  ┌────────────────────────────┼────────────────────────────────────┐  │
│  │                    Output & Validation                           │  │
│  │                                                                 │  │
│  │  ┌───────────────────────────────────────────────────────────┐  │  │
│  │  │  Output Formatter                                         │  │  │
│  │  │                                                           │  │  │
│  │  │  • Code formatting (black/gofmt/rustfmt)                  │  │  │
│  │  │  • Import organization                                    │  │  │
│  │  │  • File header comments                                   │  │  │
│  │  │  • Generation metadata annotations                        │  │  │
│  │  └───────────────────────────────────────────────────────────┘  │  │
│  │                                                                 │  │
│  │  ┌───────────────────────────────────────────────────────────┐  │  │
│  │  │  Validator                                                │  │  │
│  │  │                                                           │  │  │
│  │  │  • Type check (mypy/go vet/cargo check)                   │  │  │
│  │  │  • Lint (ruff/golangci-lint/clippy)                       │  │  │
│  │  │  • Protocol compliance check                              │  │  │
│  │  │  • Diff against committed generated code                  │  │  │
│  │  └───────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Implementation Details

### Generator Configuration

```yaml
# mcp-forge.yaml
generator:
  version: "1.0.0"

source:
  typescript_path: "node_modules/@modelcontextprotocol/sdk/dist/types.d.ts"
  protocol_path: "node_modules/@modelcontextprotocol/sdk/dist/protocol.d.ts"

targets:
  python:
    output: "python/pheno-mcp/types.py"
    template: "templates/python/"
    options:
      style: "dataclass"           # dataclass | pydantic
      include_docstrings: true
      include_type_hints: true
      format_with: "ruff"
      module_name: "pheno_mcp.types"

  go:
    output: "go/mcpkit-go/protocol/"
    template: "templates/go/"
    options:
      package_name: "protocol"
      include_comments: true
      json_tags: true
      format_with: "gofmt"

  rust:
    output: "rust/mcp-forge/internal/protocol/"
    template: "templates/rust/"
    options:
      crate_name: "mcp_protocol"
      include_doc_comments: true
      serde_derives: true
      format_with: "rustfmt"
```

### Type Mapping Table

| TypeScript | Python | Go | Rust |
|------------|--------|-----|------|
| `string` | `str` | `string` | `String` |
| `number` | `float` | `float64` | `f64` |
| `integer` | `int` | `int64` | `i64` |
| `boolean` | `bool` | `bool` | `bool` |
| `null` | `None` | `nil` | `()` |
| `T[]` | `list[T]` | `[]T` | `Vec<T>` |
| `Record<K, V>` | `dict[K, V]` | `map[K]V` | `HashMap<K, V>` |
| `T \| null` | `Optional[T]` | `*T` | `Option<T>` |
| `interface` | `@dataclass class` | `struct` | `struct` |
| `type alias` | `type alias` | `type` | `type` |
| `enum` | `Enum` | `const iota` | `enum` |
| Tagged union | `@dataclass` hierarchy | Interface + impls | `#[serde(tag)]` enum |
| `Date` | `datetime` | `time.Time` | `chrono::DateTime` |

## Code Examples

### Example 1: Running the Generator

```bash
# Generate all languages
mcp-forge generate --source ./node_modules/@modelcontextprotocol/sdk \
                   --target all \
                   --output ./generated

# Generate specific language
mcp-forge generate --source ./node_modules/@modelcontextprotocol/sdk \
                   --target python \
                   --output ./python/pheno-mcp/types.py

# Watch mode for development
mcp-forge generate --source ./node_modules/@modelcontextprotocol/sdk \
                   --target all \
                   --watch

# Validate generated code
mcp-forge generate --source ./node_modules/@modelcontextprotocol/sdk \
                   --target all \
                   --validate
```

### Example 2: Generated Python Output

```python
# Generated by mcp-forge from MCP TypeScript types
# DO NOT EDIT MANUALLY - regenerate with: mcp-forge generate --target python
# Source: @modelcontextprotocol/sdk v1.0.0
# Generated: 2026-04-03T12:00:00Z

"""MCP Protocol Types - Generated from TypeScript definitions."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Optional, Union
from datetime import datetime


@dataclass
class Implementation:
    """Identifies the client or server implementation."""
    name: str
    version: str


@dataclass
class Tool:
    """Definition for a tool the client can call."""
    name: str
    """The name of the tool."""
    input_schema: dict[str, Any]
    """A JSON Schema object defining the expected parameters."""
    description: Optional[str] = None
    """A human-readable description of the tool."""


@dataclass
class TextContent:
    """Text content for a message."""
    type: Literal["text"] = "text"
    text: str
    """The text content of the message."""


@dataclass
class ImageContent:
    """Image content for a message."""
    type: Literal["image"] = "image"
    data: str
    """Base64-encoded image data."""
    mime_type: str
    """The MIME type of the image."""


# Union type: Content = TextContent | ImageContent | ResourceContent
Content = Union[TextContent, ImageContent, "ResourceContent"]
```

### Example 3: Generated Go Output

```go
// Generated by mcp-forge from MCP TypeScript types
// DO NOT EDIT MANUALLY - regenerate with: mcp-forge generate --target go
// Source: @modelcontextprotocol/sdk v1.0.0
// Generated: 2026-04-03T12:00:00Z

package protocol

// Implementation identifies the client or server implementation.
type Implementation struct {
    Name    string `json:"name"`    // Name of the implementation
    Version string `json:"version"` // Version of the implementation
}

// Tool defines a tool the client can call.
type Tool struct {
    Name        string                 `json:"name"`                   // The name of the tool
    InputSchema map[string]interface{} `json:"inputSchema"`            // JSON Schema for parameters
    Description *string                `json:"description,omitempty"`  // Human-readable description
}

// Content represents the content of a message.
type Content interface {
    isContent()
}

// TextContent represents text content in a message.
type TextContent struct {
    Type string `json:"type"` // Always "text"
    Text string `json:"text"` // The text content
}

func (TextContent) isContent() {}

// ImageContent represents image content in a message.
type ImageContent struct {
    Type     string `json:"type"`     // Always "image"
    Data     string `json:"data"`     // Base64-encoded image data
    MimeType string `json:"mimeType"` // MIME type of the image
}

func (ImageContent) isContent() {}
```

### Example 4: CI/CD Integration

```yaml
# .github/workflows/generate-types.yml
name: Generate Protocol Types

on:
  push:
    paths:
      - "node_modules/@modelcontextprotocol/sdk/**"
      - "rust/mcp-forge/**"
  workflow_dispatch:

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: "1.24"

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Setup Rust
        uses: dtolnay/rust-toolchain@stable

      - name: Generate types
        run: |
          cd rust/mcp-forge
          go run ./cmd/generate --source ../../node_modules/@modelcontextprotocol/sdk \
                                --target all \
                                --output ../../generated

      - name: Validate Python
        run: |
          cd python/pheno-mcp
          ruff check src/pheno_mcp/types.py
          python -c "import pheno_mcp.types"

      - name: Validate Go
        run: |
          cd go/mcpkit-go
          go vet ./protocol/
          go build ./...

      - name: Validate Rust
        run: |
          cd rust/mcp-forge
          cargo check

      - name: Check for changes
        run: |
          if [[ -n $(git status --porcelain) ]]; then
            echo "Generated files are out of date. Run: mcp-forge generate --target all"
            git diff
            exit 1
          fi
```

## Cross-References

- **SPEC.md** — Section 3: Core Protocol (protocol types and message structures)
- **SOTA.md** — Section 5: Official MCP SDK Implementations (TypeScript as source of truth)
- **ADR-001** — MCP Transport Layer (transport type generation)
- **ADR-002** — Tool Registry Design (tool definition type generation)
- **rust/mcp-forge/** — Existing generator implementation
- **rust/mcp-forge/cmd/generate/** — Generator command entry point
- **rust/mcp-forge/internal/protocol/** — Generated Rust protocol types

---

*Document Version: 1.0*  
*Total Lines: 400+*  
*Proposal Date: 2026-04-03*
