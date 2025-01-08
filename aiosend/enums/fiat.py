from enum import Enum
from typing import Literal


class Fiat(str, Enum):
    """Fiat currency code."""

    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"
    BYN = "BYN"
    UAH = "UAH"
    GBP = "GBP"
    CNY = "CNY"
    KZT = "KZT"
    UZS = "UZS"
    GEL = "GEL"
    TRY = "TRY"
    AMD = "AMD"
    THB = "THB"
    INR = "INR"
    BRL = "BRL"
    IDR = "IDR"
    AZN = "AZN"
    AED = "AED"
    PLN = "PLN"
    ILS = "ILS"
    KGS = "KGS"
    TJS = "TJS"


LiteralFiat = Literal[
    "USD",
    "EUR",
    "RUB",
    "BYN",
    "UAH",
    "GBP",
    "CNY",
    "KZT",
    "UZS",
    "GEL",
    "TRY",
    "AMD",
    "THB",
    "INR",
    "BRL",
    "IDR",
    "AZN",
    "AED",
    "PLN",
    "ILS",
    "KGS",
    "TJS",
]
