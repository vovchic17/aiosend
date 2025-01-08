from aiosend.enums import Asset

from .base import CryptoPayObject


class Balance(CryptoPayObject):
    """
    Balance object.

    Source: https://help.crypt.bot/crypto-pay-api#Balance
    """

    currency_code: Asset | str
    """Cryptocurrency alphabetic code. Currently, can be “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet)."""
    available: float
    """Total available amount in float."""
    onhold: float
    """Unavailable amount currently is on hold in float."""
