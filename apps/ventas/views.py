from datetime import datetime
from unicodedata import decimal

from django.contrib import messages
from django.db.models import Q, Sum
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.


from apps.articulos.forms import ArticuloForm
from apps.articulos.models import Articulo
from apps.ventas.forms import VentaForm, DetalleForm, FacturaForm
from apps.ventas.models import detalle, Venta, Factura


def prueba(request):
    return render(request, 'base/admin.html')


def addCar(request, pk):
    cantidad = request.POST.get('cantidad', '')
    if request.session['ventaId'] == '':
        dateNow = datetime.now()
        print(dateNow)
        if cantidad:
            articulo = Articulo.objects.get(id=pk)
            codigo = articulo.codigo_articulo
            try:
                articulo = Articulo.objects.get(codigo_articulo=codigo)
            except:
                messages.warning(request, '01 No existe el codigo de registro: ' + request.GET.get('codigo', ''))
                return redirect('ventas:shop')
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
                        return redirect('articulo:articulo')
                else:
                    messages.warning(request, 'Error en registro')
                    return redirect('articulo:articulo')
            else:
                messages.warning(request, 'No hay suficientes existencias')
                return redirect('articulo:articulo')
        else:
            return render(request, 'ventas/addCar.html', {'pk': pk})
    else:
        print('estamos aqui 2', request.session['ventaId'])
        if cantidad:
            articulo = Articulo.objects.get(id=pk)
            codigo = articulo.codigo_articulo
            try:
                articulo = Articulo.objects.get(codigo_articulo=codigo)
            except:
                messages.warning(request, '01 No existe el codigo de registro: ' + request.GET.get('codigo', ''))
                return redirect('ventas:shop')
            if int(cantidad) <= articulo.stock:
                ventaId = request.session['ventaId']
                try:
                    existens = detalle.objects.filter(Q(id_venta=ventaId) & Q(id_articulo__codigo_articulo=codigo))
                    if existens:
                        evaluador = 1
                        print('estamos aqui 3')
                    else:
                        evaluador = 0
                    print("Evaluador: " + str(evaluador))
                except:
                    evaluador = 0
                if evaluador == 0:
                    subTotal = float(int(cantidad) * articulo.precio_unidad)
                    form2 = DetalleForm(
                        {
                            'cantidad': cantidad,
                            'precio': articulo.precio_unidad,
                            'sub_total': subTotal,
                            'id_articulo': articulo.pk,
                            'id_venta': ventaId
                        }
                    )
                    if form2.is_valid():
                        form2.save()
                        # Editar el registro ya existe de articulo para restar el stock
                        form3 = get_object_or_404(Articulo, pk=articulo.pk)
                        form3.stock = (articulo.stock - int(cantidad))
                        form3.save()
                        messages.success(request, 'Operacion Exitosa')
                        return redirect('articulo:articulo')
                    else:
                        messages.warning(request, 'Formulario no valido')
                        return redirect('articulo:articulo')
                else:
                    print('estamos aqui 4')
                    subTotal = float(int(cantidad) * articulo.precio_unidad)
                    detal = detalle.objects.get(Q(id_venta=ventaId) & Q(id_articulo__codigo_articulo=codigo))
                    print(detal.pk)
                    print("Paso AQUI")
                    post = get_object_or_404(detalle, pk=detal.pk)
                    post.cantidad = (detal.cantidad + int(cantidad))
                    post.sub_total = (float(detal.sub_total) + subTotal)
                    post.save()
                    # Editar el registro ya existe de articulo para restar el stock
                    form3 = get_object_or_404(Articulo, pk=articulo.pk)
                    form3.stock = (articulo.stock - int(cantidad))
                    form3.save()
                    messages.success(request, 'Operacion Exitosa')
                    return redirect('articulo:articulo')

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
    try:
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
            request.session['ventaId'] = ""
            return render(request, 'ventas/shop.html')
    except:
        request.session['ventaId'] = ""
        return render(request, 'ventas/shop.html')


def venta(request):
    presentacion = int(request.POST.get('id_presentacion', ''))
    cantidad = request.POST.get('cantidad', '')
    codigo = request.POST.get('codigo', '')
    try:
        articulo = Articulo.objects.get(codigo_articulo=codigo)
    except:
        messages.warning(request, '01 No existe el codigo de registro: ' + request.GET.get('codigo', ''))
        return redirect('ventas:shop')
    if request.session['ventaId'] == '':
        dateNow = datetime.now()
        print(dateNow)
        if presentacion == 1:
            print("PRESENTACION EN UNIDADES")
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
            print("PRESENTACION EN CAJAS")
            if cantidad:
                if int(cantidad) <= articulo.stock:
                    print('estamos aqui')
                    form = VentaForm({'fecha_venta': dateNow, 'estado': 1})
                    if form.is_valid():
                        obtener = form.save(commit=False)
                        obtener.save()
                        print('su id de venta es ', obtener.pk)
                        request.session['ventaId'] = obtener.pk
                        subTotal = float(int(cantidad) * articulo.precio_caja)
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
        print('VENTA EXISTENTE ID NUMERO ', request.session['ventaId'])
        if presentacion == 1:
            if cantidad:
                if int(cantidad) <= articulo.stock:
                    ventaId = request.session['ventaId']
                    try:
                        existens = detalle.objects.filter(Q(id_venta=ventaId) & Q(id_articulo__codigo_articulo=codigo))
                        if existens:
                            evaluador = 1
                            print('estamos aqui 3')
                        else:
                            evaluador = 0
                        print("Evaluador: " + str(evaluador))
                    except:
                        evaluador = 0
                    if evaluador == 0:
                        subTotal = float(int(cantidad) * articulo.precio_unidad)
                        form2 = DetalleForm(
                            {
                                'cantidad': cantidad,
                                'precio': articulo.precio_unidad,
                                'sub_total': subTotal,
                                'id_articulo': articulo.pk,
                                'id_venta': ventaId
                            }
                        )
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
                        print('estamos aqui 4')
                        subTotal = float(int(cantidad) * articulo.precio_unidad)
                        detal = detalle.objects.get(Q(id_venta=ventaId) & Q(id_articulo__codigo_articulo=codigo))
                        print(detal.pk)
                        print("Paso AQUI")
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
        else:
            if cantidad:
                if int(cantidad) <= articulo.stock:
                    ventaId = request.session['ventaId']
                    try:
                        existens = detalle.objects.filter(Q(id_venta=ventaId) & Q(id_articulo__codigo_articulo=codigo))
                        if existens:
                            evaluador = 1
                            print('estamos aqui 3')
                        else:
                            evaluador = 0
                        print("Evaluador: " + str(evaluador))
                    except:
                        evaluador = 0
                    if evaluador == 0:
                        cantidad = int(cantidad) * articulo.stock
                        subTotal = float(int(cantidad) * articulo.precio_caja)
                        form2 = DetalleForm(
                            {
                                'cantidad': cantidad,
                                'precio': articulo.precio_unidad,
                                'sub_total': subTotal,
                                'id_articulo': articulo.pk,
                                'id_venta': ventaId
                            }
                        )
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
                        print('estamos aqui 4')
                        subTotal = float(int(cantidad) * articulo.precio_unidad)
                        detal = detalle.objects.get(Q(id_venta=ventaId) & Q(id_articulo__codigo_articulo=codigo))
                        print(detal.pk)
                        print("Paso AQUI")
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
    pk2 = detalles.id_articulo.pk
    cantidad = detalles.cantidad
    if detalles:
        detalles.delete()
        articulos = Articulo.objects.get(id=pk2)
        if articulos:
            form3 = get_object_or_404(Articulo, pk=pk2)
            form3.stock += cantidad
            form3.save()
            messages.success(request, 'Registro Eliminado correctamente, se agrego ' + str(
                cantidad) + " Unid a " + articulos.nombre_articulo)
            return redirect('ventas:shop')
        else:
            messages.warning(request, 'Error al sumar el STOCK')
            return redirect('ventas:shop')
    else:
        messages.warning(request, 'Error al eliminar detalle')
        return redirect('ventas:shop')


def vender(request):
    ventaId = request.session['ventaId']
    if ventaId != "":
        if request.method == "POST":
            try:
                facturas = Factura.objects.latest('id')
            except:
                print("estamos en 1")
                facturas = ""
            if facturas != "":
                print("estamos en 2")
                detalles = detalle.objects.filter(id_venta=ventaId)
                if detalles:
                    total = 0
                    for foo in detalles:
                        total += (foo.cantidad * foo.id_articulo.precio_unidad)
                else:
                    total = 0
                efectivo = float(request.POST.get('cambio', ''))
                if efectivo >= total:
                    print("estamos en 3")
                    cambio = (efectivo - float(total))
                    numero = (facturas.numero + 1)
                    ventas = Venta.objects.get(id=ventaId)
                    print(ventas)
                    form = FacturaForm({'venta': ventaId, 'total': total, 'cambio': cambio, 'fecha': ventas.fecha_venta,
                                        'numero': numero, 'efectivo': efectivo})
                    print("paso error")
                    if form.is_valid():
                        print("estamos en 4")
                        form.save()

                        if ventas:
                            print("estamos en 5")
                            form = get_object_or_404(Venta, pk=ventas.pk)
                            form.estado = 0
                            form.save()
                            messages.success(request, "Venta exitosa")
                            return redirect('ventas:ticket')
                        else:
                            messages.warning(request, "No se pudo finalizar la venta")
                            return redirect('ventas:shop')
                    else:
                        messages.warning(request, "No se pudo crear el Ticket")
                        return redirect('ventas:shop')
                else:
                    messages.warning(request, "Ingrese un monto MAYOR al total")
                    return redirect('ventas:shop')
            else:
                print("estamos en 6")
                efectivo = float(request.POST.get('cambio', ''))
                detalles = detalle.objects.filter(id_venta=ventaId)
                if detalles:
                    total = 0
                    for foo in detalles:
                        total += (foo.cantidad * foo.id_articulo.precio_unidad)
                else:
                    total = 0
                if efectivo >= total:
                    print("estamos en 7")
                    cambio = (efectivo - float(total))
                    print(cambio)
                    numero = 1
                    ventas = Venta.objects.get(id=ventaId)
                    form = FacturaForm(
                        {'venta': ventaId, 'total': total, 'cambio': float(cambio), 'fecha': ventas.fecha_venta,
                         'numero': numero, 'efectivo': efectivo})
                    if form.is_valid():
                        print("estamos en 8")
                        form.save()
                        if ventas:
                            print("estamos en 9")
                            form = get_object_or_404(Venta, pk=ventas.pk)
                            form.estado = 0
                            form.save()
                            print("exito")
                            messages.success(request, "Operacion exitosa")
                            return redirect('ventas:ticket')
                        else:
                            messages.warning(request, "No se pudo finalizar la venta")
                            return redirect('ventas:shop')
                    else:
                        print('error')
                        messages.warning(request, "No se pudo crear el Ticket")
                        return redirect('ventas:shop')
                else:
                    messages.warning(request, "Ingrese un monto MAYOR al total")
                    return redirect('ventas:shop')
        else:
            messages.warning(request, "error metodo POST")
            return redirect('ventas:shop')
    else:
        messages.warning(request, "No existe ninguna venta activa")
        return redirect('ventas:shop')


def ticket(request):
    ventaId = request.session['ventaId']
    try:
        facturas = Factura.objects.get(venta_id=ventaId)
        print(facturas)
        detalles = detalle.objects.filter(id_venta=ventaId)
        request.session['ventaId'] = ""
        return render(request, 'ventas/ticket.html', {'detalle': detalles, 'factura': facturas})
    except:
        return render(request, 'ventas/ticket.html')


# Elimina la venta actual
def drop(request):
    ventaId = request.session['ventaId']

    if ventaId:
        try:
            venta = Venta.objects.get(id=ventaId)
            detalles = detalle.objects.filter(id_venta=ventaId)

        except:
            messages.warning(request, "error en ID de venta")
            return redirect('ventas:shop')

        for d in detalles:
            idArt = d.id_articulo.pk
            cantidad = d.cantidad
            form = get_object_or_404(Articulo, pk=idArt)
            form.stock += cantidad
            form.save()
            d.delete()
            print("Paso TODO")
        if venta:
            venta.delete()
            request.session['ventaId'] = ""
            messages.success(request, "Venta eliminada con exito")
            return redirect('ventas:shop')
        else:
            messages.warning(request, "error en eliminar venta")
            return redirect('ventas:shop')
    else:
        messages.warning(request, "no existe ninguna venta")
        return redirect('ventas:shop')


def editarShop(request, pk):
    detalles = detalle.objects.get(id=pk)
    if request.method == "GET":
        form = detalles
    else:
        cantidad = request.POST.get('cantidad', '')
        codigo = int(request.POST.get('codigo', ''))
        articulo = Articulo.objects.get(codigo_articulo=codigo)
        if int(cantidad) <= articulo.stock:
            try:
                form = get_object_or_404(Articulo, pk=articulo.pk)
                form.stock = articulo.stock + (detalles.cantidad - int(cantidad))
                form.save()
            except:
                messages.warning(request, "error al cargar stock")
                return redirect('ventas:shop')
            try:
                form = get_object_or_404(detalle, pk=detalles.pk)
                form.cantidad = int(cantidad)
                form.save()
                messages.success(request, "Operacion exitosa se sumaron " + str(cantidad) + " al stock")
                return redirect('ventas:shop')
            except:
                messages.warning(request, "error al cargar nueva cantidad")
                return redirect('ventas:shop')


        else:
            messages.warning(request, "No hay suficiente stock")
            return redirect('ventas:shop')
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
        return render(request, 'ventas/shop.html', {'form':form, 'query': query, 'total': total})
    else:
        request.session['ventaId'] = ""
        return render(request, 'ventas/shop.html', {'form':form})

def listarVentas(request):
    return render(request,'ventas/listVentas.html')

def llenarTablaVentas(request):
    query = Factura.objects.all().exclude(venta__estado=1)
    suma = Factura.objects.all().aggregate(Sum('total'))
    return render(request, 'ventas/listVentas.html', {'datosVenta': query, 'sumaTotal':suma})