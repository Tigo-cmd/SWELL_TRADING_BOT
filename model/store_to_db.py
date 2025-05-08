import sqlite3


# Create a SQLite database and a table to store wallet information
# This code creates a SQLite database and a table to store wallet information if it doesn't already exist.




async def init_db() -> None:
  """
  Initialize the SQLite database and create the wallets table if it doesn't exist.
  """
  # Connect to the SQLite database (or create it if it doesn't exist)
  # Connect to the SQLite database (or create it if it doesn't exist)
  # The database file will be named 'wallet.db'
  # and will be created in the current working directory.
  # The connection object is used to interact with the database.
  # The cursor object is used to execute SQL commands.  
  conn = sqlite3.connect('wallet.db')
  cursor = conn.cursor()
  cursor.execute('''
  CREATE TABLE IF NOT EXISTS wallets (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      address TEXT UNIQUE NOT NULL,
      private_key TEXT UNIQUE NOT NULL,
      balance REAL NOT NULL
  )''')
  conn.commit()  # Save changes
  conn.close()
  # The database file will be named 'wallet.db'
  # and will be created in the current working directory.
  # The connection object is used to interact with the database.

  # The cursor object is used to execute SQL commands.
  # The commit() method is used to save changes to the database.
  # The close() method is used to close the connection to the database.
async def create_wallet_db(address: str, private_key: str, balance: float) -> None:
  """
  Create a SQLite database and a table to store wallet information.
  """
  conn = sqlite3.connect('wallet.db')
  cursor = conn.cursor()
  # Create the wallets table if it doesn't exist  
  # Insert data (securely)
  cursor.execute("INSERT INTO wallets (address, private_key) VALUES (?, ?)", 
                (address, private_key))
  conn.commit()  # Save changes
  conn.close()


async def fetch_from_wallet(address, private_key):

  conn = sqlite3.connect('wallet.db')
  cursor = conn.cursor()
  cursor.execute("SELECT private_key FROM wallets WHERE address = ?", (address,))
  result = cursor.fetchone()  # Returns (private_key,) or None

  cusor.execute("SELECT address FROM wallets WHERE private_key = ?", (private_key,))
  result2 = cursor.fetchone()

  if (result, result2):
     return (result, result2)
  else:
      return "Wallet not found."


async def fetch_all_from_wallet():
  """
  fetches the address and private keys
  """
  conn = sqlite3.connect('wallet.db')
  cursor = conn.cursor()

  cursor.execute("SELECT address, private_key FROM wallets")
  wallets = cursor.fetchall()  # Returns list of tuples: [(address, private_key), ...]

  for address, private_key in wallets:
    yield {"address": address, "private_key": private_key}

  conn.close()
