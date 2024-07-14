import requests
from telebot import TeleBot

def handle_youtube_command(bot: TeleBot):
    @bot.message_handler(commands=['ytsearch'])
    def youtube_command(m):
        query = m.text[len('/ytsearch '):].strip()
        if not query:
            bot.reply_to(m, "Please provide a search query.")
            return

        try:
            response = requests.get(f"https://api.junn4.my.id/search/ytsearch?query={query}")
            response.raise_for_status()
            data = response.json()

            if data['status'] == 200 and 'result' in data and data['result']:
                first_result = data['result'][0]  # Assuming we take the first result

                if first_result['type'] == 'video':
                    video_url = first_result['url']
                    bot.send_message(m.chat.id, f"Title: {first_result['title']}\n"
                                                f"Description: {first_result['description']}\n"
                                                f"Views: {first_result['views']}\n"
                                                f"Duration: {first_result['timestamp']}\n"
                                                f"Channel: {first_result['author']['name']}\n"
                                                f"Watch it here: {video_url}")
                elif first_result['type'] == 'image':
                    image_url = first_result['url']
                    bot.send_photo(m.chat.id, image_url, caption=f"Title: {first_result['title']}\n"
                                                                  f"Description: {first_result['description']}\n"
                                                                  f"Views: {first_result['views']}\n"
                                                                  f"Channel: {first_result['author']['name']}")
                else:
                    bot.reply_to(m, "Unsupported media type.")
            else:
                bot.reply_to(m, f"No results found for '{query}'.")

        except requests.RequestException as e:
            bot.reply_to(m, f"An error occurred while fetching data: {e}")
