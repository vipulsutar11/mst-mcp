# pyrefly: ignore [missing-import]
from web3 import Web3

from config import RPC_URL, WALLET_ADDRESS


web3 = Web3(Web3.HTTPProvider(RPC_URL))


if not web3.is_connected():
    raise ConnectionError("Could not connect to blockchain RPC")


wallet_address = Web3.to_checksum_address(WALLET_ADDRESS)


def get_wallet_address():
    return wallet_address


def get_wallet_balance():
    balance_wei = web3.eth.get_balance(wallet_address)

    balance_eth = web3.from_wei(
        balance_wei,
        "ether"
    )

    return float(balance_eth)


def get_transaction_count():
    count = web3.eth.get_transaction_count(
        wallet_address
    )

    return count


def get_network_info():
    chain_id = web3.eth.chain_id

    return chain_id