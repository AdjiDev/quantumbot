from telebot import TeleBot
from telebot.types import ChatMemberStatus
import os

def handle_group_commands(bot: TeleBot):
    
    @bot.message_handler(commands=['ban'])
    def ban_user(m):
        if not m.reply_to_message:
            bot.reply_to(m, "You need to reply to the user's message to ban them.")
            return
        
        user_id = m.reply_to_message.from_user.id
        chat_id = m.chat.id
        
        try:
            bot.kick_chat_member(chat_id, user_id)
            bot.reply_to(m, "User banned successfully.")
        except Exception as e:
            bot.reply_to(m, f"Failed to ban user: {e}")
    
    @bot.message_handler(commands=['unban'])
    def unban_user(m):
        if len(m.text.split()) != 2:
            bot.reply_to(m, "Usage: /unban <user_id>")
            return
        
        user_id = int(m.text.split()[1])
        chat_id = m.chat.id
        
        try:
            bot.unban_chat_member(chat_id, user_id)
            bot.reply_to(m, "User unbanned successfully.")
        except Exception as e:
            bot.reply_to(m, f"Failed to unban user: {e}")
    
    @bot.message_handler(commands=['kick'])
    def kick_user(m):
        if not m.reply_to_message:
            bot.reply_to(m, "You need to reply to the user's message to kick them.")
            return
        
        user_id = m.reply_to_message.from_user.id
        chat_id = m.chat.id
        
        try:
            bot.kick_chat_member(chat_id, user_id)
            bot.reply_to(m, "User kicked successfully.")
        except Exception as e:
            bot.reply_to(m, f"Failed to kick user: {e}")
    
    @bot.message_handler(commands=['add'])
    def add_user(m):
        if len(m.text.split()) != 2:
            bot.reply_to(m, "Usage: /add <user_id or @username>")
            return
        
        identifier = m.text.split()[1]
        chat_id = m.chat.id
        
        try:
            if identifier.startswith('@'):
                username = identifier
                member = bot.get_chat_member(chat_id, username)
                user_id = member.user.id
            else:
                user_id = int(identifier)
            
            bot.unban_chat_member(chat_id, user_id) 
            bot.reply_to(m, "User added successfully.")
        except Exception as e:
            bot.reply_to(m, f"Failed to add user: {e}")
