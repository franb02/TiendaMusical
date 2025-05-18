from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)
    provincia = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea un perfil automáticamente cuando se crea un usuario"""
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    """Guarda el perfil cuando se actualiza el usuario"""
    instance.perfil.save()
