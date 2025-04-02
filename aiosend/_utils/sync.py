import asyncio
import functools
import inspect
import sys
from contextlib import suppress
from typing import TYPE_CHECKING

from aiosend.client import CryptoPay
from aiosend.types import CryptoPayObject

if TYPE_CHECKING:
    from collections.abc import Awaitable


def async_to_sync(obj: object, name: str) -> None:
    """Set asyncio event loop if it's not running."""
    method = getattr(obj, name)

    @functools.wraps(method)
    def sync_wrapper(
        *args: object,
        **kwargs: object,
    ) -> object:
        coro: Awaitable = method(*args, **kwargs)
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        if loop.is_running():
            return coro
        return loop.run_until_complete(coro)

    setattr(obj, name, sync_wrapper)


def syncify(obj: object) -> None:
    """Add decorators to all public methods of the object."""
    for name in dir(obj):
        with suppress(AttributeError):
            if not name.startswith("_") and inspect.iscoroutinefunction(
                getattr(obj, name),
            ):
                async_to_sync(obj, name)


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

for base in (*CryptoPay.__bases__, *CryptoPayObject.__subclasses__()):
    syncify(base)
