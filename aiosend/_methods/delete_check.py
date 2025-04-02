from typing import TYPE_CHECKING

from .base import CryptoPayMethod

if TYPE_CHECKING:
    import aiosend


class DeleteCheck:
    """deleteCheck method."""

    class DeleteCheckMethod(CryptoPayMethod[bool]):
        __return_type__ = bool
        __method__ = "deleteCheck"

        check_id: int

    async def delete_check(
        self: "aiosend.CryptoPay",
        check_id: int,
    ) -> bool:
        """
        deleteCheck method.

        Use this method to delete checks created by your app.
        Returns :code:`True` on success.

        Source: https://help.crypt.bot/crypto-pay-api#deleteCheck

        :param check_id: Check ID to be deleted.
        :return: :code:`True` on success.
        """
        return await self(self.DeleteCheckMethod(**locals()))
