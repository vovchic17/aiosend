from typing import TYPE_CHECKING

from aiohttp.web import Application, json_response

from .base import WebhookManager

if TYPE_CHECKING:
    from aiohttp.web import Request, Response

    from .base import Handler


class AiohttpManager(WebhookManager[Application]):
    """
    aiohttp webhook manager.

    Webhook manager based on :class:`aiohttp.web.Application`.
    """

    def register_handler(
        self,
        app: Application,
        path: str,
        handler: "Handler",
    ) -> None:
        """Register webhook handler."""

        async def handle(request: "Request") -> "Response":
            await handler(
                await request.json(),
                request.headers,
            )
            return json_response({"ok": True})

        app.router.add_post(path, handle)
