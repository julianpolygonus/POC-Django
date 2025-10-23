"""
Repository Layer para Teams
Esta capa maneja todas las operaciones de acceso a datos
"""
from typing import List, Optional, Tuple
from .models import Team


class TeamRepository:
    """
    Repositorio para operaciones CRUD de Team
    """

    @staticmethod
    def create_team(nombre: str, descripcion: Optional[str] = None) -> Team:
        """
        Crea un nuevo team en la base de datos

        Args:
            nombre: Nombre del team
            descripcion: Descripción del team (opcional)

        Returns:
            Team: Instancia del team creado
        """
        team = Team.objects.create(
            nombre=nombre,
            descripcion=descripcion
        )
        return team

    @staticmethod
    def get_team_by_id(team_id: int) -> Optional[Team]:
        """
        Obtiene un team por su ID

        Args:
            team_id: ID del team

        Returns:
            Team o None si no existe
        """
        try:
            return Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return None

    @staticmethod
    def get_team_by_name(nombre: str) -> Optional[Team]:
        """
        Obtiene un team por su nombre (búsqueda exacta)

        Args:
            nombre: Nombre del team

        Returns:
            Team o None si no existe
        """
        try:
            return Team.objects.get(nombre=nombre)
        except Team.DoesNotExist:
            return None

    @staticmethod
    def get_all_teams(offset: int = 0, limit: int = 10) -> Tuple[List[Team], int]:
        """
        Obtiene todos los teams con paginación

        Args:
            offset: Índice de inicio (default: 0)
            limit: Cantidad de resultados (default: 10)

        Returns:
            Tuple: (Lista de teams, total de teams)
        """
        queryset = Team.objects.all().order_by('-fecha_creacion')
        total = queryset.count()

        # Aplicar paginación manual con offset y limit
        teams = list(queryset[offset:offset + limit])

        return teams, total

    @staticmethod
    def update_team(team_id: int, **kwargs) -> Optional[Team]:
        """
        Actualiza un team existente

        Args:
            team_id: ID del team a actualizar
            **kwargs: Campos a actualizar (nombre, descripcion)

        Returns:
            Team actualizado o None si no existe
        """
        team = TeamRepository.get_team_by_id(team_id)
        if not team:
            return None

        # Actualizar solo los campos proporcionados
        for key, value in kwargs.items():
            if hasattr(team, key) and value is not None:
                setattr(team, key, value)

        team.save()
        return team

    @staticmethod
    def delete_team(team_id: int) -> bool:
        """
        Elimina un team por su ID

        Args:
            team_id: ID del team a eliminar

        Returns:
            bool: True si se eliminó, False si no existe
        """
        team = TeamRepository.get_team_by_id(team_id)
        if not team:
            return False

        team.delete()
        return True

    @staticmethod
    def exists_by_name(nombre: str) -> bool:
        """
        Verifica si existe un team con el nombre dado

        Args:
            nombre: Nombre del team

        Returns:
            bool: True si existe, False si no
        """
        return Team.objects.filter(nombre=nombre).exists()

    @staticmethod
    def exists_by_id(team_id: int) -> bool:
        """
        Verifica si existe un team con el ID dado

        Args:
            team_id: ID del team

        Returns:
            bool: True si existe, False si no
        """
        return Team.objects.filter(id=team_id).exists()
