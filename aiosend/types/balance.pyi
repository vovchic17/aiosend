from aiosend.client.client import NoneType
from aiosend.enums import Asset

from .base import CryptoPayObject

class Balance(CryptoPayObject):
    currency_code: Asset | str
    available: float
    onhold: float

    def update(self) -> NoneType: ...
