import ssl
from typing import TYPE_CHECKING, cast
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import certifi
from aiohttp.http import SERVER_SOFTWARE
from pydantic import ValidationError

from aiosend.__meta__ import __version__
from aiosend._methods import GetMe
from aiosend.exceptions import APIError, DeserializationError
from aiosend.types import App, Response

if TYPE_CHECKING:
    from aiosend import CryptoPay
    from aiosend.client import Network
    from aiosend.types import Error


def token_validate(client: "CryptoPay", network: "Network") -> App:
    method = GetMe.GetMeMethod()
    url = network.url(method)
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    try:
        request = Request(  # noqa: S310
            url,
            headers={
                "Crypto-Pay-API-Token": client._token,  # noqa: SLF001
                "Content-Type": "application/json",
                "User-Agent": f"{SERVER_SOFTWARE} aiosend/{__version__}",
            },
        )
        resp = urlopen(request, context=ssl_context).read()  # noqa: S310
    except HTTPError as e:
        resp = e.read()

    try:
        response = Response[App].model_validate_json(
            resp,
            context={"client": client},
        )
    except ValidationError as e:
        raise DeserializationError(
            method,
            "Failed to deserialize object",
        ) from e
    if not response.ok:
        error = cast("Error", response.error)
        raise APIError(method, error)
    return cast("App", response.result)
