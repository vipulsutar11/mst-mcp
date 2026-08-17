from blockchain import (
    get_wallet_address,
    get_wallet_balance,
    get_transaction_count,
    get_network_info
)
from config import CURRENCY_SYMBOL


print("=" * 50)

print("Wallet Address:")
print(get_wallet_address())

print("\nWallet Balance:")
print(get_wallet_balance(), CURRENCY_SYMBOL)

print("\nTransaction Count:")
print(get_transaction_count())

print("\nChain ID:")
print(get_network_info())

print("=" * 50)