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
        
    # Devuelve 8 instrumentos destacados aleatorios.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destacados'] = Instrumento.objects.filter(disponible=True).order_by('?')[:8]
        context['categorias'] = Categoria.objects.all()
        return context

# Vista unificada para la lista de instrumentos y categorías
class InstrumentoListView(ListView):
    model = Instrumento
    template_name = 'productos/instrumento_lista.html'
    context_object_name = 'instrumentos'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Instrumento.objects.filter(disponible=True)
        
        # Filtro por categoria (puede venir de URL o parámetro)
        categoria_slug = self.kwargs.get('slug') or self.kwargs.get('categoria_slug')
        if categoria_slug:
            queryset = queryset.filter(categoria__slug=categoria_slug)
        
        # Búsqueda
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
        
        # Añadir todas las categorías para los filtros
        context['categorias'] = Categoria.objects.all()
        
        # Añadir información de filtros activos
        categoria_slug = self.kwargs.get('slug') or self.kwargs.get('categoria_slug')
        if categoria_slug:
            categoria = get_object_or_404(Categoria, slug=categoria_slug)
            context['categoria_actual'] = categoria
            # Actualizar el título dinámicamente
            context['page_title'] = f"{categoria.nombre} - Tienda Musical"
        else:
            context['page_title'] = "Catálogo de Instrumentos"
            
        context['query'] = self.request.GET.get('q', '')
        context['orden'] = self.request.GET.get('orden', '')
        
        return context

# Vista para instrumento
class InstrumentoDetailView(DetailView):
    model = Instrumento
    template_name = 'productos/instrumento_detalle.html'
    context_object_name = 'instrumento'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['relacionados'] = Instrumento.objects.filter(
            categoria=self.object.categoria,
            disponible=True
        ).exclude(id=self.object.id).order_by('?')[:4]
        return context
