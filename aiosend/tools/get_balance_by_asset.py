from typing import TYPE_CHECKING

from aiosend.exceptions import CryptoPayError

if TYPE_CHECKING:
    import aiosend
    from aiosend.enums import Asset
    from aiosend.types import Balance


class GetBalanceByAsset:
    """Get balance by Asset."""

    async def get_balance_by_asset(
        self: "aiosend.CryptoPay",
        asset: "Asset | str",
    ) -> "Balance":
        """
        Get the balance of a specific asset.

        Wrapper for :meth:`aiosend.CryptoPay.get_balance`.

        Use this method to get the balance of a specific asset.

        :return: :class:`aiosend.types.Balance` on success.
        :raise: :class:`aiosend.exceptions.CryptoPayError` if there is no such asset.
        """
        balances = await self.get_balance()
        for balance in balances:
            if balance.currency_code == asset:
                return balance
        msg = f"Balance for {asset} not found"
        raise CryptoPayError(msg)
