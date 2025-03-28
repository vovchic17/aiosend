from datetime import datetime

from aiosend.client.client import (  # type: ignore[attr-defined]  # type: ignore[attr-defined]
    NoneType,
    _str,
    bool,  # noqa: A004  # noqa: A004
    str,  # noqa: A004
)
from aiosend.enums import Asset, CheckStatus, LiteralFiat

from .base import CryptoPayObject

class Check(CryptoPayObject):
    check_id: int
    hash: _str
    asset: Asset | _str
    amount: float
    bot_check_url: _str
    status: CheckStatus | _str
    created_at: datetime
    activated_at: datetime | None = None

    def delete(self) -> bool: ...
    def update(self) -> NoneType: ...
    def poll(self, **kwargs: object) -> None: ...
    @property
    def qr(self) -> _str: ...
    def get_image(self, fiat: LiteralFiat | _str) -> str: ...
