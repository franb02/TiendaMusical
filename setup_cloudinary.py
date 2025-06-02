#!/usr/bin/env python3
"""
Script para configurar Cloudinary automáticamente
"""
import os
import subprocess
import sys

def main():
    print("🔧 CONFIGURACIÓN DE CLOUDINARY")
    print("=" * 50)
    
    print("\n📋 Para configurar Cloudinary necesitas:")
    print("1. Ir a https://cloudinary.com/console")
    print("2. Iniciar sesión en tu cuenta")
    print("3. Copiar las credenciales del Dashboard")
    print("\n" + "=" * 50)
    
    # Solicitar credenciales
    print("\n🔑 Introduce tus credenciales de Cloudinary:")
    cloud_name = input("Cloud Name: ").strip()
    api_key = input("API Key: ").strip()
    api_secret = input("API Secret: ").strip()
    
    if not all([cloud_name, api_key, api_secret]):
        print("❌ Error: Todas las credenciales son obligatorias")
        return False
    
    # Construir CLOUDINARY_URL
    cloudinary_url = f"cloudinary://{api_key}:{api_secret}@{cloud_name}"
    
    # Leer archivo .env actual
    env_file = ".env"
    lines = []
    
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            lines = f.readlines()
    
    # Remover líneas existentes de Cloudinary (comentadas o no)
    lines = [line for line in lines if not any(var in line for var in [
        'CLOUDINARY_CLOUD_NAME', 'CLOUDINARY_API_KEY', 
        'CLOUDINARY_API_SECRET', 'CLOUDINARY_URL'
    ])]
    
    # Añadir nuevas credenciales
    lines.append(f"\n# Configuración de Cloudinary\n")
    lines.append(f"CLOUDINARY_CLOUD_NAME={cloud_name}\n")
    lines.append(f"CLOUDINARY_API_KEY={api_key}\n")
    lines.append(f"CLOUDINARY_API_SECRET={api_secret}\n")
    lines.append(f"CLOUDINARY_URL={cloudinary_url}\n")
    
    # Escribir archivo .env
    with open(env_file, 'w') as f:
        f.writelines(lines)
    
    print(f"\n✅ Credenciales guardadas en {env_file}")
    
    # Probar la configuración
    print("\n🧪 Probando la configuración...")
    try:
        # Recargar variables de entorno
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        # Probar Cloudinary
        import cloudinary
        import cloudinary.uploader
        
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
        
        # Test básico
        result = cloudinary.api.ping()
        print("✅ Conexión con Cloudinary exitosa!")
        print(f"   Cloud: {cloud_name}")
        print(f"   Status: {result.get('status', 'OK')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando Cloudinary: {e}")
        return False

if __name__ == "__main__":
    if main():
        print("\n🎉 ¡Cloudinary configurado correctamente!")
        print("\n📝 Próximos pasos:")
        print("1. Ejecuta: python diagnosticar_cloudinary.py")
        print("2. Sube algunas imágenes de prueba al admin")
        print("3. Despliega a Render con: git add . && git commit -m 'Fix cloudinary' && git push")
    else:
        print("\n❌ Configuración fallida. Revisa las credenciales.")
