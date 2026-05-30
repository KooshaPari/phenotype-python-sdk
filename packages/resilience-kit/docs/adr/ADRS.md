# ResilienceKit ADRs

## ADR 001: Pluggable Backoff Strategies

### Status: Accepted

### Context

Different failure modes require different retry strategies. Fixed delay is simple but exponential handles load spikes better.

### Decision

Implement pluggable backoff strategies:

```rust
pub enum BackoffStrategy {
    Fixed { delay: Duration },
    Linear { base: Duration },
    Exponential { base: Duration, max: Duration },
    Custom { func: Arc<dyn Fn(u32) -> Duration + Send + Sync> },
}
```

### Consequences

#### Positive

1. **Flexibility**: Choose strategy per use case
2. **Custom**: User-defined backoff logic
3. **Performance**: Appropriate strategy selection

#### Negative

1. **Complexity**: More options to understand
2. **Testing**: Multiple implementations

---

## ADR 002: Hierarchical State Machines

### Status: Accepted

### Context

Flat state machines become unwieldy with complex workflows. Hierarchy provides structure.

### Decision

Implement hierarchical state machines:

```rust
pub struct HierarchicalStateMachine<S: State> {
    current: S,
    parent: Option<Box<Self>>,
    children: HashMap<S::Id, Box<Self>>,
}
```

### Consequences

#### Positive

1. **Organization**: Natural workflow structure
2. **Reuse**: Common states as parents
3. **History**: State entry/exit tracking

#### Negative

1. **Complexity**: More complex than flat
2. **Debugging**: Harder to trace

---

## ADR 003: Async-First Retry Framework

### Status: Accepted

### Context

Retry operations often involve async I/O. Synchronous retry blocks threads.

### Decision

Implement async-first retry:

```rust
pub async fn retry<F, Fut, T, E>(
    mut operation: F,
    policy: &RetryPolicy,
) -> Result<T, RetryError<E>>
where
    F: FnMut() -> Fut,
    Fut: Future<Output = Result<T, E>>,
{
    let mut last_error: Option<E> = None;
    
    for attempt in 1..=policy.max_attempts {
        match operation().await {
            Ok(value) => return Ok(value),
            Err(error) => {
                last_error = Some(error);
                if attempt >= policy.max_attempts {
                    break;
                }
                sleep(policy.backoff.calculate_delay(attempt)).await;
            }
        }
    }
    
    Err(RetryError::Exceeded { ... })
}
```

### Consequences

#### Positive

1. **Non-blocking**: Async sleep
2. **Composable**: Works with async ecosystem
3. **Scalable**: No thread blocking

#### Negative

1. **Complexity**: Requires async runtime
2. **Testing**: Async test setup

---

*ADRs ResilienceKit - Version 1.0*
