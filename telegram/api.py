from telegram.ext import Updater
updater = Updater(token='1166220592:AAERb8dnA5rfDSRf338BGV4l2m_Sp_z6Xso', use_context=True)

dispatcher = updater.dispatcher

def send_chat(text):
        saartje = Updater("1166220592:AAERb8dnA5rfDSRf338BGV4l2m_Sp_z6Xso")
        saartje.bot.send_message(chat_id="1261249355 ", text="wil je de temperatuur weten typ dan /start ")

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id="1261249355  ", text="20°C")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()

def echo(update, context):
    context.bot.send_message(chat_id="1261249355 ", text=update.message.text)

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id="1261249355 ", text=text_caps)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id="1261249355 ", text=text_caps)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

def unknown(update, context):
    context.bot.send_message(chat_id="1261249355 ", text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)


send_chat("wil je de temperatuur weten typ dan /start ")