from datetime import datetime

from aiosend.enums import Asset, CheckStatus, LiteralFiat

from .base import CryptoPayObject


class Check(CryptoPayObject):
    """
    Check object.

    Source: https://help.crypt.bot/crypto-pay-api#Check
    """

    check_id: int
    """Unique ID for this check."""
    hash: str
    """Hash of the check."""
    asset: Asset | str
    """Cryptocurrency alphabetic code. Currently, can be “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet)."""
    amount: float
    """Amount of the check in float."""
    bot_check_url: str
    """URL should be provided to the user to activate the check."""
    status: CheckStatus | str
    """Status of the check, can be “active” or “activated”."""
    created_at: datetime
    """Date the check was created in ISO 8601 format."""
    activated_at: datetime | None = None
    """Date the check was activated in ISO 8601 format."""

    async def delete(self) -> bool:
        """
        Shortcut for method :class:`aiosend.CryptoPay.delete_check`.

        Use this method to delete check created by your app.
        Returns :code:`True` on success.

        Source: https://help.crypt.bot/crypto-pay-api#deleteCheck

        :return: :code:`True` on success.
        """
        return await self._client.delete_check(self.check_id)

    @property
    def qr(self) -> str:
        """
        Get check qr code.

        :return: check qr code.
        """
        return self._client.session.api_server.get_qr(self.bot_check_url)

    async def get_image(self, fiat: LiteralFiat | str) -> str:
        """
        Get check preview image.

        :return: check image.
        """
        fiat_amount = await self._client.exchange(
            self.amount,
            self.asset,
            fiat,
        )
        return self._client.session.api_server.get_image(
            asset=self.asset,
            asset_amount=self.amount,
            fiat=fiat,
            fiat_amount=fiat_amount,
            main="asset",
        )