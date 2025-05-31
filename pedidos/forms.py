# formularios para la aplicación de pedidos
from django import forms
from django.core.exceptions import ValidationError
from .models import Pedido


# formulario para crear pedidos
class PedidoForm(forms.ModelForm):
    
    # campo adicional para seleccionar si usar dirección del perfil
    usar_direccion_perfil = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'usar_direccion_perfil'
        }),
        label='Usar dirección de mi perfil'
    )
    
    # campo para guardar la nueva dirección en el perfil
    guardar_direccion_perfil = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'guardar_direccion_perfil'
        }),
        label='Guardar esta dirección en mi perfil para futuras compras'
    )
    
    class Meta:
        model = Pedido
        fields = [
            'nombre_cliente', 'email_cliente', 'telefono_cliente',
            'direccion_envio', 'ciudad_envio', 'codigo_postal_envio',
            'provincia_envio', 'metodo_pago', 'notas'
        ]
        
        # configuración de widgets para el formulario
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo',
                'required': True
            }),
            'email_cliente': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@ejemplo.com',
                'required': True
            }),
            'telefono_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+34 600 000 000',
                'required': True
            }),
            'direccion_envio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa',
                'rows': 3,
                'required': True
            }),
            'ciudad_envio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad',
                'required': True
            }),
            'codigo_postal_envio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '28001',
                'required': True
            }),
            'provincia_envio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Provincia',
                'required': True
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Notas adicionales (opcional)',
                'rows': 3
            }),
        }
        
        # etiquetas personalizadas para los campos
        labels = {
            'nombre_cliente': 'Nombre completo',
            'email_cliente': 'Email',
            'telefono_cliente': 'Teléfono',
            'direccion_envio': 'Dirección de envío',
            'ciudad_envio': 'Ciudad',
            'codigo_postal_envio': 'Código postal',
            'provincia_envio': 'Provincia',
            'metodo_pago': 'Método de pago',
            'notas': 'Notas adicionales',
        }
    
    # validación personalizada para teléfono
    def clean_telefono_cliente(self):
        telefono = self.cleaned_data['telefono_cliente']
        # validación básica del formato del teléfono
        telefono_limpio = telefono.replace(' ', '').replace('-', '').replace('+', '')
        if not telefono_limpio.isdigit() or len(telefono_limpio) < 9:
            raise ValidationError("Introduce un número de teléfono válido")
        return telefono
    
    # validación personalizada para código postal
    def clean_codigo_postal_envio(self):
        codigo_postal = self.cleaned_data['codigo_postal_envio']
        # validación de código postal (5 dígitos)
        if not codigo_postal.isdigit() or len(codigo_postal) != 5:
            raise ValidationError("El código postal debe tener 5 dígitos")
        return codigo_postal
    
    # validación personalizada para email
    def clean_email_cliente(self):
        email = self.cleaned_data['email_cliente']
        # limpieza básica del email
        return email.lower().strip()
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        # si hay usuario y datos del perfil, prellenar campos
        if self.usuario and hasattr(self.usuario, 'perfil'):
            perfil = self.usuario.perfil
            
            # prellenar email y nombre del usuario siempre
            if self.usuario.email:
                self.fields['email_cliente'].initial = self.usuario.email
            if self.usuario.first_name and self.usuario.last_name:
                self.fields['nombre_cliente'].initial = f"{self.usuario.first_name} {self.usuario.last_name}"
            elif self.usuario.first_name:
                self.fields['nombre_cliente'].initial = self.usuario.first_name
            
            # verificar si el perfil tiene dirección completa
            direccion_completa = all([
                perfil.direccion,
                perfil.ciudad,
                perfil.codigo_postal,
                perfil.provincia
            ])
            
            # configurar campos según si hay dirección completa
            if not direccion_completa:
                # no hay dirección completa - ocultar checkbox de usar perfil
                self.fields['usar_direccion_perfil'].widget = forms.HiddenInput()
                self.fields['usar_direccion_perfil'].initial = False
                # mostrar checkbox para guardar nueva dirección
                self.fields['guardar_direccion_perfil'].initial = True
            else:
                # hay dirección completa
                usar_perfil = True
                if self.data:
                    usar_perfil = self.data.get('usar_direccion_perfil') == 'on'
                
                # prellenar con datos del perfil si no hay POST data o si se marcó usar perfil
                if not self.data or usar_perfil:
                    self.fields['direccion_envio'].initial = perfil.direccion
                    self.fields['ciudad_envio'].initial = perfil.ciudad
                    self.fields['codigo_postal_envio'].initial = perfil.codigo_postal
                    self.fields['provincia_envio'].initial = perfil.provincia
                    if perfil.telefono:
                        self.fields['telefono_cliente'].initial = perfil.telefono
                
                # configurar checkbox de guardar según si está usando perfil
                if usar_perfil:
                    # si usa dirección del perfil, ocultar checkbox de guardar
                    self.fields['guardar_direccion_perfil'].widget = forms.HiddenInput()
                    self.fields['guardar_direccion_perfil'].initial = False
                else:
                    # si no usa dirección del perfil, mostrar opción de guardar
                    self.fields['guardar_direccion_perfil'].initial = True
        else:
            # no hay perfil - ocultar checkbox de usar perfil
            self.fields['usar_direccion_perfil'].widget = forms.HiddenInput()
            self.fields['usar_direccion_perfil'].initial = False
            # mostrar checkbox para guardar (aunque no se usará sin perfil)
            self.fields['guardar_direccion_perfil'].widget = forms.HiddenInput()
            self.fields['guardar_direccion_perfil'].initial = False
    
    def save(self, commit=True):
        pedido = super().save(commit=False)
        
        # si hay usuario y se marcó guardar dirección
        if (self.usuario and hasattr(self.usuario, 'perfil') and 
            self.cleaned_data.get('guardar_direccion_perfil', False)):
            
            perfil = self.usuario.perfil
            perfil.direccion = self.cleaned_data['direccion_envio']
            perfil.ciudad = self.cleaned_data['ciudad_envio']
            perfil.codigo_postal = self.cleaned_data['codigo_postal_envio']
            perfil.provincia = self.cleaned_data['provincia_envio']
            if self.cleaned_data.get('telefono_cliente'):
                perfil.telefono = self.cleaned_data['telefono_cliente']
            perfil.save()
        
        if commit:
            pedido.save()
        
        return pedido
