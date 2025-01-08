from enum import Enum
from typing import Literal


class CurrencyType(str, Enum):
    """Type of currency."""

    CRYPTO = "crypto"
    FIAT = "fiat"


LiteralCurrencyType = Literal[
    "crypto",
    "fiat",
]
