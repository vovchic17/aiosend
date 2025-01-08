=========
APIServer
=========

APIServer is a class allows you to build a URL to the API endpoints for specific network.

`Crypto Pay API <https://help.crypt.bot/crypto-pay-api>`_ has two networks:

* .. autoclass:: aiosend.MAINNET

The main network for transactions with real cryptocurrency.

* .. autoclass:: aiosend.TESTNET

The network for testing purposes in which currency has no real value.

Usage example
-------------

You can create an instance of :class:`CryptoPay` client for both nets.

.. literalinclude:: ../../examples/api_server.py

.. automodule:: aiosend.client.api_server
    :members:
