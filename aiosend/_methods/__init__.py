from .base import CryptoPayMethod
from .create_check import CreateCheck
from .create_invoice import CreateInvoice
from .delete_check import DeleteCheck
from .delete_invoice import DeleteInvoice
from .get_balance import GetBalance
from .get_checks import GetChecks
from .get_currencies import GetCurrencies
from .get_exchange_rates import GetExchangeRates
from .get_invoices import GetInvoices
from .get_me import GetMe
from .get_stats import GetStats
from .get_transfers import GetTransfers
from .transfer import Transfer


class Methods(
    CreateCheck,
    CreateInvoice,
    DeleteCheck,
    DeleteInvoice,
    GetBalance,
    GetChecks,
    GetCurrencies,
    GetExchangeRates,
    GetInvoices,
    GetMe,
    GetStats,
    GetTransfers,
    Transfer,
):
    pass


__all__ = (
    "CreateCheck",
    "CreateInvoice",
    "CryptoPayMethod",
    "DeleteCheck",
    "DeleteInvoice",
    "GetBalance",
    "GetChecks",
    "GetCurrencies",
    "GetExchangeRates",
    "GetInvoices",
    "GetMe",
    "GetStats",
    "GetTransfers",
    "Transfer",
)
