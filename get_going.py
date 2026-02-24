from telegram.ext import Application, CommandHandler
from telegram.error import TelegramError
import asyncio
import logging

from configs import token
from handler import start, status
from logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)


def get_going():
    try:
        # create app
        app = Application.builder().token(token).build()

        # register handler
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("status", status))

        logger.info("Инициализация успешна")
        app.run_polling()

    except TelegramError as er:
        logger.error(f"Ошибка {er}")
    except Exception as er:
        logger.error(f"Критичная ошибка - {er}", exc_info=True)

if __name__ == "__get_going__":
    get_going()
#
# @HomeAssistant_Bot.message_handler(commands=['start'])
# def bot_start(message):
#             text = 'Привет!\nВы запустили бот-помошник по дому.' \
#                    '\nПравила использования и список доступных команд можете увидеть набрав команду: ' \
#                    ' /help'
#             HomeAssistant_Bot.send_message(message.chat.id, text)
# @HomeAssistant_Bot.message_handler(commands=['help'])
# def help_cmnd(message):
#     text = '1. Чтобы ...:' \
#            '\n<...>, <...>, <...>.' \
#            '\n' \
#            '\n2. Что-то второе: /values'
#     HomeAssistant_Bot.send_message(message.chat.id, text)
#
# # @HomeAssistant_Bot.message_handler(commands=['values'])
# # def values_graphs(message):
#
#
# HomeAssistant_Bot.polling(none_stop=True)
