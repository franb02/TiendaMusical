from .models import Carrito


def carrito_context(request):
    # Context processor para hacer el carrito disponible en todos los templates    
    if not request.user.is_authenticated:
        # Usuario no autenticado no tiene carrito
        return {
            'carrito': {
                'get_total_items': lambda: 0,
                'get_total_precio': lambda: 0.0,
                'items': []
            }
        }
    
    try:
        # Usuario autenticado - usar carrito 
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        return {
            'carrito': carrito
        }
    except Exception as e:
        # En caso de error, devolver carrito vacío
        return {
            'carrito': {
                'get_total_items': lambda: 0,
                'get_total_precio': lambda: 0.0,
                'items': []
            }
        }
