from enum import Enum
from typing import Literal


class UpdateType(str, Enum):
    """Webhook update type."""

    INVOICE_PAID = "invoice_paid"


LiteralUpdateType = Literal["invoice_paid"]
