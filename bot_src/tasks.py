from celery import shared_task 
from telegram.bot import *
@shared_task
def execute_bot(api_key=None, collection_id=None, email=None, bot_id=None):
    run = BotHandler(
            api_key=api_key,
            collection_id=collection_id,
            email=email,
            bot_id = bot_id
            )
    run.run()

    return "Pooling"