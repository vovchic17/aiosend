from aiosend import CryptoPay, TESTNET
from aiosend.types import Invoice
from aiosend.webhook import DjangoManager

urlpatterns = []

cp = CryptoPay(
    "45104:AA83msd5J5wTi7nH8MjQtoCcsf8k2Z4Bsyh",
    network=TESTNET,
    webhook_manager=DjangoManager(urlpatterns, "handler"),
)


@cp.invoice_paid()
async def handler(invoice: Invoice) -> None:
    print(f"Received {invoice.amount} {invoice.asset}")


async def main() -> None:
    invoice = await cp.create_invoice(amount=1, asset="USDT")
    print("invoice link:", invoice.bot_invoice_url)
