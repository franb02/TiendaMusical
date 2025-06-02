#!/usr/bin/env python
"""
Script para diagnosticar la configuración de Cloudinary
"""
import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_musical.settings')
django.setup()

def diagnosticar_cloudinary():
    print("🔍 DIAGNÓSTICO DE CLOUDINARY")
    print("=" * 50)
    
    # Verificar variables de entorno
    print("\n📋 VARIABLES DE ENTORNO:")
    cloudinary_vars = [
        'CLOUDINARY_CLOUD_NAME',
        'CLOUDINARY_API_KEY', 
        'CLOUDINARY_API_SECRET',
        'CLOUDINARY_URL'
    ]
    
    for var in cloudinary_vars:
        value = os.environ.get(var)
        if value:
            # Ocultar información sensible
            if 'SECRET' in var or 'KEY' in var:
                masked_value = value[:8] + '*' * (len(value) - 8) if len(value) > 8 else '***'
                print(f"  ✅ {var}: {masked_value}")
            else:
                print(f"  ✅ {var}: {value}")
        else:
            print(f"  ❌ {var}: NO CONFIGURADA")
    
    # Verificar configuración de Django
    print("\n⚙️  CONFIGURACIÓN DE DJANGO:")
    print(f"  DEBUG: {settings.DEBUG}")
    print(f"  DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    
    # Verificar configuración de Cloudinary
    print("\n☁️  CONFIGURACIÓN DE CLOUDINARY:")
    try:
        import cloudinary
        print(f"  cloudinary instalado: ✅")
        print(f"  cloud_name: {cloudinary.config().cloud_name}")
        print(f"  api_key: {cloudinary.config().api_key[:8]}***" if cloudinary.config().api_key else "No configurado")
        print(f"  secure: {cloudinary.config().secure}")
    except ImportError:
        print("  ❌ cloudinary NO está instalado")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test de conexión
    print("\n🔗 TEST DE CONEXIÓN:")
    try:
        import cloudinary.uploader
        import cloudinary.api
        
        # Intentar obtener información de la cuenta
        result = cloudinary.api.ping()
        print(f"  ✅ Conexión exitosa: {result}")
        
        # Intentar subir una imagen de prueba
        print("\n📤 TEST DE SUBIDA:")
        test_result = cloudinary.uploader.upload(
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
            folder="test",
            public_id="test_image"
        )
        print(f"  ✅ Subida exitosa: {test_result.get('secure_url', 'Sin URL')}")
        
        # Eliminar la imagen de prueba
        cloudinary.uploader.destroy("test/test_image")
        print("  🗑️  Imagen de prueba eliminada")
        
    except Exception as e:
        print(f"  ❌ Error de conexión: {e}")
    
    # Verificar instrumentos con imágenes
    print("\n🎵 INSTRUMENTOS CON IMÁGENES:")
    try:
        from productos.models import Instrumento
        instrumentos = Instrumento.objects.exclude(imagen='')
        
        if instrumentos.exists():
            for instrumento in instrumentos[:5]:  # Solo mostrar los primeros 5
                print(f"  📷 {instrumento.nombre}: {instrumento.imagen}")
        else:
            print("  ℹ️  No hay instrumentos con imágenes")
            
    except Exception as e:
        print(f"  ❌ Error consultando instrumentos: {e}")

if __name__ == "__main__":
    diagnosticar_cloudinary()
