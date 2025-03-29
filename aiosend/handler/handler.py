import inspect
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from typing import Any

from magic_filter.magic import MagicFilter

CallbackType = Callable[..., Any]


@dataclass(slots=True)
class HandlerObject:
    """Handler object."""

    handler: CallbackType
    filters: tuple[MagicFilter | CallbackType, ...]

    async def check(self, obj: object) -> tuple[bool, dict[str, object]]:
        """Check if the handler is suitable for the update."""
        data: dict[str, object] = {}
        for f in self.filters:
            check = False
            if isinstance(f, MagicFilter):
                check = f.resolve(obj)
            elif inspect.isawaitable(f) or inspect.iscoroutinefunction(f):
                check = await f(obj)
            elif inspect.isfunction(f):
                check = f(obj)
            if not check:
                return False, data
            if isinstance(check, dict):
                data.update(check)
        return True, data

    async def call(
        self,
        obj: object,
        data: dict[str, object] | None = None,
    ) -> None:
        """Call handler."""
        if data is None:
            data = {}
        spec = inspect.getfullargspec(self.handler)
        is_async = inspect.iscoroutinefunction(self.handler)
        handler = partial(
            self.handler,
            obj,
            **data
            if spec.varkw is not None
            else {k: v for k, v in data.items() if k in spec.args},
        )
        if is_async:
            await handler()
        else:
            handler()
