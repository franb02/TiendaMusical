#!/usr/bin/env bash
# exit on error
set -o errexit

# Verificar variables de entorno de Cloudinary
echo "🔍 Verificando configuración de Cloudinary..."
python verificar_env.py

pip install -r requirements.txt

# Crear directorios necesarios
mkdir -p media/instrumentos

python manage.py collectstatic --no-input
python manage.py migrate

# Crear superusuario automáticamente si no existe
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()

# Usar variables de entorno o valores por defecto
admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
admin_email = os.environ.get('ADMIN_EMAIL', 'admin@tiendamusical.com')
admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')

if not User.objects.filter(username=admin_username).exists():
    User.objects.create_superuser(
        username=admin_username,
        email=admin_email,
        password=admin_password
    )
    print(f'✅ Superusuario {admin_username} creado')
else:
    print(f'ℹ️  Superusuario {admin_username} ya existe')
"

# Diagnóstico completo de Cloudinary en producción
echo "🔧 Ejecutando diagnóstico completo de Cloudinary..."
python diagnostico_produccion.py

# Migrar imágenes existentes a Cloudinary
echo "🔄 Migrando imágenes existentes a Cloudinary..."
python migrar_imagenes.py
