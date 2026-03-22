from datetime import datetime

from aiosend.enums import UpdateType

from .base import CryptoPayObject
from .invoice import Invoice


class Update(CryptoPayObject):
    """
    Update object.

    Source: https://help.send.tg/en/articles/10279948-crypto-pay-api#h_20aded801d
    """

    update_id: int
    """Non-unique update ID."""
    update_type: UpdateType
    """Webhook update type. Supported update types: `invoice_paid` - the update sent when the invoice is paid."""
    request_date: datetime
    """Date the request was sent in ISO 8601 format."""
    payload: Invoice
    """Payload contains the class Invoice."""
