from django.contrib import admin
from .models import Perfil
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Personalización del admin
admin.site.site_header = " Sonora Panel de Administración"
admin.site.site_title = "Admin Sonora"
admin.site.index_title = "Bienvenido al Panel de Administración"

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'

class CustomUserAdmin(UserAdmin):
    inlines = (PerfilInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = UserAdmin.list_filter + ('perfil__ciudad',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ()}),
    )

# Re-registramos el modelo User con nuestro CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
