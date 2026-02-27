from telegram.ext import Application, CommandHandler
from telegram.error import TelegramError
import asyncio
import logging

from configs import token
from handler import start, status, socket_off, socket_on, debug_devices
from logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)


def main():
    print("Start execution")

    try:
        print(f"There is token - {token[:5]}")
        # create app
        app = Application.builder().token(token).build()

        print("5. Добавляем обработчики...")
        # register handler
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("status", status))
        app.add_handler(CommandHandler("socket_on", socket_on))
        app.add_handler(CommandHandler("socket_off", socket_off))
        app.add_handler(CommandHandler("debug", debug_devices))


        logger.info("Инициализация успешна")
        try:
            app.run_polling()
        except Exception as e:
            logger.exception("Критическая ошибка при работе бота")

    except TelegramError as er:
        logger.error(f"Ошибка {er}")
    except Exception as er:
        logger.error(f"Критичная ошибка - {er}", exc_info=True)


if __name__ == "__main__":
    main()
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
