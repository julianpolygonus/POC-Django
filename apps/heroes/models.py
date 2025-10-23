"""
Modelos de base de datos para Heroes

Este modelo representa a los héroes que pertenecen a un equipo (Team).
Relación: Un Team puede tener MUCHOS Heroes, pero un Hero solo puede
pertenecer a UN Team (relación Many-to-One).
"""
from django.db import models
from apps.teams.models import Team


class Hero(models.Model):
    """
    Modelo Hero - Representa un héroe que pertenece a un equipo

    Relación con Team:
    - ForeignKey: Muchos heroes pueden pertenecer a un team
    - on_delete=models.CASCADE: Si se elimina el team, se eliminan sus heroes
    - related_name='heroes': Permite acceder a los heroes desde un team con team.heroes.all()
    """
    id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name="ID"
    )

    nombre = models.CharField(
        max_length=255,
        verbose_name="Nombre del héroe",
        help_text="Nombre del héroe (máximo 255 caracteres)"
    )

    descripcion = models.TextField(
        verbose_name="Descripción",
        blank=True,
        null=True,
        help_text="Descripción detallada del héroe"
    )

    poder_principal = models.CharField(
        max_length=255,
        verbose_name="Poder principal",
        blank=True,
        null=True,
        help_text="El superpoder principal del héroe"
    )

    nivel = models.IntegerField(
        verbose_name="Nivel de poder",
        default=1,
        help_text="Nivel de poder del héroe (1-100)"
    )

    # ========== RELACIÓN CON TEAM ==========
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,  # Si se elimina el team, se eliminan sus heroes
        related_name='heroes',      # Acceso inverso: team.heroes.all()
        verbose_name="Equipo",
        help_text="El equipo al que pertenece este héroe"
    )
    # =======================================

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
        help_text="Fecha y hora en que se creó el héroe"
    )

    class Meta:
        db_table = 'heroes'
        verbose_name = 'Héroe'
        verbose_name_plural = 'Héroes'
        ordering = ['-fecha_creacion']  # Ordenar por fecha de creación descendente

        # Índice para mejorar búsquedas por team
        indexes = [
            models.Index(fields=['team'], name='idx_hero_team'),
        ]

    def __str__(self):
        return f"{self.nombre} (Team: {self.team.nombre}, Nivel: {self.nivel})"

    def __repr__(self):
        return f"<Hero(id={self.id}, nombre='{self.nombre}', team_id={self.team_id})>"
