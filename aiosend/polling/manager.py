import asyncio
import warnings
from typing import TYPE_CHECKING

from aiosend import loggers

from .base import PollingConfig
from .check import CheckPollingManager
from .invoice import InvoicePollingManager

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any, Protocol

    class ClientWebhookManager("PollingManager", Protocol):  # type: ignore[misc]
        """Client webhook manager."""

        _webhook_manager: object


class PollingManager(InvoicePollingManager, CheckPollingManager):
    """
    Polling manager class.

    This class is used to handle payments
    and check activation via polling method.
    """

    def __init__(
        self,
        config: PollingConfig,
    ) -> None:
        InvoicePollingManager.__init__(self)
        CheckPollingManager.__init__(self)
        self._timeout = config.timeout
        self._delay = config.delay

    async def start_polling(
        self: "ClientWebhookManager",
        parallel: "Callable[[], Any] | None" = None,
    ) -> None:
        """
        Run polling.

        :param parallel: function to run in background.
        """
        if self._webhook_manager is not None:
            red = "\033[91m"
            reset = "\033[0m"
            warnings.warn(
                f"{red}Webhook manager is set. "
                f"Using polling may lead to event duplication.{reset}",
                stacklevel=2,
            )
        if parallel is not None:
            loop = asyncio.get_event_loop()
            loop.run_in_executor(None, parallel)
        loggers.polling.info("Start polling")
        await asyncio.gather(
            self._start_invoice_polling(),
            self._start_check_polling(),
        )
