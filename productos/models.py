from django.db import models
from django.utils.text import slugify
# Modelo para categorias 
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

# Modelo para instrumentos
class Instrumento(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    categoria = models.ForeignKey(Categoria, related_name='instrumentos', on_delete=models.CASCADE)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='instrumentos/', blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    especificaciones = models.JSONField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Instrumento'
        verbose_name_plural = 'Instrumentos'
        ordering = ['-fecha_creacion']

# Modelo para archivos de audio (dejar para mas adelante)
class ArchivoAudio(models.Model):
    instrumento = models.ForeignKey(Instrumento, related_name='audios', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='audios/')
    descripcion = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.instrumento.nombre}"
    
    class Meta:
        verbose_name = 'Archivo de Audio'
        verbose_name_plural = 'Archivos de Audio'
