from telegram import Bot, Update, ForceReply, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler

from bot.tg_messages import GIVE_CONTACT_MESSAGE


class BaseBot:
    def __init__(self, token):
        self.bot = Bot(token)
        self.dispatcher = Dispatcher(self.bot, None, workers=0)
        self.dispatcher.add_handler(CommandHandler("start", handler))

    def process_update(self, request):
        self.dispatcher.process_update(Update.de_json(request, self.bot))


def handler(update, context):
    update.message.reply_text(
        GIVE_CONTACT_MESSAGE, reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(text='give a phone number', request_contact=True)
        )
    )

