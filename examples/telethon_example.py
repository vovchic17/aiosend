from telethon import TelegramClient, events
from telethon.events.newmessage import NewMessage

from aiosend import CryptoPay
from aiosend.types import Invoice

api_id = 12345678
api_hash = "API HASH"

cp = CryptoPay("TOKEN")
client = TelegramClient("anon", api_id, api_hash)


@client.on(events.NewMessage(func=lambda e: e.is_private))
async def get_invoice(message: NewMessage.Event) -> None:
    invoice = await cp.create_invoice(1, "USDT")
    await client.send_message(
        message.chat_id,
        f"pay: {invoice.mini_app_invoice_url}",
    )
    invoice.poll(chat_id=message.chat_id)


@cp.invoice_polling()
async def handle_payment(
    invoice: Invoice,
    chat_id: int,
) -> None:
    await client.send_message(
        chat_id,
        f"payment received: {invoice.amount} {invoice.asset}",
    )


client.start()
cp.start_polling()
