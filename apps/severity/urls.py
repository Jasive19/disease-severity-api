from django.urls import path
from .views import *

urlpatterns = [
    path('/load-h5/', LoadModel.predictH5),
]


