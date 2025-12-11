from typing import TYPE_CHECKING

from aiosend import loggers
from aiosend._methods import Methods
from aiosend._utils.check_token import token_validate
from aiosend.client.network import MAINNET, TESTNET
from aiosend.exceptions import APIError, WrongNetworkError
from aiosend.polling import PollingConfig, PollingManager, PollingRouter
from aiosend.tools import Tools
from aiosend.webhook import WebhookHandler, WebhookRouter

from .session import AiohttpSession

if TYPE_CHECKING:
    from aiosend._events.router import BaseRouter
    from aiosend._methods import CryptoPayMethod
    from aiosend.client import Network
    from aiosend.types import App, _CryptoPayType


class CryptoPay(Methods, Tools, WebhookHandler, PollingManager):
    """
    Client class providing API methods.

    :param token: Crypto Bot API token
    :param network: Crypto Bot API server
    :param session: HTTP Session
    :webhook_manager: Webhook manager (based on aiohttp, fastapi, flask etc.)
    :polling_config: Configuration for invoice and check polling
    :timeout: HTTP request timeout in seconds
    :kwargs: Optional argumets to pass into the polling and webhook handlers
    """

    def __init__(
        self,
        token: str,
        network: "Network" = MAINNET,
        **kwargs: object,
    ) -> None:
        self._token = token
        session = kwargs.pop("session", AiohttpSession)
        self.session = session(network, kwargs.pop("timeout", 300))
        self._kwargs = {"cp": self}
        self._kwargs |= kwargs
        WebhookHandler.__init__(self, kwargs.pop("webhook_manager", None))
        PollingManager.__init__(
            self,
            kwargs.pop("polling_config", PollingConfig()),
        )
        self.__auth()

    async def __call__(
        self,
        method: "CryptoPayMethod[_CryptoPayType]",
    ) -> "_CryptoPayType":
        """
        Request method.

        Use this method to make an API request.

        :param method: CryptoPayMethod object.
        :return: :class:`aiosend.types.CryptoPayType` object.
        """
        loggers.client.debug(
            "Requesting: /%s with payload %s",
            method.__method__,
            method.model_dump_json(),
        )
        return await self.session.request(self._token, self, method)

    def __auth(self) -> None:
        try:
            me: App = token_validate(self, self.session.network)
            loggers.client.info(
                "Authorized as '%s' id=%d on %s",
                me.name,
                me.app_id,
                self.session.network.name,
            )
        except APIError:
            current_net = self.session.network
            self.session = self.session.__class__(
                TESTNET if current_net == MAINNET else MAINNET,
                self.session.timeout,
            )
            token_validate(self, self.session.network)
            net = self.session.network
            msg = (
                "Authorization failed. Token is served by the "
                f"{net.name}, you are using {current_net.name}"
            )
            raise WrongNetworkError(msg) from None

    def include_router(self, router: "BaseRouter") -> None:
        """
        Include router into the client.

        :param router: Router object.
        """
        if isinstance(router, WebhookRouter):
            WebhookHandler.include_router(self, router)
        elif isinstance(router, PollingRouter):
            PollingManager.include_router(self, router)
        else:
            msg = (
                f"Router {router} is neither WebhookRouter "
                "or PollingRouter instance"
            )
            raise TypeError(msg)

    def __setitem__(self, key: str, value: object) -> None:
        self._kwargs[key] = value

    def __getitem__(self, key: str) -> object:
        return self._kwargs[key]

    def __delitem__(self, key: str) -> None:
        del self._kwargs[key]

    def __contains__(self, key: str) -> bool:
        return key in self._kwargs
