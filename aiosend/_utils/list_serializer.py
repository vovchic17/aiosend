from enum import Enum
from typing import TypeVar

T = TypeVar("T")


def serialize_list(value: list[T] | None) -> str | None:
    """
    List of objects serialization.

    Serialize a list of objects into a
    string of objects separated by commas.
    """
    if value is not None:
        return ",".join(
            [x.value if isinstance(x, Enum) else str(x) for x in value],
        )
    return value
