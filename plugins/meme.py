import requests
from telebot import TeleBot

def handle_meme_command(bot: TeleBot):
    @bot.message_handler(commands=['meme'])
    def meme_command(m):
        try:
            response = requests.get("https://api.junn4.my.id/search/meme")
            response.raise_for_status()
            data = response.json()

            if data['status'] == 200 and 'result' in data and data['result']:
                result = data['result']

                if result.get('url') and result['url'].endswith('.mp4'):
                    video_url = result['url']
                    bot.send_video(m.chat.id, video_url, caption=result.get('caption', ''))
                else:
                    bot.reply_to(m, "No meme video found.")

            else:
                bot.reply_to(m, "No meme found at the moment. Try again later.")

        except requests.RequestException as e:
            bot.reply_to(m, f"An error occurred while fetching meme: {e}")
