from datetime import datetime
from typing import cast

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
        Shortcut for method :meth:`aiosend.CryptoPay.delete_check`.

        Use this method to delete check created by your app.
        Returns :code:`True` on success.

        Source: https://help.crypt.bot/crypto-pay-api#deleteCheck

        :return: :code:`True` on success.
        """
        return await self._client.delete_check(self.check_id)

    async def update(self) -> None:
        """
        Shortcut for method :meth:`aiosend.CryptoPay.get_checks`.

        Use this method to update check object.

        Source: https://help.crypt.bot/crypto-pay-api#getChecks

        :return:
        """
        check = cast("Check", await self._client.get_check(self))
        self.__dict__ = check.__dict__

    def poll(self, **kwargs: object) -> None:
        """
        Send the check to the polling manager.

        Use this method to check the status of
        the check until the timeout expires.

        :param kwargs: additional payload for the handler.

        :return:
        """
        self._client._poll_check(self, kwargs)  # noqa: SLF001

    @property
    def qr(self) -> str:
        """
        Get check qr code.

        :return: check qr code url.
        """
        return self._client.session.network.get_qr(self.bot_check_url)

    async def get_image(self, fiat: LiteralFiat | str) -> str:
        """
        Get check preview image.

        :return: check image url.
        """
        fiat_amount = await self._client.exchange(
            self.amount,
            self.asset,
            fiat,
        )
        return self._client.session.network.get_check_image(
            asset=self.asset,
            asset_amount=self.amount,
            fiat=fiat,
            fiat_amount=fiat_amount,
            main="asset",
        )
