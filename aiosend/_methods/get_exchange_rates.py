from typing import TYPE_CHECKING

from aiosend.types import ExchangeRate

from .base import CryptoPayMethod

if TYPE_CHECKING:
    from aiosend._typing import ClientProtocol


class GetExchangeRates:
    """getExchangeRates method."""

    class GetExchangeRates(CryptoPayMethod[list[ExchangeRate]]):
        __return_type__ = list[ExchangeRate]
        __method__ = "getExchangeRates"

    async def get_exchange_rates(
        self: "ClientProtocol",
    ) -> list[ExchangeRate]:
        """
        getExchangeRates method.

        Use this method to get exchange rates of supported currencies.
        Requires no parameters.
        Returns array of :class:`aiosend.types.ExchangeRate`.

        Source: https://help.send.tg/en/articles/10279948-crypto-pay-api#h_bc0e2dee1c

        :return: List of :class:`aiosend.types.ExchangeRate` objects.
        """
        return await self(self.GetExchangeRates(**locals()))
