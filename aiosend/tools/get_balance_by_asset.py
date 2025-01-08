from typing import TYPE_CHECKING

from aiosend.exceptions import CryptoPayError

if TYPE_CHECKING:
    import aiosend
    from aiosend.enums import Asset


class GetBalanceByAsset:
    """Get balance by Asset."""

    async def get_balance_by_asset(
        self: "aiosend.CryptoPay",
        asset: "Asset | str",
    ) -> float:
        """
        Get the balance of a specific asset.

        Wrapper for :class:`aiosend.CryptoPay.get_balance`.

        Use this method to get total avaliable
        amount in float of a specific asset.

        :return: :class:`float` on success.
        :raise: :class:`CryptoPayError` if there is no such asset.
        """
        balances = await self.get_balance()
        for balance in balances:
            if balance.currency_code == asset:
                return balance.available
        msg = f"Balance for {asset} not found"
        raise CryptoPayError(msg)
