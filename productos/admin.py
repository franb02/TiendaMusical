from django.contrib import admin
from .models import Categoria, Instrumento, ArchivoAudio

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ['nombre']

@admin.register(Instrumento)
class InstrumentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'disponible', 'fecha_creacion']
    list_filter = ['disponible', 'categoria', 'fecha_creacion']
    list_editable = ['precio', 'stock', 'disponible']
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ['nombre', 'descripcion']
    date_hierarchy = 'fecha_creacion'

@admin.register(ArchivoAudio)
class ArchivoAudioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'instrumento', 'descripcion']
    list_filter = ['instrumento']
    search_fields = ['titulo', 'descripcion', 'instrumento__nombre']
