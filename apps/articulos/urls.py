from django.urls import path, re_path
from apps.articulos.views import articulo, habilitarArticulo,mostrarDeshabilitados ,inventario, CrearArticulo, ArticuloListClass, articuloListJSON,articuloDetalle, buscar, inicio, generador, articulo_edi, actualizarEstado
from django.contrib.auth.decorators import login_required
from  rest_framework.urlpatterns import format_suffix_patterns

app_name='articulo'

urlpatterns = [
    path('generador/', login_required(generador) , name="generador"),
    path('buscar/', login_required(buscar) , name="buscar"),
    path('index/', login_required(inicio), name="index"),
    path('articulo/', login_required(articulo), name="articulo"),
    path(r'^articulo_detalle/(?P<pk>\d+)/$', login_required(articuloDetalle), name="articuloDetalle"),
    path(r'^editarInventario/(?P<pk>\d+)/$', login_required(articulo_edi), name="editarInventario"),
    path(r'^darBaja/(?P<pk>\d+)/$', login_required(actualizarEstado), name="darBaja"),
    path(r'^darAlta/(?P<pk>\d+)/$', login_required(habilitarArticulo), name="darAlta"),

    path('crearArticulo/', login_required(CrearArticulo.as_view()), name="crearArticulo"),
    path('inventario/', login_required(inventario), name="inventario"),
    path('deshabilitado/', login_required(mostrarDeshabilitados), name="deshabilitado"),
    path('articulo_list_json/', articuloListJSON, name="articulo_list_json"),
    path('articulo_list/', ArticuloListClass.as_view(), name="articuloList"),

]

urlpatterns = format_suffix_patterns(urlpatterns)