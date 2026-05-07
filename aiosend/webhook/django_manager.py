import json
from http import HTTPStatus
from typing import TYPE_CHECKING

from .base import WebhookManager

if TYPE_CHECKING:
    from django.http import HttpRequest, JsonResponse
    from django.urls import URLPattern  # noqa: F401

    from .base import WebServerHandler


class DjangoManager(WebhookManager["list[URLPattern]"]):
    """
    Django webhook manager.

    Webhook manager based on Django's URL routing.
    """

    def register_handler(
        self,
        feed_update: "WebServerHandler",
    ) -> None:
        """Register webhook handler."""
        try:
            from django.http import JsonResponse  # noqa: PLC0415
            from django.urls import path  # noqa: PLC0415
            from django.views.decorators.csrf import (  # noqa: PLC0415
                csrf_exempt,
            )
        except ModuleNotFoundError as e:
            msg = "django is not installed"
            raise RuntimeError(msg) from e

        @csrf_exempt
        async def handle(
            request: "HttpRequest",
        ) -> "JsonResponse":
            status = await feed_update(
                json.loads(request.body),
                dict(request.headers),
            )
            return JsonResponse(
                {"ok": status},
                status=HTTPStatus.OK
                if status
                else HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        self._app.append(path(self._path, handle))
