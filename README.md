# Tienda Musical - Proyecto Django

Una aplicación web de tienda musical desarrollada con Django que permite a los usuarios navegar, comprar instrumentos musicales y gestionar pedidos.

## Características

- Sistema de autenticación de usuarios
- Catálogo de instrumentos musicales
- Carrito de compras
- Sistema de pedidos
- Panel de administración
- Interfaz responsive con Bootstrap

## Tecnologías Utilizadas

- Django 5.1+
- PostgreSQL
- HTML5/CSS3/JavaScript
- Bootstrap 5
- Crispy Forms

## Instalación Local

1. Clona el repositorio:
```bash
git clone <tu-repositorio>
cd TiendaMusical
```

2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita .env con tus configuraciones locales
```

5. Ejecuta las migraciones:
```bash
python manage.py migrate
```

6. Crea un superusuario:
```bash
python manage.py createsuperuser
```

7. Ejecuta el servidor de desarrollo:
```bash
python manage.py runserver
```

## Despliegue en Render

### Paso 1: Preparar el repositorio

Asegúrate de que todos los archivos de configuración estén en tu repositorio:
- `build.sh` - Script de construcción
- `runtime.txt` - Versión de Python
- `requirements.txt` - Dependencias
- Configuración de producción en `settings.py`

### Paso 2: Crear el servicio en Render

1. Ve a [render.com](https://render.com) e inicia sesión
2. Haz clic en "New +" y selecciona "Web Service"
3. Conecta tu repositorio de GitHub/GitLab
4. Configura el servicio:
   - **Name**: tienda-musical (o el nombre que prefieras)
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn tienda_musical.wsgi:application`

### Paso 3: Configurar variables de entorno

En el dashboard de Render, ve a "Environment" y añade:

```
SECRET_KEY=tu-clave-secreta-super-segura-y-larga
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
```

### Paso 4: Configurar la base de datos

1. En Render, crea una nueva "PostgreSQL Database"
2. Copia la "External Database URL"
3. Úsala como valor para `DATABASE_URL` en las variables de entorno

### Paso 5: Desplegar

1. Haz clic en "Deploy" en el dashboard
2. Render automáticamente:
   - Ejecutará `build.sh`
   - Instalará dependencias
   - Recolectará archivos estáticos
   - Ejecutará migraciones
   - Iniciará la aplicación con Gunicorn

### Comandos útiles después del despliegue

Para crear un superusuario en producción:
```bash
# En el shell de Render
python manage.py createsuperuser
```

## Estructura del Proyecto

```
TiendaMusical/
├── carrito/           # App del carrito de compras
├── pedidos/           # App de gestión de pedidos
├── productos/         # App del catálogo de productos
├── usuarios/          # App de gestión de usuarios
├── static/           # Archivos estáticos (CSS, JS, imágenes)
├── templates/        # Plantillas HTML
├── media/           # Archivos multimedia subidos
├── tienda_musical/  # Configuración principal del proyecto
├── manage.py
├── requirements.txt
├── build.sh         # Script de construcción para Render
├── runtime.txt      # Versión de Python para Render
└── .env.example     # Variables de entorno de ejemplo
```

## Variables de Entorno

### Desarrollo
```bash
DEBUG=True
SECRET_KEY=django-insecure-key
```

### Producción
```bash
DEBUG=False
SECRET_KEY=clave-secreta-super-segura
DATABASE_URL=postgresql://user:password@host:port/database
```

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT.
