from typing import TYPE_CHECKING

from aiosend.types import Balance

from .base import CryptoPayMethod

if TYPE_CHECKING:
    from aiosend._typing import ClientProtocol


class GetBalance:
    """getBalance method."""

    class GetBalanceMethod(CryptoPayMethod[list[Balance]]):
        __return_type__ = list[Balance]
        __method__ = "getBalance"

    async def get_balance(self: "ClientProtocol") -> list[Balance]:
        """
        getBalance method.

        Use this method to get balances of your app.
        Requires no parameters.
        Returns array of :class:`aiosend.types.Balance`.

        Source: https://help.send.tg/en/articles/10279948-crypto-pay-api#h_86005049de

        :return: List of :class:`aiosend.types.Balance` objects.
        """
        return await self(self.GetBalanceMethod(**locals()))
