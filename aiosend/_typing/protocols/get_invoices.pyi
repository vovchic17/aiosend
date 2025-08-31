from typing import Literal, Protocol

from aiosend.enums import InvoiceStatus
from aiosend.types import Invoice

class GetInvoicesProtocol(Protocol):
    async def get_invoices(
        self,
        invoice_ids: list[int] | None = None,
        status: Literal[InvoiceStatus.ACTIVE, InvoiceStatus.PAID]
        | None = None,
        count: int | None = None,
        **kwargs: object,
    ) -> list[Invoice]: ...
