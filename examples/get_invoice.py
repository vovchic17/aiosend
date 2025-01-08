import asyncio

from aiosend import CryptoPay


async def main() -> None:
    cp = CryptoPay(token="TOKEN")

    invoice = await cp.create_invoice(1, "TON")
    print(invoice.status)  # active
    await asyncio.sleep(10)  # payment
    new_invoice = await cp.get_invoice(invoice)
    print(new_invoice.status)  # paid


if __name__ == "__main__":
    asyncio.run(main())
