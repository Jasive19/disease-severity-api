from django.db import models
from django.conf import settings
import uuid

class Analysis(models.Model):
    id = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4, unique=True)
    result = models.CharField(max_length=50)  # label severity - example: COVID
    url = models.TextField()  # Url image
    percent = models.CharField(max_length=50)# Porcentaje de resultado - exmaple: 90%
    options = models.CharField(max_length=100)# Porcentajes del resultado - examples "90.3536, 20.3553, 57.3458, 79.3563"
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.result
