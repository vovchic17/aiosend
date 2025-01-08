from .base import CryptoPayObject


class App(CryptoPayObject):
    """
    App object.

    This object represents the `Crypto Pay` app.
    """

    app_id: int
    """Crypto Pay app id."""
    name: str
    """Crypto Pay app name."""
    payment_processing_bot_username: str
    """Telegram username of the payment processing bot."""
