from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    swell_price = "0.009683"  # Static for example — you could fetch this dynamically
    welcome_text = (
        "🚀 SwellTradingBot: Your all-in-one toolkit for Swell trading 🪙\n\n"
        f"💰 SWELL Price: ${swell_price}\n\n"
        "🧱 Create your first wallet at /wallets\n"
        "[Website](https://swelltradingbot.vercel.app)| [Github](https://github.com/SwellTradingBot/) | [Twitter](https://x.com/swelltradingbot)"
    )

    # Define the keyboard structure
    keyboard = [
        [KeyboardButton("📈 Buy & Sell"), KeyboardButton("🎯 Token Sniper")],
        # [KeyboardButton("💣 Sniper Pumpfun"), KeyboardButton("🚀 Sniper Moonshot")],
        [KeyboardButton("📊 Limit Orders"), KeyboardButton("📉 DCA Orders")],
        [KeyboardButton("👤 Profile"), KeyboardButton("👛 Wallets"), KeyboardButton("💱 Trades")],
        [KeyboardButton("📎 Copy Trades"), KeyboardButton("🤝 Referral System")],
        [KeyboardButton("🔁 Transfer SWELL"), KeyboardButton("⚙️ Settings")],
        [KeyboardButton("🔥 Our STBOT Tools"),KeyboardButton("🆘 Help")],
        [KeyboardButton("🔒 Security"), KeyboardButton("🎓 Tutorials")],
        [KeyboardButton("❌ Close")]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
      welcome_text,
      parse_mode="Markdown",
      reply_markup=reply_markup
    )
    print("activated Start command...")


# Price command
async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper()  # e.g., "BTC"
        ticker = exchange.fetch_ticker(f"{symbol}/USDT")
        price = ticker['last']
        update.message.reply_text(f"The price of {symbol} is ${price}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

# Trade command (example: buy order)
def trade_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper()  # e.g., "BTC"
        amount = float(context.args[1])  # Amount to buy
        order = exchange.create_market_buy_order(f"{symbol}/USDT", amount)
        update.message.reply_text(f"Bought {amount} {symbol}: {order}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

# function to handle the trades command
async def Trades_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I'm Here To Help")


# function to handle the help reply
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I'm Here To Help")

# function to handle the buysell reply
async def Buysell_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I'm Here To Help")

# function to handle the settings reply
async def Settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I'm Here To Help")



# function to handle the wallet reply
async def CreateWallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I'm Here To Help")


# function to handle the tip reply
async def tip_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I'm Here To Help")


# function to handle the profile reply
async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I'm Here To Help")
