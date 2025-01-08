import asyncio

from aiohttp.web import Application, _run_app

from aiosend import CryptoPay
from aiosend.types import Invoice

cp = CryptoPay("TOKEN")
app = Application()


@cp.webhook_handler(app, "/handler")
async def handler(invoice: Invoice) -> None:
    print(f"Received {invoice.amount} {invoice.asset}")


async def main() -> None:
    invoice = await cp.create_invoice(1, "USDT")
    print("invoice link:", invoice.bot_invoice_url)
    await _run_app(app)


if __name__ == "__main__":
    asyncio.run(main())
