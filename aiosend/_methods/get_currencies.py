from typing import TYPE_CHECKING

from aiosend.types import Currency

from .base import CryptoPayMethod

if TYPE_CHECKING:
    from aiosend._typing import ClientProtocol


class GetCurrencies:
    """getCurrencies method."""

    class GetCurrenciesMethod(CryptoPayMethod[list[Currency]]):
        __return_type__ = list[Currency]
        __method__ = "getCurrencies"

    async def get_currencies(
        self: "ClientProtocol",
    ) -> list[Currency]:
        """
        getCurrencies method.

        Use this method to get a list of supported currencies.
        Requires no parameters.
        Returns a list of fiat and cryptocurrency alphabetic codes.

        Source: https://help.send.tg/en/articles/10279948-crypto-pay-api#h_f5cd57dd47

        :return: List of :class:`aiosend.types.Currency` objects.
        """
        return await self(self.GetCurrenciesMethod(**locals()))
