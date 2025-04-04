from typing import TYPE_CHECKING

from pydantic import Field, model_validator

from aiosend.enums import Asset, CurrencyType, Fiat, PaidBtnName
from aiosend.exceptions import MethodValuesError
from aiosend.types import Invoice, SerList

from .base import CryptoPayMethod

if TYPE_CHECKING:
    import aiosend


class CreateInvoice:
    """createInvoice method."""

    class CreateInvoiceMethod(CryptoPayMethod[Invoice]):
        __return_type__ = Invoice
        __method__ = "createInvoice"

        currency_type: str | None
        asset: str | None
        fiat: str | None
        accepted_assets: SerList[Asset] | None
        amount: float
        description: str | None
        hidden_message: str | None
        paid_btn_name: str | None
        paid_btn_url: str | None
        payload: str | None
        allow_comments: bool | None
        allow_anonymous: bool | None
        expires_in: int | None = Field(None, ge=0, le=2678400)

        @model_validator(mode="before")
        @classmethod
        def values_validate(cls, values: dict) -> dict:
            """Validate model values."""
            errors = {
                values["currency_type"] in (None, "crypto")
                and values["asset"]
                is None: 'asset is required if currency_type is "crypto"',
                values["currency_type"] == "fiat"
                and values["fiat"]
                is None: 'fiat is required if currency_type is "fiat"',
                values["currency_type"] != "fiat"
                and values["accepted_assets"]
                is not None: 'accepted_assets avaliable only if currency_type is "fiat"',
                values["paid_btn_name"] is not None
                and values["paid_btn_url"]
                is None: "paid_btn_url required if paid_btn_name is specified.",
            }
            for error, message in errors.items():
                if error:
                    raise MethodValuesError(message)

            return values

    async def create_invoice(
        self: "aiosend.CryptoPay",
        amount: float,
        asset: Asset | None = None,
        *,
        currency_type: CurrencyType | None = None,
        fiat: Fiat | None = None,
        accepted_assets: list[Asset] | None = None,
        description: str | None = None,
        hidden_message: str | None = None,
        paid_btn_name: PaidBtnName | None = None,
        paid_btn_url: str | None = None,
        payload: str | None = None,
        allow_comments: bool | None = None,
        allow_anonymous: bool | None = None,
        expires_in: int | None = None,
    ) -> Invoice:
        """
        createInvoice method.

        Use this method to create a new invoice.
        On success, returns an object of the created :class:`aiosend.types.Invoice`.

        Source: https://help.crypt.bot/crypto-pay-api#createInvoice

        :param amount: Amount of the invoice in float. For example: `125.50`
        :param currency_type: *Optional*. Type of the price, can be “crypto” or “fiat”. Defaults to crypto.
        :param asset: *Optional*. Required if currency_type is “crypto”. Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC”.
        :param fiat: *Optional*. Required if currency_type is “fiat”. Fiat currency code. Supported fiat currencies: “USD”, “EUR”, “RUB”, “BYN”, “UAH”, “GBP”, “CNY”, “KZT”, “UZS”, “GEL”, “TRY”, “AMD”, “THB”, “INR”, “BRL”, “IDR”, “AZN”, “AED”, “PLN” and “ILS".
        :param accepted_assets: *Optional*. List of cryptocurrency alphabetic codes. Assets which can be used to pay the invoice. Available only if currency_type is “fiat”. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet). Defaults to all currencies.
        :param description: *Optional*. Description for the invoice. User will see this description when they pay the invoice. Up to 1024 characters.
        :param hidden_message: *Optional*. Text of the message which will be presented to a user after the invoice is paid. Up to 2048 characters.
        :param paid_btn_name: *Optional*. Label of the button which will be presented to a user after the invoice is paid.
        :param paid_btn_url: *Optional*. Required if paid_btn_name is specified. URL opened using the button which will be presented to a user after the invoice is paid. You can set any callback link (for example, a success link or link to homepage). Starts with https or http.
        :param payload: *Optional*. Any data you want to attach to the invoice (for example, user ID, payment ID, ect). Up to 4kb.
        :param allow_comments: *Optional*. Allow a user to add a comment to the payment. Defaults to :code:`True`.
        :param allow_anonymous: *Optional*. Allow a user to pay the invoice anonymously. Defaults to :code:`True`.
        :param expires_in: *Optional*. You can set a payment time limit for the invoice in seconds. Values between 1-2678400 are accepted.
        :return: :class:`aiosend.types.Invoice` object
        """
        return await self(self.CreateInvoiceMethod(**locals()))
