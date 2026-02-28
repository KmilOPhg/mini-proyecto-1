from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Tarea

@csrf_exempt
def crear_tarea(request):
    if request.method == "GET":
        tareas = list(Tarea.objects.values())
        return JsonResponse(tareas, safe=False)

    if request.method == "POST":
        data = json.loads(request.body)
        tarea = Tarea.objects.create(nombre=data["nombre"])
        return JsonResponse({
            "id": tarea.id,
            "nombre": tarea.nombre
        })
