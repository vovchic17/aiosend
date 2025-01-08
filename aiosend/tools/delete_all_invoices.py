from typing import TYPE_CHECKING

from aiosend.enums import InvoiceStatus

if TYPE_CHECKING:
    import aiosend


class DeleteAllInvoices:
    """Delete all invoices."""

    async def delete_all_invoices(
        self: "aiosend.CryptoPay",
    ) -> None:
        """
        Delete all invoices.

        Wrapper for :class:`aiosend.CryptoPay.get_invoices`
        and :class:`aiosend.CryptoPay.delete_invoice`

        Use this method to delete all existing
        invoices created by your app.

        :return:
        """
        invoices = await self.get_invoices(status=InvoiceStatus.ACTIVE)
        for invoice in invoices:
            await invoice.delete()
