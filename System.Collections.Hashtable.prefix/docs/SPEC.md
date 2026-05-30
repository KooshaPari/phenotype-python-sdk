# ResilienceKit Specification

## 1. Overview

ResilienceKit provides resilience patterns for the Phenotype ecosystem.

### 1.1 Components

- **phenotype-retry**: Retry logic with backoff strategies
- **phenotype-state-machine**: Hierarchical state machines
- **phenotype-async-traits**: Async trait utilities
- **phenotype-port-traits**: Port trait abstractions

## 2. Retry System

### 2.1 Error Types

```rust
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum RetryError<E> {
    #[error("Max retry attempts ({attempts}) exceeded")]
    Exceeded { attempts: u32, last_error: E },
    #[error("Retry cancelled")]
    Cancelled,
}
```

### 2.2 Backoff Strategies

```rust
#[derive(Clone)]
pub enum BackoffStrategy {
    Fixed { delay: Duration },
    Linear { base: Duration },
    Exponential { base: Duration, max: Duration },
    Custom { func: Arc<dyn Fn(u32) -> Duration + Send + Sync> },
}

impl BackoffStrategy {
    pub fn fixed(delay: Duration) -> Self {
        Self::Fixed { delay }
    }
    
    pub fn linear(base: Duration) -> Self {
        Self::Linear { base }
    }
    
    pub fn exponential(base: Duration, max: Duration) -> Self {
        Self::Exponential { base, max }
    }
    
    pub fn custom<F: Fn(u32) -> Duration + Send + Sync + 'static>(func: F) -> Self {
        Self::Custom { func: Arc::new(func) }
    }
    
    pub fn calculate_delay(&self, attempt: u32) -> Duration {
        match self {
            Self::Fixed { delay } => *delay,
            Self::Linear { base } => *base * attempt,
            Self::Exponential { base, max } => {
                let exp = attempt.saturating_sub(1) as u32;
                (*base * 2_u32.saturating_pow(exp)).min(*max)
            }
            Self::Custom { func } => func(attempt),
        }
    }
}
```

### 2.3 Retry Policy

```rust
#[derive(Clone)]
pub struct RetryPolicy {
    pub max_attempts: u32,
    pub backoff: BackoffStrategy,
}

impl RetryPolicy {
    pub fn new(max_attempts: u32, backoff: BackoffStrategy) -> Self {
        Self {
            max_attempts: max_attempts.max(1),
            backoff,
        }
    }
    
    pub fn default_exponential(max_attempts: u32) -> Self {
        Self::new(
            max_attempts,
            BackoffStrategy::exponential(Duration::from_millis(100), Duration::from_secs(5)),
        )
    }
}

impl Default for RetryPolicy {
    fn default() -> Self {
        Self::default_exponential(3)
    }
}
```

### 2.4 Retry Functions

```rust
/// Retry an operation
pub async fn retry<F, Fut, T, E>(
    mut operation: F,
    policy: &RetryPolicy,
) -> Result<T, RetryError<E>>
where
    F: FnMut() -> Fut,
    Fut: Future<Output = Result<T, E>>,
    E: std::error::Error + Send + Sync + 'static,
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
    
    Err(RetryError::Exceeded {
        attempts: policy.max_attempts,
        last_error: last_error.unwrap(),
    })
}

/// Retry with context
pub async fn retry_with_context<F, Fut, T, E>(
    mut operation: F,
    policy: &RetryPolicy,
) -> Result<T, RetryError<E>>
where
    F: FnMut(RetryContext) -> Fut,
    Fut: Future<Output = Result<T, E>>,
    E: std::error::Error + Send + Sync + 'static,
{
    let start = Instant::now();
    let mut last_error: Option<E> = None;
    
    for attempt in 1..=policy.max_attempts {
        let context = RetryContext {
            attempt,
            max_attempts: policy.max_attempts,
            elapsed: start.elapsed(),
            last_error: last_error.as_ref().map(|e| e.to_string()),
        };
        
        match operation(context).await {
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
    
    Err(RetryError::Exceeded {
        attempts: policy.max_attempts,
        last_error: last_error.unwrap(),
    })
}
```

### 2.5 Retry Context

```rust
#[derive(Debug, Clone)]
pub struct RetryContext {
    pub attempt: u32,
    pub max_attempts: u32,
    pub elapsed: Duration,
    pub last_error: Option<String>,
}

impl RetryContext {
    pub fn is_first_attempt(&self) -> bool {
        self.attempt == 1
    }
    
    pub fn is_last_attempt(&self) -> bool {
        self.attempt >= self.max_attempts
    }
}
```

## 3. State Machine System

### 3.1 State Trait

```rust
pub trait State: Debug + Clone + Send + Sync + 'static {
    type Id: Debug + Clone + Eq + Hash + Send + Sync;
    fn id(&self) -> Self::Id;
    fn validate_transition(&self, to: &Self) -> Result<(), String>;
    fn on_enter(&self);
    fn on_exit(&self);
}

pub trait Handler: Debug + Send + Sync + 'static {
    type State: State;
    fn handle(&self, state: &Self::State, event: Event) -> HandlerResult<Self::State>;
}

#[derive(Debug, Clone)]
pub struct Event {
    pub event_type: String,
    pub payload: Option<serde_json::Value>,
}

#[derive(Debug)]
pub enum HandlerResult<S: State> {
    Stay,
    Transition(S),
    Exit,
}
```

### 3.2 Hierarchical State Machine

```rust
#[derive(Debug)]
pub struct HierarchicalStateMachine<S: State> {
    current: S,
    parent: Option<Box<Self>>,
    children: HashMap<S::Id, Box<Self>>,
    handler: Option<Box<dyn Handler<State = S>>>,
    history: Vec<S>,
}

impl<S: State + Default> Default for HierarchicalStateMachine<S> {
    fn default() -> Self {
        Self {
            current: S::default(),
            parent: None,
            children: HashMap::new(),
            handler: None,
            history: Vec::new(),
        }
    }
}

impl<S: State> HierarchicalStateMachine<S> {
    pub fn new(initial: S) -> Self {
        Self {
            current: initial,
            parent: None,
            children: HashMap::new(),
            handler: None,
            history: Vec::new(),
        }
    }
    
    pub fn current(&self) -> &S {
        &self.current
    }
    
    pub fn transition(&mut self, new_state: S) -> Result<(), String> {
        self.current.validate_transition(&new_state)?;
        self.current.on_exit();
        self.history.push(self.current.clone());
        new_state.on_enter();
        self.current = new_state;
        Ok(())
    }
    
    pub fn process(&mut self, event: Event) -> HandlerResult<S> {
        if let Some(handler) = &self.handler {
            handler.handle(&self.current, event)
        } else {
            HandlerResult::Stay
        }
    }
    
    pub fn history(&self) -> &[S] {
        &self.history
    }
    
    pub fn reset(&mut self, initial: S) {
        self.current = initial;
        self.history.clear();
    }
}
```

## 4. Usage

### 4.1 Retry Usage

```rust
use phenotype_retry::{retry, RetryPolicy, BackoffStrategy};
use std::time::Duration;

let policy = RetryPolicy::new(
    5,
    BackoffStrategy::exponential(Duration::from_millis(100), Duration::from_secs(5)),
);

let result = retry(
    || async {
        // Async operation that might fail
        do_something().await
    },
    &policy,
).await;
```

### 4.2 State Machine Usage

```rust
#[derive(Debug, Clone)]
enum MyState {
    Idle,
    Running,
    Stopped,
}

impl State for MyState {
    type Id = String;
    
    fn id(&self) -> Self::Id {
        format!("{:?}", self).to_lowercase()
    }
    
    fn validate_transition(&self, to: &Self) -> Result<(), String> {
        match (self, to) {
            (MyState::Idle, MyState::Running) => Ok(()),
            (MyState::Running, MyState::Stopped) => Ok(()),
            (MyState::Stopped, MyState::Idle) => Ok(()),
            _ => Err("Invalid transition".to_string()),
        }
    }
    
    fn on_enter(&self) {
        println!("Entering: {:?}", self);
    }
    
    fn on_exit(&self) {
        println!("Exiting: {:?}", self);
    }
}

let mut sm = HierarchicalStateMachine::new(MyState::Idle);
sm.transition(MyState::Running)?;
```

---

*Specification Version: 1.0*
