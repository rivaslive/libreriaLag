from django.urls import path, re_path
from apps.ventas.views import prueba, addCar, carShopping, shop
app_name='ventas'

urlpatterns = [
    path('articulo/', prueba),
    path('car_shopping/', carShopping, name="carShopping"),
    path(r'^add_car/(?P<pk>\d+)/$', addCar, name="addCar"),
    path('shop/', shop, name="shop"),
]
