import functools
import hashlib
import json
from abc import ABC, abstractmethod
from hmac import HMAC
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from aiosend import loggers
from aiosend.types import Update

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Mapping

    import aiosend
    from aiosend.types import Invoice

    InvoiceHandler = Callable[[Invoice], Awaitable]
    Handler = Callable[[dict[str, Any], Mapping[str, str]], Awaitable]

_APP = TypeVar("_APP")


class WebhookManager(Generic[_APP], ABC):
    """
    Webhook manager.

    If you want to implement your own webhook
    manager, you must inherit from this class.
    """

    @abstractmethod
    def register_handler(
        self,
        app: _APP,
        path: str,
        handler: "Handler",
    ) -> None:
        """
        Register webhook handler.

        Override this method in your own webhook manager class.
        This method is used for registering webhook handler in your app.
        You should call `handler` whenever an update arrives.

        :param app: Web application.
        :param path: Path to webhook route.
        :param handler: Handler object.
        :return:
        """


class RequestHandler(Generic[_APP]):
    """Updates handler."""

    def __init__(
        self,
        manager: WebhookManager[_APP],
    ) -> None:
        self._webhook_manager = manager

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
        return hmac == headers.get("Crypto-Pay-Api-Signature")

    async def feed_update(
        self,
        handler: "InvoiceHandler",
        body: dict[str, Any],
        headers: dict[str, str],
    ) -> None:
        """
        Feed an update to the invoice handler.

        :param body: parsed json body.
        :param headers: request headers.
        """
        update = Update.model_validate(body, context={"client": self})
        if self._check_signature(body, headers):
            await handler(update.payload)
            loggers.webhook.info(
                "Webhook Update id=%d is handled.",
                update.update_id,
            )
        else:
            loggers.webhook.info(
                "Webhook Update id=%d is not handled. Signature is invalid.",
                update.update_id,
            )

    def webhook_handler(
        self,
        app: _APP,
        path: str,
    ) -> "Callable[[InvoiceHandler], InvoiceHandler]":
        """
        Register a handler for webhook invoice updates.

        :param app: web application.
        :param path: webhook path.

        :return: handler function.
        """

        def wrapper(handler: "InvoiceHandler") -> "InvoiceHandler":
            self._webhook_manager.register_handler(
                app,
                path,
                functools.partial(self.feed_update, handler),
            )
            return handler

        return wrapper
