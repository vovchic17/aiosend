from typing import TYPE_CHECKING

from aiosend.types import App

from .base import CryptoPayMethod

if TYPE_CHECKING:
    import aiosend


class GetMe:
    """getMe method."""

    class GetMeMethod(CryptoPayMethod[App]):
        __return_type__ = App
        __method__ = "getMe"

    async def get_me(self: "aiosend.CryptoPay") -> App:
        """
        getMe method.

        Use this method to test your app's authentication token.
        Requires no parameters.
        On success, returns basic information about an app.

        Source: https://help.crypt.bot/crypto-pay-api#getMe

        :return: :class:`aiosend.types.App` object.
        """
        return await self(self.GetMeMethod(**locals()))
