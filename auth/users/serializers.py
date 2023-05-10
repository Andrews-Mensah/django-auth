from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    
    
    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     if password is not None:
    #        hPassword = make_password(password)
    #        User.save(hPassword)