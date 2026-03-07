from django.db import models

class Tarea(models.Model):
    nombre = models.CharField(max_length=100, help_text="El nombre descriptivo de la tarea")
    # Añadimos null y blank para que no sea obligatoria en subtareas
    descripcion = models.CharField(max_length=100, null=True, blank=True, help_text="La descripción de la tarea")
    completada = models.BooleanField(default=False, help_text="Casilla para marcar la tarea como completa")
    fecha_entrega = models.DateTimeField(null=True, blank=True, help_text="Formato: AAAA-MM-DD HH:MM:SS")
    carga_mental = models.CharField(null=True, blank=True, max_length=100, help_text="Carga mental (1-5)")

    # Definimos el parent arriba
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subtareas',
        help_text="ID de la tarea padre"
    )

    def save(self, *args, **kwargs):
        # Herencia lógica
        if self.parent:
            if not self.fecha_entrega:
                self.fecha_entrega = self.parent.fecha_entrega
            if not self.carga_mental:
                self.carga_mental = self.parent.carga_mental
            if not self.descripcion:
                self.descripcion = f"Subtarea de: {self.parent.nombre}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre