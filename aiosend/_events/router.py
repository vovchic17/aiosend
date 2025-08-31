from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Self

    from aiosend._events.observer import EventObserver
    from aiosend.types import CryptoPayObject


class BaseRouter:
    """Base router for handling and propogate events."""

    def __init__(self, *, name: str | None = None) -> None:
        self.name = name or hex(id(self))
        self.observers: dict[str, EventObserver] = {}
        self.parent: BaseRouter | None = None
        self.sub_routers: list[BaseRouter] = []

    def include_router(self, router: "Self") -> None:
        """Include another router to this one."""
        if not isinstance(self, type(router)):
            msg = (
                f"Router {router} is not a {self.__class__.__name__} instance"
            )
            raise TypeError(msg)

        if router is self:
            msg = "Router cannot include self"
            raise ValueError(msg)

        if router.parent is not None:
            msg = f"Router is already attached to {router.parent}"
            raise RuntimeError(msg)

        parent = router.parent
        while parent is not None:
            if parent is self:
                msg = f"Circular inclusion between {self} and {router}"
                raise RuntimeError(msg)
            parent = parent.parent

        self.sub_routers.append(router)

    def include_routers(self, *routers: "Self") -> None:
        """Include multiple routers to this one."""
        for router in routers:
            self.include_router(router)

    async def propagate_event(
        self,
        event: "CryptoPayObject",
        event_type: str,
        **kwargs: object,
    ) -> bool:
        is_handled = False

        observer = self.observers.get(event_type)
        if observer is not None:
            is_handled = await observer.trigger(event, **kwargs)

        for router in self.sub_routers:
            is_handled = await router.propagate_event(
                event,
                event_type,
                **kwargs,
            )
            if is_handled:
                break

        return is_handled

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name}"

    def __repr__(self) -> str:
        return f"<{self}>"
