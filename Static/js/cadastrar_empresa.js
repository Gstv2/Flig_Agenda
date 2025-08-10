
document.addEventListener('DOMContentLoaded', function() {
    // Toggle dos períodos
    document.querySelectorAll('.btn-toggle-horario').forEach(btn => {
        btn.addEventListener('click', function() {
        const icon = this.querySelector('i');
        const periodo = this.parentElement;
        const inputs = periodo.querySelectorAll('input[type="time"]');
        
        if (icon.classList.contains('fa-toggle-on')) {
            icon.classList.replace('fa-toggle-on', 'fa-toggle-off');
            inputs.forEach(input => input.disabled = true);
        } else {
            icon.classList.replace('fa-toggle-off', 'fa-toggle-on');
            inputs.forEach(input => input.disabled = false);
        }
        });
    });

    document.querySelectorAll('[data-periodo="noite"]').forEach(btn => {
        const icon = btn.querySelector('i');
        const periodo = btn.parentElement;
        const inputs = periodo.querySelectorAll('input[type="time"]');
        inputs.forEach(input => input.disabled = true);
        });

    // Fechado checkbox
    document.querySelectorAll('.horario-dia input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
        const row = this.closest('.horario-dia-row');
        const inputs = row.querySelectorAll('input[type="time"]');
        const toggles = row.querySelectorAll('.btn-toggle-horario i');
        
        if (!this.checked) {
            inputs.forEach(input => input.disabled = true);
            toggles.forEach(toggle => {
            toggle.classList.replace('fa-toggle-on', 'fa-toggle-off');
            });
        } else {
            inputs.forEach(input => input.disabled = false);
            toggles.forEach(toggle => {
            toggle.classList.replace('fa-toggle-off', 'fa-toggle-on');
            });
        }
        });
    });
});
  // Máscaras para os campos
  document.addEventListener('DOMContentLoaded', function() {
    // Máscara para CNPJ
    const cnpjInput = document.querySelector('input[name="cnpj"]');
    cnpjInput.addEventListener('input', function(e) {
      let value = e.target.value.replace(/\D/g, '');
      
      if (value.length > 14) {
        value = value.substring(0, 14);
      }
      
      // Aplica a máscara: 00.000.000/0000-00
      if (value.length > 2) {
        value = value.replace(/^(\d{2})/, '$1.');
      }
      if (value.length > 6) {
        value = value.replace(/^(\d{2})\.(\d{3})/, '$1.$2.');
      }
      if (value.length > 10) {
        value = value.replace(/^(\d{2})\.(\d{3})\.(\d{3})/, '$1.$2.$3/');
      }
      if (value.length > 15) {
        value = value.replace(/^(\d{2})\.(\d{3})\.(\d{3})\/(\d{4})/, '$1.$2.$3/$4-');
      }
      
      e.target.value = value;
    });
    
    // Máscara para telefone
    const telefoneInput = document.querySelector('input[name="telefone"]');
    telefoneInput.addEventListener('input', function(e) {
      let value = e.target.value.replace(/\D/g, '');
      
      if (value.length > 11) {
        value = value.substring(0, 11);
      }
      
      // Aplica a máscara: (00) 00000-0000 ou (00) 0000-0000
      if (value.length > 0) {
        value = value.replace(/^(\d{0,2})/, '($1');
      }
      if (value.length > 3) {
        value = value.replace(/^(\(\d{2})/, '$1) ');
      }
      if (value.length > 10) {
        value = value.replace(/^(\(\d{2}\))\s(\d{5})/, '$1 $2-');
      } else if (value.length > 9) {
        value = value.replace(/^(\(\d{2}\))\s(\d{4})/, '$1 $2-');
      }
      
      e.target.value = value;
    });
    
    // Máscara para CPF
    const cpfInput = document.querySelector('input[name="cpf_responsavel"]');
    cpfInput.addEventListener('input', function(e) {
      let value = e.target.value.replace(/\D/g, '');
      
      if (value.length > 11) {
        value = value.substring(0, 11);
      }
      
      // Aplica a máscara: 000.000.000-00
      if (value.length > 3) {
        value = value.replace(/^(\d{3})/, '$1.');
      }
      if (value.length > 7) {
        value = value.replace(/^(\d{3})\.(\d{3})/, '$1.$2.');
      }
      if (value.length > 11) {
        value = value.replace(/^(\d{3})\.(\d{3})\.(\d{3})/, '$1.$2.$3-');
      }
      
      e.target.value = value;
    });
    
    // Validação antes do envio do formulário
    const form = document.querySelector('.cadastrar-empresa-form');
    form.addEventListener('submit', function(e) {
      // Valida CNPJ (deve ter 14 dígitos)
      const cnpjValue = cnpjInput.value.replace(/\D/g, '');
      if (cnpjValue.length !== 14) {
        alert('CNPJ deve conter 14 dígitos');
        e.preventDefault();
        return;
      }
      
      // Valida telefone (deve ter 10 ou 11 dígitos)
      const telefoneValue = telefoneInput.value.replace(/\D/g, '');
      if (telefoneValue.length < 10 || telefoneValue.length > 11) {
        alert('Telefone deve conter 10 ou 11 dígitos');
        e.preventDefault();
        return;
      }
      
      // Valida CPF (deve ter 11 dígitos)
      const cpfValue = cpfInput.value.replace(/\D/g, '');
      if (cpfValue.length !== 11) {
        alert('CPF deve conter 11 dígitos');
        e.preventDefault();
        return;
      }
    });
  });


// static/js/cadastrar_empresa.js
document.addEventListener('DOMContentLoaded', function() {
    const bannerInput = document.getElementById('bannerInput');
    const bannerPreview = document.getElementById('bannerPreview');
    const previewImage = document.getElementById('previewImage');
    const bannerDropzone = document.getElementById('bannerDropzone');

    // Preview da imagem selecionada
    bannerInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                bannerPreview.style.display = 'block';
            }
            
            reader.readAsDataURL(file);
        }
    });

    // Drag and drop
    bannerDropzone.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('dragover');
    });

    bannerDropzone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
    });

    bannerDropzone.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
        
        if (e.dataTransfer.files.length) {
            bannerInput.files = e.dataTransfer.files;
            const event = new Event('change');
            bannerInput.dispatchEvent(event);
        }
    });
});
