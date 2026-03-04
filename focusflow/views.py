from rest_framework import viewsets, status
from focusflow.serializer import TareaSerializer
from .models import Tarea
from rest_framework.response import Response


class VistaTarea(viewsets.ModelViewSet):
    serializer_class = TareaSerializer

    def get_queryset(self):
        # Traemos las que no tienen padre
        if self.action == 'list':
            return Tarea.objects.filter(parent__isnull=True).prefetch_related('subtareas')
        return Tarea.objects.all()

    # Mensaje al crear una tarea
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "mensaje": "¡Tarea creada exitosamente!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "mensaje": "Error al validar los datos de la tarea",
            "errores": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # Mensaje al actualizar una tarea
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) # Soporta PATCH (actualización parcial)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                "mensaje": "Tarea actualizada correctamente",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "mensaje": "Error en la actualización de la tarea",
            "errores": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # Mensaje al eliminar una tarea
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        nombre = instance.nombre
        self.perform_destroy(instance)
        return Response({
            "mensaje": f"La tarea '{nombre}' ha sido eliminada con éxito."
        }, status=status.HTTP_200_OK) # Cambiamos a 200 para que el cuerpo del mensaje sea visible
