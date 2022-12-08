from django.urls import path, include
from .views import manage_items, manage_item
from rest_framework import routers
from app1.views import UserViewSet, create_in_memory_db

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('api/list_and_post_from_redis/', manage_items), # отображает список и добавляет новую запись(Redis)
    path('api/item_redis/<int:id>/', manage_item), # PUT, GET, DELETE для записи(Redis)
    path('api/v1/', include(router.urls)), # отображает список и CRUD-операции (Sqlite)
    path('api/create_in_memory_db/', create_in_memory_db) # Наполняет базу данных в памяти (Redis)
]

