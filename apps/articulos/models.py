from django.db import models

# Create your models here.
class Categoria(models.Model):
    #id_categoria = models.AutoField(primary_key=True)
    nombre_Categoria = models.CharField(max_length=45, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.nombre_Categoria)

class Presentacion(models.Model):
    #id_presentacion = models.AutoField(primary_key=True)
    nombre_presentacion = models.CharField(
        max_length=45, null=False, blank=False)
    def __str__(self):
        return '{}'.format(self.nombre_presentacion)

class Articulo(models.Model):
    #id_articulo = models.AutoField(primary_key=True)
    nombre_articulo = models.CharField(max_length=45, null=False, blank=False)
    codigo_articulo = models.CharField(max_length=45, null=False, blank=False)
    stock_caja = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    #precio_unidad = models.DecimalField(decimal_places=3,null=False, blank=False)
    is_activate = models.IntegerField(null=False, blank=False)
    id_categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, null=False, blank=False)
    id_presentacion = models.ForeignKey(
        Presentacion, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return '{} {}'.format(self.nombre_articulo, self.codigo_articulo)