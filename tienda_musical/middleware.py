"""
Middleware personalizado - Ya no necesario con Cloudinary en producción
"""
from django.conf import settings
from django.http import Http404, HttpResponse
from django.utils._os import safe_join
import os
import mimetypes
import logging

logger = logging.getLogger(__name__)

class MediaServeMiddleware:
    """
    Middleware para servir archivos media solo en desarrollo
    En producción Cloudinary maneja los archivos media
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Solo procesar archivos media en desarrollo (DEBUG=True)
        # En producción, Cloudinary maneja las imágenes automáticamente
        if settings.DEBUG and hasattr(settings, 'MEDIA_URL') and request.path.startswith(settings.MEDIA_URL):
            try:
                # Obtener la ruta del archivo
                relative_path = request.path[len(settings.MEDIA_URL):]
                file_path = safe_join(settings.MEDIA_ROOT, relative_path)
                
                logger.info(f"Sirviendo archivo local en desarrollo: {file_path}")
                
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    # Determinar el tipo de contenido
                    content_type, _ = mimetypes.guess_type(file_path)
                    
                    # Leer y devolver el archivo
                    with open(file_path, 'rb') as f:
                        response = HttpResponse(f.read(), content_type=content_type)
                        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
                        response['Cache-Control'] = 'public, max-age=31536000'  # Cache por 1 año
                        return response
                else:
                    logger.warning(f"Archivo no encontrado en desarrollo: {file_path}")
                    raise Http404("Archivo media no encontrado")
            except Exception as e:
                logger.error(f"Error sirviendo archivo media en desarrollo: {e}")
                raise Http404("Archivo media no encontrado")
        
        # Para cualquier otra petición, continuar normalmente
        response = self.get_response(request)
        return response
