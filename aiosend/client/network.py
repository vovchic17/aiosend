from dataclasses import dataclass
from typing import TYPE_CHECKING

from aiosend.enums import Asset, Fiat

if TYPE_CHECKING:
    from typing import Literal

    from aiosend._methods import CryptoPayMethod


@dataclass(frozen=True)
class Network:
    """Configuration for endpoints."""

    name: str
    """Net name"""
    base: str
    """Base URL"""

    def url(self, method: "CryptoPayMethod") -> str:
        """Return URL for method."""
        return self.base.format(method=method.__method__)

    def get_qr(self, link: str) -> str:
        """Return qr code link."""
        return f"https://qr.crypt.bot/?url={link}"

    def get_check_image(
        self,
        asset: "Asset | str",
        asset_amount: float,
        fiat: "Fiat | str",
        fiat_amount: float,
        main: "Literal['asset', 'fiat']",
    ) -> str:
        """Return check image url."""
        if isinstance(asset, Asset):
            asset = asset.value
        if isinstance(fiat, Fiat):
            fiat = fiat.value
        asset_amount = round(asset_amount, 3)
        fiat_amount = round(fiat_amount, 3)
        return (
            "https://imggen.send.tg/checks/image?"
            f"asset={asset}"
            f"&asset_amount={asset_amount}"
            f"&fiat={fiat}"
            f"&fiat_amount={fiat_amount}"
            f"&main={main}"
        )

    def get_rates_image(
        self,
        base: "Asset | Fiat | str",
        quote: "Asset | Fiat | str",
        rate: float,
        percent: float,
    ) -> str:
        """Return rates image url."""
        if isinstance(base, Asset | Fiat):
            base = base.value
        if isinstance(quote, Asset | Fiat):
            quote = quote.value
        return (
            "https://imggen.send.tg/rates/image?"
            f"base={base}"
            f"&quote={quote}"
            f"&rate={rate}"
            f"&percent={percent}"
        )


MAINNET = Network(
    name="MAINNET",
    base="https://pay.crypt.bot/api/{method}",
)
TESTNET = Network(
    name="TESTNET",
    base="https://testnet-pay.crypt.bot/api/{method}",
)
