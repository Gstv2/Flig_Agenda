from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from Models.empresas import Empresas
from Controller.auth_controller import login_required

empresas_bp = Blueprint('empresas', __name__)

@empresas_bp.route('/cadastrar_empresa', methods=['GET', 'POST'])
@login_required
def cadastrar_empresa():
    if request.method == 'POST':
        nome_fantasia = request.form.get('nome_fantasia')
        cnpj = request.form.get('cnpj')
        descricao = request.form.get('descricao')
        endereco = request.form.get('endereco')
        telefone = request.form.get('telefone')
        usuario_id = session['user']['id']

        dados_empresa = {
            "usuario_id": usuario_id,
            "nome_fantasia": nome_fantasia,
            "cnpj": cnpj,
            "descricao": descricao,
            "endereco": endereco,
            "telefone": telefone
        }

        print("Dados recebidos do formulário:", dados_empresa)  # Debug

        try:
            resultado = Empresas.criar_empresas(dados_empresa)
            if resultado:
                flash("Estabelecimento cadastrado com sucesso!", "success")
                return redirect(url_for('minhas_empresas'))  # Use url_for corretamente
            else:
                flash("Erro ao cadastrar estabelecimento.", "error")
        except Exception as e:
            flash(f"Erro inesperado: {e}", "error")

    return render_template('cadastrar_empresa.html')

# Rotas corrigidas:
@empresas_bp.route('/buscar_empresas', methods=['GET'])
@login_required
def buscar_empresas():
    empresas = Empresas.buscar_empresas()  # Nota: Esta função não está definida no código mostrado
    return empresas

@empresas_bp.route('/buscar_empresa_id/<int:id>', methods=['GET'])  # Correção: incluir parâmetro na rota
@login_required
def buscar_empresa_id(id):  # Renomeada para evitar confusão
    empresa = Empresas.buscar_empresa_id(id)
    print(empresa)
    return empresa

@empresas_bp.route('/buscar_empresa_id_usuario/<int:id_usuario>', methods=['GET'])  # Correção: incluir parâmetro na rota
@login_required
def buscar_empresa_por_id(id_usuario):  # Renomeada para evitar confusão
    empresa = Empresas.buscar_empresas_por_usuario(id_usuario)
    return jsonify(empresa) if empresa else jsonify({"error": "Empresa não encontrada"}), 404