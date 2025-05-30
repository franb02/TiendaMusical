# Importamos las librerias necesarias para crear formularios personalizados ya que las necestiamos para poner el email
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Perfil


# Formulario personalizado para registro de usuarios
class RegistroUsuarioForm(UserCreationForm):
    # Campo email personalizado - obligatorio a diferencia del modelo base
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        }),
        help_text='Ingresa una dirección de email válida.'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        # Widgets personalizados para aplicar estilos Bootstrap
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
        }
    
    # Constructor personalizado para añadir estilos a campos heredados
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases CSS a los campos de contraseña
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })
    
    # Valida que el email no este registrado
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Ya existe un usuario con este email.')
        return email
    
    # Guarda el usuario con el email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# Formulario de autenticación que permite login con email o usuario
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Email o nombre de usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com o nombre de usuario'
        })
    )
    
    # Aplicamos estilos al campo password
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })


# Formulario personalizado para recuperación de contraseña descativado
class CustomPasswordResetForm(PasswordResetForm):
    # Campo email con estilos personalizados
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        }),
        help_text='Ingresa el email asociado a tu cuenta.'
    )


# Formulario para establecer nueva contraseña después del reset
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nueva contraseña',
            'autocomplete': 'new-password'  
        }),
        strip=False,
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar nueva contraseña',
            'autocomplete': 'new-password'
        }),
        strip=False,
    )


# Formulario  para editar el perfil del usuario

class PerfilForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nombre',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        label='Apellidos',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tus apellidos'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        })
    )
    
    class Meta:
        model = Perfil
        fields = ['telefono', 'direccion', 'ciudad', 'codigo_postal', 'provincia', 'foto']
        # Widgets personalizados para cada campo del perfil
        widgets = {
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+34 123 456 789'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Calle, número, piso...'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Madrid'
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '28001'
            }),
            'provincia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Madrid'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        # Etiquetas personalizadas para los campos
        labels = {
            'telefono': 'Teléfono',
            'direccion': 'Dirección completa',
            'ciudad': 'Ciudad',
            'codigo_postal': 'Código postal',
            'provincia': 'Provincia',
            'foto': 'Foto de perfil'
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extraemos el usuario de los kwargs
        super().__init__(*args, **kwargs)
        
        # Si tenemos un usuario, rellenamos los campos con sus datos 
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
    
    # Validación del email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Obtenemos el usuario actual si existe
        user = self.instance.user if hasattr(self.instance, 'user') else None
        
        if User.objects.filter(email=email).exclude(pk=user.pk if user else None).exists():
            raise ValidationError('Ya existe un usuario con este email.')
        return email
