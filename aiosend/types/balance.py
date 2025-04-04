from aiosend.enums import Asset

from .base import CryptoPayObject


class Balance(CryptoPayObject):
    """
    Balance object.

    Source: https://help.crypt.bot/crypto-pay-api#Balance
    """

    currency_code: Asset | str
    """Cryptocurrency alphabetic code. Currently, can be “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet)."""
    available: float
    """Total available amount in float."""
    onhold: float
    """Unavailable amount currently is on hold in float."""

    async def update(self) -> None:
        """
        Shortcut for method :meth:`aiosend.CryptoPay.get_balance`.

        Use this method to update balance object.

        Source: https://help.crypt.bot/crypto-pay-api#getBalance

        :return:
        """
        balance = await self._client.get_balance_by_asset(self.currency_code)
        self.__dict__ = balance.__dict__
