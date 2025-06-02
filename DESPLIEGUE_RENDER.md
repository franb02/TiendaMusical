# 🚀 Guía de Despliegue en Render - Tienda Musical

## ✅ Archivos de Configuración Creados

Los siguientes archivos han sido configurados para el despliegue:

- ✅ `build.sh` - Script de construcción para Render
- ✅ `runtime.txt` - Especifica Python 3.11.10
- ✅ `requirements.txt` - Dependencias actualizadas
- ✅ `settings.py` - Configurado para producción
- ✅ `.env.example` - Plantilla de variables de entorno
- ✅ `.gitignore` - Actualizado para Render

## 🛠️ Pasos para Desplegar en Render

### 1. Subir código a GitHub/GitLab
```bash
git add .
git commit -m "Configuración para despliegue en Render"
git push origin main
```

### 2. Crear Web Service en Render
1. Ve a [render.com](https://render.com)
2. Crea una cuenta o inicia sesión
3. Haz clic en "New +" → "Web Service"
4. Conecta tu repositorio

### 3. Configuración del Web Service
```
Name: tienda-musical
Environment: Python 3
Build Command: ./build.sh
Start Command: gunicorn tienda_musical.wsgi:application
```

### 4. Variables de Entorno en Render
```
SECRET_KEY=6au0l7vhq93un==n=uq@_io2^+jrlh-6n+tl7g$+)sn33o*v$s
DEBUG=False
```

### 5. Crear Base de Datos PostgreSQL
1. En Render dashboard: "New +" → "PostgreSQL"
2. Configurar nombre: `tienda-musical-db`
3. Copiar la "External Database URL"
4. Añadir a variables de entorno: `DATABASE_URL=<url-copiada>`

### 6. Desplegar
1. Haz clic en "Create Web Service"
2. Render automáticamente:
   - Clonará tu repositorio
   - Ejecutará `build.sh`
   - Instalará dependencias
   - Recolectará archivos estáticos
   - Ejecutará migraciones
   - Iniciará la aplicación

## 🔧 Comandos Post-Despliegue

### Crear superusuario en producción:
En el shell de Render (desde el dashboard):
```bash
python manage.py createsuperuser
```

### Cargar datos iniciales (si tienes fixtures):
```bash
python manage.py loaddata tu_fixture.json
```

## 🌐 URLs del Proyecto Desplegado

- **Aplicación web**: `https://tu-app-name.onrender.com`
- **Admin panel**: `https://tu-app-name.onrender.com/admin/`

## 🔐 Configuraciones de Seguridad Aplicadas

- ✅ SECRET_KEY segura generada
- ✅ DEBUG=False en producción
- ✅ ALLOWED_HOSTS configurado para Render
- ✅ HTTPS/SSL configuraciones
- ✅ Cookies seguras
- ✅ HSTS habilitado
- ✅ WhiteNoise para archivos estáticos

## 📁 Estructura de Archivos para Render

```
TiendaMusical/
├── build.sh              # Script de construcción
├── runtime.txt           # Versión de Python
├── requirements.txt      # Dependencias
├── .env.example         # Plantilla de variables
├── verificar_entorno.py # Script de verificación
├── manage.py
├── tienda_musical/
│   ├── settings.py      # Configurado para producción
│   ├── wsgi.py
│   └── urls.py
├── static/              # Archivos estáticos
├── staticfiles/         # Archivos recolectados
├── media/               # Archivos multimedia
└── apps/                # Aplicaciones Django
```

## 🐛 Solución de Problemas Comunes

### Error de migraciones:
```bash
python manage.py migrate --run-syncdb
```

### Error de archivos estáticos:
```bash
python manage.py collectstatic --clear --noinput
```

### Verificar logs en Render:
- Ve al dashboard de tu servicio
- Haz clic en "Logs" para ver errores

### Reiniciar el servicio:
- En el dashboard: "Manual Deploy" → "Clear build cache & deploy"

## 🎯 Próximos Pasos Opcionales

1. **Configurar dominio personalizado** en Render
2. **Configurar email backend** (SendGrid, Mailgun)
3. **Implementar almacenamiento externo** (AWS S3) para archivos media
4. **Configurar monitoreo** y alertas
5. **Implementar CI/CD** para despliegues automáticos

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs en Render dashboard
2. Verifica que todas las variables de entorno estén configuradas
3. Asegúrate de que la base de datos esté conectada correctamente

¡Tu aplicación Tienda Musical está lista para ser desplegada en Render! 🎉
