=======
Webhook
=======

.. tip::
    To use webhooks you need to enable them in the `@CryptoBot <https://send.t.me>`_ settings as follows:

    🏝 Crypto Pay -> My Apps -> YOUR APP -> Webhooks -> 🌕 Enable webhooks.

.. automethod:: aiosend.CryptoPay.webhook

Usage example with `aiohttp web server <https://docs.aiohttp.org/en/stable/web_quickstart.html>`_
-------------------------------------------------------------------------------------------------
.. literalinclude:: ../../examples/webhook_aiohttp.py

Usage example with `fastapi web server <https://fastapi.tiangolo.com/tutorial/first-steps/>`_
---------------------------------------------------------------------------------------------
.. tip::
    In order to use aiosend with fastapi you need to install extra package

.. code-block:: bash

    pip install aiosend[fastapi]

.. literalinclude:: ../../examples/webhook_fastapi.py

Usage example with `flask web server <https://flask.palletsprojects.com/en/3.0.x/quickstart/#quickstart>`_
----------------------------------------------------------------------------------------------------------
.. tip::
    In order to use aiosend with flask you need to install extra package

.. code-block:: bash

    pip install aiosend[flask]

.. literalinclude:: ../../examples/webhook_flask.py

**aiosend** uses `aiohttp <https://docs.aiohttp.org/en/stable/index.html>`_ as web server by default.
You can implement your own webhook manager by inheriting :class:`aiosend.webhook.WebhookManager`
and overriding :attr:`aiosend.webhook.WebhookManager.register_handler`.

.. autoclass:: aiosend.webhook.WebhookManager
    :members:

.. autoclass:: aiosend.webhook.AiohttpManager
    :show-inheritance:
    :members:

.. autoclass:: aiosend.webhook.FastAPIManager
    :show-inheritance:
    :members:

.. autoclass:: aiosend.webhook.FlaskManager
    :show-inheritance:
    :members: