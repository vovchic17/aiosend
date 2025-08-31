from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from aiosend import loggers
from aiosend.enums import InvoiceStatus

from .base import BasePollingManager, PollingTask
from .router import PollingRouter

if TYPE_CHECKING:
    from typing import Literal

    from aiosend.enums import Asset, Fiat
    from aiosend.types import Invoice


class InvoicePollingManager(BasePollingManager, PollingRouter, ABC):
    """Invoice polling manager."""

    def __init__(self) -> None:
        super().__init__()
        self._invoice_tasks: dict[int, PollingTask[Invoice]] = {}

    @abstractmethod
    async def get_invoices(  # noqa: PLR0913
        self,
        asset: "Asset | None" = None,
        fiat: "Fiat | None" = None,
        invoice_ids: list[int] | None = None,
        status: """Literal[InvoiceStatus.ACTIVE,
        InvoiceStatus.PAID] | None""" = None,
        offset: int | None = None,
        count: int | None = None,
    ) -> list["Invoice"]:
        """getinvoices method."""

    def _poll_invoice(
        self,
        invoice: "Invoice",
        **kwargs: object,
    ) -> None:
        self._invoice_tasks[invoice.invoice_id] = PollingTask(
            invoice,
            self._timeout,
            kwargs,
        )

    async def _handle_invoice(
        self,
        invoice: "Invoice",
    ) -> None:
        task = self._invoice_tasks[invoice.invoice_id]
        task.timeout -= self._delay
        if (
            invoice.status in (InvoiceStatus.PAID, InvoiceStatus.EXPIRED)
            or task.timeout <= 0
        ):
            del self._invoice_tasks[invoice.invoice_id]
        if task.timeout <= 0 or invoice.status == InvoiceStatus.EXPIRED:
            if await self.propagate_event(
                invoice,
                "invoice_expired",
                **task.data | self._kwargs,
            ):
                loggers.polling.info(
                    "EXPIRED INVOICE id=%d is handled.",
                    invoice.invoice_id,
                )
            else:
                loggers.polling.info(
                    "EXPIRED INVOICE id=%d is not handled.",
                    invoice.invoice_id,
                )

        elif invoice.status == InvoiceStatus.PAID:
            if await self.propagate_event(
                invoice,
                "invoice_paid",
                **task.data | self._kwargs,
            ):
                loggers.polling.info(
                    "PAID INVOICE id=%d is handled.",
                    invoice.invoice_id,
                )
            else:
                loggers.polling.info(
                    "PAID INVOICE id=%d is not handled.",
                    invoice.invoice_id,
                )

    async def _start_invoice_polling(self) -> None:
        """Start invoice polling."""
        await self._start_polling(
            self.get_invoices,
            self._handle_invoice,
            self._invoice_tasks,
            "invoice_ids",
        )
