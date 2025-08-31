from typing import TYPE_CHECKING

from aiosend._events.handler import HandlerObject

if TYPE_CHECKING:
    from collections.abc import Callable

    from aiosend._events.handler import CallbackType
    from aiosend.types import CryptoPayObject


class EventObserver:
    def __init__(self) -> None:
        self.handlers: list[HandlerObject] = []

    def __call__(
        self,
        *filters: "CallbackType",
    ) -> "Callable[[CallbackType], CallbackType]":
        def wrapper(handler: "CallbackType") -> "CallbackType":
            self.register(handler, *filters)
            return handler

        return wrapper

    def register(
        self,
        handler: "CallbackType",
        *filters: "CallbackType",
    ) -> None:
        self.handlers.append(HandlerObject(handler, filters))

    async def trigger(
        self,
        event: "CryptoPayObject",
        **kwargs: object,
    ) -> bool:
        for handler in self.handlers:
            result, data = await handler.check(event)
            if result:
                await handler.call(event, data | kwargs)
                return True
        return False
