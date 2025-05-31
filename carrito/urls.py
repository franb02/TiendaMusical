from django.urls import path
from . import views

urlpatterns = [
    path('', views.CarritoView.as_view(), name='carrito_detalle'),
    path('agregar/<int:instrumento_id>/', views.carrito_agregar, name='carrito_agregar'),
    path('eliminar/<int:instrumento_id>/', views.carrito_eliminar, name='carrito_eliminar'),
    path('actualizar/<int:instrumento_id>/', views.carrito_actualizar, name='carrito_actualizar'),
    path('resumen/', views.carrito_resumen, name='carrito_resumen'),
    path('limpiar/', views.carrito_limpiar, name='carrito_limpiar'),
]