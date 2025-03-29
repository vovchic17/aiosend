import asyncio

from aiosend import CryptoPay


async def main() -> None:
    cp = CryptoPay(token="TOKEN")
    app = await cp.get_me()
    print(app.name)  # Your App's Name


if __name__ == "__main__":
    asyncio.run(main())
