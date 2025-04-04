from typing import TYPE_CHECKING

from pydantic import Field, field_serializer

from aiosend.enums import Asset, Fiat, InvoiceStatus
from aiosend.types import Invoice, SerList

from .base import CryptoPayMethod

if TYPE_CHECKING:
    import aiosend


class GetInvoices:
    """getInvoices method."""

    class GetInvoicesMethod(CryptoPayMethod[list[Invoice]]):
        __return_type__ = list[Invoice]
        __method__ = "getInvoices"

        asset: str | None
        fiat: str | None
        invoice_ids: SerList[int] | None
        status: InvoiceStatus | None
        offset: int | None
        count: int | None = Field(None, ge=1, le=1000)

        @field_serializer("invoice_ids")
        def serialize_ids(self, value: list[int] | None) -> str | None:
            """Serialize list of invoice ids."""
            if value is not None:
                return ",".join(map(str, value))
            return value

    async def get_invoices(
        self: "aiosend.CryptoPay",
        asset: Asset | None = None,
        fiat: Fiat | None = None,
        invoice_ids: list[int] | None = None,
        status: InvoiceStatus | None = None,
        offset: int | None = None,
        count: int | None = None,
    ) -> list[Invoice]:
        """
        getInvoices method.

        Use this method to get invoices created by your app.
        On success, returns array of :class:`aiosend.types.Invoice`.

        Source: https://help.crypt.bot/crypto-pay-api#getInvoices

        :param asset: *Optional*. Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet). Defaults to all currencies.
        :param fiat: *Optional*. Fiat currency code. Supported fiat currencies: “USD”, “EUR”, “RUB”, “BYN”, “UAH”, “GBP”, “CNY”, “KZT”, “UZS”, “GEL”, “TRY”, “AMD”, “THB”, “INR”, “BRL”, “IDR”, “AZN”, “AED”, “PLN” and “ILS". Defaults to all currencies.
        :param invoice_ids: *Optional*. List of invoice IDs separated by comma.
        :param status: *Optional*. Status of invoices to be returned. Available statuses: “active” and “paid”. Defaults to all statuses.
        :param offset: *Optional*. Offset needed to return a specific subset of invoices. Defaults to 0.
        :param count: *Optional*. Number of invoices to be returned. Values between 1-1000 are accepted. Defaults to 100.
        :return: List of :class:`aiosend.types.Invoice` objects.
        """
        return await self(self.GetInvoicesMethod(**locals()))
