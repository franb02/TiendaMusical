from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Categoria, Instrumento
from django.db.models import Q

# Vista para la pagina de inicio
class HomeView(ListView):
    model = Instrumento
    template_name = 'productos/home.html'
    context_object_name = 'instrumentos'

    # Devuelve los 8 instrumentos más recientes
    def get_queryset(self):
        return Instrumento.objects.filter(disponible=True).order_by('-fecha_creacion')[:8]
        
    # Devuelve 4 instrumentos destacados aleatorios.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['destacados'] = Instrumento.objects.filter(disponible=True).order_by('?')[:4]
        return context

# Vista para la lista de instrumentos y filtros
class InstrumentoListView(ListView):
    model = Instrumento
    template_name = 'productos/instrumento_lista.html'
    context_object_name = 'instrumentos'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Instrumento.objects.filter(disponible=True)
        
        # Filtro por categoria
        categoria_slug = self.kwargs.get('categoria_slug')
        if categoria_slug:
            queryset = queryset.filter(categoria__slug=categoria_slug)
        
        # Busqueda
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(descripcion__icontains=query) |
                Q(categoria__nombre__icontains=query)
            )
        
        # Ordenamiento
        orden = self.request.GET.get('orden')
        if orden == 'precio_asc':
            queryset = queryset.order_by('precio')
        elif orden == 'precio_desc':
            queryset = queryset.order_by('-precio')
        elif orden == 'nombre':
            queryset = queryset.order_by('nombre')
        else:
            queryset = queryset.order_by('-fecha_creacion')
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        
        # Añadir información de filtros activos
        categoria_slug = self.kwargs.get('categoria_slug')
        if categoria_slug:
            context['categoria_actual'] = get_object_or_404(Categoria, slug=categoria_slug)
            
        context['query'] = self.request.GET.get('q', '')
        context['orden'] = self.request.GET.get('orden', '')
        
        return context

# Vista para la lista de categorías
class CategoriaDetailView(DetailView):
    model = Categoria
    template_name = 'productos/categoria_detalle.html'
    context_object_name = 'categoria'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instrumentos'] = Instrumento.objects.filter(
            categoria=self.object,
            disponible=True
        )
        context['categorias'] = Categoria.objects.all()
        return context

# Vista para instrumento
class InstrumentoDetailView(DetailView):
    model = Instrumento
    template_name = 'productos/instrumento_detalle.html'
    context_object_name = 'instrumento'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['relacionados'] = Instrumento.objects.filter(
            categoria=self.object.categoria,
            disponible=True
        ).exclude(id=self.object.id).order_by('?')[:4]
        return context
