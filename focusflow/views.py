from rest_framework import viewsets, status, generics, permissions
from focusflow.serializer import TareaSerializer, RegistroSerializer
from .models import Tarea
from rest_framework.response import Response

# VISTA DE REGISTRO
class VistaRegistro(generics.CreateAPIView):
    serializer_class = RegistroSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "mensaje": f"¡Usuario {user.username} creado exitosamente!",
            }, status=status.HTTP_201_CREATED)

        # Si llega aquí, es un 400. Devolvemos los errores específicos de Django.
        return Response({
            "mensaje": "Error en el registro",
            "errores": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# VISTA TAREAS PROTEGIDA
class VistaTarea(viewsets.ModelViewSet):
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated] # Obligatorio estar logueado

    def get_queryset(self):
        # Traemos las que no tienen padre
        # solo devuelve tareas del usuario que hace la petición
        user = self.request.user
        if self.action == 'list':
            return Tarea.objects.filter(usuario=user, parent__isnull=True).prefetch_related('subtareas')
        return Tarea.objects.filter(usuario=user)


    def perform_create(self, serializer):
        # Asigna automáticamente el usuario logueado a la nueva tarea
        serializer.save(usuario=self.request.user)

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
