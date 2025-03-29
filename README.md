<p align="center"> <!-- markdownlint-disable MD033 MD041 MD045 MD013-->
  <img src="https://raw.githubusercontent.com/vovchic17/static/refs/heads/main/src/aiosend.png" align="center"/>
  <h1 align="center">aiosend</h1>
</p>

[![Python](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/vovchic17/static/main/src/badges/python310_313.json)](https://www.python.org/)
[![Crypto Pay API](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/vovchic17/static/refs/heads/main/src/badges/cryptopayapi.json)](https://help.crypt.bot/crypto-pay-api)
[![Documentation Status](https://readthedocs.org/projects/aiosend/badge/?version=latest)](https://aiosend.readthedocs.io/en/latest/?badge=latest)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![Aiohttp](https://img.shields.io/badge/aiohttp-v3-2c5bb4?logo=aiohttp)](https://docs.aiohttp.org/en/stable/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Code linter: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)
[![Checked with mypy](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/vovchic17/static/main/src/badges/mypy.json)](https://mypy-lang.org/)

**aiosend** is a syncronous & asynchronous [Crypto Pay API](https://help.crypt.bot/crypto-pay-api) client.

> ## [Official documentation](https://aiosend.readthedocs.io/en/latest/)
>
> ## [<img src="https://raw.githubusercontent.com/vovchic17/static/refs/heads/main/src/telegram_logo.svg" width="30" align="top">  Telegram chat](https://aiosend.t.me/)

## Quick start

```python
import asyncio
from aiosend import CryptoPay


async def main():
    cp = CryptoPay(token="TOKEN")
    app = await cp.get_me()
    print(app.name)  # Your App's Name


if __name__ == "__main__":
    asyncio.run(main())
```

## aiogram 3.x integration example

```python
import asyncio
from aiogram import Bot, Dispatcher
from aiosend import CryptoPay

cp = CryptoPay("TOKEN")
bot = Bot("TOKEN")
dp = Dispatcher()


@dp.message()
async def get_invoice(message):
    invoice = await cp.create_invoice(1, "USDT")
    await message.answer(f"pay: {invoice.bot_invoice_url}")
    invoice.poll(message=message)


@cp.invoice_polling()
async def handle_payment(invoice, message):
    await message.answer(f"invoice #{invoice.invoice_id} has been paid")


async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        cp.start_polling(),
    )


if __name__ == "__main__":
    asyncio.run(main())
```
