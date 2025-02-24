from datetime import datetime

from aiosend.client.client import (  # type: ignore[attr-defined]
    NoneType,
    _bool,
    bool,  # noqa: A004
)
from aiosend.enums import (
    Asset,
    CurrencyType,
    Fiat,
    InvoiceStatus,
    PaidBtnName,
)

from .base import CryptoPayObject

class Invoice(CryptoPayObject):
    invoice_id: int
    hash: str
    currency_type: CurrencyType | str
    asset: Asset | str | None = None
    fiat: Fiat | str | None = None
    amount: float
    paid_asset: Asset | str | None = None
    paid_amount: float | None = None
    paid_fiat_rate: float | None = None
    accepted_assets: list[Asset | str] | None = None
    fee_asset: Asset | str | None = None
    fee_amount: float | None = None
    fee_in_usd: float | None = None
    fee: str | None = None
    pay_url: str | None = None
    bot_invoice_url: str
    mini_app_invoice_url: str
    web_app_invoice_url: str
    description: str | None = None
    status: InvoiceStatus | str | None = None
    created_at: datetime
    paid_usd_rate: float | None = None
    usd_rate: str | None = None
    allow_comments: _bool
    allow_anonymous: _bool
    expiration_date: datetime | None = None
    paid_at: datetime | None = None
    paid_anonymously: _bool | None = None
    comment: str | None = None
    hidden_message: str | None = None
    payload: str | None = None
    paid_btn_name: PaidBtnName | str | None = None
    paid_btn_url: str | None = None

    def delete(self) -> bool: ...
    def update(self) -> NoneType: ...
    def poll(self, **kwargs: object) -> None: ...
    @property
    def qr(self) -> str: ...
