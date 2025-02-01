import asyncio

from flask import Flask

from aiosend import CryptoPay
from aiosend.webhook import FlaskManager
from aiosend.types import Invoice

app = Flask(__name__)
cp = CryptoPay(
    "TOKEN",
    webhook_manager=FlaskManager(app, "/handler"),
)


@cp.webhook()
async def handler(invoice: Invoice) -> None:
    print(f"Received {invoice.amount} {invoice.asset}")


async def main() -> None:
    invoice = await cp.create_invoice(1, "USDT")
    print("invoice link:", invoice.bot_invoice_url)


if __name__ == "__main__":
    asyncio.run(main())
    app.run()
