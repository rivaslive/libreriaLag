from django.urls import path, re_path
from apps.ventas.views import prueba

urlpatterns = [
    path('articulo/', prueba),
]
