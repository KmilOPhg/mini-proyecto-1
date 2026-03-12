from rest_framework import serializers
from .models import Tarea
from django.contrib.auth.models import User
import re


# Serializador para crear tareas
class TareaSerializer(serializers.ModelSerializer):
    # Esto mostrará la lista de subtareas dentro de cada tarea
    subtareas = serializers.SerializerMethodField()

    class Meta:
        model = Tarea
        fields = '__all__'

    # subtareas = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def get_subtareas(self, obj):
        # Buscamos las tareas cuyo padre sea la tarea actual
        hijos = Tarea.objects.filter(parent=obj)
        return TareaSerializer(hijos, many=True).data


# Serializador para crear usuarios
class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # Añadimos el campo nombre_completo que no está en el modelo original
    nombre_completo = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'nombre_completo']

    def validate_username(self, value):
        if not re.match(r'^[\w.-]+$', value):
            raise serializers.ValidationError(
                "El nombre de usuario no debe contener espacios ni caracteres especiales."
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value

    def create(self, validated_data):
        nombre = validated_data.pop('nombre_completo', '')

        # Creamos el usuario
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=nombre  # AQUÍ se guardan los espacios (Ej: Juan Pérez)
        )
        return user
