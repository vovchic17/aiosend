from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic

from aiosend.types import _CryptoPayType


@dataclass(slots=True)
class PollingConfig:
    """Polling configuration."""

    timeout: int = 300
    """Timeout in seconds."""
    delay: int = 2
    """Time to wait between the requests in seconds."""


@dataclass(slots=True)
class PollingTask(Generic[_CryptoPayType]):
    """
    Wrapper for an Invoice.

    This class is used to make a polling task.
    """

    object: _CryptoPayType
    """Invoice object."""
    timeout: int
    """Remaining time for checking the invoice status."""
    data: dict[str, "Any"]
    """Additional payload"""


class BasePollingManager(ABC):
    """Base polling manager."""

    _timeout: int
    _delay: int

    @abstractmethod
    async def start_polling() -> None:
        """Start polling."""
