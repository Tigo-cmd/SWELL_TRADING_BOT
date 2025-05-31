from web3 import Web3
import json
import time
from decimal import Decimal
import os
from dotenv import load_dotenv
load_dotenv()

# INFURA_KEY = os.getenv('INFURA_KEY')

# abi = json.loads('[{"inputs":[{"internalType":"address","name":"_receiver","type":"address"},{"internalType":"uint256","name":"_totalSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
# infura_url = f"https://mainnet.infura.io/v3/{INFURA_KEY}"
# w3 = Web3(Web3.HTTPProvider(infura_url))
# swellAdress = "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"
# SWELL = w3.to_checksum_address(swellAdress)
# print(w3.is_connected())
# contract = w3.eth.contract(address=swellAdress, abi=abi)

# print("Contract Name:", contract.functions.name().call())
# print("Contract totalsupply:", contract.functions.totalSupply().call())
# print("Contract Symbol:", contract.functions.symbol().call())
# print("Contract Decimals:", contract.functions.decimals().call())
# print("Contract Balance:", contract.functions.balanceOf().call())
# print("Contract Allowance:", contract.functions.allowance(adress, adress).call())
# print("Contract Address:", contract.address)

class SwellSwapper:
	def __init__(self):
			# Get Infura key and construct URL
			infura_key = os.getenv("INFURA_KEY")
			if not infura_key:
					raise ValueError("INFURA_KEY not found in environment variables")
					
			infura_url = f"https://mainnet.infura.io/v3/{infura_key}"
			self.w3 = Web3(Web3.HTTPProvider(infura_url))
			
			# Verify connection
			if not self.w3.is_connected():
					raise ConnectionError("Failed to connect to Ethereum network")

			# Initialize contract addresses
			self.SWELL = Web3.to_checksum_address("0x0a6E7Ba5042B38349e437ec6Db6214AEC7B35676")
			# self.USDT = Web3.to_checksum_address("0xdAC17F958D2ee523a2206206994597C13D831ec7")
			self.UNISWAP_ROUTER = Web3.to_checksum_address("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")  # Updated to correct Uniswap V2 Router
			
			try:
					# Load router ABI
					with open("uniswap_abi.json", "r") as f:
							self.router_abi = json.load(f)
					
					# Load token ABI
					with open("swell_abi.json", "r") as f:
							self.token_abi = json.load(f)
			except FileNotFoundError as e:
					raise FileNotFoundError(f"ABI file not found: {str(e)}")
			
			# Initialize router contract
			self.router_contract = self.w3.eth.contract(
					address=self.UNISWAP_ROUTER, 
					abi=self.router_abi
			)
	async def check_swell_balance(self, address: str) -> Decimal:
			"""
			Check SWELL token balance for a given address
			Returns balance in SWELL
			"""
			try:
					# Create contract instance for SWELL token
					swell_contract = self.w3.eth.contract(
							address=self.SWELL,
							abi=self.token_abi  # Make sure to load SWELL token ABI
					)
					
					# Get balance in Wei
					balance_wei = swell_contract.functions.balanceOf(address).call()
					
					# Get token decimals
					decimals = swell_contract.functions.decimals().call()
					
					# Convert to decimal
					balance = Decimal(balance_wei) / Decimal(10 ** decimals)
					
					return balance

			except Exception as e:
					raise Exception(f"Failed to check balance: {str(e)}")
	async def check_allowance(self, owner_address: str) -> Decimal:
		"""
		Check if SWELL tokens are approved for trading on Uniswap
		"""
		try:
				swell_contract = self.w3.eth.contract(
						address=self.SWELL,
						abi=self.token_abi
				)
				
				allowance = swell_contract.functions.allowance(
						owner_address,
						self.UNISWAP_ROUTER
				).call()
				
				decimals = swell_contract.functions.decimals().call()
				return Decimal(allowance) / Decimal(10 ** decimals)

		except Exception as e:
				raise Exception(f"Failed to check allowance: {str(e)}")

	async def approve_tokens(self, wallet_address: str, private_key: str, amount: Decimal) -> str:
		"""
		Approve SWELL tokens for trading on Uniswap
		"""
		try:
				swell_contract = self.w3.eth.contract(
						address=self.SWELL,
						abi=self.token_abi
				)
				
				# Convert amount to Wei
				decimals = swell_contract.functions.decimals().call()
				amount_wei = int(amount * Decimal(10 ** decimals))
				
				# Build approval transaction
				tx = swell_contract.functions.approve(
						self.UNISWAP_ROUTER,
						amount_wei
				).build_transaction({
						"from": wallet_address,
						"nonce": self.w3.eth.get_transaction_count(wallet_address),
						"gas": 100000,
						"gasPrice": self.w3.to_wei("20", "gwei"),
				})
				
				# Sign and send transaction
				signed = self.w3.eth.account.sign_transaction(tx, private_key)
				tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
				
				return tx_hash.hex()

		except Exception as e:
				raise Exception(f"Failed to approve tokens: {str(e)}")
	
	async def get_token_info(self, token_address: str) -> dict:
		"""
		fetch and analyze token information from the blockchain
		"""
		try:
			token_address = Web3.to_checksum_adresss(token_address)
			token_contract = self.w3.eth.contract(
				address=token_address,
				abi=self.token_abi
			)
			# Fetch token details
			symbol = token_contract.functions.symbol().call()
			decimals = token_contract.functions.decimals().call()
			total_supply = token_contract.functions.totalSupply().call()
			            # Get pool information from Uniswap
			factory = self.w3.eth.contract(
					address="0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",  # Uniswap V2 Factory
					abi=self.factory_abi
			)
			
			pool_address = factory.functions.getPair(token_address, self.SWELL).call()
			pool_contract = self.w3.eth.contract(
					address=pool_address,
					abi=self.pair_abi
			)

			# Get reserves
			reserves = pool_contract.functions.getReserves().call()
			token0 = pool_contract.functions.token0().call()
			
			# Calculate pool metrics
			if token0.lower() == token_address.lower():
					token_reserves = reserves[0]
					swell_reserves = reserves[1]
			else:
					token_reserves = reserves[1]
					swell_reserves = reserves[0]

			# Calculate prices and ratios
			swell_price = await self.get_swell_price()  # Implement this method to get SWELL/USD price
			token_price = (swell_reserves / token_reserves) * swell_price
			market_cap = (total_supply / (10 ** decimals)) * token_price
			liquidity = (swell_reserves / (10 ** 18)) * swell_price * 2  # multiply by 2 for both sides of pool
			swell_ratio = token_reserves / swell_reserves

			# Calculate price impact for 1 SWELL
			price_impact = await self.calculate_price_impact(token_address, Web3.to_wei(1, 'ether'))

			return {
					"symbol": symbol,
					"address": token_address,
					"launch_date": "N/A",  # Would need external API for this
					"exchange": "Uniswap V2",
					"market_cap": market_cap,
					"liquidity": liquidity,
					"price": token_price,
					"pooled_swell": swell_reserves / (10 ** 18),
					"renounced": await self.check_contract_renounced(token_address),
					"frozen": False,  # Would need specific contract analysis
					"revoked": False,  # Would need specific contract analysis
					"swell_ratio": swell_ratio,
					"price_impact": price_impact,
					"website": "N/A",  # Would need external API
					"documentation": "N/A"  # Would need external API
			}
		except Exception as e:
				raise Exception(f"Failed to fetch token info: {str(e)}")
	async def calculate_price_impact(self, token_address: str, amount_in: int) -> float:
					"""
					Calculate price impact for a given swap amount
					"""
					try:
							# Get amounts out
							amounts = self.router_contract.functions.getAmountsOut(
									amount_in,
									[self.SWELL, token_address]
							).call()

							# Calculate price impact
							price_impact = ((amounts[0] - amounts[1]) / amounts[0]) * 100
							return abs(price_impact)

					except Exception as e:
							raise Exception(f"Failed to calculate price impact: {str(e)}")

	async def execute_swap(
			self,
			token_address: str,
			wallet_address: str,
			private_key: str,
			amount_in: Decimal,
			slippage: Decimal = Decimal("0.5")
	) -> str:
			"""
			Execute token swap from SWELL to target token
			"""
			try:
					# Convert amount to Wei
					amount_in_wei = Web3.to_wei(amount_in, 'ether')

					# Check SWELL balance
					balance = await self.check_swell_balance(wallet_address)
					if balance < amount_in:
							raise Exception(f"Insufficient SWELL balance. Have: {balance}, Need: {amount_in}")

					# Check and handle allowance
					allowance = await self.check_allowance(wallet_address)
					if allowance < amount_in:
							await self.approve_tokens(wallet_address, private_key, amount_in)
							# Wait for approval to be mined
							time.sleep(15)

					# Get minimum amount out with slippage
					amounts = self.router_contract.functions.getAmountsOut(
							amount_in_wei,
							[self.SWELL, token_address]
					).call()
					min_amount_out = int(amounts[1] * (1 - (slippage / 100)))

					# Build swap transaction
					deadline = int(time.time()) + 300  # 5 minutes
					tx = self.router_contract.functions.swapExactTokensForTokens(
							amount_in_wei,
							min_amount_out,
							[self.SWELL, token_address],
							wallet_address,
							deadline
					).build_transaction({
							"from": wallet_address,
							"nonce": self.w3.eth.get_transaction_count(wallet_address),
							"gas": 200000,
							"gasPrice": self.w3.eth.get_gas_price(),
					})

					# Sign and send transaction
					signed = self.w3.eth.account.sign_transaction(tx, private_key)
					tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)

					return tx_hash.hex()

			except Exception as e:
					raise Exception(f"Swap failed: {str(e)}")

	async def check_contract_renounced(self, token_address: str) -> bool:
			"""
			Check if contract ownership is renounced
			"""
			try:
					token_contract = self.w3.eth.contract(
							address=token_address,
							abi=self.token_abi
					)
					
					# Try to call owner() function if it exists
					try:
							owner = token_contract.functions.owner().call()
							return owner == "0x0000000000000000000000000000000000000000"
					except:
							return False

			except Exception:
					return False

	async def get_swell_price(self) -> float:
			"""
			Get current SWELL price in USD
			"""
			try:
					# Get SWELL/USDT price from Uniswap
					amounts = self.router_contract.functions.getAmountsOut(
							Web3.to_wei(1, 'ether'),
							[self.SWELL, self.USDT]
					).call()
					
					return amounts[1] / (10 ** 6)  # USDT has 6 decimals

			except Exception as e:
					raise Exception(f"Failed to fetch SWELL price: {str(e)}")