import telebot
#from .auth import apikey
from .rag import *
from telebot.async_telebot import AsyncTeleBot
from .utils import *
from celery import shared_task 
from bot_src.constants import *
import asyncio

bot = telebot.TeleBot(default_apikey, parse_mode=None)


class BotHandler():

    def __init__(self, api_key=default_apikey, email=None, bot_id=None, collection_id=None):
        self.api_key = api_key
        self.bot =  telebot.TeleBot(self.api_key, parse_mode=None)
        self.collection_id = collection_id
        self.owner_email = email
        self.bot_id = bot_id
        self.group = None
        self.private = None
        # self.is_authenticated = False
        self.handlers() 

    def handlers(self):
        @self.bot.message_handler(commands=['start', 'help'])
        def send_message(message):
            
            self.bot.reply_to(message=message, text='how can i help you?')


        @self.bot.message_handler(commands=['query'])
        def bookworm(message):
            response = check_conversation(query=message.text)
            #print(response)
            self.bot.reply_to(message=message, text=response)
            pass
        @self.bot.message_handler(commands=['add_group'])
        def add_group(message):
            if message.chat.type == "group":
                from_user = message.from_user.id
                for admin in bot.get_chat_administrators(message.chat.id):
                    if from_user == admin.user.id and admin.status == 'creator':
                        tg = register_group_to_model(tg_name=message.chat.title, tg_id=message.chat.id, owner=self.owner_email, chat_type='group')
                        self.bot.reply_to(message=message, text=tg)
                    else :
                        self.bot.reply_to(message=message,text= "This operation can only be done by group creators")
            # get the message id
            else:
                self.bot.reply_to(message=message,text= "This operation can only be done in a group")
            

        @self.bot.message_handler(commands=['register_private_chat'])
        def register_private_chat(message):
            
            if message.chat.type == "private":
                from_user = message.from_user.id
                tg = register_group_to_model(tg_name=message.chat.username, 
                                             tg_id=message.chat.id, owner=self.owner_email, 
                                             chat_type='private')
            else:
                self.bot.reply_to(
                    message=message, text="This operation can only be done in private chats"
                )
        
        @self.bot.message_handler(commands=['add_document'], content_types=["document"])
        def add_document(message):
            pass

    

    
    def run(self):
        self.bot.infinity_polling()
    
    def stop(self):
        self.bot.stop_bot()








@bot.message_handler(commands=['start', 'help'])
def send_message(message):
    
    print(message)
    bot.reply_to(message=message, text='how can i help you?')

@bot.message_handler(commands=['add_group'])
def add_group(message):
    print(message)
            # get the message id
    if message.chat.type == "group":
        from_user = message.from_user.id

        for admin in bot.get_chat_administrators(message.chat.id):
            if from_user == admin.user.id and admin.status == 'creator':
                print(
                    f"sent : {from_user}\n{admin.user.id}\n{admin.status}"
                )
                print('we grabbed him')
        # grab the chat_id
    

# @bot.message_handler(commands=['query'])
# def bookworm(message):
#     response = load_collection(message.text)
#     print(response)
#     bot.reply_to(message=message, text=response)

# @bot.message_handler(commands=['add_group'])

# def bookworm(message):
#     pass


# @bot.message_handler(commands=['verify'])
# def verify_client_watched_yt_video(message):
#     print('cool')


# @bot.message_handler(commands=["add_document_to_nodes"], content_types='document')
# def add_document(document):
#     pass   


# @bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
#                 'text', 'location', 'contact', 'sticker'])
# def all_message(message):
#     print(message.text)
#     bot.reply_to(message=message, text='Thank you for contacting us')







#bot.infinity_polling()