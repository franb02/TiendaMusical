// JavaScript común para todas las páginas de pedidos

document.addEventListener('DOMContentLoaded', function() {
    
    // Funcionalidad para el filtro de pedidos
    inicializarFiltrosPedidos();
    
    // Funcionalidad para confirmaciones de cancelación
    inicializarConfirmacionesCancelacion();
    
    // Funcionalidad para estados de pedidos
    inicializarTooltipsEstado();
    
});

// Inicializa los filtros de pedidos en la página de lista
function inicializarFiltrosPedidos() {
    const formularioFiltros = document.getElementById('filtros-form');
    if (!formularioFiltros) return;
    
    const entradaFiltros = formularioFiltros.querySelectorAll('select, input[type="date"]');
    entradaFiltros.forEach(entrada => {
        entrada.addEventListener('change', function() {
            formularioFiltros.submit();
        });
    });
    
    // Búsqueda
    const entradaBusqueda = formularioFiltros.querySelector('input[name="buscar"]');
    if (entradaBusqueda) {
        let temporizador;
        entradaBusqueda.addEventListener('input', function() {
            clearTimeout(temporizador);
            temporizador = setTimeout(() => {
                formularioFiltros.submit();
            }, 500);
        });
    }
    
    // Botón para limpiar filtros
    const botonLimpiar = document.createElement('button');
    botonLimpiar.type = 'button';
    botonLimpiar.className = 'btn btn-outline-secondary btn-sm';
    botonLimpiar.innerHTML = '<i class="fas fa-times me-1"></i>Limpiar';
    botonLimpiar.addEventListener('click', function() {
        entradaFiltros.forEach(entrada => {
            if (entrada.type === 'select-one') {
                entrada.selectedIndex = 0;
            } else {
                entrada.value = '';
            }
        });
        formularioFiltros.submit();
    });
    
    const contenedorBoton = formularioFiltros.querySelector('.d-grid');
    if (contenedorBoton) {
        contenedorBoton.appendChild(botonLimpiar);
    }
}

// confirmaciones para cancelar pedidos

function inicializarConfirmacionesCancelacion() {
    const formulariosCancelacion = document.querySelectorAll('form[action*="cancelar"]');
    
    formulariosCancelacion.forEach(formulario => {
        formulario.addEventListener('submit', function(e) {
            const pedidoId = this.action.match(/cancelar\/([^\/]+)/)?.[1] || '';
            
            const confirmado = confirm(
                `¿Estás seguro de que quieres cancelar el pedido #${pedidoId}?\n\n` +
                'Esta acción no se puede deshacer y el stock será restaurado.'
            );
            
            if (!confirmado) {
                e.preventDefault();
            }
        });
    });
}

// Inicializa tooltips para estados de pedidos

function inicializarTooltipsEstado() {
    const badgesEstado = document.querySelectorAll('.estado-badge');
    
    badgesEstado.forEach(badge => {
        const estado = badge.classList.toString().match(/estado-(\w+)/)?.[1];
        if (estado) {
            const textoTooltip = obtenerTooltipEstado(estado);
            badge.setAttribute('title', textoTooltip);
            badge.setAttribute('data-bs-toggle', 'tooltip');
        }
    });
    
    // Inicializar tooltips de Bootstrap
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const listaTooltipTrigger = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        listaTooltipTrigger.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Obtiene el texto del tooltip para un estado
function obtenerTooltipEstado(estado) {
    const tooltips = {
        'pendiente': 'El pedido está pendiente de confirmación',
        'confirmado': 'El pedido ha sido confirmado y está siendo preparado',
        'enviado': 'El pedido ha sido enviado y está en camino',
        'entregado': 'El pedido ha sido entregado con éxito',
        'cancelado': 'El pedido ha sido cancelado'
    };
    
    return tooltips[estado] || 'Estado del pedido';
}

// Utilidades para manejo de errores y mensajes en pedidos
const UtilidadesPedidos = {

    mostrarToast: function(mensaje, tipo = 'info') {
        const contenedorToast = document.querySelector('.toast-container') || 
                              this.crearContenedorToast();
        
        const htmlToast = `
            <div class="toast align-items-center text-white bg-${tipo}" role="alert">
                <div class="d-flex">
                    <div class="toast-body">${mensaje}</div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        
        contenedorToast.insertAdjacentHTML('beforeend', htmlToast);
        
        const toast = contenedorToast.lastElementChild;
        if (typeof bootstrap !== 'undefined' && bootstrap.Toast) {
            new bootstrap.Toast(toast).show();
        }
    },
    
    // crea el contenedor de toasts si no existe
    
    crearContenedorToast: function() {
        const contenedor = document.createElement('div');
        contenedor.className = 'toast-container position-fixed top-0 end-0 p-3';
        contenedor.style.zIndex = '1060';
        document.body.appendChild(contenedor);
        return contenedor;
    },
    
    // Formatea números como moneda
     
    formatearMoneda: function(cantidad) {
        return new Intl.NumberFormat('es-ES', {
            style: 'currency',
            currency: 'EUR'
        }).format(cantidad);
    },
    
    // Formatea fechas
    formatearFecha: function(fecha) {
        return new Intl.DateTimeFormat('es-ES', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(fecha));
    }
};

window.UtilidadesPedidos = UtilidadesPedidos;
