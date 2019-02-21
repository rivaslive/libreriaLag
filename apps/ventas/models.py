from django.db import models
from apps.articulos.models import Articulo

# Create your models here.
class Venta(models.Model):
    fecha_venta = models.DateField(null=False, blank=False)
    estado = models.IntegerField(null=False, blank=False)
    def __str__(self):
        return '{}'.format(self.fecha_venta)

class detalle(models.Model):
    cantidad = models.IntegerField(null=False, blank=False)
    precio = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    descuento = models.DecimalField(default=0, max_digits=5, decimal_places=2, null=True, blank=True)
    sub_total = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    id_articulo = models.ForeignKey(
        Articulo, on_delete=models.CASCADE, null=False, blank=False)
    id_venta = models.ForeignKey(
        Venta, on_delete=models.CASCADE, null=False, blank=False)

class Factura(models.Model):
    venta = models.OneToOneField(Venta, null=False, blank=False, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    cambio = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    fecha = models.DateTimeField(null=False, blank=False)
    numero = models.IntegerField(default=00000000, null=False, blank=False)
    efectivo = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    descuentoTotal = models.DecimalField(default=0, max_digits=5, decimal_places=2, null=True, blank=True)
