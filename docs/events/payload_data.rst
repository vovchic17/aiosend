============
Payload Data
============

Payload Data is used to generate a structured payload using the pydantic model.

.. autoclass:: aiosend.PayloadData
    :members:
    :exclude-members: model_config

Usage example
-------------

Define a subclass of :class:`PayloadData <aiosend.PayloadData>`
The keyword :code:`prefix` is required to specify the prefix, and the :code:`sep`
argument can be provided to define the separator (default is :).

.. code-block:: python

    class MyData(PayloadData, prefix="md"):
        foo: str
        bar: int

Now you can create an instance of this class, pack it into a string,
and then pass it in the :attr:`Invoice payload <aiosend.types.Invoice.payload>`.

.. code-block:: python

    my_data = MyData(foo="foo", bar=123).pack()
    await cp.create_invoice(1, "USDT", payload=my_data)

To handle an invoice payment event, you need to declare a handler with a PayloadData filter.
You can access an instance of your PayloadData via the handler’s named argument :code:`payload_data`.

.. code-block:: python

    @cp.invoice_paid(MyData.filter())
    async def handler(invoice: Invoice, payload_data: MyData) -> None:
        print(invoice.amount, payload_data.foo)

Also you can filter events by specific rules using
`magic filters from aiogram 3.x <https://docs.aiogram.dev/en/latest/dispatcher/filters/magic_filters.html#magic-filters>`_

.. code-block:: python

    from magic_filter import F # or from aiogram import F

    @cp.invoice_paid(MyData.filter(F.bar == 123))
    async def handler(invoice: Invoice, payload_data: MyData) -> None:
        print(invoice.amount, payload_data.foo)