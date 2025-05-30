// Asegurar que el DOM esté cargado
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScrolls);
} else {
    initScrolls();
}

function initScrolls() {
    // Inicializar scroll para productos destacados
    initializeProductScroll('destacados');
    
    // Inicializar scroll para productos recientes
    initializeProductScroll('recientes');
}

function initializeProductScroll(sectionId) {
    const container = document.getElementById(`productos-${sectionId}`);
    
    if (!container) {
        return;
    }
    
    const scrollContainer = container.querySelector('.productos-scroll');
    const leftBtn = container.querySelector('.scroll-btn-left');
    const rightBtn = container.querySelector('.scroll-btn-right');
    
    if (!scrollContainer || !leftBtn || !rightBtn) {
        return;
    }

    // Configurar eventos de los botones
    leftBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        scrollContainer.scrollBy({
            left: -300,
            behavior: 'smooth'
        });
    });
    
    rightBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        scrollContainer.scrollBy({
            left: 300,
            behavior: 'smooth'
        });
    });
    
    // Mostrar/ocultar botones según la posición del scroll
    function updateScrollButtons() {
        const scrollLeft = scrollContainer.scrollLeft;
        const scrollWidth = scrollContainer.scrollWidth;
        const clientWidth = scrollContainer.clientWidth;
        
        // Solo mostrar botones si hay overflow
        if (scrollWidth <= clientWidth) {
            leftBtn.style.display = 'none';
            rightBtn.style.display = 'none';
            return;
        } else {
            leftBtn.style.display = 'flex';
            rightBtn.style.display = 'flex';
        }
        
        // Actualizar estado del botón izquierdo
        if (scrollLeft <= 0) {
            leftBtn.style.opacity = '0.3';
            leftBtn.style.pointerEvents = 'none';
        } else {
            leftBtn.style.opacity = '0.8';
            leftBtn.style.pointerEvents = 'auto';
        }
        
        // Actualizar estado del botón derecho
        const atEnd = scrollLeft >= (scrollWidth - clientWidth - 10);
        if (atEnd) {
            rightBtn.style.opacity = '0.3';
            rightBtn.style.pointerEvents = 'none';
        } else {
            rightBtn.style.opacity = '0.8';
            rightBtn.style.pointerEvents = 'auto';
        }
    }
    
    // Actualizar botones cuando se hace scroll
    scrollContainer.addEventListener('scroll', updateScrollButtons);
    
    // Actualizar botones inicialmente con un pequeño delay
    setTimeout(() => {
        updateScrollButtons();
    }, 100);
    
    // Actualizar botones cuando se redimensiona la ventana
    window.addEventListener('resize', () => {
        setTimeout(updateScrollButtons, 100);
    });
    
    // Agregar soporte para arrastrar en dispositivos móviles
    let isDown = false;
    let startX;
    let scrollLeftStart;

    scrollContainer.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.pageX - scrollContainer.offsetLeft;
        scrollLeftStart = scrollContainer.scrollLeft;
    });

    scrollContainer.addEventListener('mouseleave', () => {
        isDown = false;
    });

    scrollContainer.addEventListener('mouseup', () => {
        isDown = false;
    });

    scrollContainer.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - scrollContainer.offsetLeft;
        const walk = (x - startX) * 2;
        scrollContainer.scrollLeft = scrollLeftStart - walk;
    });
}
