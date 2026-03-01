from django.urls import path, include
from rest_framework import routers
from focusflow import views

router = routers.DefaultRouter()
router.register(r'tareas', views.VistaTarea, 'tareas')

#Lo que sigue despues de la ruta en config urls
#EJEMPLO: (desde config/urls) /api/tareas
urlpatterns = [
    path('api/', include(router.urls))
]