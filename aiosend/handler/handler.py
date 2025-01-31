import inspect
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from typing import Any

from magic_filter.magic import MagicFilter

Handler = Callable[..., Any]


@dataclass(slots=True)
class HandlerObject:
    """Handler object."""

    handler: Handler
    filters: tuple[MagicFilter, ...]

    def check(self, obj: object) -> bool:
        """Check if the handler is suitable for the object."""
        return all(f.resolve(obj) for f in self.filters)

    async def call(
        self,
        obj: object,
        data: dict[str, "Any"] | None = None,
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
