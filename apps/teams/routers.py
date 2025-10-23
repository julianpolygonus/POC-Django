"""
Routers para Teams
Configuración de rutas y endpoints
"""
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet


def get_teams_router():
    """
    Configura y retorna el router para Teams

    Returns:
        DefaultRouter: Router configurado con las rutas de Teams
    """
    router = DefaultRouter()
    router.register(r'teams', TeamViewSet, basename='team')
    return router


# Crear instancia del router
teams_router = get_teams_router()
