
// Configuración de validación básica
const configuracionValidacion = {
    mensajes: {
        campoVacio: 'Este campo es obligatorio',
        emailInvalido: 'Ingresa un email válido',
        contrasenaCorta: 'La contraseña debe tener al menos 8 caracteres'
    }
};

// Inicializar cuando cargue la página
document.addEventListener('DOMContentLoaded', function() {
    agregarClasesBootstrap();
    configurarValidacionBasica();
});

// Agregar clases Bootstrap a los campos
function agregarClasesBootstrap() {
    const camposFormulario = document.querySelectorAll('input');
    
    camposFormulario.forEach(function(campo) {
        campo.classList.add('form-control');
    });
}

// Validación básica en tiempo real
function configurarValidacionBasica() {
    const formularios = document.querySelectorAll('form');
    
    formularios.forEach(function(formulario) {
        formulario.addEventListener('submit', function(evento) {
            if (!validarFormulario(formulario)) {
                evento.preventDefault();
            }
        });
        
        // Validación en tiempo real para campos específicos
        const camposEmail = formulario.querySelectorAll('input[type="email"]');
        const camposContrasena = formulario.querySelectorAll('input[type="password"]');
        
        camposEmail.forEach(function(campo) {
            campo.addEventListener('blur', function() {
                validarEmail(campo);
            });
        });
        
        camposContrasena.forEach(function(campo) {
            campo.addEventListener('blur', function() {
                validarContrasena(campo);
            });
        });
    });
}

// Validar formulario completo
function validarFormulario(formulario) {
    let esValido = true;
    const camposObligatorios = formulario.querySelectorAll('input[required]');
    
    camposObligatorios.forEach(function(campo) {
        if (!campo.value.trim()) {
            mostrarError(campo, configuracionValidacion.mensajes.campoVacio);
            esValido = false;
        } else {
            limpiarError(campo);
        }
    });
    
    return esValido;
}

// Validar email
function validarEmail(campoEmail) {
    const patronEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (campoEmail.value && !patronEmail.test(campoEmail.value)) {
        mostrarError(campoEmail, configuracionValidacion.mensajes.emailInvalido);
        return false;
    } else {
        limpiarError(campoEmail);
        return true;
    }
}

// Validar contraseña
function validarContrasena(campoContrasena) {
    if (campoContrasena.value && campoContrasena.value.length < 8) {
        mostrarError(campoContrasena, configuracionValidacion.mensajes.contrasenaCorta);
        return false;
    } else {
        limpiarError(campoContrasena);
        return true;
    }
}

// Mostrar mensaje de error
function mostrarError(campo, mensaje) {
    limpiarError(campo);
    
    campo.classList.add('is-invalid');
    
    const mensajeError = document.createElement('div');
    mensajeError.className = 'invalid-feedback';
    mensajeError.textContent = mensaje;
    
    campo.parentNode.appendChild(mensajeError);
}

// Limpiar error
function limpiarError(campo) {
    campo.classList.remove('is-invalid');
    
    const mensajeAnterior = campo.parentNode.querySelector('.invalid-feedback');
    if (mensajeAnterior) {
        mensajeAnterior.remove();
    }
}
