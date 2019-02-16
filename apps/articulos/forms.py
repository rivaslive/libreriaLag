from django import forms

from apps.articulos.models import Articulo


class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['nombre_articulo', 'codigo_articulo', 'stock', 'precio_unidad', 'id_categoria', 'is_activate']

    def __init__(self, *args, **kwargs):
        super(ArticuloForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })