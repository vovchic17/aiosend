from datetime import datetime

from aiosend.enums import UpdateType

from .base import CryptoPayObject
from .invoice import Invoice


class Update(CryptoPayObject):
    """
    Update object.

    Source: https://help.crypt.bot/crypto-pay-api#webhook-updates
    """

    update_id: int
    update_type: UpdateType
    request_date: datetime
    payload: Invoice
