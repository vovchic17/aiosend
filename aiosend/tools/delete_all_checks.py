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

        Wrapper for :meth:`aiosend.CryptoPay.get_checks`
        and :meth:`aiosend.CryptoPay.delete_check`

        Use this method to delete all existing
        checks created by your app.

        :return:
        """
        checks = await self.get_checks(status=CheckStatus.ACTIVE, count=1000)
        for check in checks:
            await check.delete()
