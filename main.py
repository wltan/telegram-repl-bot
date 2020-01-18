from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from api_key import API_KEY
import logging
import sys

# Command handlers
def start(update, context):
    update.message.reply_text("Hello World!")

def default(update, context):
    pass

# Initializing the bot
def main():
    # Log to stdout
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    updater = Updater(API_KEY, use_context=True)

    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, default))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
