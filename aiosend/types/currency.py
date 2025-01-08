from aiosend.enums import Asset, Fiat

from .base import CryptoPayObject


class Currency(CryptoPayObject):
    """
    Currency object.

    This object represents an `Crypto Pay` currency.
    """

    is_blockchain: bool
    """True, if the currency is blockchain currency."""
    is_stablecoin: bool
    """True, if the currency is stablecoin."""
    is_fiat: bool
    """True, if the currency is fiat."""
    name: str
    """Currency name."""
    code: Fiat | Asset | str
    """Currency code."""
    url: str | None = None
    """Currency url."""
    decimals: int
    """Currency decimals."""
