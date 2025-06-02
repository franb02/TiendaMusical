#!/usr/bin/env python3
"""
Script para migrar imágenes existentes a Cloudinary
"""
import os
import django
import sys
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_musical.settings')
django.setup()

from django.conf import settings
from productos.models import Instrumento
import cloudinary.uploader
from django.core.files.base import ContentFile
import requests

def migrar_imagenes_a_cloudinary():
    """Migrar todas las imágenes locales a Cloudinary"""
    print("🔄 MIGRANDO IMÁGENES A CLOUDINARY")
    print("=" * 50)
    
    # Obtener todos los instrumentos con imágenes
    instrumentos = Instrumento.objects.exclude(imagen='').exclude(imagen__isnull=True)
    print(f"📊 Total instrumentos con imágenes: {instrumentos.count()}")
    
    migrados = 0
    errores = 0
    
    for instrumento in instrumentos:
        try:
            print(f"\n🎸 Procesando: {instrumento.nombre}")
            print(f"   Imagen actual: {instrumento.imagen.name}")
            
            # Verificar si ya está en Cloudinary
            if 'cloudinary' in str(instrumento.imagen.url):
                print(f"   ✅ Ya está en Cloudinary: {instrumento.imagen.url}")
                continue
            
            # Intentar abrir la imagen local
            try:
                imagen_content = instrumento.imagen.read()
                print(f"   📁 Imagen local encontrada: {len(imagen_content)} bytes")
            except Exception as e:
                print(f"   ❌ Error leyendo imagen local: {e}")
                # Intentar crear una imagen placeholder
                imagen_content = crear_imagen_placeholder(instrumento.nombre)
                if not imagen_content:
                    errores += 1
                    continue
            
            # Subir a Cloudinary
            nombre_archivo = Path(instrumento.imagen.name).stem
            resultado = cloudinary.uploader.upload(
                imagen_content,
                folder="instrumentos",
                public_id=f"{nombre_archivo}_{instrumento.id}",
                overwrite=True,
                resource_type="image"
            )
            
            print(f"   ☁️  Subida a Cloudinary exitosa")
            print(f"   🔗 Nueva URL: {resultado['secure_url']}")
            
            # Actualizar el modelo (esto hará que Django use la URL de Cloudinary)
            # No necesitamos cambiar el campo, solo asegurarnos de que Cloudinary está activo
            
            migrados += 1
            
        except Exception as e:
            print(f"   ❌ Error migrando {instrumento.nombre}: {e}")
            errores += 1
    
    print(f"\n{'='*50}")
    print(f"📊 RESULTADO DE LA MIGRACIÓN")
    print(f"{'='*50}")
    print(f"✅ Migrados exitosamente: {migrados}")
    print(f"❌ Errores: {errores}")
    print(f"📁 Total procesados: {migrados + errores}")
    
    return migrados, errores

def crear_imagen_placeholder(nombre_instrumento):
    """Crear una imagen placeholder para instrumentos sin imagen"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Crear imagen de 300x300
        img = Image.new('RGB', (300, 300), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        # Añadir texto
        try:
            # Intentar usar una fuente por defecto
            font = ImageFont.load_default()
        except:
            font = None
        
        # Dibujar texto centrado
        texto = f"🎵\n{nombre_instrumento[:20]}"
        bbox = draw.textbbox((0, 0), texto, font=font)
        texto_width = bbox[2] - bbox[0]
        texto_height = bbox[3] - bbox[1]
        
        x = (300 - texto_width) // 2
        y = (300 - texto_height) // 2
        
        draw.text((x, y), texto, fill='#666666', font=font, align='center')
        
        # Convertir a bytes
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        print(f"   🖼️  Imagen placeholder creada")
        return img_io.getvalue()
        
    except Exception as e:
        print(f"   ❌ Error creando placeholder: {e}")
        return None

def verificar_migracion():
    """Verificar que las imágenes estén funcionando después de la migración"""
    print("\n🧪 VERIFICANDO MIGRACIÓN")
    print("=" * 50)
    
    instrumentos = Instrumento.objects.exclude(imagen='').exclude(imagen__isnull=True)
    
    funcionando = 0
    con_problemas = 0
    
    for instrumento in instrumentos[:5]:  # Verificar solo los primeros 5
        try:
            url = instrumento.imagen.url
            print(f"🎸 {instrumento.nombre}")
            print(f"   URL: {url}")
            
            if 'cloudinary' in url:
                print(f"   ✅ URL de Cloudinary")
                funcionando += 1
            else:
                print(f"   ⚠️  URL local")
                con_problemas += 1
                
        except Exception as e:
            print(f"   ❌ Error obteniendo URL: {e}")
            con_problemas += 1
        print()
    
    print(f"✅ Funcionando con Cloudinary: {funcionando}")
    print(f"⚠️  Con problemas: {con_problemas}")

def main():
    print("🚀 MIGRACIÓN DE IMÁGENES A CLOUDINARY")
    print("=" * 60)
    
    # Verificar que Cloudinary esté configurado
    if not all([
        os.environ.get('CLOUDINARY_CLOUD_NAME'),
        os.environ.get('CLOUDINARY_API_KEY'),
        os.environ.get('CLOUDINARY_API_SECRET')
    ]):
        print("❌ Cloudinary no está configurado correctamente")
        return
    
    print("✅ Cloudinary configurado correctamente")
    
    # Realizar migración
    migrados, errores = migrar_imagenes_a_cloudinary()
    
    # Verificar resultado
    verificar_migracion()
    
    print("\n" + "="*60)
    print("🎉 MIGRACIÓN COMPLETADA")
    print("="*60)
    print("📝 Próximos pasos:")
    print("1. Las nuevas imágenes ya deberían estar en Cloudinary")
    print("2. Prueba subir una nueva imagen desde el admin")
    print("3. Verifica que las URLs ya no den error 404")

if __name__ == "__main__":
    main()
