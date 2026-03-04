from rest_framework import serializers
from .models import Tarea

class TareaSerializer(serializers.ModelSerializer):
    # Esto mostrará la lista de subtareas dentro de cada tarea
    subtareas = serializers.SerializerMethodField()

    class Meta:
        model = Tarea
        fields = '__all__'

    #subtareas = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def get_subtareas(self, obj):
        # Buscamos las tareas cuyo padre sea la tarea actual
        hijos = Tarea.objects.filter(parent=obj)
        return TareaSerializer(hijos, many=True).data