import asyncio

from aiosend import CryptoPay


async def main() -> None:
    cp = CryptoPay("TOKEN")

    invoice = await cp.create_invoice(1, "USDT")

    print(invoice.status)  # active
    await asyncio.sleep(10)  # payment
    await invoice.update()
    print(invoice.status)  # paid

    print(invoice.qr)  # qr code link

    await invoice.delete()  # delete the invoice


if __name__ == "__main__":
    asyncio.run(main())
