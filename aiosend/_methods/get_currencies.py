from typing import TYPE_CHECKING

from aiosend.types import Currency

from .base import CryptoPayMethod

if TYPE_CHECKING:
    import aiosend


class GetCurrencies:
    """getCurrencies method."""

    class GetCurrenciesMethod(CryptoPayMethod[list[Currency]]):
        __return_type__ = list[Currency]
        __method__ = "getCurrencies"

    async def get_currencies(
        self: "aiosend.CryptoPay",
    ) -> list[Currency]:
        """
        getCurrencies method.

        Use this method to get a list of supported currencies.
        Requires no parameters.
        Returns a list of fiat and cryptocurrency alphabetic codes.

        Source: https://help.crypt.bot/crypto-pay-api#getCurrencies

        :return: List of :class:`aiosend.types.Currency` objects.
        """
        return await self(self.GetCurrenciesMethod(**locals()))
