# ADR-001: MCP Transport Layer

**Document ID:** PHENOTYPE_MCPKIT_ADR_001  
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

**MCP Transport Layer: Dual Transport Support (SSE and stdio)**

## Status

**Accepted** — This decision has been implemented across the McpKit codebase.

## Context

### Problem Statement

MCP servers must support multiple deployment scenarios, each with fundamentally different communication requirements:

1. **Local/IDE Integration**: Tools like Claude Desktop, VS Code extensions, and CLI applications spawn MCP servers as child processes and communicate via standard I/O streams. This requires a lightweight, process-based transport with minimal overhead.

2. **Remote/Cloud Deployment**: Production MCP servers deployed as network services require HTTP-based communication with support for multiple concurrent clients, authentication, and network resilience.

3. **Testing Environments**: Unit and integration tests need deterministic, easily mockable transport mechanisms that don't require network infrastructure.

4. **Hybrid Deployments**: Some scenarios require switching between transports based on runtime configuration without changing application logic.

### Transport Options Evaluated

#### Option A: stdio Only

```
┌──────────────┐     ┌──────────────┐
│   MCP Host   │     │  MCP Server  │
│  (Parent)    │     │  (Child)     │
│              │     │              │
│  stdin  ◄────┼─────┼── stdout     │
│  stdout ─────┼────►┼── stdin      │
│              │     │              │
└──────────────┘     └──────────────┘
```

**Pros:**
- Simplest implementation
- Zero network dependencies
- Natural process isolation
- Easy debugging via stdout/stderr

**Cons:**
- Only works for local processes
- No multi-client support
- Cannot be deployed remotely
- Limited to single connection per server

#### Option B: SSE Only

```
┌──────────────┐                          ┌──────────────┐
│   MCP Host   │                          │  MCP Server  │
│   (Client)   │                          │              │
│              │  GET /sse                │              │
│              │─────────────────────────►│              │
│              │  text/event-stream       │              │
│              │◄─────────────────────────│              │
│              │                          │              │
│              │  POST /message           │              │
│              │─────────────────────────►│              │
│              │  application/json        │              │
└──────────────┘                          └──────────────┘
```

**Pros:**
- Supports remote deployment
- Multi-client capable
- HTTP ecosystem compatible (load balancers, proxies)
- Standard web technology

**Cons:**
- Requires HTTP server infrastructure
- More complex session management
- Network latency overhead
- Requires TLS for security

#### Option C: WebSocket (Proposed)

```
┌──────────────┐                          ┌──────────────┐
│   MCP Host   │                          │  MCP Server  │
│              │                          │              │
│              │  WebSocket Upgrade       │              │
│              │─────────────────────────►│              │
│              │◄─────────────────────────│  101 Switch  │
│              │                          │              │
│              │  Bidirectional frames    │              │
│              │◄────────────────────────►│              │
└──────────────┘                          └──────────────┘
```

**Pros:**
- True bidirectional streaming
- Lower latency than SSE
- Single connection for both directions

**Cons:**
- Not part of MCP specification (yet)
- Less mature ecosystem support
- Proxy/load balancer compatibility issues
- Requires additional implementation effort

#### Option D: Dual Transport (SSE + stdio)

```
┌──────────────────────────────────────────────────────────────┐
│                    Transport Abstraction Layer                 │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐           ┌─────────────────┐           │
│  │   StdioTransport│           │   SSETransport  │           │
│  │                 │           │                 │           │
│  │ • stdin/stdout  │           │ • HTTP GET /sse │           │
│  │ • Line-based    │           │ • HTTP POST     │           │
│  │ • Single client │           │ • Multi-session │           │
│  │ • Zero config   │           │ • Network-ready │           │
│  └────────┬────────┘           └────────┬────────┘           │
│           │                             │                     │
│           └─────────────┬───────────────┘                     │
│                         │                                     │
│              ┌──────────▼──────────┐                          │
│              │   Transport Trait   │                          │
│              │                     │                          │
│              │ • send(message)     │                          │
│              │ • receive()         │                          │
│              │ • close()           │                          │
│              │ • is_connected()    │                          │
│              └─────────────────────┘                          │
│                         │                                     │
│              ┌──────────▼──────────┐                          │
│              │   MCP Server Core   │                          │
│              │                     │                          │
│              │ • Protocol logic    │                          │
│              │ • Tool dispatch     │                          │
│              │ • Resource handling │                          │
│              └─────────────────────┘                          │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Pros:**
- Covers all deployment scenarios
- Unified API through transport abstraction
- Transport selection at runtime
- Future-proof for additional transports

**Cons:**
- Two implementations to maintain
- More complex testing matrix
- Larger codebase

### Requirements

| Requirement | Priority | Description |
|-------------|----------|-------------|
| R1 | Must | Support stdio for local/IDE deployment |
| R2 | Must | Support SSE for remote/cloud deployment |
| R3 | Must | Unified transport interface |
| R4 | Must | Runtime transport selection |
| R5 | Should | Session management for SSE |
| R6 | Should | Graceful shutdown for both transports |
| R7 | Could | WebSocket support (future) |
| R8 | Could | HTTP/2 stream transport (future) |

## Decision

**Implement dual transport support with a unified `Transport` abstraction layer.**

Both SSE and stdio transports will be implemented as concrete types conforming to a common `Transport` trait/interface. The MCP server core will be transport-agnostic, receiving messages through the abstraction layer.

### Transport Interface Definition

The transport abstraction defines the following contract:

```
┌──────────────────────────────────────────────────────────────┐
│                    Transport Interface                         │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Methods:                                                     │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ connect()         → Establish connection               │   │
│  │ send(message)     → Send JSON-RPC message              │   │
│  │ receive()         → Receive JSON-RPC message           │   │
│  │ close()           → Graceful shutdown                  │   │
│  │ is_connected()    → Connection status check            │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                               │
│  Properties:                                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ name            → Transport identifier                 │   │
│  │ capabilities    → Supported features                   │   │
│  │ session_id      → Unique session (SSE only)            │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                               │
│  Events:                                                      │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ on_message      → Message received callback            │   │
│  │ on_close        → Connection closed callback           │   │
│  │ on_error        → Error occurred callback              │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### Transport Selection Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    Transport Selection                         │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Server Startup                                               │
│       │                                                       │
│       ▼                                                       │
│  ┌─────────────────┐                                         │
│  │ Check --transport│                                        │
│  │ flag or config   │                                        │
│  └────────┬────────┘                                         │
│           │                                                   │
│    ┌──────┴──────┐                                           │
│    │             │                                           │
│    ▼             ▼                                           │
│  "stdio"       "sse"                                         │
│    │             │                                           │
│    ▼             ▼                                           │
│  ┌──────────┐  ┌──────────────────┐                          │
│  │Stdio     │  │SSE Transport     │                          │
│  │Transport │  │                  │                          │
│  │          │  │ • Start HTTP srv │                          │
│  │ • Bind   │  │ • Configure CORS │                          │
│  │   stdin  │  │ • Set up routes  │                          │
│  │ • Bind   │  │ • Session manager│                          │
│  │   stdout │  │                  │                          │
│  └────┬─────┘  └────────┬─────────┘                          │
│       │                 │                                     │
│       └────────┬────────┘                                     │
│                │                                              │
│                ▼                                              │
│  ┌─────────────────────────┐                                  │
│  │   MCP Server Core       │                                  │
│  │   (transport-agnostic)  │                                  │
│  └─────────────────────────┘                                  │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Consequences

### Positive Consequences

1. **Universal Deployment Flexibility**: McpKit servers can run as local CLI tools (stdio), IDE integrations (stdio), or cloud services (SSE) without any code changes. The same tool implementation works across all deployment scenarios, significantly reducing maintenance burden and ensuring consistent behavior.

2. **Transport-Agnostic Core Logic**: By abstracting the transport layer, the MCP server core (protocol handling, tool dispatch, resource management) remains completely decoupled from communication details. This enables easier testing, cleaner architecture, and simpler addition of future transports (WebSocket, HTTP/2 streams, gRPC).

3. **IDE and CLI Native Support**: stdio transport provides zero-configuration integration with Claude Desktop, VS Code, and any CLI tool that can spawn child processes. This is the primary deployment model for developer tools and local AI assistants, requiring no network setup or authentication configuration.

4. **Production-Ready Remote Access**: SSE transport enables deploying McpKit servers as cloud services accessible by multiple clients simultaneously. Session management, CORS configuration, and HTTP ecosystem compatibility (load balancers, reverse proxies, API gateways) make it suitable for production environments.

5. **Comprehensive Testing Strategy**: stdio transport enables simple, deterministic unit testing without network dependencies. SSE transport can be integration-tested with HTTP test clients. The transport abstraction allows mocking the entire communication layer for isolated core logic testing.

6. **Future-Proof Architecture**: The transport abstraction pattern makes it straightforward to add new transport mechanisms (WebSocket, HTTP/2, Unix domain sockets, named pipes) without modifying the server core. Each new transport is a self-contained implementation conforming to the established interface.

7. **Graceful Degradation**: If SSE infrastructure is unavailable (no HTTP server, network issues), the server can fall back to stdio mode. Conversely, if process spawning is restricted (sandboxed environments), SSE provides an alternative communication channel.

### Negative Consequences

1. **Dual Implementation Maintenance**: Two transport implementations must be maintained, tested, and kept in sync with protocol updates. Bug fixes in one transport may need to be evaluated for applicability to the other. This increases the ongoing maintenance burden and requires careful version management.

2. **Expanded Testing Matrix**: Every feature must be tested against both transports, effectively doubling the test surface area. Transport-specific edge cases (SSE session timeouts, stdio process termination) require dedicated test scenarios. CI pipelines must cover both transport modes.

3. **Increased Code Complexity**: The transport abstraction layer adds indirection that can make debugging more challenging. Stack traces span multiple abstraction layers, and transport-specific issues may be harder to isolate. Developers must understand both transport implementations to fully grasp the system.

4. **Session Management Overhead (SSE)**: SSE transport requires managing client sessions, handling connection drops, implementing heartbeat mechanisms, and cleaning up abandoned sessions. This adds significant complexity compared to the stateless stdio model and introduces potential memory leak vectors.

5. **Documentation Burden**: Users need documentation for both transport modes, including configuration examples, troubleshooting guides, and deployment instructions for each scenario. This increases the documentation maintenance burden and can lead to outdated or inconsistent documentation.

6. **Resource Consumption**: Running an HTTP server for SSE transport consumes additional system resources (memory, file descriptors, CPU) compared to stdio. In resource-constrained environments (containers, serverless), this overhead may be significant and requires careful capacity planning.

7. **Security Surface Expansion**: SSE transport introduces network attack vectors (MITM, session hijacking, DoS) that don't exist with stdio. This requires implementing TLS, authentication, rate limiting, and input validation specifically for the network transport, increasing the security audit surface.

## Architecture

### Transport Layer Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        McpKit Transport Architecture                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Application Layer                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    MCP Server Core                               │  │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌─────────────┐  │  │
│  │  │ Lifecycle │  │   Tools   │  │Resources  │  │  Prompts    │  │  │
│  │  │ Manager   │  │  Registry │  │  Manager  │  │  Manager    │  │  │
│  │  └───────────┘  └───────────┘  └───────────┘  └─────────────┘  │  │
│  └───────────────────────────────┬─────────────────────────────────┘  │
│                                  │                                    │
│  ┌───────────────────────────────▼─────────────────────────────────┐  │
│  │                    Transport Abstraction                         │  │
│  │                                                                 │  │
│  │  ┌───────────────────────────────────────────────────────────┐  │  │
│  │  │                    Transport Trait                         │  │  │
│  │  │                                                           │  │  │
│  │  │  async fn connect(&mut self) -> Result<(), Error>;        │  │  │
│  │  │  async fn send(&self, msg: JsonRpcMessage) -> Result<()>; │  │  │
│  │  │  async fn receive(&mut self) -> Result<JsonRpcMessage>;   │  │  │
│  │  │  async fn close(&mut self) -> Result<(), Error>;          │  │  │
│  │  │  fn is_connected(&self) -> bool;                          │  │  │
│  │  └───────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────┬─────────────────────────────────┘  │
│                                  │                                    │
│  ┌───────────────────────────────┴─────────────────────────────────┐  │
│  │                    Concrete Transports                           │  │
│  │                                                                 │  │
│  │  ┌─────────────────────────┐  ┌─────────────────────────────┐   │  │
│  │  │    StdioTransport       │  │      SSETransport           │   │  │
│  │  │                         │  │                             │   │  │
│  │  │  stdin: AsyncRead       │  │  http_server: HttpServer    │   │  │
│  │  │  stdout: AsyncWrite     │  │  sessions: SessionManager   │   │  │
│  │  │  codec: LineCodec       │  │  sse_endpoint: String       │   │  │
│  │  │                         │  │  msg_endpoint: String       │   │  │
│  │  │  connect(): bind stdio  │  │  connect(): start HTTP      │   │  │
│  │  │  send(): write line     │  │  send(): broadcast to sess  │   │  │
│  │  │  receive(): read line   │  │  receive(): from POST       │   │  │
│  │  └─────────────────────────┘  └─────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### SSE Session Management

```
┌──────────────────────────────────────────────────────────────────────┐
│                    SSE Session Management                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    SessionManager                                │  │
│  │                                                                 │  │
│  │  sessions: HashMap<String, Session>                             │  │
│  │  max_sessions: usize                                            │  │
│  │  session_timeout: Duration                                      │  │
│  │                                                                 │  │
│  │  ┌───────────────────────────────────────────────────────────┐  │  │
│  │  │                    Session                                 │  │  │
│  │  │                                                           │  │  │
│  │  │  id: String                    (UUID)                     │  │  │
│  │  │  created_at: Instant           (creation time)            │  │  │
│  │  │  last_activity: Instant        (keepalive tracking)       │  │  │
│  │  │  message_tx: Sender            (SSE event channel)        │  │  │
│  │  │  message_rx: Receiver          (client receives)          │  │  │
│  │  │  state: SessionState           (Active/Draining/Closed)   │  │  │
│  │  └───────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Session Lifecycle:                                                   │
│                                                                       │
│  Created ───► Active ───► Draining ───► Closed                       │
│     │            │            │            │                          │
│     │            │            │            │                          │
│     │      (timeout)     (graceful     (cleanup)                     │
│     │      (max sess)     close)                                     │
│     │            │            │                                      │
│     └────────────┴────────────┴──────────► Cleanup                    │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Implementation Details

### Python Implementation

```python
"""McpKit Transport Layer - Python Implementation."""
from abc import ABC, abstractmethod
from typing import Optional, Protocol
import asyncio
import json

class TransportError(Exception):
    """Base transport error."""
    pass

class ConnectionError(TransportError):
    """Connection failed."""
    pass

class ParseError(TransportError):
    """Message parse failed."""
    pass

class Transport(ABC):
    """Abstract transport for MCP communication."""

    @abstractmethod
    async def connect(self) -> None:
        """Establish the transport connection."""
        pass

    @abstractmethod
    async def send(self, message: dict) -> None:
        """Send a JSON-RPC message."""
        pass

    @abstractmethod
    async def receive(self) -> dict:
        """Receive a JSON-RPC message."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Gracefully close the transport."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if transport is connected."""
        pass

class StdioTransport(Transport):
    """Standard I/O transport for local process communication."""

    def __init__(self):
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._connected = False

    async def connect(self) -> None:
        """Bind to stdin/stdout."""
        loop = asyncio.get_event_loop()
        self._reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(self._reader)
        await loop.connect_read_pipe(lambda: protocol, asyncio.get_event_loop()._stdin)
        writer_transport, writer_protocol = await loop.connect_write_pipe(
            asyncio.streams.FlowControlMixin,
            asyncio.get_event_loop()._stdout,
        )
        self._writer = asyncio.streams.StreamWriter(
            writer_transport, writer_protocol, self._reader, loop
        )
        self._connected = True

    async def send(self, message: dict) -> None:
        """Write JSON-RPC message to stdout."""
        if not self._connected:
            raise ConnectionError("Transport not connected")
        data = json.dumps(message) + "\n"
        self._writer.write(data.encode("utf-8"))
        await self._writer.drain()

    async def receive(self) -> dict:
        """Read JSON-RPC message from stdin."""
        if not self._connected:
            raise ConnectionError("Transport not connected")
        line = await self._reader.readline()
        if not line:
            raise ConnectionError("EOF received")
        try:
            return json.loads(line.decode("utf-8"))
        except json.JSONDecodeError as e:
            raise ParseError(f"Invalid JSON: {e}")

    async def close(self) -> None:
        """Close the transport."""
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected
```

### Go Implementation

```go
package transport

import (
    "bufio"
    "context"
    "encoding/json"
    "fmt"
    "io"
    "os"
    "sync"
)

// Transport defines the interface for MCP communication
type Transport interface {
    Connect(ctx context.Context) error
    Send(ctx context.Context, message json.RawMessage) error
    Receive(ctx context.Context) (json.RawMessage, error)
    Close() error
    IsConnected() bool
}

// TransportError represents a transport-level error
type TransportError struct {
    Op  string
    Err error
}

func (e *TransportError) Error() string {
    return fmt.Sprintf("transport %s: %v", e.Op, e.Err)
}

// StdioTransport implements Transport using standard I/O
type StdioTransport struct {
    scanner   *bufio.Scanner
    encoder   *json.Encoder
    mu        sync.Mutex
    connected bool
}

// NewStdioTransport creates a new stdio transport
func NewStdioTransport() *StdioTransport {
    return &StdioTransport{
        scanner: bufio.NewScanner(os.Stdin),
        encoder: json.NewEncoder(os.Stdout),
    }
}

// Connect binds to stdin/stdout
func (t *StdioTransport) Connect(ctx context.Context) error {
    t.mu.Lock()
    defer t.mu.Unlock()
    t.connected = true
    return nil
}

// Send writes a JSON-RPC message to stdout
func (t *StdioTransport) Send(ctx context.Context, message json.RawMessage) error {
    t.mu.Lock()
    defer t.mu.Unlock()

    if !t.connected {
        return &TransportError{Op: "send", Err: fmt.Errorf("not connected")}
    }

    if err := t.encoder.Encode(message); err != nil {
        return &TransportError{Op: "send", Err: err}
    }
    return nil
}

// Receive reads a JSON-RPC message from stdin
func (t *StdioTransport) Receive(ctx context.Context) (json.RawMessage, error) {
    t.mu.Lock()
    defer t.mu.Unlock()

    if !t.connected {
        return nil, &TransportError{Op: "receive", Err: fmt.Errorf("not connected")}
    }

    if !t.scanner.Scan() {
        if err := t.scanner.Err(); err != nil {
            return nil, &TransportError{Op: "receive", Err: err}
        }
        return nil, &TransportError{Op: "receive", Err: io.EOF}
    }

    return json.RawMessage(t.scanner.Bytes()), nil
}

// Close shuts down the transport
func (t *StdioTransport) Close() error {
    t.mu.Lock()
    defer t.mu.Unlock()
    t.connected = false
    return nil
}

// IsConnected returns the connection status
func (t *StdioTransport) IsConnected() bool {
    t.mu.Lock()
    defer t.mu.Unlock()
    return t.connected
}
```

## Code Examples

### Example 1: Transport Selection at Startup

```python
# Python: Transport selection via CLI argument
import argparse
import asyncio

async def main():
    parser = argparse.ArgumentParser(description="McpKit Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport to use",
    )
    parser.add_argument("--port", type=int, default=8000, help="SSE port")
    args = parser.parse_args()

    server = McpServer(name="mcpkit", version="0.1.0")

    if args.transport == "stdio":
        transport = StdioTransport()
    else:
        transport = SSETransport(port=args.port)

    await transport.connect()
    await server.run(transport)

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 2: SSE Transport Configuration

```python
# Python: SSE transport with custom configuration
from mcp.server.sse import SseServerTransport

transport = SSETransport(
    host="0.0.0.0",
    port=8000,
    sse_endpoint="/sse",
    message_endpoint="/message",
    cors_origins=["https://example.com"],
    session_timeout=300,  # 5 minutes
    max_sessions=100,
)

await transport.connect()
```

### Example 3: Custom Transport Implementation

```python
# Python: WebSocket transport (future)
class WebSocketTransport(Transport):
    """WebSocket-based MCP transport."""

    def __init__(self, uri: str):
        self.uri = uri
        self.ws = None
        self._connected = False

    async def connect(self) -> None:
        import websockets
        self.ws = await websockets.connect(self.uri)
        self._connected = True

    async def send(self, message: dict) -> None:
        await self.ws.send(json.dumps(message))

    async def receive(self) -> dict:
        data = await self.ws.recv()
        return json.loads(data)

    async def close(self) -> None:
        await self.ws.close()
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected
```

## Cross-References

- **SPEC.md** — Section 7: Transport Layer (transport trait definition)
- **SOTA.md** — Section 4: Transport Mechanisms Deep Dive (SSE and stdio analysis)
- **ADR-002** — Tool Registry Design (tool dispatch over transport)
- **ADR-003** — SDK Generation Strategy (transport code generation)
- **registry.yaml** — Workspace configuration for transport implementations
- **python/pheno_mcp/adapters/** — Python transport adapter implementations
- **rust/mcp-forge/internal/lsp/transport.go** — Go transport reference implementation

---

*Document Version: 1.0*  
*Total Lines: 400+*  
*Decision Date: 2026-04-03*
