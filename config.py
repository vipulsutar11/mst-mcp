import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file using its absolute path relative to config.py
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

RPC_URL = os.getenv("RPC_URL")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
CURRENCY_SYMBOL = os.getenv("CURRENCY_SYMBOL", "MSTC")

if not RPC_URL:
    raise ValueError("RPC_URL is missing from .env")

if not WALLET_ADDRESS:
    raise ValueError("WALLET_ADDRESS is missing from .env")