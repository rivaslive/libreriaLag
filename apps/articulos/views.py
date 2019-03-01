from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import status, generics

from apps.articulos.models import Articulo
from apps.articulos.forms import ArticuloForm
from django.db.models import Sum, Q
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.articulos.serializers import ArticuloSerializer

# ver articulos
from apps.ventas.models import detalle
import json
from chartjs.views.lines import BaseLineChartView
from django.views.generic import TemplateView



def articulo(request):
    try:
        if request.session['ventaId']:
            ventaId = request.session['ventaId']
            notify = detalle.objects.filter(id_venta=ventaId).count()
            query = Articulo.objects.filter(is_activate=1).order_by('-pk')
            return render(request, 'productos/articulo.html', {'articulo': query, 'notify':notify})
        else:
            request.session['ventaId'] = ''
            query = Articulo.objects.filter(is_activate=1).order_by('-pk')
            return render(request, 'productos/articulo.html', {'articulo': query})
    except:
        request.session['ventaId'] = ''
        query = Articulo.objects.filter(is_activate=1)
        return render(request, 'productos/articulo.html', {'articulo': query})
# ver articulos



def articuloDetalle(request, pk):
    query = Articulo.objects.get(id=pk)
    return render(request, 'productos/articuloDetalle.html', {'articulo': query})



# crear articulos
class CrearArticulo(SuccessMessageMixin, CreateView):
    template_name = 'productos/productoModal.html'
    form_class = ArticuloForm

    def get_success_url(self):
        return reverse_lazy('articulo:articulo')
    success_message = 'Operacion Exitosa'



# Mostrar los productos sin stock
def inventario(request):
    codigo = request.POST.get('codigo', '')
    if codigo == "1234":
        # Articulos con estado activo, con stock mayor que 1 pero menores que 10
        query = Articulo.objects.filter(Q(stock__gt=0) & Q(stock__lt=11)).exclude(is_activate=0).order_by('stock')
        # Articulos con 0 existencias
        query_ar = Articulo.objects.filter(stock=0).exclude(is_activate=0).order_by('stock')
        # Todos los demás articulos mayores ue 10
        query_are = Articulo.objects.filter(stock__gt=10).exclude(is_activate=0).order_by('stock')
        return render(request, 'productos/inventario.html', {'inventario1': query, 'inventario': query_ar, 'inventariop': query_are})
    else:
        if codigo:
            messages.warning(request, 'Codigo Incorrecto')
            return redirect('articulo:articulo')
        return render(request, 'base/codigo.html')
        


    #Buscar Articulos
def buscar(request):
    buscar= request.GET.get('search','')
    queryset = Articulo.objects.filter(Q(nombre_articulo__icontains=buscar)|Q(codigo_articulo__contains=buscar)).exclude(is_activate=0).order_by('nombre_articulo')

    return render(request,'productos/articulo.html',{'articulo':queryset, 'busqueda':buscar})



def inicio(request):

    return render(request, 'productos/index.html')


def generador(request):
    try:
        evaluation = request.POST.get('evaluation', '')
        if evaluation:
            articulos = Articulo.objects.values_list('codigo_articulo', flat=True).order_by('pk')
            print(articulos)
            i = 0
            while i == 0:
                codigo = random.randrange(1000000, 99999999, 1)
                articulos = Articulo.objects.filter(codigo_articulo=codigo).count()
                print(articulos)
                if articulos == 0:
                    return render(request, 'productos/generador.html', {'codigo': codigo})
                else:
                    print("funciona")
        else:
            return render(request, 'productos/generador.html')
    except:
        return render(request, 'productos/generador.html')



def articulo_edi(request, pk):
    articulo = Articulo.objects.get(id=pk)

    if request.method == 'GET':
        form = ArticuloForm(instance=articulo)
    else:
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Articulo editado correctamente')
        return redirect('articulo:inventario')
    return render(request, 'productos/productoModal.html', {'form': form, 'pk': pk, 'articulo':articulo})



def actualizarEstado(request, pk):
   arti = Articulo.objects.get(id=pk)
   if request.method == 'POST':
     respuesta = get_object_or_404(Articulo, pk=arti.pk)
     respuesta.is_activate = 0
     respuesta.save()
     messages.success(request, 'Articulo deshabilitado')
     return redirect('articulo:deshabilitado')
   return render(request, 'productos/cambiarEstadoModal.html', {'arti': arti, 'pk':pk})



def mostrarDeshabilitados(request):
    query = Articulo.objects.filter(is_activate=0).order_by('id')
    return  render(request,'productos/articuloDeshabilitado.html', {'inventario': query})

def habilitarArticulo(request, pk):
    arti = Articulo.objects.get(id=pk)
    if request.method == 'POST':
        respuesta = get_object_or_404(Articulo, pk=arti.pk)
        respuesta.is_activate = 1
        respuesta.save()
        messages.success(request, 'Articulo Habilitado')
        return redirect('articulo:articulo')
    return render(request, 'productos/cambiarEstadoModal.html', {'articulo': arti, 'pka': pk})



@api_view(['GET', 'POST'])
def articuloListJSON(request, format=None):
    if request.method == 'GET':
        articulos = Articulo.objects.all()
        serializer = ArticuloSerializer(articulos, many=True)
        datos = json.dumps(serializer.data)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ArticuloSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ArticuloListClass(generics.ListCreateAPIView):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer

