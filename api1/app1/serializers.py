from rest_framework import serializers
from . models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class UserModel:
    def __init__(self, id, full_name):
        self.id = id
        self.full_name = full_name



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name')