from django.db import models

class Tarea(models.Model):
    nombre = models.CharField(max_length=100, help_text="El nombre descriptivo de la tarea")
    completada = models.BooleanField(default=False, help_text="Casilla para marcar la tarea como completa")

    # null=True y blank=True permiten que las tareas principales no tengan padre.
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subtareas',
        help_text="ID de la tarea padre, si esto es tarea padre se deja vacio"
    )

    def __str__(self):
        return self.nombre