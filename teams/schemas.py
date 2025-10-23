"""
Schemas (serializadores) para la app teams
"""
from rest_framework import serializers
from .models import Team


class TeamCreateSchema(serializers.ModelSerializer):
    """
    Schema para crear un Team
    No incluye el ID ya que es autogenerado
    """
    nombre = serializers.CharField(
        max_length=255,
        required=True,
        help_text="Nombre del equipo"
    )
    descripcion = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="Descripción del equipo"
    )
    fecha_creacion = serializers.DateTimeField(
        required=False,
        read_only=True,
        help_text="Fecha de creación (generada automáticamente)"
    )

    class Meta:
        model = Team
        fields = ['nombre', 'descripcion', 'fecha_creacion']
        read_only_fields = ['fecha_creacion']


class TeamReadSchema(serializers.ModelSerializer):
    """
    Schema para leer un Team
    Incluye todos los campos incluyendo el ID
    """
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(allow_null=True, allow_blank=True)
    fecha_creacion = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'nombre', 'descripcion', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']


class TeamUpdateSchema(serializers.ModelSerializer):
    """
    Schema para actualizar un Team
    Todos los campos son opcionales excepto el ID (que no se incluye)
    """
    nombre = serializers.CharField(
        max_length=255,
        required=False,
        help_text="Nombre del equipo"
    )
    descripcion = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="Descripción del equipo"
    )

    class Meta:
        model = Team
        fields = ['nombre', 'descripcion']
        # Todos los campos son opcionales en el update
        extra_kwargs = {
            'nombre': {'required': False},
            'descripcion': {'required': False},
        }

    def update(self, instance, validated_data):
        """
        Actualiza solo los campos que fueron enviados
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
