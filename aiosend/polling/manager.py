import asyncio
import inspect
from dataclasses import dataclass
from functools import partial
from typing import TYPE_CHECKING, cast

from aiosend import loggers
from aiosend.enums import InvoiceStatus
from aiosend.exceptions import CryptoPayError

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any

    import aiosend
    from aiosend.types import Invoice

    Handler = Callable[..., Any]


@dataclass(slots=True)
class PollingConfig:
    """Polling configuration."""

    timeout: int = 300
    """Timeout in seconds."""
    delay: int = 2
    """Time to wait between the requests in seconds."""


@dataclass(slots=True)
class PollingTask:
    """
    Wrapper for an Invoice.

    This class is used to make a polling task.
    """

    invoice: "Invoice"
    """Invoice object."""
    timeout: int
    """Remaining time for checking the invoice status."""
    data: "dict[str, Any]"
    """Additional payload"""


class PollingManager:
    """
    Polling manager class.

    This class is used to handle payments
    via invoices polling method.
    """

    def __init__(
        self,
        config: PollingConfig,
    ) -> None:
        self._timeout = config.timeout
        self._delay = config.delay
        self._tasks: dict[int, PollingTask] = {}
        self._handler: Handler | None = None
        self._exp_handler: Handler | None = None

    def polling_handler(self) -> "Callable[[Handler], Handler]":
        """
        Register a handler for polling invoice updates.

        Decorator for handler function.

        :return: handler function.
        """

        def wrapper(handler: "Handler") -> "Handler":
            if self._handler is not None:
                msg = "Polling handler has already been declared"
                raise CryptoPayError(msg)
            self._handler = handler
            return handler

        return wrapper

    def expired_handler(self) -> "Callable[[Handler], Handler]":
        """
        Register a handler for timed out invoices.

        Decorator for handler function.

        :return: handler function.
        """

        def wrapper(handler: "Handler") -> "Handler":
            if self._exp_handler is not None:
                msg = "Expired handler has already been declared"
                raise CryptoPayError(msg)
            self._exp_handler = handler
            return handler

        return wrapper

    def _add_invoice(
        self,
        invoice: "Invoice",
        data: "dict[str, Any]",
    ) -> None:
        if self._handler is None:
            msg = "Polling handler hasn't been declared"
            raise CryptoPayError(msg)
        self._tasks[invoice.invoice_id] = PollingTask(
            invoice=invoice,
            timeout=self._timeout,
            data=data,
        )

    @staticmethod
    async def __call_handler(
        handler: "Handler",
        invoice: "Invoice",
        data: "dict[str, Any]",
    ) -> None:
        spec = inspect.getfullargspec(handler)
        is_async = inspect.iscoroutinefunction(handler)
        handler = partial(
            handler,
            invoice,
            **data
            if spec.varkw is not None
            else {k: v for k, v in data.items() if k in spec.args},
        )
        if is_async:
            await handler()
        else:
            handler()

    async def __process_invoice(
        self,
        invoice: "Invoice",
    ) -> None:
        self._tasks[invoice.invoice_id].timeout -= self._delay
        if invoice.status == InvoiceStatus.PAID:
            await self.__call_handler(
                cast("Handler", self._handler),
                invoice,
                self._tasks[invoice.invoice_id].data,
            )
            loggers.polling.info(
                "Invoice id=%d has been paid",
                invoice.invoice_id,
            )
        if (
            self._tasks[invoice.invoice_id].timeout <= 0
            or invoice.status == InvoiceStatus.EXPIRED
        ):
            if self._exp_handler is not None:
                await self.__call_handler(
                    cast("Handler", self._exp_handler),
                    invoice,
                    self._tasks[invoice.invoice_id].data,
                )
            loggers.polling.info(
                "Invoice id=%d timed out",
                invoice.invoice_id,
            )
        if (
            invoice.status in (InvoiceStatus.PAID, InvoiceStatus.EXPIRED)
            or self._tasks[invoice.invoice_id].timeout <= 0
        ):
            del self._tasks[invoice.invoice_id]

    async def start_polling(
        self: "aiosend.CryptoPay",
        parallel: "Callable[[], Any] | None" = None,
    ) -> None:
        """
        Run invoices polling.

        :param parallel: function to run in background.
        :raises CryptoPayError: when polling handler is not declared.
        """
        if parallel is not None:
            loop = asyncio.get_event_loop()
            loop.run_in_executor(None, parallel)
        if self._handler is None:
            msg = (
                "Polling handler hasn't been declared, example:\n"
                "from aiosend import CryptoPay\n"
                'cp = CryptoPay("TOKEN")\n'
                "@cp.polling_handler()\n"
                "async def handler(invoice): ..."
            )
            raise CryptoPayError(msg)
        loggers.polling.info("Start polling")
        while True:
            await asyncio.sleep(self._delay)
            if not self._tasks:
                continue
            invoices = await self.get_invoices(
                invoice_ids=list(self._tasks),
            )
            for invoice in invoices:
                await self.__process_invoice(invoice)
            loggers.polling.debug(
                "Tasks left: %s Waiting %d seconds...",
                len(self._tasks),
                self._delay,
            )
