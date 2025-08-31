=============
Check polling
=============

Polling is a method of receiving updates by periodically sending requests.
Once :attr:`check status <aiosend.types.Check.status>` is changed to
:attr:`ACTIVATED <aiosend.enums.CheckStatus.ACTIVATED>`,
:class:`polling manager <aiosend.polling.PollingManager>` will call the
:meth:`check_activated <aiosend.CryptoPay.check_activated>` handler.
Check polling uses the :meth:`/getChecks <aiosend.CryptoPay.get_checks>` method.

.. attention::
    :class:`Polling manager <aiosend.polling.PollingManager>` has
    :class:`configuration <aiosend.polling.PollingConfig>`
    that defines the :attr:`delay <aiosend.polling.PollingConfig.delay>` (between requests)
    and :attr:`timeout <aiosend.polling.PollingConfig.timeout>`
    for each check in the awaiting queue.
    After the timeout polling manager will stop polling that check
    and call the :meth:`check_expired <aiosend.CryptoPay.check_expired>` handler
    if it is declared.

    **Default is 2 seconds delay and 300 seconds (5 min) timeout**.

    :doc:`You can change the polling configuration. <polling_config>`

Usage example
-------------
.. literalinclude:: ../../examples/check_polling.py