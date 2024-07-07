import random

# Simple user-agent generator for demonstration purposes
def generate_user_agents(amount):
    user_agents = []
    for _ in range(amount):
        browser = random.choice(["Firefox", "Chrome", "Safari", "Opera", "Edge"])
        version = random.randint(50, 100)
        os = random.choice(["Windows", "Macintosh", "Linux"])
        user_agent = f"{browser}/{version} ({os})"
        user_agents.append(user_agent)
    return user_agents

def init(bot, send_typing_action):
    @bot.message_handler(commands=['generateua'])
    @send_typing_action
    def handle_generateua(message):
        try:
            amount = int(message.text.split()[1])
            user_agents = generate_user_agents(amount)
            file_path = 'plugins/temp/docs/ua.txt'
            with open(file_path, 'w') as f:
                f.write("\n".join(user_agents))
            bot.send_document(message.chat.id, open(file_path, 'rb'))
        except (IndexError, ValueError):
            bot.reply_to(message, "Usage: /generateua <amount>")
