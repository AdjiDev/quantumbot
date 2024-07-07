import random

def init(bot, send_typing_action):
    @bot.message_handler(commands=['genproxy'])
    @send_typing_action
    def handle_genproxy(message):
        try:
            amount = int(message.text.split()[1])
        except (IndexError, ValueError):
            bot.reply_to(message, "Usage: /genproxy <amount>")
            return
        
        proxies = generate_proxies(amount)
        save_proxies_to_file(proxies, 'plugins/temp/proxy.txt')
        with open('plugins/temp/proxy.txt', 'rb') as file:
            bot.send_document(message.chat.id, file)

def generate_proxies(amount):
    proxies = []
    for _ in range(amount):
        proxy = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}:{random.randint(1000, 9999)}"
        proxies.append(proxy)
    return proxies

def save_proxies_to_file(proxies, filename):
    with open(filename, 'w') as file:
        for proxy in proxies:
            file.write(proxy + '\n')
