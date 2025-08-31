import asyncio
from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic

from aiosend import loggers
from aiosend.types import _CryptoPayType

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from typing import Any


@dataclass(slots=True)
class PollingConfig:  # type: ignore[misc]
    # https://github.com/python/mypy/issues/17121
    """Polling configuration."""

    timeout: int = 300
    """Timeout in seconds."""
    delay: int = 2
    """Time to wait between the requests in seconds."""


@dataclass(slots=True)
class PollingTask(Generic[_CryptoPayType]):  # type: ignore[misc]
    # https://github.com/python/mypy/issues/17121
    """
    Wrapper for an Invoice.

    This class is used to make a polling task.
    """

    obj: _CryptoPayType
    """Invoice object."""
    timeout: int
    """Remaining time for checking the invoice status."""
    data: dict[str, "Any"]
    """Additional payload"""


class BasePollingManager(ABC):
    """Base polling manager."""

    _timeout: int
    _delay: int
    _kwargs: dict[str, "Any"]

    async def _start_polling(
        self,
        get_updates: "Callable[..., Awaitable[list[Any]]]",
        handle_update: "Callable[[Any], Awaitable[None]]",
        tasks: "dict[int, PollingTask]",
        updater_key: str,
    ) -> None:
        """Start polling."""
        while True:
            await asyncio.sleep(self._delay)
            if not tasks:
                continue
            try:
                updates = await get_updates(**{updater_key: list(tasks)})
            except Exception:  # noqa: BLE001 logger catches exception
                loggers.polling.exception("Error while getting updates:\n")
                continue
            for update in updates:
                try:
                    await handle_update(update)
                except Exception:  # noqa: BLE001, PERF203
                    loggers.polling.exception(
                        "Error while handling update:\n",
                    )
                    continue
            loggers.polling.debug(
                "Tasks left: %s Waiting %d seconds...",
                len(tasks),
                self._delay,
            )
