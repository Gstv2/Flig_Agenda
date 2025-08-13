from flask import Blueprint, jsonify, request, session, flash, redirect, url_for, render_template
from Models.servicos import Servico
from Controller.auth_controller import login_required
import logging

servicos_bp = Blueprint('servicos', __name__)
logger = logging.getLogger(__name__)

@servicos_bp.route('/servicos/empresa/<int:empresa_id>', methods=['POST'])
@login_required
def criar_servico(empresa_id):
    """Cria um novo serviço para a empresa"""
    try:
        dados = request.form.to_dict()  # agora pega dados do form
        if not dados:
            return jsonify({"error": "Dados não fornecidos"}), 400

        if not dados.get('nome') or not dados.get('preco'):
            flash("Nome e preço são obrigatórios!", "error")
            return redirect(url_for('dashboard_empresa', id_empresa=empresa_id))

        dados['empresa_id'] = empresa_id
        dados['preco'] = float(dados['preco'])  # garantir formato numérico

        novo_servico = Servico.criar_servico(dados)
        if novo_servico:
            flash("Serviço criado com sucesso!", "success")
        else:
            flash("Erro ao criar serviço", "error")

        return redirect(url_for('dashboard_empresa', id_empresa=empresa_id))

    except Exception as e:
        logger.error(f"Erro ao criar serviço: {str(e)}")
        flash("Erro interno no servidor", "error")
        return redirect(url_for('dashboard_empresa', id_empresa=empresa_id))

@servicos_bp.route('/servicos/empresa/<int:empresa_id>', methods=['GET'])
def listar_servicos(empresa_id):
    """Lista todos os serviços de uma empresa"""
    try:
        servicos = Servico.buscar_servicos_empresa(empresa_id)
        return servicos
    except Exception as e:
        logger.error(f"Erro ao listar serviços: {str(e)}")
        return jsonify({"error": "Erro ao buscar serviços"}), 500

@servicos_bp.route('/servicos/<int:servico_id>/editar', methods=['GET', 'POST'])
@login_required
def atualizar_servico(servico_id):
    if request.method == 'POST':
        dados = request.form.to_dict()
        servico_atualizado = Servico.atualizar_servico(servico_id, dados)
        flash("Serviço atualizado com sucesso!", "success")
        return redirect(url_for('dashboard_empresa', id_empresa=session.get('empresa_id')))
    servico = Servico.buscar_servico_por_id(servico_id)
    return redirect(url_for('dashboard_empresa', id_empresa=session.get('empresa_id')))

@servicos_bp.route('/servicos/<int:servico_id>/deletar', methods=['GET', 'POST'])
@login_required
def deletar_servico(servico_id):
    sucesso = Servico.deletar_servico(servico_id)
    if sucesso:
        print("Serviço excluído!", "success")
        return redirect(url_for('dashboard_empresa', id_empresa=session.get('empresa_id')))
    else:
        print("Serviço não encontrado.", "error")
    return redirect(url_for('dashboard_empresa', id_empresa=session.get('empresa_id')))