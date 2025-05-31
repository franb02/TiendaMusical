// JavaScript para checkout

document.addEventListener('DOMContentLoaded', function() {
    // Manejo de direcciones
    const radioGuardada = document.getElementById('usar_guardada');
    const radioNueva = document.getElementById('nueva_direccion');
    const formularioNueva = document.getElementById('formulario-nueva-direccion');
    
    function toggleFormulario() {
        if (radioNueva && radioNueva.checked) {
            if (formularioNueva) formularioNueva.style.display = 'block';
        } else if (radioGuardada && radioGuardada.checked) {
            if (formularioNueva) formularioNueva.style.display = 'none';
        }
    }
    
    if (radioGuardada) radioGuardada.addEventListener('change', toggleFormulario);
    if (radioNueva) radioNueva.addEventListener('change', toggleFormulario);
    toggleFormulario();
    
    // Validación básica
    const form = document.getElementById('checkout-form');
    const submitBtn = document.getElementById('btn-confirmar');
    const terminos = document.getElementById('terminos');
    
    if (terminos && submitBtn) {
        terminos.addEventListener('change', () => {
            submitBtn.disabled = !terminos.checked;
        });
        submitBtn.disabled = !terminos.checked;
    }
    
    if (form && submitBtn) {
        form.addEventListener('submit', function() {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...';
        });
    }
});

// Función para confirmar pedido desde modal
function confirmarPedido() {
    const form = document.getElementById('checkout-form');
    if (form) form.submit();
}