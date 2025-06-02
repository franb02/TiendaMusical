#!/usr/bin/env python3
"""
Script para diagnosticar problemas de Cloudinary en producción
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_musical.settings')
django.setup()

from django.conf import settings
import cloudinary
import cloudinary.uploader
import cloudinary.api

def verificar_variables_entorno():
    """Verificar variables de entorno de Cloudinary"""
    print("🔍 VERIFICANDO VARIABLES DE ENTORNO")
    print("=" * 50)
    
    variables = [
        'CLOUDINARY_CLOUD_NAME',
        'CLOUDINARY_API_KEY', 
        'CLOUDINARY_API_SECRET',
        'CLOUDINARY_URL'
    ]
    
    for var in variables:
        valor = os.environ.get(var)
        if valor:
            # Ocultar datos sensibles
            if 'SECRET' in var or 'URL' in var:
                valor_mostrar = valor[:10] + "..." if len(valor) > 10 else valor
            else:
                valor_mostrar = valor
            print(f"✅ {var}: {valor_mostrar}")
        else:
            print(f"❌ {var}: NO CONFIGURADA")
    
    return all(os.environ.get(var) for var in variables[:3])

def verificar_configuracion_django():
    """Verificar configuración de Django"""
    print("\n⚙️  VERIFICANDO CONFIGURACIÓN DE DJANGO")
    print("=" * 50)
    
    print(f"📁 DEBUG: {settings.DEBUG}")
    print(f"📁 MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'No configurado')}")
    print(f"📁 MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'No configurado')}")
    print(f"📁 DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    
    cloudinary_storage = getattr(settings, 'CLOUDINARY_STORAGE', {})
    print(f"☁️  CLOUDINARY_STORAGE configurado: {'✅' if cloudinary_storage else '❌'}")
    
    return True

def test_cloudinary_connection():
    """Probar conexión con Cloudinary"""
    print("\n🔗 PROBANDO CONEXIÓN CON CLOUDINARY")
    print("=" * 50)
    
    try:
        # Verificar configuración
        config = cloudinary.config()
        print(f"☁️  Cloud Name: {config.cloud_name}")
        print(f"🔑 API Key: {config.api_key}")
        print(f"🔒 API Secret: {'***' if config.api_secret else 'NO CONFIGURADO'}")
        
        # Test de ping
        result = cloudinary.api.ping()
        print(f"✅ Conexión exitosa: {result}")
        
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_upload_simple():
    """Probar subida simple a Cloudinary"""
    print("\n📤 PROBANDO SUBIDA A CLOUDINARY")
    print("=" * 50)
    
    try:
        # Crear una imagen simple en memoria
        import io
        from PIL import Image
        
        # Crear imagen de 50x50 píxeles
        img = Image.new('RGB', (50, 50), color='blue')
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        # Subir a Cloudinary
        result = cloudinary.uploader.upload(
            img_io.getvalue(),
            folder="test_tienda",
            public_id="test_conexion",
            overwrite=True
        )
        
        print(f"✅ Subida exitosa!")
        print(f"   Public ID: {result.get('public_id')}")
        print(f"   URL: {result.get('secure_url')}")
        print(f"   Formato: {result.get('format')}")
        
        # Intentar eliminar la imagen de prueba
        try:
            cloudinary.uploader.destroy(result['public_id'])
            print("🗑️  Imagen de prueba eliminada")
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ Error en subida: {e}")
        import traceback
        traceback.print_exc()
        return False

def verificar_instrumentos_en_db():
    """Verificar instrumentos en la base de datos"""
    print("\n🎵 VERIFICANDO INSTRUMENTOS EN DB")
    print("=" * 50)
    
    from productos.models import Instrumento
    
    instrumentos = Instrumento.objects.all()
    print(f"📊 Total instrumentos: {instrumentos.count()}")
    
    con_imagen = instrumentos.exclude(imagen='').exclude(imagen__isnull=True)
    print(f"🖼️  Con imagen: {con_imagen.count()}")
    
    for inst in con_imagen[:5]:  # Mostrar solo los primeros 5
        print(f"   🎸 {inst.nombre}")
        print(f"      Imagen: {inst.imagen.name if inst.imagen else 'Sin imagen'}")
        if inst.imagen:
            try:
                url = inst.imagen.url
                print(f"      URL: {url}")
            except Exception as e:
                print(f"      ❌ Error obteniendo URL: {e}")
        print()

def main():
    print("🔧 DIAGNÓSTICO DE CLOUDINARY EN PRODUCCIÓN")
    print("=" * 60)
    
    # Test 1: Variables de entorno
    vars_ok = verificar_variables_entorno()
    
    # Test 2: Configuración Django
    config_ok = verificar_configuracion_django()
    
    # Test 3: Conexión Cloudinary
    if vars_ok:
        conn_ok = test_cloudinary_connection()
        
        # Test 4: Subida de prueba
        if conn_ok:
            upload_ok = test_upload_simple()
    else:
        print("\n❌ No se pueden hacer más tests sin las variables de entorno")
        conn_ok = False
        upload_ok = False
    
    # Test 5: Verificar DB
    verificar_instrumentos_en_db()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    
    print(f"🔧 Variables entorno: {'✅' if vars_ok else '❌'}")
    print(f"⚙️  Configuración Django: {'✅' if config_ok else '❌'}")
    
    if vars_ok:
        print(f"🔗 Conexión Cloudinary: {'✅' if conn_ok else '❌'}")
        if conn_ok:
            print(f"📤 Subida funcional: {'✅' if upload_ok else '❌'}")
    
    if not vars_ok:
        print("\n🚨 PROBLEMA PRINCIPAL: Variables de entorno no configuradas")
        print("📝 SOLUCIÓN:")
        print("1. Ve a https://dashboard.render.com/")
        print("2. Selecciona tu proyecto")
        print("3. Ve a 'Environment'")
        print("4. Añade las variables de Cloudinary")
        print("5. Redespliega el proyecto")
    
    elif not conn_ok:
        print("\n🚨 PROBLEMA PRINCIPAL: No se puede conectar a Cloudinary")
        print("📝 SOLUCIÓN: Verifica que las credenciales sean correctas")
    
    elif not upload_ok:
        print("\n🚨 PROBLEMA PRINCIPAL: No se pueden subir archivos")
        print("📝 SOLUCIÓN: Verifica permisos en Cloudinary")
    
    else:
        print("\n🎉 ¡Todo parece estar funcionando correctamente!")

if __name__ == "__main__":
    main()
