import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update
from wiki import search
# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# telegram bot token
TOKEN = "ENTER YOUR TOKEN"

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello!"


@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    """webhook view which receives updates from telegram"""
    # create update object from json-format request data
    update = Update.de_json(request.get_json(), bot)
    # process update
    dp.process_update(update)
    return "ok"


def start(bot, update):
    """callback function for /start handler"""
    author = update.message.from_user.first_name
    reply = "Hi! {}".format(author)
    bot.send_message(chat_id=update.message.chat_id, text=reply)


def _help(bot, update):
    """callback function for /help handler"""
    help_txt = '''Here for Help... 
               I am WIKIPEDIA search BOT
               Enter the Word you want to search such as Taylor Swift '''
    bot.send_message(chat_id=update.message.chat_id, text=help_txt)


def echo_text(bot, update):
    """callback function for text message handler"""
    user_input = update.message.text
    reply = search(user_input)
    bot.send_message(chat_id=update.message.chat_id, text=reply)


def echo_sticker(bot, update):
    """callback function for sticker message handler"""
    bot.send_sticker(chat_id=update.message.chat_id,
                     sticker=update.message.sticker.file_id)


def error(bot, update):
    """callback function for error handler"""
    logger.error("Update '%s' caused error '%s'", update, update.error)

bot = Bot(TOKEN)
try:
    bot.set_webhook("https://enigmatic-citadel-27238.herokuapp.com/" + TOKEN)
except Exception as e:
    print(e)


dp = Dispatcher(bot, None)
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", _help))
dp.add_handler(MessageHandler(Filters.text, echo_text))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_error_handler(error)

if __name__ == "__main__":
    app.run(port=8443)
