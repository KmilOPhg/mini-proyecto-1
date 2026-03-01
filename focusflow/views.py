from rest_framework import viewsets
from focusflow.serializer import TareaSerializer
from .models import Tarea


class VistaTarea(viewsets.ModelViewSet):
    serializer_class = TareaSerializer
    queryset = Tarea.objects.all()
