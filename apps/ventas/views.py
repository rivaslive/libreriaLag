from datetime import datetime
from unicodedata import decimal

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.


from apps.articulos.forms import ArticuloForm
from apps.articulos.models import Articulo
from apps.ventas.forms import VentaForm, DetalleForm
from apps.ventas.models import detalle, Venta

def prueba(request):
    return render(request, 'base/admin.html')

def addCar(request, pk):
    cantidad = request.GET.get('cantidad', '')
    articulo = Articulo.objects.get(id=pk)
    if request.session['ventaId'] == '':
        dateNow = datetime.now()
        print(dateNow)
        if cantidad:
            if int(cantidad) <= articulo.stock:
                print('estamos aqui')
                form = VentaForm({'fecha_venta': dateNow, 'estado': 1})
                if form.is_valid():
                    obtener = form.save(commit=False)
                    obtener.save()
                    print('su id de venta es ', obtener.pk)
                    request.session['ventaId'] = obtener.pk
                    subTotal = float(int(cantidad) * articulo.precio_unidad)
                    print('correcto')
                    form2 = DetalleForm(
                        {'cantidad': cantidad, 'precio': articulo.precio_unidad, 'sub_total': subTotal, 'id_articulo': pk,
                         'id_venta': request.session['ventaId']})
                    if form2.is_valid():
                        form2.save()
                        form3 = get_object_or_404(Articulo, pk=articulo.pk)
                        form3.stock = (articulo.stock - int(cantidad))
                        form3.save()
                        messages.success(request, 'Operacion Exitosa')
                        return redirect('articulo:articulo')
                return render(request, 'ventas/addCar.html', {'pk': pk})
            else:
                messages.warning(request, 'No hay suficientes existencias')
                return redirect('articulo:articulo')
        else:
            return render(request, 'ventas/addCar.html', {'pk': pk})
    else:
        print('estamos aqui 2', request.session['ventaId'])
        if cantidad:
            if int(cantidad) <= articulo.stock:
                ventaId = request.session['ventaId']
                subTotal = float(int(cantidad) * articulo.precio_unidad)
                form2 = DetalleForm(
                    {'cantidad': cantidad, 'precio': articulo.precio_unidad, 'sub_total': subTotal, 'id_articulo': pk,
                     'id_venta': ventaId})
                if form2.is_valid():
                    form2.save()
                    #Editar el registro ya existe de articulo para restar el stock
                    form3 = get_object_or_404(Articulo, pk=articulo.pk)
                    form3.stock = (articulo.stock - int(cantidad))
                    form3.save()
                    messages.success(request, 'Operacion Exitosa')
                    return redirect('articulo:articulo')
                return render(request, 'ventas/addCar.html', {'pk': pk})
            else:
                messages.warning(request, 'No hay suficientes existencias')
                return redirect('articulo:articulo')
        else:
            return render(request, 'ventas/addCar.html', {'pk': pk})


def carShopping(request):
    ventaId = request.session['ventaId']
    if ventaId:
        query = detalle.objects.filter(id_venta=ventaId)
        if query:
            total = 0
            for foo in query:
                total += (foo.cantidad * foo.id_articulo.precio_unidad)
        else:
            total = 0
        print('ventaId 0', query)
        return render(request, 'ventas/carShopping.html', {'query': query, 'total': total})
    else:
        return render(request, 'ventas/carShopping.html')

def shop(request):
    return render(request, 'ventas/shop.html')
