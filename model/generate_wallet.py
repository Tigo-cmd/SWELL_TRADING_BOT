from web3 import Web3
import secrets


async def generate_wallet()->(str, str):
  # Generate a new Ethereum wallet

  w3 = Web3(Web3.HTTPProvider("https://swellchain-mainnet.infura.io/v3/5460cf9251af48b1bd909965c50c9adf/"))
  private_key = "0x" + secrets.token_hex(32)
  account = w3.eth.account.from_key(private_key)
  address = account.address
  
  return (private_key, address)