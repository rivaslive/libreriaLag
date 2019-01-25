from django import forms

from apps.ventas.models import Venta


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['fecha_venta', 'estado']
    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })