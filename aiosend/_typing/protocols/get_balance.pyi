from typing import Protocol

from aiosend.types import Balance

class GetBalanceProtocol(Protocol):
    async def get_balance(self) -> list[Balance]: ...
