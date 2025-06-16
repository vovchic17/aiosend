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
    asset: Asset | str | None
    fiat: Fiat | str | None
    amount: float
    paid_asset: Asset | str | None
    paid_amount: float | None
    paid_fiat_rate: float | None
    accepted_assets: list[Asset | str] | None
    fee_asset: Asset | str | None
    fee_amount: float | None
    fee_in_usd: float | None
    fee: str | None
    pay_url: str | None
    bot_invoice_url: str
    mini_app_invoice_url: str
    web_app_invoice_url: str
    description: str | None
    status: InvoiceStatus | str | None
    swap_to: Asset | str | None
    is_swapped: bool | None
    swapped_uid: str | None
    swapped_to: Asset | None
    swapped_rate: float | None
    swapped_output: float | None
    swapped_usd_amount: float | None
    swapped_usd_rate: float | None
    created_at: datetime
    paid_usd_rate: float | None
    usd_rate: str | None
    allow_comments: _bool
    allow_anonymous: _bool
    expiration_date: datetime | None
    paid_at: datetime | None
    paid_anonymously: _bool | None
    comment: str | None
    hidden_message: str | None
    payload: str | None
    paid_btn_name: PaidBtnName | str | None
    paid_btn_url: str | None

    def delete(self) -> bool: ...
    def update(self) -> NoneType: ...
    def poll(self, **kwargs: object) -> None: ...
    @property
    def qr(self) -> str: ...
