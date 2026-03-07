from django.db import models
from django.utils import timezone


class Tarea(models.Model):
    # 1. Definimos las opciones del Enum aquí dentro
    class TipoTarea(models.TextChoices):
        EXAMEN = 'EX', 'Examen'
        QUIZ = 'QU', 'Quiz'
        TALLER = 'TA', 'Taller'
        PROYECTO = 'PR', 'Proyecto'
        OTRO = 'OT', 'Otro'

    nombre = models.CharField(max_length=100, help_text="El nombre descriptivo de la tarea")
    descripcion = models.CharField(max_length=100, null=True, blank=True, help_text="La descripción de la tarea")
    completada = models.BooleanField(default=False, help_text="Casilla para marcar la tarea como completa")
    fecha_entrega = models.DateTimeField(null=True, blank=True, help_text="Formato: AAAA-MM-DD HH:MM:SS")
    fecha_creacion = models.DateTimeField(default=timezone.now, help_text="Fecha de creacion de la tarea")
    carga_mental = models.CharField(null=True, blank=True, max_length=100, help_text="Carga mental (1-5)")

    #Así se define el campo tipo_tarea
    tipo_tarea = models.CharField(
        max_length=2,
        choices=TipoTarea.choices,
        default=TipoTarea.OTRO,
        help_text="Selecciona el tipo de tarea"
    )

    curso = models.CharField(null=True, blank=True, max_length=255, help_text="Casilla para el curso")

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subtareas',
        help_text="ID de la tarea padre"
    )

    def save(self, *args, **kwargs):
        # Herencia lógica de la tarea padre a la subtarea
        if self.parent:
            # Heredar fecha de entrega si la subtarea no tiene una propia
            if not self.fecha_entrega:
                self.fecha_entrega = self.parent.fecha_entrega

            # Heredar carga mental
            if not self.carga_mental:
                self.carga_mental = self.parent.carga_mental

            # Heredar el TIPO DE TAREA del Enum
            if not self.tipo_tarea or self.tipo_tarea == self.TipoTarea.OTRO:
                self.tipo_tarea = self.parent.tipo_tarea

            # Descripción automática basada en el padre
            if not self.descripcion:
                self.descripcion = f"Subtarea de: {self.parent.nombre}"

            # Herencia del curso
            if not self.curso:
                self.curso = self.parent.curso

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
