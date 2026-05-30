# McpKit State of the Art (SOTA) Research

## Executive Summary

McpKit implements the Model Context Protocol (MCP) specification for the Phenotype ecosystem. MCP, developed by Anthropic, provides a standardized way for AI systems to interact with external tools, resources, and context. This research analyzes the MCP landscape, protocol implementations, and establishes architectural foundations for McpKit.

## 1. Model Context Protocol Landscape

### 1.1 Protocol Genesis

MCP emerged from the need for standardized AI-to-tool communication:

**Pre-MCP Era (2020-2024):**
- Ad-hoc function calling implementations
- OpenAI Function Calling API
- LangChain tool abstractions
- Custom integrations per platform

**MCP Standardization (2024+):**
- Protocol specification by Anthropic
- JSON-RPC 2.0 based communication
- Server capabilities negotiation
- Resource and tool discovery

### 1.2 Protocol Comparison

| Protocol | Transport | Discovery | State | Ecosystem |
|----------|-----------|-----------|-------|-----------|
| MCP | SSE, stdio | Built-in | Stateful | Growing |
| OpenAI Functions | HTTP | Manual | Stateless | Large |
| LangChain Tools | In-process | Code | Stateful | Large |
| Semantic Kernel | Various | Mixed | Mixed | Medium |

### 1.3 MCP Architecture

```
┌──────────────┐        JSON-RPC 2.0         ┌──────────────┐
│   MCP Client │◄───────────────────────────►│  MCP Server  │
│              │   (SSE or stdio transport)  │              │
│  • Claude    │                             │  • Tools     │
│  • IDE       │                             │  • Resources │
│  • CLI       │                             │  • Prompts   │
└──────────────┘                             └──────────────┘
```

### 1.4 Protocol Flow

1. **Initialization:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "roots": {"listChanged": true}
    },
    "clientInfo": {
      "name": "phenotype-client",
      "version": "1.0.0"
    }
  }
}
```

2. **Tool Discovery:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

3. **Tool Execution:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "search_files",
    "arguments": {
      "pattern": "*.rs",
      "directory": "/src"
    }
  }
}
```

## 2. Protocol Implementation Analysis

### 2.1 Transport Mechanisms

#### 2.1.1 Server-Sent Events (SSE)

SSE provides server-to-client streaming:

```rust
pub struct SseTransport {
    client: reqwest::Client,
    endpoint: Url,
    event_source: Option<EventSource>,
}

impl Transport for SseTransport {
    async fn connect(&mut self) -> Result<(), TransportError> {
        let response = self.client
            .get(self.endpoint.join("/sse")?)
            .send()
            .await?;
            
        if response.status().is_success() {
            self.event_source = Some(EventSource::new(response));
            Ok(())
        } else {
            Err(TransportError::ConnectionFailed)
        }
    }
    
    async fn send(&self, message: JsonRpcMessage) -> Result<(), TransportError> {
        self.client
            .post(self.endpoint.join("/message")?)
            .json(&message)
            .send()
            .await?;
        Ok(())
    }
    
    async fn receive(&mut self) -> Result<JsonRpcMessage, TransportError> {
        if let Some(ref mut es) = self.event_source {
            let event = es.next().await?;
            serde_json::from_str(&event.data)
                .map_err(|e| TransportError::ParseError(e.to_string()))
        } else {
            Err(TransportError::NotConnected)
        }
    }
}
```

#### 2.1.2 Standard IO (stdio)

stdio transport for local process communication:

```rust
pub struct StdioTransport {
    stdin: ChildStdin,
    stdout: BufReader<ChildStdout>,
    process: Child,
}

impl StdioTransport {
    pub async fn spawn(command: &str, args: &[&str]) -> Result<Self, TransportError> {
        let mut process = Command::new(command)
            .args(args)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .spawn()?;
            
        let stdin = process.stdin.take().unwrap();
        let stdout = BufReader::new(process.stdout.take().unwrap());
        
        Ok(Self {
            stdin,
            stdout,
            process,
        })
    }
}

#[async_trait]
impl Transport for StdioTransport {
    async fn send(&self, message: JsonRpcMessage) -> Result<(), TransportError> {
        let json = serde_json::to_string(&message)?;
        self.stdin.write_all(json.as_bytes()).await?;
        self.stdin.write_all(b"\n").await?;
        self.stdin.flush().await?;
        Ok(())
    }
    
    async fn receive(&mut self) -> Result<JsonRpcMessage, TransportError> {
        let mut line = String::new();
        self.stdout.read_line(&mut line).await?;
        serde_json::from_str(&line)
            .map_err(|e| TransportError::ParseError(e.to_string()))
    }
}
```

### 2.2 JSON-RPC 2.0 Implementation

#### 2.2.1 Message Types

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type")]
pub enum JsonRpcMessage {
    Request(JsonRpcRequest),
    Response(JsonRpcResponse),
    Notification(JsonRpcNotification),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JsonRpcRequest {
    pub jsonrpc: String,
    pub id: JsonRpcId,
    pub method: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub params: Option<serde_json::Value>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JsonRpcResponse {
    pub jsonrpc: String,
    pub id: JsonRpcId,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub result: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<JsonRpcError>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JsonRpcError {
    pub code: i32,
    pub message: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub data: Option<serde_json::Value>,
}
```

#### 2.2.2 Error Codes

```rust
pub mod error_codes {
    // Standard JSON-RPC errors
    pub const PARSE_ERROR: i32 = -32700;
    pub const INVALID_REQUEST: i32 = -32600;
    pub const METHOD_NOT_FOUND: i32 = -32601;
    pub const INVALID_PARAMS: i32 = -32602;
    pub const INTERNAL_ERROR: i32 = -32603;
    
    // MCP-specific errors
    pub const RESOURCE_NOT_FOUND: i32 = -32001;
    pub const TOOL_EXECUTION_ERROR: i32 = -32002;
    pub const CAPABILITY_NOT_SUPPORTED: i32 = -32003;
}
```

## 3. Tool System

### 3.1 Tool Definition

```rust
/// Tool definition for MCP server
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Tool {
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub input_schema: serde_json::Value,  // JSON Schema
}

impl Tool {
    pub fn new(name: impl Into<String>, description: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            description: Some(description.into()),
            input_schema: serde_json::json!({
                "type": "object",
                "properties": {},
                "required": []
            }),
        }
    }
    
    pub fn with_schema(mut self, schema: serde_json::Value) -> Self {
        self.input_schema = schema;
        self
    }
}

/// Tool call request
#[derive(Debug, Clone, Deserialize)]
pub struct ToolCall {
    pub name: String,
    pub arguments: serde_json::Value,
}

/// Tool call result
#[derive(Debug, Clone, Serialize)]
#[serde(tag = "type")]
pub enum ToolResult {
    #[serde(rename = "text")]
    Text { text: String },
    #[serde(rename = "image")]
    Image { data: String, mime_type: String },
    #[serde(rename = "error")]
    Error { message: String },
}
```

### 3.2 Tool Handler Trait

```rust
#[async_trait]
pub trait ToolHandler: Send + Sync {
    /// Get tool definition
    fn definition(&self) -> Tool;
    
    /// Execute tool with arguments
    async fn execute(&self, arguments: serde_json::Value) -> Result<ToolResult, ToolError>;
}

/// Registry for tool handlers
pub struct ToolRegistry {
    handlers: HashMap<String, Box<dyn ToolHandler>>,
}

impl ToolRegistry {
    pub fn register(&mut self, handler: impl ToolHandler + 'static) {
        let definition = handler.definition();
        self.handlers.insert(definition.name, Box::new(handler));
    }
    
    pub async fn execute(
        &self,
        name: &str,
        arguments: serde_json::Value,
    ) -> Result<ToolResult, ToolError> {
        let handler = self.handlers.get(name)
            .ok_or(ToolError::ToolNotFound(name.to_string()))?;
        handler.execute(arguments).await
    }
    
    pub fn list_tools(&self) -> Vec<Tool> {
        self.handlers.values()
            .map(|h| h.definition())
            .collect()
    }
}
```

## 4. Resource System

### 4.1 Resource Definition

```rust
/// Resource definition
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Resource {
    pub uri: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub name: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub mime_type: Option<String>,
}

/// Resource contents
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type")]
pub enum ResourceContent {
    #[serde(rename = "text")]
    Text { uri: String, text: String },
    #[serde(rename = "blob")]
    Blob { uri: String, blob: String },  // base64 encoded
}

/// Resource provider trait
#[async_trait]
pub trait ResourceProvider: Send + Sync {
    /// List available resources
    async fn list_resources(&self) -> Result<Vec<Resource>, ResourceError>;
    
    /// Read resource contents
    async fn read_resource(&self, uri: &str) -> Result<ResourceContent, ResourceError>;
    
    /// Subscribe to resource changes (if supported)
    async fn subscribe(&self, uri: &str) -> Result<Subscription, ResourceError>;
}
```

## 5. Server Implementation

### 5.1 Server Capabilities

```rust
/// Server capabilities
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ServerCapabilities {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub tools: Option<ToolCapabilities>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub resources: Option<ResourceCapabilities>,
}

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ToolCapabilities {
    pub list_changed: bool,
}

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct ResourceCapabilities {
    pub subscribe: bool,
    pub list_changed: bool,
}

/// Server information
#[derive(Debug, Clone)]
pub struct ServerInfo {
    pub name: String,
    pub version: String,
    pub protocol_version: String,
    pub capabilities: ServerCapabilities,
}

impl ServerInfo {
    pub fn new(name: impl Into<String>, version: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            version: version.into(),
            protocol_version: "2024-11-05".to_string(),
            capabilities: ServerCapabilities::default(),
        }
    }
    
    pub fn with_tools(mut self) -> Self {
        self.capabilities.tools = Some(ToolCapabilities { list_changed: true });
        self
    }
    
    pub fn with_resources(mut self) -> Self {
        self.capabilities.resources = Some(ResourceCapabilities {
            subscribe: true,
            list_changed: true,
        });
        self
    }
}
```

### 5.2 Server Builder

```rust
pub struct McpServer {
    info: ServerInfo,
    tools: ToolRegistry,
    resources: Option<Box<dyn ResourceProvider>>,
    transport: Box<dyn Transport>,
}

pub struct McpServerBuilder {
    info: ServerInfo,
    tools: ToolRegistry,
    resources: Option<Box<dyn ResourceProvider>>,
}

impl McpServerBuilder {
    pub fn new(name: impl Into<String>, version: impl Into<String>) -> Self {
        Self {
            info: ServerInfo::new(name, version),
            tools: ToolRegistry::new(),
            resources: None,
        }
    }
    
    pub fn with_tool(mut self, handler: impl ToolHandler + 'static) -> Self {
        self.tools.register(handler);
        self
    }
    
    pub fn with_resources(mut self, provider: impl ResourceProvider + 'static) -> Self {
        self.resources = Some(Box::new(provider));
        self
    }
    
    pub fn build_with_stdio(self) -> Result<McpServer, BuildError> {
        let transport = StdioTransport::new()?;
        self.build(transport)
    }
    
    pub fn build_with_sse(self, endpoint: &str) -> Result<McpServer, BuildError> {
        let transport = SseTransport::new(endpoint)?;
        self.build(transport)
    }
    
    fn build(self, transport: impl Transport + 'static) -> Result<McpServer, BuildError> {
        let mut info = self.info;
        
        if !self.tools.list_tools().is_empty() {
            info = info.with_tools();
        }
        
        if self.resources.is_some() {
            info = info.with_resources();
        }
        
        Ok(McpServer {
            info,
            tools: self.tools,
            resources: self.resources,
            transport: Box::new(transport),
        })
    }
}
```

## 6. Comparison with Alternatives

### 6.1 OpenAI Function Calling

| Feature | MCP | OpenAI |
|---------|-----|--------|
| Transport | SSE, stdio | HTTP |
| Discovery | Built-in | Manual |
| Streaming | Yes | Yes |
| State | Stateful per connection | Stateless |
| Resources | First-class | Not supported |
| Subscription | Supported | Not supported |

### 6.2 LangChain Tools

```rust
// LangChain-style tool (for comparison)
pub trait LangChainTool: Send + Sync {
    fn name(&self) -> &str;
    fn description(&self) -> &str;
    fn parameters(&self) -> serde_json::Value;
    fn run(&self, args: serde_json::Value) -> Result<String, ToolError>;
}

// MCP tool (McpKit style)
#[async_trait]
pub trait McpTool: Send + Sync {
    fn definition(&self) -> Tool;
    async fn execute(&self, arguments: serde_json::Value) -> Result<ToolResult, ToolError>;
}
```

## 7. Future Directions

### 7.1 Protocol Extensions

```rust
/// Proposed streaming response extension
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StreamingToolResult {
    pub stream_id: String,
    pub chunks: Vec<StreamChunk>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StreamChunk {
    pub index: usize,
    pub content: ToolResult,
    pub is_final: bool,
}
```

### 7.2 Multi-Modal Support

```rust
/// Proposed multi-modal content types
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type")]
pub enum MultiModalContent {
    Text { text: String },
    Image { url: String, mime_type: String },
    Audio { url: String, duration_ms: u32 },
    Video { url: String, duration_ms: u32 },
    File { uri: String, mime_type: String, size_bytes: u64 },
}
```

## 8. References

1. Anthropic MCP Specification: https://modelcontextprotocol.io/
2. JSON-RPC 2.0 Specification: https://www.jsonrpc.org/specification
3. Server-Sent Events: https://html.spec.whatwg.org/multipage/server-sent-events.html

---

*Document Version: 1.0*
