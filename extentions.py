from configs import currency_dict
import requests
import json
class APIException(Exception):
    pass
class ConverterTool:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Вы ввели одинаковые валюты: "{base} - {quote}"')

        try:
            from_ticker = currency_dict[base.lower()]
        except KeyError:
            raise APIException(
                f'\nНе удалось получить значение введённой валюты: "{base}".\nПроверьте корректность ввода, уточните правильное наименование валюты'\
                f'по команде: /values.')

        try:
            to_ticker = currency_dict[quote.lower()]
        except KeyError:
            raise APIException(
                f'Не удалось получить значение введённой валюты: "{quote}".\nПроверьте корректность ввода, уточните правильное наименование валюты'\
                f'по команде: /values.')

        try:
            if float(amount) < 0:
                raise APIException(f'Вы ввели отрицательное значение: "{amount}"')
            else:
                amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обратотать введённое количество валюты для конвертации - "{amount}"')

        req_API = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={from_ticker}&tsyms={to_ticker}')
        result = json.loads(req_API.content)[currency_dict[quote.lower()]]

        return result