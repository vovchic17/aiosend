from typing import TYPE_CHECKING

from aiosend.exceptions import CryptoPayError

if TYPE_CHECKING:
    import aiosend
    from aiosend.enums import Asset, Fiat


class Exchange:
    """Exchange."""

    async def exchange(
        self: "aiosend.CryptoPay",
        amount: float,
        source: "Asset | Fiat | str",
        target: "Asset | Fiat | str",
    ) -> float:
        """
        Exchange currency.

        Wrapper for :meth:`aiosend.CryptoPay.get_exchange_rates`.

        Use this method to get the equivalent amount in
        the target currency for the source currency.

        :return: :class:`float` on success.
        :raise: :class:`aiosend.exceptions.CryptoPayError` if there is no such exchange rate.
        """
        ex_rates = await self.get_exchange_rates()
        for ex_rate in ex_rates:
            if ex_rate.source == source and ex_rate.target == target:
                return ex_rate.rate * amount
            if ex_rate.source == target and ex_rate.target == source:
                return amount / ex_rate.rate

        msg = f"Exchange rate for {source} => {target} not found"
        raise CryptoPayError(msg)
