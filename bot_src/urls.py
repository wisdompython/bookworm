from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'bot', BotAPIViewSet, basename='bot')
router.register(r'telegram', TelegramGroupViewSet, basename='telegram')
router.register(r'collection', CollectionViewSet, basename='collection')
router.register(r'datasources', DataSourceViewSet, basename='datasources')
urlpatterns=router.urls