from typing import TYPE_CHECKING

from aiosend import loggers
from aiosend._methods import Methods
from aiosend._utils import PropagatingThread
from aiosend.client.network import MAINNET, TESTNET
from aiosend.exceptions import APIError, WrongNetworkError
from aiosend.polling import PollingConfig, PollingManager
from aiosend.tools import Tools
from aiosend.webhook import RequestHandler

from .session import AiohttpSession

if TYPE_CHECKING:
    from aiosend._methods import CryptoPayMethod
    from aiosend.client import Network
    from aiosend.types import App, _CryptoPayType
    from aiosend.webhook import _APP, WebhookManager

    from .session import BaseSession


class CryptoPay(Methods, Tools, RequestHandler, PollingManager):
    """
    Client class providing API methods.

    :param token: Crypto Bot API token
    :param network: Crypto Bot API server
    :param session: HTTP Session
    :webhook_manager: Webhook manager (based on aiohttp, fastapi, flask etc.)
    :polling_config: Configuration for invoice and check polling
    :kwargs: Optional argumets to pass into the polling and webhook handlers
    """

    def __init__(
        self,
        token: str,
        network: "Network" = MAINNET,
        session: "type[BaseSession]" = AiohttpSession,
        webhook_manager: "WebhookManager[_APP] | None" = None,
        polling_config: "PollingConfig | None" = None,
        **kwargs: object,
    ) -> None:
        self._token = token
        self.session = session(network)
        self._kwargs = kwargs
        RequestHandler.__init__(self, webhook_manager)
        PollingManager.__init__(self, polling_config or PollingConfig())
        thread = PropagatingThread(target=self.__auth)
        thread.start()
        thread.join()

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
            me: App = self.get_me()  # type: ignore[assignment]
            loggers.client.info(
                "Authorized as '%s' id=%d on %s",
                me.name,
                me.app_id,
                self.session.network.name,
            )
        except APIError:
            current_net = self.session.network
            if current_net == MAINNET:
                self.session = self.session.__class__(TESTNET)
            else:
                self.session = self.session.__class__(MAINNET)
            self.get_me()  # type: ignore[unused-coroutine]
            net = self.session.network
            msg = (
                "Authorization failed. Token is served by the "
                f"{net.name}, you are using {current_net.name}"
            )
            raise WrongNetworkError(msg) from None

    def __setitem__(self, key: str, value: object) -> None:
        self._kwargs[key] = value

    def __getitem__(self, key: str) -> object:
        return self._kwargs[key]

    def __delitem__(self, key: str) -> None:
        del self._kwargs[key]

    def __contains__(self, key: str) -> bool:
        return key in self._kwargs
