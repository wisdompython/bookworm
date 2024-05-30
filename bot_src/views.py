from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser, FileUploadParser
from rest_framework.generics import CreateAPIView, GenericAPIView, DestroyAPIView
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from celery import shared_task 
from asgiref.sync import sync_to_async
from telegram.bot import *
from .tasks import *
from .models import *
from .serializers import *


class RegisterTelegramGroupView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TelegramGroupSerializer

class CreateCollectionView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Collection.objects.all()
    serializer_class = CreateCollectionSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.email)
    

class CreateDataSourceView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    serializer_class = DataSourceSerializer
    queryset = DataSource.objects.all()

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            files = request.FILES.getlist('document')
            print(files)
            print(files)
            get_collection = (Collection.objects.get(title=serializer.data['collection_title']))
            for file in files:
                new_document = DataSource.objects.create(
                    document_name=file.name,
                    collection=get_collection, file=file)

            return Response("created")
        return Response(serializer.errors)

# interact with bot

class BotAPIViewSet(ViewSet):

    def create(self,request):

        serializer = RegisterBotSerializer(data=request.data)
        permission_classes = (IsAuthenticated,)

        if serializer.is_valid():
            bot = Bot.objects.create(
                api_key = serializer.data['api_key'],
                bot_name = serializer.data['bot_name'],
                owner = request.user
            )

            bot.save
            return Response(
                serializer.data
            )
        return Response(serializer.errors)
            
        

    @action(methods=['get'], permission_classes=[IsAuthenticated], detail=False)
    async def get_instructions(self, request):

        return Response(
            f"""1. Interact with Bot at https://t.me/bk_worm_bot\n
                2. Add the bot to your group chat\n
                3. use this command to get your group id : /register_group <your email_address>\n
                   *make sure you use the same email address as the one you used to set up your account*\n
                """        
            )
    
    
    @action(methods=['post'], permission_classes=[IsAuthenticated], detail=False)
    def start_bot(self, request):
        serializers = StartBotSerializer(data=request.data)
        if serializers.is_valid():
            bot = Bot.objects.get(owner=request.user)

            collection = Collection.objects.get(title = serializers.data['collection_title'])
            execute_bot.delay(bot.api_key, collection.id, request.user.email, bot_id= bot.id)

            return Response("Polling Started")
        return Response(serializers.errors)
    
    @action(methods=['get'], permission_classes=[IsAuthenticated], detail=False)
    def stop_bot(self, request):
    
        bot = Bot.objects.get(owner=request.user)
        stop = BotHandler(
            api_key=bot.api_key
        )
        asyncio.create_task(stop.stop())

        return Response("Polling Ended")
    

