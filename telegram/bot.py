import telebot
from .rag import *
from .utils import *
from .bot_client import BotClient
from bot_src.constants import *

class BookWorm(BotClient):
    def __init__(self, email=None, bot_id=None, token=default_apikey):
        super().__init__(token)
        self.owner_email = email
        self.bot_id = bot_id
        self.bot_client = None
        self.docs = []
        self.handlers()

    def handlers(self):
        @self.message_handler(commands=['get_chat_id'])
        def get_chat_id(message):
            self.reply_to(message, f"chat_id: {message.chat.id}\nchat_type: {message.chat.type}")

        @self.message_handler(commands=['start', 'help'])
        def send_message(message):
            self.reply_to(message, 'How can I help you?')

        @self.message_handler(commands=['register'])
        def register(message):
            # self.bot_client = AuthUser(bot=self.bot)
            msg = self.reply_to(message, "Email Address:")
            self.register_next_step_handler(msg, self.submit_email)

        @self.message_handler(commands=['login'])
        def login(message):
            msg = self.reply_to(message, "Email Address:")
            self.register_next_step_handler(msg, self.submit_password)

        @self.message_handler(commands=['query'])
        def bookworm(message):
            response = check_conversation(query=message.text)
            self.reply_to(message, response)

        @self.message_handler(commands=['profile'])
        def profile(message):
            self.reply_to(message, self.email)
                

        @self.message_handler(commands=['create_collection'])
        def create_collection(message):
            msg = self.reply_to(message, "Please enter the collection name:")
            self.register_next_step_handler(msg, self.process_collection_name)
            

        @self.message_handler(content_types=['document'])
        def add_document(message):
            # Implement document handling logic here
            self.reply_to(message, "Document received. Processing...")

        @self.message_handler(commands=['remove_document'])
        def remove_document(message):
            # Implement document removal logic here
            self.reply_to(message, "Please specify the document to remove.")

        @self.message_handler(commands=['set_prompt'])
        def set_prompt(message):
            # Implement prompt setting logic here
            self.reply_to(message, "Please enter the new prompt:")

    def process_collection_name(self, message):
        # Implement collection creation logic here

        # we need to check that the text is not empty
        collection_name = message.text
        self.chat_id = message.chat.id

        self.collection_data = {
            "chat": self.chat_id,
            "collection_name":collection_name,
            "documents": []
        }

        # Add code to create the collection
        msg = self.reply_to(message, "Document:")
        self.register_next_step_handler(msg,self.add_document)


    def add_document(self, message):
    
        docs = self.get_document(message.document)

        self.collection_data["documents"].append(docs)
        
        msg = self.reply_to(message, "Add another document (yes or no)")

        self.register_next_step_handler(msg,self.plus_docs)

    
    def plus_docs(self, message):
        if message.text.lower() == "yes":

            msg = self.reply_to(message, "Document:")
            self.register_next_step_handler(msg,self.add_document)
        
        elif message.text.lower() == "no":
            response = self.send_collection_(self.collection_data)

        else:
            self.reply_to(msg, "the correct options are yes or no")
            

    
    def get_document(self, document):
        
        file = self.get_file(document.file_id)
        print(file.file_path)

        downloaded_file = self.download_file(file.file_path)


        return {
            "file_name":document.file_name,
            "file":downloaded_file
        }


            
    

    def run(self):
        self.infinity_polling()

    def stop(self):
        self.stop_bot()