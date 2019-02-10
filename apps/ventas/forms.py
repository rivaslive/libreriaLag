from django import forms

from apps.ventas.models import Venta, detalle, Factura


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

class DetalleForm(forms.ModelForm):
    class Meta:
        model = detalle
        fields = ['cantidad','precio','sub_total','id_articulo','id_venta']
    def __init__(self, *args, **kwargs):
        super(DetalleForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = [
            'venta',
            'total',
            'cambio',
            'fecha',
            'numero',
            'efectivo'
        ]