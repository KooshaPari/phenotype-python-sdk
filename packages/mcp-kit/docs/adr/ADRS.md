# McpKit ADRs

## ADR 001: MCP Protocol Implementation with JSON-RPC 2.0

### Status: Accepted

### Context

The Model Context Protocol requires a standardized communication mechanism. Options:
- gRPC: Fast, but requires schema compilation
- REST: Simple, but less efficient for bidirectional
- GraphQL: Flexible, but complex for this use case
- JSON-RPC 2.0: Lightweight, widely supported, standard

### Decision

Use JSON-RPC 2.0 as the protocol foundation:

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JsonRpcRequest {
    pub jsonrpc: String,
    pub id: JsonRpcId,
    pub method: String,
    pub params: Option<serde_json::Value>,
}
```

### Consequences

#### Positive

1. **Standard**: Well-defined specification
2. **Simple**: Easy to implement and debug
3. **Batched**: Supports request batching
4. **Error handling**: Built-in error codes

#### Negative

1. **Verbosity**: JSON overhead vs binary protocols
2. **No streaming**: Requires SSE or WebSockets for streaming
3. **Type safety**: Runtime parameter validation

---

## ADR 002: Dual Transport Support (SSE and stdio)

### Status: Accepted

### Context

MCP servers need to support multiple deployment scenarios:
- Local tools: stdio transport via process spawning
- Remote services: SSE for HTTP-based communication
- IDE integration: Often uses stdio
- Cloud deployment: Requires SSE

### Decision

Implement both SSE and stdio transports with unified trait:

```rustn#[async_trait]
pub trait Transport: Send + Sync {
    async fn send(&self, message: JsonRpcMessage) -> Result<(), TransportError>;
    async fn receive(&mut self) -> Result<JsonRpcMessage, TransportError>;
}

pub struct SseTransport { /* ... */ }
pub struct StdioTransport { /* ... */ }
```

### Consequences

#### Positive

1. **Flexibility**: Works in any deployment scenario
2. **Testing**: stdio for unit tests
3. **Production**: SSE for distributed systems
4. **Fallback**: Either transport available

#### Negative

1. **Complexity**: Two implementations to maintain
2. **Testing**: Must test both transports
3. **Documentation**: More examples needed

---

## ADR 003: Async-First Server Architecture

### Status: Accepted

### Context

Tool execution often involves I/O (filesystem, network, databases). Synchronous execution blocks the server and limits concurrency.

### Decision

Implement async-first architecture with tokio:

```rust
#[async_trait]
pub trait ToolHandler: Send + Sync {
    async fn execute(&self, arguments: serde_json::Value) -> Result<ToolResult, ToolError>;
}

pub struct McpServer {
    tools: ToolRegistry,
    runtime: Arc<tokio::runtime::Runtime>,
}

impl McpServer {
    pub async fn handle_request(&self, request: JsonRpcRequest) -> JsonRpcResponse {
        match request.method.as_str() {
            "tools/call" => {
                let result = self.tools.execute(name, args).await;
                // ...
            }
            _ => JsonRpcResponse::error(-32601, "Method not found"),
        }
    }
}
```

### Consequences

#### Positive

1. **Scalability**: Handle many concurrent requests
2. **I/O efficiency**: Non-blocking I/O operations
3. **Resource usage**: Better CPU utilization
4. **Modern**: Standard for Rust networking

#### Negative

1. **Complexity**: Async/await learning curve
2. **Debugging**: Harder to trace execution
3. **Compatibility**: Not all libraries are async

---

*ADRs McpKit - Version 1.0*
