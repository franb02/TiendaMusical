#!/usr/bin/env python3
"""
Script para probar la funcionalidad de imágenes
"""
import os
import django
import sys
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_musical.settings')
django.setup()

from django.conf import settings
from productos.models import Instrumento, Categoria
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile

def test_configuracion_media():
    """Probar configuración de archivos media"""
    print("🧪 PROBANDO CONFIGURACIÓN DE IMÁGENES")
    print("=" * 50)
    
    print(f"📁 DEBUG: {settings.DEBUG}")
    print(f"📁 MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'No configurado')}")
    print(f"📁 MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'No configurado')}")
    print(f"📁 DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    
    # Verificar que el directorio existe
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if media_root:
        instrumentos_dir = Path(media_root) / 'instrumentos'
        print(f"📁 Directorio instrumentos existe: {instrumentos_dir.exists()}")
        if not instrumentos_dir.exists():
            instrumentos_dir.mkdir(parents=True, exist_ok=True)
            print("✅ Directorio creado")
    
    return True

def test_crear_categoria():
    """Crear una categoría de prueba si no existe"""
    print("\n🏷️  PROBANDO CATEGORÍAS")
    print("-" * 30)
    
    categoria, created = Categoria.objects.get_or_create(
        nombre="Guitarras",
        defaults={
            'descripcion': 'Instrumentos de cuerda'
        }
    )
    
    if created:
        print("✅ Categoría 'Guitarras' creada")
    else:
        print("ℹ️  Categoría 'Guitarras' ya existe")
    
    return categoria

def test_crear_instrumento_sin_imagen():
    """Crear un instrumento sin imagen"""
    print("\n🎸 PROBANDO INSTRUMENTO SIN IMAGEN")
    print("-" * 40)
    
    categoria = test_crear_categoria()
    
    instrumento, created = Instrumento.objects.get_or_create(
        nombre="Guitarra Acústica Test",
        defaults={
            'categoria': categoria,
            'descripcion': 'Guitarra de prueba sin imagen',
            'precio': 299.99,
            'stock': 5
        }
    )
    
    if created:
        print("✅ Instrumento sin imagen creado")
    else:
        print("ℹ️  Instrumento sin imagen ya existe")
    
    print(f"   URL imagen: {instrumento.imagen.url if instrumento.imagen else 'Sin imagen'}")
    return instrumento

def test_crear_imagen_dummy():
    """Crear una imagen dummy para pruebas"""
    print("\n🖼️  CREANDO IMAGEN DUMMY")
    print("-" * 30)
    
    # Crear una imagen PNG simple (1x1 pixel)
    import io
    from PIL import Image
    
    # Crear imagen de 100x100 píxeles
    img = Image.new('RGB', (100, 100), color='red')
    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    
    # Crear archivo Django
    imagen_file = SimpleUploadedFile(
        name='guitarra_test.png',
        content=img_io.read(),
        content_type='image/png'
    )
    
    print("✅ Imagen dummy creada")
    return imagen_file

def test_crear_instrumento_con_imagen():
    """Crear un instrumento con imagen"""
    print("\n🎸🖼️  PROBANDO INSTRUMENTO CON IMAGEN")
    print("-" * 45)
    
    try:
        categoria = test_crear_categoria()
        imagen = test_crear_imagen_dummy()
        
        # Eliminar instrumento anterior si existe
        Instrumento.objects.filter(nombre="Guitarra Eléctrica Test").delete()
        
        instrumento = Instrumento.objects.create(
            nombre="Guitarra Eléctrica Test",
            categoria=categoria,
            descripcion='Guitarra de prueba con imagen',
            precio=599.99,
            stock=3,
            imagen=imagen
        )
        
        print("✅ Instrumento con imagen creado")
        print(f"   ID: {instrumento.id}")
        print(f"   Nombre: {instrumento.nombre}")
        print(f"   Imagen: {instrumento.imagen.name if instrumento.imagen else 'Sin imagen'}")
        
        if instrumento.imagen:
            print(f"   URL imagen: {instrumento.imagen.url}")
            
            # Verificar que el archivo existe
            ruta_fisica = Path(settings.MEDIA_ROOT) / instrumento.imagen.name
            print(f"   Archivo existe: {ruta_fisica.exists()}")
            print(f"   Ruta física: {ruta_fisica}")
        
        return instrumento
        
    except Exception as e:
        print(f"❌ Error creando instrumento con imagen: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("🧪 TEST DE FUNCIONALIDAD DE IMÁGENES")
    print("=" * 60)
    
    # Test 1: Configuración
    test_configuracion_media()
    
    # Test 2: Instrumento sin imagen
    test_crear_instrumento_sin_imagen()
    
    # Test 3: Instrumento con imagen
    instrumento_con_imagen = test_crear_instrumento_con_imagen()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE INSTRUMENTOS")
    print("=" * 60)
    
    instrumentos = Instrumento.objects.all()
    for inst in instrumentos:
        print(f"🎵 {inst.nombre}")
        print(f"   Precio: €{inst.precio}")
        print(f"   Imagen: {'✅' if inst.imagen else '❌'}")
        if inst.imagen:
            print(f"   URL: {inst.imagen.url}")
        print()
    
    print("🎉 Tests completados!")
    
    if instrumento_con_imagen:
        print("\n📝 PRÓXIMOS PASOS:")
        print("1. Inicia el servidor: python manage.py runserver")
        print("2. Ve al admin: http://127.0.0.1:8000/admin/")
        print("3. Verifica que las imágenes se muestren correctamente")
        print("4. Si funciona localmente, configuraremos Cloudinary para producción")

if __name__ == "__main__":
    main()
