"""
Views básicas del proyecto
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def hola_mundo(request):
    """
    Endpoint de prueba que retorna un mensaje de hola mundo
    """
    return Response(
        {
            'mensaje': 'Hola Mundo',
            'descripcion': 'API REST con Django REST Framework',
            'version': '1.0.0',
            'status': 'ok'
        },
        status=status.HTTP_200_OK
    )
