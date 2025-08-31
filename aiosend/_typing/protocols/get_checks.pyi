from typing import Protocol

from aiosend.enums import CheckStatus
from aiosend.types import Check

class GetChecksProtocol(Protocol):
    async def get_checks(
        self,
        check_ids: list[int] | None = None,
        status: CheckStatus | None = None,
        count: int | None = None,
        **kwargs: object,
    ) -> list[Check]: ...
