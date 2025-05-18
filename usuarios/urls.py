from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.RegistroUsuarioView.as_view(), name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/editar/', views.editar_perfil_view, name='editar_perfil'),
]