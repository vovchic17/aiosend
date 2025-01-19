import asyncio

from aiosend import CryptoPay


async def main() -> None:
    cp = CryptoPay("TOKEN")

    check = await cp.create_check(1, "USDT")

    # invoice preview image with fiat conversion
    print(await check.get_image("USD"))

    print(check.qr)  # check qr code link

    await check.delete()  # delete check


if __name__ == "__main__":
    asyncio.run(main())
