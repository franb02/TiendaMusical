from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.core.exceptions import ValidationError
import json
import logging

from productos.models import Instrumento
from .models import Carrito, ItemCarrito
from .forms import CarritoAgregarProductoForm

logger = logging.getLogger(__name__)

# Vista para mostrar el carrito de compras a usuarios autenticados
@method_decorator(login_required, name='dispatch')
class CarritoView(LoginRequiredMixin, View):    
    def get(self, request):
        try:
            # Solo usuarios autenticados usar carrito persistente
            carrito, created = Carrito.objects.get_or_create(usuario=request.user)
            items = carrito.items.select_related('instrumento').all()
            
            # Agregar información de stock a cada item
            for item in items:
                item.stock_disponible = item.instrumento.stock
                item.stock_restante = item.instrumento.stock - item.cantidad
                item.puede_aumentar = item.cantidad < item.instrumento.stock
                
            total_items = carrito.get_total_items()
            subtotal = carrito.get_subtotal()
            impuestos = carrito.get_impuestos()
            total = carrito.get_total()
            
            context = {
                'items': items,
                'total_items': total_items,
                'subtotal': subtotal,
                'impuestos': impuestos,
                'total': total,
            }
            return render(request, 'carrito/detalle.html', context)
        except Exception as e:
            # Si hay cualquier error, mostrar carrito vacio
            logger.error(f"Error en CarritoView para usuario {request.user.id}: {e}")
            context = {
                'items': [],
                'total_items': 0,
                'subtotal': 0,
                'impuestos': 0,
                'total': 0,
            }
            return render(request, 'carrito/detalle.html', context)

# Vista para agregar productos al carrito con ajax
@require_POST
@login_required
def carrito_agregar(request, instrumento_id):
    instrumento = get_object_or_404(Instrumento, id=instrumento_id)
    
    try:
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad <= 0:
            cantidad = 1
    except (ValueError, TypeError):
        cantidad = 1
    
    # Verificar stock disponible
    if cantidad > instrumento.stock:
        return JsonResponse({
            'success': False,
            'message': f'Solo hay {instrumento.stock} unidades disponibles',
            'stock_disponible': instrumento.stock
        })
    
    try:
        with transaction.atomic():
            carrito, created = Carrito.objects.get_or_create(usuario=request.user)
            
            item, created = ItemCarrito.objects.get_or_create(
                carrito=carrito,
                instrumento=instrumento,
                defaults={'cantidad': cantidad}
            )
            
            if not created:
                # El item ya existe, actualizar cantidad
                nueva_cantidad = item.cantidad + cantidad
                if nueva_cantidad > instrumento.stock:
                    return JsonResponse({
                        'success': False,
                        'message': f'No hay suficiente stock. Máximo: {instrumento.stock}',
                        'stock_disponible': instrumento.stock
                    })
                item.cantidad = nueva_cantidad
                item.save()
            
            total_items = carrito.get_total_items()
            total_precio = carrito.get_total()
            
            return JsonResponse({
                'success': True,
                'message': f'{instrumento.nombre} agregado al carrito',
                'total_items': total_items,
                'total_precio': float(total_precio),
                'cart_total_items': total_items, 
                'subtotal': float(carrito.get_subtotal()),
                'impuestos': float(carrito.get_impuestos())
            })
            
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })
    except Exception as e:
        logger.error(f"Error agregando al carrito: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Error interno del servidor'
        })

# Vista para eliminar productos del carrito 
@require_POST
@login_required
def carrito_eliminar(request, instrumento_id):
    instrumento = get_object_or_404(Instrumento, id=instrumento_id)
    
    # Solo usuarios autenticados usar carrito persistente
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    try:
        item = ItemCarrito.objects.get(carrito=carrito, instrumento=instrumento)
        item.delete()
    except ItemCarrito.DoesNotExist:
        pass
    
    # devolver un  JSON en caso de ser una peticion ajax
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        return JsonResponse({
            'success': True,
            'message': f'{instrumento.nombre} eliminado del carrito',
            'total_items': carrito.get_total_items(),
            'total_precio': float(carrito.get_total()),
            'subtotal': float(carrito.get_subtotal()),
            'impuestos': float(carrito.get_impuestos())
        })
    
    # Si no es ajaxx, redirigir al carrito
    return redirect('carrito_detalle')

# Vista para actualizar la cantidad de productos en el carrito
@require_POST
@login_required
def carrito_actualizar(request, instrumento_id):
    instrumento = get_object_or_404(Instrumento, id=instrumento_id)
    
    try:
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        if nueva_cantidad <= 0:
            nueva_cantidad = 1
    except (ValueError, TypeError):
        return redirect('carrito_detalle')
    
    # stock disponible
    if nueva_cantidad > instrumento.stock:
        return redirect('carrito_detalle')
    
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    try:
        item = ItemCarrito.objects.get(carrito=carrito, instrumento=instrumento)
        item.cantidad = nueva_cantidad
        item.save()
        
        precio_item = item.get_total_precio()
        total_items = carrito.get_total_items()
        total_precio = carrito.get_total()
        subtotal = carrito.get_subtotal()
        impuestos = carrito.get_impuestos()
        
    except ItemCarrito.DoesNotExist:
        return redirect('carrito_detalle')
    
    # devolver un  JSON en caso de ser una peticion ajax
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Cantidad actualizada',
            'nueva_cantidad': nueva_cantidad,
            'precio_item': float(precio_item),
            'total_items': total_items,
            'total_precio': float(total_precio),
            'subtotal': float(subtotal),
            'impuestos': float(impuestos)
        })
    
    # Si no es ajax, redirigir al carrito
    return redirect('carrito_detalle')

# Vista para obtener el resumen del carrito con ajax
def carrito_resumen(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'total_items': 0,
            'total_precio': 0.0,
            'subtotal': 0.0,
            'impuestos': 0.0
        })
    
    try:
        # Usuario autenticado - usar carrito persistente
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        total_items = carrito.get_total_items()
        total_precio = carrito.get_total()
        subtotal = carrito.get_subtotal()
        impuestos = carrito.get_impuestos()
        
        return JsonResponse({
            'total_items': total_items,
            'total_precio': float(total_precio),
            'subtotal': float(subtotal),
            'impuestos': float(impuestos)
        })
    except Exception as e:
        logger.error(f"Error en carrito_resumen para usuario {request.user.id}: {e}")
        return JsonResponse({
            'total_items': 0,
            'total_precio': 0.0,
            'subtotal': 0.0,
            'impuestos': 0.0
        })

# Vista para limpiar todo el carrito
@require_POST
@login_required
def carrito_limpiar(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito.items.all().delete()

    # devolver un  JSON en caso de ser una peticion ajax
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        return JsonResponse({
            'success': True,
            'message': 'Carrito vaciado correctamente',
            'total_items': 0,
            'total_precio': 0,
            'subtotal': 0,
            'impuestos': 0
        })
    
    # Si no es ajax, redirigir al carrito
    return redirect('carrito_detalle')