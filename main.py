from telegram.ext import *
from telegram import *
import logging
import sys

from api_key import API_KEY
import repl

# Command handlers
def start(update, context):
    """
    Intro message
    """
    context.chat_data["mode"] = 0
    update.message.reply_text("Hello World!")

def mode(update, context):
    """
    On a valid message, clears any existing data and sets a new mode.
    """
    args = drop_command(update.message.text, "/mode")
    if args == "1":
        # 1. REPL mode
        drop_data(update, context)
        context.chat_data["mode"] = 1
        options = [
            InlineKeyboardButton("python (Python)", callback_data="python"),
            InlineKeyboardButton("jshell (Java)", callback_data="java"),
            InlineKeyboardButton("igcc (C)", callback_data="c"),
            InlineKeyboardButton("js-slang (Source)", callback_data="source")]
        update.message.reply_text("Please choose the type of interpreter:",
                                  reply_markup=InlineKeyboardMarkup.from_column(options))
    elif args == "2":
        # 2. Batch mode
        drop_data(update, context)
        context.chat_data["mode"] = 2
        update.message.reply_text("Set mode 2")
    else:
        update.message.reply_text("Please use one of the following:\n" +
                                  "'/mode 1' - REPL mode\n" +
                                  "'/mode 2' - Batch mode\n")

def exit(update, context):
    """
    Kills any currently running container instances.
    """
    if "container" in context.chat_data:
        repl.kill(context.chat_data["container"])
        del context.chat_data["container"]
    else:
        update.message.reply_text("Error: Interpreter not started or already terminated")

def default(update, context):
    if "mode" in context.chat_data and context.chat_data["mode"] == 1:
        if "container" in context.chat_data:
            repl.pipein(context.chat_data["container"], update.message.text)
        else:
            update.message.reply_text("Error: Interpreter not started or already terminated")

# Callback handlers
def button(update, context):
    if "mode" in context.chat_data and context.chat_data["mode"] == 1 and "container" not in context.chat_data:
        query = update.callback_query
        message = query.message
        lang = query.data
        message.edit_reply_markup() # remove the buttons
        shell = {
            "python": "python (Python)",
            "java"  : "jshell (Java)",
            "c"     : "igcc (C)",
            "source": "js-slang (Source)"
            }[lang]
        message.reply_text("Now starting " + shell + " interpreter...")
        pipeout = lambda s: message.reply_text(s)
        container = repl.launch(lang, pipeout)
        context.chat_data["container"] = container
    else:
        print(context.chat_data["mode"]) # debug statement

# Miscellaneous functions
def drop_data(update, context):
    """
    Clears all chat data and 'resets' the state of the bot.
    """
    context.chat_data.clear()
    context.user_data.clear()

def drop_command(message, command):
    """
    Given a message text, drops the command prefix from the string.
    """
    return message[len(command) + 1:]

# Initializing the bot
def main():
    # Log to stdout
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    updater = Updater(API_KEY, use_context=True)

    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("mode", mode))
    dp.add_handler(CommandHandler("exit", exit))
    dp.add_handler(MessageHandler(Filters.text, default))

    # Add callback handler
    dp.add_handler(CallbackQueryHandler(button))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
