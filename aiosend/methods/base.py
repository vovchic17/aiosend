from abc import ABC
from typing import ClassVar, Generic

from pydantic import BaseModel, ConfigDict

from aiosend.types import _CryptoPayType


class CryptoPayMethod(BaseModel, Generic[_CryptoPayType], ABC):
    """Base `Crypto Pay API` method class."""

    model_config = ConfigDict(
        extra="ignore",
        frozen=True,
    )

    __return_type__: ClassVar[type[_CryptoPayType]]
    __method__: ClassVar[str]
