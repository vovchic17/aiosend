.. raw:: html

   <h1 class="BB">aiosend</h1>

Introduction
------------

**aiosend** is a synchronous & asynchronous `Crypto Pay API <https://help.crypt.bot/crypto-pay-api>`_ client.

.. seealso::
   |telegram| **aiosend** has `community chat on Telegram <https://aiosend.t.me>`_

.. |telegram| image:: https://raw.githubusercontent.com/vovchic17/static/2cae16d0c4289f9556dacc13322dd4a2fcca214f/src/telegram_logo.svg
   :width: 24px
   :alt: python

Features
--------
* provides :doc:`invoice polling handler <client/invoice_polling>` and :doc:`check polling handler <client/check_polling>`
* provides :doc:`webhook handler <client/webhook>`
* provides :doc:`additional function shortcuts <client/tools>`
* supports sync and async usage


Quick start
-----------

.. literalinclude:: ../examples/quick_start.py


Synchronous usage
-----------------

.. literalinclude:: ../examples/sync.py

Contents
--------
.. toctree::
   :maxdepth: 2

   install
   client/index
   types
   enums
   api/index
   errors
   examples/index
   integration_examples/index
