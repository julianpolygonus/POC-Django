"""
Views/Controllers para Teams

Esta capa maneja las peticiones HTTP y las respuestas.
La documentación Swagger se encuentra en teams/docs.py para mantener
este archivo limpio y enfocado en la lógica de negocio.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import TeamService
from .schemas import TeamCreateSchema, TeamReadSchema, TeamUpdateSchema
from .docs import (
    create_team_docs,
    list_teams_docs,
    retrieve_team_docs,
    update_team_docs,
    delete_team_docs,
    get_by_name_docs
)


class TeamViewSet(viewsets.ViewSet):
    """
    ViewSet para operaciones CRUD de Teams

    Endpoints disponibles:
    - POST /api/teams/ - Crear un nuevo team
    - GET /api/teams/ - Listar todos los teams (con paginación)
    - GET /api/teams/{id}/ - Obtener un team por ID
    - GET /api/teams/by-name/?nombre={nombre} - Obtener un team por nombre
    - PATCH /api/teams/{id}/ - Actualizar un team
    - DELETE /api/teams/{id}/ - Eliminar un team
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = TeamService()

    @create_team_docs
    def create(self, request):
        """
        POST /api/teams/
        Crea un nuevo team
        """
        # Validar datos de entrada
        serializer = TeamCreateSchema(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Llamar al servicio
        team = self.service.create_team(
            nombre=serializer.validated_data['nombre'],
            descripcion=serializer.validated_data.get('descripcion')
        )

        # Serializar respuesta
        response_serializer = TeamReadSchema(team)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @list_teams_docs
    def list(self, request):
        """
        GET /api/teams/
        Lista todos los teams con paginación
        """
        # Obtener parámetros de paginación
        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 10))

        # Llamar al servicio
        result = self.service.get_all_teams(offset=offset, limit=limit)

        # Serializar teams
        teams_serializer = TeamReadSchema(result['teams'], many=True)

        # Construir respuesta
        response_data = {
            "teams": teams_serializer.data,
            "total": result['total'],
            "offset": result['offset'],
            "limit": result['limit'],
            "has_next": result['has_next'],
            "has_previous": result['has_previous']
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @retrieve_team_docs
    def retrieve(self, request, pk=None):
        """
        GET /api/teams/{id}/
        Obtiene un team por su ID
        """
        # Llamar al servicio
        team = self.service.get_team_by_id(int(pk))

        # Serializar respuesta
        serializer = TeamReadSchema(team)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @get_by_name_docs
    @action(detail=False, methods=['get'], url_path='by-name')
    def get_by_name(self, request):
        """
        GET /api/teams/by-name/?nombre={nombre}
        Obtiene un team por su nombre
        """
        nombre = request.query_params.get('nombre')

        # Llamar al servicio
        team = self.service.get_team_by_name(nombre)

        # Serializar respuesta
        serializer = TeamReadSchema(team)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @update_team_docs
    def partial_update(self, request, pk=None):
        """
        PATCH /api/teams/{id}/
        Actualiza un team existente (parcial)
        """
        # Validar datos de entrada
        serializer = TeamUpdateSchema(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Llamar al servicio
        team = self.service.update_team(
            team_id=int(pk),
            nombre=serializer.validated_data.get('nombre'),
            descripcion=serializer.validated_data.get('descripcion')
        )

        # Serializar respuesta
        response_serializer = TeamReadSchema(team)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @delete_team_docs
    def destroy(self, request, pk=None):
        """
        DELETE /api/teams/{id}/
        Elimina un team
        """
        # Llamar al servicio
        result = self.service.delete_team(int(pk))

        return Response(result, status=status.HTTP_200_OK)
