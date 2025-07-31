from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from Models.estabelecimentos import Estabelecimento
from Controller.auth_controller import login_required

estabelecimento_bp = Blueprint('estabelecimento', __name__)

@estabelecimento_bp.route('/cadastrar_empresa', methods=['GET', 'POST'])
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
            resultado = Estabelecimento.criar_empresas(dados_empresa)
            if resultado:
                flash("Estabelecimento cadastrado com sucesso!", "success")
                return redirect(url_for('minhas_empresas'))  # Use url_for corretamente
            else:
                flash("Erro ao cadastrar estabelecimento.", "error")
        except Exception as e:
            flash(f"Erro inesperado: {e}", "error")

    return render_template('cadastrar_empresa.html')

@estabelecimento_bp.route('/buscar_empresas', methods=['GET'])
@login_required
def buscar_empresas():
    estabelecimentos = Estabelecimento.buscar_empresas()
    return estabelecimentos

