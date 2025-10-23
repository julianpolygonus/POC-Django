from django.db import models


class Team(models.Model):
    """
    Modelo para representar un equipo (Team)
    """
    id = models.AutoField(primary_key=True, editable=False)
    nombre = models.CharField(max_length=255, verbose_name="Nombre del equipo")
    descripcion = models.TextField(verbose_name="Descripción del equipo", blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        db_table = 'teams'
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} (ID: {self.id})"
