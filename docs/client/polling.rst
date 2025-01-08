=======
Polling
=======

Polling is a method of receiving updates by periodically sending requests.
Once :attr:`invoice status <aiosend.types.Invoice.status>` is changed to
:attr:`PAID <aiosend.enums.InvoiceStatus.PAID>`,
:attr:`polling manager <aiosend.polling.PollingManager>` will call the
:attr:`polling_handler <aiosend.CryptoPay.polling_handler>`.
Polling uses the :attr:`/getInvoices <aiosend.CryptoPay.get_invoices>` method.

.. attention::
    :attr:`Polling manager <aiosend.polling.PollingManager>` has
    :attr:`configuration <aiosend.polling.PollingConfig>`
    that defines the :attr:`delay <aiosend.polling.PollingConfig.delay>` (between requests)
    and :attr:`timeout <aiosend.polling.PollingConfig.timeout>`
    for each invoice in the awaiting queue.
    After the timeout polling manager will stop polling that invoice
    and call the :attr:`expired_handler <aiosend.CryptoPay.expired_handler>`
    if it is declared.

    **Default is 2 seconds delay and 300 seconds (5 min) timeout**.

    :ref:`You can change the polling configuration. <PC>`

.. automethod:: aiosend.CryptoPay.polling_handler
.. automethod:: aiosend.CryptoPay.expired_handler

Usage example
-------------
.. literalinclude:: ../../examples/polling.py

.. autoclass:: aiosend.polling.PollingConfig
    :members:

.. _PC:

Polling configuration
---------------------
You can configure your own polling configuration.

.. literalinclude:: ../../examples/polling_config.py

.. autoclass:: aiosend.polling.PollingManager
    :members: