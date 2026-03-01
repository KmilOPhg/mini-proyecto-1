from django.db import models

class Tarea(models.Model):
    nombre = models.CharField(max_length=100) #Es para decir que esto es un string en la bd

    #Que dato ver en el panel de admin de django
    def __str__(self):
        return self.nombre