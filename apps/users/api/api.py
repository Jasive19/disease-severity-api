from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from apps.users.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from apps.users.api.serializers import (
    UserSerializer,
    UserListSerializer
)

def response(data):
    return  {
        'id': data.get('id'),
        'email': data.get('email'),
        'password': data.get('password'),
        'name': data.get('name'),
        'first_name': data.get('first_name'),
        'last_name': data.get('last_name'),
        'is_admin': data.get('is_admin'),
        "is_active": data.get('is_active'),
        'image': data.get('image'),
        'user_permissions': data.get('user_permissions'),
    }

def getUser(request):
    token_authorization = request.headers["Authorization"].split()[1]
    token = Token.objects.filter(key=token_authorization).first()
    if token:
        user = token.user
        if user:
            return user.id


def bad_Request(request):
    return Response({
        'success': False,
        'data': [],
        'message': 'Usuario no encontrado'
    }, status=status.HTTP_401_UNAUTHORIZED)



class UserViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    queryset = None


    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)


    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.all()
            return self.queryset


    def list(self, request):
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return Response({
            'success': True,
            'data': users_serializer.data,
        }, status=status.HTTP_200_OK)


    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        data = response(user_serializer.data)
        return Response({
          'success': True,
          'data': data,
        }, status=status.HTTP_200_OK)


    def create(self, request):
        data = {
            'email': request.data.get('email', None),
            'password': request.data.get('password', None),
            'name': request.data.get('name', None),
            'last_name': request.data.get('last_name', None),
        }
        user_serializer = self.serializer_class(data=data)
        
        if user_serializer.is_valid():
            user_serializer.save()
            data = response(user_serializer.data)
            return Response({
                'data': data,
                'success': True,
                'message': 'Usuario registrado correctamente.'
            }, status=status.HTTP_201_CREATED)

        return Response({
            'message': 'Hay errores en el registro',
            'success': False,
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


    # def update(self, request, pk=None):
    #     user = self.get_object(pk)

    #     data = {
    #         'email': request.data.get('email'),
    #         'name': request.data.get('name'),
    #         'first_name': request.data.get('first_name'),
    #         'last_name': request.data.get('last_name'),
    #         'image': request.data.get('image'),
    #     }

    #     user_serializer = self.serializer_class(user, data=data)
    #     if user_serializer.is_valid():
    #         user_serializer.save()
    #         data = response(user_serializer.data)
    #         return Response({
    #             'data': data,
    #             'success': True,
    #             'message': 'Usuario actualizado correctamente'
    #         }, status=status.HTTP_200_OK)

    #     return Response({
    #         'success': False,
    #         'message': 'Ah ocurrido un error en la actualización',
    #         'errors': user_serializer.errors
    #     }, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        user_destroy = self.model.objects.filter(pk=pk).update(is_active=False)
        if user_destroy == 1:
            user = self.get_object(pk)
            user_serializer = self.serializer_class(user)
            data = response(user_serializer.data)
            return Response({
                'data': data,
                'success': True,
                'message': 'Usuario eliminado correctamente'
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'message': 'No existe el usuario que desea eliminar'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH','POST'])
def modify(request):
    user_id = getUser(request)
    if user_id is None:
        return bad_Request(request)
    user = User.objects.filter(id=user_id).first()
    
    data = {
        'email': request.data.get('email'),
        'name': request.data.get('name'),
        'last_name': request.data.get('last_name'),
        'first_name': request.data.get('first_name'),
        'image': request.data.get('image'),
    }

    if request.data.get('password'):
        data['password'] = request.data.get('password')

    # "is_superuser":
        #     "is_active":
        #     "is_staff":
        #     "user_permissions": []

    if user:
        user_serializer = UserSerializer(user, data=data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            data = response(user_serializer.data)
            return Response({
                'success': True,
                'data': data,
                'message': 'Usuario actualizado correctamente'
            }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'message': 'Ah ocurrido un error en la actualización',
        'errors': user_serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


