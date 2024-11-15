from django.db import models
from users.models import *
import os
import uuid


def get_upload_path(instance, filename):
      return os.path.join('collections', instance.collection.title, filename)

# many do
class DataSource(models.Model):
    document_name = models.CharField(max_length=200)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE, related_name='collection_data', null=True)
    file = models.FileField(upload_to=get_upload_path)

    def __str__(self):
        return self.document_name
    
class Bot(models.Model):
    api_key = models.CharField(max_length=300, unique=True)
    bot_name = models.CharField(max_length=300)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class BotInstance(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    task_id = models.TextField(null=True)

    def __str__(self):
        return f"id :{self.id}"
    

class TelegramGroup(models.Model):
    chat_choices = [
        ("private", "private"),
        ("group", "group")
    ]
    group_name = models.CharField(max_length=300)
    group_id = models.IntegerField(unique=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat_type = models.CharField(max_length=30, choices=chat_choices)

class Collection(models.Model):
    id  = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    processing = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return self.title
    

class Conversation(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    group = models.ForeignKey(TelegramGroup, on_delete=models.CASCADE, null=True)
    
