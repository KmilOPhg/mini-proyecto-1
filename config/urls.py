from django.contrib import admin
from django.urls import path
from focusflow.views import crear_tarea

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/tareas/", crear_tarea),
]
