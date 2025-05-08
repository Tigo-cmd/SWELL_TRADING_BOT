from web3 import Web3
import secrets
from dotenv import load_dotenv
import os
load_dotenv()
# Load environment variables

INFURA_KEY = os.getenv('INFURA_KEY')

async def generate_wallet()->(str, str):
  # Generate a new Ethereum wallet

  w3 = Web3(Web3.HTTPProvider(f"https://swellchain-mainnet.infura.io/v3/{INFURA_KEY}/"))
  private_key = "0x" + secrets.token_hex(32)
  account = w3.eth.account.from_key(private_key)
  address = account.address
  
  return (private_key, address)