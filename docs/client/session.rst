=======
Session
=======

**aiosend** uses `aiohttp <https://docs.aiohttp.org/en/stable/index.html>`_ session by default.
You can implement your own session by inheriting :class:`BaseSession <aiosend.client.session.BaseSession>`
and overriding :meth:`request <aiosend.client.session.BaseSession.request>` method.

.. automodule:: aiosend.client.session
    :show-inheritance:
    :members: