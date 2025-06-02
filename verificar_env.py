"""
Verificación rápida de Cloudinary para logging en producción
"""
import os
print("=" * 60)
print("🔍 VERIFICACIÓN DE CLOUDINARY EN RENDER")
print("=" * 60)

# Verificar variables de entorno
vars_cloudinary = [
    'CLOUDINARY_CLOUD_NAME',
    'CLOUDINARY_API_KEY', 
    'CLOUDINARY_API_SECRET',
    'CLOUDINARY_URL'
]

print("📋 Variables de entorno:")
for var in vars_cloudinary:
    valor = os.environ.get(var)
    if valor:
        # Mostrar solo parte para seguridad
        if 'SECRET' in var or 'URL' in var:
            valor_seguro = valor[:8] + "..." if len(valor) > 8 else "***"
        else:
            valor_seguro = valor
        print(f"  ✅ {var}: {valor_seguro}")
    else:
        print(f"  ❌ {var}: NO CONFIGURADA")

# Verificar configuración básica
print(f"\n📁 DEBUG: {os.environ.get('DEBUG', 'True')}")
print(f"📁 DATABASE_URL: {'✅ Configurada' if os.environ.get('DATABASE_URL') else '❌ No configurada'}")

print("=" * 60)
