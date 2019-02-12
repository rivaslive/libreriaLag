from django.urls import path, re_path
from apps.articulos.views import articulo, inventario, CrearArticulo, articuloDetalle, buscar, inicio, generador
from django.contrib.auth.decorators import login_required

app_name='articulo'

urlpatterns = [
    path('generador/', login_required(generador) , name="generador"),
    path('buscar/', login_required(buscar) , name="buscar"),
    path('index/', login_required(inicio), name="index"),
    path('articulo/', login_required(articulo), name="articulo"),
    path(r'^articulo_detalle/(?P<pk>\d+)/$', login_required(articuloDetalle), name="articuloDetalle"),
    path('crearArticulo/', login_required(CrearArticulo.as_view()), name="crearArticulo"),
    path('inventario/', login_required(inventario), name="inventario"),
 
]

