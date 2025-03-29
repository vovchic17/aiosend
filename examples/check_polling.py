import asyncio

from aiosend import CryptoPay
from aiosend.types import Check

cp = CryptoPay("TOKEN")


@cp.check_polling()
async def check_handler(check: Check, payload: str) -> None:
    print(f"Received", check.amount, check.asset, payload)


@cp.expired_check_polling()
async def expired_check_handler(check: Check, payload: str) -> None:
    print(f"Expired check", check.check_id, payload)


async def main() -> None:
    check = await cp.create_check(1, "USDT")
    print("check link:", check.check_id)
    check.poll(payload="payload")
    await cp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
