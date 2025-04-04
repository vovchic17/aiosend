from datetime import datetime
from typing import cast

from pydantic import Field

from aiosend.enums import (
    Asset,
    CurrencyType,
    Fiat,
    InvoiceStatus,
    PaidBtnName,
)

from .base import CryptoPayObject


class Invoice(CryptoPayObject):
    """
    Invoice object.

    Source: https://help.crypt.bot/crypto-pay-api#Invoice
    """

    invoice_id: int
    """Unique ID for this invoice."""
    hash: str
    """Hash of the invoice."""
    currency_type: CurrencyType | str
    """Type of the price, can be “crypto” or “fiat”."""
    asset: Asset | str | None = None
    """*Optional*. Cryptocurrency code. Available only if the value of the field currency_type is “crypto”. Currently, can be “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet)."""
    fiat: Fiat | str | None = None
    """*Optional*. Fiat currency code. Available only if the value of the field currency_type is “fiat”. Currently one of “USD”, “EUR”, “RUB”, “BYN”, “UAH”, “GBP”, “CNY”, “KZT”, “UZS”, “GEL”, “TRY”, “AMD”, “THB”, “INR”, “BRL”, “IDR”, “AZN”, “AED”, “PLN” and “ILS"."""
    amount: float
    """Amount of the invoice for which the invoice was created."""
    paid_asset: Asset | str | None = None
    """*Optional*. Cryptocurrency alphabetic code for which the invoice was paid. Available only if currency_type is “fiat” and status is “paid”."""
    paid_amount: float | None = None
    """*Optional*. Amount of the invoice for which the invoice was paid. Available only if currency_type is “fiat” and status is “paid”."""
    paid_fiat_rate: float | None = None
    """*Optional*. The rate of the paid_asset valued in the fiat currency. Available only if the value of the field currency_type is “fiat” and the value of the field status is “paid”."""
    accepted_assets: list[Asset | str] | None = None
    """*Optional*. List of assets which can be used to pay the invoice. Available only if currency_type is “fiat”. Currently, can be “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet)."""
    fee_asset: Asset | str | None = None
    """*Optional*. Asset of service fees charged when the invoice was paid. Available only if status is “paid”."""
    fee_amount: float | None = None
    """*Optional*. Amount of service fees charged when the invoice was paid. Available only if status is “paid”."""
    fee_in_usd: float | None = None
    """*Optional*. Amount in USD of service fees charged when the invoice was paid. Available only if status is “paid”."""
    fee: str | None = Field(
        None,
        deprecated="fee field is deprecated, use fee_amount instead.",
    )
    """*Optional*. Amount of charged service fees. Available only in the payload of the webhook update (described here for reference)."""
    pay_url: str | None = Field(
        None,
        deprecated="pay_url field is deprecated, use bot_invoice_url instead.",
    )
    """*Deprecated*. URL should be provided to the user to pay the invoice (described here for reference)."""
    bot_invoice_url: str
    """URL should be provided to the user to pay the invoice."""
    mini_app_invoice_url: str
    """Use this URL to pay an invoice to the Telegram Mini App version."""
    web_app_invoice_url: str
    """Use this URL to pay an invoice to the Web version of Crypto Bot."""
    description: str | None = None
    """*Optional*. Description for this invoice."""
    status: InvoiceStatus | str | None = None
    """Status of the transfer, can be “active”, “paid” or “expired”."""
    created_at: datetime
    """Date the invoice was created in ISO 8601 format."""
    paid_usd_rate: float | None = None
    """*Optional*. Price of the asset in USD. Available only if status is “paid”."""
    usd_rate: str | None = Field(
        None,
        deprecated="usd_rate field is deprecated, use paid_usd_rate instead.",
    )
    """*Optional*. Price of the asset in USD. Available only in the Webhook update payload."""
    allow_comments: bool
    """True, if the user can add comment to the payment."""
    allow_anonymous: bool
    """True, if the user can pay the invoice anonymously."""
    expiration_date: datetime | None = None
    """*Optional*. Date the invoice expires in ISO 8601 format."""
    paid_at: datetime | None = None
    """*Optional*. Date the invoice was paid in ISO 8601 format."""
    paid_anonymously: bool | None = None
    """True, if the invoice was paid anonymously."""
    comment: str | None = None
    """*Optional*. Comment to the payment from the user."""
    hidden_message: str | None = None
    """*Optional*. Text of the hidden message for this invoice."""
    payload: str | None = None
    """*Optional*. Previously provided data for this invoice."""
    paid_btn_name: PaidBtnName | str | None = None
    """*Optional*. Label of the button, can be “viewItem”, “openChannel”, “openBot” or “callback”."""
    paid_btn_url: str | None = None
    """*Optional*. URL opened using the button."""

    async def delete(self) -> bool:
        """
        Shortcut for method :meth:`aiosend.CryptoPay.delete_invoice`.

        Use this method to delete invoice created by your app.
        Returns :code:`True` on success.

        Source: https://help.crypt.bot/crypto-pay-api#hwjK

        :return: :code:`True` on success.
        """
        return await self._client.delete_invoice(self.invoice_id)

    async def update(self) -> None:
        """
        Shortcut for method :meth:`aiosend.CryptoPay.get_invoices`.

        Use this method to update invoice object.

        Source: https://help.crypt.bot/crypto-pay-api#getInvoices

        :return:
        """
        invoice = cast("Invoice", await self._client.get_invoice(self))
        self.__dict__ = invoice.__dict__

    def poll(self, **kwargs: object) -> None:
        """
        Send the invoice to the polling manager.

        Use this method to check the status of
        the invoice until the timeout expires.

        :param kwargs: additional payload for the handler.

        :return:
        """
        self._client._poll_invoice(self, kwargs)  # noqa: SLF001

    @property
    def qr(self) -> str:
        """
        Get invoice qr code.

        :return: invoice qr code url.
        """
        return self._client.session.network.get_qr(self.bot_invoice_url)
