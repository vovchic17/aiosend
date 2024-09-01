from telebot import TeleBot
from telebot.types import Message

from cryptopay import CryptoPay
from cryptopay.types import Invoice

bot = TeleBot("TOKEN")
cp = CryptoPay("TOKEN")


@bot.message_handler()
def get_invoice(message: Message) -> None:
    invoice = cp.create_invoice(1, "USDT")
    bot.send_message(
        message.from_user.id,
        f"pay: {invoice.mini_app_invoice_url}",
    )
    invoice.await_payment(user_id=message.from_user.id)


@cp.polling_handler()
def handle_payment(
    invoice: Invoice,
    user_id: int,
) -> None:
    bot.send_message(
        user_id,
        f"payment received: {invoice.amount} {invoice.asset}",
    )


if __name__ == "__main__":
    cp.run_polling(bot.infinity_polling)
