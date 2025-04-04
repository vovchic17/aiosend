from typing import TYPE_CHECKING

from aiosend.types import ExchangeRate

from .base import CryptoPayMethod

if TYPE_CHECKING:
    import aiosend


class GetExchangeRates:
    """getExchangeRates method."""

    class GetExchangeRates(CryptoPayMethod[list[ExchangeRate]]):
        __return_type__ = list[ExchangeRate]
        __method__ = "getExchangeRates"

    async def get_exchange_rates(
        self: "aiosend.CryptoPay",
    ) -> list[ExchangeRate]:
        """
        getExchangeRates method.

        Use this method to get exchange rates of supported currencies.
        Requires no parameters.
        Returns array of :class:`aiosend.types.ExchangeRate`.

        Source: https://help.crypt.bot/crypto-pay-api#getExchangeRates

        :return: List of :class:`aiosend.types.ExchangeRate` objects.
        """
        return await self(self.GetExchangeRates(**locals()))
