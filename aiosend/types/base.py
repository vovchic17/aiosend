from abc import ABC
from typing import TYPE_CHECKING, Annotated, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, PrivateAttr
from pydantic.functional_serializers import PlainSerializer

from aiosend._utils import serialize_list

if TYPE_CHECKING:
    from aiosend import CryptoPay

_CryptoPayType = TypeVar(
    "_CryptoPayType",
    bound="CryptoPayObject | list | bool",
)
_T = TypeVar("_T")
SerList = Annotated[list[_T], PlainSerializer(serialize_list, str | None)]


class CryptoPayObject(BaseModel, ABC):
    """Base object class for types."""

    _client: "CryptoPay" = PrivateAttr()

    model_config = ConfigDict(
        extra="allow",
    )

    def model_post_init(self, ctx: dict) -> None:
        """Bind client to CryptoPayObject."""
        self._client = ctx["client"]


class Error(BaseModel):
    """API error model."""

    code: int
    name: str

    model_config = ConfigDict(
        extra="allow",
        frozen=True,
    )


class ItemsList(BaseModel, Generic[_CryptoPayType]):
    """
    Items list.

    This model is used to convert a dictionary with the `items` key to a list.
    """

    items: _CryptoPayType


class Response(BaseModel, Generic[_CryptoPayType]):
    """API response model."""

    ok: bool
    result: _CryptoPayType | ItemsList[_CryptoPayType] | None = None
    error: Error | None = None
