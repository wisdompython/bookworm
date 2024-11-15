
import requests
import telebot

default_api_url = "http://localhost:8000"

class BotClient(telebot.TeleBot):
    def  __init__(self, token):
        super().__init__(token)
        self.email = None
        self.password = None
        self.confirm_password = None

    def submit_email(self, message):
        self.email = message.text
        msg = self.reply_to(message, "Password:")
        self.register_next_step_handler(msg, self.set_password)

    def set_password(self, message):
        self.password = message.text
        msg = self.reply_to(message, "Confirm password:")
        self.register_next_step_handler(msg, self.submit_confirm_password)

    def submit_password(self, message):
        self.email = message.text
        msg = self.reply_to(message, "Password:")
        self.register_next_step_handler(msg, self.login)

    def submit_confirm_password(self, message):
        self.confirm_password = message.text
        create_user = self.register(endpoint='register')
        self.reply_to(message, create_user.text)


    def register(self, endpoint, api_url=default_api_url):
        response = requests.post(
            url=f"{api_url}/{endpoint}/",
            data={
                "email": self.email,
                "password": self.password,
                "confirm_password": self.confirm_password
            }
        )
        return response

    def login(self,message, endpoint='getapikey', api_url=default_api_url):
        self.password = message.text
        url = f"{api_url}/{endpoint}/"
        response = requests.get(
            url=url,
            auth=(self.email, self.password)
        )
        print(response)
        print(response.json())
        self.api_key = response.json()
        self.reply_to(message, f"login successful, token : {self.api_key}")
    
    
    def send_collection_(self, data):    
        response = requests.post(
            url=f"{default_api_url}/collection/",
            data=data
        )
        return response

        
    def get_api_key(self, api_url=default_api_url, endpoint="getapikey"):
        url = f"{api_url}/{endpoint}/"
        response = requests.get(
            url=url,
            auth=(self.email, self.password)
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get API key: {response.text}")
    
    

