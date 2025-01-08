from typing import TYPE_CHECKING

from aiosend.enums import CheckStatus

if TYPE_CHECKING:
    import aiosend


class DeleteAllChecks:
    """Delete all checks."""

    async def delete_all_checks(
        self: "aiosend.CryptoPay",
    ) -> None:
        """
        Delete all checks.

        Wrapper for :class:`aiosend.CryptoPay.get_checks`
        and :class:`aiosend.CryptoPay.delete_check`

        Use this method to delete all existing
        checks created by your app.

        :return:
        """
        checks = await self.get_checks(status=CheckStatus.ACTIVE)
        for check in checks:
            await check.delete()
