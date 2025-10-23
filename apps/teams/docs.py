"""
Documentación Swagger para endpoints de Teams

Este archivo centraliza toda la documentación de la API para mantener
views.py limpio y enfocado solo en la lógica de negocio.

Organización:
- Cada endpoint tiene su decorador @swagger_auto_schema
- Los decoradores se importan en views.py
- Facilita el mantenimiento y la lectura del código
"""
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .schemas import TeamCreateSchema, TeamReadSchema, TeamUpdateSchema


# ==================== CREATE TEAM ====================
create_team_docs = swagger_auto_schema(
    operation_summary="Crear un nuevo team",
    operation_description="Crea un nuevo team en la base de datos. El nombre debe ser único.",
    request_body=TeamCreateSchema,
    responses={
        201: openapi.Response(
            description="Team creado exitosamente",
            schema=TeamReadSchema
        ),
        400: openapi.Response(
            description="Datos inválidos o el team ya existe",
            examples={
                "application/json": {
                    "nombre": ["Ya existe un team con el nombre 'Example Team'"]
                }
            }
        )
    },
    tags=['Teams']
)


# ==================== LIST TEAMS ====================
list_teams_docs = swagger_auto_schema(
    operation_summary="Listar todos los teams",
    operation_description="Obtiene una lista paginada de todos los teams ordenados por fecha de creación (más recientes primero).",
    manual_parameters=[
        openapi.Parameter(
            'offset',
            openapi.IN_QUERY,
            description="Índice de inicio para la paginación (default: 0)",
            type=openapi.TYPE_INTEGER,
            required=False,
            default=0
        ),
        openapi.Parameter(
            'limit',
            openapi.IN_QUERY,
            description="Cantidad de resultados a retornar (default: 10, max: 100)",
            type=openapi.TYPE_INTEGER,
            required=False,
            default=10
        ),
    ],
    responses={
        200: openapi.Response(
            description="Lista de teams obtenida exitosamente",
            examples={
                "application/json": {
                    "teams": [
                        {
                            "id": 1,
                            "nombre": "Team Alpha",
                            "descripcion": "Descripción del team",
                            "fecha_creacion": "2025-10-23T10:30:00Z"
                        }
                    ],
                    "total": 1,
                    "offset": 0,
                    "limit": 10,
                    "has_next": False,
                    "has_previous": False
                }
            }
        ),
        400: openapi.Response(
            description="Parámetros de paginación inválidos"
        )
    },
    tags=['Teams']
)


# ==================== RETRIEVE TEAM ====================
retrieve_team_docs = swagger_auto_schema(
    operation_summary="Obtener un team por ID",
    operation_description="Obtiene los detalles de un team específico mediante su ID.",
    responses={
        200: openapi.Response(
            description="Team encontrado exitosamente",
            schema=TeamReadSchema
        ),
        404: openapi.Response(
            description="Team no encontrado",
            examples={
                "application/json": {
                    "detail": "No se encontró el team con ID 999"
                }
            }
        )
    },
    tags=['Teams']
)


# ==================== UPDATE TEAM ====================
update_team_docs = swagger_auto_schema(
    operation_summary="Actualizar un team",
    operation_description="Actualiza parcialmente los datos de un team existente. Todos los campos son opcionales.",
    request_body=TeamUpdateSchema,
    responses={
        200: openapi.Response(
            description="Team actualizado exitosamente",
            schema=TeamReadSchema
        ),
        400: openapi.Response(
            description="Datos inválidos",
            examples={
                "application/json": {
                    "nombre": ["Ya existe otro team con el nombre 'Example Team'"]
                }
            }
        ),
        404: openapi.Response(
            description="Team no encontrado",
            examples={
                "application/json": {
                    "detail": "No se encontró el team con ID 999"
                }
            }
        )
    },
    tags=['Teams']
)


# ==================== DELETE TEAM ====================
delete_team_docs = swagger_auto_schema(
    operation_summary="Eliminar un team",
    operation_description="Elimina permanentemente un team de la base de datos.",
    responses={
        200: openapi.Response(
            description="Team eliminado exitosamente",
            examples={
                "application/json": {
                    "message": "Team 'Example Team' eliminado exitosamente",
                    "id": 1
                }
            }
        ),
        404: openapi.Response(
            description="Team no encontrado",
            examples={
                "application/json": {
                    "detail": "No se encontró el team con ID 999"
                }
            }
        )
    },
    tags=['Teams']
)


# ==================== CUSTOM ACTION: GET BY NAME ====================
get_by_name_docs = swagger_auto_schema(
    operation_summary="Buscar team por nombre",
    operation_description="Obtiene un team específico mediante su nombre (búsqueda exacta).",
    manual_parameters=[
        openapi.Parameter(
            'nombre',
            openapi.IN_QUERY,
            description="Nombre exacto del team a buscar",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={
        200: openapi.Response(
            description="Team encontrado exitosamente",
            schema=TeamReadSchema
        ),
        400: openapi.Response(
            description="Nombre no proporcionado",
            examples={
                "application/json": {
                    "nombre": ["El nombre del team es requerido para la búsqueda"]
                }
            }
        ),
        404: openapi.Response(
            description="Team no encontrado",
            examples={
                "application/json": {
                    "detail": "No se encontró el team con nombre 'Example Team'"
                }
            }
        )
    },
    tags=['Teams']
)
