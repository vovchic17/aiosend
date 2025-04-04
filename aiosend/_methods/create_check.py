from typing import TYPE_CHECKING

from aiosend.enums import Asset
from aiosend.types import Check

from .base import CryptoPayMethod

if TYPE_CHECKING:
    import aiosend


class CreateCheck:
    """createCheck method."""

    class CreateCheckMethod(CryptoPayMethod[Check]):
        __return_type__ = Check
        __method__ = "createCheck"

        asset: str
        amount: float
        pin_to_user_id: int | None
        pin_to_username: str | None

    async def create_check(
        self: "aiosend.CryptoPay",
        amount: float,
        asset: Asset,
        pin_to_user_id: int | None = None,
        pin_to_username: str | None = None,
    ) -> Check:
        """
        createCheck method.

        Use this method to create a new check.
        On success, returns an object of the created :class:`aiosend.types.Check`.

        Source: https://help.crypt.bot/crypto-pay-api#createCheck

        :param amount: Amount of the check in float. For example: `125.50`
        :param asset: Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet).
        :param pin_to_user_id: *Optional*. ID of the user who will be able to activate the check.
        :param pin_to_username: *Optional*. A user with the specified username will be able to activate the check.
        :return: :class:`aiosend.types.Check` object
        """
        return await self(self.CreateCheckMethod(**locals()))
