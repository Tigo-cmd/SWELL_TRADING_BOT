#!/usr/bin/python3 env
"""
swell trading bot implentation and intergration
"""
from typing import final
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from telegram.ext import Updater, CommandHandler
import requests

# Telegram bot token from BotFather
TELEGRAM_TOKEN = "8010846115:AAGIeu4dBKCxI3vr6CU4BZBkF1Ojh-XYlvU"
TOKEN: Final = TELEGRAM_API_TOKEN


def main():
  print('Starting Bot......')
  app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

  app.add_handler(CommandHandler("start", start))
  print('Polling......')
  print('Waiting For User Input......')
  app.run_polling()
  # updater.idle()

if __name__ == "__main__":
  main()


# def main():
#     updater = Updater(TELEGRAM_TOKEN, use_context=True)
#     dp = updater.dispatcher

#     # Add command handlers
#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("price", price))
#     dp.add_handler(CommandHandler("trade", trade))

#     # Start the bot
#     updater.start_polling()
#     updater.idle()

# if __name__ == "__main__":
#     main()