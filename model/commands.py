from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from telegram.ext import ContextTypes
from utils import shorten_address
from store_to_db import (
    create_wallet_db, 
    fetch_all_from_wallet, 
    fetch_from_wallet, 
    init_db, 
    balance_check, 
    delete_wallets_by_user,
    delete_specific_wallet
    )
from api import get_swell_price
from telegram.helpers import escape_markdown
from generate_wallet import generate_wallet
import asyncio
from mainet import SwellSwapper
from web3 import Web3

swapper = SwellSwapper()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None : 
    swell_price = get_swell_price()
    swell_price = "{:,.6f}".format(swell_price)  # Format the price to 2 decimal places
    username = update.message.from_user.username
    if username:
        welcome_text = (
        f"Welcome @{username}\n"
        "🚀 SwellTradingBot: Your all-in-one toolkit for Swell trading 🪙\n\n"
        f"💰 SWELL Price: ${swell_price}\n\n"
        "🧱 Create your wallets at /wallets\n"
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
        [InlineKeyboardButton("📈️Trades", callback_data='trades'),InlineKeyboardButton("💳️Wallets", callback_data='wallet')],
        [InlineKeyboardButton("👨‍🦱️Profile", callback_data='profile')],
        [InlineKeyboardButton("🤑️Prices", callback_data='prices'),InlineKeyboardButton("🌟️Buysell", callback_data='buysell')],
        [InlineKeyboardButton("🛠️Settings", callback_data='settings')],
        [InlineKeyboardButton("ℹ️Help", callback_data='help')],
        [InlineKeyboardButton("❌ Close", callback_data="close")],
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
        if query.data == "return_":
            await query.message.delete()
            await CreateWallet_command(update, context)
                # In your button_callback function, add:
        elif query.data == 'enter_token_address':
            await query.message.reply_text(
                "📝 Please paste the token contract address:",
                reply_markup=ForceReply(selective=True)
            )
            context.user_data['awaiting_token_address'] = True
        
        elif query.data.startswith('buy_'):
            token_address = query.data.split('_')[1]
            # Fetch user's wallets
            user_id = update.effective_user.id
            wallets = fetch_all_from_wallet(user_id)
            
            if not wallets:
                await query.message.reply_text(
                    "❌ No wallets found. Please create a wallet first using /wallet"
                )
                return
            
            # Create wallet selection buttons
            wallet_buttons = []
            for wallet in wallets:
                short_address = shorten_address(wallet["address"])
                wallet_buttons.append([
                    InlineKeyboardButton(
                        f"💳 {short_address}",
                        callback_data=f"select_wallet_{wallet['address']}_{token_address}"
                    )
                ])
            
            wallet_buttons.append([InlineKeyboardButton("❌ Cancel", callback_data='buysell')])
            reply_markup = InlineKeyboardMarkup(wallet_buttons)
            
            await query.message.reply_text(
                "Select a wallet to trade with:",
                reply_markup=reply_markup
            )
        elif query.data == "wallet":
            await CreateWallet_command(update, context)
        elif query.data == "remove_all":
            await query.message.reply_text(
                "Are you sure you want to remove all wallets? Type *CONFIRM* to proceed.",
                reply_markup=ForceReply(selective=True),
                parse_mode="Markdown",
            )
            context.user_data["awaiting_confirmation"] = "remove_all"  # Set confirmation state
            # asyncio.sleep(5)  # Wait for 5 seconds before deleting the message
            # await confirmation_message.delete()  # Delete the confirmation message
        elif query.data == "profile":
            await profile_command(update, context)
        elif query.data.startswith("address_"):
            address = query.data.split("_", 1)[1]
            await address_handler(update, context, address)
        elif query.data == "trades":
            await Trades_command(update, context)
        elif query.data == "settings":
            await Settings_command(update, context)
        elif query.data == "help":
            await help_command(update, context)
            selected = update.callback_query
        elif query.data == "swap_tokens":
            await token_swap(update, context)
            await query.message.delete()
        elif query.data == "Generate_wallet":
            await wallet_callback_handler(update, context, 0)
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
        elif query.data == "close":
            await query.message.delete()
        elif query.data.startswith("delete"):
            await query.message.reply_text(
                "Are you sure you want to delete this wallet? Type *CONFIRM* to proceed.",
                reply_markup=ForceReply(selective=True),
                parse_mode="Markdown",
            )
            context.user_data["awaiting_confirmation"] = "delete"  # Set confirmation state
            address = query.data.split("_", 1)[1]
            await message_handler(update, context, address)
        else:
            await query.message.reply_text("Unknown command. Please try again.")


    except Exception as e:
        print(f"Error handling callback: {e}")
        await query.message.reply_text("An error occurred while processing your request.")


async def token_swap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        keyboard = [
            [InlineKeyboardButton("🔃️ SWELL/USDT", callback_data='swap_swell/usdt')],
        ]
    updated = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        "Select a token to swap:",
        reply_markup=updated,
        parse_mode="Markdown"
    )

async def address_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, addr:str) -> None:
    message = f"Address: {addr}\n"
    # Fetch the private key from the database
    Button = [
        [InlineKeyboardButton("✍️ Edit", callback_data='edit'), InlineKeyboardButton("🗑️ Delete", callback_data=f'delete{addr}')],
        [InlineKeyboardButton("🔃️ Transfer Swell", callback_data='reload_all'), InlineKeyboardButton(" Transfer to First 10 Wallets", callback_data="first_10")],
        [InlineKeyboardButton("🔃️ Transfer Token", callback_data='transfer_token')],
        [InlineKeyboardButton("🔃️ Return To Wallets", callback_data='return_')],
        [InlineKeyboardButton("❌ Close", callback_data="close")],
    ]

    reply_markup = InlineKeyboardMarkup(Button)

    await update.callback_query.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, addr:str = None) -> None:
    user_message = update.message.text.strip()  # Get the user's message
    print(user_message)
    user_id = update.effective_user.id
    # Check if the user is in a confirmation state
    if context.user_data.get("awaiting_confirmation") == "remove_all":
        if user_message.upper() == "CONFIRM":
            # Perform the remove_all action
            await delete_wallets_by_user(user_id)
            # await update.message.reply_text("All your wallets have been removed.")
            # Clear the confirmation state
            context.user_data["awaiting_confirmation"] = None
        else:
            await update.message.reply_text(
                "Action canceled. Type *CONFIRM* if you want to proceed.",
                parse_mode="Markdown",
            )
        await update.message.delete()  # Delete the message after confirmation
        await CreateWallet_command(update, context)
    elif context.user_data.get("awaiting_confirmation") == "delete":
        if user_message.upper() == "CONFIRM":
            # Perform the delete action
            await delete_specific_wallet(user_id, addr)
            # await update.message.reply_text("Your wallet has been deleted.")
            # Clear the confirmation state
            context.user_data["awaiting_confirmation"] = None
        else:
            await update.message.reply_text(
                "Action canceled. Type *CONFIRM* if you want to proceed.",
                parse_mode="Markdown",
            )
    elif context.user_data.get('awaiting_token_address'):
        if Web3.is_address(user_message):
            context.user_data['awaiting_token_address'] = False
            await analyze_token(update, context, user_message)
        else:
            await update.message.reply_text(
                "❌ Invalid token address. Please enter a valid contract address."
            )
        return

async def wallet_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, num: int) -> None:
    user_id = update.effective_user.id
    await update.callback_query.message.reply_text("generating wallets...")
    if num:
        for i in range(num):
            # Generate a new wallet
            # This is a placeholder for the actual wallet generation logic
            # You should replace this with your actual wallet generation code
            private_key, address = await generate_wallet()
            print(private_key, address)
            await create_wallet_db(user_id, address, private_key, 0.0)
            escaped_key = escape_markdown(private_key, version=2)
            await update.callback_query.message.reply_text(
                f"New Wallet Info: \nAddress: \n<code>{address}</code>  \nPrivate_key: \n<tg-spoiler>{escaped_key}</tg-spoiler> \n⚠️ do not disclose your key",
                parse_mode="HTML", # Use HTML to format the message
            )
    else:
        private_key, address = await generate_wallet()
        print(private_key, address)
        await create_wallet_db(user_id, address, private_key, 0.0)
        escaped_key = escape_markdown(private_key, version=2)
        await update.callback_query.message.reply_text(
            f"New Wallet Info: \nAddress: \n<code>{address}</code>  \nPrivate_key: \n<tg-spoiler>{escaped_key}</tg-spoiler> \n⚠️ do not disclose your key",
            parse_mode="HTML", # Use HTML to format the message
        )
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


# function to handle the trades command
async def Trades_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.message.reply_text("You Don't Have Any Transaction Yet")
    elif update.message:
        await update.message.reply_text("You Don't Have Any Transaction Yet")


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
    keyboard = [
        [InlineKeyboardButton("🔍 Enter Token Address", callback_data='enter_token_address')],
        [InlineKeyboardButton("🔃️ Swap Swell Tokens", callback_data='swap_tokens')],
        [InlineKeyboardButton("❌ Close", callback_data="close")]
    ]
    main = InlineKeyboardMarkup(keyboard)
    
    message = (
        "🪙 *Token Trading*\n\n"
        "1. Enter token contract address to analyze\n"
        "2. Review token information\n"
        "3. Select wallet and amount\n"
        "4. Confirm swap"
    )
    
    if update.callback_query:
        await update.callback_query.message.reply_text(
            message,
            reply_markup=main,
            parse_mode="Markdown"
        )
    elif update.message:
        await update.message.reply_text(
            message,
            reply_markup=main,
            parse_mode="Markdown"
        )
async def analyze_token(update: Update, context: ContextTypes.DEFAULT_TYPE, token_address: str) -> None:
    try:
        # Initialize SwellSwapper
        token_info = await swapper.get_token_info(token_address)
        
        # Format token information
        info_message = (
            f"*Token Information*\n\n"
            f"*Symbol:* {token_info['symbol']}\n"
            f"*Contract Address:* `{token_info['address']}`\n"
            f"*Launch Date:* {token_info['launch_date']}\n\n"
            f"*Exchange:* {token_info['exchange']}\n"
            f"*Market Cap:* ${token_info['market_cap']:,.2f}\n"
            f"*Liquidity:* ${token_info['liquidity']:,.2f}\n"
            f"*Token Price:* ${token_info['price']:,.8f}\n"
            f"*Pooled SWELL:* {token_info['pooled_swell']:,.2f}\n\n"
            f"*Security Info:*\n"
            f"- Renounced: {'✅' if token_info['renounced'] else '❌'}\n"
            f"- Frozen: {'❌' if token_info['frozen'] else '✅'}\n"
            f"- Revoked: {'❌' if token_info['revoked'] else '✅'}\n\n"
            f"*Swap Info:*\n"
            f"1 SWELL = {token_info['swell_ratio']} {token_info['symbol']}\n"
            f"Price Impact: {token_info['price_impact']}%\n\n"
            f"*Links:*\n"
            f"[Website]({token_info['website']}) | "
            f"[Documentation]({token_info['documentation']})"
        )
        
        # Create keyboard for buying options
        keyboard = [
            [InlineKeyboardButton("💰 Buy Token", callback_data=f'buy_{token_address}')],
            [InlineKeyboardButton("🔄 Refresh Info", callback_data=f'refresh_{token_address}')],
            [InlineKeyboardButton("❌ Cancel", callback_data='buysell')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            info_message,
            reply_markup=reply_markup,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ Error analyzing token: {str(e)}\n\n"
            "Please verify the contract address and try again.",
            parse_mode="Markdown"
        )
# function to handle the settings reply
async def Settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # function to handle the help reply
        pass

# function to handle the wallet reply
async def CreateWallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    # Check if the user has any wallets
    # If not, create a new wallet
    # If the user has wallets, fetch them from the database
    # and display them in the message
    message = "Wallets"
    wallets = fetch_all_from_wallet(user_id)
    wallet_address = [] # list to store the wallet address in and append to the message if the wallet exists
    num = 1
    if wallets:
        for wallet in wallets:
            balance = await check_balance_command(address=wallet["address"])
            wallet_address.append(
                [InlineKeyboardButton(f"{num}. {wallet["address"]}", callback_data=f"address_{wallet["address"]}"), 
                InlineKeyboardButton(f"Balance: {balance}", callback_data="balance")]
            )
            num += 1
        message = f"Wallets ({num - 1})"
    else:
        message = "No wallets found. Please create a new wallet."
    keyboard = [
        [InlineKeyboardButton("➕️ Connect Wallet", callback_data='connect_wallet'), 
        InlineKeyboardButton("➕️ Generate New Wallet", callback_data='Generate_wallet')],
        [InlineKeyboardButton("➕️ Generate 5 Wallets", callback_data='5_wallets'), 
        InlineKeyboardButton("➕️ Generate 10 Wallets", callback_data='10_wallets')],
        [InlineKeyboardButton("➕️ Transfer all Swell To One", callback_data='transfer_all')],
        [InlineKeyboardButton("🔃️ Reload List", callback_data='reload_all'), InlineKeyboardButton("🗑️ Remove All", callback_data='remove_all')],
        [InlineKeyboardButton("❌ Close", callback_data="close")],
    ]
     # Combine wallet buttons and keyboard buttons
    updated_markup = wallet_address + keyboard
    reply_markup = InlineKeyboardMarkup(updated_markup)
    if update.callback_query:
        await update.callback_query.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode="Markdown",
            )
    elif update.message:
        await update.message.reply_text(
            message,
            reply_markup=reply_markup,
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
    # This function should fetch the user's profile information from the database
    user_id = update.effective_user.id
    wallets = fetch_all_from_wallet(user_id)
    if not wallets:
        await update.message.reply_text("You don't have any wallets yet. Please create a wallet using /wallets.")
        return
    message = "🆔️ Your Profile:\n" \
    "--------------------------------------------------\n"\
    "Balance ◎: 0 Swell / $0\n" \
    "-------------------------------------------------" 
    wallet_address = []
    num = 1
    for wallet in wallets:
        short_address = shorten_address(wallet["address"])
        wallet_address.append(
            [InlineKeyboardButton(f"💳️ Wallet {num} {short_address}", callback_data=f"address_{wallet["address"]}"), ]
        )
        num += 1
    keyboard = [
        [InlineKeyboardButton("🚀️ Sell all", callback_data='sellall'), InlineKeyboardButton("🔥️ Burn_all", callback_data='Burn_all')],
    ]
    keyboard2 = [[InlineKeyboardButton("❌ Close", callback_data="close")]]
    updated_markup = keyboard + wallet_address + keyboard2
    reply_markup = InlineKeyboardMarkup(updated_markup)
    if update.callback_query:
        await update.callback_query.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
    elif update.message:
        await update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )


async def check_balance_command(address: str) -> None:
    try:
        if address:
            balance = await swapper.check_swell_balance(address)
        return balance
    except Exception as e:
        print(f"Error checking balance: {e}")