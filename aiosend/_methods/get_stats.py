from datetime import datetime
from typing import TYPE_CHECKING

from aiosend.types import AppStats

from .base import CryptoPayMethod

if TYPE_CHECKING:
    import aiosend


class GetStats:
    """getStats method."""

    class GetStatsMethod(CryptoPayMethod[AppStats]):
        __return_type__ = AppStats
        __method__ = "getStats"

        start_at: datetime | None
        end_at: datetime | None

    async def get_stats(
        self: "aiosend.CryptoPay",
        start_at: datetime | None = None,
        end_at: datetime | None = None,
    ) -> AppStats:
        """
        getStats method.

        Use this method to get app statistics.
        On success, returns :class:`aiosend.types.AppStats`.

        Source: https://help.crypt.bot/crypto-pay-api#jvP3

        :param start_at: *Optional*. Date from which start calculating statistics. Default is current date minus 24 hours.
        :param end_at: *Optional*. The date on which to finish calculating statistics. Default is current date.
        :return: :class:`aiosend.types.AppStats` object.
        """
        return await self(self.GetStatsMethod(**locals()))
