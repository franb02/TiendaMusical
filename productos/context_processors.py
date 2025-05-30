from .models import Categoria

def categoria_actual(request):
    return {
        'categorias': Categoria.objects.all()
    }
