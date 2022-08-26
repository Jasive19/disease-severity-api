from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        update_user = super().update(instance, validated_data)
        if validated_data.get('password'):
            update_user.set_password(validated_data['password'])
        update_user.save()
        return update_user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password','groups',)

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=6, write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {
                  'message':'Debe ingresar ambas contraseñas iguales'
                }
            )
        return data