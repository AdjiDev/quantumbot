"""

By adjidev (Rizky Kian Adji Putra)
Copyright (c) 2024
Read MIT license before recode this script

"""
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import plugins.ytmp3 as ytmp3
import plugins.ytmp4 as ytmp4
from config import limit, timezone, owner_id
import time
import threading
from datetime import datetime
import pytz
import os

def init(bot, send_typing_action):
    def reset_limit_daily():
        while True:
            current_time = datetime.now(pytz.timezone(timezone))
            if current_time.hour == 5 and current_time.minute == 0:
                global limit
                limit = 25 
                bot.send_message(owner_id, "Daily limit has been reset to 25.")
            time.sleep(60)

    threading.Thread(target=reset_limit_daily, daemon=True).start()

    @bot.message_handler(commands=['start'])
    @send_typing_action
    def start(m):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('FEATURES', callback_data='FEATURES'))
        bot.reply_to(m, 'CLICK BUTTON BELOW TO SEE BOT FEATURES', reply_markup=markup, parse_mode='Markdown')

    @bot.callback_query_handler(func=lambda call: call.data == 'FEATURES')
    def callback(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        new_markup = InlineKeyboardMarkup()
        new_markup.add(InlineKeyboardButton('AI CHATBOT', callback_data='ai_feature'))
        new_markup.add(InlineKeyboardButton('EXTRA', callback_data='extra_features'))
        new_markup.add(InlineKeyboardButton('GROUP TOOLS', callback_data='group_utilities'))
        bot.send_message(call.message.chat.id, 'LIST OF BOT FEATURES:', reply_markup=new_markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('ai_'))
    def ai_features(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f'```AI\n/gemini - coming soon```', parse_mode='Markdown')
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith('extra_'))
    def extra_features(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f'```EXTRA-FEATURES\n/ytmp3 - download yt video url to mp3\n/ytmp4 download youtube video url to mp4\n/genproxy - generate random proxies\n/generateua - generate random user agent```', parse_mode='Markdown')
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith('group_'))
    def group_utilities(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f'```GROUP-TOOLS\n/ban - ban user\n/unban - unban user\n/allowsendmsg - allow group send message permission```', parse_mode='Markdown')

    @bot.message_handler(commands=['ytmp3'])
    @send_typing_action
    def ytmp3_handler(m):
        global limit
        if limit > 0:
            limit -= 1
            yt_url = m.text.split()[1] if len(m.text.split()) > 1 else None
            if yt_url:
                output_path = 'plugins/temp/audio'
                os.makedirs(output_path, exist_ok=True)
                bot.reply_to(m, 'Downloading audio, please wait...')
                mp3_file = ytmp3.download_youtube_audio(yt_url, output_path)
                if os.path.isfile(mp3_file):
                    with open(mp3_file, 'rb') as audio:
                        bot.send_audio(m.chat.id, audio)
                    os.remove(mp3_file)
                else:
                    bot.reply_to(m, f"Error: {mp3_file}")
            else:
                bot.reply_to(m, 'Please provide a valid YouTube URL.')
        else:
            bot.reply_to(m, 'Download limit reached for today. Your limit will reset at 05:00.')

    @bot.message_handler(commands=['ytmp4'])
    @send_typing_action
    def ytmp4_handler(m):
        global limit
        if limit > 0:
            limit -= 1
            yt_url = m.text.split()[1] if len(m.text.split()) > 1 else None
            if yt_url:
                output_path = 'plugins/temp/video'
                os.makedirs(output_path, exist_ok=True)
                bot.reply_to(m, 'Downloading video, please wait...')
                video_file = ytmp4.download_youtube_video(yt_url, output_path)
                if os.path.isfile(video_file):
                    with open(video_file, 'rb') as video:
                        bot.send_video(m.chat.id, video)
                    os.remove(video_file)
                else:
                    bot.reply_to(m, f"Error: {video_file}")
            else:
                bot.reply_to(m, 'Please provide a valid YouTube URL.')
        else:
            bot.reply_to(m, 'Download limit reached for today. Your limit will reset at 05:00.')
