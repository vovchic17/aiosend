from datetime import datetime

from .base import CryptoPayObject


class AppStats(CryptoPayObject):
    """
    AppStats object.

    Source: http://help.crypt.bot/crypto-pay-api#wnPA
    """

    volume: float
    """Total volume of paid invoices in USD."""
    conversion: float
    """Conversion of all created invoices."""
    unique_users_count: int
    """The unique number of users who have paid the invoice."""
    created_invoice_count: int
    """Total created invoice count."""
    paid_invoice_count: int
    """Total paid invoice count."""
    start_at: datetime
    """The date on which the statistics calculation was started in ISO 8601 format."""
    end_at: datetime
    """The date on which the statistics calculation was ended in ISO 8601 format."""
