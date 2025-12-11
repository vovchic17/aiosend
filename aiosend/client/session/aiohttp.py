import ssl
from typing import TYPE_CHECKING, cast

import certifi
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from aiohttp.http import SERVER_SOFTWARE

from aiosend.__meta__ import __version__
from aiosend.exceptions import APITimeoutError

from .base import BaseSession

if TYPE_CHECKING:
    import aiosend
    from aiosend._methods import CryptoPayMethod
    from aiosend.client import Network
    from aiosend.types import _CryptoPayType


class AiohttpSession(BaseSession):
    """
    Http session based on aiohttp.

    This class is a wrapper of `aiohttp.ClientSession`.
    """

    def __init__(self, network: "Network", timeout: float = 300) -> None:
        super().__init__(network, timeout)
        self._session: ClientSession | None = None

    async def request(
        self,
        token: str,
        client: "aiosend.CryptoPay",
        method: "CryptoPayMethod[_CryptoPayType]",
    ) -> "_CryptoPayType":
        """Make http request."""
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self._session = ClientSession(
            timeout=ClientTimeout(self.timeout),
            connector=TCPConnector(
                ssl_context=ssl_context,
            ),
        )
        async with self._session as session:
            try:
                resp = await session.post(
                    url=self.network.url(method),
                    data=method.model_dump_json(exclude_none=True),
                    headers={
                        "Crypto-Pay-API-Token": token,
                        "Content-Type": "application/json",
                        "User-Agent": f"{SERVER_SOFTWARE} "
                        f"aiosend/{__version__}",
                    },
                )
            except TimeoutError as e:
                raise APITimeoutError(method, self.timeout) from e
            response = self._check_response(client, method, await resp.text())
        return cast("_CryptoPayType", response.result)
