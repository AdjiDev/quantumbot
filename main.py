"""
Made by Adjidev ( Rizky Kian Adji Putra )
free recoded no enc but please give star😭😭
"""

import os
import logging
from telebot import TeleBot, types
from time import sleep as delay
import dotenv

dotenv.load_dotenv()

bot = TeleBot(os.getenv('BOT_TOKEN'))

commands = [
    "/start - Start the bot",
    "/help - Show this help message",
    "/ban <tag> - Ban a user (reply to their message)",
    "/unban <user_id> - Unban a user by their ID",
    "/kick <tag> - Kick a user (reply to their message)",
    "/add <user_id or @username> - Add a user to the group by their ID or username",
    "/meme - Get a random meme",
    "/ss <url> - Take a screenshot of the specified URL",
    "/genai on/off - Analyze image with given image",
    "/pinsearch <query> - Search Pinterest for images based on the query",
    "/ytsearch <query> - Search YouTube for videos based on the query",
    "/tiktoksearch <query> - Search TikTok for videos based on the query",
    "/infogempa - Get the latest earthquake information",
    "/mediafire <url> - Download file from MediaFire"
]

COMMANDS_PER_PAGE = 5
IMAGE_URL = 'https://telegra.ph/file/fb4df59d202f0d171b5f3.jpg'

@bot.message_handler(commands=['help'])
def help_command(m):
    send_paginated_commands(m.chat.id, 0)

def send_paginated_commands(chat_id, page):
    start = page * COMMANDS_PER_PAGE
    end = start + COMMANDS_PER_PAGE
    help_text = "Here are the available commands:\n\n" + "\n".join(commands[start:end])
    
    keyboard = types.InlineKeyboardMarkup()
    if start > 0:
        keyboard.add(types.InlineKeyboardButton("Previous", callback_data=f"help_page_{page-1}"))
    if end < len(commands):
        keyboard.add(types.InlineKeyboardButton("Next", callback_data=f"help_page_{page+1}"))

    bot.send_photo(chat_id, IMAGE_URL, caption=help_text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('help_page_'))
def handle_help_page_callback(call):
    page = int(call.data.split('_')[-1])
    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption="Here are the available commands:\n\n" + "\n".join(commands[page*COMMANDS_PER_PAGE:(page+1)*COMMANDS_PER_PAGE]),
        reply_markup=generate_pagination_keyboard(page)
    )

def generate_pagination_keyboard(page):
    keyboard = types.InlineKeyboardMarkup()
    if page > 0:
        keyboard.add(types.InlineKeyboardButton("Previous", callback_data=f"help_page_{page-1}"))
    if (page + 1) * COMMANDS_PER_PAGE < len(commands):
        keyboard.add(types.InlineKeyboardButton("Next", callback_data=f"help_page_{page+1}"))
    return keyboard

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_chat_action(m.chat.id, 'typing')
    delay(5)
    bot.reply_to(m, 'Type /help for available commands')

# impor plugins
from plugins.mediafire import handle_mediafire_command
from plugins.genai import handle_genai_command
from plugins.pinsearch import handle_pinterest_command
from plugins.infogempa import handle_infogempa_command
from plugins.tiktoksearch import handle_tiktoksearch_command
from plugins.ytsearch import handle_youtube_command
from plugins.meme import handle_meme_command
from plugins.ssweb import handle_ssweb_command

# Daftar plugins baru sini 
handle_genai_command(bot)
handle_mediafire_command(bot)
handle_pinterest_command(bot)
handle_infogempa_command(bot)
handle_tiktoksearch_command(bot)
handle_youtube_command(bot)
handle_meme_command(bot)
handle_ssweb_command(bot)

def start_bot():
    print('Bot is running!')
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Bot polling failed: {e}")
            print('Reconnecting...')
            delay(15)

if __name__ == '__main__':
    start_bot()
