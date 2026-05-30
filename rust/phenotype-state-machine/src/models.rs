//! State machine models
//!
//! Provides the data structures for hierarchical state machines.

use std::fmt::Debug;
use std::hash::Hash;

/// Core trait for state machine states
///
/// This trait defines the interface for types that can be used as states
/// in a hierarchical state machine.
pub trait State: Debug + Clone + Send + Sync + 'static {
    /// State identifier type
    type Id: Debug + Clone + Eq + Hash + Send + Sync;

    /// Get state identifier
    fn state_id(&self) -> Self::Id;
    /// Get parent state id if this is a substate
    fn parent(&self) -> Option<Self::Id>;
    /// Check if this state is active given the current state
    fn is_active(&self, current: &Self::Id) -> bool;
}

/// Async state machine wrapper
#[allow(dead_code)]
pub struct AsyncStateMachine<S: State> {
    inner: StateMachine<S>,
    handler: Option<Box<dyn Handler<S>>>,
}

/// Event handler trait for state machines
pub trait Handler<S: State>: Send + Sync {
    /// Handle state entry
    fn on_enter(&self, state: &S);
    /// Handle state exit
    fn on_exit(&self, state: &S);
    /// Handle event
    fn handle(&self, event: Event, state: &S) -> HandlerResult<S>;
}

/// Event for state machine
#[derive(Debug, Clone)]
pub struct Event {
    /// Event type
    pub event_type: String,
    /// Event payload
    pub payload: Option<serde_json::Value>,
}

/// Handler result
#[derive(Debug, Clone)]
pub enum HandlerResult<S: State> {
    /// Stay in current state
    Stay,
    /// Transition to new state
    Transition(S),
    /// Exit state machine
    Exit,
}

impl<S: State> AsyncStateMachine<S> {
    /// Create new async state machine
    pub fn new(initial: S) -> Self {
        Self {
            inner: StateMachine::new(initial),
            handler: None,
        }
    }

    /// Get current state ID
    pub fn current_id(&self) -> Option<S::Id> {
        self.inner.current_id()
    }

    /// Set event handler
    #[allow(dead_code)]
    pub fn with_handler<H: Handler<S> + 'static>(mut self, handler: H) -> Self {
        self.handler = Some(Box::new(handler));
        self
    }

    /// Get handler reference
    pub fn handler(&self) -> Option<&dyn Handler<S>> {
        self.handler.as_ref().map(|b| b.as_ref())
    }

    /// Async transition to new state
    pub async fn transition(&mut self, new_state: S) {
        self.inner.transition(new_state);
    }

    /// Reset to initial state
    pub async fn reset(&mut self, initial: S) {
        self.inner = StateMachine::new(initial);
    }

    /// Get state history
    pub fn history(&self) -> &[S] {
        self.inner.history()
    }

    /// Process an event
    pub async fn process_event(&mut self, event: Event) -> HandlerResult<S> {
        if let Some(current) = self.inner.current() {
            if let Some(handler) = &self.handler {
                return handler.handle(event, current);
            }
        }
        HandlerResult::Stay
    }
}

/// Simple state machine implementation
#[derive(Debug, Clone)]
#[allow(dead_code)]
pub struct StateMachine<S: State> {
    current: S,
    history: Vec<S>,
    transitions: Vec<(S::Id, S::Id)>,
}

impl<S: State> StateMachine<S> {
    /// Create a new state machine with an initial state.
    pub fn new(initial: S) -> Self {
        Self {
            current: initial.clone(),
            history: vec![initial],
            transitions: Vec::new(),
        }
    }

    /// Get a reference to the current state if available.
    pub fn current(&self) -> Option<&S> {
        Some(&self.current)
    }

    /// Get the ID of the current state.
    pub fn current_id(&self) -> Option<S::Id> {
        Some(self.current.state_id())
    }

    /// Add a transition between two states.
    #[allow(dead_code)]
    pub fn add_transition(&mut self, from: S::Id, to: S::Id) {
        self.transitions.push((from, to));
    }

    /// Get the history of states visited.
    pub fn history(&self) -> &[S] {
        &self.history
    }

    /// Transition to new state
    pub fn transition(&mut self, new_state: S) {
        self.history.push(new_state.clone());
        self.current = new_state;
    }

    /// Reset to a specific state.
    pub fn reset(&mut self, state: S) {
        self.current = state.clone();
        self.history.clear();
        self.history.push(state);
    }
}

/// State history for tracking transitions
#[derive(Debug, Clone)]
#[allow(dead_code)]
pub struct StateHistory<S: State> {
    entries: Vec<HistoryEntry<S>>,
    max_size: usize,
}

impl<S: State> StateHistory<S> {
    /// Create new state history
    #[allow(dead_code)]
    pub fn new(max_size: usize) -> Self {
        Self {
            entries: Vec::new(),
            max_size,
        }
    }

    /// Add entry to history
    #[allow(dead_code)]
    pub fn push(&mut self, entry: HistoryEntry<S>) {
        if self.entries.len() >= self.max_size {
            self.entries.remove(0);
        }
        self.entries.push(entry);
    }

    /// Get all entries
    #[allow(dead_code)]
    pub fn entries(&self) -> &[HistoryEntry<S>] {
        &self.entries
    }
}

/// History entry
#[derive(Debug, Clone)]
#[allow(dead_code)]
pub struct HistoryEntry<S: State> {
    state: S,
    timestamp: u64,
}

impl<S: State> HistoryEntry<S> {
    /// Create new history entry
    #[allow(dead_code)]
    pub fn new(state: S, timestamp: u64) -> Self {
        Self { state, timestamp }
    }

    /// Get state
    #[allow(dead_code)]
    pub fn state(&self) -> &S {
        &self.state
    }

    /// Get timestamp
    #[allow(dead_code)]
    pub fn timestamp(&self) -> u64 {
        self.timestamp
    }
}
