from typing import TYPE_CHECKING

from aiosend.enums import Asset, CheckStatus
from aiosend.types import Check, SerList

from .base import CryptoPayMethod

if TYPE_CHECKING:
    import aiosend


class GetChecks:
    """getChecks method."""

    class GetChecksMethod(CryptoPayMethod[list[Check]]):
        __return_type__ = list[Check]
        __method__ = "getChecks"

        asset: str | None = None
        check_ids: SerList[int] | None
        status: str | None
        offset: int | None
        count: int | None

    async def get_checks(
        self: "aiosend.CryptoPay",
        asset: Asset | None = None,
        check_ids: list[int] | None = None,
        status: CheckStatus | None = None,
        offset: int | None = None,
        count: int | None = None,
    ) -> list[Check]:
        """
        getChecks method.

        Use this method to get checks created by your app.
        On success, returns array of :class:`Check`.

        Source: https://help.crypt.bot/crypto-pay-api#getChecks

        :param asset: *Optional*. Cryptocurrency alphabetic code.
        :param check_ids: *Optional*. List of check IDs.
        :param status: *Optional*. Status of check to be returned. Available statuses: “active” and “activated”.
        :param offset: *Optional*. Offset needed to return a specific subset of check. Defaults to 0.
        :param count: *Optional*. Number of check to be returned. Values between 1-1000 are accepted. Defaults to 100.
        :return: List of :class:`Check` objects.
        """
        return await self(self.GetChecksMethod(**locals()))
