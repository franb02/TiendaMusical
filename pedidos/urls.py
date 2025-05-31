# rutas para la aplicación de pedidos
from django.urls import path
from . import views

urlpatterns = [
    # rutas para proceso de checkout y pedidos
    path('checkout/', views.CheckoutView.as_view(), name='pedidos_checkout'),
    path('mis-pedidos/', views.mis_pedidos, name='pedidos_mis_pedidos'),
    path('detalle/<uuid:pedido_id>/', views.detalle_pedido, name='pedidos_detalle'),
    path('cancelar/<uuid:pedido_id>/', views.cancelar_pedido, name='pedidos_cancelar'),
]