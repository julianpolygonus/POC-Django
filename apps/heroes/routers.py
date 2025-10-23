"""
Configuración de Router para Heroes

Este archivo configura el DefaultRouter de Django REST Framework
para generar automáticamente las URLs de los endpoints de Heroes.

El router genera automáticamente las siguientes rutas:
- POST   /heroes/                    → create()
- GET    /heroes/                    → list()
- GET    /heroes/{pk}/               → retrieve()
- PATCH  /heroes/{pk}/               → partial_update()
- DELETE /heroes/{pk}/               → destroy()
- GET    /heroes/by-name/            → get_by_name() (custom action)
- GET    /heroes/{pk}/by-team/       → get_by_team() (custom action)

Nota: El prefijo 'api/' se agrega en config/urls.py
"""
from rest_framework.routers import DefaultRouter
from .views import HeroViewSet


def get_heroes_router():
    """
    Crea y configura el router para Heroes.

    Returns:
        DefaultRouter: Router configurado con HeroViewSet
    """
    router = DefaultRouter()

    # Registrar el ViewSet
    # - r'heroes': Prefijo de URL (se convierte en /heroes/)
    # - HeroViewSet: La clase ViewSet que maneja las operaciones
    # - basename='hero': Nombre base para las rutas (se usa para reverse URLs)
    router.register(r'heroes', HeroViewSet, basename='hero')

    return router


# Exportar el router ya configurado
heroes_router = get_heroes_router()
