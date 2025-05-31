from django.contrib import admin
from .models import Pedido, ItemPedido


# Clase inline para mostrar los items del pedido dentro del admin de Pedido
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('precio_total',)
    
    # Desactivar la capacidad de agregar nuevos items desde el inline
    def has_add_permission(self, request, obj=None):
        return False


# Configuración del admin para el modelo Pedido
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    
    list_display = [
        'numero_pedido',
        'nombre_cliente', 
        'email_cliente',
        'estado',
        'metodo_pago',
        'total',
        'fecha_creacion'
    ]
    
    list_filter = [
        'estado',
        'metodo_pago',
        'fecha_creacion',
        'provincia_envio'
    ]
    
    search_fields = [
        'numero_pedido',
        'nombre_cliente',
        'email_cliente',
        'telefono_cliente'
    ]
    
    readonly_fields = [
        'numero_pedido',
        'fecha_creacion',
        'fecha_actualizacion',
        'subtotal',
        'total'
    ]
    
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('numero_pedido', 'estado', 'fecha_creacion', 'fecha_actualizacion')
        }),
        ('Datos del Cliente', {
            'fields': ('usuario', 'nombre_cliente', 'email_cliente', 'telefono_cliente')
        }),
        ('Dirección de Envío', {
            'fields': ('direccion_envio', 'ciudad_envio', 'codigo_postal_envio', 'provincia_envio')
        }),
        ('Pago y Total', {
            'fields': ('metodo_pago', 'subtotal', 'total')
        }),
        ('Notas', {
            'fields': ('notas',),
            'classes': ('collapse',)
        })
    )
    
    inlines = [ItemPedidoInline]
    
    # Configurar campos de solo lectura dependiendo del contexto (nuevo vs existente)
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editando un pedido existente
            return self.readonly_fields + [
                'usuario', 'nombre_cliente', 'email_cliente', 'telefono_cliente',
                'direccion_envio', 'ciudad_envio', 'codigo_postal_envio', 'provincia_envio',
                'metodo_pago'
            ]
        return self.readonly_fields
    
    # Desactivar la creación de pedidos desde el admin
    def has_add_permission(self, request):
        return False


# Configuración del admin para el modelo ItemPedido
@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    
    list_display = [
        'pedido',
        'nombre_producto',
        'cantidad',
        'precio_unitario',
        'precio_total'
    ]
    
    list_filter = [
        'pedido__estado',
        'pedido__fecha_creacion'
    ]
    
    search_fields = [
        'pedido__numero_pedido',
        'nombre_producto',
        'pedido__nombre_cliente'
    ]
    
    readonly_fields = [
        'pedido',
        'instrumento',
        'cantidad',
        'precio_unitario',
        'precio_total',
        'nombre_producto'
    ]
    
    # Desactivar la creación de items desde el admin
    def has_add_permission(self, request):
        return False
    
    # Desactivar la edición de items desde el admin
    def has_change_permission(self, request, obj=None):
        return False