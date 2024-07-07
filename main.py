"""

By adjidev (Rizky Kian Adji Putra)
Copyright (c) 2024
Read MIT license before recode this script

"""
import telebot
import time
from config import token, typing_delay, limit, timezone, owner_id
from plugins.start import init as start_init
from plugins.proxy_generator import init as proxy_init
from plugins.ua_generator import init as ua_init
from plugins.group_tools import init as group_tools_init
import threading
from datetime import datetime
import pytz

bot = telebot.TeleBot(token)
global_limit = limit

def send_typing_action(func):
    def wrapper(message):
        global global_limit
        if global_limit > 0:
            bot.send_chat_action(message.chat.id, 'typing')
            time.sleep(typing_delay)
            global_limit -= 1
            return func(message)
        else:
            bot.send_message(message.chat.id, "Limit reached. Please try again later.")
    return wrapper

def reset_limit_daily():
    while True:
        current_time = datetime.now(pytz.timezone(timezone))
        if current_time.hour == 5 and current_time.minute == 0:
            global global_limit
            global_limit = 25
            bot.send_message(owner_id, "Daily limit has been reset to 25.")
        time.sleep(60)

start_init(bot, send_typing_action)
proxy_init(bot, send_typing_action)
ua_init(bot, send_typing_action)
group_tools_init(bot, send_typing_action)

reset_thread = threading.Thread(target=reset_limit_daily)
reset_thread.start()

if __name__ == '__main__':
    print('BOT IS RUNNING . . .')
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f'Error: {e}')
