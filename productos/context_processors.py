from .models import Categoria

def categoria_actual(request):
    return {
        'categorias_globales': Categoria.objects.all()
    }
