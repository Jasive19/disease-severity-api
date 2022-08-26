from django.contrib import admin
from django.urls import path, include
from apps.severity.views import *

urlpatterns = [
    path('api/v1/user/', include('apps.users.api.urls')),
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/analysis/', include('apps.analysis.urls')),
    path('admin/', admin.site.urls),
    path('', Welcome.home),
]   