from aiosend.enums import Asset, Fiat

from .base import CryptoPayObject


class ExchangeRate(CryptoPayObject):
    """
    ExchangeRate object.

    Source: https://help.crypt.bot/crypto-pay-api#ExchangeRate
    """

    is_valid: bool
    """True, if the received rate is up-to-date."""
    is_crypto: bool
    """True, if the source is the cryptocurrency."""
    is_fiat: bool
    """True, if the source is the fiat currency."""
    source: Asset | Fiat | str
    """Currency alphabetic code. Currently, can be “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC”."""
    target: Fiat | str
    """Fiat currency code. Currently, can be “USD”, “EUR”, “RUB”, “BYN”, “UAH”, “GBP”, “CNY”, “KZT”, “UZS”, “GEL”, “TRY”, “AMD”, “THB”, “INR”, “BRL”, “IDR”, “AZN”, “AED”, “PLN” and “ILS"."""
    rate: float
    """The current rate of the source asset valued in the target currency."""
