import requests
import telebot
import schedule
import time

from telebot import types


bot = telebot.TeleBot('token')

def main():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    key1 = types.KeyboardButton('Список ордеров')
    key2 = types.KeyboardButton('Инфо')
    key3 = types.KeyboardButton('Просмотр сделок')
    markup.add(key1, key2, key3)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в моего бота по торговле на бирже Yobit', reply_markup=main())

@bot.message_handler(content_types=['text'])
def cont(message):
    if message.text == 'Инфо':
        bot.send_message(message.chat.id, get_ticker, reply_markup=main())
    elif message.text == 'Список ордеров':
        bot.send_message(message.chat.id, get_depth, reply_markup=main())
    elif message.text == 'Просмотр сделок':
        bot.send_message(message.chat.id, get_trades, reply_markup=main())

#   [-] =======================================================================>


def get_info():
    response = requests.get("https://yobit.net/api/3/info")

    with open("info.txt", "w") as file:
        file.write(response.text)
    return response.text


def get_ticker(coin1="btc", coin2="usd"):
    response = requests.get(f"https://yobit.net/api/3/ticker/{coin1}_{coin2}?ignore_invalid=1")


    with open("ticker.txt", 'w') as file:
        file.write(response.text)
    return response.text


def get_depth(coin1="btc", coin2="usd", limit=150):
    response = requests.get(f"https://yobit.net/api/3/depth/{coin1}_{coin2}?limit={limit}ignore_invalid=1")

    with open("depth.txt", 'w') as file:
        file.write(response.text)

    bids = response.json()[f"{coin1}_usd"]["bids"]

    total_bids_amount = 0
    for item in bids:
        price = item[0]
        coin_amount = item[1]

        total_bids_amount += price * coin_amount


    return f"Total bids: {total_bids_amount} $"



def get_trades(coin1="btc", coin2="usd", limit=150):
    response = requests.get(f"https://yobit.net/api/3/trades/{coin1}_{coin2}?limit={limit}&ignore_invalid=1")

    with open("trades.txt", 'w') as file:
        file.write(response.text)

    total_trade_ask = 0
    total_trade_bid = 0

    for item in response.json()[f"{coin1}_{coin2}"]:
        if item["type"] == "ask":
            total_trade_ask += item["price"] * item["amount"]
        else:
            total_trade_bid += item["price"] * item["amount"]

    info = f"[-] TOTAL {coin1} SELL: {total_trade_ask} $\n[+] TOTAL {coin1} BUY: {total_trade_bid} $"

    return info




if __name__ == '__main__':
    main()


bot.polling(none_stop=True)
