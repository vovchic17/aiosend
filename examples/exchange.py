import asyncio
from aiosend import CryptoPay


async def main() -> None:
    cp = CryptoPay(token="TOKEN")

    print(await cp.exchange(10, "USDT", "USD"))  # 9.998635


if __name__ == "__main__":
    asyncio.run(main())
