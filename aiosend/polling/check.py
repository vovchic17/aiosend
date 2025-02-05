import asyncio
from typing import TYPE_CHECKING, Any

from magic_filter.magic import MagicFilter

from aiosend import loggers
from aiosend.enums import CheckStatus
from aiosend.handler import HandlerObject

from .base import BasePollingManager, PollingTask

if TYPE_CHECKING:
    from collections.abc import Callable

    import aiosend
    from aiosend.handler import Handler
    from aiosend.types import Check


class CheckPollingManager(BasePollingManager):
    """Check polling manager."""

    def __init__(self) -> None:
        self._check_tasks: dict[int, PollingTask[Check]] = {}
        self._check_handlers: list[HandlerObject] = []
        self._exp_check_handlers: list[HandlerObject] = []

    def check_polling(
        self,
        *filters: MagicFilter,
    ) -> "Callable[[Handler], Handler]":
        """
        Register a handler for polling check updates.

        Decorator for handler function.

        :return: handler function.
        """

        def wrapper(handler: "Handler") -> "Handler":
            self._check_handlers.append(HandlerObject(handler, filters))
            return handler

        return wrapper

    def expired_check_polling(
        self,
        *filters: MagicFilter,
    ) -> "Callable[[Handler], Handler]":
        """
        Register a handler for timed out checks.

        Decorator for handler function.

        :return: handler function.
        """

        def wrapper(handler: "Handler") -> "Handler":
            self._exp_check_handlers.append(HandlerObject(handler, filters))
            return handler

        return wrapper

    def _poll_check(self, check: "Check", data: dict[str, Any]) -> None:
        self._check_tasks[check.check_id] = PollingTask(
            check,
            self._timeout,
            data,
        )

    async def _handle_check(self: "aiosend.CryptoPay", check: "Check") -> None:
        self._check_tasks[check.check_id].timeout -= self._delay
        if self._check_tasks[check.check_id].timeout <= 0:
            for handler in self._exp_check_handlers:
                if handler.check(check):
                    await handler.call(
                        check,
                        self._check_tasks[check.check_id].data | self._kwargs,
                    )
                    loggers.check_polling.info(
                        "ACTIVATED CHECK id=%d is handled.",
                        check.check_id,
                    )
                    break
            else:
                loggers.check_polling.info(
                    "ACTIVATED CHECK id=%d is not handled.",
                    check.check_id,
                )
        elif check.status == CheckStatus.ACTIVATED:
            for handler in self._check_handlers:
                if handler.check(check):
                    await handler.call(
                        check,
                        self._check_tasks[check.check_id].data | self._kwargs,
                    )
                    loggers.check_polling.info(
                        "EXPIRED CHECK id=%d is handled.",
                        check.check_id,
                    )
                    break
            else:
                loggers.check_polling.info(
                    "EXPIRED CHECK id=%d is not handled.",
                    check.check_id,
                )

        if (
            check.status == CheckStatus.ACTIVATED
            or self._check_tasks[check.check_id].timeout <= 0
        ):
            del self._check_tasks[check.check_id]

    async def _start_check_polling(self: "aiosend.CryptoPay") -> None:
        """Start check polling."""
        while True:
            await asyncio.sleep(self._delay)
            if not self._check_tasks:
                continue
            checks = await self.get_checks(
                check_ids=list(self._check_tasks),
            )
            for check in checks:
                await self._handle_check(check)
            loggers.check_polling.debug(
                "Tasks left: %s Waiting %d seconds...",
                len(self._check_tasks),
                self._delay,
            )
