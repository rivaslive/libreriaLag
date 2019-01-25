from datetime import datetime

from django.shortcuts import render, redirect

# Create your views here.
from apps.ventas.forms import VentaForm


def prueba(request):
    return render(request, 'base/admin.html')

def addCar(request, pk):
    if request.session['ventaId'] == '':
        cantidad = request.GET.get('cantidad', '')
        dateNow = datetime.now()
        print(dateNow)
        form = VentaForm({'fecha_venta':dateNow, 'estado':1})
        if form.is_valid():
            form.save()
            print(form.pk)
            return redirect('articulo:articulo')
        return render(request, 'productos/inventario.html')
