from django.shortcuts import render
import json
from django.conf import settings
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, viewsets
from . models import User
from . serializers import UserSerializer
from django.http import HttpResponse
from rest_framework.views import APIView



class UserViewSet(viewsets.ModelViewSet): # Отображает список и CRUD-операции (Sqlite)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({"user": 'delete user' + ' ' + kwargs["pk"]})

# Создаем экземпляр Redis
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

def create_in_memory_db(request): # Наполняем базу данных Redis
    users = [
        (1, 'Иванов Федор Николаевич'),
        (2, 'Ментшов Дмитрий Олегович'),
        (3, 'Смирнов Петр Андреевич'),
        (4, 'Ковылев Сергей Владимирович'),
        (5, 'Рыжов Олег Петрович'),
        (6, 'Петрова Людмила Георгиевна'),
        (7, 'Филипова Анна Викторовна'),
        (8, 'Светлова Екатерина Павловна'),
        (9, 'Ильин Олег Федорович'),
        (10, 'Обоймов Николай Васильевич'),
        (11, 'Морозова Людмила Дмитриевна')
    ]

    for i in users:
        redis_instance.set(i[0], i[1])

    return HttpResponse('Была создана база данных Redis')


@api_view(['GET', 'POST'])
def manage_items(request, *args, **kwargs): # Отображает список и добавляет запись (Redis)
    if request.method == 'GET':
        items = {}
        count = 0
        for key in redis_instance.keys("*"):
            items[key.decode("utf-8")] = redis_instance.get(key)
            count += 1
        response = {
            'count': count,
            'msg': f"Found {count} items.",
            'items': items
        }
        return Response(response, status=200)
    elif request.method == 'POST':
        item = json.loads(request.body)
        key = list(item.keys())[0]
        value = item[key]
        redis_instance.set(key, value)
        response = {
            'msg': f"{key} successfully set to {value}"
        }
        return Response(response, 201)


@api_view(['GET', 'PUT', 'DELETE']) # GET, PUT, DELETE для записи (Redis)
def manage_item(request, *args, **kwargs):
    if request.method == 'GET':
        if kwargs['id']:
            value = redis_instance.get(kwargs['id'])
            if value:
                response = {
                    'id': kwargs['id'],
                    'value': value,
                    'msg': 'success'
                }
                return Response(response, status=200)
            else:
                response = {
                    'id': kwargs['id'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)
    elif request.method == 'PUT':
        if kwargs['id']:
            request_data = json.loads(request.body)
            new_value = request_data['new_value']
            value = redis_instance.get(kwargs['id'])
            if value:
                redis_instance.set(kwargs['id'], new_value)
                response = {
                    'id': kwargs['id'],
                    'value': value,
                    'msg': f"Successfully updated {kwargs['id']}"
                }
                return Response(response, status=200)
            else:
                response = {
                    'id': kwargs['id'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)

    elif request.method == 'DELETE':
        if kwargs['id']:
            result = redis_instance.delete(kwargs['id'])
            if result == 1:
                response = {
                    'msg': f"{kwargs['id']} successfully deleted"
                }
                return Response(response, status=404)
            else:
                response = {
                    'id': kwargs['id'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)