from django.urls import path
from apps.analysis.views import (update, index, show, create, delete)

urlpatterns = [
  path('update/<int:id>', update , name = 'analysis_update_api' ),
  path('detail/<int:id>', show , name = 'analysis_detail_api'),
  path('delete', delete , name = 'analysis_delete_api'),
  path('create', create , name = 'analysis_create_api'),
  path('list', index , name = 'analysis_list_api' ),
]
