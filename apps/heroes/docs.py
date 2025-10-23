"""
Documentación Swagger para endpoints de Heroes

Este archivo centraliza toda la documentación de la API para mantener
views.py limpio y enfocado solo en la lógica de negocio.

Endpoints documentados:
- POST /api/heroes/ - Crear un nuevo héroe
- GET /api/heroes/ - Listar todos los héroes (con paginación)
- GET /api/heroes/{id}/ - Obtener un héroe por ID
- GET /api/heroes/by-name/?nombre={nombre} - Obtener un héroe por nombre
- GET /api/heroes/by-team/{team_id}/ - Obtener todos los héroes de un equipo
- PATCH /api/heroes/{id}/ - Actualizar un héroe
- DELETE /api/heroes/{id}/ - Eliminar un héroe
"""
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .schemas import HeroCreateSchema, HeroReadSchema, HeroUpdateSchema


# ==================== CREATE HERO ====================
create_hero_docs = swagger_auto_schema(
    operation_summary="Crear un nuevo héroe",
    operation_description="""
    Crea un nuevo héroe en la base de datos.

    **Validaciones:**
    - El nombre debe ser único (no puede haber dos héroes con el mismo nombre)
    - El nombre no puede estar vacío ni exceder 255 caracteres
    - El team_id debe corresponder a un equipo existente
    - El nivel debe estar entre 1 y 100

    **Relación con Team:**
    - Un héroe DEBE pertenecer a un equipo (team_id es requerido)
    - El equipo debe existir previamente
    - Si se elimina el equipo, se eliminan todos sus héroes (CASCADE)
    """,
    request_body=HeroCreateSchema,
    responses={
        201: openapi.Response(
            description="Héroe creado exitosamente",
            schema=HeroReadSchema,
            examples={
                "application/json": {
                    "id": 1,
                    "nombre": "Superman",
                    "descripcion": "El hombre de acero",
                    "poder_principal": "Super fuerza",
                    "nivel": 95,
                    "team_id": 1,
                    "team": {
                        "id": 1,
                        "nombre": "Justice League",
                        "descripcion": "Los héroes más poderosos"
                    },
                    "fecha_creacion": "2025-10-23T10:30:00Z"
                }
            }
        ),
        400: openapi.Response(
            description="Datos inválidos",
            examples={
                "application/json": {
                    "nombre": ["Ya existe un héroe con el nombre 'Superman'"]
                }
            }
        ),
        404: openapi.Response(
            description="Team no encontrado",
            examples={
                "application/json": {
                    "team_id": ["No existe un equipo con ID 999"]
                }
            }
        )
    },
    tags=['Heroes']
)


# ==================== LIST HEROES ====================
list_heroes_docs = swagger_auto_schema(
    operation_summary="Listar todos los héroes",
    operation_description="""
    Obtiene una lista paginada de todos los héroes ordenados por fecha de creación
    (más recientes primero).

    **Incluye información del team:**
    Cada héroe retorna tanto el team_id como el objeto completo del team para evitar
    tener que hacer peticiones adicionales.

    **Paginación:**
    - offset: Índice de inicio (default: 0)
    - limit: Cantidad de resultados (default: 10, max: 100)
    """,
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
            description="Lista de héroes obtenida exitosamente",
            examples={
                "application/json": {
                    "heroes": [
                        {
                            "id": 1,
                            "nombre": "Superman",
                            "descripcion": "El hombre de acero",
                            "poder_principal": "Super fuerza",
                            "nivel": 95,
                            "team_id": 1,
                            "team": {
                                "id": 1,
                                "nombre": "Justice League",
                                "descripcion": "Los héroes más poderosos"
                            },
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
    tags=['Heroes']
)


# ==================== RETRIEVE HERO ====================
retrieve_hero_docs = swagger_auto_schema(
    operation_summary="Obtener un héroe por ID",
    operation_description="""
    Obtiene los detalles completos de un héroe específico mediante su ID.

    **Incluye:**
    - Todos los campos del héroe
    - Información completa del equipo al que pertenece
    """,
    responses={
        200: openapi.Response(
            description="Héroe encontrado exitosamente",
            schema=HeroReadSchema
        ),
        404: openapi.Response(
            description="Héroe no encontrado",
            examples={
                "application/json": {
                    "detail": "No se encontró el héroe con ID 999"
                }
            }
        )
    },
    tags=['Heroes']
)


# ==================== UPDATE HERO ====================
update_hero_docs = swagger_auto_schema(
    operation_summary="Actualizar un héroe",
    operation_description="""
    Actualiza parcialmente los datos de un héroe existente.
    Todos los campos son opcionales.

    **Validaciones:**
    - Si se actualiza el nombre: debe ser único (no puede ser igual a otro héroe)
    - Si se actualiza el nivel: debe estar entre 1 y 100
    - Si se actualiza el team_id: el nuevo equipo debe existir

    **Cambiar de equipo:**
    Puedes cambiar un héroe de un equipo a otro enviando el nuevo team_id.
    """,
    request_body=HeroUpdateSchema,
    responses={
        200: openapi.Response(
            description="Héroe actualizado exitosamente",
            schema=HeroReadSchema
        ),
        400: openapi.Response(
            description="Datos inválidos",
            examples={
                "application/json": {
                    "nombre": ["Ya existe otro héroe con el nombre 'Batman'"]
                }
            }
        ),
        404: openapi.Response(
            description="Héroe o Team no encontrado",
            examples={
                "application/json": {
                    "detail": "No se encontró el héroe con ID 999"
                }
            }
        )
    },
    tags=['Heroes']
)


# ==================== DELETE HERO ====================
delete_hero_docs = swagger_auto_schema(
    operation_summary="Eliminar un héroe",
    operation_description="""
    Elimina permanentemente un héroe de la base de datos.

    **Nota:** Esta operación no afecta al equipo. Solo elimina el héroe.
    """,
    responses={
        200: openapi.Response(
            description="Héroe eliminado exitosamente",
            examples={
                "application/json": {
                    "message": "Héroe 'Superman' del equipo 'Justice League' eliminado exitosamente",
                    "id": 1
                }
            }
        ),
        404: openapi.Response(
            description="Héroe no encontrado",
            examples={
                "application/json": {
                    "detail": "No se encontró el héroe con ID 999"
                }
            }
        )
    },
    tags=['Heroes']
)


# ==================== CUSTOM ACTION: GET BY NAME ====================
get_by_name_docs = swagger_auto_schema(
    operation_summary="Buscar héroe por nombre",
    operation_description="""
    Obtiene un héroe específico mediante su nombre (búsqueda exacta).

    **Nota:** La búsqueda es case-sensitive (distingue mayúsculas/minúsculas).
    """,
    manual_parameters=[
        openapi.Parameter(
            'nombre',
            openapi.IN_QUERY,
            description="Nombre exacto del héroe a buscar",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={
        200: openapi.Response(
            description="Héroe encontrado exitosamente",
            schema=HeroReadSchema
        ),
        400: openapi.Response(
            description="Nombre no proporcionado",
            examples={
                "application/json": {
                    "nombre": ["El nombre del héroe es requerido para la búsqueda"]
                }
            }
        ),
        404: openapi.Response(
            description="Héroe no encontrado",
            examples={
                "application/json": {
                    "detail": "No se encontró el héroe con nombre 'Superman'"
                }
            }
        )
    },
    tags=['Heroes']
)


# ==================== CUSTOM ACTION: GET HEROES BY TEAM ====================
get_by_team_docs = swagger_auto_schema(
    operation_summary="Obtener todos los héroes de un equipo",
    operation_description="""
    Obtiene una lista paginada de todos los héroes que pertenecen a un equipo específico.

    **Uso común:**
    Este endpoint es muy útil para mostrar todos los miembros de un equipo.
    Por ejemplo: "Dame todos los héroes de la Justice League"

    **Relación inversa:**
    Esto es equivalente a acceder a `team.heroes.all()` en el ORM de Django,
    pero expuesto como endpoint REST.

    **Incluye:**
    - Lista de héroes del equipo
    - Información del equipo (team_info)
    - Paginación (offset, limit, has_next, has_previous)
    """,
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
            description="Lista de héroes del equipo obtenida exitosamente",
            examples={
                "application/json": {
                    "heroes": [
                        {
                            "id": 1,
                            "nombre": "Superman",
                            "descripcion": "El hombre de acero",
                            "poder_principal": "Super fuerza",
                            "nivel": 95,
                            "team_id": 1,
                            "team": {
                                "id": 1,
                                "nombre": "Justice League",
                                "descripcion": "Los héroes más poderosos"
                            },
                            "fecha_creacion": "2025-10-23T10:30:00Z"
                        },
                        {
                            "id": 2,
                            "nombre": "Batman",
                            "descripcion": "El caballero oscuro",
                            "poder_principal": "Inteligencia",
                            "nivel": 90,
                            "team_id": 1,
                            "team": {
                                "id": 1,
                                "nombre": "Justice League",
                                "descripcion": "Los héroes más poderosos"
                            },
                            "fecha_creacion": "2025-10-23T10:25:00Z"
                        }
                    ],
                    "total": 2,
                    "offset": 0,
                    "limit": 10,
                    "has_next": False,
                    "has_previous": False,
                    "team_info": {
                        "id": 1,
                        "nombre": "Justice League",
                        "descripcion": "Los héroes más poderosos"
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Parámetros de paginación inválidos"
        ),
        404: openapi.Response(
            description="Team no encontrado",
            examples={
                "application/json": {
                    "detail": "No existe un equipo con ID 999"
                }
            }
        )
    },
    tags=['Heroes']
)
