===============
Invoice polling
===============

Polling is a method of receiving updates by periodically sending requests.
Once :attr:`invoice status <aiosend.types.Invoice.status>` is changed to
:attr:`PAID <aiosend.enums.InvoiceStatus.PAID>`,
:class:`polling manager <aiosend.polling.PollingManager>` will call the
:meth:`invoice_paid <aiosend.CryptoPay.invoice_paid>` handler.
Invoice polling uses the :meth:`/getInvoices <aiosend.CryptoPay.get_invoices>` method.

.. attention::
    :class:`Polling manager <aiosend.polling.PollingManager>` has
    :class:`configuration <aiosend.polling.PollingConfig>`
    that defines the :attr:`delay <aiosend.polling.PollingConfig.delay>` (between requests)
    and :attr:`timeout <aiosend.polling.PollingConfig.timeout>`
    for each invoice in the awaiting queue.
    After the timeout polling manager will stop polling that invoice
    and call the :meth:`invoice_expired <aiosend.CryptoPay.invoice_expired>` handler
    if it is declared.

    **Default is 2 seconds delay and 300 seconds (5 min) timeout**.

    :doc:`You can change the polling configuration. <polling_config>`

Usage example
-------------
.. literalinclude:: ../../examples/invoice_polling.py