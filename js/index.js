/**
 * Scripts principais do site Piripiri
 * Gerencia a funcionalidade do sidebar e outras interações
 */

/**
 * Abre o menu lateral (sidebar)
 * Adiciona as classes 'active' aos elementos sidebar e overlay
 */
function abrirMenu() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('overlay');
  
  if (sidebar && overlay) {
    sidebar.classList.add('active');
    overlay.classList.add('active');
    
    // Previne scroll do body quando sidebar está aberto
    document.body.style.overflow = 'hidden';
  }
}

/**
 * Fecha o menu lateral (sidebar)
 * Remove as classes 'active' dos elementos sidebar e overlay
 */
function fecharMenu() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('overlay');
  
  if (sidebar && overlay) {
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
    
    // Restaura scroll do body
    document.body.style.overflow = '';
  }
}

/**
 * Fecha o sidebar quando uma tecla é pressionada
 * @param {KeyboardEvent} event - Evento de tecla
 */
function handleKeyPress(event) {
  if (event.key === 'Escape') {
    fecharMenu();
  }
}

/**
 * Inicializa os event listeners quando o DOM estiver carregado
 */
document.addEventListener('DOMContentLoaded', function() {
  // Adiciona listener para tecla ESC
  document.addEventListener('keydown', handleKeyPress);
  
  // Adiciona listener para clique no overlay
  const overlay = document.getElementById('overlay');
  if (overlay) {
    overlay.addEventListener('click', fecharMenu);
  }
  
  // Adiciona listeners para botões de fechar
  const closeButtons = document.querySelectorAll('.close-btn');
  closeButtons.forEach(button => {
    button.addEventListener('click', fecharMenu);
  });
});