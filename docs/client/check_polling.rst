=============
Check polling
=============

Polling is a method of receiving updates by periodically sending requests.
Once :attr:`check status <aiosend.types.Check.status>` is changed to
:attr:`ACTIVATED <aiosend.enums.InvoiceStatus.ACTIVATED>`,
:attr:`polling manager <aiosend.polling.PollingManager>` will call the
:attr:`check_polling <aiosend.CryptoPay.check_polling>` handler.
Check polling uses the :attr:`/getChecks <aiosend.CryptoPay.get_invoices>` method.

.. attention::
    :attr:`Polling manager <aiosend.polling.PollingManager>` has
    :attr:`configuration <aiosend.polling.PollingConfig>`
    that defines the :attr:`delay <aiosend.polling.PollingConfig.delay>` (between requests)
    and :attr:`timeout <aiosend.polling.PollingConfig.timeout>`
    for each check in the awaiting queue.
    After the timeout polling manager will stop polling that check
    and call the :attr:`expired_check_polling <aiosend.CryptoPay.expired_check_polling>` handler
    if it is declared.

    **Default is 2 seconds delay and 300 seconds (5 min) timeout**.

    :ref:`You can change the polling configuration. <PollingConfigAnchor>`

.. automethod:: aiosend.CryptoPay.check_polling
.. automethod:: aiosend.CryptoPay.expired_check_polling

Usage example
-------------
.. literalinclude:: ../../examples/check_polling.py