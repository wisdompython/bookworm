from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserLoginSerializer(serializers.ModelSerializer):
    favorite_color = models.CharField()
    class Meta:
        model = CustomUser
        fields = ["id", "email", "password"]


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser  
        fields=("email", "password", "confirm_password")
        extra_kwargs = {'password': {'write_only': True}, 
                        "confirm_password":{'write_only':True}}
        
    def validate(self, attrs):                    
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
        try:
            validate_password(attrs['password'])
        except ValidationError as err:
            raise serializers.ValidationError(
            {"password": err.messages})
        return attrs
    
    def create(self, validated_data):

        
        
        new_user = CustomUser.objects.create(
            email = validated_data['email'],
        )
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user


