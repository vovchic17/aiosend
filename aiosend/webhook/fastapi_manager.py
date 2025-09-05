from typing import TYPE_CHECKING

from .base import WebhookManager

if TYPE_CHECKING:
    from fastapi import APIRouter, FastAPI  # noqa: F401

    from .base import WebServerHandler


class FastAPIManager(WebhookManager["FastAPI | APIRouter"]):
    """
    FastAPI webhook manager.

    Webhook manager based on :class:`fastapi.FastAPI`.
    """

    def register_handler(
        self,
        feed_update: "WebServerHandler",
    ) -> None:
        """Register webhook handler."""
        try:
            from fastapi import HTTPException, Request  # noqa: PLC0415
        except ModuleNotFoundError as e:
            msg = "fastapi is not installed"
            raise RuntimeError(msg) from e

        @self._app.post(self._path)
        async def handle(request: Request) -> dict:
            status = await feed_update(
                await request.json(),
                dict(request.headers),
            )
            resp = {"ok": status}
            if not status:
                raise HTTPException(500, resp)
            return resp
