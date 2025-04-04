from typing import TYPE_CHECKING

from aiosend.types import Check

if TYPE_CHECKING:
    import aiosend


class GetCheck:
    """Get check."""

    async def get_check(
        self: "aiosend.CryptoPay",
        check: int | Check,
    ) -> Check | None:
        """
        Get exactly one check or none.

        Wrapper for :meth:`aiosend.CryptoPay.get_checks`

        Use this method to update status of an existing check
        object or to get this object by passing the check id.

        :return: :meth:`aiosend.types.Check` object.
        """
        check_id = check.check_id if isinstance(check, Check) else check

        checks = await self.get_checks(check_ids=[check_id])
        if checks:
            return checks[0]
        return None
