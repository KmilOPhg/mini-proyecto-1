from django.contrib import admin
from django.urls import path, include
from focusflow.views import VistaTarea

#Aqui es como empieza la ruta
#EJEMPLO tareas/ (ir a urls de focusflow))
urlpatterns = [
    path('admin/', admin.site.urls),
    path("tareas/", include('focusflow.urls')),
]
