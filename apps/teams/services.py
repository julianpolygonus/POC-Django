"""
Services Layer para Teams
Esta capa contiene la lógica de negocio y validaciones
"""
from typing import List, Dict, Optional, Tuple
from rest_framework.exceptions import ValidationError, NotFound
from .repository import TeamRepository
from .models import Team


class TeamService:
    """
    Servicio para manejar la lógica de negocio de Teams
    """

    def __init__(self):
        self.repository = TeamRepository()

    def create_team(self, nombre: str, descripcion: Optional[str] = None) -> Team:
        """
        Crea un nuevo team validando que no exista previamente

        Args:
            nombre: Nombre del team
            descripcion: Descripción del team (opcional)

        Returns:
            Team: Team creado

        Raises:
            ValidationError: Si el nombre está vacío o el team ya existe
        """
        # Validar que el nombre no esté vacío
        if not nombre or nombre.strip() == "":
            raise ValidationError({
                "nombre": "El nombre del team es requerido y no puede estar vacío"
            })

        # Validar longitud del nombre
        if len(nombre) > 255:
            raise ValidationError({
                "nombre": "El nombre del team no puede exceder 255 caracteres"
            })

        # Verificar que no exista un team con el mismo nombre
        if self.repository.exists_by_name(nombre):
            raise ValidationError({
                "nombre": f"Ya existe un team con el nombre '{nombre}'"
            })

        # Crear el team
        team = self.repository.create_team(
            nombre=nombre.strip(),
            descripcion=descripcion.strip() if descripcion else None
        )

        return team

    def get_team_by_id(self, team_id: int) -> Team:
        """
        Obtiene un team por su ID validando que exista

        Args:
            team_id: ID del team

        Returns:
            Team: Team encontrado

        Raises:
            NotFound: Si el team no existe
        """
        # Validar que el ID sea válido
        if team_id <= 0:
            raise ValidationError({
                "id": "El ID debe ser un número positivo"
            })

        # Buscar el team
        team = self.repository.get_team_by_id(team_id)

        if not team:
            raise NotFound({
                "detail": f"No se encontró el team con ID {team_id}"
            })

        return team

    def get_team_by_name(self, nombre: str) -> Team:
        """
        Obtiene un team por su nombre validando que exista

        Args:
            nombre: Nombre del team

        Returns:
            Team: Team encontrado

        Raises:
            NotFound: Si el team no existe
        """
        # Validar que el nombre no esté vacío
        if not nombre or nombre.strip() == "":
            raise ValidationError({
                "nombre": "El nombre del team es requerido para la búsqueda"
            })

        # Buscar el team
        team = self.repository.get_team_by_name(nombre.strip())

        if not team:
            raise NotFound({
                "detail": f"No se encontró el team con nombre '{nombre}'"
            })

        return team

    def get_all_teams(self, offset: int = 0, limit: int = 10) -> Dict:
        """
        Obtiene todos los teams con paginación

        Args:
            offset: Índice de inicio (default: 0)
            limit: Cantidad de resultados (default: 10, max: 100)

        Returns:
            Dict: Diccionario con teams, total, offset y limit

        Raises:
            ValidationError: Si los parámetros de paginación son inválidos
        """
        # Validar parámetros de paginación
        if offset < 0:
            raise ValidationError({
                "offset": "El offset debe ser un número positivo o cero"
            })

        if limit <= 0:
            raise ValidationError({
                "limit": "El limit debe ser un número positivo mayor a cero"
            })

        if limit > 100:
            raise ValidationError({
                "limit": "El limit no puede ser mayor a 100"
            })

        # Obtener teams paginados
        teams, total = self.repository.get_all_teams(offset=offset, limit=limit)

        return {
            "teams": teams,
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_next": (offset + limit) < total,
            "has_previous": offset > 0
        }

    def update_team(self, team_id: int, nombre: Optional[str] = None,
                    descripcion: Optional[str] = None) -> Team:
        """
        Actualiza un team validando que exista y los datos sean válidos

        Args:
            team_id: ID del team a actualizar
            nombre: Nuevo nombre del team (opcional)
            descripcion: Nueva descripción del team (opcional)

        Returns:
            Team: Team actualizado

        Raises:
            NotFound: Si el team no existe
            ValidationError: Si los datos son inválidos
        """
        # Validar que el ID sea válido
        if team_id <= 0:
            raise ValidationError({
                "id": "El ID debe ser un número positivo"
            })

        # Verificar que el team exista
        if not self.repository.exists_by_id(team_id):
            raise NotFound({
                "detail": f"No se encontró el team con ID {team_id}"
            })

        # Validar que al menos un campo se esté actualizando
        if nombre is None and descripcion is None:
            raise ValidationError({
                "detail": "Debe proporcionar al menos un campo para actualizar (nombre o descripcion)"
            })

        # Preparar datos para actualizar
        update_data = {}

        # Validar y agregar nombre si se proporciona
        if nombre is not None:
            if nombre.strip() == "":
                raise ValidationError({
                    "nombre": "El nombre no puede estar vacío"
                })

            if len(nombre) > 255:
                raise ValidationError({
                    "nombre": "El nombre del team no puede exceder 255 caracteres"
                })

            # Verificar que no exista otro team con el mismo nombre
            existing_team = self.repository.get_team_by_name(nombre.strip())
            if existing_team and existing_team.id != team_id:
                raise ValidationError({
                    "nombre": f"Ya existe otro team con el nombre '{nombre}'"
                })

            update_data['nombre'] = nombre.strip()

        # Agregar descripción si se proporciona
        if descripcion is not None:
            update_data['descripcion'] = descripcion.strip() if descripcion else None

        # Actualizar el team
        team = self.repository.update_team(team_id, **update_data)

        return team

    def delete_team(self, team_id: int) -> Dict:
        """
        Elimina un team validando que exista

        Args:
            team_id: ID del team a eliminar

        Returns:
            Dict: Mensaje de confirmación

        Raises:
            NotFound: Si el team no existe
        """
        # Validar que el ID sea válido
        if team_id <= 0:
            raise ValidationError({
                "id": "El ID debe ser un número positivo"
            })

        # Verificar que el team exista antes de eliminar
        team = self.repository.get_team_by_id(team_id)
        if not team:
            raise NotFound({
                "detail": f"No se encontró el team con ID {team_id}"
            })

        # Guardar información del team antes de eliminar
        team_name = team.nombre

        # Eliminar el team
        deleted = self.repository.delete_team(team_id)

        if not deleted:
            raise ValidationError({
                "detail": "No se pudo eliminar el team"
            })

        return {
            "message": f"Team '{team_name}' eliminado exitosamente",
            "id": team_id
        }
