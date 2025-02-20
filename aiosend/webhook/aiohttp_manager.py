from typing import TYPE_CHECKING

from aiohttp.web import json_response

from .base import WebhookManager

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from typing import Any

    from aiohttp.web import Application, Request, Response  # noqa: F401


class AiohttpManager(WebhookManager["Application"]):
    """
    aiohttp webhook manager.

    Webhook manager based on :class:`aiohttp.web.Application`.
    """

    def register_handler(
        self,
        feed_update: """Callable[[dict[str, Any],
        dict[str, str]], Awaitable[bool]]""",
    ) -> None:
        """Register webhook handler."""

        async def handle(request: "Request") -> "Response":
            status = await feed_update(
                await request.json(),
                dict(request.headers),
            )
            return json_response(
                {"ok": status},
                status=200 if status else 500,
            )

        self._app.router.add_post(self._path, handle)
