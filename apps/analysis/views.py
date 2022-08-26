from apps.analysis.serializers import AnalysisSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from apps.analysis.models import Analysis
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import get_authorization_header
from apps.severity.views import LoadModel


def bad_Request(request):
    return Response({
        'success': False,
        'data': [],
        'message': 'Usuario no encontrado'
    }, status=status.HTTP_401_UNAUTHORIZED)


def getUser(request):
    token_authorization = request.headers["Authorization"].split()[1]
    token = Token.objects.filter(key=token_authorization).first()
    if token:
        user = token.user
        if user:
            return user.id


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def index(request):
    user_id = getUser(request)
    if user_id is None:
        return bad_Request(request)
    analysis = Analysis.objects.filter(user_id=user_id, is_active=True)
    analysis_serializer = AnalysisSerializer(analysis, many=True)
    return Response({
        'success': True,
        'data': analysis_serializer.data,
        'message': 'Ok'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def show(request, id=None):
    user_id = getUser(request)
    if user_id is None:
        return bad_Request(request)
    analysis = Analysis.objects.filter(
        id=id, user_id=user_id, is_active=True).first()
    analysis_serializer = AnalysisSerializer(analysis)
    data = analysis_serializer.data
    return Response({
        'success': True,
        'data': data,
        'message': 'Ok'
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([])
@authentication_classes([])
def update(request, id=None):
    user_id = getUser(request)
    if user_id is None:
        return bad_Request(request)
    analysis = Analysis.objects.filter(
        id=id, user_id=user_id, is_active=True).first()
    if analysis:
        analysis_serializer = AnalysisSerializer(
            analysis, data=request.data, partial=True)
        if analysis_serializer.is_valid():
            analysis_serializer.save()
            data = analysis_serializer.data
            return Response({
                'success': True,
                'data': data,
                'message': 'Análisis actualizado correctamente'
            }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'message': 'Ah ocurrido un error en la actualización',
        'errors': analysis_serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def create(request):
    user_id = getUser(request)
    if user_id is None:
        return bad_Request(request)
    print(user_id)
    analysis = LoadModel.predictH5(request)
    data = {
        'result': analysis.get('result', None),
        'url': analysis.get('url', None),
        'percent': analysis.get('percent', None),
        'options': analysis.get('options', None),
        'user_id': user_id,
    }

    analysis_serializer = AnalysisSerializer(data=data)
    if analysis_serializer.is_valid():
        analysis_serializer.save()
        data = analysis_serializer.data
        return Response({
            'data': data,
            'success': True,
            'message': 'Análisis registrado correctamente.'
        }, status=status.HTTP_201_CREATED)

    return Response({
        'message': 'Hay errores en el registro',
        'success': False,
        'errors': analysis_serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([])
@authentication_classes([])
def delete(request):
    user_id = getUser(request)
    if user_id is None:
        return bad_Request(request)
    id = request.data.get('id')
    analysis_destroy = Analysis.objects.filter(
        id=id, user_id=user_id).update(is_active=False)
    
    if analysis_destroy == 1:
        analysis = get_object_or_404(Analysis, id=id)
        analysis_serializer = AnalysisSerializer(analysis)
        data = analysis_serializer.data
        
        return Response({
            'data': data,
            'success': True,
            'message': 'Análisis eliminado correctamente'
        }, status=status.HTTP_200_OK)
    return Response({
        'success': False,
        'message': 'No existe el analisis que desea eliminar'
    }, status=status.HTTP_404_NOT_FOUND)
