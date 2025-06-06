from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .models import Perfil
from .forms import RegistroUsuarioForm, EmailAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm, PerfilForm

#Vista para registro de usuarios
class RegistroUsuarioView(CreateView):
    template_name = 'usuarios/registro.html'
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cuenta creada exitosamente. Ahora puedes iniciar sesión con tu email o nombre de usuario.')
        return response

#Vista para inicio de sesion de usuarios usuario y email
def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Mostrar email si esta disponible, sino nombre de usuario
                display_name = user.email if user.email else user.username
                
                # Manejar redirección  
                next_url = request.GET.get('next') or request.POST.get('next')
                
                # Verificar si el usuario es administrador y redirigir al admin
                if user.is_staff or user.is_superuser:
                    messages.success(request, f'Bienvenido al panel de administración, {display_name}!')
                    return redirect('/admin/')
                else:
                    messages.success(request, f'Bienvenido, {display_name}!')
                    # Usar next_url si existe, sino ir a home
                    if next_url:
                        return redirect(next_url)
                    return redirect('home')
        else:
            messages.error(request, 'Email/usuario o contraseña incorrectos')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

#Vista para cerrar sesion
def logout_view(request):
    # Verificar si viene del admin
    viene_del_admin = request.META.get('HTTP_REFERER', '').endswith('/admin/') or '/admin/' in request.META.get('HTTP_REFERER', '')
    
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    
    # Si viene del admin y tiene nextparameter, redirigir ahí
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    elif viene_del_admin:
        return redirect('login')
    else:
        return redirect('home')

#Vista para ver el perfil de usuario
@login_required
def perfil_view(request):
    perfil = request.user.perfil
    return render(request, 'usuarios/perfil_unificado.html', {
        'perfil': perfil,
        'modo_edicion': False
    })

#Vista para editar perfil de usuario
@login_required
def editar_perfil_view(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil, user=request.user)
        if form.is_valid():
            # Actualizar datos del usuario
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            # Guardar el perfil
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil, user=request.user)
    
    return render(request, 'usuarios/perfil_unificado.html', {
        'form': form,
        'modo_edicion': True
    })
