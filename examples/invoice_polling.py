import asyncio

from aiosend import CryptoPay
from aiosend.types import Invoice

cp = CryptoPay("TOKEN")


@cp.invoice_polling()
async def payment_handler(invoice: Invoice, payload: str) -> None:
    print(f"Received", invoice.amount, invoice.asset, payload)


@cp.expired_invoice_polling()
async def expired_invoice_handler(invoice: Invoice, payload: str) -> None:
    print(f"Expired invoice", invoice.invoice_id, payload)


async def main() -> None:
    invoice = await cp.create_invoice(1, "USDT")
    print("invoice link:", invoice.bot_invoice_url)
    invoice.poll(payload="payload")
    await cp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
