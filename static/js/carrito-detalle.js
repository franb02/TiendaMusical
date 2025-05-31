// Funcionalidad para la página del carrito

// Token CSRF para peticiones POST
function getCsrfToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    if (token) return token.value;
    
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') return value;
    }
    return null;
}

// Mostrar mensajes al usuario usando clases Bootstrap
function mostrarToast(mensaje, tipo) {
    const toast = document.getElementById('cart-toast');
    const message = document.getElementById('toast-message');
    
    if (!toast || !message) return;
    
    message.textContent = mensaje;
    toast.className = 'toast';
    
    if (tipo === 'success') {
        toast.classList.add('bg-success', 'text-white');
    } else {
        toast.classList.add('bg-danger', 'text-white');
    }
    
    try {
        const bsToast = new bootstrap.Toast(toast, { autohide: true, delay: 3000 });
        bsToast.show();
    } catch (error) {
        console.error('Error al mostrar toast:', error);
    }
}

// Peticiones POST al servidor
function request(url, data = {}) {
    const csrf = getCsrfToken();
    if (!csrf) {
        mostrarToast('Error: Token CSRF no encontrado', 'error');
        return Promise.reject('No CSRF token');
    }

    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrf,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: new URLSearchParams(data).toString()
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
    });
}

// Cambiar cantidad del producto
function cambiarCantidad(id, cantidad) {
    const item = document.querySelector(`[data-id="${id}"]`);
    if (!item) return;
    
    const stock = parseInt(item.dataset.stock) || 0;
    const input = item.querySelector('.input-cantidad');
    
    if (cantidad <= 0) {
        mostrarToast('La cantidad mínima es 1', 'error');
        if (input) input.value = 1;
        return;
    }
    
    if (cantidad > stock) {
        mostrarToast(`Stock máximo: ${stock} unidades`, 'error');
        if (input) input.value = stock;
        return;
    }
    
    request(`/carrito/actualizar/${id}/`, { cantidad })
        .then(data => {
            if (data.success) {
                const precio = document.querySelector(`[data-id="${id}"] .precio-total-item`);
                if (precio && data.precio_item) {
                    precio.textContent = `€${parseFloat(data.precio_item).toFixed(2)}`;
                }
                
                actualizarTotalesUI(data);
                actualizarContadorCarrito();
                mostrarToast('Cantidad actualizada', 'success');
            } else {
                mostrarToast(data.message || 'Error al actualizar cantidad', 'error');
                setTimeout(() => location.reload(), 1500);
            }
        })
        .catch(() => {
            mostrarToast('Error al actualizar cantidad', 'error');
            setTimeout(() => location.reload(), 1500);
        });
}

// Eliminar producto del carrito
function eliminarDelCarrito(id) {
    if (!confirm('¿Eliminar este producto del carrito?')) return;
    
    request(`/carrito/eliminar/${id}/`)
        .then(data => {
            if (data.success) {
                const item = document.querySelector(`[data-id="${id}"]`);
                if (item) item.remove();
                
                actualizarTotalesUI(data);
                actualizarContadorCarrito();
                mostrarToast(data.message, 'success');
                
                if (data.total_items === 0) {
                    setTimeout(() => location.reload(), 1000);
                }
            } else {
                mostrarToast(data.message, 'error');
            }
        })
        .catch(() => mostrarToast('Error al eliminar producto', 'error'));
}

// Vaciar carrito completo
function limpiarCarrito() {
    if (!confirm('¿Estás seguro de vaciar todo el carrito?')) return;
    
    request('/carrito/limpiar/')
        .then(data => {
            if (data.success) {
                const contador = document.getElementById('cart-count');
                if (contador) {
                    contador.textContent = '0';
                    contador.style.display = 'none';
                }
                
                mostrarToast('Carrito vaciado correctamente', 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                mostrarToast(data.message, 'error');
            }
        })
        .catch(() => mostrarToast('Error al vaciar carrito', 'error'));
}

// Actualizar totales en la interfaz
function actualizarTotalesUI(data) {
    if (data.subtotal !== undefined) {
        const subtotal = document.getElementById('subtotal');
        if (subtotal) subtotal.textContent = `€${parseFloat(data.subtotal).toFixed(2)}`;
    }
    
    if (data.impuestos !== undefined) {
        const impuestos = document.getElementById('impuestos');
        if (impuestos) impuestos.textContent = `€${parseFloat(data.impuestos).toFixed(2)}`;
    }
    
    if (data.total_precio !== undefined) {
        const total = document.getElementById('total');
        if (total) total.textContent = `€${parseFloat(data.total_precio).toFixed(2)}`;
    }
}

// Inicialización de contador carrito 
document.addEventListener('DOMContentLoaded', function() {
    actualizarContadorCarrito();
    
    document.querySelectorAll('.input-cantidad').forEach(input => {
        input.addEventListener('change', function() {
            const item = this.closest('[data-id]');
            if (item) {
                const id = item.getAttribute('data-id');
                const cantidad = parseInt(this.value) || 1;
                
                if (cantidad > 0) {
                    cambiarCantidad(id, cantidad);
                } else {
                    this.value = 1;
                    mostrarToast('La cantidad mínima es 1', 'error');
                }
            }
        });
        
        input.addEventListener('input', function() {
            if (this.value < 1) this.value = 1;
        });
    });
});
