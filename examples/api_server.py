from aiosend import MAINNET, TESTNET, CryptoPay

main_client = CryptoPay(
    "TOKEN",
    MAINNET,  # MAINNET is default
)

test_client = CryptoPay(
    "TOKEN",
    TESTNET,
)
