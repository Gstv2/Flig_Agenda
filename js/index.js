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

  // Alternar seleção do tipo de usuário no login
  const userTypeLabels = document.querySelectorAll('.user-type');
  userTypeLabels.forEach(label => {
    label.addEventListener('click', function() {
      userTypeLabels.forEach(l => l.classList.remove('selected'));
      this.classList.add('selected');
      // Marcar o input correspondente como checked
      const input = this.querySelector('input[type="radio"]');
      if (input) input.checked = true;
    });
  });

  // Tabs dinâmicas para salao_mock.html
  const tabButtons = document.querySelectorAll('.tabs-container .tab');
  const tabContents = {
    'Informações': document.getElementById('tab-info'),
    'Serviços': document.getElementById('tab-servicos'),
    'Avaliações': document.getElementById('tab-avaliacoes'),
    'Agendar': document.getElementById('tab-agendar')
  };
  tabButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      // Remove classe ativo de todos
      tabButtons.forEach(b => b.classList.remove('ativo'));
      this.classList.add('ativo');
      // Esconde todos os conteúdos
      Object.values(tabContents).forEach(div => div.style.display = 'none');
      // Mostra o conteúdo correspondente
      const label = this.textContent.trim();
      if(tabContents[label]) tabContents[label].style.display = '';
    });
  });
});