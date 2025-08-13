document.addEventListener('DOMContentLoaded', function() {
    // =============================================
    // Máscaras para os campos
    // =============================================
    
    // Máscara para CNPJ
    const cnpjInput = document.querySelector('input[name="cnpj"]');
    if (cnpjInput) {
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
    }
    
    // Máscara para telefone
    const telefoneInput = document.querySelector('input[name="telefone"]');
    if (telefoneInput) {
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
    }
    
    // Máscara para CPF
    const cpfInput = document.querySelector('input[name="cpf_responsavel"]');
    if (cpfInput) {
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
    }
    
    // =============================================
    // Upload do banner
    // =============================================
    const bannerInput = document.getElementById('bannerInput');
    const bannerPreview = document.getElementById('bannerPreview');
    const previewImage = document.getElementById('previewImage');
    const bannerDropzone = document.getElementById('bannerDropzone');

    if (bannerInput && bannerPreview && previewImage && bannerDropzone) {
        // Preview da imagem selecionada
        bannerInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                // Verifica o tipo e tamanho do arquivo
                const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
                const maxSize = 5 * 1024 * 1024; // 5MB
                
                if (!validTypes.includes(file.type)) {
                    alert('Por favor, selecione uma imagem no formato JPG, PNG ou GIF.');
                    return;
                }
                
                if (file.size > maxSize) {
                    alert('A imagem deve ter no máximo 5MB.');
                    return;
                }
                
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
    }

    // =============================================
    // Validação do formulário
    // =============================================
    const form = document.querySelector('.cadastrar-empresa-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Valida CNPJ (deve ter 14 dígitos)
            if (cnpjInput) {
                const cnpjValue = cnpjInput.value.replace(/\D/g, '');
                if (cnpjValue.length !== 14) {
                    alert('CNPJ deve conter 14 dígitos');
                    isValid = false;
                }
            }
            
            // Valida telefone (deve ter 10 ou 11 dígitos)
            if (telefoneInput) {
                const telefoneValue = telefoneInput.value.replace(/\D/g, '');
                if (telefoneValue.length < 10 || telefoneValue.length > 11) {
                    alert('Telefone deve conter 10 ou 11 dígitos');
                    isValid = false;
                }
            }
            
            // Valida CPF (deve ter 11 dígitos)
            if (cpfInput) {
                const cpfValue = cpfInput.value.replace(/\D/g, '');
                if (cpfValue.length !== 11) {
                    alert('CPF deve conter 11 dígitos');
                    isValid = false;
                }
            }
        });
    }
});
