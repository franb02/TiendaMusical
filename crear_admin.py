#!/usr/bin/env python
"""
Script para crear usuario admin manualmente
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

def crear_admin():
    """Crear usuario admin"""
    User = get_user_model()
    
    username = 'admin'
    email = 'fbarrosos02@educarexx.es'
    password = 'admin123'  # Cambia esto por la contraseña que quieras
    
    # Verificar si ya existe
    if User.objects.filter(username=username).exists():
        print(f"❌ El usuario '{username}' ya existe")
        user = User.objects.get(username=username)
        print(f"   📧 Email: {user.email}")
        print(f"   🔑 Es superusuario: {'Sí' if user.is_superuser else 'No'}")
        return
    
    # Crear usuario
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Usuario '{username}' creado exitosamente!")
        print(f"   📧 Email: {email}")
        print(f"   🔑 Es superusuario: Sí")
        print(f"   🔓 Contraseña: {password}")
        print()
        print("🌐 Ahora puedes acceder al admin en:")
        print("   https://tienda-musical.onrender.com/admin/")
        
    except Exception as e:
        print(f"❌ Error al crear usuario: {e}")

if __name__ == "__main__":
    crear_admin()