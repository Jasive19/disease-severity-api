from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
class UserSerializer(serializers.ModelSerializer):
  CurrentUserDefault()
  class Meta:
    model = get_user_model()
    fields = '__all__'

  def validate_password(self, value):
    return make_password(value)

  def update(self, instance, validated_data):
        update_user = super().update(instance, validated_data)
        if validated_data.get('password'):
            update_user.set_password(validated_data['password'])
        update_user.save()
        return update_user