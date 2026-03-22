from datetime import datetime
from typing import Literal

from aiosend.enums import Asset

from .base import CryptoPayObject


class Transfer(CryptoPayObject):
    """
    Transfer object.

    Source: https://help.send.tg/en/articles/10279948-crypto-pay-api#h_771b6213d1
    """

    transfer_id: int
    """Unique ID for this transfer."""
    spend_id: str | None = None # not returned by API on /transfer
    """Unique UTF-8 string."""
    user_id: int
    """Telegram user ID the transfer was sent to."""
    asset: Asset | str
    """Cryptocurrency alphabetic code. Currently, can be “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet)."""
    amount: float
    """Amount of the transfer in float."""
    status: Literal["completed"]
    """Status of the transfer, can only be “completed”."""
    completed_at: datetime
    """Date the transfer was completed in ISO 8601 format."""
    comment: str | None = None
    """*Optional*. Comment for this transfer."""
