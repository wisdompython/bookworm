# from .bot import *
# import requests
# from http.client import *
# default_api_url = f"http://localhost:8000"



# class AdminBot(BotHandler):
#     def __init__(self, api_key=default_apikey, email=None, bot_id=None, collection_id=None, task_id=None):
#         super().__init__(api_key, email, bot_id)
        
#         self.task_id = None
#         self.api_key=api_key

    
#     def handlers(self):
#         super().handlers()

#         @self.bot.message_handler(commands=['user_register'])
#         def user_register(message):
#             print(message)
#             msg = self.bot.reply_to(message,"Email Adress : ")
#             self.bot.register_next_step_handler(msg, self.submit_email)


#         @self.bot.message_handler(commands=['hello'])
#         def hello(message):
#             self.bot.reply_to(message,'hello')


#     def submit_email(self,message):
#         self.user_email = message.text
#         msg = self.bot.reply_to(message,"Password:")
#         self.bot.register_next_step_handler(msg, self.submit_password)

#     def submit_password(self,message):
#         self.user_password = message.text
#         msg = self.bot.reply_to(message, "confirm password:")
#         self.bot.register_next_step_handler(msg, self.submit_confirm_password)

#     def submit_confirm_password(self, message):
#         self.confirm_password = message.text
#         create_user = self.create_user(self.user_email, self.user_password, self.confirm_password )
#         msg = self.bot.reply_to(message, create_user)

#     def create_user(self, email, password, confirm_password, api_url=default_api_url, endpoint=None):

#         response = requests.post(
#             url=f"{api_url}/{endpoint}", data={
#                 "email":email, "password":password, "confirm_password":confirm_password
#             }
#         )
    
#     def login(self, email, password):
#         pass
    



