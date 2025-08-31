from typing import Protocol

from aiosend.types import ExchangeRate

class GetExchangeRatesProtocol(Protocol):
    async def get_exchange_rates(self) -> list[ExchangeRate]: ...
