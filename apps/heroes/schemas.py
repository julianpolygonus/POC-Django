"""
Schemas (Serializers) para Heroes

Define tres schemas principales:
1. HeroCreateSchema - Para crear un nuevo héroe (sin ID)
2. HeroReadSchema - Para leer un héroe existente (con todos los campos + info del team)
3. HeroUpdateSchema - Para actualizar un héroe (todos los campos opcionales excepto ID)

Importante sobre la relación con Team:
- Al crear/actualizar: Se envía solo team_id (entero)
- Al leer: Se retorna team_id + información completa del team (nombre, descripción)
"""
from rest_framework import serializers
from .models import Hero
from apps.teams.models import Team


# ========== SERIALIZER ANIDADO PARA TEAM ==========
class TeamNestedSerializer(serializers.ModelSerializer):
    """
    Serializer anidado para mostrar información del Team dentro de Hero.

    Esto permite que cuando consultes un Hero, también veas información
    básica de su Team sin hacer otra petición.

    Ejemplo de respuesta:
    {
        "id": 1,
        "nombre": "Superman",
        "team_id": 5,
        "team": {
            "id": 5,
            "nombre": "Justice League",
            "descripcion": "Los héroes más poderosos"
        }
    }
    """
    class Meta:
        model = Team
        fields = ['id', 'nombre', 'descripcion']
        read_only_fields = ['id', 'nombre', 'descripcion']


# ========== CREATE SCHEMA ==========
class HeroCreateSchema(serializers.ModelSerializer):
    """
    Schema para CREAR un nuevo héroe.

    Campos requeridos:
    - nombre: Nombre del héroe
    - team_id: ID del equipo al que pertenece (debe existir)

    Campos opcionales:
    - descripcion: Descripción del héroe
    - poder_principal: Su superpoder
    - nivel: Nivel de poder (default: 1)

    Campos automáticos (NO enviar):
    - id: Se genera automáticamente
    - fecha_creacion: Se genera automáticamente
    """
    # Usamos PrimaryKeyRelatedField para aceptar solo el ID del team
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        source='team',
        write_only=True,
        help_text="ID del equipo al que pertenece el héroe"
    )

    class Meta:
        model = Hero
        fields = [
            'nombre',
            'descripcion',
            'poder_principal',
            'nivel',
            'team_id',  # Solo el ID al crear
        ]
        extra_kwargs = {
            'nombre': {
                'required': True,
                'help_text': 'Nombre del héroe (requerido)'
            },
            'descripcion': {
                'required': False,
                'help_text': 'Descripción del héroe (opcional)'
            },
            'poder_principal': {
                'required': False,
                'help_text': 'Superpoder principal (opcional)'
            },
            'nivel': {
                'required': False,
                'default': 1,
                'help_text': 'Nivel de poder del héroe (1-100, default: 1)'
            },
        }

    def validate_nombre(self, value):
        """Validar que el nombre no esté vacío"""
        if not value or value.strip() == "":
            raise serializers.ValidationError("El nombre del héroe no puede estar vacío")
        return value.strip()

    def validate_nivel(self, value):
        """Validar que el nivel esté entre 1 y 100"""
        if value < 1 or value > 100:
            raise serializers.ValidationError("El nivel debe estar entre 1 y 100")
        return value


# ========== READ SCHEMA ==========
class HeroReadSchema(serializers.ModelSerializer):
    """
    Schema para LEER un héroe existente.

    Incluye TODOS los campos del modelo, incluyendo:
    - id: ID del héroe
    - fecha_creacion: Fecha de creación
    - team_id: ID del equipo
    - team: Información completa del equipo (anidada)

    Este schema retorna más información que el Create/Update para
    proporcionar el contexto completo del héroe.
    """
    # Mostrar el ID del team como campo separado
    team_id = serializers.IntegerField(source='team.id', read_only=True)

    # Mostrar información completa del team anidada
    team = TeamNestedSerializer(read_only=True)

    class Meta:
        model = Hero
        fields = [
            'id',
            'nombre',
            'descripcion',
            'poder_principal',
            'nivel',
            'team_id',      # ID del team (para referencia rápida)
            'team',         # Objeto completo del team (para ver detalles)
            'fecha_creacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'team_id', 'team']


# ========== UPDATE SCHEMA ==========
class HeroUpdateSchema(serializers.ModelSerializer):
    """
    Schema para ACTUALIZAR un héroe existente.

    Todos los campos son OPCIONALES (puedes actualizar solo lo que necesites).

    Campos actualizables:
    - nombre
    - descripcion
    - poder_principal
    - nivel
    - team_id (cambiar el héroe de equipo)

    Campos NO actualizables:
    - id (nunca se puede cambiar)
    - fecha_creacion (se establece solo al crear)
    """
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        source='team',
        required=False,  # Opcional al actualizar
        help_text="ID del equipo (opcional, para cambiar de equipo)"
    )

    class Meta:
        model = Hero
        fields = [
            'nombre',
            'descripcion',
            'poder_principal',
            'nivel',
            'team_id',
        ]
        extra_kwargs = {
            'nombre': {
                'required': False,
                'help_text': 'Nombre del héroe (opcional)'
            },
            'descripcion': {
                'required': False,
                'help_text': 'Descripción del héroe (opcional)'
            },
            'poder_principal': {
                'required': False,
                'help_text': 'Superpoder principal (opcional)'
            },
            'nivel': {
                'required': False,
                'help_text': 'Nivel de poder (1-100, opcional)'
            },
        }

    def validate_nombre(self, value):
        """Validar que el nombre no esté vacío si se proporciona"""
        if value is not None and value.strip() == "":
            raise serializers.ValidationError("El nombre del héroe no puede estar vacío")
        return value.strip() if value else value

    def validate_nivel(self, value):
        """Validar que el nivel esté entre 1 y 100 si se proporciona"""
        if value is not None and (value < 1 or value > 100):
            raise serializers.ValidationError("El nivel debe estar entre 1 y 100")
        return value

    def update(self, instance, validated_data):
        """
        Actualizar solo los campos que se enviaron en el request.
        Los campos no enviados mantienen su valor actual.
        """
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.poder_principal = validated_data.get('poder_principal', instance.poder_principal)
        instance.nivel = validated_data.get('nivel', instance.nivel)
        instance.team = validated_data.get('team', instance.team)

        instance.save()
        return instance
