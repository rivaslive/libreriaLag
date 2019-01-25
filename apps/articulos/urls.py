from django.urls import path, re_path
from apps.articulos.views import articulo, inventario, CrearArticulo, articuloDetalle

app_name='articulo'

urlpatterns = [
    path('articulo/', articulo, name="articulo"),
    path(r'^articulo_detalle/(?P<pk>\d+)/$', articuloDetalle, name="articuloDetalle"),
    path('crearArticulo/', CrearArticulo.as_view(), name="crearArticulo"),
    path('inventario/', inventario, name="inventario"),
]
