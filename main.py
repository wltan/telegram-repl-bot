from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
token = "TOKEN"

# Command handlers
def start(update, context):
    pass

def default(update, context):
    pass

# Initializing the bot
def main():
    updater = Updater(token, use_context=True)

    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, default))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
