from django.shortcuts import render

# Create your views here.
def articulo(request):
    return render(request, 'productos/articulo.html')
def inventario(request):
    return render(request, 'productos/inventario.html')