from typing import Protocol

from aiosend.client.session import BaseSession

class SessionNetworkProtocol(Protocol):
    session: BaseSession
