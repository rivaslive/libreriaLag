from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre_Categoria = models.CharField(max_length=45, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.nombre_Categoria)


class Articulo(models.Model):
    nombre_articulo = models.CharField(max_length=45, null=False, blank=False)
    codigo_articulo = models.CharField(max_length=45, null=False, blank=False)
    stock = models.IntegerField(null=True, blank=True)
    precio_unidad = models.DecimalField(max_digits=5,decimal_places=2,null=False, blank=False)
    is_activate = models.IntegerField(null=False, blank=False)
    id_categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, null=False, blank=False)
"""
    def __str__(self):
        return '{} {}'.format(self.nombre_articulo, self.codigo_articulo, float(self.precio_unidad))
"""