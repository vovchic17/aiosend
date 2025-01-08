from enum import Enum
from typing import Literal


class InvoiceStatus(str, Enum):
    """Status of invoice."""

    ACTIVE = "active"
    PAID = "paid"
    EXPIRED = "expired"


LiteralInvoiceStatus = Literal[
    "active",
    "paid",
    "expired",
]
