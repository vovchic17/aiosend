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
* supports both synchronous and asynchronous use
* provides :doc:`invoice polling <events/invoice_polling>` and :doc:`check polling <events/check_polling>`
* provides :doc:`webhook handling <events/webhook>`
* fully typed, has :doc:`literal type hints and warnings <client/hints_warns>`
* uses powerful `magic filters from aiogram 3.x <https://docs.aiogram.dev/en/latest/dispatcher/filters/magic_filters.html#magic-filters>`_
* provides :doc:`dependency injection <client/di>`
* provides :doc:`additional tool methods <client/tools>`
* provides :doc:`shortcut methods for types <client/shortcuts>`

Quick start
-----------

.. literalinclude:: ../examples/quick_start.py

Contents
--------
.. toctree::
   :maxdepth: 1

   install
   api/index
   client/index
   events/index
   integration_examples/index
