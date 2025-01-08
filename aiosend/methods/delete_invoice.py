from typing import TYPE_CHECKING

from .base import CryptoPayMethod

if TYPE_CHECKING:
    import aiosend


class DeleteInvoice:
    """deleteInvoice method."""

    class DeleteInvoiceMethod(CryptoPayMethod[bool]):
        __return_type__ = bool
        __method__ = "deleteInvoice"

        invoice_id: int

    async def delete_invoice(
        self: "aiosend.CryptoPay",
        invoice_id: int,
    ) -> bool:
        """
        deleteInvoice method.

        Use this method to delete invoices created by your app.
        Returns :code:`True` on success.

        Source: https://help.crypt.bot/crypto-pay-api#hwjK

        :param invoice_id: Invoice ID to be deleted.
        :return: :code:`True` on success.
        """
        return await self(self.DeleteInvoiceMethod(**locals()))
