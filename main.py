import logging
import sqlite3
from telegram import Update
from telegram.ext import (
    filters, MessageHandler, ApplicationBuilder, 
    ContextTypes, CommandHandler
)

from interpreter import new_interpreter
import msg
import config

logging.basicConfig(
    #filename='bot.log',
    #filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def create_msg_handler(msg_text):
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=msg_text
        )
    return handler

async def interpret(update: Update, context: ContextTypes.DEFAULT_TYPE):
    interpreter = new_interpreter()
    img_out, error_out, text_out = interpreter.interpreting_pipeline(
        update.message.text.lower()
    )
    if img_out is not None:
        img_out.save("./output.png")
        await context.bot.send_photo(
            chat_id=update.effective_chat.id, 
            photo="./output.png"
        )
    if error_out + text_out != "":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=error_out + "\n\n" + text_out
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token(config.bot_token).build()

    command_msgs = {
        'start': msg.start_msg,
        'help': msg.help_msg,
        'forward': msg.forward_msg,
        'backward': msg.backward_msg,
        'right': msg.right_msg,
        'left': msg.left_msg,
        'penup': msg.penup_msg,
        'pendown': msg.pendown_msg,
        'repeat': msg.repeat_msg,
        'make': msg.make_msg,
        'if': msg.if_msg,
        'to': msg.to_msg,
        'clean': msg.clean_msg,
        'home': msg.home_msg,
        'clearscreen': msg.clearscreen_msg,
        'hideturtle': msg.hideturtle_msg,
        'showturtle': msg.showturtle_msg,
        'setheading': msg.setheading_msg,
        'print': msg.print_msg
    }

    for command, msg_text in command_msgs.items():
        application.add_handler(
            CommandHandler(command, create_msg_handler(msg_text))
        )

    interpret_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), interpret
    )
    application.add_handler(interpret_handler)

    application.run_polling()
