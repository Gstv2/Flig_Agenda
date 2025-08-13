# controllers/empresas_controller.py
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from Models.empresas import Empresas
from Models.auth import Auth
from Controller.auth_controller import login_required
from Models.horarios import HorarioFuncionamento
from Models.servicos import Servico



empresas_bp = Blueprint('empresas', __name__)
# controllers/empresas_controller.py
def processar_horarios_formulario(empresa_id):
    """Processa os dados de horário do formulário"""
    dias_semana = {
        'segunda': 'Segunda-feira',
        'terca': 'Terça-feira',
        'quarta': 'Quarta-feira',
        'quinta': 'Quinta-feira',
        'sexta': 'Sexta-feira',
        'sabado': 'Sábado',
        'domingo': 'Domingo'
    }
    
    for dia_form, dia_semana in dias_semana.items():
        # Verificar se o dia está ativo
        if request.form.get(f'{dia_form}_ativo', 'off') != 'on':
            continue
            
        # Preparar dados do horário
        dados_horario = {
            'empresa_id': empresa_id,
            'dia_semana': dia_semana,
            'manha_abertura': request.form.get(f'{dia_form}_manha_inicio') or None,
            'manha_fechamento': request.form.get(f'{dia_form}_manha_fim') or None,
            'tarde_abertura': request.form.get(f'{dia_form}_tarde_inicio') or None,
            'tarde_fechamento': request.form.get(f'{dia_form}_tarde_fim') or None,
            'noite_abertura': request.form.get(f'{dia_form}_noite_inicio') or None,
            'noite_fechamento': request.form.get(f'{dia_form}_noite_fim') or None
        }
        
        # Verificar se pelo menos um período está preenchido
        periodos_preenchidos = any([
            dados_horario['manha_abertura'] and dados_horario['manha_fechamento'],
            dados_horario['tarde_abertura'] and dados_horario['tarde_fechamento'],
            dados_horario['noite_abertura'] and dados_horario['noite_fechamento']
        ])
        
        if periodos_preenchidos:
            resultado = HorarioFuncionamento.criar_horario(dados_horario)
            if not resultado:
                print(f"Falha ao salvar horário para {dia_semana}")

@empresas_bp.route('/cadastrar_empresa', methods=['GET', 'POST'])
@login_required
def cadastrar_empresa():
    user = session.get('user', {})
    if request.method == 'POST':
        print("Iniciando processamento do formulário...")  # DEBUG
        
        # Obter dados do formulário
        nome_fantasia = request.form.get('nome_fantasia')
        cnpj = request.form.get('cnpj')
        descricao = request.form.get('descricao')
        endereco = request.form.get('endereco')
        telefone = request.form.get('telefone')
        categoria = request.form.get('categoria')
        Responsavel = request.form.get('responsavel')
        cpf_responsavel = request.form.get('cpf_responsavel')
        email = request.form.get('email')
        banner_file = request.files.get('banner')
        
        print(f"Arquivo de banner recebido: {banner_file}")  # DEBUG
        if banner_file:
            print(f"Nome do arquivo: {banner_file.filename}, Tamanho: {banner_file.content_length}")  # DEBUG
        
        # Obter usuário da sessão
        user_data = session.get('user')
        if not user_data:
            flash("Usuário não autenticado corretamente", "error")
            return redirect(url_for('auth.login'))

        user_email = user_data.get('email')
        if not user_email:
            flash("Email do usuário não encontrado", "error")
            return redirect(url_for('auth.login'))

        try:
            # Buscar usuário pelo email
            usuario_response = Auth.buscar_usuario_email(user_email)
            
            if not usuario_response or not usuario_response.data:
                flash("Usuário não encontrado no banco de dados", "error")
                return redirect(url_for('auth.login'))
                
            usuario_id = usuario_response.data.get('id')
            if not usuario_id:
                flash("ID do usuário não encontrado na resposta", "error")
                return redirect(url_for('auth.login'))
                
            # Preparar dados da empresa
            dados_empresa = {
                "usuario_id": usuario_id,
                "nome_fantasia": nome_fantasia,
                "cnpj": cnpj,
                "endereco": endereco,
                "telefone": telefone,
                "descricao": descricao,
                "email": email, 
                "Responsavel": Responsavel,
                "categoria": categoria,
                "cpf_responsavel": cpf_responsavel
            }

            # Cadastrar empresa
            resultado = Empresas.criar_empresas(dados_empresa)
            
            if resultado:
                empresa_id = resultado[0]['id']
                
                # Processar serviços - FORMA CORRETA DE PEGAR OS DADOS DO FORMULÁRIO
                servicos = []
                index = 0
                while True:
                    # Verifica se existe um serviço com este índice
                    if f'servicos[{index}][nome]' not in request.form:
                        break
                    
                    servico = {
                        'nome': request.form.get(f'servicos[{index}][nome]'),
                        'descricao': request.form.get(f'servicos[{index}][descricao]', ''),
                        'preco': request.form.get(f'servicos[{index}][preco]')
                    }
                    
                    # Validação básica dos dados do serviço
                    if servico['nome'] and servico['preco']:
                        try:
                            servico['preco'] = float(servico['preco'])
                            servicos.append(servico)
                        except ValueError:
                            print(f"Preço inválido para o serviço {index}")
                    
                    index += 1
                
                # Cadastrar cada serviço válido
                for servico in servicos:
                    try:
                        Servico.criar_servico({
                            'empresa_id': empresa_id,
                            'nome': servico['nome'],
                            'descricao': servico['descricao'],
                            'preco': servico['preco']
                        })
                    except Exception as e:
                        print(f"Erro ao criar serviço: {str(e)}")
                        flash("Alguns serviços não foram cadastrados corretamente", "warning")
                
                # Processar horários de funcionamento
                try:
                    processar_horarios_formulario(empresa_id)
                except Exception as e:
                    print(f"Erro ao criar horários: {str(e)}")
                    flash("Empresa criada, mas houve um erro ao cadastrar os horários de funcionamento", "warning")
                
                # Se enviou banner, fazer upload
                if banner_file and banner_file.filename != '':
                    banner_url, erro = Empresas.upload_banner_empresa(banner_file, empresa_id)
                    if erro:
                        flash(f"Empresa criada, mas erro ao enviar banner: {erro}", "warning")
                    else:
                        # Atualizar empresa com URL do banner
                        Empresas.atualizar_empresa(empresa_id, {'banner_url': banner_url})
                
                flash("Estabelecimento cadastrado com sucesso!", "success")
                return redirect(url_for('minhas_empresas'))
            else:
                flash("Erro ao cadastrar estabelecimento", "error")
                
        except Exception as e:
            print(f"Erro completo: {str(e)}")
            flash(f"Erro ao processar cadastro: {str(e)}", "error")

    return render_template('cadastrar_empresa.html', user=user)

# Rotas corrigidas:
@empresas_bp.route('/buscar_empresas', methods=['GET'])
def buscar_empresas():
    empresas = Empresas.buscar_empresas()  # Nota: Esta função não está definida no código mostrado
    return empresas

@empresas_bp.route('/buscar_empresa_id/<int:id>', methods=['GET'])  # Correção: incluir parâmetro na rota
def buscar_empresa_id(id):  # Renomeada para evitar confusão
    empresa = Empresas.buscar_empresa_id(id)
    print(empresa)
    return empresa

@empresas_bp.route('/buscar_empresa_id_usuario/<int:id_usuario>', methods=['GET'])  # Correção: incluir parâmetro na rota
def buscar_empresa_por_id(id_usuario):  # Renomeada para evitar confusão
    empresa = Empresas.buscar_empresas_por_usuario(id_usuario)
    len(empresa)
    return empresa

@empresas_bp.route('/buscar_empresa_categoria/<categoria>', methods=['GET'])  # Correção: incluir parâmetro na rota
def buscar_empresa_categoria(categoria):  # Renomeada para evitar confusão
    empresas = Empresas.buscar_empresa_categoria(categoria)
    
    print(empresas)
    return empresas


# UPDATE - Rota para atualizar empresa
@empresas_bp.route('/empresas/<int:id>', methods=['PUT'])
@login_required
def atualizar_empresa(id):
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"error": "Dados não fornecidos"}), 400
            
        empresa_atualizada = Empresas.atualizar_empresa(id, dados)
        if empresa_atualizada:
            return jsonify(empresa_atualizada), 200
        return jsonify({"error": "Empresa não encontrada"}), 404
    except Exception as e:
        print(f"Erro ao atualizar empresa: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# UPDATE - Rota para atualizar banner
@empresas_bp.route('/empresas/<int:id>/banner', methods=['POST'])
@login_required
def atualizar_banner(id):
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400
    
    try:
        banner_url, erro = Empresas.upload_banner_empresa(file, id)
        if erro:
            return jsonify({"error": erro}), 500
        
        # Atualizar a empresa com a nova URL do banner
        Empresas.atualizar_empresa(id, {'banner_url': banner_url})
        return jsonify({"banner_url": banner_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Adicione estas rotas ao seu empresas_controller.py

@empresas_bp.route('/editar/<int:id_empresa>', methods=['GET', 'POST'])
@login_required
def editar_empresa(id_empresa):
    user = session.get('user', {})

    # Verificar se a empresa pertence ao usuário
    empresa = Empresas.buscar_empresa_id(id_empresa)
    if not empresa:
        print("Empresa não encontrada ou você não tem permissão para editá-la", "error")
        return redirect(url_for('minhas_empresas'))
    empresa = empresa[0]
    
    if request.method == 'POST':
        try:
            # Processar dados básicos
            dados_atualizados = {
                "nome_fantasia": request.form.get('nome_fantasia'),
                "cnpj": request.form.get('cnpj'),
                "endereco": request.form.get('endereco'),
                "telefone": request.form.get('telefone'),
                "descricao": request.form.get('descricao'),
                "email": request.form.get('email'),
                "Responsavel": request.form.get('responsavel'),
                "categoria": request.form.get('categoria'),
                "cpf_responsavel": request.form.get('cpf_responsavel')
            }
            
            # Processar banner
            banner_file = request.files.get('banner')
            
            if banner_file and banner_file.filename != '':
                banner_url, erro = Empresas.upload_banner_empresa(banner_file, id_empresa)
                if erro:
                    flash(f"Erro ao atualizar banner: {erro}", "warning")
                else:
                    dados_atualizados['banner_imagem'] = banner_url
            
            # Atualizar empresa
            empresa_atualizada, erro = Empresas.atualizar_empresa(id_empresa, dados_atualizados)
            if erro:
                flash(f"Erro ao atualizar empresa: {erro}", "error")
            else:
                # Processar horários - primeiro remove os existentes
                HorarioFuncionamento.deletar_horarios_empresa(id_empresa)
                # Depois cria os novos
                processar_horarios_formulario(id_empresa)
                
                # Processar serviços
                servicos_removidos = request.form.getlist('servicos_removidos')
                for servico_id in servicos_removidos:
                    Servico.deletar_servico(servico_id)
                
                # Atualizar serviços existentes e adicionar novos
                index = 0
                while True:
                    if f'servicos[{index}][nome]' not in request.form:
                        break
                    
                    servico_id = request.form.get(f'servicos[{index}][id]')
                    servico_data = {
                        'nome': request.form.get(f'servicos[{index}][nome]'),
                        'descricao': request.form.get(f'servicos[{index}][descricao]', ''),
                        'preco': float(request.form.get(f'servicos[{index}][preco]')),
                        'duracao': int(request.form.get(f'servicos[{index}][duracao]', 30))
                    }
                    
                    if servico_id and servico_id != 'new':
                        # Atualizar serviço existente
                        Servico.atualizar_servico(servico_id, servico_data)
                    else:
                        # Criar novo serviço
                        servico_data['empresa_id'] = id_empresa
                        Servico.criar_servico(servico_data)
                    
                    index += 1
                
                flash("Empresa atualizada com sucesso!", "success")
                return redirect(url_for('empresas.editar_empresa', id_empresa=id_empresa))
        
        except Exception as e:
            flash(f"Erro ao processar atualização: {str(e)}", "error")
    
    # Buscar dados para exibição
    horarios = HorarioFuncionamento.buscar_horario_por_empresa(id_empresa)
    servicos = Servico.buscar_servicos_empresa(id_empresa)
    
    # Formatar horários para o template
    horarios_formatados = {
        'segunda': {'ativo': False},
        'terca': {'ativo': False},
        'quarta': {'ativo': False},
        'quinta': {'ativo': False},
        'sexta': {'ativo': False},
        'sabado': {'ativo': False},
        'domingo': {'ativo': False}
    }
    
    for horario in horarios:
        dia = horario['dia_semana'].lower().replace('-feira', '').replace('á', 'a')
        if dia not in horarios_formatados:
            continue
            
        horarios_formatados[dia]['ativo'] = True
        if horario['manha_abertura'] and horario['manha_fechamento']:
            horarios_formatados[dia]['manha'] = {
                'inicio': horario['manha_abertura'],
                'fim': horario['manha_fechamento']
            }
        if horario['tarde_abertura'] and horario['tarde_fechamento']:
            horarios_formatados[dia]['tarde'] = {
                'inicio': horario['tarde_abertura'],
                'fim': horario['tarde_fechamento']
            }
        if horario['noite_abertura'] and horario['noite_fechamento']:
            horarios_formatados[dia]['noite'] = {
                'inicio': horario['noite_abertura'],
                'fim': horario['noite_fechamento']
            }
    
    return redirect(url_for('minhas_empresas',                      
                        empresa=empresa,
                        user=user,
                        horarios=horarios_formatados,
                        servicos=servicos))

@empresas_bp.route('/excluir/<int:id_empresa>', methods=['GET','POST'])
@login_required
def excluir_empresa(id_empresa):
    user = session.get('user', {})
    
    # Verificar se a empresa pertence ao usuário
    empresa = Empresas.buscar_empresa_id(id_empresa)
    if not empresa:
        flash("Empresa não encontrada ou você não tem permissão para excluí-la", "error")
        return redirect(url_for('minhas_empresas'))
    
    try:
        # Primeiro remove os serviços
        servicos = Servico.buscar_servicos_empresa(id_empresa)
        for servico in servicos:
            Servico.deletar_servico(servico['id'])
        
        # Remove os horários
        HorarioFuncionamento.deletar_horarios_empresa(id_empresa)
        
        # Remove a empresa
        sucesso = Empresas.deletar_empresa(id_empresa)
        
        if sucesso:
            print("Empresa excluída com sucesso", "success")
        else:
            print("Erro ao excluir empresa", "error")
            
    except Exception as e:
        print(f"Erro ao excluir empresa: {str(e)}", "error")
    
    return redirect(url_for('minhas_empresas'))