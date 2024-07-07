from telebot import types

def is_admin(bot, chat_id, user_id):
    chat_member = bot.get_chat_member(chat_id, user_id)
    return chat_member.status in ['administrator', 'creator']

def init(bot, send_typing_action):
    @bot.message_handler(commands=['ban'])
    @send_typing_action
    def handle_ban(message):
        if not is_admin(bot, message.chat.id, message.from_user.id):
            bot.reply_to(message, "You need to be an admin to use this command.")
            return

        try:
            user_id = int(message.text.split()[1])
        except (IndexError, ValueError):
            bot.reply_to(message, "Usage: /ban <user_id>")
            return
        
        try:
            bot.kick_chat_member(message.chat.id, user_id)
            bot.reply_to(message, f"User {user_id} has been banned.")
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")

    @bot.message_handler(commands=['unban'])
    @send_typing_action
    def handle_unban(message):
        if not is_admin(bot, message.chat.id, message.from_user.id):
            bot.reply_to(message, "You need to be an admin to use this command.")
            return

        try:
            user_id = int(message.text.split()[1])
        except (IndexError, ValueError):
            bot.reply_to(message, "Usage: /unban <user_id>")
            return
        
        try:
            bot.unban_chat_member(message.chat.id, user_id)
            bot.reply_to(message, f"User {user_id} has been unbanned.")
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")

    @bot.message_handler(commands=['allowsendmsg'])
    @send_typing_action
    def handle_allowsendmsg(message):
        if not is_admin(bot, message.chat.id, message.from_user.id):
            bot.reply_to(message, "You need to be an admin to use this command.")
            return

        try:
            allow = message.text.split()[1].lower() == 'true'
        except IndexError:
            bot.reply_to(message, "Usage: /allowsendmsg <true/false>")
            return
        
        permissions = types.ChatPermissions(can_send_messages=allow)
        try:
            bot.set_chat_permissions(message.chat.id, permissions)
            bot.reply_to(message, f"Sending messages is now {'allowed' if allow else 'disallowed'}.")
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")
