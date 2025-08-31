from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from aiosend import loggers
from aiosend.enums import CheckStatus

from .base import BasePollingManager, PollingTask
from .router import PollingRouter

if TYPE_CHECKING:
    from aiosend.enums import Asset
    from aiosend.types import Check


class CheckPollingManager(BasePollingManager, PollingRouter, ABC):
    """Check polling manager."""

    def __init__(self) -> None:
        super().__init__()
        self._check_tasks: dict[int, PollingTask[Check]] = {}

    @abstractmethod
    async def get_checks(
        self,
        asset: "Asset | None" = None,
        check_ids: list[int] | None = None,
        status: CheckStatus | None = None,
        offset: int | None = None,
        count: int | None = None,
    ) -> list["Check"]:
        """getchecks method."""

    def _poll_check(self, check: "Check", **kwargs: object) -> None:
        self._check_tasks[check.check_id] = PollingTask(
            check,
            self._timeout,
            kwargs,
        )

    async def _handle_check(self, check: "Check") -> None:
        task = self._check_tasks[check.check_id]
        task.timeout -= self._delay
        if check.status == CheckStatus.ACTIVATED or task.timeout <= 0:
            del self._check_tasks[check.check_id]
        if task.timeout <= 0:
            if await self.propagate_event(
                check,
                "check_expired",
                **task.data | self._kwargs,
            ):
                loggers.polling.info(
                    "EXPIRED CHECK id=%d is handled.",
                    check.check_id,
                )
            else:
                loggers.polling.info(
                    "EXPIRED CHECK id=%d is not handled.",
                    check.check_id,
                )
        elif check.status == CheckStatus.ACTIVATED:
            if await self.propagate_event(
                check,
                "check_activated",
                **task.data | self._kwargs,
            ):
                loggers.polling.info(
                    "ACTIVATED CHECK id=%d is handled.",
                    check.check_id,
                )
            else:
                loggers.polling.info(
                    "ACTIVATED CHECK id=%d is not handled.",
                    check.check_id,
                )

    async def _start_check_polling(self) -> None:
        """Start check polling."""
        await self._start_polling(
            self.get_checks,
            self._handle_check,
            self._check_tasks,
            "check_ids",
        )
