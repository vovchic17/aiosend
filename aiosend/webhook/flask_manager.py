from typing import TYPE_CHECKING

from .base import WebhookManager

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from typing import Any

    from flask import Flask  # noqa: F401


class FlaskManager(WebhookManager["Flask"]):
    """
    Flask webhook manager.

    Webhook manager based on :class:`flask.Flask`.
    """

    def register_handler(
        self,
        feed_update: """Callable[[dict[str, Any],
        dict[str, str]], Awaitable[bool]]""",
    ) -> None:
        """Register webhook handler."""
        try:
            from flask import request
        except ModuleNotFoundError as e:
            msg = "flask is not installed"
            raise RuntimeError(msg) from e

        @self._app.post(self._path)
        async def handle() -> tuple[dict[str, bool], int]:
            status = await feed_update(
                request.get_json(),
                dict(request.headers),
            )
            return {"ok": status}, 200 if status else 500
