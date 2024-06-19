from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'bot', BotAPIViewSet, basename='collection')
router.register(r'telegram', TelegramGroupViewSet, basename='telegram')
urlpatterns = [
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('create_collection/', CreateCollectionView.as_view(), name='create_collection'),
    path('create_datasource/', CreateDataSourceView.as_view()),
   

]+router.urls