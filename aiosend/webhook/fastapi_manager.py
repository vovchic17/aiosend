from typing import TYPE_CHECKING

from .base import WebhookManager

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from typing import Any

    from fastapi import FastAPI  # noqa: F401


class FastAPIManager(WebhookManager["FastAPI"]):
    """
    FastAPI webhook manager.

    Webhook manager based on :class:`fastapi.FastAPI`.
    """

    def register_handler(
        self,
        feed_update: """Callable[[dict[str, Any],
        dict[str, str]], Awaitable[bool]]""",
    ) -> None:
        """Register webhook handler."""
        try:
            from fastapi import HTTPException, Request
        except ModuleNotFoundError as e:
            msg = "fastapi is not installed"
            raise RuntimeError(msg) from e

        @self._app.post(self._path)
        async def handle(request: Request) -> dict:
            status = await feed_update(
                await request.json(),
                dict(request.headers),
            )
            if not status:
                raise HTTPException(500, {"ok": status})
            return {"ok": status}
