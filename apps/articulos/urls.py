from django.urls import path, re_path
from apps.articulos.views import articulo, inventario, CrearArticulo

app_name='articulo'

urlpatterns = [
    path('articulo/', articulo, name="articulo"),
    path('crearArticulo/', CrearArticulo.as_view(), name="crearArticulo"),
    path('inventario/', inventario, name="inventario"),
]
