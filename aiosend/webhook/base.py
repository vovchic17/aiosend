import hashlib
import re
from abc import ABC, abstractmethod
from hmac import HMAC
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from aiosend import loggers
from aiosend.types import Update

from .router import WebhookRouter

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Mapping

    WebServerHandler = Callable[
        [str, Mapping[str, str]],
        Awaitable[bool],
    ]

_APP = TypeVar("_APP", bound=Any)


class WebhookManager(ABC, Generic[_APP]):
    """
    Webhook manager.

    If you want to implement your own webhook
    manager, you must inherit from this class.
    """

    def __init__(self, app: _APP, path: str) -> None:
        self._app = app
        self._path = path

    @abstractmethod
    def register_handler(
        self,
        feed_update: "WebServerHandler",
    ) -> None:
        """
        Register webhook handler.

        Override this method in your own webhook manager class.
        This method is used for registering webhook handler in your app.

        :param handler: Web server handler object.
        :return:
        """


class WebhookHandler(WebhookRouter):
    """Updates handler."""

    _token: str
    _kwargs: dict[str, "Any"]

    def __init__(
        self,
        manager: WebhookManager[_APP] | None,
    ) -> None:
        if manager is not None:
            manager.register_handler(self.feed_update)
        self._webhook_manager = manager

    def _check_signature(
        self,
        body: str,
        headers: "Mapping[str, str]",
    ) -> bool:
        """
        Verify the received update and the integrity of the received data.

        Source: https://help.send.tg/en/articles/10279948-crypto-pay-api#h_f0180ed474

        :param body: unparsed JSON string.
        :param headers: request headers.
        :return: True if the signature is correct, False otherwise.
        """
        secret = hashlib.sha256(self._token.encode()).digest()
        hmac = HMAC(secret, body.encode(), hashlib.sha256).hexdigest()
        signature = headers.get(
            "Crypto-Pay-Api-Signature",
        ) or headers.get(
            "crypto-pay-api-signature",
        )
        return hmac == signature

    @staticmethod
    def _extract_update_id(body: str) -> int:
        mtch = re.match(r'"update_id"\s*:\s*(\d+)', body)
        if mtch is None:
            msg = "Can't extract update_id from request body"
            raise ValueError(msg)
        update_id = mtch.group(1)
        if not update_id.isdigit():
            msg = "Invalid update_id"
            raise ValueError(msg)
        return int(update_id)

    async def feed_update(
        self,
        body: str,
        headers: "Mapping[str, str]",
    ) -> bool:
        """
        Feed an update to the invoice handler.

        :param body: parsed json body.
        :param headers: request headers.

        :return: :code:`True` on success.
        """
        try:
            if not self._check_signature(body, headers):
                try:
                    update_id = self._extract_update_id(body)
                    loggers.webhook.warning(
                        "Webhook Update id=%d is not handled. "
                        "Signature is invalid.",
                        update_id,
                    )
                except ValueError as e:
                    loggers.webhook.warning(
                        "Webhook Update is not handled. %s",
                        e,
                    )
                return False
            update = Update.model_validate_json(body, context={"client": self})
            if await self.propagate_event(
                update.payload,
                update.update_type,
                **self._kwargs,
            ):
                loggers.webhook.info(
                    "Webhook Update id=%d is handled.",
                    update.update_id,
                )
            else:
                loggers.webhook.info(
                    "Webhook Update id=%d is not handled. "
                    "No suitable handlers.",
                    update.update_id,
                )
        except Exception:  # noqa: BLE001 logger catches exception
            loggers.webhook.exception("Error while handling update:\n")
            return False
        return True
