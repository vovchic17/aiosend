import asyncio

from aiosend import CryptoPay
from aiosend.polling import PollingConfig
from aiosend.types import Invoice

cp = CryptoPay(
    "TOKEN",
    polling_config=PollingConfig(
        timeout=600,  # 10 minutes
        delay=3,  # request every 3 seconds
    ),
)


@cp.invoice_polling()
async def handler(invoice: Invoice) -> None:
    print(f"Received", invoice.amount, invoice.asset)


# called after timeout (600s) or when invoice status is "expired"
@cp.expired_invoice_polling()
async def expired_invoice_handler(invoice: Invoice, payload: str) -> None:
    print(f"Expired invoice", invoice.invoice_id, payload)


async def main() -> None:
    invoice = await cp.create_invoice(1, "USDT")
    print("invoice link:", invoice.bot_invoice_url)
    invoice.poll()
    await cp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
