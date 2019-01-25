from django.urls import path, re_path
from apps.ventas.views import prueba, addCar
app_name='ventas'

urlpatterns = [
    path('articulo/', prueba),
    path(r'^add_car/(?P<pk>\d+)/$', addCar, name="addCar"),
]
