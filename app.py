import telebot
from config import keys, TOKEN
from extensions import MoneyConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате: \n <имя валюты> (увы, доступно только евро)\n\
    <имя валюты, в которой надо узнать цену первой валюты>\n <количество первой валюты>\n\
    Увидеть список всех доступных валют:     /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys:
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise APIException("Неверное количество параметров. Инструкция: /help")
        quote, base, amount = values
        total_base = MoneyConverter.get_price(quote, base, amount)
        total_base = float(total_base) * float(amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя. \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду \n{e}. Надеюсь вы помните, что первая валюта только евро")
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
