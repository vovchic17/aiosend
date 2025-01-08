import asyncio

from aiosend import CryptoPay


async def main() -> None:
    cp = CryptoPay(token="TOKEN")

    print(await cp.get_balance_by_asset("USDT"))  # 1.2345


if __name__ == "__main__":
    asyncio.run(main())
