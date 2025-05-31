from django.contrib import admin
from django.utils.html import format_html
from .models import Carrito, ItemCarrito

# Clase para mostrar items del carrito dentro del admin de Carrito
class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0
    readonly_fields = ('fecha_agregado', 'fecha_actualizacion', 'get_total_precio_formatted')
    fields = ('instrumento', 'cantidad', 'get_total_precio_formatted', 'fecha_agregado', 'fecha_actualizacion')
    
    def get_total_precio_formatted(self, obj):
        if obj.id:
            return f"€{obj.get_total_precio():.2f}"
        return "-"
    get_total_precio_formatted.short_description = 'Precio Total'


# Administrador del modelo Carrito 
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'session_key', 'get_total_items', 'get_total', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('fecha_creacion', 'fecha_actualizacion')
    search_fields = ('usuario__username', 'usuario__email', 'session_key')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    inlines = [ItemCarritoInline]
    ordering = ('-fecha_actualizacion',)  # Ordenar por última actualización
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'
    
    def get_total(self, obj):
        return f"€{obj.get_total():.2f}"
    get_total.short_description = 'Total'
    
    # Acción personalizada para limpiar carritos
    actions = ['limpiar_carritos']
    
    def limpiar_carritos(self, request, queryset):
        for carrito in queryset:
            carrito.limpiar()
        self.message_user(request, f'Se limpiaron {queryset.count()} carritos.')
    limpiar_carritos.short_description = 'Limpiar carritos seleccionados'


# Administrador del modelo ItemCarrito para gestión individual de items
@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'instrumento', 'cantidad', 'get_total_precio', 'fecha_agregado')
    list_filter = ('fecha_agregado', 'fecha_actualizacion', 'instrumento__categoria')
    search_fields = ('carrito__usuario__username', 'instrumento__nombre')
    readonly_fields = ('fecha_agregado', 'fecha_actualizacion')
    ordering = ('-fecha_agregado',)
    
    def get_total_precio(self, obj):
        return f"€{obj.get_total_precio():.2f}"
    get_total_precio.short_description = 'Precio Total'