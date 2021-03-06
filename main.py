from telegram.ext import *
from telegram import *
import logging
import sys
import re
import os

from api_key import API_KEY
import repl
import batch

# Command handlers
def start(update, context):
    """
    Intro message
    """
    if "mode" not in context.chat_data:
        context.chat_data["mode"] = 0
    update.message.reply_text("Hello World!")
    update.message.reply_text("To use me, please use /mode.")

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
        update.message.reply_text("Please upload your source files. Recognized file types:\n" +
                                ".txt - Will be sent to standard input\n" + 
                                ".c - gcc\n" +
                                ".cpp - g++\n" +
                                ".java - JDK\n" +
                                ".py - CPython")
    else:
        update.message.reply_text("Please use one of the following:\n" +
                                  "'/mode 1' - REPL mode\n" +
                                  "'/mode 2' - Batch mode\n")

def exit(update, context):
    """
    Kills any currently running container instances.
    """
    if "container" in context.chat_data:
        if context.chat_data["mode"] == 1:
            repl.kill(context.chat_data["container"])
        if context.chat_data["mode"] == 2:
            batch.kill(context.chat_data["container"])
        update.message.reply_text("Container terminated")
    else:
        update.message.reply_text("Error: Interpreter not started or already terminated")

def run(update, context):
    """
    Runs the batch process specified for mode 2
    """
    if "mode" in context.chat_data and context.chat_data["mode"] == 2:
        if "file_ext" in context.chat_data:
            ext = context.chat_data["file_ext"]
            chat_id = str(update.effective_chat.id)
            path = "user_files/" + chat_id + "/"
            src = "file" + ext
            stdin = "file" + ".txt"
            if not os.path.exists(path + stdin):
                stdin = None
            lang = {
                ".c": "c",
                ".cpp": "c++",
                ".java": "java",
                ".py": "python"
            }[ext]
            def on_finish(outfile):
                doc = open(path + outfile, "rb")
                update.message.reply_document(document=doc)
            def on_close():
                context.chat_data.pop("container", None)
            batch.launch(path, src, stdin, lang, on_finish, on_close)
        else:
            update.message.reply_text("Error: No source code file detected.")
    else:
        update.message.reply_text("Error: This command is only available in mode 2. Please run /mode to change the mode.")

# Message handlers
def default(update, context):
    """
    Called on any noncommand text message
    In mode 1, pipes the message into the container if it exists.
    """
    if "mode" in context.chat_data and context.chat_data["mode"] == 1:
        if "container" in context.chat_data:
            # replace leading \t strings
            raw_input = update.message.text
            indent = 0
            while raw_input[:2] == "\\t":
                indent += 1
                raw_input = raw_input[2:]
            # literal \n string sent - send blank line
            if raw_input == "\\n":
                raw_input = ""
            stdin = indent * "\t" + raw_input
            repl.pipein(context.chat_data["container"], stdin + "\n")
        else:
            update.message.reply_text("Error: Interpreter not started or already terminated")
    else:
        pass # no defined behaviour in other modes

KNOWN_FILE_TYPES = (".txt", ".c", ".cpp", ".java", ".py")
def document(update, context):
    """
    Called on any message with a document
    In mode 2, stores and prepares the files for compilation in the container
    """
    if "mode" in context.chat_data and context.chat_data["mode"] == 2:
        doc = update.message.document
        file_ext = os.path.splitext(doc.file_name)[1]
        if file_ext in KNOWN_FILE_TYPES:
            chat_id = str(update.effective_chat.id)
            if file_ext != ".txt":
                context.chat_data["file_ext"] = file_ext
                # delete previous files
                for other in KNOWN_FILE_TYPES[1:]:
                    path = "user_files/" + chat_id + "/file" + other
                    if os.path.exists(path):
                        os.remove(path)
            if not os.path.exists("user_files"):
                os.mkdir("user_files")
            if not os.path.exists("user_files/" + chat_id):
                os.mkdir("user_files/" + chat_id)
            doc.get_file().download(custom_path="user_files/" + chat_id + "/file" + file_ext, timeout=1000)
        else:
            update.message.reply_text("Unknown file type: " + file_ext)
    else:
        pass # no defined behaviour in other modes

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
        def pipeout(out):
            if re.match("\S", out): # contains non-whitespace character
                message.reply_text(out)
        def on_close():
            context.chat_data.pop("container", None)
        container = repl.launch(lang, pipeout, on_close)
        context.chat_data["container"] = container
    else:
        print(context.chat_data["mode"]) # debug statement

# Miscellaneous functions
def drop_data(update, context):
    """
    Clears all chat data and 'resets' the state of the bot.
    """
    if "container" in context.chat_data:
        repl.kill(context.chat_data["container"])
    chat_id = str(update.effective_chat.id)
    for ext in KNOWN_FILE_TYPES:
        path = "user_files/" + chat_id + ext
        if os.path.exists(path):
            os.remove(path)
    context.user_data["mode"] = 0
    update.message.reply_text("Existing data cleared!")

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

    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("mode", mode))
    dp.add_handler(CommandHandler("exit", exit))
    dp.add_handler(CommandHandler("run", run))

    dp.add_handler(MessageHandler(Filters.text, default))
    dp.add_handler(MessageHandler(Filters.document, document))

    dp.add_handler(CallbackQueryHandler(button))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
