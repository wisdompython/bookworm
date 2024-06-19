from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register([
    Collection, DataSource, TelegramGroup,Bot, BotInstance
])