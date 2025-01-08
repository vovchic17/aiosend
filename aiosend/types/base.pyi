from abc import ABC
from collections.abc import Generator
from typing import Generic, TypeAlias, TypeVar

from pydantic import BaseModel
from typing_extensions import Self

from aiosend import CryptoPay

_CryptoPayType = TypeVar(
    "_CryptoPayType",
    bound=CryptoPayObject | list | bool,
)
_T = TypeVar("_T")
SerList: TypeAlias = list[_T]

class CryptoPayObject(BaseModel, ABC):
    _client: CryptoPay
    def __await__(self) -> Generator[None, None, Self]: ...

class Error(BaseModel):
    code: int
    name: str

class ItemsList(BaseModel, Generic[_CryptoPayType]):
    items: _CryptoPayType

class Response(BaseModel, Generic[_CryptoPayType]):
    ok: bool
    result: _CryptoPayType | ItemsList[_CryptoPayType] | None = None
    error: Error | None = None
