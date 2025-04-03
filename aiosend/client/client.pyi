from builtins import bool as _bool
from builtins import float as _float
from builtins import list as _list
from builtins import str as _str
from collections.abc import Awaitable, Callable, Generator
from datetime import datetime
from logging import Logger
from types import NoneType as _NoneType
from typing import Any, TypeVar

from typing_extensions import Self

from aiosend._handler import CallbackType, HandlerObject
from aiosend._methods import CryptoPayMethod
from aiosend.client import Network
from aiosend.enums import (
    Asset,
    CheckStatus,
    CurrencyType,
    Fiat,
    InvoiceStatus,
    LiteralAsset,
    LiteralCheckStatus,
    LiteralCurrencyType,
    LiteralFiat,
    LiteralInvoiceStatus,
    LiteralPaidBtnName,
    PaidBtnName,
)
from aiosend.polling import PollingConfig
from aiosend.polling.base import PollingTask
from aiosend.types import (
    App,
    AppStats,
    Balance,
    Check,
    Currency,
    ExchangeRate,
    Invoice,
    Transfer,
    _CryptoPayType,
)
from aiosend.webhook import (
    _APP,
    WebhookManager,
)

from .session import BaseSession

_T = TypeVar("_T")

# These classes are needed for synchronous type hinting.
# Stub file annotates the methods as synchronous, but
# while using this lib asynchronously, the actual return type
# is a coroutine that returns an annotated type, so these classes
# will annotate awaited object as return type.

class list(_list[_T]):  # noqa: A001, N801
    def __await__(self) -> Generator[None, None, Self]: ...

class bool(_bool):  # type: ignore[misc]  # noqa: A001, N801
    def __await__(self) -> Generator[None, None, Self]: ...

class str(_str):  # noqa: A001, N801
    def __await__(self) -> Generator[None, None, Self]: ...

class float(_float):  # noqa: A001, N801
    def __await__(self) -> Generator[None, None, Self]: ...

class NoneType(_NoneType):  # type: ignore[misc, valid-type]
    def __await__(self) -> Generator[None, None, None]: ...

class CryptoPay:
    _token: _str
    session: BaseSession
    _webhook_manager: WebhookManager
    _webhook_handlers: list[HandlerObject]
    _timeout: int
    _delay: int
    _check_tasks: dict[int, PollingTask[Check]]
    _invoice_tasks: dict[int, PollingTask[Invoice]]
    _check_handlers: list[HandlerObject]
    _invoice_handlers: list[HandlerObject]
    _exp_check_handlers: list[HandlerObject]
    _exp_invoice_handlers: list[HandlerObject]
    _kwargs: dict[_str, Any]

    def __init__(
        self,
        token: _str,
        network: Network = ...,
        session: type[BaseSession] = ...,
        webhook_manager: WebhookManager[_APP] | None = None,
        polling_config: PollingConfig | None = None,
        **kwargs: object,
    ) -> None: ...
    async def __call__(
        self,
        method: CryptoPayMethod[_CryptoPayType],
    ) -> _CryptoPayType: ...
    def get_me(self) -> App: ...
    def create_invoice(
        self,
        amount: _float,
        asset: Asset | LiteralAsset | _str | None = None,
        *,
        currency_type: CurrencyType | LiteralCurrencyType | _str | None = None,
        fiat: Fiat | LiteralFiat | _str | None = None,
        accepted_assets: _list[Asset | LiteralAsset | _str] | None = None,
        description: _str | None = None,
        hidden_message: _str | None = None,
        paid_btn_name: PaidBtnName | LiteralPaidBtnName | _str | None = None,
        paid_btn_url: _str | None = None,
        payload: _str | None = None,
        allow_comments: bool | None = None,
        allow_anonymous: bool | None = None,
        expires_in: int | None = None,
    ) -> Invoice: ...
    def delete_invoice(
        self,
        invoice_id: int,
    ) -> bool: ...
    def create_check(
        self,
        amount: _float,
        asset: Asset | LiteralAsset | _str,
        pin_to_user_id: int | None = None,
        pin_to_username: _str | None = None,
    ) -> Check: ...
    def delete_check(
        self,
        check_id: int,
    ) -> bool: ...
    def transfer(
        self,
        user_id: int,
        asset: Asset | LiteralAsset | _str,
        amount: _float,
        spend_id: _str | None = None,
        comment: _str | None = None,
        disable_send_notification: bool | None = None,
    ) -> Transfer: ...
    def get_invoices(
        self,
        asset: Asset | LiteralAsset | _str | None = None,
        fiat: Fiat | LiteralFiat | _str | None = None,
        invoice_ids: _list[int] | None = None,
        status: InvoiceStatus | LiteralInvoiceStatus | _str | None = None,
        offset: int | None = None,
        count: int | None = None,
    ) -> list[Invoice]: ...
    def get_checks(
        self,
        asset: Asset | LiteralAsset | _str | None = None,
        check_ids: _list[int] | None = None,
        status: CheckStatus | LiteralCheckStatus | _str | None = None,
        offset: int | None = None,
        count: int | None = None,
    ) -> list[Check]: ...
    def get_transfers(
        self,
        asset: Asset | LiteralAsset | _str | None = None,
        transfer_ids: _list[int] | None = None,
        spend_id: _str | None = None,
        offset: int | None = None,
        count: int | None = None,
    ) -> list[Transfer]: ...
    def get_balance(self) -> list[Balance]: ...
    def get_exchange_rates(self) -> list[ExchangeRate]: ...
    def get_currencies(self) -> list[Currency]: ...
    def get_stats(
        self,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
    ) -> AppStats: ...
    def delete_all_checks(self) -> NoneType: ...
    def delete_all_invoices(self) -> NoneType: ...
    def exchange(
        self,
        amount: _float,
        source: Asset | LiteralAsset | Fiat | LiteralFiat | _str,
        target: Asset | LiteralAsset | Fiat | LiteralFiat | _str,
    ) -> float: ...
    def get_balance_by_asset(
        self,
        asset: Asset | LiteralAsset | _str,
    ) -> Balance: ...
    def invoice_polling(
        self,
        *filters: CallbackType,
    ) -> Callable[[CallbackType], CallbackType]: ...
    def expired_invoice_polling(
        self,
        *filters: CallbackType,
    ) -> Callable[[CallbackType], CallbackType]: ...
    def check_polling(
        self,
        *filters: CallbackType,
    ) -> Callable[[CallbackType], CallbackType]: ...
    def expired_check_polling(
        self,
        *filters: CallbackType,
    ) -> Callable[[CallbackType], CallbackType]: ...
    def webhook(
        self,
        *filters: CallbackType,
    ) -> Callable[[CallbackType], CallbackType]: ...
    def feed_update(
        self,
        body: dict[_str, Any],
        headers: dict[_str, _str],
    ) -> NoneType: ...
    def _handle_invoice(self, invoice: Invoice) -> NoneType: ...
    def _handle_check(self, invoice: Check) -> NoneType: ...
    def _poll_invoice(
        self,
        invoice: Invoice,
        data: dict[_str, Any],
    ) -> None: ...
    def _poll_check(
        self,
        invoice: Check,
        data: dict[_str, Any],
    ) -> None: ...
    def _start_polling(
        self,
        get_updates: Callable[..., Awaitable[_list[object]]],
        handle_update: Callable[[object], Awaitable[None]],
        tasks: dict[int, PollingTask],
        updater_key: _str,
        logger: Logger,
    ) -> NoneType: ...
    def _start_invoice_polling(self) -> NoneType: ...
    def _start_check_polling(self) -> NoneType: ...
    def start_polling(
        self,
        parallel: Callable[[], Any] | None = None,
    ) -> NoneType: ...
    def get_invoice(
        self,
        invoice: int | Invoice,
    ) -> Invoice | NoneType: ...
    def get_check(
        self,
        check: int | Check,
    ) -> Check | NoneType: ...
    def get_rates_image(
        self,
        base: Asset | LiteralAsset | Fiat | LiteralFiat | _str,
        quote: Asset | LiteralAsset | Fiat | LiteralFiat | _str,
        rate: _float,
        percent: _float,
    ) -> _str: ...
    def __setitem__(self, key: _str, value: object) -> None: ...
    def __getitem__(self, key: _str) -> object: ...
    def __delitem__(self, key: _str) -> None: ...
    def __contains__(self, key: _str) -> _bool: ...
