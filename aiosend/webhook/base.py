import hashlib
import json
from abc import ABC, abstractmethod
from hmac import HMAC
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from magic_filter.magic import MagicFilter

from aiosend import loggers
from aiosend._handler import HandlerObject
from aiosend.exceptions import CryptoPayError
from aiosend.types import Update

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Mapping

    import aiosend
    from aiosend._handler import CallbackType

    WebServerHandler = Callable[[dict[str, Any], Mapping[str, str]], Awaitable]

_APP = TypeVar("_APP")


class WebhookManager(Generic[_APP], ABC):
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
        feed_update: """Callable[[dict[str, Any],
        dict[str, str]], Awaitable[bool]]""",
    ) -> None:
        """
        Register webhook handler.

        Override this method in your own webhook manager class.
        This method is used for registering webhook handler in your app.

        :param handler: Web server handler object.
        :return:
        """


class RequestHandler:
    """Updates handler."""

    def __init__(
        self,
        manager: WebhookManager[_APP] | None,
    ) -> None:
        if manager is not None:
            manager.register_handler(self.feed_update)
        self._webhook_manager = manager
        self._webhook_handlers: list[HandlerObject] = []

    def _check_signature(
        self: "aiosend.CryptoPay",
        body: "dict[str, Any]",
        headers: dict[str, str],
    ) -> bool:
        """
        Verify the received update and the integrity of the received data.

        Source: https://help.crypt.bot/crypto-pay-api#verifying-webhook-updates

        :param body: unparsed JSON string.
        :param headers: request headers.
        :return: True if the signature is correct, False otherwise.
        """
        secret = hashlib.sha256(self._token.encode()).digest()
        check_string = json.dumps(
            body,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        hmac = HMAC(secret, check_string.encode(), hashlib.sha256).hexdigest()
        return hmac == headers.get("crypto-pay-api-signature")

    async def feed_update(
        self: "aiosend.CryptoPay",
        body: "dict[str, Any]",
        headers: dict[str, str],
    ) -> bool:
        """
        Feed an update to the invoice handler.

        :param body: parsed json body.
        :param headers: request headers.

        :return: :code:`True` on success.
        """
        try:
            update = Update.model_validate(body, context={"client": self})
            if not self._check_signature(body, headers):  # type: ignore[attr-defined]
                loggers.webhook.info(
                    "Webhook Update id=%d is not handled. "
                    "Signature is invalid.",
                    update.update_id,
                )
                return False
            for handler in self._webhook_handlers:
                result, data = await handler.check(update.payload)
                if result:
                    await handler.call(update.payload, data | self._kwargs)
                    loggers.webhook.info(
                        "Webhook Update id=%d is handled.",
                        update.update_id,
                    )
                    break
            else:
                loggers.webhook.info(
                    "Webhook Update id=%d is not handled. "
                    "No suitable handlers.",
                    update.update_id,
                )
        except Exception:  # noqa: BLE001
            loggers.webhook.exception("Error while handling update:\n")
            return False
        return True

    def webhook(
        self,
        *filters: MagicFilter,
    ) -> "Callable[[CallbackType], CallbackType]":
        """
        Register a handler for webhook invoice updates.

        Decorator for handler function.

        :return: handler function.
        """

        def wrapper(handler: "CallbackType") -> "CallbackType":
            if self._webhook_manager is None:
                msg = "Webhook manager is not set."
                raise CryptoPayError(msg)
            self._webhook_handlers.append(HandlerObject(handler, filters))
            return handler

        return wrapper
