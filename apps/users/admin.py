from django.contrib import admin
from django.contrib.auth.models import Group
from apps.users.models import User

admin.site.unregister(Group)  # new
admin.site.register(User)