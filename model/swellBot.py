#!/usr/bin/python3 env
"""
swell trading bot implentation and intergration
"""
from typing import Final
from telegram import (
  Update, 
  ReplyKeyboardMarkup, 
  KeyboardButton
  )
from telegram.ext import (
  Application, 
  CommandHandler, 
  MessageHandler, 
  filters, 
  ContextTypes
)
import requests
from commands import (
  start_command,
  trade_command,
  price_command,
  Trades_command,
  help_command,
  Buysell_command,
  Settings_command,
  CreateWallet_command,
  tip_command,
  profile_command,
)
# Telegram bot token from BotFather
TELEGRAM_TOKEN = "8010846115:AAGIeu4dBKCxI3vr6CU4BZBkF1Ojh-XYlvU"
TOKEN: Final = TELEGRAM_TOKEN


if __name__ == '__main__':
    print('Starting Bot......')
    app = Application.builder().token(TOKEN).build()

    # default commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('trade', trade_command))
    app.add_handler(CommandHandler('prices', prices_command))
    app.add_handler(CommandHandler('buysell', Buysell_command))
    app.add_handler(CommandHandler('wallet', CreateWallet_command))
    app.add_handler(CommandHandler('tip', tip_command))
    app.add_handler(CommandHandler('profile', profile_command))
    app.add_handler(CommandHandler('Trades', Trades_command))
    app.add_handler(CommandHandler('settings', settings))
    app.add_handler(CommandHandler('help', help_command))

    # message commands
    app.add_handler(MessageHandler(filters.TEXT, message_handler))

    # voice commands
    app.add_handler(MessageHandler(filters.VOICE, voice_messsage))

    # Errors
    app.add_error_handler(error)

    # bot Polling
    print('Polling......')
    print('Waiting For User Input......')
    app.run_polling(poll_interval=3)
