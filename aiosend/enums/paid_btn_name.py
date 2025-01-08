from enum import Enum
from typing import Literal


class PaidBtnName(str, Enum):
    """
    Paid button name.

    Label of the button which will be presented
    to a user after the invoice is paid.
    """

    VIEWITEM = "viewItem"
    OPENCHANNEL = "openChannel"
    OPENBOT = "openBot"
    CALLBACK = "callback"


LiteralPaidBtnName = Literal[
    "viewItem",
    "openChannel",
    "openBot",
    "callback",
]
