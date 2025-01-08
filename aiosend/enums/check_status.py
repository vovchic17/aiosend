from enum import Enum
from typing import Literal


class CheckStatus(str, Enum):
    """Status of check."""

    ACTIVE = "active"
    ACTIVATED = "activated"


LiteralCheckStatus = Literal[
    "active",
    "activated",
]
