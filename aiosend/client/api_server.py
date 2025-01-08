from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal

    from aiosend.enums import Asset, Fiat
    from aiosend.methods import CryptoPayMethod


@dataclass(frozen=True)
class APIServer:
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

    def get_image(
        self,
        asset: "Asset | str",
        asset_amount: float,
        fiat: "Fiat | str",
        fiat_amount: float,
        main: "Literal['asset', 'fiat']",
    ) -> str:
        """Return check image url."""
        return (
            "https://imggen.send.tg/checks/image?"
            f"asset={asset}"
            f"&asset_amount={asset_amount}"
            f"&fiat={fiat}"
            f"&fiat_amount={fiat_amount}"
            f"&main={main}"
        )


MAINNET = APIServer(
    name="MAINNET",
    base="https://pay.crypt.bot/api/{method}",
)
TESTNET = APIServer(
    name="TESTNET",
    base="https://testnet-pay.crypt.bot/api/{method}",
)