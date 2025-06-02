#!/usr/bin/env python3
"""
Test específico para verificar que las imágenes van a Cloudinary
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_musical.settings')
django.setup()

from django.conf import settings
from productos.models import Instrumento, Categoria
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

def test_nueva_imagen_cloudinary():
    """Probar que una nueva imagen va directamente a Cloudinary"""
    print("🧪 TEST: NUEVA IMAGEN → CLOUDINARY")
    print("=" * 50)
    
    # Verificar configuración
    print(f"🔧 DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    
    # Crear categoría si no existe
    categoria, created = Categoria.objects.get_or_create(
        nombre="Test Cloudinary",
        defaults={'descripcion': 'Categoría de prueba'}
    )
    print(f"📁 Categoría: {categoria.nombre}")
    
    # Crear imagen de prueba
    img = Image.new('RGB', (200, 200), color='green')
    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    
    imagen_file = SimpleUploadedFile(
        name='test_cloudinary.png',
        content=img_io.read(),
        content_type='image/png'
    )
    print("🖼️  Imagen de prueba creada")
    
    # Eliminar instrumento anterior si existe
    Instrumento.objects.filter(nombre="Test Cloudinary Nuevo").delete()
    
    # Crear instrumento
    instrumento = Instrumento.objects.create(
        nombre="Test Cloudinary Nuevo",
        categoria=categoria,
        descripcion='Instrumento para probar Cloudinary',
        precio=99.99,
        stock=1,
        imagen=imagen_file
    )
    
    print(f"🎸 Instrumento creado: {instrumento.nombre}")
    print(f"📁 Archivo imagen: {instrumento.imagen.name}")
    
    # Verificar URL
    try:
        url = instrumento.imagen.url
        print(f"🔗 URL generada: {url}")
        
        if 'cloudinary' in url:
            print("✅ ¡ÉXITO! La imagen está en Cloudinary")
            return True
        else:
            print("❌ ERROR: La imagen NO está en Cloudinary")
            print(f"   URL local: {url}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR obteniendo URL: {e}")
        return False

def verificar_configuracion_completa():
    """Verificar toda la configuración de Cloudinary"""
    print("\n🔍 VERIFICACIÓN COMPLETA DE CONFIGURACIÓN")
    print("=" * 50)
    
    # Variables de entorno
    vars_requeridas = ['CLOUDINARY_CLOUD_NAME', 'CLOUDINARY_API_KEY', 'CLOUDINARY_API_SECRET']
    todas_configuradas = True
    
    for var in vars_requeridas:
        valor = os.environ.get(var)
        if valor:
            print(f"✅ {var}: Configurada")
        else:
            print(f"❌ {var}: NO configurada")
            todas_configuradas = False
    
    # Configuración Django
    storage = getattr(settings, 'DEFAULT_FILE_STORAGE', None)
    print(f"\n📁 DEFAULT_FILE_STORAGE: {storage}")
    
    if storage == 'cloudinary_storage.storage.MediaCloudinaryStorage':
        print("✅ Storage configurado para Cloudinary")
    else:
        print("❌ Storage NO configurado para Cloudinary")
        todas_configuradas = False
    
    return todas_configuradas

def main():
    print("🚀 TEST DE CLOUDINARY EN DJANGO ADMIN")
    print("=" * 60)
    
    # Verificar configuración
    config_ok = verificar_configuracion_completa()
    
    if not config_ok:
        print("\n❌ CONFIGURACIÓN INCOMPLETA")
        print("📝 Revisa las variables de entorno y configuración")
        return
    
    # Test de imagen nueva
    exito = test_nueva_imagen_cloudinary()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO DEL TEST")
    print("=" * 60)
    
    if exito:
        print("🎉 ¡TODO FUNCIONA CORRECTAMENTE!")
        print("📝 Las nuevas imágenes van a Cloudinary automáticamente")
    else:
        print("❌ HAY UN PROBLEMA CON LA CONFIGURACIÓN")
        print("📝 Las imágenes no van a Cloudinary")
        
        # Sugerencias de solución
        print("\n💡 POSIBLES SOLUCIONES:")
        print("1. Verifica que las variables estén en el .env")
        print("2. Reinicia el servidor de Django")
        print("3. Revisa los logs del servidor")

if __name__ == "__main__":
    main()
