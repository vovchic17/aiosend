from typing import Protocol

from aiosend._methods import CryptoPayMethod
from aiosend.types import _CryptoPayType

class ClientProtocol(Protocol):
    async def __call__(
        self,
        method: CryptoPayMethod[_CryptoPayType],
    ) -> _CryptoPayType: ...
