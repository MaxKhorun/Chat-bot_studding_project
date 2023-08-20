import telebot
from configs import TOKEN, currency_dict
from extentions import APIException, ConverterTool

currency_Bot = telebot.TeleBot(TOKEN)

@currency_Bot.message_handler(commands=['start'])
def bot_start(message):
            text = 'Привет!\nВы запустили бот-помошник для конвертации валют.' \
                   '\nПравила использования и список доступных команд можете увидеть набрав команду: ' \
                   ' /help'
            currency_Bot.send_message(message.chat.id, text)
@currency_Bot.message_handler(commands=['help'])
def help_cmnd(message):
    text = '1. Чтобы сконвертировать валюту по текущему курсу, введите без кавычек через пробел:' \
           '\n<валюта, из которой переводим>, < валюта в которую переводим>, <количество единиц валюты>.' \
           '\n' \
           '\n2. Наименование валют для запроса конвертации смотрите в списке доступных по команде: /values'
    currency_Bot.send_message(message.chat.id, text)
@currency_Bot.message_handler(commands=['values'])
def curency_rates(message):
    text = 'Доступные валюты для перевода: '
    for k in currency_dict.keys():
        text = '\n'.join((text, k, ))
    currency_Bot.send_message(message.chat.id, text)

@currency_Bot.message_handler(content_types=['text'])
def currency_convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Некорректное количество параметров')
        else:
            base, qoute, amount = values
            result = ConverterTool.get_price(base, qoute, amount)
    except APIException as er:
        currency_Bot.reply_to(message, f'Ошибка ввода, проверьте данные. Ошибка - {er}')
    except Exception as er:
        currency_Bot.reply_to(message, f'Невозможно обработать команду, ошибка - {er}')
    else:
        text_res = f'количество {amount} {base} в {qoute} по курсу {result} = {round(result*float(amount), 3)}'
        currency_Bot.send_message(message.chat.id, text_res)

currency_Bot.polling(none_stop=True)
