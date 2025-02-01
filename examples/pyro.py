from pyrogram import Client, filters
from pyrogram.types import Message

from aiosend import CryptoPay
from aiosend.types import Invoice

app = Client("my_account")
cp = CryptoPay("TOKEN")


@app.on_message(filters.private)
async def get_invoice(client: Client, message: Message) -> None:
    invoice = await cp.create_invoice(1, "USDT")
    await message.reply_text(
        f"pay: {invoice.mini_app_invoice_url}",
    )
    invoice.poll(message=message)


@cp.invoice_polling()
async def handle_payment(
    invoice: Invoice,
    message: Message,
) -> None:
    await message.reply_text(
        f"payment received: {invoice.amount} {invoice.asset}",
    )


cp.start_polling(app.start)
