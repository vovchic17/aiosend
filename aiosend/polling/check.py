from typing import TYPE_CHECKING, Any

from aiosend import loggers
from aiosend._handler import HandlerObject
from aiosend.enums import CheckStatus

from .base import BasePollingManager, PollingTask

if TYPE_CHECKING:
    from collections.abc import Callable

    import aiosend
    from aiosend._handler import CallbackType
    from aiosend.types import Check


class CheckPollingManager(BasePollingManager):
    """Check polling manager."""

    def __init__(self) -> None:
        self._check_tasks: dict[int, PollingTask[Check]] = {}
        self._check_handlers: list[HandlerObject] = []
        self._exp_check_handlers: list[HandlerObject] = []

    def check_polling(
        self,
        *filters: "CallbackType",
    ) -> "Callable[[CallbackType], CallbackType]":
        """
        Register a handler for polling check updates.

        Decorator for handler function.

        :return: handler function.
        """

        def wrapper(handler: "CallbackType") -> "CallbackType":
            self._check_handlers.append(HandlerObject(handler, filters))
            return handler

        return wrapper

    def expired_check_polling(
        self,
        *filters: "CallbackType",
    ) -> "Callable[[CallbackType], CallbackType]":
        """
        Register a handler for timed out checks.

        Decorator for handler function.

        :return: handler function.
        """

        def wrapper(handler: "CallbackType") -> "CallbackType":
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
        task = self._check_tasks[check.check_id]
        if check.status == CheckStatus.ACTIVATED or task.timeout <= 0:
            del self._check_tasks[check.check_id]
        if task.timeout <= 0:
            for handler in self._exp_check_handlers:
                result, data = await handler.check(check)
                if result:
                    await handler.call(
                        check,
                        data | task.data | self._kwargs,
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
                result, data = await handler.check(check)
                if result:
                    await handler.call(
                        check,
                        data | task.data | self._kwargs,
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

    async def _start_check_polling(self: "aiosend.CryptoPay") -> None:
        """Start check polling."""
        await self._start_polling(
            self.get_checks,  # type: ignore[arg-type]
            self._handle_check,  # type: ignore[arg-type]
            self._check_tasks,
            "check_ids",
            loggers.check_polling,
        )
