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
