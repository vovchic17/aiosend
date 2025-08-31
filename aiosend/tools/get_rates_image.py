from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiosend._typing import SessionNetworkProtocol
    from aiosend.enums import Asset, Fiat


class GetRatesImage:
    """Get rates image."""

    def get_rates_image(
        self: "SessionNetworkProtocol",
        base: "Asset | Fiat | str",
        quote: "Asset | Fiat | str",
        rate: float,
        percent: float,
    ) -> str:
        """
        Get rates image.

        Use this method to get exchange rates image.

        :return: rates image url.
        """
        return self.session.network.get_rates_image(
            base,
            quote,
            rate,
            percent,
        )
