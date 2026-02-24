import telebot
from configs import token
from exceptions import APIException, ConverterTool

HomeAssistant_Bot = telebot.TeleBot(token)

@HomeAssistant_Bot.message_handler(commands=['start'])
def bot_start(message):
            text = 'Привет!\nВы запустили бот-помошник по дому.' \
                   '\nПравила использования и список доступных команд можете увидеть набрав команду: ' \
                   ' /help'
            HomeAssistant_Bot.send_message(message.chat.id, text)
@HomeAssistant_Bot.message_handler(commands=['help'])
def help_cmnd(message):
    text = '1. Чтобы ...:' \
           '\n<...>, <...>, <...>.' \
           '\n' \
           '\n2. Что-то второе: /values'
    HomeAssistant_Bot.send_message(message.chat.id, text)

# @HomeAssistant_Bot.message_handler(commands=['values'])
# def values_graphs(message):


@HomeAssistant_Bot.message_handler(content_types=['text'])
def currency_convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Некорректное количество параметров')
        else:
            base, qoute, amount = values
            result = ConverterTool.get_price(base, qoute, amount)
    except APIException as er:
        HomeAssistant_Bot.reply_to(message, f'Ошибка ввода, проверьте данные. Ошибка - {er}')
    except Exception as er:
        HomeAssistant_Bot.reply_to(message, f'Невозможно обработать команду, ошибка - {er}')
    else:
        text_res = f'количество {amount} {base} в {qoute} по курсу {result} = {round(result*float(amount), 3)}'
        HomeAssistant_Bot.send_message(message.chat.id, text_res)

HomeAssistant_Bot.polling(none_stop=True)
