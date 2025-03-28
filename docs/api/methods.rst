.. _MethodsAnchor:

=======
Methods
=======

`Crypto Pay API <https://help.crypt.bot/crypto-pay-api>`_ methods implementation.

.. automethod:: aiosend.CryptoPay.get_me
.. automethod:: aiosend.CryptoPay.create_invoice
.. automethod:: aiosend.CryptoPay.delete_invoice
.. tip::
    To use /create_check method you need to enable it to the restriction settings in `@CryptoBot <https://send.t.me>`_ as follows:

    🏝 Crypto Pay -> My Apps -> <Your App> -> Security -> Checks -> Enable.
.. automethod:: aiosend.CryptoPay.create_check
.. automethod:: aiosend.CryptoPay.delete_check
.. tip::
    To use /transfer method you need to enable it to the restriction settings in `@CryptoBot <https://send.t.me>`_ as follows:

    🏝 Crypto Pay -> My Apps -> <Your App> -> Security -> Transfers -> Enable.
.. automethod:: aiosend.CryptoPay.transfer
.. automethod:: aiosend.CryptoPay.get_invoices
.. automethod:: aiosend.CryptoPay.get_checks
.. automethod:: aiosend.CryptoPay.get_transfers
.. automethod:: aiosend.CryptoPay.get_balance
.. automethod:: aiosend.CryptoPay.get_exchange_rates
.. automethod:: aiosend.CryptoPay.get_currencies
.. automethod:: aiosend.CryptoPay.get_stats