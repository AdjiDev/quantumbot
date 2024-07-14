import requests
from telebot import TeleBot, types

def handle_mediafire_command(bot: TeleBot):
    @bot.message_handler(commands=['mediafire'])
    def mediafire_command(message):
        bot.reply_to(message, "Please provide a MediaFire file URL.")

    @bot.message_handler(func=lambda message: message.text.startswith('/mediafire '))
    def handle_mediafire_url(message):
        url = message.text.split('/mediafire ')[1].strip()
        process_mediafire_file(bot, message, url)

def process_mediafire_file(bot, message, url):
    try:
        api_url = f"https://api.junn4.my.id/download/mediafire?url={url}"
        response = requests.get(api_url)
        data = response.json()

        if data['status'] == 200:
            filename = data['result']['filename']
            filetype = data['result']['filetype']
            download_link = data['result']['link']
            details = data['result']['detail']

            reply_text = f"Filename: {filename}\n" \
                         f"Filetype: {filetype}\n" \
                         f"Details: {details}\n" \
                         f"Download Link: {download_link}"

            bot.reply_to(message, reply_text)
        else:
            bot.reply_to(message, "Failed to retrieve MediaFire download link. Please check the URL and try again.")

    except requests.RequestException as e:
        bot.reply_to(message, f"An error occurred while processing the request: {e}")

