import telebot
#from .auth import apikey
from .rag import *
from telebot.async_telebot import AsyncTeleBot
from .utils import *
from celery import shared_task 
from bot_src.constants import *
from .auth import *
import asyncio

bot = telebot.TeleBot(default_apikey, parse_mode=None)


class TelegramBot:

    def __init__(self, api_key=default_apikey, email=None, bot_id=None):
        self.api_key = api_key
        self.bot =  telebot.TeleBot(self.api_key, parse_mode=None)
        self.owner_email = email
        self.bot_id = bot_id
        self.handlers() 
    def handlers(self):

        @self.bot.message_handler(commands=['get_chat_id'])
        def get_chat_id(message):
            self.bot.reply_to(message, f" chat_id :{message.chat.id}\nchat_type{message.chat.type}")

    def check_type(self, message):
        return message.chat.type
        
    def run(self):
        self.bot.infinity_polling()
    
    
    def stop(self):
        self.bot.stop_bot()

class BotHandler(TelegramBot):
    
    def __init__(self, api_key=default_apikey, email=None, bot_id=None, collection_id=None, task_id=None):
        super().__init__(api_key, email, bot_id)
        
        self.group = None
        self.private = None
        self.collection_id = collection_id
        self.bot_client = None
        self.task_id=task_id
        self.private_chat_id = None
        

    def handlers(self):
        super().handlers()
        @self.bot.message_handler(commands=['start', 'help'])
        def send_message(message):
            self.bot.reply_to(message=message, text='how can i help you?')
        
        @self.bot.message_handler(commands=['register'])
        def register(message):
            print(message)
            msg = self.bot.reply_to(message,"Email Address : ")
            self.bot_client = BotClient(
                bot = self.bot
            )
            self.bot.register_next_step_handler(msg, self.bot_client.submit_email)
        
        @self.bot.message_handler(commands=['login'])
        def login(message):
            msg = self.bot.reply_to(message, "Email Address")

            self.bot_client = BotClient(
                bot = self.bot
            )
            self.bot.register_next_step_handler(msg, self.bot_client.submit_password)




        @self.bot.message_handler(commands=['query'])
        def bookworm(message):
            response = check_conversation(query=message.text)
            #print(response)
            self.bot.reply_to(message=message, text=response)

    
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
        
        @self.bot.message_handler(
                content_types=['document'])
        def add_document(message):
            print(message.json)

        @self.bot.message_handler(commands=['remove_document'])
        def remove_document(message):
            pass

        @self.bot.message_handler(commands=['set_prompt'])
        def set_prompt(message):
            pass


    
  
    




