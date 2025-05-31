from django.db import models
from django.contrib.auth.models import User
from productos.models import Instrumento
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction

#Modelo para el carrito 
class Carrito(models.Model):    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrito', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True) 
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
    
    def __str__(self):
        if self.usuario:
            return f'Carrito de {self.usuario.username}'
        return f'Carrito anónimo {self.session_key}'
    
    # total de items en el carrito
    def get_total_items(self):
        return sum(item.cantidad for item in self.items.all())
    # subtotal del carrito
    def get_subtotal(self):
        return sum(item.get_total_precio() for item in self.items.all())
    #  Calcula IVA
    def get_impuestos(self):
        return self.get_subtotal() * Decimal('0.21')
    # subtotal del carrito + IVA
    def get_total(self):
        return self.get_subtotal() + self.get_impuestos()
    # vacia el carrito
    def limpiar(self):
        self.items.all().delete()

# Modelo para cada item en el carrito 
class ItemCarrito(models.Model):    
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Item de Carrito'
        verbose_name_plural = 'Items de Carrito'
        unique_together = ('carrito', 'instrumento')
    
    def __str__(self):
        return f'{self.cantidad} x {self.instrumento.nombre}'
    # Calcula el precio total del item 
    def get_total_precio(self):
        return self.cantidad * self.instrumento.precio
    
    def save(self, *args, **kwargs):
        # Validar stock antes de guardar
        if self.cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor a 0')
        if self.cantidad > self.instrumento.stock:
            raise ValidationError(f'No hay suficiente stock. Disponible: {self.instrumento.stock}')
        super().save(*args, **kwargs)

    def clean(self):
        if self.cantidad and self.instrumento:
            if self.cantidad > self.instrumento.stock:
                raise ValidationError(f'No hay suficiente stock para {self.instrumento.nombre}. Disponible: {self.instrumento.stock}')