import telebot
from config import keys, TOKEN
from extentions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты, цену которой вы хотите узнать> \
\n<имя валюты, в которой надо узнать цену первой валюты> \
\n<количество первой валюты> \nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')

        base, quote, amount = values
        price = CryptoConverter.convert(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду. \n{e}')
    else:
        text = f'{amount} {keys[base]} = {price} {keys[quote]}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)