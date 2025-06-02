"""
Middleware personalizado para servir archivos media en producción con WhiteNoise
"""
from django.conf import settings
from django.http import Http404, HttpResponse
from django.utils._os import safe_join
from django.views.static import serve
import os
import mimetypes


class MediaServeMiddleware:
    """
    Middleware para servir archivos media en producción
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Solo procesar si es una petición de media y estamos en producción
        if not settings.DEBUG and request.path.startswith(settings.MEDIA_URL):
            try:
                # Obtener la ruta del archivo
                relative_path = request.path[len(settings.MEDIA_URL):]
                file_path = safe_join(settings.MEDIA_ROOT, relative_path)
                
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    # Determinar el tipo de contenido
                    content_type, _ = mimetypes.guess_type(file_path)
                    
                    # Leer y devolver el archivo
                    with open(file_path, 'rb') as f:
                        response = HttpResponse(f.read(), content_type=content_type)
                        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
                        return response
                else:
                    raise Http404("Archivo media no encontrado")
            except:
                raise Http404("Archivo media no encontrado")
        
        # Para cualquier otra petición, continuar normalmente
        response = self.get_response(request)
        return response
