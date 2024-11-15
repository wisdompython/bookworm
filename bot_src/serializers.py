from rest_framework import serializers
from .models import *

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()
    data_source = serializers.CharField(max_length=200)
    chat_history = serializers.ListField()

class DataSourceSerializer(serializers.Serializer):
    collection_title = serializers.CharField(max_length=300)
    document = serializers.ListField(
        child = serializers.FileField()
    )

    def create(self, validated_data):
        documents = validated_data.pop("document")

        collection, created = Collection.objects.get_or_create(title=validated_data['collection_title'])

        for file in documents:
            DataSource.objects.create(
                document_name = file.name,
                collection = collection,
                file=file
            )
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
class TelegramGroupSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), queryset = CustomUser.objects.all()
    )
    class Meta:
        model = TelegramGroup
        fields = ('group_id','group_name', "chat_type")


class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation

    

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
        
        