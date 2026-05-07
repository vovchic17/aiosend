import asyncio

import django
from django.conf import settings


settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    SECRET_KEY="django-insecure-aiosend-example",
)
django.setup()

from aiosend import CryptoPay, TESTNET
from aiosend.types import Invoice
from aiosend.webhook import DjangoManager

urlpatterns = []
cp = CryptoPay(
    "TOKEN",
    webhook_manager=DjangoManager(urlpatterns, "handler"),
)

@cp.invoice_paid()
async def handler(invoice: Invoice) -> None:
    print(f"Received {invoice.amount} {invoice.asset}")

async def main() -> None:
    invoice = await cp.create_invoice(1, "USDT")
    print("invoice link:", invoice.bot_invoice_url)

if __name__ == "__main__":
    import os
    from django.core.management import execute_from_command_line
    if os.environ.get("RUN_MAIN") != "true":
        asyncio.run(main())
    execute_from_command_line(["manage.py", "runserver"])
