import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from telebot import TeleBot

def handle_ssweb_command(bot: TeleBot):
    @bot.message_handler(commands=['ss'])
    def ss_command(m):
        if len(m.text.split()) != 2:
            bot.reply_to(m, "Usage: /ss <url>")
            return

        url = m.text.split()[1]
        screenshot_path = f"../tmp/screenshot_{m.chat.id}.png"

        try:
            # Set up Selenium Chrome driver
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            
            driver.get(url)
            driver.set_window_size(1920, 1080)
            driver.save_screenshot(screenshot_path)
            driver.quit()
            
            with open(screenshot_path, 'rb') as screenshot:
                bot.send_photo(m.chat.id, screenshot, caption=f"Screenshot of {url}")

            os.remove(screenshot_path)

        except Exception as e:
            bot.reply_to(m, f"An error occurred while taking the screenshot: {e}")
