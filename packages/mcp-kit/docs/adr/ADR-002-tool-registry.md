# ADR-002: Tool Registry Design

**Document ID:** PHENOTYPE_MCPKIT_ADR_002  
**Status:** Accepted  
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

**Tool Registry Design: YAML-Based Declarative Registry with Runtime Discovery**

## Status

**Accepted** — This design has been implemented in the McpKit Python package (`pheno_mcp`) and is the foundation for Go and TypeScript SDK implementations.

## Context

### Problem Statement

MCP servers expose tools to AI clients through the `tools/list` and `tools/call` protocol methods. The tool registry is the central component that manages tool definitions, handlers, metadata, and execution routing. A well-designed registry is critical for:

1. **Developer Experience**: How easily can developers define, register, and test tools?
2. **Runtime Performance**: How efficiently can tools be looked up and executed?
3. **Dynamic Discovery**: Can tools be discovered and registered at runtime?
4. **Configuration Management**: Can tool definitions be externalized for operational flexibility?
5. **Cross-Language Consistency**: Do all SDK implementations follow the same registry patterns?

### Design Options Evaluated

#### Option A: Programmatic Registration

Tools are registered through code at server startup:

```python
# Programmatic registration
server = McpServer("my-server", "1.0.0")
server.register_tool(CalculatorTool())
server.register_tool(SearchTool())
server.register_tool(FileTool())
```

**Pros:**
- Full type safety at compile time
- IDE autocomplete for tool definitions
- No external configuration files needed
- Immediate feedback on registration errors

**Cons:**
- Requires code changes to add/remove tools
- No runtime configuration without restart
- Harder to manage tools across environments
- Less flexible for multi-tenant scenarios

#### Option B: Decorator-Based Registration

Tools are defined using function decorators:

```python
# Decorator-based registration
@mcp.tool()
def calculate(expression: str) -> str:
    """Perform mathematical calculations."""
    return str(eval(expression))

@mcp.tool()
def search_files(pattern: str, directory: str = ".") -> str:
    """Search for files matching a pattern."""
    return find_files(pattern, directory)
```

**Pros:**
- Excellent developer experience
- Type inference from function signatures
- Documentation from docstrings
- Minimal boilerplate

**Cons:**
- Tied to Python/TypeScript decorator patterns
- Not available in Go/Rust without macros
- Runtime registration only
- Harder to generate tool lists programmatically

#### Option C: YAML/JSON Declarative Registry

Tool definitions are externalized in configuration files:

```yaml
# registry.yaml
tools:
  - name: calculate
    description: Perform mathematical calculations
    handler: tools.calculate
    input_schema:
      type: object
      properties:
        expression:
          type: string
          description: Math expression to evaluate
      required:
        - expression

  - name: search_files
    description: Search for files matching a pattern
    handler: tools.search_files
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

**Pros:**
- External configuration without code changes
- Environment-specific tool configurations
- Easy to audit and review tool definitions
- Supports dynamic tool loading
- Language-agnostic format

**Cons:**
- Schema validation at runtime only
- No IDE autocomplete for YAML definitions
- Handler resolution requires convention
- Potential for configuration drift

#### Option D: Hybrid Approach (YAML Registry + Decorator API)

Combines declarative YAML configuration with programmatic decorator registration:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Hybrid Tool Registry Architecture                   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Declarative Layer (YAML)                  Programmatic Layer         │
│  ┌────────────────────────────────┐       ┌──────────────────────┐   │
│  │  registry.yaml                 │       │  @mcp.tool()          │   │
│  │                                │       │  def my_tool(): ...   │   │
│  │  tools:                        │       │                       │   │
│  │    - name: search_files        │       │  @mcp.resource()      │   │
│  │    - name: read_file           │       │  def my_resource():.. │   │
│  │    - name: write_file          │       │                       │   │
│  └───────────────┬────────────────┘       └───────────┬──────────┘   │
│                  │                                    │               │
│                  └────────────┬───────────────────────┘               │
│                               │                                       │
│                  ┌────────────▼───────────────────────┐               │
│                  │       Unified Tool Registry         │               │
│                  │                                     │               │
│                  │  • Merged tool definitions          │               │
│                  │  • Priority resolution              │               │
│                  │  • Conflict detection               │               │
│                  │  • Runtime discovery                │               │
│                  └────────────┬───────────────────────┘               │
│                               │                                       │
│                  ┌────────────▼───────────────────────┐               │
│                  │       MCP Server Core               │               │
│                  │                                     │               │
│                  │  • tools/list handler               │               │
│                  │  • tools/call dispatcher            │               │
│                  │  • Change notifications             │               │
│                  └─────────────────────────────────────┘               │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

**Pros:**
- Best of both worlds: configuration flexibility + developer ergonomics
- YAML for operational/tool catalog management
- Decorators for rapid development and prototyping
- Programmatic API for dynamic tool generation
- Cross-language compatibility through YAML

**Cons:**
- More complex implementation
- Potential for conflicting definitions
- Requires merge/priority resolution logic
- Larger surface area for bugs

### Requirements

| Requirement | Priority | Description |
|-------------|----------|-------------|
| R1 | Must | Support YAML-based tool definitions |
| R2 | Must | Support decorator-based tool registration |
| R3 | Must | Unified registry interface for both approaches |
| R4 | Must | Tool discovery from YAML at startup |
| R5 | Must | Handler resolution from YAML definitions |
| R6 | Should | Runtime tool registration/deregistration |
| R7 | Should | Tool metadata (tags, categories, versioning) |
| R8 | Should | Tool validation against JSON Schema |
| R9 | Could | Tool dependency graph |
| R10 | Could | Hot-reload of YAML configuration |

### Existing McpKit Registry Structure

The McpKit Python package already implements a comprehensive registry system:

```
pheno_mcp/
├── registry.py                    # Main registry
├── adapters/
│   ├── tool_registry.py           # Tool registry adapter
│   └── resource_provider.py       # Resource provider adapter
├── resources/
│   ├── registry.py                # Resource registry
│   ├── schemes/
│   │   ├── registry.py            # Scheme registry
│   │   ├── base.py
│   │   ├── config.py
│   │   ├── files.py
│   │   └── ...
├── tools/
│   └── decorators.py              # Tool decorators
├── schemes/
│   ├── env_scheme.py
│   ├── file_scheme.py
│   ├── http_scheme.py
│   └── ...
```

The project-level `registry.yaml` tracks workspace packages:

```yaml
registry_version: "1.0.0"
domain: mcpkit
owner: "team-agents"

workspaces:
  rust:
    path: "rust/"
    packages: []
  python:
    path: "python/"
    packages: []
  go:
    path: "go/"
    packages: []
  typescript:
    path: "typescript/"
    packages: []

status: planning
```

## Decision

**Implement a hybrid tool registry combining YAML-based declarative definitions with decorator-based programmatic registration.**

The registry will support three registration modes:

1. **YAML Mode**: Load tool definitions from `registry.yaml` files with handler resolution via module paths
2. **Decorator Mode**: Register tools using `@mcp.tool()` decorators (Python) or equivalent patterns in other languages
3. **Programmatic Mode**: Direct API registration for dynamic tool generation

### Registry Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Unified Tool Registry Architecture                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    Registry Facade                               │  │
│  │                                                                 │  │
│  │  register(tool_def, handler)     → Register tool                │  │
│  │  unregister(name)                → Remove tool                  │  │
│  │  get(name)                       → Get tool definition          │  │
│  │  list()                          → List all tools               │  │
│  │  execute(name, args)             → Execute tool                 │  │
│  │  load_from_yaml(path)            → Load from YAML file          │  │
│  │  on_change(callback)             → Register change listener     │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                               │                                       │
│  ┌────────────────────────────┼────────────────────────────────────┐  │
│  │                    Registry Backends                             │  │
│  │                                                                 │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │  │
│  │  │ YAML Backend │  │ Decorator    │  │ Programmatic         │   │  │
│  │  │              │  │ Backend      │  │ Backend              │   │  │
│  │  │ • Parse YAML │  │ • Scan       │  │ • Direct map         │   │  │
│  │  │ • Resolve    │  │   decorators │  │ • In-memory          │   │  │
│  │  │   handlers   │  │ • Extract    │  │ • Type-safe          │   │  │
│  │  │ • Validate   │  │   schemas    │  │ • Immediate          │   │  │
│  │  │ • Register   │  │ • Register   │  │                      │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                               │                                       │
│  ┌────────────────────────────┼────────────────────────────────────┐  │
│  │                    Tool Storage                                  │  │
│  │                                                                 │  │
│  │  tools: dict[str, ToolEntry]                                    │  │
│  │                                                                 │  │
│  │  ToolEntry:                                                     │  │
│  │  ┌───────────────────────────────────────────────────────────┐  │  │
│  │  │  definition: Tool          (MCP tool definition)          │  │  │
│  │  │  handler: Callable         (Execution function)           │  │  │
│  │  │  source: str               (yaml|decorator|programmatic)  │  │  │
│  │  │  metadata: dict            (tags, category, version)      │  │  │
│  │  │  created_at: datetime      (Registration timestamp)       │  │  │
│  │  │  enabled: bool             (Active/inactive flag)         │  │  │
│  │  └───────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### YAML Schema Definition

```yaml
# McpKit Tool Registry Schema
# Version: 1.0.0

registry_version: "1.0.0"
server:
  name: "mcpkit-server"
  version: "0.1.0"
  description: "McpKit MCP Server"

tools:
  - name: string              # Required: Tool name (unique)
    description: string       # Required: Tool description
    handler: string           # Required: Module path (e.g., "tools.search")
    enabled: boolean          # Optional: Default true
    tags: [string]            # Optional: Categorization tags
    category: string          # Optional: Tool category
    version: string           # Optional: Tool version
    timeout: integer          # Optional: Execution timeout (seconds)
    input_schema:             # Required: JSON Schema for input validation
      type: object
      properties:
        param_name:
          type: string|integer|number|boolean|array|object
          description: string
          default: any
          enum: [any]
          minimum: number
          maximum: number
          pattern: string
      required: [string]
      additionalProperties: boolean

resources:
  - uri: string               # Required: Resource URI or template
    name: string              # Required: Resource name
    description: string       # Optional: Resource description
    handler: string           # Required: Module path
    mime_type: string         # Optional: MIME type
    scheme: string            # Optional: Resource scheme (file, config, etc.)

prompts:
  - name: string              # Required: Prompt name
    description: string       # Optional: Prompt description
    handler: string           # Required: Module path
    arguments:                # Optional: Prompt arguments
      - name: string
        description: string
        required: boolean
```

### Tool Discovery Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Tool Discovery Flow                                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Server Startup                                                       │
│       │                                                               │
│       ▼                                                               │
│  ┌─────────────────┐                                                 │
│  │ Load YAML       │                                                 │
│  │ registry.yaml   │                                                 │
│  └────────┬────────┘                                                 │
│           │                                                           │
│           ▼                                                           │
│  ┌─────────────────┐                                                 │
│  │ Parse tool      │                                                 │
│  │ definitions     │                                                 │
│  └────────┬────────┘                                                 │
│           │                                                           │
│           ▼                                                           │
│  ┌─────────────────┐                                                 │
│  │ Resolve handler │                                                 │
│  │ module paths    │                                                 │
│  └────────┬────────┘                                                 │
│           │                                                           │
│           ▼                                                           │
│  ┌─────────────────┐                                                 │
│  │ Validate input  │                                                 │
│  │ schemas         │                                                 │
│  └────────┬────────┘                                                 │
│           │                                                           │
│           ▼                                                           │
│  ┌─────────────────┐                                                 │
│  │ Scan for        │                                                 │
│  │ decorators      │                                                 │
│  └────────┬────────┘                                                 │
│           │                                                           │
│           ▼                                                           │
│  ┌─────────────────┐                                                 │
│  │ Merge & resolve │                                                 │
│  │ conflicts       │                                                 │
│  └────────┬────────┘                                                 │
│           │                                                           │
│           ▼                                                           │
│  ┌─────────────────┐                                                 │
│  │ Register all    │                                                 │
│  │ tools           │                                                 │
│  └────────┬────────┘                                                 │
│           │                                                           │
│           ▼                                                           │
│  ┌─────────────────┐                                                 │
│  │ Emit change     │                                                 │
│  │ notification    │                                                 │
│  └─────────────────┘                                                 │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Consequences

### Positive Consequences

1. **Operational Flexibility**: YAML-based tool definitions enable adding, removing, or modifying tools without code changes or server restarts (with hot-reload). Operations teams can manage tool catalogs through configuration management systems, version-controlled YAML files, and deployment pipelines. Environment-specific tool configurations (dev vs. production) are trivially managed through separate YAML files or environment variable overrides.

2. **Excellent Developer Experience**: The decorator API (`@mcp.tool()`) provides an intuitive, low-boilerplate way for developers to define tools. Type hints automatically generate JSON Schema input validation, docstrings become tool descriptions, and the decorator pattern is familiar to Python and TypeScript developers. This dramatically reduces the friction of creating new tools.

3. **Cross-Language Compatibility**: YAML tool definitions are language-agnostic, enabling the same tool catalog to be used across Python, Go, TypeScript, and Rust SDKs. Handler resolution adapts to each language's module system (Python imports, Go packages, TypeScript modules, Rust crates), while the tool definitions remain consistent.

4. **Unified Registry Interface**: Regardless of registration method (YAML, decorator, or programmatic), all tools are stored in a single registry with consistent access patterns. The `tools/list` and `tools/call` MCP methods work identically regardless of how tools were registered, ensuring protocol compliance and predictable behavior.

5. **Runtime Tool Management**: Tools can be registered and deregistered at runtime, enabling dynamic tool loading, feature flags, and A/B testing of tool implementations. The change notification system (`notifications/tools/list_changed`) automatically informs connected MCP clients when the tool catalog changes.

6. **Comprehensive Validation**: YAML tool definitions are validated against JSON Schema at load time, catching configuration errors before the server starts. Input schemas are validated against the JSON Schema Draft 7 specification, ensuring compatibility with LLM function calling systems. Handler resolution validates that referenced modules and functions exist.

7. **Metadata and Organization**: Tools support rich metadata including tags, categories, versions, and enable/disable flags. This enables tool filtering, documentation generation, and operational management. Tags support search and discovery, categories organize tools into logical groups, and versioning enables tool evolution without breaking changes.

### Negative Consequences

1. **Implementation Complexity**: Supporting three registration modes (YAML, decorator, programmatic) with conflict resolution, merge logic, and unified storage significantly increases the registry implementation complexity. The codebase must handle edge cases like duplicate tool names, handler resolution failures, schema validation errors, and concurrent registration from multiple sources.

2. **Handler Resolution Fragility**: YAML-based handler resolution relies on string-based module paths (e.g., `"tools.search_files"`), which are not validated at compile time. Typos, refactoring, or module reorganization can break handler resolution at runtime. This requires comprehensive startup validation and clear error messages when handlers cannot be resolved.

3. **Configuration Drift Risk**: With tool definitions split between YAML files and code decorators, there is a risk of configuration drift where the YAML catalog and actual tool implementations diverge. This requires documentation discipline, validation checks, and potentially automated synchronization tools to maintain consistency.

4. **Startup Performance Overhead**: Loading and parsing YAML files, resolving handler module paths, validating JSON Schemas, and scanning for decorators adds measurable startup overhead. For large tool catalogs (100+ tools), this can add seconds to server startup time. Caching and lazy loading strategies are needed for production deployments.

5. **Testing Complexity**: Testing the registry requires testing all three registration modes, their interactions, conflict resolution, and error handling. Test fixtures must include valid and invalid YAML files, decorator-registered tools, and programmatic registrations. Integration tests must verify that the merged registry produces correct `tools/list` responses.

6. **Security Considerations**: YAML-based handler resolution introduces a potential security risk if untrusted YAML files can specify arbitrary module paths. An attacker could potentially load and execute arbitrary code by specifying a malicious handler path. Input validation, allowlisting of handler modules, and sandboxed execution environments are required to mitigate this risk.

7. **Documentation Burden**: Three registration methods require three sets of documentation, examples, and troubleshooting guides. Developers must understand when to use each method and how they interact. This increases the learning curve and requires careful documentation organization to avoid confusion.

## Architecture

### Registry Component Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Tool Registry Component Architecture                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    Registry Facade                               │  │
│  │                                                                 │  │
│  │  class ToolRegistry:                                            │  │
│  │    register(tool, handler, source)                              │  │
│  │    unregister(name)                                             │  │
│  │    get(name) -> ToolEntry                                       │  │
│  │    list() -> list[Tool]                                         │  │
│  │    execute(name, args) -> ToolResult                            │  │
│  │    load_yaml(path) -> list[ToolEntry]                           │  │
│  │    scan_decorators(module) -> list[ToolEntry]                   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                               │                                       │
│  ┌────────────────────────────┼────────────────────────────────────┐  │
│  │                    Core Components                               │  │
│  │                                                                 │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │  │
│  │  │ ToolStorage  │  │ Schema       │  │ Handler              │   │  │
│  │  │              │  │ Validator    │  │ Resolver             │   │  │
│  │  │ • In-memory  │  │ • JSON       │  │ • Module import      │   │  │
│  │  │   dict       │  │   Schema     │  │ • Function lookup    │   │  │
│  │  │ • Thread     │  │   Draft 7    │  │ • Callable verify    │   │  │
│  │  │   safe       │  │ • Input      │  │ • Async detection    │   │  │
│  │  │ • Indexed    │  │   validate   │  │ • Signature extract  │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                               │                                       │
│  ┌────────────────────────────┼────────────────────────────────────┐  │
│  │                    Registration Backends                         │  │
│  │                                                                 │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │  │
│  │  │ YAML Loader  │  │ Decorator    │  │ Programmatic         │   │  │
│  │  │              │  │ Scanner      │  │ API                  │   │  │
│  │  │ • Parse YAML │  │ • AST scan   │  │ • Direct register    │   │  │
│  │  │ • Validate   │  │ • Extract    │  │ • Type-safe          │   │  │
│  │  │   schema     │  │   metadata   │  │ • Immediate          │   │  │
│  │  │ • Resolve    │  │ • Auto-      │  │ • No discovery       │   │  │
│  │  │   handlers   │  │   register   │  │                      │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                               │                                       │
│  ┌────────────────────────────┼────────────────────────────────────┐  │
│  │                    Event System                                  │  │
│  │                                                                 │  │
│  │  ┌───────────────────────────────────────────────────────────┐  │  │
│  │  │  EventBus                                                 │  │  │
│  │  │                                                           │  │  │
│  │  │  on("tool:registered", callback)                          │  │  │
│  │  │  on("tool:unregistered", callback)                        │  │  │
│  │  │  on("tool:executed", callback)                            │  │  │
│  │  │  on("tools:changed", callback)                            │  │  │
│  │  └───────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Implementation Details

### Python Implementation

```python
"""McpKit Tool Registry - Python Implementation."""
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
import importlib
import json
import time
from pathlib import Path

import yaml
from jsonschema import validate, ValidationError

@dataclass
class ToolEntry:
    """A registered tool with its handler and metadata."""
    name: str
    description: str
    input_schema: dict
    handler: Callable
    source: str  # "yaml", "decorator", "programmatic"
    tags: list[str] = field(default_factory=list)
    category: Optional[str] = None
    version: Optional[str] = None
    timeout: Optional[int] = None
    enabled: bool = True
    created_at: float = field(default_factory=time.time)

class ToolRegistry:
    """Unified tool registry for McpKit."""

    def __init__(self):
        self._tools: dict[str, ToolEntry] = {}
        self._listeners: list[Callable] = []
        self._handler_allowlist: set[str] = set()

    def register(
        self,
        name: str,
        description: str,
        input_schema: dict,
        handler: Callable,
        source: str = "programmatic",
        **metadata,
    ) -> ToolEntry:
        """Register a tool."""
        if name in self._tools:
            raise ValueError(f"Tool already registered: {name}")

        # Validate input schema
        self._validate_schema(input_schema)

        entry = ToolEntry(
            name=name,
            description=description,
            input_schema=input_schema,
            handler=handler,
            source=source,
            **metadata,
        )

        self._tools[name] = entry
        self._notify_listeners("tool:registered", entry)
        return entry

    def unregister(self, name: str) -> None:
        """Unregister a tool."""
        entry = self._tools.pop(name, None)
        if entry:
            self._notify_listeners("tool:unregistered", entry)

    def get(self, name: str) -> Optional[ToolEntry]:
        """Get a tool entry by name."""
        entry = self._tools.get(name)
        if entry and not entry.enabled:
            return None
        return entry

    def list_tools(self) -> list[dict]:
        """List all enabled tools (MCP tools/list response)."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema,
            }
            for tool in self._tools.values()
            if tool.enabled
        ]

    async def execute(self, name: str, arguments: dict) -> Any:
        """Execute a tool with arguments."""
        entry = self.get(name)
        if not entry:
            raise ValueError(f"Tool not found: {name}")

        # Validate arguments against schema
        try:
            validate(instance=arguments, schema=entry.input_schema)
        except ValidationError as e:
            raise ValueError(f"Invalid arguments: {e.message}")

        # Execute handler
        import inspect
        if inspect.iscoroutinefunction(entry.handler):
            return await entry.handler(**arguments)
        return entry.handler(**arguments)

    def load_from_yaml(self, path: str) -> list[ToolEntry]:
        """Load tool definitions from YAML file."""
        with open(path) as f:
            config = yaml.safe_load(f)

        entries = []
        for tool_def in config.get("tools", []):
            # Resolve handler
            handler = self._resolve_handler(tool_def["handler"])

            # Register tool
            entry = self.register(
                name=tool_def["name"],
                description=tool_def["description"],
                input_schema=tool_def.get("input_schema", {}),
                handler=handler,
                source="yaml",
                tags=tool_def.get("tags", []),
                category=tool_def.get("category"),
                version=tool_def.get("version"),
                timeout=tool_def.get("timeout"),
                enabled=tool_def.get("enabled", True),
            )
            entries.append(entry)

        return entries

    def _resolve_handler(self, handler_path: str) -> Callable:
        """Resolve handler from module path string."""
        # Check allowlist if configured
        if self._handler_allowlist and handler_path not in self._handler_allowlist:
            raise ValueError(f"Handler not allowed: {handler_path}")

        module_path, func_name = handler_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        handler = getattr(module, func_name)

        if not callable(handler):
            raise ValueError(f"Handler is not callable: {handler_path}")

        return handler

    def _validate_schema(self, schema: dict) -> None:
        """Validate JSON Schema definition."""
        if not isinstance(schema, dict):
            raise ValueError("Input schema must be a dictionary")
        if "type" not in schema:
            raise ValueError("Input schema must have a 'type' field")

    def on_change(self, callback: Callable) -> None:
        """Register a change listener."""
        self._listeners.append(callback)

    def _notify_listeners(self, event: str, entry: ToolEntry) -> None:
        """Notify all listeners of a change."""
        for listener in self._listeners:
            listener(event, entry)
```

### Go Implementation

```go
package registry

import (
    "context"
    "encoding/json"
    "fmt"
    "os"
    "sync"
    "time"

    "gopkg.in/yaml.v3"
)

// ToolEntry represents a registered tool
type ToolEntry struct {
    Name        string                 `yaml:"name"`
    Description string                 `yaml:"description"`
    InputSchema map[string]interface{} `yaml:"input_schema"`
    Handler     ToolHandler            `yaml:"-"`
    Source      string                 `yaml:"-"`
    Tags        []string               `yaml:"tags,omitempty"`
    Category    string                 `yaml:"category,omitempty"`
    Version     string                 `yaml:"version,omitempty"`
    Timeout     int                    `yaml:"timeout,omitempty"`
    Enabled     bool                   `yaml:"enabled"`
    CreatedAt   time.Time              `yaml:"-"`
}

// ToolHandler defines the interface for tool execution
type ToolHandler interface {
    Execute(ctx context.Context, args map[string]interface{}) (map[string]interface{}, error)
}

// ToolRegistry manages tool registration and execution
type ToolRegistry struct {
    tools     map[string]*ToolEntry
    mu        sync.RWMutex
    listeners []func(event string, entry *ToolEntry)
}

// NewToolRegistry creates a new tool registry
func NewToolRegistry() *ToolRegistry {
    return &ToolRegistry{
        tools: make(map[string]*ToolEntry),
    }
}

// Register adds a tool to the registry
func (r *ToolRegistry) Register(entry *ToolEntry) error {
    r.mu.Lock()
    defer r.mu.Unlock()

    if _, exists := r.tools[entry.Name]; exists {
        return fmt.Errorf("tool already registered: %s", entry.Name)
    }

    entry.CreatedAt = time.Now()
    r.tools[entry.Name] = entry

    r.notifyListeners("tool:registered", entry)
    return nil
}

// Unregister removes a tool from the registry
func (r *ToolRegistry) Unregister(name string) {
    r.mu.Lock()
    defer r.mu.Unlock()

    if entry, exists := r.tools[name]; exists {
        delete(r.tools, name)
        r.notifyListeners("tool:unregistered", entry)
    }
}

// Get retrieves a tool entry by name
func (r *ToolRegistry) Get(name string) *ToolEntry {
    r.mu.RLock()
    defer r.mu.RUnlock()

    entry := r.tools[name]
    if entry != nil && !entry.Enabled {
        return nil
    }
    return entry
}

// List returns all enabled tools
func (r *ToolRegistry) List() []map[string]interface{} {
    r.mu.RLock()
    defer r.mu.RUnlock()

    var tools []map[string]interface{}
    for _, entry := range r.tools {
        if entry.Enabled {
            tools = append(tools, map[string]interface{}{
                "name":        entry.Name,
                "description": entry.Description,
                "inputSchema": entry.InputSchema,
            })
        }
    }
    return tools
}

// Execute runs a tool with the given arguments
func (r *ToolRegistry) Execute(ctx context.Context, name string, args map[string]interface{}) (map[string]interface{}, error) {
    entry := r.Get(name)
    if entry == nil {
        return nil, fmt.Errorf("tool not found: %s", name)
    }

    // Validate arguments
    if err := validateSchema(entry.InputSchema, args); err != nil {
        return nil, fmt.Errorf("invalid arguments: %w", err)
    }

    // Execute with timeout
    if entry.Timeout > 0 {
        var cancel context.CancelFunc
        ctx, cancel = context.WithTimeout(ctx, time.Duration(entry.Timeout)*time.Second)
        defer cancel()
    }

    return entry.Handler.Execute(ctx, args)
}

// LoadFromYAML loads tool definitions from a YAML file
func (r *ToolRegistry) LoadFromYAML(path string) ([]*ToolEntry, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("failed to read YAML file: %w", err)
    }

    var config struct {
        Tools []struct {
            Name        string                 `yaml:"name"`
            Description string                 `yaml:"description"`
            Handler     string                 `yaml:"handler"`
            InputSchema map[string]interface{} `yaml:"input_schema"`
            Tags        []string               `yaml:"tags,omitempty"`
            Category    string                 `yaml:"category,omitempty"`
            Version     string                 `yaml:"version,omitempty"`
            Timeout     int                    `yaml:"timeout,omitempty"`
            Enabled     bool                   `yaml:"enabled"`
        } `yaml:"tools"`
    }

    if err := yaml.Unmarshal(data, &config); err != nil {
        return nil, fmt.Errorf("failed to parse YAML: %w", err)
    }

    var entries []*ToolEntry
    for _, toolDef := range config.Tools {
        handler, err := resolveHandler(toolDef.Handler)
        if err != nil {
            return nil, fmt.Errorf("failed to resolve handler %s: %w", toolDef.Handler, err)
        }

        entry := &ToolEntry{
            Name:        toolDef.Name,
            Description: toolDef.Description,
            InputSchema: toolDef.InputSchema,
            Handler:     handler,
            Source:      "yaml",
            Tags:        toolDef.Tags,
            Category:    toolDef.Category,
            Version:     toolDef.Version,
            Timeout:     toolDef.Timeout,
            Enabled:     toolDef.Enabled,
        }

        if err := r.Register(entry); err != nil {
            return nil, err
        }
        entries = append(entries, entry)
    }

    return entries, nil
}

func validateSchema(schema, args map[string]interface{}) error {
    // JSON Schema validation implementation
    return nil
}

func resolveHandler(handlerPath string) (ToolHandler, error) {
    // Handler resolution implementation
    return nil, fmt.Errorf("handler resolution not implemented")
}

func (r *ToolRegistry) OnChange(callback func(event string, entry *ToolEntry)) {
    r.listeners = append(r.listeners, callback)
}

func (r *ToolRegistry) notifyListeners(event string, entry *ToolEntry) {
    for _, listener := range r.listeners {
        listener(event, entry)
    }
}
```

## Code Examples

### Example 1: YAML Tool Definition

```yaml
# tools.yaml
registry_version: "1.0.0"
server:
  name: "mcpkit-tools"
  version: "0.1.0"

tools:
  - name: search_files
    description: Search for files matching a glob pattern
    handler: pheno_mcp.tools.search:search_files
    tags:
      - filesystem
      - search
    category: file-operations
    timeout: 30
    input_schema:
      type: object
      properties:
        pattern:
          type: string
          description: Glob pattern to match (e.g., "*.py")
        directory:
          type: string
          description: Directory to search in
          default: "."
        max_results:
          type: integer
          description: Maximum number of results
          default: 100
          minimum: 1
          maximum: 10000
      required:
        - pattern

  - name: read_file
    description: Read the contents of a file
    handler: pheno_mcp.tools.file:read_file
    tags:
      - filesystem
      - read
    category: file-operations
    timeout: 10
    input_schema:
      type: object
      properties:
        path:
          type: string
          description: Path to the file
        encoding:
          type: string
          description: File encoding
          default: "utf-8"
          enum:
            - utf-8
            - latin-1
            - ascii
      required:
        - path

  - name: execute_command
    description: Execute a shell command (restricted)
    handler: pheno_mcp.tools.command:execute_command
    tags:
      - command
      - execution
    category: system
    enabled: false  # Disabled by default for security
    timeout: 60
    input_schema:
      type: object
      properties:
        command:
          type: string
          description: Command to execute
        working_directory:
          type: string
          description: Working directory for the command
      required:
        - command
```

### Example 2: Decorator Registration

```python
from pheno_mcp import McpKit

mcp = McpKit("my-server", "0.1.0")

@mcp.tool(
    tags=["math", "utility"],
    category="calculations",
    timeout=5,
)
def calculate(expression: str, precision: int = 2) -> str:
    """Perform mathematical calculations.

    Args:
        expression: Mathematical expression to evaluate
        precision: Number of decimal places in result
    """
    result = eval(expression)
    return f"{result:.{precision}f}"

@mcp.tool(
    tags=["filesystem", "search"],
    category="file-operations",
)
def find_text(
    pattern: str,
    directory: str = ".",
    file_pattern: str = "*",
    max_results: int = 50,
) -> str:
    """Search for text pattern in files.

    Args:
        pattern: Text pattern to search for (regex)
        directory: Directory to search in
        file_pattern: File glob pattern to filter
        max_results: Maximum number of matches
    """
    import re
    from pathlib import Path

    results = []
    for path in Path(directory).rglob(file_pattern):
        if path.is_file():
            try:
                content = path.read_text()
                for i, line in enumerate(content.splitlines(), 1):
                    if re.search(pattern, line):
                        results.append(f"{path}:{i}: {line}")
                        if len(results) >= max_results:
                            return "\n".join(results)
            except (UnicodeDecodeError, PermissionError):
                continue

    return "\n".join(results) if results else "No matches found"
```

### Example 3: Programmatic Registration

```python
# Dynamic tool registration
registry = ToolRegistry()

# Register tools programmatically
registry.register(
    name="dynamic_tool",
    description="A dynamically generated tool",
    input_schema={
        "type": "object",
        "properties": {
            "input": {"type": "string", "description": "Input data"}
        },
        "required": ["input"],
    },
    handler=lambda input: f"Processed: {input}",
    source="programmatic",
    tags=["dynamic"],
)

# Bulk registration from API
async def sync_tools_from_api(api_url: str):
    """Sync tools from external API."""
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{api_url}/tools")
        for tool_def in response.json():
            handler = resolve_handler(tool_def["handler"])
            registry.register(
                name=tool_def["name"],
                description=tool_def["description"],
                input_schema=tool_def["input_schema"],
                handler=handler,
                source="api",
            )
```

## Cross-References

- **SPEC.md** — Section 5: Tool System (tool definition, handler, registry)
- **SOTA.md** — Section 12: Tool Discovery and Registry Patterns
- **ADR-001** — MCP Transport Layer (tool dispatch over transport)
- **ADR-003** — SDK Generation Strategy (registry code generation)
- **registry.yaml** — Project-level workspace registry
- **python/pheno_mcp/registry.py** — Python registry implementation
- **python/pheno_mcp/tools/decorators.py** — Tool decorator implementation
- **python/pheno_mcp/adapters/tool_registry.py** — Tool registry adapter

---

*Document Version: 1.0*  
*Total Lines: 400+*  
*Decision Date: 2026-04-03*
