document.addEventListener('DOMContentLoaded', function() {
    // =============================================
    // Controle dos horários de funcionamento
    // =============================================
    // Inicialização - desativa todos os períodos noturnos por padrão
    document.querySelectorAll('[data-periodo="noite"] i').forEach(icon => {
        icon.classList.replace('fa-toggle-on', 'fa-toggle-off');
        const inputs = icon.closest('.horario-noite').querySelectorAll('input[type="time"]');
        inputs.forEach(input => {
            input.disabled = true;
            input.value = '';
        });
    });

    // Toggle dos períodos
    document.querySelectorAll('.btn-toggle-horario').forEach(btn => {
        btn.addEventListener('click', function() {
            const icon = this.querySelector('i');
            const periodoContainer = this.closest('[class^="horario-"]');
            const inputs = periodoContainer.querySelectorAll('input[type="time"]');
            
            if (icon.classList.contains('fa-toggle-on')) {
                icon.classList.replace('fa-toggle-on', 'fa-toggle-off');
                inputs.forEach(input => {
                    input.disabled = true;
                    input.value = '';
                });
            } else {
                icon.classList.replace('fa-toggle-off', 'fa-toggle-on');
                inputs.forEach(input => input.disabled = false);
                
                // Define valores padrão se estiverem vazios
                inputs.forEach((input, index) => {
                    if (!input.value) {
                        input.value = index === 0 ? '08:00' : '12:00';
                    }
                });
            }
        });
    });

    // Validação antes do envio
    document.querySelector('form').addEventListener('submit', function(e) {
        let isValid = true;
        const diasAtivos = document.querySelectorAll('.horario-dia input[type="checkbox"]:checked');
        
        if (diasAtivos.length === 0) {
            alert('Selecione pelo menos um dia de funcionamento');
            isValid = false;
        } else {
            diasAtivos.forEach(dia => {
                const row = dia.closest('.horario-dia-row');
                const periodosAtivos = row.querySelectorAll('.btn-toggle-horario i.fa-toggle-on');
                
                if (periodosAtivos.length === 0) {
                    alert(`O dia ${dia.nextElementSibling.textContent.trim()} está ativo mas não tem períodos definidos`);
                    isValid = false;
                } else {
                    periodosAtivos.forEach(icon => {
                        const btn = icon.closest('.btn-toggle-horario');
                        const periodo = btn.closest('[class^="horario-"]');
                        const inicio = periodo.querySelector('input[type="time"]:first-child').value;
                        const fim = periodo.querySelector('input[type="time"]:last-child').value;
                        
                        if (!inicio || !fim) {
                            alert(`Preencha ambos os horários para ${dia.nextElementSibling.textContent.trim()} - ${btn.dataset.periodo}`);
                            isValid = false;
                        } else if (inicio >= fim) {
                            alert(`Horário inválido para ${dia.nextElementSibling.textContent.trim()} - ${btn.dataset.periodo} (início deve ser antes do fim)`);
                            isValid = false;
                        }
                    });
                }
            });
        }
        
        if (!isValid) {
            e.preventDefault();
        }
    });


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
            
            // Validação dos horários
            const diasAtivos = document.querySelectorAll('.horario-dia input[type="checkbox"]:checked');
            if (diasAtivos.length === 0) {
                alert('Selecione pelo menos um dia de funcionamento');
                isValid = false;
            } else {
                // Verifica se cada dia ativo tem pelo menos um período com horários válidos
                diasAtivos.forEach(dia => {
                    const row = dia.closest('.horario-dia-row');
                    const periodosAtivos = row.querySelectorAll('.btn-toggle-horario i.fa-toggle-on');
                    
                    if (periodosAtivos.length === 0) {
                        alert(`O dia ${dia.nextElementSibling.textContent.trim()} está ativo mas não tem períodos definidos`);
                        isValid = false;
                        return;
                    }
                    
                    // Verifica os horários de cada período ativo
                    periodosAtivos.forEach(icon => {
                        const btn = icon.closest('.btn-toggle-horario');
                        const diaNome = btn.dataset.dia;
                        const periodo = btn.dataset.periodo;
                        const inicio = document.querySelector(`input[name="${diaNome}_${periodo}_inicio"]`).value;
                        const fim = document.querySelector(`input[name="${diaNome}_${periodo}_fim"]`).value;
                        
                        if (!inicio || !fim) {
                            alert(`Preencha os horários para ${diaNome.replace('_', ' ')} - ${periodo}`);
                            isValid = false;
                        } else if (inicio >= fim) {
                            alert(`O horário de início deve ser anterior ao de fim para ${diaNome.replace('_', ' ')} - ${periodo}`);
                            isValid = false;
                        }
                    });
                });
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
});


// Funções para manipulação de serviços
let servicoCount = 1;

function adicionarServico() {
    const container = document.getElementById('servicosContainer');
    const novoItem = document.createElement('div');
    novoItem.className = 'servico-item';
    
    novoItem.innerHTML = `
        <div class="servico-field-group">
            <label>Nome do Serviço *</label>
            <input type="text" name="servicos[${servicoCount}][nome]" placeholder="Ex: Corte de Cabelo" required>
        </div>
        <div class="servico-field-group">
            <label>Preço (R$) *</label>
            <input type="number" name="servicos[${servicoCount}][preco]" placeholder="Ex: 50.00" min="0" step="0.01" required>
        </div>
        <div class="servico-field-group">
            <label>Descrição</label>
            <textarea name="servicos[${servicoCount}][descricao]" rows="2" placeholder="Descreva o serviço..."></textarea>
        </div>
        <button type="button" class="btn-remove-servico" onclick="removerServico(this)">
            <i class="fas fa-trash"></i>
        </button>
    `;
    
    container.appendChild(novoItem);
    servicoCount++;
}

function removerServico(botao) {
    const itens = document.querySelectorAll('.servico-item');
    if (itens.length > 1) {
        botao.closest('.servico-item').remove();
    } else {
        alert('Você deve ter pelo menos um serviço cadastrado');
    }
}

// Validação do formulário antes de enviar
document.querySelector('form').addEventListener('submit', function(e) {
    // Validação dos serviços
    const servicos = document.querySelectorAll('.servico-item');
    let servicosValidos = true;
    
    servicos.forEach(servico => {
        const nome = servico.querySelector('input[name*="[nome]"]').value;
        const preco = servico.querySelector('input[name*="[preco]"]').value;
        
        if (!nome || !preco) {
            servicosValidos = false;
            servico.style.border = '1px solid red';
        } else {
            servico.style.border = 'none';
        }
    });
    
    if (!servicosValidos) {
        e.preventDefault();
        alert('Preencha todos os campos obrigatórios dos serviços');
    }
});

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    // Garante que sempre tenha pelo menos um serviço
    if (document.querySelectorAll('.servico-item').length === 0) {
        adicionarServico();
    }
});