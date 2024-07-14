import requests
from telebot import TeleBot
import os

def handle_pinterest_command(bot: TeleBot):
    @bot.message_handler(commands=['pinterest'])
    def pinterest_command(m):
        query = m.text[len('/pinterest '):].strip()
        if not query:
            bot.reply_to(m, "Please provide a search query.")
            return

        try:
            response = requests.get(f"https://api.junn4.my.id/search/pinterest?query={query}")
            response.raise_for_status()
            data = response.json()

            if data['status'] == "true" and 'result' in data and data['result']:
                image_url = data['result'][0]
                image_response = requests.get(image_url)
                image_response.raise_for_status()

                with open("pinterest_image.jpg", "wb") as img_file:
                    img_file.write(image_response.content)

                with open("pinterest_image.jpg", "rb") as img_file:
                    bot.send_photo(m.chat.id, img_file, caption=f"Result for '{query}':")

                os.remove("pinterest_image.jpg")
            else:
                bot.reply_to(m, f"No results found for '{query}'.")

        except requests.RequestException as e:
            bot.reply_to(m, f"An error occurred while fetching data: {e}")

def handle_downloadimage_command(bot: TeleBot):
    @bot.message_handler(commands=['downloadimage'])
    def downloadimage_command(m):
        pinterest_url = m.text[len('/downloadimage '):].strip()
        if not pinterest_url:
            bot.reply_to(m, "Please provide a Pinterest URL.")
            return

        try:
            image_response = requests.get(pinterest_url)
            image_response.raise_for_status()

            with open("downloaded_image.jpg", "wb") as img_file:
                img_file.write(image_response.content)

            with open("downloaded_image.jpg", "rb") as img_file:
                bot.send_photo(m.chat.id, img_file, caption=f"Downloaded image from: {pinterest_url}")

            os.remove("downloaded_image.jpg")

        except requests.RequestException as e:
            bot.reply_to(m, f"An error occurred while downloading the image: {e}")

