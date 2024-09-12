from celery import shared_task
from celery.contrib.abortable import AbortableTask
from telegram.bot import *
from telegram.auth import *
from study_bot.celery import app
default_collection ='cc08b5a5-e898-4f66-9215-21b7fd5c6f0c'


bookworm_object = None


# @shared_task(bind=True)
# def execute_bookworm(self):
#     global bookworm_object
#     bookworm_object = BookWorm().run()


    
@shared_task(bind=True)
def execute_bot(self,api_key=None, collection_id=None, email=None, bot_id=None):
    run = BookWorm(
            #collection_id=collection_id,
            email=email,
            bot_id = bot_id,
            )
    run.run()

    run.task_id = self.request.id
    print(type(run.task_id))
    print(run.task_id)
    return run.task_id


@shared_task(bind=True )
def stop_admin_bot(self, task_id):

    # admin_bot = AdminBot(
    # collection_id='cc08b5a5-e898-4f66-9215-21b7fd5c6f0c',
    # bot_id=1).stop()

    #print(admin_bot.task_id)

    return task_id