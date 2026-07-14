//! Phenotype Event Bus - Async event publishing and subscription
//!
//! Provides a compatibility facade over the canonical `pheno-events` bus.

#![cfg_attr(docsrs, feature(doc_auto_cfg))]

use std::any::Any;
use std::collections::HashMap;
use std::sync::Arc;

use async_trait::async_trait;
use pheno_events::{
    bus::{Bus as CanonicalBus, InMemoryBus, Subscription},
    core::EventEnvelope as CanonicalEnvelope,
};
use serde::{de::DeserializeOwned, Serialize};
use tokio::sync::{broadcast, mpsc, OnceCell};
use uuid::Uuid;

const LEGACY_SOURCE: &str = "phenotype-python-sdk";

/// Event trait for all bus events
pub trait Event: Send + Sync + Serialize + 'static {
    fn event_type(&self) -> &'static str;
    fn event_id(&self) -> Uuid;
    fn timestamp(&self) -> chrono::DateTime<chrono::Utc>;
    fn as_any(&self) -> &dyn Any;
}

/// Event envelope for transport
#[derive(Debug, Clone)]
pub struct EventEnvelope {
    pub id: Uuid,
    pub event_type: String,
    pub payload: serde_json::Value,
    pub metadata: HashMap<String, String>,
    pub timestamp: chrono::DateTime<chrono::Utc>,
}

/// Event bus trait
#[async_trait]
pub trait EventBus: Send + Sync + 'static {
    async fn publish<E: Event + Serialize + DeserializeOwned>(
        &self,
        event: E,
    ) -> Result<(), EventBusError>;

    /// Subscribe to events of a specific type
    async fn subscribe<E: Event + DeserializeOwned>(
        &self,
    ) -> Result<mpsc::Receiver<E>, EventBusError>;

    /// Subscribe to all events
    fn subscribe_all(&self) -> Result<broadcast::Receiver<EventEnvelope>, EventBusError>;
}

/// Event bus error types
#[derive(Debug, thiserror::Error)]
pub enum EventBusError {
    #[error("Failed to publish event: {0}")]
    PublishFailed(String),

    #[error("Failed to subscribe: {0}")]
    SubscribeFailed(String),

    #[error("Event type not registered: {0}")]
    UnknownEventType(String),

    #[error("Event bus is closed")]
    BusClosed,
}

/// In-memory event bus implementation
pub struct InMemoryEventBus {
    canonical: InMemoryBus,
    broadcast_tx: broadcast::Sender<EventEnvelope>,
    bridge: OnceCell<Subscription>,
}

impl InMemoryEventBus {
    pub fn new(capacity: usize) -> Self {
        let (tx, _) = broadcast::channel(capacity);
        Self {
            canonical: InMemoryBus::new(),
            broadcast_tx: tx,
            bridge: OnceCell::new(),
        }
    }

    async fn ensure_bridge(&self) -> Result<(), EventBusError> {
        let sender = self.broadcast_tx.clone();
        self.bridge
            .get_or_try_init(|| async move {
                self.canonical
                    .subscribe(Arc::new(move |event, _last_seen| {
                        let sender = sender.clone();
                        Box::pin(async move {
                            let mut metadata = HashMap::from([
                                ("source".to_string(), event.source),
                                (
                                    "schema_version".to_string(),
                                    event.schema_version.to_string(),
                                ),
                            ]);
                            if let Some(causation_id) = event.causation_id {
                                metadata
                                    .insert("causation_id".to_string(), causation_id.to_string());
                            }
                            if let Some(correlation_id) = event.correlation_id {
                                metadata.insert(
                                    "correlation_id".to_string(),
                                    correlation_id.to_string(),
                                );
                            }
                            let legacy = EventEnvelope {
                                id: event.id,
                                event_type: event.event_type,
                                payload: event.payload,
                                metadata,
                                timestamp: event.timestamp,
                            };
                            let _ = sender.send(legacy);
                            Ok(())
                        })
                    }))
                    .await
                    .map_err(|error| EventBusError::SubscribeFailed(error.to_string()))
            })
            .await
            .map(|_| ())
    }
}

impl Default for InMemoryEventBus {
    fn default() -> Self {
        Self::new(1000)
    }
}

#[async_trait]
impl EventBus for InMemoryEventBus {
    async fn publish<E: Event>(&self, event: E) -> Result<(), EventBusError> {
        self.ensure_bridge().await?;
        self.canonical
            .publish(CanonicalEnvelope {
                id: event.event_id(),
                event_type: event.event_type().to_string(),
                source: LEGACY_SOURCE.to_string(),
                timestamp: event.timestamp(),
                causation_id: None,
                correlation_id: None,
                schema_version: 1,
                payload: serde_json::to_value(&event)
                    .map_err(|error| EventBusError::PublishFailed(error.to_string()))?,
            })
            .await
            .map_err(|error| EventBusError::PublishFailed(error.to_string()))?;
        Ok(())
    }

    async fn subscribe<E: Event + DeserializeOwned>(
        &self,
    ) -> Result<mpsc::Receiver<E>, EventBusError> {
        let (tx, rx) = mpsc::channel(100);
        self.ensure_bridge().await?;
        let mut events = self.broadcast_tx.subscribe();
        tokio::spawn(async move {
            loop {
                tokio::select! {
                    _ = tx.closed() => break,
                    received = events.recv() => match received {
                        Ok(envelope) => {
                            let event_type = envelope.event_type;
                            if let Ok(event) = serde_json::from_value::<E>(envelope.payload) {
                                if event.event_type() == event_type && tx.send(event).await.is_err() {
                                    break;
                                }
                            }
                        }
                        Err(broadcast::error::RecvError::Lagged(skipped)) => {
                            tracing::warn!(skipped, "typed event subscription lagged; events were skipped");
                            continue;
                        }
                        Err(broadcast::error::RecvError::Closed) => break,
                    }
                }
            }
        });

        Ok(rx)
    }

    fn subscribe_all(&self) -> Result<broadcast::Receiver<EventEnvelope>, EventBusError> {
        Ok(self.broadcast_tx.subscribe())
    }
}

/// Event handler trait
#[async_trait]
pub trait EventHandler<E: Event>: Send + Sync {
    async fn handle(&self, event: E) -> Result<(), EventBusError>;
}

/// Event bus builder
pub struct EventBusBuilder {
    capacity: usize,
    enable_persistence: bool,
}

impl EventBusBuilder {
    pub fn new() -> Self {
        Self {
            capacity: 1000,
            enable_persistence: false,
        }
    }

    pub fn with_capacity(mut self, capacity: usize) -> Self {
        self.capacity = capacity;
        self
    }

    pub fn with_persistence(mut self, enabled: bool) -> Self {
        self.enable_persistence = enabled;
        self
    }

    pub fn build(self) -> Arc<InMemoryEventBus> {
        Arc::new(InMemoryEventBus::new(self.capacity))
    }
}

impl Default for EventBusBuilder {
    fn default() -> Self {
        Self::new()
    }
}

/// Event stream for reactive processing
pub struct EventStream {
    receiver: broadcast::Receiver<EventEnvelope>,
}

impl EventStream {
    pub async fn next(&mut self) -> Option<EventEnvelope> {
        self.receiver.recv().await.ok()
    }

    pub fn filter<F>(self, predicate: F) -> FilteredStream<F>
    where
        F: Fn(&EventEnvelope) -> bool,
    {
        FilteredStream {
            inner: self,
            predicate,
        }
    }
}

/// Filtered event stream
pub struct FilteredStream<F> {
    inner: EventStream,
    predicate: F,
}

impl<F: Fn(&EventEnvelope) -> bool> FilteredStream<F> {
    pub async fn next(&mut self) -> Option<EventEnvelope> {
        loop {
            match self.inner.next().await {
                Some(event) if (self.predicate)(&event) => return Some(event),
                Some(_) => continue,
                None => return None,
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{Event, EventBus, InMemoryEventBus, LEGACY_SOURCE};
    use chrono::{DateTime, Utc};
    use serde::{Deserialize, Serialize};
    use tokio::time::{timeout, Duration};
    use uuid::Uuid;

    #[derive(Debug, Clone, Deserialize, Serialize)]
    struct UserCreated {
        id: Uuid,
        timestamp: DateTime<Utc>,
    }

    impl Event for UserCreated {
        fn event_type(&self) -> &'static str {
            "user.created"
        }

        fn event_id(&self) -> Uuid {
            self.id
        }

        fn timestamp(&self) -> DateTime<Utc> {
            self.timestamp
        }

        fn as_any(&self) -> &dyn std::any::Any {
            self
        }
    }

    #[tokio::test]
    async fn publish_forwards_through_the_canonical_bus() {
        let bus = InMemoryEventBus::default();
        let mut all_events = bus.subscribe_all().expect("subscribe all");
        let event = UserCreated {
            id: Uuid::now_v7(),
            timestamp: Utc::now(),
        };

        bus.publish(event.clone()).await.expect("publish");

        let envelope = timeout(Duration::from_secs(1), all_events.recv())
            .await
            .expect("delivery timeout")
            .expect("broadcast delivery");
        assert_eq!(envelope.id, event.id);
        assert_eq!(envelope.event_type, "user.created");
        assert_eq!(envelope.payload["id"], event.id.to_string());
        assert_eq!(envelope.metadata["source"], LEGACY_SOURCE);
        assert_eq!(envelope.metadata["schema_version"], "1");
    }

    #[tokio::test]
    async fn typed_subscription_deserializes_legacy_events() {
        let bus = InMemoryEventBus::default();
        let mut receiver = bus.subscribe::<UserCreated>().await.expect("subscribe");
        tokio::task::yield_now().await;
        let event = UserCreated {
            id: Uuid::now_v7(),
            timestamp: Utc::now(),
        };

        bus.publish(event.clone()).await.expect("publish");

        let received = timeout(Duration::from_secs(1), receiver.recv())
            .await
            .expect("delivery timeout")
            .expect("typed delivery");
        assert_eq!(received.id, event.id);
    }
}
