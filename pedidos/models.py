from django.db import models
from django.contrib.auth.models import User
from productos.models import Instrumento
import uuid
from decimal import Decimal

# Modelo para pedidos de compra
class Pedido(models.Model):
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    METODO_PAGO_CHOICES = [
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('paypal', 'PayPal'),
        ('transferencia', 'Transferencia'),
        ('contrareembolso', 'Contra Reembolso'),
    ]
    
    # ID único
    numero_pedido = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Cliente
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos', null=True, blank=True)
    nombre_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField()
    telefono_cliente = models.CharField(max_length=15)
    
    # Envío
    direccion_envio = models.TextField()
    ciudad_envio = models.CharField(max_length=100)
    codigo_postal_envio = models.CharField(max_length=10)
    provincia_envio = models.CharField(max_length=100)
    
    # Pedido
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    
    # Totales
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f'Pedido {self.numero_pedido} - {self.nombre_cliente}'
    # Guardar pedido
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    #  Calcula el total incluyendo IVA
    def calcular_total(self):
        try:
            self.subtotal = sum(item.precio_total for item in self.items.all())
            # Calculamos el IVA (21%) directamente
            iva = self.subtotal * Decimal('0.21')
            self.total = self.subtotal + iva
            return self.total
        except Exception as e:
            # En caso de error, establecer valores por defecto
            self.subtotal = Decimal('0.00')
            self.total = Decimal('0.00')
            return self.total
    
    @property
    def impuestos(self):
        return self.subtotal * Decimal('0.21') if hasattr(self, 'subtotal') and self.subtotal else Decimal('0.00')
    
    @property
    def costo_envio(self):
        return Decimal('0.00')
    
    def get_estado_info(self):
        estado_info = {
            'pendiente': {'color': 'warning', 'icono': 'fas fa-clock', 'texto': 'Pendiente'},
            'confirmado': {'color': 'info', 'icono': 'fas fa-check-circle', 'texto': 'Confirmado'},
            'enviado': {'color': 'primary', 'icono': 'fas fa-truck', 'texto': 'Enviado'},
            'entregado': {'color': 'success', 'icono': 'fas fa-check', 'texto': 'Entregado'},
            'cancelado': {'color': 'danger', 'icono': 'fas fa-times', 'texto': 'Cancelado'},
        }
        return estado_info.get(self.estado, {'color': 'secondary', 'icono': 'fas fa-question', 'texto': 'Desconocido'})
    
    def puede_cancelar(self):
        return self.estado in ['pendiente', 'confirmado']
    
    def cancelar(self):
        if not self.puede_cancelar():
            raise Exception("No se puede cancelar este pedido")
        
        # Restaurar stock
        for item in self.items.all():
            instrumento = item.instrumento
            instrumento.stock += item.cantidad
            instrumento.save()
        
        self.estado = 'cancelado'
        self.save()

# Items del pedido
class ItemPedido(models.Model):
    
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Datos del producto (por si cambia)
    nombre_producto = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Items de Pedido'
    
    def __str__(self):
        return f'{self.cantidad} x {self.nombre_producto}'
    
    def save(self, *args, **kwargs):
        self.precio_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
