"""
Capa de Repository para Heroes

Esta capa maneja ÚNICAMENTE el acceso a la base de datos.
NO contiene lógica de negocio, solo operaciones CRUD.

Responsabilidades:
- Crear, leer, actualizar y eliminar heroes en la base de datos
- Queries optimizadas con select_related para evitar N+1 queries
- Retornar objetos del modelo o None (nunca lanza excepciones de negocio)

IMPORTANTE sobre relaciones:
- Usamos select_related('team') para traer el team en la misma query
- Esto evita el problema de N+1 queries (muy importante en ORMs)
"""
from typing import Optional, List, Tuple
from .models import Hero
from apps.teams.models import Team


class HeroRepository:
    """
    Repository para operaciones de base de datos de Hero.

    Todos los métodos son @staticmethod porque no necesitan estado.
    """

    @staticmethod
    def create_hero(
        nombre: str,
        team: Team,
        descripcion: Optional[str] = None,
        poder_principal: Optional[str] = None,
        nivel: int = 1
    ) -> Hero:
        """
        Crea un nuevo héroe en la base de datos.

        Args:
            nombre: Nombre del héroe
            team: Objeto Team (no team_id, sino el objeto completo)
            descripcion: Descripción del héroe (opcional)
            poder_principal: Superpoder principal (opcional)
            nivel: Nivel de poder (default: 1)

        Returns:
            Hero: Objeto Hero creado con su ID asignado
        """
        hero = Hero.objects.create(
            nombre=nombre,
            team=team,
            descripcion=descripcion,
            poder_principal=poder_principal,
            nivel=nivel
        )
        # Recargar para obtener el team completo
        hero.refresh_from_db()
        return hero

    @staticmethod
    def get_hero_by_id(hero_id: int) -> Optional[Hero]:
        """
        Obtiene un héroe por su ID.

        IMPORTANTE: Usa select_related('team') para evitar N+1 queries.
        Esto trae el team del héroe en la misma consulta SQL.

        Args:
            hero_id: ID del héroe a buscar

        Returns:
            Hero si existe, None si no se encuentra
        """
        try:
            # select_related('team') hace un JOIN y trae el team en la misma query
            return Hero.objects.select_related('team').get(id=hero_id)
        except Hero.DoesNotExist:
            return None

    @staticmethod
    def get_hero_by_name(nombre: str) -> Optional[Hero]:
        """
        Obtiene un héroe por su nombre (búsqueda exacta).

        Args:
            nombre: Nombre exacto del héroe

        Returns:
            Hero si existe, None si no se encuentra
        """
        try:
            return Hero.objects.select_related('team').get(nombre=nombre)
        except Hero.DoesNotExist:
            return None

    @staticmethod
    def get_all_heroes(offset: int = 0, limit: int = 10) -> Tuple[List[Hero], int]:
        """
        Obtiene todos los héroes con paginación.

        IMPORTANTE: Usa select_related('team') para optimizar.
        Sin esto, Django haría 1 query por cada hero para traer su team (N+1).

        Args:
            offset: Índice de inicio (default: 0)
            limit: Cantidad de resultados (default: 10)

        Returns:
            Tuple[List[Hero], int]: (Lista de heroes, Total de heroes)
        """
        queryset = Hero.objects.select_related('team').all().order_by('-fecha_creacion')
        total = queryset.count()
        heroes = list(queryset[offset:offset + limit])
        return heroes, total

    @staticmethod
    def get_heroes_by_team(team_id: int, offset: int = 0, limit: int = 10) -> Tuple[List[Hero], int]:
        """
        Obtiene todos los héroes de un equipo específico con paginación.

        Esta es una de las queries más comunes: "Dame todos los heroes del Team X"

        Args:
            team_id: ID del equipo
            offset: Índice de inicio (default: 0)
            limit: Cantidad de resultados (default: 10)

        Returns:
            Tuple[List[Hero], int]: (Lista de heroes del team, Total de heroes del team)
        """
        queryset = Hero.objects.select_related('team').filter(team_id=team_id).order_by('-fecha_creacion')
        total = queryset.count()
        heroes = list(queryset[offset:offset + limit])
        return heroes, total

    @staticmethod
    def update_hero(
        hero_id: int,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None,
        poder_principal: Optional[str] = None,
        nivel: Optional[int] = None,
        team: Optional[Team] = None
    ) -> Optional[Hero]:
        """
        Actualiza un héroe existente.

        Solo actualiza los campos que NO sean None.

        Args:
            hero_id: ID del héroe a actualizar
            nombre: Nuevo nombre (opcional)
            descripcion: Nueva descripción (opcional)
            poder_principal: Nuevo poder (opcional)
            nivel: Nuevo nivel (opcional)
            team: Nuevo team (opcional, para cambiar de equipo)

        Returns:
            Hero actualizado si existe, None si no se encuentra
        """
        try:
            hero = Hero.objects.select_related('team').get(id=hero_id)

            # Actualizar solo los campos que se proporcionaron
            if nombre is not None:
                hero.nombre = nombre
            if descripcion is not None:
                hero.descripcion = descripcion
            if poder_principal is not None:
                hero.poder_principal = poder_principal
            if nivel is not None:
                hero.nivel = nivel
            if team is not None:
                hero.team = team

            hero.save()
            hero.refresh_from_db()
            return hero

        except Hero.DoesNotExist:
            return None

    @staticmethod
    def delete_hero(hero_id: int) -> bool:
        """
        Elimina un héroe de la base de datos.

        Args:
            hero_id: ID del héroe a eliminar

        Returns:
            bool: True si se eliminó, False si no existía
        """
        try:
            hero = Hero.objects.get(id=hero_id)
            hero.delete()
            return True
        except Hero.DoesNotExist:
            return False

    @staticmethod
    def exists_by_id(hero_id: int) -> bool:
        """
        Verifica si existe un héroe con el ID dado.

        Args:
            hero_id: ID del héroe

        Returns:
            bool: True si existe, False si no
        """
        return Hero.objects.filter(id=hero_id).exists()

    @staticmethod
    def exists_by_name(nombre: str) -> bool:
        """
        Verifica si existe un héroe con el nombre dado.

        Args:
            nombre: Nombre del héroe

        Returns:
            bool: True si existe, False si no
        """
        return Hero.objects.filter(nombre=nombre).exists()

    @staticmethod
    def count_heroes_by_team(team_id: int) -> int:
        """
        Cuenta cuántos héroes tiene un equipo.

        Útil para validaciones o estadísticas.

        Args:
            team_id: ID del equipo

        Returns:
            int: Cantidad de heroes en el equipo
        """
        return Hero.objects.filter(team_id=team_id).count()
