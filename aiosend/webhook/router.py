from aiosend._events.observer import EventObserver
from aiosend._events.router import BaseRouter


class WebhookRouter(BaseRouter):
    """Router for webhook updates."""

    def __init__(self, name: str | None = None) -> None:
        super().__init__(name=name)

        self.invoice_paid = EventObserver()

        self.observers = {
            "invoice_paid": self.invoice_paid,
        }
