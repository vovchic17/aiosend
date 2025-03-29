import asyncio

from aiosend import CryptoPay
from aiosend.types import Invoice

cp = CryptoPay("TOKEN", var1="value1")  # injection
cp["var2"] = "value2"  # injection


async def main() -> None:
    invoice = await cp.create_invoice(1, "USDT")
    print("invoice link:", invoice.bot_invoice_url)
    invoice.poll(var3="value3")  # injection
    await cp.start_polling()


@cp.invoice_polling()
async def payment_handler(
    invoice: Invoice,
    var1: str,  # this one is from constructor
    var2: str,  # this one is from key assignment
    var3: str,  # this one is from poll method kwargs
) -> None:
    print(f"Invoice #{invoice.invoice_id} {var1=} {var2=} {var3=}")


if __name__ == "__main__":
    asyncio.run(main())
