from typing import TYPE_CHECKING

from .base import CryptoPayMethod

if TYPE_CHECKING:
    from aiosend._typing import ClientProtocol


class DeleteInvoice:
    """deleteInvoice method."""

    class DeleteInvoiceMethod(CryptoPayMethod[bool]):
        __return_type__ = bool
        __method__ = "deleteInvoice"

        invoice_id: int

    async def delete_invoice(
        self: "ClientProtocol",
        invoice_id: int,
    ) -> bool:
        """
        deleteInvoice method.

        Use this method to delete invoices created by your app.
        Returns :code:`True` on success.

        Source: https://help.send.tg/en/articles/10279948-crypto-pay-api#h_da2ea9f39c

        :param invoice_id: Invoice ID to be deleted.
        :return: :code:`True` on success.
        """
        return await self(self.DeleteInvoiceMethod(**locals()))
