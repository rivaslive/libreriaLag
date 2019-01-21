from django.urls import path, re_path
from apps.articulos.views import articulo, inventario

app_name='articulo'

urlpatterns = [
    path('articulo/', articulo, name="articulo"),
    path('inventario/', inventario, name="inventario"),
]
