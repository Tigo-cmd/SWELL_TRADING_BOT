from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from store_to_db import create_wallet_db, fetch_all_from_wallet, fetch_from_wallet, init_db, balance_check
from generate_wallet import generate_wallet


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None : 
    swell_price = "0.009683"  # Static for example — you could fetch this dynamically
    username = update.message.from_user.username
    if username:
        welcome_text = (
        f"Welcome @{username}\n"
        "🚀 SwellTradingBot: Your all-in-one toolkit for Swell trading 🪙\n\n"
        f"💰 SWELL Price: ${swell_price}\n\n"
        "🧱 Create your first wallet at /wallets\n"
        "[Website](https://swelltradingbot.vercel.app)| [Github](https://github.com/SwellTradingBot/) | [Twitter](https://x.com/swelltradingbot)"
    )
    else:
        welcome_text = (
            f"Welcome "
            "🚀 SwellTradingBot: Your all-in-one toolkit for Swell trading 🪙\n\n"
            f"💰 SWELL Price: ${swell_price}\n\n"
            "🧱 Create your first wallet at /wallets\n"
            "[Website](https://swelltradingbot.vercel.app)| [Github](https://github.com/SwellTradingBot/) | [Twitter](https://x.com/swelltradingbot)"
        )

    # Create a keyboard with buttons
    keyboard = [
        [InlineKeyboardButton("📈️Trade", callback_data='trade'),InlineKeyboardButton("💳️Wallets", callback_data='wallet')],
        [InlineKeyboardButton("👨‍🦱️Profile", callback_data='profile'),InlineKeyboardButton("♦️Trades", callback_data='trades')],
        [InlineKeyboardButton("🤑️Prices", callback_data='prices'),InlineKeyboardButton("🌟️Buysell", callback_data='buysell')],
        [InlineKeyboardButton("🛠️Settings", callback_data='settings')],
        [InlineKeyboardButton("ℹ️Help", callback_data='help')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        welcome_text, 
        reply_markup=reply_markup, 
        parse_mode="Markdown"
    )
    print("activated Start command...")


# Callback query handler
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    # Map callback data to functions or responses
    try:
        if query.data == "trade":
            await trade_command(update, context)
        elif query.data == "wallet":
            await CreateWallet_command(update, context)
        elif query.data == "profile":
            await profile_command(update, context)
        elif query.data == "trades":
            await Trades_command(update, context)
        elif query.data == "settings":
            await Settings_command(update, context)
        elif query.data == "help":
            await help_command(update, context)
            selected = update.callback_query
        elif query.data == "Generate_wallet":
            await wallet_callback_handler(update, context)
        elif query.data == "5_wallets":
            await wallet_callback_handler(update, context, 5)
            print("Wallet created and stored in the database.")
        elif query.data == "10_wallets":
            await wallet_callback_handler(update, context, 10)
            print("Wallet created and stored in the database.")
        elif query.data == "connect_wallet":
            await query.message.reply_text("Connect your wallet to the bot.")
        elif query.data == "reload_all":
            await query.message.reply_text("Reloading all wallets...")
            wallets = await fetch_all_from_wallet()
            for wallet in wallets:
                address = wallet['address']
                private_key = wallet['private_key']
                await query.message.reply_text(f"Address: {address}, Private Key: {private_key}")
        elif query.data == "transfer_all":
            await query.message.reply_text("Transferring all Swell to one wallet...")
            wallets = await fetch_all_from_wallet()
            for wallet in wallets:
                address = wallet['address']
                private_key = wallet['private_key']
                await query.message.reply_text(f"Address: {address}, Private Key: {private_key}")
        else:
            await query.message.reply_text("Unknown command. Please try again.")

    except Exception as e:
        print(f"Error handling callback: {e}")
        await query.message.reply_text("An error occurred while processing your request.")

async def wallet_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, num: int) -> None:
    await update.callback_query.message.reply_text("generating wallets...")
    if num:
        for _ in range(num):
            # Generate a new wallet
            # This is a placeholder for the actual wallet generation logic
            # You should replace this with your actual wallet generation code
            private_key, address = await generate_wallet()
            print(private_key, address)
            await update.callback_query.message.reply_text(f"address: {address}, private_key: {private_key} \n⚠️ do not disclose your key")
            await create_wallet_db(address, private_key, 0.0)
    else:
        private_key, address = await generate_wallet()
        print(private_key, address)
        await update.callback_query.message.reply_text(f"address: {address}, private_key: {private_key} \n⚠️ do not disclose your key")
        await create_wallet_db(address, private_key, 0.0)
        print("Wallet created and stored in the database.")
        print("Wallet created and stored in the database.")

# Price command
async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        symbol = context.args[0].upper()  # e.g., "BTC"
        ticker = exchange.fetch_ticker(f"{symbol}/USDT")
        price = ticker['last']
        update.message.reply_text(f"The price of {symbol} is ${price}")
    except Exception as e:
       await update.message.reply_text(f"Error: {str(e)}")

# Trade command (example: buy order)
async def trade_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.message.reply_text("I'm Here To Help")
    elif update.message:
        await update.message.reply_text("I'm Here To Help")

# function to handle the trades command
async def Trades_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.message.reply_text("I'm Here To Help")
    elif update.message:
        await update.message.reply_text("I'm Here To Help")


# function to handle the help reply
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
    "/start - Get started and Trade Swell confidently\n"
    "/wallet - Create a wallet and multiple wallets\n"
    "/profile - View your portfolio\n"
    "/trades - Monitor and Track your trades\n"
    "/buysell - Swap Tokens\n"
    "/settings - Set preferences and Automations, auto buy, auto sell, slippage\n"
    "/prices - Check prices on ecosystem\n"
    "/tip - Last tip levels\n"
    "/language - Select language\n"
    "/help - Tutorial & Help"
    )
    if update.callback_query:
        await update.callback_query.message.reply_text(help_text, parse_mode="Markdown")
    elif update.message:
        await update.message.reply_text(help_text, parse_mode="Markdown") 

# function to handle the buysell reply
async def Buysell_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.message.reply_text("I'm Here To Help")
    elif update.message:
        await update.message.reply_text("I'm Here To Help")

# function to handle the settings reply
async def Settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # function to handle the help reply
        pass





# function to handle the wallet reply
async def CreateWallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # message = "\nwallets"
    wallets = fetch_all_from_wallet()
    wallet_address = [] # list to store the wallet address in and append to the message if the wallet exists
    num = 1
    if wallets:
        for wallet in wallets:
            balance = balance_check(wallet["address"])
            wallet_address.append(
                [InlineKeyboardButton(wallet[f"{num}. address"], callback_data=wallet["address"]), 
                InlineKeyboardButton(balance, callback_data="balance")]
            )
            num += 1
    keyboard = [
        [InlineKeyboardButton("➕️ Connect Wallet", callback_data='connect_wallet'), InlineKeyboardButton("➕️ Generate New Wallet", callback_data='Generate_wallet')],
        [InlineKeyboardButton("➕️ Generate 5 Wallets", callback_data='5_wallets'), InlineKeyboardButton("➕️ Generate 10 Wallets", callback_data='10_wallets')],
        [InlineKeyboardButton("➕️ Transfer all Swell To One", callback_data='transfer_all')],
        [InlineKeyboardButton("🔃️ Reload All", callback_data='reload_all')],
    ]
     # Combine wallet buttons and keyboard buttons
    updated_markup = wallet_address + keyboard
    reply_markup = InlineKeyboardMarkup(updated_markup)
    if update.callback_query:
        await update.callback_query.message.reply_text(
            "wallets",
            reply_markup=updated_markup,
            parse_mode="Markdown",
            )
    elif update.message:
        await update.message.reply_text(
            message,
            reply_markup=updated_markup,
            parse_mode="Markdown",
            )


async def error(update: Update, Context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Update {update} caused error {Context.error}")



# function to handle the tip reply
async def tip_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.message.reply_text("I'm Here To Help")
    elif update.message:
        await update.message.reply_text("I'm Here To Help")


# function to handle the profile reply
async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.message.reply_text("I'm Here To Help")
    elif update.message:
        await update.message.reply_text("I'm Here To Help")
