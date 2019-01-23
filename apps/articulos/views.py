from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.articulos.models import Articulo
from apps.articulos.forms import ArticuloForm
from django.db.models import Q


# ver articulos


def articulo(request):
    query = Articulo.objects.filter(is_activate=1)
    return render(request, 'productos/articulo.html', {'articulo': query})


# crear articulos
class CrearArticulo(CreateView):
    template_name = 'productos/productoModal.html'
    form_class = ArticuloForm
    success_url = reverse_lazy('articulo:articulo')

# Mostrar los productos sin stock


def inventario(request):
    # Articulos con estado activo, con stock mayor que 1 pero menores que 10
    query = Articulo.objects.filter(Q(stock__gt=0) & Q(stock__lt=11)).exclude(is_activate=0)
    # Articulos con 0 existencias
    query_ar = Articulo.objects.filter(stock=0).exclude(is_activate=0)
    # Todos los demás articulos mayores ue 10
    query_are = Articulo.objects.filter(stock__gt=10).exclude(is_activate=0)

    return render(request, 'productos/inventario.html', {'inventario1': query, 'inventario': query_ar, 'inventariop': query_are})
