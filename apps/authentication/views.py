from rest_framework import status
from rest_framework.response import Response
from django.contrib.sessions.models import Session
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from apps.authentication.serializers import UserSerializer
from ..users.models import User
from ..users.api.serializers import PasswordSerializer, UserSerializer as UserApiSerializer

def response(data):
    return {
        'id': data.get('id'),
        'email': data.get('email'),
        'name': data.get('name'),
        'first_name': data.get('first_name'),
        'last_name': data.get('last_name'),
        'is_admin': data.get('is_admin'),
        "is_active": data.get('is_active'),
        'image': data.get('image'),
        'user_permissions': data.get('user_permissions'),
    }


class UserToken(APIView):
    def get(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        try:
            user_token = Token.objects.get(
                user=UserSerializer().Meta.model.objects.filter(email=email).first()
            )
            return Response({
                'token': user_token.key
            })
        except:
            return Response({
                'error': 'Las credenciales enviadas son incorrectas.'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken, APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        login_serializer = self.serializer_class(
            data={'username': email, 'password': password}, context={'request': request})

        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UserSerializer(user)
                data = response(user_serializer.data)
                return Response({
                    'token': token.key,
                    'user': data,
                    'success': True,
                    'message': '¡Bienvenido!'
                }, status=status.HTTP_200_OK)

            return Response({'success': False, 'message': 'Ha ocurrido un error al intentar iniciar sesión'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': False, 'message': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.headers["Authorization"].split()[1]
        token = Token.objects.filter(key=token).first()
        if token:
            user = token.user
            all_sessions = Session.objects.all()
            current_session = list(filter(lambda session: session.get_decoded().get(
                '_auth_user_id') == str(user.id), all_sessions))
            map(lambda session: session.delete(), current_session)
            token.delete()
            return Response({
                'message': 'Sesión cerrada correctamente.',
                'success': True
            }, status=status.HTTP_200_OK)

        return Response({
            'message': '',
            'success': False,
        }, status=status.HTTP_200_OK)


class VerifyTokenView(APIView):

    def post(self, request):
        token_authorization = request.headers["Authorization"].split()[1]
        token = Token.objects.filter(key=token_authorization).first()
        if token:
            user = token.user
            user_serializer = UserSerializer(user)
            data = response(user_serializer.data)
            return Response({
                'message': 'Ok',
                'user': data,
                'success': True,
            }, status=status.HTTP_200_OK)

        return Response({
            'message': "Token no válido",
            'success': False,
        }, status=status.HTTP_400_BAD_REQUEST)


class SignupView(ObtainAuthToken):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request, *args, **kwargs):
        data = {
            'email': request.data.get('email', None),
            'password': request.data.get('password', None),
            'name': request.data.get('name', None),
            'first_name': request.data.get('first_name', None),
            'last_name': request.data.get('last_name', None),
        }

        user_serializer = UserSerializer(data=data)
        if user_serializer.is_valid():
            if user_serializer.save():
                data = response(user_serializer.data)
                user = LoginView.post(self, request)
                
                return Response({
                    'message': '¡Registro exitoso, bienvenido!',
                    'success': True,
                    'user': user.data},
                    status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Ah ocurrido un error: ' + user_serializer.errors,
            'success': False,
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        token_authorization = request.headers["Authorization"].split()[1]
        token = Token.objects.filter(key=token_authorization).first()
        if token:
            user = token.user
            user_id = user.id
            user = User.objects.filter(id=user_id).first()
            
            PasswordSerializer().validate(data={
                'password': request.data.get('new_password', None),
                'confirm_password': request.data.get('confirm_password', None),
            })
            
            # user.check_password(request.data.get('password', None),)
            
            data = {
                'email': user.email,
                'name': user.name,
                'password': request.data.get('new_password',None)
            }

            user_serializer = UserApiSerializer(user, data=data, partial=True)
            if user_serializer.is_valid():
                if user_serializer.save():
                    data = response(user_serializer.data) 
                    LogoutView.post(self, request)
                    return Response({
                        'message': 'Contraseña actualizada con éxito',
                        'success': True,
                    },status=status.HTTP_201_CREATED)

            return Response({
                'message': 'Ah ocurrido un error: ',
                'detail': user_serializer.errors,
                'success': False,   
            }, status=status.HTTP_400_BAD_REQUEST)
