import time
import google.generativeai as genai
from PIL import Image
import os
import requests
from telebot import TeleBot, types

# Configure Generative AI with API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Global variable to track if Generative AI processing is enabled
generative_ai_enabled = True

def handle_genai_command(bot: TeleBot):
    @bot.message_handler(commands=['genai'])
    def genai_toggle_command(m):
        global generative_ai_enabled

        if len(m.text.split()) == 2:
            action = m.text.split()[1].lower()

            if action == 'on':
                generative_ai_enabled = True
                bot.reply_to(m, "Generative AI processing is now enabled.")
            elif action == 'off':
                generative_ai_enabled = False
                bot.reply_to(m, "Generative AI processing is now disabled.")
            else:
                bot.reply_to(m, "Invalid command. Use '/genai on' or '/genai off'.")

    @bot.message_handler(content_types=['photo', 'video'])
    def genai_command(m):
        global generative_ai_enabled
        
        try:
            if not generative_ai_enabled:
                return

            # Notify the user that the bot is processing
            bot.send_chat_action(m.chat.id, 'typing')
            time.sleep(2)  # Simulate typing action for 2 seconds

            file_id = None
            file_path = None

            if m.content_type == 'photo':
                file_id = m.photo[-1].file_id
            elif m.content_type == 'video':
                bot.reply_to(m, "Currently, only images are supported for description.")
                return

            if file_id:
                # Download and process the image/video
                file_info = bot.get_file(file_id)
                file_path = file_info.file_path

                file_url = f"https://api.telegram.org/file/bot{os.getenv('BOT_TOKEN')}/{file_path}"
                file_response = requests.get(file_url)
                file_bytes = file_response.content

                with open("temp_file", "wb") as f:
                    f.write(file_bytes)

                img = Image.open("temp_file")

                # Generate content description using Generative AI model
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                response = model.generate_content([m.caption or "Describe this image:", img])

                # Send the generated description as a reply
                bot.reply_to(m, response.text)

                # Clean up temporary file
                os.remove("temp_file")
            else:
                bot.reply_to(m, "Failed to retrieve the file.")
        
        except requests.RequestException as e:
            bot.reply_to(m, f"An error occurred while downloading the image: {e}")
        
        except genai.GenerationError as e:
            bot.reply_to(m, f"Error generating content: {e}")
        
        except Exception as e:
            bot.reply_to(m, f"An unexpected error occurred: {e}")

