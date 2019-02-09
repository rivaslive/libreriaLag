from datetime import datetime
from unicodedata import decimal

from django.contrib import messages
from django.db.models import Q
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
        return render(request, 'ventas/shop.html', {'query': query, 'total': total})
    else:
        return render(request, 'ventas/shop.html')

def venta(request):
    cantidad = request.GET.get('cantidad', '')
    codigo = request.GET.get('codigo', '')
    try:
        articulo = Articulo.objects.get(codigo_articulo=codigo)
    except:
        messages.warning(request, 'No existe el codigo de registro: ' + request.GET.get('codigo', ''))
        return redirect('ventas:shop')
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
                        {'cantidad': cantidad, 'precio': articulo.precio_unidad, 'sub_total': subTotal,
                         'id_articulo': articulo.pk,
                         'id_venta': request.session['ventaId']})
                    if form2.is_valid():
                        form2.save()
                        form3 = get_object_or_404(Articulo, pk=articulo.pk)
                        form3.stock = (articulo.stock - int(cantidad))
                        form3.save()
                        messages.success(request, 'Operacion Exitosa')
                        return redirect('ventas:venta')
                else:
                    messages.warning(request, 'Error en registro')
                    return redirect('ventas:shop')
            else:
                messages.warning(request, 'No hay suficientes existencias')
                return redirect('ventas:shop')
        else:
            messages.warning(request, 'Ingrese una cantidad')
            return redirect('ventas:shop')
    else:
        print('estamos aqui 2', request.session['ventaId'])
        if cantidad:
            if int(cantidad) <= articulo.stock:
                try:
                    existens=detalle.objects.filter(id_articulo__codigo_articulo=codigo)
                    if existens:
                        evaluador=1
                    else:
                        evaluador = 0
                    print("Evaluador: " + str(evaluador))
                except:
                    evaluador=0
                if evaluador == 0:
                    ventaId = request.session['ventaId']
                    subTotal = float(int(cantidad) * articulo.precio_unidad)
                    form2 = DetalleForm(
                        {'cantidad': cantidad, 'precio': articulo.precio_unidad, 'sub_total': subTotal,
                         'id_articulo': articulo.pk,
                         'id_venta': ventaId})
                    if form2.is_valid():
                        form2.save()
                        # Editar el registro ya existe de articulo para restar el stock
                        form3 = get_object_or_404(Articulo, pk=articulo.pk)
                        form3.stock = (articulo.stock - int(cantidad))
                        form3.save()
                        messages.success(request, 'Operacion Exitosa')
                        return redirect('ventas:venta')
                    else:
                        messages.warning(request, 'Formulario no valido')
                        return redirect('ventas:shop')
                else:
                    ventaId = request.session['ventaId']
                    subTotal = float(int(cantidad) * articulo.precio_unidad)

                    detal = detalle.objects.get(Q(id_venta=ventaId) & Q(id_articulo__codigo_articulo=articulo.codigo_articulo))
                    print(detal.pk)
                    post = get_object_or_404(detalle, pk=detal.pk)
                    post.cantidad = (detal.cantidad + int(cantidad))
                    post.sub_total = (float(detal.sub_total) + subTotal)
                    post.save()
                    # Editar el registro ya existe de articulo para restar el stock
                    form3 = get_object_or_404(Articulo, pk=articulo.pk)
                    form3.stock = (articulo.stock - int(cantidad))
                    form3.save()
                    messages.success(request, 'Operacion Exitosa')
                    return redirect('ventas:venta')

            else:
                messages.warning(request, 'No hay suficientes existencias')
                return redirect('ventas:shop')
        else:
            messages.warning(request, 'Ingrese una Cantidad')
            return redirect('ventas:shop')



def eliminarDetalle(request, pk):
    detalles = detalle.objects.get(id=pk)
    pk2=detalles.id_articulo.pk
    cantidad = detalles.cantidad
    if request.method == "POST":
        detalles.delete()
        articulos=Articulo.objects.get(id=pk2)
        if articulos:
            form3 = get_object_or_404(Articulo, pk=pk2)
            form3.stock += cantidad
            form3.save()
            messages.success(request, 'Registro Eliminado correctamente, se agrego '+ str(cantidad) + " Unid a " + articulos.nombre_articulo)
            return redirect('ventas:shop')
        else:
            messages.warning(request, 'Error al sumar el STOCK')
            return redirect('ventas:shop')
    else:
        return render(request, 'ventas/deleteDetalleModal.html', {'pk':pk})



