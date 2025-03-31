=======
Filters
=======

**Filters** are needed for routing updates to the specific handler.
:class:`WebhookManager <aiosend.webhook.WebhookManager>` and
:class:`PollingManager <aiosend.polling.PollingManager>` will
check if the handler is suitable for the update.
Once a handler with a suitable set of filters is found,
searching of handler will be stopped.

Filters can be:
---------------
* asynchronous function
* synchronous function
* lambda function
* instance of `MagicFilter <https://docs.aiogram.dev/en/latest/dispatcher/filters/magic_filters.html#magic-filters>`_

Usage example
-------------
For example, you can create a couple
of invoices and poll them like that

.. code-block:: python

    import asyncio
    from aiosend import CryptoPay
    from aiosend.types import Invoice

    cp = CryptoPay("TOKEN")

    async def main() -> None:
        invoice1 = await cp.create_invoice(
            1, "USDT", payload="product1",
        )
        invoice2 = await cp.create_invoice(
            1, "USDT", payload="product2",
        )
        print(invoice.bot_invoice_url)
        invoice1.poll()
        invoice2.poll()
        await cp.start_polling()

Magic filter
------------

.. code-block:: python

    from magic_filter import F

    @cp.invoice_polling(F.payload == "product1")
    async def handler1(invoice: Invoice) -> None:
        print(f"paid {invoice.amount} {invoice.asset} for product1")


    @cp.invoice_polling(F.payload == "product2")
    async def handler2(invoice: Invoice) -> None:
        print(f"paid {invoice.amount} {invoice.asset} for product2")

Function filter
---------------

You can use either :code:`def`, :code:`async def` or :code:`lambda`

.. code-block:: python

    def filter1(invoice: Invoice) -> bool:
        return invoice.payload == "product1"

    async def filter2(invoice: Invoice) -> bool:
        return invoice.payload == "product2" 

    @cp.invoice_polling(filter1)
    async def handler1(invoice: Invoice) -> None:
        print(f"paid {invoice.amount} {invoice.asset} for product1")

    @cp.invoice_polling(filter2, lambda inv: inv.amount == 1)
    async def handler2(invoice: Invoice) -> None:
        print(f"paid {invoice.amount} {invoice.asset} for product2")

Get filter result as handler argument
-------------------------------------

You can use `aiogram 3.x magic filter's
<https://docs.aiogram.dev/en/dev-3.x/dispatcher/filters/magic_filters.html#get-filter-result-as-handler-argument>`_
:code:`as_` method to get filter result as handler argument

.. code-block:: python

    from aiogram import F

    @cp.invoice_polling(F.payload.as_("payload"))
    async def handler1(invoice: Invoice, payload: str) -> None:
        print(f"paid #{invoice.invoice_id} paylaod: {payload}")

You can also return context data from function filters like that

.. code-block:: python

    def myfilter(invoice: Invoice) -> bool | dict[str, object]:
        if invoice.payload is None:
            return False
        return {"payload": invoice.payload}
        

    @cp.invoice_polling(myfilter)
    async def handler1(invoice: Invoice, payload: str) -> None:
        print(f"paid #{invoice.invoice_id} paylaod: {payload}")