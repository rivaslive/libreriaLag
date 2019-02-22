from rest_framework import serializers

from apps.articulos.models import Articulo, Categoria

class ArticuloSerializer(serializers.ModelSerializer):
    id_categoria = serializers.StringRelatedField()
    class Meta:
        model = Articulo
        fields = ('nombre_articulo', 'codigo_articulo', 'stock', 'precio_unidad', 'is_activate', 'id_categoria')