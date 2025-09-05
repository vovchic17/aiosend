from typing import Protocol

from aiosend.polling import PollingManager

class ClientWebhookManagerProtocol(PollingManager, Protocol):  # type: ignore[misc]
    _webhook_manager: object
