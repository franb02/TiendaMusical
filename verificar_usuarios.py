#!/usr/bin/env python
"""
Script para verificar usuarios en la base de datos
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

from django.contrib.auth import get_user_model

def verificar_usuarios():
    """Verifica qué usuarios existen en la base de datos"""
    User = get_user_model()
    
    print("🔍 Verificando usuarios en la base de datos...")
    print("-" * 50)
    
    usuarios = User.objects.all()
    
    if not usuarios.exists():
        print("❌ No hay usuarios en la base de datos")
        return False
    
    print(f"✅ Total de usuarios: {usuarios.count()}")
    print()
    
    for usuario in usuarios:
        print(f"👤 Usuario: {usuario.username}")
        print(f"   📧 Email: {usuario.email}")
        print(f"   🔑 Es superusuario: {'Sí' if usuario.is_superuser else 'No'}")
        print(f"   🔓 Es staff: {'Sí' if usuario.is_staff else 'No'}")
        print(f"   📅 Creado: {usuario.date_joined}")
        print("-" * 30)
    
    # Verificar específicamente el usuario admin
    try:
        admin_user = User.objects.get(username='admin')
        print("✅ Usuario 'admin' encontrado:")
        print(f"   📧 Email: {admin_user.email}")
        print(f"   🔑 Es superusuario: {'Sí' if admin_user.is_superuser else 'No'}")
        print(f"   ✅ Activo: {'Sí' if admin_user.is_active else 'No'}")
    except User.DoesNotExist:
        print("❌ Usuario 'admin' NO encontrado")
        print("💡 Necesitas crear el usuario admin")
    
    return True

if __name__ == "__main__":
    verificar_usuarios()