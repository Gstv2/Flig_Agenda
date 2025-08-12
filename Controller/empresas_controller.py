# controllers/empresas_controller.py
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from config import supabase
from Models.empresas import Empresas
from Models.auth import Auth
from Controller.auth_controller import login_required
import logging

empresas_bp = Blueprint('empresas', __name__)
logger = logging.getLogger(__name__)

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
            logger.error(f"Erro ao cadastrar empresa: {str(e)}")
            flash(f"Erro ao processar cadastro: {str(e)}", "error")

    return render_template('cadastrar_empresa.html', user=user)

@empresas_bp.route('/atualizar_banner/<int:empresa_id>', methods=['POST'])
@login_required
def atualizar_banner(empresa_id):
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400
    
    banner_url, erro = Empresas.upload_banner_empresa(file, empresa_id)
    if erro:
        return jsonify({"error": erro}), 500
    
    return jsonify({"banner_url": banner_url})

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
    return jsonify(empresa) if empresa else jsonify({"error": "Empresa não encontrada"}), 404

@empresas_bp.route('/buscar_empresa_categoria/<categoria>', methods=['GET'])  # Correção: incluir parâmetro na rota
def buscar_empresa_categoria(categoria):  # Renomeada para evitar confusão
    empresas = Empresas.buscar_empresa_categoria(categoria)
    print(empresas)
    return empresas