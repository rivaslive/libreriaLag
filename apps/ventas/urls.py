from django.urls import path, re_path
from apps.ventas.views import prueba, carShopping,regresarVentas, reporte, shop,venta, eliminarDetalle, vender, ticket, drop, editarShop, llenarTablaVentas, detalleVenta
from django.contrib.auth.decorators import login_required
app_name = 'ventas'

urlpatterns = [
    path('articulo/', login_required(prueba)),
    path('vender/', login_required(vender), name="vender"),
    path('drop/', login_required(drop), name="drop"),
    path('ticket/', login_required(ticket), name="ticket"),
    path('car_shopping/',  login_required(carShopping), name="carShopping"),

    path(r'^deleteDetail/(?P<pk>\d+)/$',  login_required(eliminarDetalle), name="deleteDetail"),
    path(r'^editarShop/(?P<pk>\d+)/$',  login_required(editarShop), name="editarShop"),
    path(r'^detalleVenta/(?P<pk>\d+)/$',  login_required(detalleVenta), name="detalleVenta"),
    path(r'^regresarVentas/(?P<pk>\d+)/$',  login_required(regresarVentas), name="regresarVentas"),
    path('shop/',  login_required(shop), name="shop"),
    path('venta/',  login_required(venta), name="venta"),
    path('listventa/', login_required(llenarTablaVentas), name="listVenta"),
    path('reporte/', login_required(reporte), name="reporte")
]
