import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(base, quote, amount):
        if quote == base:
            raise ConvertionException('Введены одинаковые валюты')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Конвертация валюты {base} невозможна')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Конвертация в валюту {quote} невозможна')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        price = json.loads(r.content)[keys[quote]]

        return price * amount