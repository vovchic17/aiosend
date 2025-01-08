from typing import TYPE_CHECKING

from .base import WebhookManager

if TYPE_CHECKING:
    from flask import Flask

    from .base import Handler


class FlaskManager(WebhookManager["Flask"]):
    """
    Flask webhook manager.

    Webhook manager based on :class:`flask.Flask`.
    """

    def register_handler(
        self,
        app: "Flask",
        path: str,
        handler: "Handler",
    ) -> None:
        """Register webhook handler."""
        try:
            from flask import request
        except ModuleNotFoundError as e:
            msg = "fastapi is not installed"
            raise RuntimeError(msg) from e

        @app.post(path)
        async def handle() -> dict:
            await handler(
                request.get_json(),
                request.headers,
            )
            return {"ok": True}
