from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('productos/', views.InstrumentoListView.as_view(), name='producto_lista'),
    path('categoria/<slug:slug>/', views.CategoriaDetailView.as_view(), name='categoria_detalle'),
    path('producto/<slug:slug>/', views.InstrumentoDetailView.as_view(), name='instrumento_detalle'),
]