Routers
-------

Router is an object for routing updates. There are two types of routers:
:class:`PollingRouter <aiosend.polling.PollingRouter>` and
:class:`WebhookRouter <aiosend.webhook.WebhookRouter>`.
:class:`CryptoPay <aiosend.CryptoPay>` is the root router for both of them.
One router can include another router, but in the end,
the parent router must be included in the root router via
:meth:`include_router <aiosend._events.BaseRouter.include_router>` or
:meth:`include_routers <aiosend._events.BaseRouter.include_routers>` methods.

Usage example

.. literalinclude:: ../../examples/router.py

.. autoclass:: aiosend._events.BaseRouter
    :members:

.. autoclass:: aiosend.polling.PollingRouter
    :show-inheritance:

.. autoclass:: aiosend.webhook.WebhookRouter
    :show-inheritance:

Event observers
---------------
Event observer is an object that stores event handlers.
You can attach a new event handler to event observer using a 
:code:`@router.<event type>(...)` decorator or a :code:`router.<event type>.register(...)` method.

.. autoclass:: aiosend._events.EventObserver
    :members:

Polling Router
==============

Available observers for :class:`PollingRouter <aiosend.polling.PollingRouter>` are listed here.

Paid invoice
~~~~~~~~~~~~

.. code-block:: python

    @router.invoice_paid()
    def invoice_paid(invoice: Invoice) -> None: ...

Expired invoice
~~~~~~~~~~~~~~~

.. code-block:: python

    @router.invoice_expired()
    def invoice_expired(invoice: Invoice) -> None: ...

Activated check
~~~~~~~~~~~~~~~

.. code-block:: python

    @router.check_activated()
    def check_activated(check: Check) -> None: ...

Expired check
~~~~~~~~~~~~~

.. code-block:: python

    @router.check_expired()
    def check_expired(check: Check) -> None: ...

Webhook Router
==============

Available observers for :class:`WebhookRouter <aiosend.webhook.WebhookRouter>` are listed here.

Paid invoice
~~~~~~~~~~~~

.. code-block:: python

    @router.invoice_paid()
    def invoice_paid(invoice: Invoice) -> None: ...