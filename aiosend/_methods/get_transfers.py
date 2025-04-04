from typing import TYPE_CHECKING

from pydantic import Field

from aiosend.enums import Asset
from aiosend.types import SerList, Transfer

from .base import CryptoPayMethod

if TYPE_CHECKING:
    import aiosend


class GetTransfers:
    """getTransfers method."""

    class GetTransfersMethod(CryptoPayMethod[list[Transfer]]):
        __return_type__ = list[Transfer]
        __method__ = "getTransfers"

        asset: str | None
        transfer_ids: SerList[int] | None
        spend_id: str | None
        offset: int | None
        count: int | None = Field(None, ge=1, le=1000)

    async def get_transfers(
        self: "aiosend.CryptoPay",
        asset: Asset | None = None,
        transfer_ids: list[int] | None = None,
        spend_id: str | None = None,
        offset: int | None = None,
        count: int | None = None,
    ) -> list[Transfer]:
        """
        getTransfers method.

        Use this method to get transfers created by your app.
        On success, returns array of :class:`aiosend.types.Transfer`.

        Source: https://help.crypt.bot/crypto-pay-api#getTransfers

        :param asset: *Optional*. Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet). Defaults to all currencies.
        :param transfer_ids: *Optional*. List of transfer IDs separated by comma.
        :param spend_id: *Optional*. Unique UTF-8 transfer string.
        :param offset: *Optional*. Offset needed to return a specific subset of transfers. Defaults to 0.
        :param count: *Optional*. Number of transfers to be returned. Values between 1-1000 are accepted. Defaults to 100.
        :return: List of :class:`aiosend.types.Transfer` objects.
        """
        return await self(self.GetTransfersMethod(**locals()))
