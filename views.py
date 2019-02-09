# Create your views here.
import time
from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.views.generic.edit import BaseCreateView

from apps.productos.form import ProductoForm
from apps.productos.models import Producto

from django.db.models import Q


def ListadoProducto(request):
    user = request.user
    if user.has_perm('producto.is_admin'):
        producto = Producto.objects.all().order_by("-id")
        return render(request, 'productos/producto.html', {'productos': producto})
    else:
        return redirect('ventas:error')

# BUSCADOR DE PRODUCTOS
def productoBuscar(request):
    user = request.user
    if user.has_perm('producto.is_admin'):
        buscar = request.GET.get('buscar', '')
        print (buscar)
        queryset = Producto.objects.filter(Q(nombre__contains=buscar)|Q(categoria__nombre__contains=buscar)).order_by('nombre')
        return render(request, 'productos/producto.html', {'productos': queryset, 'busq':buscar})
    else:
        return redirect('ventas:error')


class CreateProducto(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/productoModal.html'
    success_url = reverse_lazy('productos:producto')

    #def post(self, request, *args, **kwargs):
    #    user = self.request.user
    #    if user.has_perm('producto.is_admin'):

     #       form_class = self.get_form_class()
     #       form = self.get_form(form_class)
     #       if form.is_valid():
    #            post = form.save(commit=False)
    #            if post.precio >= post.precio_neto and post.precio >= post.precio_promo:
     #               return self.form_valid(form)
     #           return redirect('productos:create_producto')
     #       else:
     #           return redirect('productos:create_producto')
    #    else:
     #       return redirect('ventas:error')

class UpdateProducto(UpdateView):
    model = Producto
    template_name = 'productos/productoModal.html'
    form_class = ProductoForm
    success_url = reverse_lazy('productos:producto')


class DetalleProducto(DetailView):
    model = Producto
    template_name = 'productos/detalle_producto.html'


def EliminarProducto(request, pk):
    producto = Producto.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductoForm(instance=producto)
        post = form.save(commit=False)
        post.estado = 0
        post.save()
        return redirect('productos:producto')
    else:
        return render(request, 'productos/deleteModel.html', {'productos': producto})


def Index(request):
    user = request.user
    if user.has_perm('producto.is_admin'):
        return render(request, 'default/index.html')
    elif user.has_perm('productos.is_user'):
        return redirect('ventas:venta')
    else:
        return redirect('ventas:error')


def prueba(request):
    return render(request, 'productos/prueba.html')


def img(request, pk):
    img = Producto.objects.get(id=pk)
    return render(request, 'productos/imgModal.html', {'img': img})
