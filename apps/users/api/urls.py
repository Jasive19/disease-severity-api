from django.urls import path
from apps.users.api.api import ( UserViewSet, modify )
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('', UserViewSet, basename="users")

urlpatterns = [
  path('update', modify , name = 'user_update_api' ),
]
urlpatterns += router.urls