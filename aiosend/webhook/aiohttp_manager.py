from http import HTTPStatus
from typing import TYPE_CHECKING

from aiohttp.web import json_response

from .base import WebhookManager

if TYPE_CHECKING:
    from aiohttp.web import Application, Request, Response  # noqa: F401

    from .base import WebServerHandler


class AiohttpManager(WebhookManager["Application"]):
    """
    aiohttp webhook manager.

    Webhook manager based on :class:`aiohttp.web.Application`.
    """

    def register_handler(
        self,
        feed_update: "WebServerHandler",
    ) -> None:
        """Register webhook handler."""

        async def handle(request: "Request") -> "Response":
            status = await feed_update(
                await request.json(),
                dict(request.headers),
            )
            return json_response(
                {"ok": status},
                status=HTTPStatus.OK
                if status
                else HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        self._app.router.add_post(self._path, handle)
