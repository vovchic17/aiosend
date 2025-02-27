from enum import Enum
from typing import Literal


class Asset(str, Enum):
    """Cryptocurrency alphabetic code."""

    USDT = "USDT"
    TON = "TON"
    SOL = "SOL"
    GRAM = "GRAM"
    NOT = "NOT"
    HMSTR = "HMSTR"
    CATI = "CATI"
    MY = "MY"
    DOGS = "DOGS"
    BTC = "BTC"
    LTC = "LTC"
    ETH = "ETH"
    BNB = "BNB"
    TRX = "TRX"
    USDC = "USDC"
    JET = "JET"
    SEND = "SEND"
    PEPE = "PEPE"
    WIF = "WIF"
    BONK = "BONK"
    MAJOR = "MAJOR"
    TRUMP = "TRUMP"
    MELANIA = "MELANIA"
    MEMHASH = "MEMHASH"


LiteralAsset = Literal[
    "USDT",
    "TON",
    "SOL",
    "GRAM",
    "NOT",
    "HMSTR",
    "CATI",
    "MY",
    "DOGS",
    "BTC",
    "LTC",
    "ETH",
    "BNB",
    "TRX",
    "USDC",
    "JET",
    "SEND",
    "PEPE",
    "WIF",
    "BONK",
    "MAJOR",
    "TRUMP",
    "MELANIA",
    "MEMHASH",
]
