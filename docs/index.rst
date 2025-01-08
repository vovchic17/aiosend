.. raw:: html

   <h1><span class="BB">A</span>sync<span class="BB">IOC</span>rypto<span class="BB">P</span>ay<span class="BB">A</span>PI</h1>

Introduction
------------

**aiosend** is a syncronous & asynchronous `Crypto Pay API <https://help.crypt.bot/crypto-pay-api>`_ client.

.. seealso::
   |telegram| **aiosend** has `community chat on Telegram <https://aiosend.t.me>`_

.. |telegram| image:: https://raw.githubusercontent.com/vovchic17/static/2cae16d0c4289f9556dacc13322dd4a2fcca214f/src/telegram_logo.svg
   :width: 24px
   :alt: python

Features
--------
* provides :doc:`polling handler <client/polling>`
* provides :doc:`webhook handler <client/webhook>`
* provides :doc:`additional function shortcuts <client/tools>`
* supports sync and async usage


Quick start
-----------

.. literalinclude:: ../examples/quick_start.py


Syncronous usage
----------------

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
