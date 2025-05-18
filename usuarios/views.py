from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Perfil

#Vista para registro de usuarios
class RegistroUsuarioView(CreateView):
    template_name = 'usuarios/registro.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
        return response

#Vista para inicio de sesion de usuarios
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido, {username}!')
                return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

#Vista para cerrar sesion
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('home')

#Vista para ver el perfil de usuario
@login_required
def perfil_view(request):
    perfil = request.user.perfil
    return render(request, 'usuarios/perfil.html', {'perfil': perfil})

#Vista para editar perfil de usuario EN DESARROLLO
@login_required
def editar_perfil_view(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        messages.success(request, 'Perfil actualizado correctamente')
        return redirect('perfil')
    return render(request, 'usuarios/editar_perfil.html', {'perfil': perfil})
