.. _ShortcutsAnchor:

================
Shortcut methods
================

These methods simplify the use of standard :ref:`Crypto Pay API methods <MethodsAnchor>`
and also provide additional functionality to the objects.

Updating objects
----------------

.. automethod:: aiosend.types.Balance.update
.. automethod:: aiosend.types.Check.update
.. automethod:: aiosend.types.ExchangeRate.update
.. automethod:: aiosend.types.Invoice.update

Deleting objects
----------------

.. automethod:: aiosend.types.Check.delete
.. automethod:: aiosend.types.Invoice.delete

QR code of object
-----------------

.. autoproperty:: aiosend.types.Check.qr
.. autoproperty:: aiosend.types.Invoice.qr

Check image
-----------

.. automethod:: aiosend.types.Check.get_image

Poll objects
------------

.. automethod:: aiosend.types.Check.poll
.. automethod:: aiosend.types.Invoice.poll

Usage examples
--------------

.. literalinclude:: ../../examples/invoice_object.py

.. literalinclude:: ../../examples/check_object.py