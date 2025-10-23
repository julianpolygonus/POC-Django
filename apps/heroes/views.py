"""
Views/Controllers para Heroes

Esta capa maneja las peticiones HTTP y las respuestas.
La documentación Swagger se encuentra en heroes/docs.py para mantener
este archivo limpio y enfocado en la lógica de negocio.

Responsabilidades:
- Recibir requests HTTP
- Validar datos de entrada usando schemas (serializers)
- Llamar a la capa de Services para ejecutar lógica de negocio
- Retornar responses HTTP apropiadas

NO maneja:
- Lógica de negocio (eso es responsabilidad de Services)
- Acceso a base de datos (eso es responsabilidad de Repository)
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import HeroService
from .schemas import HeroCreateSchema, HeroReadSchema, HeroUpdateSchema
from .docs import (
    create_hero_docs,
    list_heroes_docs,
    retrieve_hero_docs,
    update_hero_docs,
    delete_hero_docs,
    get_by_name_docs,
    get_by_team_docs
)


class HeroViewSet(viewsets.ViewSet):
    """
    ViewSet para operaciones CRUD de Heroes

    Endpoints disponibles:
    - POST /api/heroes/ - Crear un nuevo héroe
    - GET /api/heroes/ - Listar todos los héroes (con paginación)
    - GET /api/heroes/{id}/ - Obtener un héroe por ID
    - GET /api/heroes/by-name/?nombre={nombre} - Buscar héroe por nombre
    - GET /api/heroes/by-team/{team_id}/ - Obtener héroes de un equipo
    - PATCH /api/heroes/{id}/ - Actualizar un héroe
    - DELETE /api/heroes/{id}/ - Eliminar un héroe

    Relación con Team:
    - Un héroe pertenece a UN solo team (team_id es FK)
    - Un team puede tener MUCHOS heroes (relación inversa: team.heroes.all())
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = HeroService()

    @create_hero_docs
    def create(self, request):
        """
        POST /api/heroes/
        Crea un nuevo héroe

        Body esperado:
        {
            "nombre": "Superman",
            "descripcion": "El hombre de acero",
            "poder_principal": "Super fuerza",
            "nivel": 95,
            "team_id": 1
        }
        """
        # Validar datos de entrada
        serializer = HeroCreateSchema(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extraer team_id del serializer
        # Nota: el serializer usa source='team' pero recibe team_id
        team = serializer.validated_data['team']  # Es el objeto Team completo

        # Llamar al servicio
        hero = self.service.create_hero(
            nombre=serializer.validated_data['nombre'],
            team_id=team.id,  # Pasamos el ID al servicio
            descripcion=serializer.validated_data.get('descripcion'),
            poder_principal=serializer.validated_data.get('poder_principal'),
            nivel=serializer.validated_data.get('nivel', 1)
        )

        # Serializar respuesta
        response_serializer = HeroReadSchema(hero)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @list_heroes_docs
    def list(self, request):
        """
        GET /api/heroes/
        Lista todos los héroes con paginación

        Query params:
        - offset: Índice de inicio (default: 0)
        - limit: Cantidad de resultados (default: 10, max: 100)
        """
        # Obtener parámetros de paginación
        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 10))

        # Llamar al servicio
        result = self.service.get_all_heroes(offset=offset, limit=limit)

        # Serializar heroes
        heroes_serializer = HeroReadSchema(result['heroes'], many=True)

        # Construir respuesta
        response_data = {
            "heroes": heroes_serializer.data,
            "total": result['total'],
            "offset": result['offset'],
            "limit": result['limit'],
            "has_next": result['has_next'],
            "has_previous": result['has_previous']
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @retrieve_hero_docs
    def retrieve(self, request, pk=None):
        """
        GET /api/heroes/{id}/
        Obtiene un héroe por su ID
        """
        # Llamar al servicio
        hero = self.service.get_hero_by_id(int(pk))

        # Serializar respuesta
        serializer = HeroReadSchema(hero)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @get_by_name_docs
    @action(detail=False, methods=['get'], url_path='by-name')
    def get_by_name(self, request):
        """
        GET /api/heroes/by-name/?nombre={nombre}
        Obtiene un héroe por su nombre

        Esta es una custom action (no sigue las convenciones estándar del ViewSet)
        - detail=False: No requiere {pk} en la URL
        - methods=['get']: Solo acepta GET
        - url_path='by-name': El segmento de URL será 'by-name'
        """
        nombre = request.query_params.get('nombre')

        # Llamar al servicio
        hero = self.service.get_hero_by_name(nombre)

        # Serializar respuesta
        serializer = HeroReadSchema(hero)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @get_by_team_docs
    @action(detail=True, methods=['get'], url_path='by-team')
    def get_by_team(self, request, pk=None):
        """
        GET /api/heroes/{team_id}/by-team/
        Obtiene todos los héroes de un equipo específico

        Esta custom action SIMULA una relación inversa de Team → Heroes.
        Es equivalente a: team.heroes.all()

        - detail=True: Requiere {pk} en la URL (el pk es el team_id)
        - methods=['get']: Solo acepta GET
        - url_path='by-team': El segmento de URL será 'by-team'

        Nota: Aunque es un endpoint de heroes, el {pk} representa el team_id
        """
        # Obtener parámetros de paginación
        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 10))

        # Llamar al servicio (pk es el team_id en este caso)
        result = self.service.get_heroes_by_team(
            team_id=int(pk),
            offset=offset,
            limit=limit
        )

        # Serializar heroes
        heroes_serializer = HeroReadSchema(result['heroes'], many=True)

        # Construir respuesta
        response_data = {
            "heroes": heroes_serializer.data,
            "total": result['total'],
            "offset": result['offset'],
            "limit": result['limit'],
            "has_next": result['has_next'],
            "has_previous": result['has_previous'],
            "team_info": result['team_info']
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @update_hero_docs
    def partial_update(self, request, pk=None):
        """
        PATCH /api/heroes/{id}/
        Actualiza un héroe existente (parcial)

        Body esperado (todos los campos opcionales):
        {
            "nombre": "New Name",
            "descripcion": "New description",
            "poder_principal": "New power",
            "nivel": 80,
            "team_id": 2
        }
        """
        # Validar datos de entrada
        serializer = HeroUpdateSchema(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Extraer team_id si se proporcionó
        team_id = None
        if 'team' in serializer.validated_data:
            team = serializer.validated_data['team']
            team_id = team.id

        # Llamar al servicio
        hero = self.service.update_hero(
            hero_id=int(pk),
            nombre=serializer.validated_data.get('nombre'),
            descripcion=serializer.validated_data.get('descripcion'),
            poder_principal=serializer.validated_data.get('poder_principal'),
            nivel=serializer.validated_data.get('nivel'),
            team_id=team_id
        )

        # Serializar respuesta
        response_serializer = HeroReadSchema(hero)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @delete_hero_docs
    def destroy(self, request, pk=None):
        """
        DELETE /api/heroes/{id}/
        Elimina un héroe
        """
        # Llamar al servicio
        result = self.service.delete_hero(int(pk))

        return Response(result, status=status.HTTP_200_OK)
