from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.db import transaction

from .models import Pedido, ItemPedido
from .forms import PedidoForm
from carrito.models import Carrito


# Vista para el proceso de checkout de compra
class CheckoutView(LoginRequiredMixin, View):
    
    def get(self, request):
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            if not carrito.items.exists():
                messages.warning(request, 'Tu carrito está vacío')
                return redirect('carrito_detalle')
                
            items = carrito.items.all()
            subtotal = carrito.get_subtotal()
            impuestos = carrito.get_impuestos()
            total = carrito.get_total()
            form = PedidoForm(usuario=request.user)
            
            # Verificar si el usuario tiene dirección completa en su perfil
            direccion_completa = False
            if hasattr(request.user, 'perfil'):
                perfil = request.user.perfil
                direccion_completa = all([
                    perfil.direccion,
                    perfil.ciudad,
                    perfil.codigo_postal,
                    perfil.provincia
                ])
            
            context = {
                'form': form,
                'items': items,
                'subtotal': subtotal,
                'impuestos': impuestos,
                'total': total,
                'direccion_completa': direccion_completa,
            }
            return render(request, 'pedidos/checkout.html', context)
            
        except Carrito.DoesNotExist:
            messages.error(request, 'No tienes un carrito activo')
            return redirect('producto_lista')
    
    def post(self, request):
        form = PedidoForm(request.POST, usuario=request.user)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    carrito = Carrito.objects.get(usuario=request.user)
                    pedido = self.crear_pedido(request, form, carrito)
                    carrito.delete()
                    
                    messages.success(request, f'¡Pedido {pedido.numero_pedido} creado exitosamente! Tu compra ha sido procesada.')
                    return redirect('pedidos_detalle', pedido_id=str(pedido.numero_pedido))
                    
            except Exception as e:
                messages.error(request, f'Error al procesar el pedido: {str(e)}')
        
        # Si hay errores, mostrar formulario de nuevo
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            items = carrito.items.all()
            total = carrito.get_total()
        except Exception:
            messages.error(request, 'Error al recuperar el carrito')
            return redirect('producto_lista')

        context = {
            'form': form,
            'items': items,
            'total': total,
        }
        return render(request, 'pedidos/checkout.html', context)
    
    def crear_pedido(self, request, form, carrito):
        pedido = form.save(commit=False)
        pedido.usuario = request.user
        pedido.save()
        
        try:
            # Crear items del pedido y reducir stock
            for item_carrito in carrito.items.all():
                instrumento = item_carrito.instrumento
                
                # Verificar stock
                if item_carrito.cantidad > instrumento.stock:
                    raise Exception(f"Stock insuficiente para {instrumento.nombre}")
                
                # Reducir stock del instrumento
                instrumento.stock -= item_carrito.cantidad
                instrumento.save()
                
                # Crear item del pedido
                ItemPedido.objects.create(
                    pedido=pedido,
                    instrumento=instrumento,
                    cantidad=item_carrito.cantidad,
                    precio_unitario=instrumento.precio,
                    precio_total=instrumento.precio * item_carrito.cantidad,
                    nombre_producto=instrumento.nombre
                )
            
            # Recalcular total con IVA después de crear los items
            pedido.calcular_total()
            pedido.save()
            
            return pedido
        except Exception as e:
            raise e
    
# vista para mostrar pedidos del usuario
@login_required
def mis_pedidos(request):
    from django.db.models import Q
    from datetime import datetime
    from django.core.paginator import Paginator
    
    # Obtener todos los pedidos del usuario
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    # Aplicar filtros de búsqueda
    buscar = request.GET.get('buscar', '').strip()
    if buscar:
        pedidos = pedidos.filter(
            Q(numero_pedido__icontains=buscar) |
            Q(nombre_cliente__icontains=buscar) |
            Q(items__nombre_producto__icontains=buscar)
        ).distinct()
    
    # Filtrar por estado
    estado = request.GET.get('estado', '').strip()
    if estado:
        pedidos = pedidos.filter(estado=estado)
    
    # Filtrar por fecha desde
    fecha_desde = request.GET.get('fecha_desde', '').strip()
    if fecha_desde:
        try:
            fecha_desde_obj = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_creacion__date__gte=fecha_desde_obj)
        except ValueError:
            pass
    
    # Filtrar por fecha hasta
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()
    if fecha_hasta:
        try:
            fecha_hasta_obj = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_creacion__date__lte=fecha_hasta_obj)
        except ValueError:
            pass
    
    # Paginación
    paginator = Paginator(pedidos, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener estadísticas para mostrar
    stats = {
        'total': Pedido.objects.filter(usuario=request.user).count(),
        'pendientes': Pedido.objects.filter(usuario=request.user, estado='pendiente').count(),
        'confirmados': Pedido.objects.filter(usuario=request.user, estado='confirmado').count(),
        'enviados': Pedido.objects.filter(usuario=request.user, estado='enviado').count(),
        'entregados': Pedido.objects.filter(usuario=request.user, estado='entregado').count(),
        'cancelados': Pedido.objects.filter(usuario=request.user, estado='cancelado').count(),
    }
    
    context = {
        'pedidos': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'stats': stats,
        'filtros_activos': bool(buscar or estado or fecha_desde or fecha_hasta),
    }
    return render(request, 'pedidos/mis_pedidos.html', context)


# vista para mostrar detalle de un pedido específico
@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, numero_pedido=pedido_id, usuario=request.user)
    
    context = {
        'pedido': pedido,
        'items': pedido.items.all(),
        'puede_cancelar': pedido.puede_cancelar()
    }
    return render(request, 'pedidos/detalle.html', context)


# vista para cancelar un pedido existente
@login_required
def cancelar_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, numero_pedido=pedido_id, usuario=request.user)
        
        try:
            pedido.cancelar()
            messages.success(request, 'Pedido cancelado exitosamente')
        except Exception as e:
            messages.error(request, f'Error al cancelar pedido: {str(e)}')
    
    return redirect('pedidos_detalle', pedido_id=pedido_id)
