# from web3 import Web3
# import secrets

# private_key = secrets.token_hex(32)
# w3 = Web3(Web3.HTTPProvider("https:///v3/5460cf9251af48b1bd909965c50c9adf/"))

# account = w3.eth.account.from_key(private_key)
# address = account.address
# print(f"Private Key: {private_key}")
# print(f"Address: {address}")





import requests
import json
 
url = "https://swellchain-mainnet.infura.io/v3/5460cf9251af48b1bd909965c50c9adf"
payload = {
  "jsonrpc": "2.0",
  "method": "eth_blockNumber",
  "params": [],
  "id": 1
}
headers = {"content-type": "application/json"}
 
response = requests.post(url, data=json.dumps(payload), headers=headers).json()
print(response)