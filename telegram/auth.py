import requests
from http import *
default_api_url = "http://localhost:8000"
import base64


class BotClient:

    def __init__(self, email=None, password=None, confirm_password=None, bot=None):
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
        self.access_token = None
        self.refresh_token=None
        self.headers = None
        self.is_authenticated = None
        self.bot = bot
    
   

    def submit_email(self,message):
        self.email = message.text
        print(self.email)
        msg = self.bot.reply_to(message,"Password:")
        self.bot.register_next_step_handler(msg, self.set_password)

    def set_password(self,message):
        self.password = message.text
        msg = self.bot.reply_to(message, "confirm password:")
        self.bot.register_next_step_handler(msg, self.submit_confirm_password)

    def submit_password(self,message):
        self.email = message.text
        msg = self.bot.reply_to(message, "password")
        self.bot.register_next_step_handler(msg, self.exec_login)

    def submit_confirm_password(self, message):
        self.confirm_password = message.text
        create_user = self.register(endpoint='register')
        msg = self.bot.reply_to(message, create_user)


    def exec_login(self, message):
        self.password = message.text
        response = self.login(endpoint='getapikey')
        self.bot.reply_to(message, f"Here is your api key {response.json()}")
    
    def register(self, endpoint, api_url=default_api_url):      
        response = requests.post(
            url=f"{api_url}/{endpoint}/", data={
                "email":self.email, "password":self.password, "confirm_password":self.confirm_password
            }
        )

        return response
    
    def login(self, endpoint, api_url=default_api_url):
        print(endpoint)
        url = f"{api_url}/{endpoint}/"
        print(url)
        data =f"{self.email}:{self.password}"
       
        response = requests.get(
            url=url, auth=(self.email, self.password)
        )

        return response