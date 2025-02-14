import asyncio
from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic

from aiosend.types import _CryptoPayType

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from logging import Logger
    from typing import Any


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

    async def _start_polling(
        self,
        get_updates: "Callable[..., Awaitable[list[object]]]",
        handle_update: "Callable[[object], Awaitable[None]]",
        tasks: "dict[int, PollingTask]",
        updater_key: str,
        logger: "Logger",
    ) -> None:
        """Start polling."""
        while True:
            await asyncio.sleep(self._delay)
            if not tasks:
                continue
            updates = await get_updates(**{updater_key: list(tasks)})
            for update in updates:
                await handle_update(update)
            logger.debug(
                "Tasks left: %s Waiting %d seconds...",
                len(tasks),
                self._delay,
            )
