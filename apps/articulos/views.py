from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.articulos.models import Articulo
from apps.articulos.forms import ArticuloForm

#ver articulos
def articulo(request):
    query=Articulo.objects.filter(is_activate=1)
    return render(request, 'productos/articulo.html', {'articulo':query})


#crear articulos
class CrearArticulo(CreateView):
    template_name = 'productos/productoModal.html'
    form_class = ArticuloForm
    success_url = reverse_lazy('articulo:articulo')


def inventario(request):
    return render(request, 'productos/inventario.html')