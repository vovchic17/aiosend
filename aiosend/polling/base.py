import inspect
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from typing import Any, Generic

from magic_filter.magic import MagicFilter

from aiosend.types import _CryptoPayType

Handler = Callable[..., Any]


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


@dataclass(slots=True)
class HandlerObject:
    """Handler object."""

    handler: Handler
    filters: tuple[MagicFilter, ...]

    def check(self, obj: object) -> bool:
        """Check if the handler is suitable for the object."""
        return all(f.resolve(obj) for f in self.filters)

    async def call(self, obj: object, data: dict[str, "Any"]) -> None:
        """Call handler."""
        spec = inspect.getfullargspec(self.handler)
        is_async = inspect.iscoroutinefunction(self.handler)
        handler = partial(
            self.handler,
            obj,
            **data
            if spec.varkw is not None
            else {k: v for k, v in data.items() if k in spec.args},
        )
        if is_async:
            await handler()
        else:
            handler()


class BasePollingManager(ABC):
    """Base polling manager."""

    _timeout: int
    _delay: int

    @abstractmethod
    async def start_polling() -> None:
        """Start polling."""
