from aiosend._events.observer import EventObserver
from aiosend._events.router import BaseRouter


class PollingRouter(BaseRouter):
    """Router for polling events."""

    def __init__(self, *, name: str | None = None) -> None:
        super().__init__(name=name)

        self.invoice_paid = EventObserver()
        self.invoice_expired = EventObserver()
        self.check_activated = EventObserver()
        self.check_expired = EventObserver()

        self.observers = {
            "invoice_paid": self.invoice_paid,
            "invoice_expired": self.invoice_expired,
            "check_activated": self.check_activated,
            "check_expired": self.check_expired,
        }
