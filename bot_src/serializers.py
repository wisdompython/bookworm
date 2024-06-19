from rest_framework import serializers
from .models import *

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()
    data_source = serializers.CharField(max_length=200)
    chat_history = serializers.ListField()
    

class CreateCollectionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=300)
    description = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        collection = Collection.objects.create(
            title= validated_data['title'],
            description = validated_data['description'],
            owner = self.context['request'].user
            
        )

        return collection
    

class DataSourceSerializer(serializers.Serializer):
    collection_title = serializers.CharField(max_length=300)
    document = serializers.ListField(
        child = serializers.FileField()
    )

    
class TelegramGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TelegramGroup
        fields = ('group_id','group_name', 'private','group')

    

class RegisterBotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bot
        fields = ("api_key", "bot_name")

class StartBotSerializer(serializers.Serializer):
    collection_title = serializers.CharField(max_length=300)
    bot_id = serializers.IntegerField()
    as_admin = serializers.BooleanField(default=False)

class StopBotSerializer(serializers.Serializer):
   bot_instance_id = serializers.IntegerField()
        
        