from typing import TYPE_CHECKING

from aiosend import loggers
from aiosend.client import MAINNET, TESTNET
from aiosend.exceptions import APIError, WrongNetworkError
from aiosend.methods import Methods
from aiosend.polling import PollingConfig, PollingManager
from aiosend.tools import Tools
from aiosend.utils import PropagatingThread
from aiosend.webhook import AiohttpManager, RequestHandler

from .session import AiohttpSession

if TYPE_CHECKING:
    from aiosend.client import APIServer
    from aiosend.methods import CryptoPayMethod
    from aiosend.types import App, _CryptoPayType
    from aiosend.webhook import _APP, WebhookManager

    from .session import BaseSession


class CryptoPay(Methods, Tools, RequestHandler, PollingManager):
    """
    Client class providing API methods.

    :param token: Crypto Bot API token
    :param session: HTTP Session
    :param api_server: Crypto Bot API server
    """

    def __init__(
        self,
        token: str,
        api_server: "APIServer" = MAINNET,
        session: "type[BaseSession]" = AiohttpSession,
        manager: "WebhookManager[_APP] | None" = None,
        polling_config: "PollingConfig | None" = None,
    ) -> None:
        self._token = token
        self.session = session(api_server)
        RequestHandler.__init__(self, manager or AiohttpManager())
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
        :return: :class:`CryptoPayType` object.
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
                self.session.api_server.name,
            )
        except APIError:
            current_net = self.session.api_server
            if current_net == MAINNET:
                self.session = self.session.__class__(TESTNET)
            else:
                self.session = self.session.__class__(MAINNET)
            self.get_me()  # type: ignore[unused-coroutine]
            net = self.session.api_server
            msg = (
                "Authorization failed. Token is served by the "
                f"{net.name}, you are using {current_net.name}"
            )
            raise WrongNetworkError(msg) from None
