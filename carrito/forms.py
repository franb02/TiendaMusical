from django import forms
from django.core.exceptions import ValidationError
from productos.models import Instrumento

# Formulario para agregar productos al carrito
class CarritoAgregarProductoForm(forms.Form):    
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '99',
            'step': '1'
        })
    )
    actualizar = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
    
    def __init__(self, *args, **kwargs):
        self.instrumento = kwargs.pop('instrumento', None)
        super().__init__(*args, **kwargs)
        
        if self.instrumento:
            self.fields['cantidad'].widget.attrs['max'] = str(self.instrumento.stock)
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        
        if self.instrumento and cantidad > self.instrumento.stock:
            raise ValidationError(
                f'Solo hay {self.instrumento.stock} unidades disponibles'
            )
        
        return cantidad
