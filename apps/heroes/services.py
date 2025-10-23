"""
Capa de Services para Heroes

Esta capa contiene TODA la lógica de negocio y validaciones.
Se comunica con el Repository para acceder a la base de datos.

Responsabilidades:
- Validar datos de negocio (nombre único, nivel válido, team existe, etc.)
- Implementar reglas de negocio
- Manejar errores y lanzar excepciones apropiadas
- Coordinar operaciones entre múltiples repositories si es necesario

NO maneja:
- Requests/Responses HTTP (eso es responsabilidad de Views)
- Queries directas a la BD (eso es responsabilidad de Repository)
"""
from typing import Dict, Any
from rest_framework.exceptions import ValidationError, NotFound
from .repository import HeroRepository
from apps.teams.repository import TeamRepository
from .models import Hero


class HeroService:
    """
    Servicio de lógica de negocio para Heroes.

    Coordina operaciones entre HeroRepository y TeamRepository,
    aplicando todas las validaciones necesarias.
    """

    def __init__(self):
        self.hero_repository = HeroRepository()
        self.team_repository = TeamRepository()

    # ==================== CREATE ====================
    def create_hero(
        self,
        nombre: str,
        team_id: int,
        descripcion: str = None,
        poder_principal: str = None,
        nivel: int = 1
    ) -> Hero:
        """
        Crea un nuevo héroe con validaciones de negocio.

        Validaciones:
        1. Nombre no puede estar vacío
        2. Nombre debe ser único (no puede haber dos heroes con el mismo nombre)
        3. Nombre no puede exceder 255 caracteres
        4. Team debe existir (no se puede asignar a un team inexistente)
        5. Nivel debe estar entre 1 y 100
        6. Poder principal no puede exceder 255 caracteres

        Args:
            nombre: Nombre del héroe
            team_id: ID del equipo al que pertenece
            descripcion: Descripción del héroe (opcional)
            poder_principal: Superpoder principal (opcional)
            nivel: Nivel de poder (1-100, default: 1)

        Returns:
            Hero: Héroe creado

        Raises:
            ValidationError: Si alguna validación falla
        """
        # Validación 1: Nombre no vacío
        if not nombre or nombre.strip() == "":
            raise ValidationError({"nombre": "El nombre del héroe es requerido"})

        # Validación 2: Nombre no puede exceder 255 caracteres
        if len(nombre) > 255:
            raise ValidationError({"nombre": "El nombre no puede exceder 255 caracteres"})

        # Validación 3: Nombre único
        if self.hero_repository.exists_by_name(nombre.strip()):
            raise ValidationError({
                "nombre": f"Ya existe un héroe con el nombre '{nombre.strip()}'"
            })

        # Validación 4: Team debe existir
        team = self.team_repository.get_team_by_id(team_id)
        if not team:
            raise ValidationError({
                "team_id": f"No existe un equipo con ID {team_id}"
            })

        # Validación 5: Nivel debe estar entre 1 y 100
        if nivel < 1 or nivel > 100:
            raise ValidationError({
                "nivel": "El nivel debe estar entre 1 y 100"
            })

        # Validación 6: Poder principal no puede exceder 255 caracteres
        if poder_principal and len(poder_principal) > 255:
            raise ValidationError({
                "poder_principal": "El poder principal no puede exceder 255 caracteres"
            })

        # Crear el héroe
        hero = self.hero_repository.create_hero(
            nombre=nombre.strip(),
            team=team,  # Pasamos el objeto Team, no el ID
            descripcion=descripcion.strip() if descripcion else None,
            poder_principal=poder_principal.strip() if poder_principal else None,
            nivel=nivel
        )

        return hero

    # ==================== READ BY ID ====================
    def get_hero_by_id(self, hero_id: int) -> Hero:
        """
        Obtiene un héroe por su ID.

        Validaciones:
        1. ID debe ser positivo
        2. Héroe debe existir

        Args:
            hero_id: ID del héroe

        Returns:
            Hero: Héroe encontrado

        Raises:
            ValidationError: Si el ID no es válido
            NotFound: Si el héroe no existe
        """
        # Validación 1: ID positivo
        if hero_id <= 0:
            raise ValidationError({"id": "El ID debe ser un número positivo"})

        # Validación 2: Héroe debe existir
        hero = self.hero_repository.get_hero_by_id(hero_id)
        if not hero:
            raise NotFound({"detail": f"No se encontró el héroe con ID {hero_id}"})

        return hero

    # ==================== READ BY NAME ====================
    def get_hero_by_name(self, nombre: str) -> Hero:
        """
        Obtiene un héroe por su nombre.

        Validaciones:
        1. Nombre no puede estar vacío
        2. Héroe debe existir

        Args:
            nombre: Nombre del héroe

        Returns:
            Hero: Héroe encontrado

        Raises:
            ValidationError: Si el nombre está vacío
            NotFound: Si el héroe no existe
        """
        # Validación 1: Nombre no vacío
        if not nombre or nombre.strip() == "":
            raise ValidationError({"nombre": "El nombre del héroe es requerido para la búsqueda"})

        # Validación 2: Héroe debe existir
        hero = self.hero_repository.get_hero_by_name(nombre.strip())
        if not hero:
            raise NotFound({"detail": f"No se encontró el héroe con nombre '{nombre.strip()}'"})

        return hero

    # ==================== READ ALL ====================
    def get_all_heroes(self, offset: int = 0, limit: int = 10) -> Dict[str, Any]:
        """
        Obtiene todos los héroes con paginación.

        Validaciones:
        1. Offset debe ser >= 0
        2. Limit debe estar entre 1 y 100

        Args:
            offset: Índice de inicio (default: 0)
            limit: Cantidad de resultados (default: 10, max: 100)

        Returns:
            Dict con heroes, total, offset, limit, has_next, has_previous

        Raises:
            ValidationError: Si los parámetros de paginación son inválidos
        """
        # Validación 1: Offset no negativo
        if offset < 0:
            raise ValidationError({"offset": "El offset debe ser mayor o igual a 0"})

        # Validación 2: Limit entre 1 y 100
        if limit < 1 or limit > 100:
            raise ValidationError({"limit": "El limit debe estar entre 1 y 100"})

        # Obtener heroes
        heroes, total = self.hero_repository.get_all_heroes(offset, limit)

        # Calcular has_next y has_previous
        has_next = (offset + limit) < total
        has_previous = offset > 0

        return {
            "heroes": heroes,
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_next": has_next,
            "has_previous": has_previous
        }

    # ==================== READ HEROES BY TEAM ====================
    def get_heroes_by_team(self, team_id: int, offset: int = 0, limit: int = 10) -> Dict[str, Any]:
        """
        Obtiene todos los héroes de un equipo específico con paginación.

        Validaciones:
        1. Team debe existir
        2. Offset debe ser >= 0
        3. Limit debe estar entre 1 y 100

        Args:
            team_id: ID del equipo
            offset: Índice de inicio (default: 0)
            limit: Cantidad de resultados (default: 10, max: 100)

        Returns:
            Dict con heroes, total, offset, limit, has_next, has_previous, team_info

        Raises:
            ValidationError: Si los parámetros son inválidos
            NotFound: Si el team no existe
        """
        # Validación 1: Team debe existir
        team = self.team_repository.get_team_by_id(team_id)
        if not team:
            raise NotFound({"detail": f"No existe un equipo con ID {team_id}"})

        # Validación 2: Offset no negativo
        if offset < 0:
            raise ValidationError({"offset": "El offset debe ser mayor o igual a 0"})

        # Validación 3: Limit entre 1 y 100
        if limit < 1 or limit > 100:
            raise ValidationError({"limit": "El limit debe estar entre 1 y 100"})

        # Obtener heroes del team
        heroes, total = self.hero_repository.get_heroes_by_team(team_id, offset, limit)

        # Calcular has_next y has_previous
        has_next = (offset + limit) < total
        has_previous = offset > 0

        return {
            "heroes": heroes,
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_next": has_next,
            "has_previous": has_previous,
            "team_info": {
                "id": team.id,
                "nombre": team.nombre,
                "descripcion": team.descripcion
            }
        }

    # ==================== UPDATE ====================
    def update_hero(
        self,
        hero_id: int,
        nombre: str = None,
        descripcion: str = None,
        poder_principal: str = None,
        nivel: int = None,
        team_id: int = None
    ) -> Hero:
        """
        Actualiza un héroe existente.

        Validaciones:
        1. Héroe debe existir
        2. Si se actualiza el nombre: no puede estar vacío, no puede exceder 255 chars,
           no puede ser igual a otro héroe existente
        3. Si se actualiza el nivel: debe estar entre 1 y 100
        4. Si se actualiza el poder: no puede exceder 255 caracteres
        5. Si se actualiza el team: el nuevo team debe existir

        Args:
            hero_id: ID del héroe a actualizar
            nombre: Nuevo nombre (opcional)
            descripcion: Nueva descripción (opcional)
            poder_principal: Nuevo poder (opcional)
            nivel: Nuevo nivel (opcional)
            team_id: Nuevo team ID (opcional)

        Returns:
            Hero: Héroe actualizado

        Raises:
            ValidationError: Si alguna validación falla
            NotFound: Si el héroe no existe
        """
        # Validación 1: Héroe debe existir
        hero = self.hero_repository.get_hero_by_id(hero_id)
        if not hero:
            raise NotFound({"detail": f"No se encontró el héroe con ID {hero_id}"})

        # Validación 2: Si se actualiza el nombre
        if nombre is not None:
            if nombre.strip() == "":
                raise ValidationError({"nombre": "El nombre del héroe no puede estar vacío"})

            if len(nombre) > 255:
                raise ValidationError({"nombre": "El nombre no puede exceder 255 caracteres"})

            # Verificar que no exista otro héroe con ese nombre
            existing_hero = self.hero_repository.get_hero_by_name(nombre.strip())
            if existing_hero and existing_hero.id != hero_id:
                raise ValidationError({
                    "nombre": f"Ya existe otro héroe con el nombre '{nombre.strip()}'"
                })

        # Validación 3: Si se actualiza el nivel
        if nivel is not None:
            if nivel < 1 or nivel > 100:
                raise ValidationError({"nivel": "El nivel debe estar entre 1 y 100"})

        # Validación 4: Si se actualiza el poder principal
        if poder_principal is not None and len(poder_principal) > 255:
            raise ValidationError({
                "poder_principal": "El poder principal no puede exceder 255 caracteres"
            })

        # Validación 5: Si se actualiza el team
        team = None
        if team_id is not None:
            team = self.team_repository.get_team_by_id(team_id)
            if not team:
                raise ValidationError({"team_id": f"No existe un equipo con ID {team_id}"})

        # Actualizar héroe
        hero = self.hero_repository.update_hero(
            hero_id=hero_id,
            nombre=nombre.strip() if nombre else None,
            descripcion=descripcion.strip() if descripcion else None,
            poder_principal=poder_principal.strip() if poder_principal else None,
            nivel=nivel,
            team=team
        )

        return hero

    # ==================== DELETE ====================
    def delete_hero(self, hero_id: int) -> Dict[str, Any]:
        """
        Elimina un héroe.

        Validaciones:
        1. Héroe debe existir

        Args:
            hero_id: ID del héroe a eliminar

        Returns:
            Dict con mensaje de éxito y ID del héroe eliminado

        Raises:
            NotFound: Si el héroe no existe
        """
        # Validación 1: Héroe debe existir
        hero = self.hero_repository.get_hero_by_id(hero_id)
        if not hero:
            raise NotFound({"detail": f"No se encontró el héroe con ID {hero_id}"})

        # Guardar información para el mensaje
        hero_nombre = hero.nombre
        team_nombre = hero.team.nombre

        # Eliminar
        self.hero_repository.delete_hero(hero_id)

        return {
            "message": f"Héroe '{hero_nombre}' del equipo '{team_nombre}' eliminado exitosamente",
            "id": hero_id
        }
