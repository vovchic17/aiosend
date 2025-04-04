from typing import TYPE_CHECKING

from aiosend.types import Invoice

if TYPE_CHECKING:
    import aiosend


class GetInvoice:
    """Get invoice."""

    async def get_invoice(
        self: "aiosend.CryptoPay",
        invoice: int | Invoice,
    ) -> Invoice | None:
        """
        Get exactly one invoice or none.

        Wrapper for :meth:`aiosend.CryptoPay.get_invoices`

        Use this method to update status of an existing invoice
        object or to get this object by passing the invoice id.

        :return: :class:`aiosend.types.Invoice` object.
        """
        invoice_id = (
            invoice.invoice_id if isinstance(invoice, Invoice) else invoice
        )

        invoices = await self.get_invoices(invoice_ids=[invoice_id])
        if invoices:
            return invoices[0]
        return None
