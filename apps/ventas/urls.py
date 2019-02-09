from django.urls import path, re_path
from apps.ventas.views import prueba, addCar, carShopping, shop,venta, eliminarDetalle
app_name='ventas'

urlpatterns = [
    path('articulo/', prueba),
    path('car_shopping/', carShopping, name="carShopping"),
    path(r'^add_car/(?P<pk>\d+)/$', addCar, name="addCar"),
    path(r'^deleteDetail/(?P<pk>\d+)/$', eliminarDetalle, name="deleteDetail"),
    path('shop/', shop, name="shop"),
    path('venta/', venta, name="venta"),
]
