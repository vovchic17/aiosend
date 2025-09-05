from decimal import Decimal
from enum import Enum
from fractions import Fraction
from types import NoneType, UnionType
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Union,
    cast,
    get_args,
    get_origin,
)
from uuid import UUID

from magic_filter import MagicFilter
from pydantic import BaseModel
from pydantic_core import PydanticUndefined

from aiosend.types import Invoice

if TYPE_CHECKING:
    from pydantic import ConfigDict
    from pydantic.fields import FieldInfo
    from typing_extensions import Self, Unpack

    class PayloadDataConfigDict(ConfigDict, total=False):
        sep: str
        prefix: str


class PayloadData(BaseModel):
    """Base payload data class."""

    __separator__: ClassVar[str]
    __prefix__: ClassVar[str]
    MAX_PAYLOAD_LENGTH: ClassVar[int] = 4000

    def __init_subclass__(
        cls,
        **kwargs: "Unpack[PayloadDataConfigDict]",
    ) -> None:
        if "prefix" not in kwargs:
            msg = (
                f"prefix required, usage example: "
                f"`class {cls.__name__}"
                "(PayloadData, prefix='my_payload'): ...`"
            )
            raise ValueError(msg)
        cls.__separator__ = kwargs.pop("sep", ":")
        cls.__prefix__ = kwargs.pop("prefix")
        if cls.__separator__ in cls.__prefix__:
            msg = (
                f"Separator symbol {cls.__separator__!r} can not be used "
                f"inside prefix {cls.__prefix__!r}"
            )
            raise ValueError(msg)
        super().__init_subclass__(**cast("ConfigDict", kwargs))

    def _encode_value(self, key: str, value: object) -> str:
        if value is None:
            return ""
        if isinstance(value, Enum):
            return str(value.value)
        if isinstance(value, UUID):
            return value.hex
        if isinstance(value, bool):
            return str(int(value))
        if isinstance(value, int | str | float | Decimal | Fraction):
            return str(value)
        msg = (
            f"Attribute {key}={value!r} of type {type(value).__name__!r}"
            f" can not be packed to payload data"
        )
        raise ValueError(msg)

    def pack(self) -> str:
        """Generate payload data string."""
        result = [self.__prefix__]
        for key, value in self.model_dump().items():
            encoded = self._encode_value(key, value)
            if self.__separator__ in encoded:
                msg = (
                    f"Separator symbol {self.__separator__!r} can not be used "
                    f"in value {key}={encoded!r}"
                )
                raise ValueError(msg)
            result.append(encoded)
        payload = self.__separator__.join(result)
        if len(payload.encode()) > self.MAX_PAYLOAD_LENGTH:
            msg = (
                f"Resulted payload data is too long! "
                f"len({payload!r}.encode()) > {self.MAX_PAYLOAD_LENGTH}"
            )
            raise ValueError(msg)
        return payload

    @staticmethod
    def _check_field_is_nullable(field: "FieldInfo") -> bool:
        """Check if the given field is nullable."""
        if not field.is_required():
            return True

        return get_origin(field.annotation) in (
            Union,
            UnionType,
        ) and NoneType in get_args(field.annotation)

    @classmethod
    def unpack(cls: type["Self"], value: str) -> "Self":
        """Parse payload data string."""
        prefix, *parts = value.split(cls.__separator__)
        names = cls.model_fields.keys()
        if len(parts) != len(names):
            msg = (
                f"Payload data {cls.__name__!r} takes {len(names)} arguments "
                f"but {len(parts)} were given"
            )
            raise TypeError(msg)
        if prefix != cls.__prefix__:
            msg = f"Bad prefix ({prefix!r} != {cls.__prefix__!r})"
            raise ValueError(msg)
        payload = {}
        for k, v in zip(names, parts, strict=False):
            field = cls.model_fields[k]
            val: str | None = v
            if (
                v == ""
                and cls._check_field_is_nullable(field)
                and field.default != ""
            ):
                val = (
                    field.default
                    if field.default is not PydanticUndefined
                    else None
                )
            payload[k] = val
        return cls(**payload)

    @classmethod
    def filter(cls, rule: MagicFilter | None = None) -> "PayloadDataFilter":
        """
        Generate a filter for payload with rule.

        :param rule: magic rule
        """
        return PayloadDataFilter(cls, rule)


class PayloadDataFilter:
    """Payload data filter."""

    def __init__(
        self,
        payload_data: type[PayloadData],
        rule: MagicFilter | None = None,
    ) -> None:
        self.payload_data = payload_data
        self.rule = rule

    async def __call__(
        self,
        invoice: Invoice,
    ) -> bool | dict[str, object]:
        if not isinstance(invoice, Invoice) or not invoice.payload:
            return False
        try:
            payload_data = self.payload_data.unpack(invoice.payload)
        except (TypeError, ValueError):
            return False

        if self.rule is None or self.rule.resolve(payload_data):
            return {"payload_data": payload_data}
        return False
