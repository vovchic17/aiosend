from aiosend.client.client import NoneType
from aiosend.enums import Asset, Fiat

from .base import CryptoPayObject

class ExchangeRate(CryptoPayObject):
    is_valid: bool
    is_crypto: bool
    is_fiat: bool
    source: Asset | Fiat | str
    target: Fiat | str
    rate: float

    def update(self) -> NoneType: ...
