from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser, FileUploadParser
from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from celery import shared_task 
from asgiref.sync import sync_to_async
from study_bot.celery import app
from telegram.bot import *
from .tasks import *
from .models import *
from .serializers import *

class CustomAuth(TokenAuthentication):
    keyword = 'Bearer'


class TelegramGroupViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuth, JWTAuthentication, TokenAuthentication, BasicAuthentication]
    serializer_class = TelegramGroupSerializer
    queryset = TelegramGroup.objects.all()

    


class CollectionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    queryset = Collection.objects.all()
    serializer_class = CreateCollectionSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    

class DataSourceViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    parser_classes = [MultiPartParser]
    serializer_class = DataSourceSerializer
    queryset = DataSource.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

class BotAPIViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    serializer_class = RegisterBotSerializer
    
    @action(methods=['get'], permission_classes=[IsAuthenticated], detail=False)
    def create_conversation(self, request):
        pass
        

    @action(methods=['get'], permission_classes=[IsAuthenticated], detail=False)
    async def get_instructions(self, request):

        return Response(
            f"""1. Interact with Bot at https://t.me/bk_worm_bot\n
                2. Add the bot to your group chat\n
                3. use this command to get your group id : /register_group <your email_address>\n
                   *make sure you use the same email address as the one you used to set up your account*\n"""        
            )
    
    
    @action(methods=['post'], permission_classes=[IsAuthenticated], detail=False)
    def start_bot(self, request):
        serializers = StartBotSerializer(data=request.data)
        if serializers.is_valid():
            bot = Bot.objects.get(id=serializers.data['bot_id'])
            collection = Collection.objects.get(title = serializers.data['collection_title'])
            run_bot = execute_bot.delay()
            print(run_bot)
            bot_instance = BotInstance.objects.create(bot=bot, task_id=run_bot)
            bot_instance.save()
            return Response({
                "bot_id": bot.id
            })
            
        return Response(serializers.errors)


    @action(methods=['post'], permission_classes=[IsAuthenticated], detail=False)
    def stop_bot(self, request):
        serializers = StopBotSerializer(data=request.data)
        if request.user.is_admin:
            if serializers.is_valid():
                bot_instance = BotInstance.objects.get(id=serializers.data['bot_instance_id'])
                print(bot_instance.task_id)
                bot = stop_admin_bot.delay(task_id=bot_instance.task_id)
           
            
                app.control.revoke(bot_instance.task_id, terminate=True)

            return Response("BookWorm stopped")
        return Response("You cannot perform this action, contact the admin")
    
    

class TelegramGroups(ModelViewSet):
    queryset = TelegramGroup