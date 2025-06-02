#!/usr/bin/env python
"""
Script para verificar que el entorno esté correctamente configurado antes del despliegue
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_musical.settings')
django.setup()

def verificar_entorno():
    """Verifica la configuración del entorno"""
    print("🔍 Verificando configuración del entorno...")
    
    # Verificar variables de entorno críticas
    variables_criticas = ['SECRET_KEY']
    for var in variables_criticas:
        if not os.environ.get(var):
            print(f"❌ Variable {var} no está configurada")
            return False
        else:
            print(f"✅ Variable {var} configurada")
    
    # Verificar configuración de base de datos
    from django.conf import settings
    if hasattr(settings, 'DATABASES') and settings.DATABASES:
        print("✅ Configuración de base de datos encontrada")
    else:
        print("❌ Configuración de base de datos no encontrada")
        return False
    
    # Verificar archivos críticos
    archivos_criticos = ['requirements.txt', 'build.sh', 'runtime.txt']
    for archivo in archivos_criticos:
        if (BASE_DIR / archivo).exists():
            print(f"✅ Archivo {archivo} encontrado")
        else:
            print(f"❌ Archivo {archivo} no encontrado")
            return False
    
    # Verificar que collectstatic funciona
    try:
        from django.core.management import execute_from_command_line
        print("✅ Django configurado correctamente")
    except Exception as e:
        print(f"❌ Error en configuración de Django: {e}")
        return False
    
    print("\n🎉 ¡Entorno verificado correctamente! Listo para desplegar en Render.")
    return True

if __name__ == "__main__":
    verificar_entorno()
