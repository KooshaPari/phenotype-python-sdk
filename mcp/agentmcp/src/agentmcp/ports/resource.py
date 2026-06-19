"""Resource port."""

from abc import ABC, abstractmethod


class ResourcePort(ABC):
    @abstractmethod
    def fetch(self, uri: str) -> bytes:
        """Fetch resource by URI."""
        ...

    @abstractmethod
    def list(self) -> list[str]:
        """List available resource URIs."""
        ...
