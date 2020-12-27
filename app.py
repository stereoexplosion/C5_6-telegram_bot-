import telebot

from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Данный бот позволяет конвертировать друг в друга различные типы валют, исходя из текущего курса. \
\nЧтобы начать работу, введите команду боту в следующем формате: \n<Имя валюты> \
<В какую валюту перевести> \
<Количество переводимой валюты> \
\nДля корректной работы вводите сумму конвертации единым числом, без пробелов. \
\nЕсли число дробное, в качестве разделителя используйте точку. \
\nПример ввода: рубль доллар 5600.5 \nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
       text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        values = [x.lower() for x in values]
        if len(values) != 3:
            raise APIException("Неверное количество параметров. Попробуйте ещё раз.")

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")

    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)
bot.polling(none_stop=True)
