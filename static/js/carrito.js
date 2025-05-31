// Funcionalidad para agregar productos al carrito

// Manejo de formularios cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    // Formulario individual (detalle de producto)
    const formularioDetalle = document.querySelector('#formulario-agregar-carrito');
    
    if (formularioDetalle) {
        formularioDetalle.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const datosFormulario = new FormData(this);
            
            fetch(this.action, {
                method: 'POST',
                body: datosFormulario,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    actualizarContadorCarrito(data.total_items);
                    mostrarToast('Producto agregado al carrito correctamente', 'success');
                    
                    // Resetear cantidad a 1
                    const campoCantidad = document.querySelector('#id_cantidad');
                    if (campoCantidad) campoCantidad.value = 1;
                } else {
                    mostrarToast(data.message || 'Error al agregar el producto', 'error');
                }
            })
            .catch(() => mostrarToast('Error de conexión', 'error'));
        });
    }

    // Formularios múltiples (lista de productos)
    document.querySelectorAll('.add-to-cart-form').forEach(formulario => {
        formulario.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const datosFormulario = new FormData(this);
            const url = this.dataset.url;
            
            fetch(url, {
                method: 'POST',
                body: datosFormulario,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    actualizarContadorCarrito(data.total_items);
                    mostrarToast('Producto agregado al carrito correctamente', 'success');
                } else {
                    mostrarToast(data.message || 'Error al agregar el producto', 'error');
                }
            })
            .catch(() => mostrarToast('Error de conexión', 'error'));
        });
    });
});

// Mostrar mensajes al usuario
function mostrarToast(mensaje, tipo = 'success') {
    const toast = document.getElementById('cart-toast');
    const mensajeToast = document.getElementById('toast-message');
    
    if (!toast || !mensajeToast) return;
    
    const iconoHeader = toast.querySelector('.toast-header i');
    
    mensajeToast.textContent = mensaje;
    
    // Cambiar icono según el tipo
    if (iconoHeader) {
        if (tipo === 'success') {
            iconoHeader.className = 'fas fa-check-circle text-success me-2';
        } else {
            iconoHeader.className = 'fas fa-exclamation-triangle text-warning me-2';
        }
    }
    
    // Mostrar toast usando Bootstrap
    try {
        const bsToast = new bootstrap.Toast(toast, {
            autohide: true,
            delay: 3000
        });
        bsToast.show();
    } catch (error) {
        console.error('Error al mostrar toast:', error);
    }
}
