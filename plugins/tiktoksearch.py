import requests
from telebot import TeleBot

def handle_tiktoksearch_command(bot: TeleBot):
    @bot.message_handler(commands=['ttsearch'])
    def tiktoksearch_command(m):
        query = m.text[len('/ttsearch '):].strip()
        if not query:
            bot.reply_to(m, "Please provide a search query.")
            return

        try:
            response = requests.get(f"https://api.junn4.my.id/search/tiktoksearch?query={query}")
            response.raise_for_status()
            data = response.json()

            if data['status'] == 200 and 'result' in data and data['result']:
                result = data['result']

                bot.send_photo(m.chat.id, result['cover'], caption=result['title'])

                if 'no_watermark' in result:
                    bot.send_video(m.chat.id, result['no_watermark'])
                elif 'watermark' in result:
                    bot.send_video(m.chat.id, result['watermark'])

                if 'music' in result:
                    bot.send_audio(m.chat.id, result['music'])

            else:
                bot.reply_to(m, f"No results found for '{query}'.")

        except requests.RequestException as e:
            bot.reply_to(m, f"An error occurred while fetching data: {e}")
