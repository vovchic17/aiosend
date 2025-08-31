from aiosend import PollingRouter
from aiosend.types import Invoice

router = PollingRouter(name=__name__)

@router.invoice_paid()
def invoice_paid(invoice: Invoice) -> None:
    print(f"invoice_paid: {invoice.invoice_id}")
